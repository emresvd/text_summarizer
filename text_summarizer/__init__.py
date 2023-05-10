import spacy
from spacy.lang.en.stop_words import STOP_WORDS
from string import punctuation
from heapq import nlargest


def summarize(text: str, per: float = 0.1) -> dict:
    nlp = spacy.load('en_core_web_sm')
    doc = nlp(text)

    word_fs = {}
    for word in doc:
        if word.text.lower() not in list(STOP_WORDS):
            if word.text.lower() not in punctuation:
                if word.text not in word_fs.keys():
                    word_fs[word.text] = 1
                else:
                    word_fs[word.text] += 1

    max_f = max(word_fs.values())

    for word in word_fs.keys():
        word_fs[word] = word_fs[word] / max_f
    word_fs = dict(sorted(word_fs.items(), key=lambda x: x[1], reverse=True))

    sentence_tokens = [sent for sent in doc.sents]
    sentence_scores = {}
    for sent in sentence_tokens:
        for word in sent:
            if word.text.lower() in word_fs.keys():
                if sent not in sentence_scores.keys():
                    sentence_scores[sent] = word_fs[word.text.lower()]
                else:
                    sentence_scores[sent] += word_fs[word.text.lower()]
    sentence_scores = dict(
        sorted(sentence_scores.items(), key=lambda x: x[1], reverse=True))

    select_length = int(len(sentence_tokens) * per)

    summary = nlargest(select_length, sentence_scores, key=sentence_scores.get)
    summary = "".join(word.text for word in summary)

    return {
        "summary": summary,
        "word_fs": word_fs,
        "sentence_scores": sentence_scores,
        "max_f": max_f,
        "select_length": select_length,
        "sentence_tokens": sentence_tokens,
        "word_fs": word_fs,
        "doc": doc,
        "nlp": nlp
    }
