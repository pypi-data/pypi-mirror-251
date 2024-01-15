## TongueSwitcher v2

TongueSwitcher was designed to be a code-switching identification system for German-English. It is mostly rule-based, using specially created wordlists for most of the heavy-lifting. It is therefore fast and efficient.

Identification is performed at the word and sub-word level, and then the identity of still unknown words is computed by the nearest identified tokens.

### Usage 

```python
from tongueswitcher.executor import Executor

ts = Executor()

sentences = ["ich glaub ich muss echt rewatchen like i feel so empty was soll ich denn jetzt machen"]

results = ts.tongueswitcher_detect(sentences)

>>> [[{'lan': 'D', 'pos': 'PRON', 'token': 'ich'},
      {'lan': 'D', 'pos': 'VERB', 'token': 'glaub'},
      {'lan': 'D', 'pos': 'PRON', 'token': 'ich'},
      {'lan': 'D', 'pos': 'AUX', 'token': 'muss'},
      {'lan': 'D', 'pos': 'ADV', 'token': 'echt'},
      {'breakdown': 're+watch+en',
       'lan': 'M',
       'lans': 'E+E+D',
       'pos': 'VERB',
       'prefixes': {'lans': ['E'], 'text': ['re']},
       'roots': {'lans': ['E'], 'text': ['watch']},
       'suffixes': {'lans': ['D'], 'text': ['en']},
       'token': 'rewatchen'},
      {'lan': 'E', 'pos': 'SCONJ', 'token': 'like'},
      {'lan': 'E', 'pos': 'PRON', 'token': 'i'},
      {'lan': 'E', 'pos': 'VERB', 'token': 'feel'},
      {'lan': 'E', 'pos': 'ADV', 'token': 'so'},
      {'lan': 'E', 'pos': 'ADJ', 'token': 'empty'},
      {'lan': 'D.ILH', 'pos': 'ADV', 'token': 'was'},
      {'lan': 'D', 'pos': 'AUX', 'token': 'soll'},
      {'lan': 'D', 'pos': 'PRON', 'token': 'ich'},
      {'lan': 'D', 'pos': 'ADV', 'token': 'denn'},
      {'lan': 'D', 'pos': 'ADV', 'token': 'jetzt'},
      {'lan': 'D', 'pos': 'VERB', 'token': 'machen'}]]
```

### Labels

TongueSwitcher v2 identifies words with the following acronyms:

```
E = English
D = German
M = Mixed
NE = Named Entity
O = Other
```

With possible subcategorizations:

```
.ILH = Interlingual homograph
.B = Borrowed word
.HT = Hashtag
.E  = Emoji
.P  = Punctuation
```

### Dependencies

Other than the wordlists, we used Flair for POS tagging and a finetuned RoBERTa model for binary named entity recognition.

We used python version 3.7.

### Citation

For more detail, please refer to our paper:

```
@inproceedings{sterner2023tongueswitcher,
  author    = {Igor Sterner and Simone Teufel},
  title     = {TongueSwitcher: Fine-Grained Identification of German-English Code-Switching},
  booktitle = {Sixth Workshop on Computational Approaches to Linguistic Code-Switching},
  publisher = {Empirical Methods in Natural Language Processing},
  year      = {2023},
}
```