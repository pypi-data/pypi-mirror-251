import json
import pickle
from concurrent.futures import ThreadPoolExecutor, as_completed

import pkg_resources
import torch
from flair.data import Sentence
from flair.models import SequenceTagger
from transformers import AutoModelForTokenClassification, AutoTokenizer
from .tweet_level import TweetProcessor

from HanTa import HanoverTagger as ht


class Executor(TweetProcessor):
    def __init__(self):

        self.data = pickle.load(open(pkg_resources.resource_filename('tongueswitcher', "data/dictionaries.pkl"), "rb"))
        self.bigrams = self.open_json(pkg_resources.resource_filename('tongueswitcher', "data/combined_bigrams.json"))
        self.clh_pos_tags = self.open_json(pkg_resources.resource_filename('tongueswitcher', "data/clh_pos_editted.json"))

        self.mixed_tagger = ht.HanoverTagger(pkg_resources.resource_filename('tongueswitcher', 'data/morphmodel_geren.pgz'))
        self.en_tagger = ht.HanoverTagger(pkg_resources.resource_filename('tongueswitcher', 'data/morphmodel_en.pgz'))
        self.de_tagger = ht.HanoverTagger(pkg_resources.resource_filename('tongueswitcher', 'data/morphmodel_ger.pgz'))

        self.flair_tagger = SequenceTagger.load("flair/upos-multi")

        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

        ner_model_name = "igorsterner/german-english-roberta-base-binary-ner"
        self.ner_tokenizer = AutoTokenizer.from_pretrained(ner_model_name, add_prefix_space=True)
        self.ner_model = AutoModelForTokenClassification.from_pretrained(ner_model_name).to(self.device)

    def process_tweet(self, sentence, id_num):

        words_processed = [{"token": token.text, "lan": "U", "pos": token.get_label("upos").value} for token in sentence]
        full_anno = self.detect(words_processed, sentence.text)
        return full_anno, sentence, id_num


    def tongueswitcher_detect(self, sentences):

        sentences = [Sentence(sentence) for sentence in sentences]

        self.flair_tagger.predict(sentences, mini_batch_size=256)
        
        with ThreadPoolExecutor() as executor:
            full_annos = {}
            futures = {executor.submit(self.process_tweet, sentence, id_num) for id_num, sentence in enumerate(sentences)}
            for future in as_completed(futures):
                id_num = future.result()[2]
                full_annos[id_num] = future.result()[0]
        
        full_annos = self.batch_and_add_ner_labels(full_annos)

        return list(full_annos.values())


    def batch_and_add_ner_labels(self, full_annos):

        batch_size = 256

        full_annos_items = list(full_annos.items())
        num_batches = len(full_annos_items) // batch_size + (len(full_annos_items) % batch_size > 0)

        batches = [dict() for _ in range(num_batches)]

        for i, (key, value) in enumerate(full_annos_items):
            batch_index = i // batch_size
            batches[batch_index][key] = value     

        for batch in batches:
            
            words_batch = [[token["token"] for token in t] for t in batch.values()]
            id_nums = [t for t in batch.keys()]

            ner_labels = self.get_ner_token_labels(words_batch)

            for i in range(len(batch)):
                for j in range(len(words_batch[i])):
                    if ner_labels[i][j] == "I":
                        full_annos[id_nums[i]][j]["lan"] = "NE." + full_annos[id_nums[i]][j]["lan"]
        
        return full_annos

    @staticmethod
    def most_frequent(lst):

        if len(lst) == 0:
            return "Other"

        freqs = {}
        most_seen = None
        max_freq = -1

        for item in lst:
            freq = freqs.get(item, 0)
            freq += 1
            freqs[item] = freq

            if freq > max_freq:
                most_seen = item
                max_freq = freq

        return most_seen

    def get_ner_token_labels(self, words_batch):

        subword_inputs = self.ner_tokenizer(
            words_batch, truncation=True, is_split_into_words=True, return_tensors="pt", padding=True
        ).to(self.device)

        with torch.no_grad():
            logits = self.ner_model(**subword_inputs).logits

        predictions = torch.argmax(logits, dim=2)

        batch_predicted_word_labels = []

        for i in range(len(words_batch)):

            subword2word = subword_inputs.word_ids(batch_index=i)

            predicted_subword_labels = [self.ner_model.config.id2label[t.item()] for t in predictions[i]]

            predicted_word_labels = [[] for _ in range(len(words_batch[i]))]

            for idx, predicted_subword_label in enumerate(predicted_subword_labels):
                if subword2word[idx] is None:
                    continue
                else:
                    if predicted_subword_label != "O":
                        predicted_subword_label = "I"
                    predicted_word_labels[subword2word[idx]].append(predicted_subword_label)

            predicted_word_labels = [
                self.most_frequent(sublist) for sublist in predicted_word_labels
            ]

            batch_predicted_word_labels.append(predicted_word_labels)

        return batch_predicted_word_labels

    @staticmethod
    def open_json(file_name):
        with open(file_name, "r", encoding='utf-8') as f:
            return json.load(f)