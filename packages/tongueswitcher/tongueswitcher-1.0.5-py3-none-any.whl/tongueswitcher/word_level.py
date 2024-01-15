import copy
import json

import emoji


class WordProcessor():
    def __init__(self):
        pass
    
    def word_processor(self, annotated_words):

        for i in range(len(annotated_words)):
            
            word = annotated_words[i]["token"]

            if bool(emoji.emoji_count(word)):
                annotated_words[i]["lan"] = "O.E"
                continue
            elif annotated_words[i]["pos"] == "PUNCT":
                annotated_words[i]["lan"] = "O.P"
                continue
            elif annotated_words[i]["token"] in ["URL", "PHONE-NUMBER", "EMAIL"]:
                annotated_words[i]["lan"] = "O.O"
                continue

            word = ''.join([i for i in word if (i.isalpha() or i == "'" or i == "-" or i == ".")])

            if not word:
                continue                

            if word.lower() in self.data.borrowings.de2en:
                annotated_words[i]["lan"] = "E.B"
                continue        
            elif word.lower() in self.data.borrowings.en2de:
                annotated_words[i]["lan"] = "D.B"
                continue
            elif (word.lower() in self.data.dictionaries.cs and len(word) > 2) or word.lower() in self.data.dictionaries.en_one_two:
                annotated_words[i]["lan"] = "E"
                continue
            elif word.startswith("'") and i > 0 and (annotated_words[i-1]["token"].lower() + word.lower()) in self.data.dictionaries.cs:
                annotated_words[i]["lan"] = "E"
                annotated_words[i-1]["lan"] = "E"
                continue
            elif word.lower() in self.clh_pos_tags:
                lan = self.cl_homonyms_checker(word.lower(), annotated_words[i]["pos"])
                # annotated_words[i]["clh"] = True
                if lan == "E":
                    annotated_words[i]["lan"] = "E"
                    continue
                elif lan == "D":
                    annotated_words[i]["lan"] = "D"
                    continue
            elif (word.lower() in self.data.dictionaries.de and len(word) > 2) or (word.lower() in self.data.dictionaries.not_cs and len(word) > 2) or word.lower() in self.data.dictionaries.de_one_two:
                annotated_words[i]["lan"] = "D"
                continue
            elif (word.lower() in self.data.dictionaries.en and len(word) > 2) or word.lower() in self.data.dictionaries.en_one_two: 
                annotated_words[i]["lan"] = "E"
                continue
            elif not word[0].isupper() and len(word) > 6:
                word_dict = self.morph_pre_suf(annotated_words[i].copy())
                if word_dict["lan"] != "U":
                    annotated_words[i] = word_dict
                    continue

            if len(word) > 6:

                if "-" in word:
                    word_morphemes = word.split("-")

                    if all([len(m) > 3 for m in word_morphemes]):
                        annotated_words[i] = self.process_morphemes(annotated_words[i], word_morphemes)

                        if annotated_words[i]["lan"] != 'U':
                            continue
                    else:
                        continue

                for tagger in [self.de_tagger, self.mixed_tagger, self.en_tagger]:

                    lemma, word_morphemes = self.morph_word(word, tagger)
                    annotated_words[i] = self.process_morphemes(annotated_words[i], word_morphemes)

                    if annotated_words[i]["lan"] != 'U':
                        break
                    elif lemma.lower() in self.data.dictionaries.cs:
                        annotated_words[i]["lan"] = "E"
                        break
                    elif lemma.lower() in self.data.dictionaries.not_cs:
                        annotated_words[i]["lan"] = "D"
                        break



            if any(char in word.lower() for char in ["ä", "ö", "ü", "ß"]):
                # probably a dialect sentence
                return

        return annotated_words

    def process_morphemes(self, word_dict, word_morphemes):

        # print(word_morphemes)
        word_morphemes_filtered = ["".join(filter(str.isalpha, morpheme)) for morpheme in word_morphemes]
        # print(word_morphemes_filtered)

        en_prefixes = []
        de_prefixes = []
        prefixes = []

        en_roots = []
        de_roots = []
        roots = []

        en_suffixes = []
        de_suffixes = []
        suffixes = []

        found_roots = False

        for morpheme in word_morphemes_filtered:
            lower_morpheme = morpheme.lower()

            if lower_morpheme in self.data.dictionaries.cs: # lenth of the word?
                en_roots.append(morpheme)
                roots.append((morpheme, 'E'))
                found_roots = True
            elif lower_morpheme in self.data.dictionaries.not_cs:
                de_roots.append(morpheme)
                roots.append((morpheme, 'D'))
                found_roots = True
            elif lower_morpheme in self.data.affixes.pure_prefixes_en and not found_roots:
                en_prefixes.append(morpheme)
                prefixes.append((morpheme, 'E'))
            elif lower_morpheme in self.data.affixes.pure_prefixes_de and not found_roots:
                de_prefixes.append(morpheme)
                prefixes.append((morpheme, 'D'))
            elif lower_morpheme in self.data.affixes.pure_suffixes_en and found_roots:
                en_suffixes.append(morpheme)
                suffixes.append((morpheme, 'E'))
            elif lower_morpheme in self.data.affixes.pure_suffixes_de and found_roots:
                de_suffixes.append(morpheme)
                suffixes.append((morpheme, 'D'))

        de_morphemes = de_prefixes + de_roots + de_suffixes
        en_morphemes = en_prefixes + en_roots + en_suffixes

        # print(f"en_prefixes: {en_prefixes}")
        # print(f"de_prefixes: {de_prefixes}")
        # print(f"prefixes: {prefixes}")

        # print(f"en_roots: {en_roots}")
        # print(f"de_roots: {de_roots}")
        # print(f"roots: {roots}")

        # print(f"en_suffixes: {en_suffixes}")
        # print(f"de_suffixes: {de_suffixes}")
        # print(f"suffixes: {suffixes}")

        # print(f"found_roots: {found_roots}")

        # print(f"de_morphemes: {de_morphemes}")
        # print(f"en_morphemes: {en_morphemes}")

        # if len(en_morphemes) == len(word_morphemes_filtered):
        #     word_dict["lan"] = "E"
        # if "".join([p[0] for p in prefixes] + [r[0] for r in roots]) in self.data.dictionaries.not_cs:
        #     word_dict["lan"] = "D"
        # elif "".join([r[0] for r in roots] + [s[0] for s in suffixes]) in self.data.dictionaries.not_cs:
        #     word_dict["lan"] = "D"
        if de_morphemes and en_roots:

            word_dict["lan"] = "M"
            word_dict["roots"] = {"text": [i[0] for i in roots], "lans": [i[1] for i in roots]}

            if prefixes:
                word_dict["prefixes"] = {"text": [i[0] for i in prefixes], "lans": [i[1] for i in prefixes]}
            if suffixes:
                word_dict["suffixes"] = {"text": [i[0] for i in suffixes], "lans": [i[1] for i in suffixes]}

            lans = word_dict.get("prefixes", {}).get("lans", []) + word_dict.get("roots", {}).get("lans", []) + word_dict.get("suffixes", {}).get("lans", [])
            breakdown = word_dict.get("prefixes", {}).get("text", []) + word_dict.get("roots", {}).get("text", []) + word_dict.get("suffixes", {}).get("text", [])

            word_dict["lans"] = "+".join(lans)

            breakdown = [subword.replace("+", "") for subword in word_morphemes]
            word_dict["breakdown"] = "+".join(breakdown)

        elif en_morphemes and not de_morphemes and roots:
            word_dict["lan"] = "E"
        elif de_morphemes and not en_morphemes and roots:
            word_dict["lan"] = "D"

        return word_dict


    def morph_pre_suf(self, word_dict):

        word_dict["roots"] = {"text": [word_dict["token"]], "lans": ["U"]}
        options = [word_dict]
        solutions = []
        self.checked = []
        
        options, solutions = self.strip(self.prefix_stripper, self.data.affixes.pure_prefixes_en, 'E', options, solutions)
        options, solutions = self.strip(self.prefix_stripper, self.data.affixes.pure_prefixes_de, 'D', options, solutions)

        options, solutions = self.strip(self.suffix_stripper, self.data.affixes.pure_suffixes_en, 'E', options, solutions)
        options, solutions = self.strip(self.suffix_stripper, self.data.affixes.pure_suffixes_de, 'D', options, solutions)

        options, solutions = self.strip(self.prefix_stripper, self.data.affixes.prefixes_second_de, 'D', options, solutions)
        options, solutions = self.strip(self.prefix_stripper, self.data.affixes.prefixes_second_en, 'E', options, solutions)

        # solutions = list(set(solutions))
        if len(solutions) > 0:

            for root_dict in sorted(solutions, key=lambda x: len("".join(x['roots']['text']))):
                lans = root_dict.get("prefixes", {}).get("lans", []) + root_dict.get("roots", {}).get("lans", []) + root_dict.get("suffixes", {}).get("lans", [])

                if len(set(lans)) < 2:
                    word_dict["lan"] = lans[0]
                    return word_dict
                else:
                    breakdown = root_dict.get("prefixes", {}).get("text", []) + root_dict.get("roots", {}).get("text", []) + root_dict.get("suffixes", {}).get("text", [])

                    root_dict["lans"] = "+".join(lans)

                    breakdown = [word.replace("+", "") for word in breakdown]
                    root_dict["breakdown"] = "+".join(breakdown)
                    root_dict["lan"] = 'M'
                    return root_dict
        
        return word_dict

    def strip(self, stripper_func, strip_list, lan, options, solutions):

        options = stripper_func(strip_list, lan, options)

        for i in range(len(options.copy())):
            word_dict = copy.deepcopy(options[i]) 
            if word_dict in self.checked:
                continue
            self.checked.append(copy.deepcopy(options[i]))
            root = word_dict["roots"]["text"][0].lower()
            if root in self.data.dictionaries.cs:
                word_dict["roots"]["lans"] = ['E']
                if word_dict not in solutions:
                    solutions.append(word_dict)
            elif len(root) > 2 and root[-1] != "e" and root + 'e' in self.data.dictionaries.cs:
                word_dict["roots"]["text"] = [root + 'e']
                word_dict["roots"]["lans"] = ['E']
                if "prefixes" in word_dict and len(word_dict["prefixes"]["text"]) > 1:
                    continue
                if "suffixes" in word_dict and len(word_dict["suffixes"]["text"]) > 1:
                    continue
                if word_dict not in solutions:
                    solutions.append(word_dict)
            elif len(root) > 2 and root[-1] == root[-2] and (root[:-1] in self.data.dictionaries.cs):
                word_dict["roots"]["text"] = [root[:-1]]
                word_dict["roots"]["lans"] = ['E']
                if "prefixes" in word_dict and len(word_dict["prefixes"]["text"]) > 1:
                    continue
                if "suffixes" in word_dict and len(word_dict["suffixes"]["text"]) > 1:
                    continue
                if word_dict not in solutions:
                    solutions.append(word_dict)
            # else:
            #     compound_roots, compound_lans = self.find_roots(root)
            #     if compound_roots:
            #         word_dict["roots"]["text"] = compound_roots
            #         word_dict["roots"]["lans"] = compound_lans
            #         if word_dict not in solutions:
            #             solutions.append(word_dict)


        return options, solutions
        
    def find_roots(self, compound_word):
        def find_subword(word):
            for i in range(len(word), -1, -1):
                prefix = word[:i]
                if prefix in self.data.dictionaries.cs and len(prefix) > 3:
                    rest = word[i:]
                    if not rest:
                        return [(prefix, 'E')]
                    subwords = find_subword(rest)
                    if subwords is not None:
                        return [(prefix, 'E')] + subwords
                elif prefix in self.data.dictionaries.not_cs and len(prefix) > 3:
                    rest = word[i:]
                    if not rest:
                        return [(prefix, 'D')]
                    subwords = find_subword(rest)
                    if subwords is not None:
                        return [(prefix, 'D')] + subwords
            return None

        roots = find_subword(compound_word)
        if roots is not None:
            roots, lans = zip(*roots)
            return list(roots), list(lans)
        else:
            return [], []


    def suffix_stripper(self, strip_list, lan, options):
        new_options = []
        for i in range(len(options.copy())):
            word = options[i]["roots"]["text"][0]
            for s in strip_list:
                if word.lower().endswith(s):
                    word_dict = copy.deepcopy(options[i]) 
                    word_dict["roots"]["text"] = [word[:-len(s)]]
                    if "suffixes" not in word_dict:
                        word_dict["suffixes"] = {"text": [word[-len(s):]], "lans": [lan]}
                    else:
                        word_dict["suffixes"]["text"].insert(0, word[-len(s):])
                        word_dict["suffixes"]["lans"].insert(0, lan)

                    new_options.append(word_dict)

        options += new_options

        return options

    def prefix_stripper(self, strip_list, lan, options):
        new_options = []
        for i in range(len(options.copy())):

            word = options[i]["roots"]["text"][0]
            for s in strip_list:
                if word.lower().startswith(s):
                    word_dict = copy.deepcopy(options[i]) 
                    word_dict["roots"]["text"] = [word[len(s):]]
                    if "prefixes" not in word_dict:
                        word_dict["prefixes"] = {"text": [word[:len(s)]], "lans": [lan]}
                    else:
                        word_dict["prefixes"]["text"].append(word[:len(s)])
                        word_dict["prefixes"]["lans"].append(lan)

                    new_options.append(word_dict)

        options += new_options

        return options


    @staticmethod
    def open_prefixes_suffixes(dir):
        with open(dir, 'r', encoding = 'utf-8') as f:
            return f.read().splitlines()

    @staticmethod
    def open_cl_homonyms(dir):
        with open(dir, 'r', encoding='utf-8') as f:
            return json.load(f)

    def cl_homonyms_checker(self, word, pos):


        if word not in self.clh_pos_tags:
            return "U"
        elif pos not in self.clh_pos_tags[word]:
            return "U"
        else:
            return self.clh_pos_tags[word][pos]

    def morph_word(self, word, tagger):

        analysis = tagger.analyze(word,taglevel=3)
        morphemes = [i[0] for i in analysis[1]]

        return analysis[0], morphemes