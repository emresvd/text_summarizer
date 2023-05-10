import spacy
from spacy.lang.en.stop_words import STOP_WORDS
from string import punctuation
from heapq import nlargest

with open("test.txt", "r", encoding="utf-8") as f:
    text = f.read()

nlp = spacy.load('en_core_web_sm')
doc = nlp(text)

tokens = [token.text for token in doc]

word_fs = {}
for word in doc:
    if word.text.lower() not in list(STOP_WORDS):
        if word.text.lower() not in punctuation:
            if word.text not in word_fs.keys():
                word_fs[word.text] = 1
            else:
                word_fs[word.text] += 1

print(dict(sorted(word_fs.items(), key=lambda x: x[1], reverse=True)))

max_f = max(word_fs.values())

for word in word_fs.keys():
    word_fs[word] = word_fs[word] / max_f
print(dict(sorted(word_fs.items(), key=lambda x: x[1], reverse=True)))

sentence_tokens = [sent for sent in doc.sents]

sentence_scores = {}
for sent in sentence_tokens:
    for word in sent:
        if word.text.lower() in word_fs.keys():
            if sent not in sentence_scores.keys():
                sentence_scores[sent] = word_fs[word.text.lower()]
            else:
                sentence_scores[sent] += word_fs[word.text.lower()]
print(dict(sorted(sentence_scores.items(), key=lambda x: x[1], reverse=True)))

per = 0.1
select_length = int(len(sentence_tokens) * per)

summary = nlargest(select_length, sentence_scores, key=sentence_scores.get)
summary = "".join(word.text for word in summary)

print("sum", summary)
