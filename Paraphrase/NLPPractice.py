import spacy
import nltk
from nltk.corpus import wordnet as wn
from nltk.stem.wordnet import WordNetLemmatizer
nltk.download('wordnet')

sentences = ["The red book near the campus of SUNY is glowing under the sunshine.",
             "I feel happy about a new car that I bought yesterday."]

nlp = spacy.load("en_core_web_lg")
tags_to_replace = {"VERB", "ADJ", "ADV", "NOUN", "PROPN"}

from nltk.corpus import wordnet as wn
wn.synsets('car')

def paraphrase(s):
    s_out = []
    
    for token in nlp(s):
        synset = wn.synsets(token.text)
        pos = token.pos_
        tag = token.tag_
        
        # get the present tense verb
        word = token
        if token.pos_== 'VERB':
            word = nlp(str(token).replace(token.text, token.lemma_))
        
        if pos in tags_to_replace: # replace the word with a synonym
            if len(synset) == 0: # if there is no synonym
                s_out.append(token.text)
            else: # search for a synonym
                # get candidates
                candidates = []
                for synset in wn.synsets(token.text):
                    for lemma in synset.lemmas():
                        candidates.append(lemma.name())
                        
                # get the word with maximum similarity with the original word
                max = 0
                max_word = ""
                for candidate in candidates:
                    # exclude the word that is identical to the original word
                    cand = nlp(str(candidate))[0]
                    cand_pt = str(nlp(candidate.replace(cand.text, cand.lemma_)))
                    if str(word).lower() == cand_pt.lower(): 
                        continue
                    similarity = word.similarity(cand)
                    if max < similarity:
                        max = similarity
                        max_word = cand
                
                new_word = max_word
                old_tag = token.tag_
                new_tag = ""
                if len(new_word) != 0:
                    new_tag = nlp(str(new_word))[0].tag_
                else:
                    new_word = word
                    new_tag = tag
                
                if (old_tag == new_tag):
                    s_out.append(new_word)
                else: # match verb tense
                    s_out.append(new_word)
        else:
            s_out.append(token.text) # do not replace
    
    return s_out


# test
for sentence in sentences:
    new_sentence_list = paraphrase(sentence)
    new_sentence = " ".join(str(e) for e in new_sentence_list)
    print(new_sentence)
