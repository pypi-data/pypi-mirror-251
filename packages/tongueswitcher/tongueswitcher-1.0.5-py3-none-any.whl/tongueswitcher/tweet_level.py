from .word_level import WordProcessor


class TweetProcessor(WordProcessor):
    def __init__(self):
        pass


    def detect(self, annotated_words, tweet):

        annotated_words = self.combine_hashtags(annotated_words, tweet)

        annotated_words_ts = self.word_processor(annotated_words)

        if not annotated_words_ts:
            return annotated_words
        elif sum([1 for i in annotated_words_ts if i["lan"] == "U"]) / len(annotated_words) > 0.5:
            return annotated_words
        else:
            annotated_words = annotated_words_ts
    
        annotated_words = self.first_smoothen(annotated_words)      
        annotated_words = self.ngram_search(annotated_words, self.bigrams)
        annotated_words = self.second_smoothen(annotated_words)  

        annotated_words = self.deal_with_hashtags(annotated_words)
        annotated_words = self.deal_with_ilh(annotated_words)
        annotated_words = self.smooth_borrowings(annotated_words) 

        return annotated_words


    @staticmethod
    def smooth_borrowings(annotated_words):

        for i in range(len(annotated_words)):
            surrounding_lans = []
            if ".B" in annotated_words[i]["lan"]:
                if i > 0:
                    if "D" in annotated_words[i-1]["lan"]:
                        surrounding_lans.append("D")
                    elif "E" in annotated_words[i-1]["lan"]:
                        surrounding_lans.append("E")
                if i < len(annotated_words) - 2:
                    if "D" in annotated_words[i+1]["lan"]:
                        surrounding_lans.append("D")
                    elif "E" in annotated_words[i+1]["lan"]:
                        surrounding_lans.append("E")
                
                if ("E" in surrounding_lans and "E" in annotated_words[i]["lan"]) or ("D" in surrounding_lans and "D" in annotated_words[i]["lan"]):
                    annotated_words[i]["lan"] = annotated_words[i]["lan"].replace(".B", "")

        return annotated_words

    def deal_with_ilh(self, annotated_words):
    
        for i in range(len(annotated_words)):
            if annotated_words[i]["token"].lower() in self.clh_pos_tags:
                annotated_words[i]["lan"] = annotated_words[i]["lan"] + ".ILH"

        return annotated_words

    @staticmethod
    def combine_hashtags(annotated_words, tweet):

        in_hashtag = False
        idx_to_remove = []

        for i in range(len(annotated_words)):

            if annotated_words[i]["token"] == '#':
                in_hashtag = True
            elif in_hashtag:
                if "#" + annotated_words[i]["token"] in tweet:
                    annotated_words[i]["token"] = "#" + annotated_words[i]["token"]
                    idx_to_remove.append(i-1)
                
                in_hashtag = False
            else:
                continue

        for i in sorted(idx_to_remove, reverse=True):
            annotated_words.pop(i)

        return annotated_words

    @staticmethod
    def deal_with_hashtags(annotated_words):

        for i in range(len(annotated_words)):

            if annotated_words[i]["token"].startswith("#"):
                annotated_words[i]["lan"] = annotated_words[i]["lan"] + ".HT"
            else:
                continue

        return annotated_words

    @staticmethod
    def add_bio_keys(tweet_dict):
        last_lan = None
        for token in tweet_dict:
            if token["lan"] != 'E':
                token["bio"] = 'O'
            elif token["lan"] == last_lan:
                token["bio"] = 'I-' + token["lan"]
            else:
                token["bio"] = 'B-' + token["lan"]
            last_lan = token["lan"]

        return tweet_dict

    @staticmethod
    def flatten_morph(l):
        return ['+'.join(item) for item in l]

    @staticmethod
    def flatten_labels(l):
        return [''.join(item) for item in l]

    @staticmethod
    def flatten(input):
        new_list = []
        for i in input:
            for j in i:
                new_list.append(j)
        return new_list
    
    def intraword_dict(self, annotated_words):

        intrawords = {"geliked", "gelikt", "geliket", "getaggt", "geposted", "gepostet", "gedownloadet", "gedownloaded", "rewatchen", "rewatched", "rewatcht", "geairdroppt", "lieblingsuserin", "gepreordered", "gepaintet", "ausgeblendete", "verblendet"}

        for i in range(0, len(annotated_words)):
            if annotated_words[i][0] in intrawords:
                annotated_words[i] = (annotated_words[i][0], annotated_words[i][1], 3)
        
        return annotated_words

    def second_smoothen(self, annotated_words): 


        for i in range(len(annotated_words)):

            if annotated_words[i]["lan"] != 'U':
                continue

            j = i
            surrounding_lans = set()
            while j > 0:
                if "E" in annotated_words[j-1]["lan"]:
                    surrounding_lans.add("E")
                    break
                elif "D" in annotated_words[j-1]["lan"]:
                    surrounding_lans.add("D")
                    break
                else:
                    j -= 1

            j = i
            while j < len(annotated_words) - 2:
                if "E" in annotated_words[j+1]["lan"]:
                    surrounding_lans.add("E")
                    break
                elif "D" in annotated_words[j+1]["lan"]:
                    surrounding_lans.add("D")
                    break
                else:
                    j += 1

            if len(surrounding_lans) == 1:
                annotated_words[i]["lan"] = surrounding_lans.pop()
            else:
                annotated_words[i]["lan"] = "D"
            
        
        return annotated_words
    
    def first_smoothen(self, annotated_words): 


        for i in range(len(annotated_words)):

            if annotated_words[i]["lan"] != 'U':
                continue
            elif i == 0:
                if "E" in annotated_words[i+1]["lan"]:
                    annotated_words[i]["lan"] = "E"
                elif "D" in annotated_words[i+1]["lan"]:
                    annotated_words[i]["lan"] = "D"
            elif i == len(annotated_words) - 1:
                if "E" in annotated_words[i-1]["lan"]:
                    annotated_words[i]["lan"] = "E"
                elif "D" in annotated_words[i-1]["lan"]:
                    annotated_words[i]["lan"] = "D"
            elif "E" in annotated_words[i-1]["lan"] and "E" in annotated_words[i+1]["lan"]:
                annotated_words[i]["lan"] = "E"
            elif "E" in annotated_words[i-1]["lan"] and "O" in annotated_words[i+1]["lan"]:
                annotated_words[i]["lan"] = "E"
            elif "O" in annotated_words[i-1]["lan"] and "E" in annotated_words[i+1]["lan"]:
                annotated_words[i]["lan"] = "E"
            elif "D" in annotated_words[i-1]["lan"] and "D" in annotated_words[i+1]["lan"]:
                annotated_words[i]["lan"] = "D"
            elif "D" in annotated_words[i-1]["lan"] and "O" in annotated_words[i+1]["lan"]:
                annotated_words[i]["lan"] = "D"
            elif "O" in annotated_words[i-1]["lan"] and "D" in annotated_words[i+1]["lan"]:
                annotated_words[i]["lan"] = "D"
        
        return annotated_words
    
    

    def multiword_search(self, annotated_words, multiwords, lan):

        words = [i["token"].lower() for i in annotated_words]

        for i in range(len(annotated_words)):
            if annotated_words[i]["lan"] == 'U' and annotated_words[i]["token"].lower() in multiwords:
                for multiword_exp in multiwords[annotated_words[i]["token"].lower()]:
                    multiword_exp_words = multiword_exp.split()
                    pivot = multiword_exp_words.index(annotated_words[i]["token"].lower())
                    exp_len = len(multiword_exp_words)
                    # if ' '.join(words[i-pivot:i-pivot+exp_len]) == multiword_exp.lower():
                    #     print("WOW")
                    if i-pivot+exp_len <= len(words) and i-pivot >= 0 and ' '.join(words[i-pivot:i-pivot+exp_len]) == multiword_exp.lower():
                        lans_in_mwe = [annotated_words[k]["lan"] for k in range(i-pivot,i-pivot+exp_len)]
                        if lan == 'D':
                            annotated_words[i]["lan"] = "D"
                            break
                        elif lan == 'E' and 'D' not in lans_in_mwe:
                            annotated_words[i]["lan"] = "E"
                            break

        return annotated_words

    def ngram_search(self, annotated_words, ngrams):

        words = [i["token"].lower() for i in annotated_words]

        for i in range(len(annotated_words)):
            if annotated_words[i]["lan"] == 'U' and annotated_words[i]["token"].lower() in ngrams:
                for ng, _, lan in ngrams[annotated_words[i]["token"].lower()]:
                    phrase = ng.split()
                    pivot = phrase.index(annotated_words[i]["token"].lower())
                    exp_len = len(phrase)

                    if i-pivot+exp_len <= len(words) and i-pivot >= 0 and ' '.join(words[i-pivot:i-pivot+exp_len]) == ng.lower():
                        annotated_words[i]["lan"] = lan
                        break

        return annotated_words