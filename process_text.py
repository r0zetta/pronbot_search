# -*- coding: utf-8 -*-
from collections import Counter
import re
import spacy
from nltk.stem.snowball import SnowballStemmer
import spacy

def get_tweet_tags(tweet):
    preprocessed = preprocess_text(tweet)
    if preprocessed is not None:
        return process_sentence(preprocessed)

def preprocess_text(text, lang="en"):
    valid = {"en": u"0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ#@'…… ",
             "fi": u"0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZäöåÄÖÅ:#@…… ",
             "sv": u"0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZäöåÄÖÅ'#@…… "}
    url_match = u"(https?:\/\/[0-9a-zA-Z\-\_]+\.[\-\_0-9a-zA-Z]+\.?[0-9a-zA-Z\-\_]*\/?.*)"
    name_match = u"\@[\_0-9a-zA-Z]+\:?"
    text = re.sub(url_match, u"", text)
    text = re.sub(name_match, u"", text)
    text = re.sub(u"\&amp\;?", u"", text)
    text = re.sub(u"[\:\.]{1,}$", u"", text)
    text = re.sub(u"^RT\:?", u"", text)
    text = re.sub(u"/", u" ", text)
    text = re.sub(u"-", u" ", text)
    text = re.sub(u"\w*[\…]", u"", text)
    if lang in valid:
        text = u''.join(x for x in text if x in valid[lang])
    else:
        text = u''.join(x for x in text if x in valid["en"])
    text = text.strip()
    if len(text.split()) > 5:
        return text

# Tokenize sentence into words
def tokenize_sentence(text, stopwords=None):
    words = re.split(r'(\s+)', text)
    if len(words) < 1:
        return
    tokens = []
    for w in words:
        if w is not None:
            w = w.strip()
            w = w.lower()
            if w.isspace() or w == "\n" or w == "\r":
                w = None
            if w is not None and "http" in w:
                w = None
            if w is not None and len(w) < 1:
                w = None
            if w is not None and u"…" in w:
                w = None
            if w is not None:
                tokens.append(w)
    if len(tokens) < 1:
        return
# Remove stopwords and other undesirable tokens
    cleaned = []
    for token in tokens:
        if len(token) > 0:
            if stopwords is not None:
                if token in stopwords:
                    token = None
            if token is not None:
                if re.search(".+…$", token):
                    token = None
            if token is not None:
                if token == "#":
                    token = None
            if token is not None:
                cleaned.append(token)
    if len(cleaned) < 1:
        return
    return cleaned



def get_tokens_nlp(doc, stemmer, lang="en"):
    ret = []
    skip_tokens = {"en": ["are", "do", "'s", "be", "is", "https//", "#", "-pron-", "so", "as", "that", "not", "who", "which", "thing", "even", "said", "says", "say", "keep", "like", "will", "have", "what", "can", "how", "get", "there", "would", "when", "then", "here", "other", "know", "let", "all"],
                   "sv": ["t", "s", "o", "#", "m", "2", "c", "1", "3", "4", "03", "000", "a", "in", "ta", "nr", "se", "fö", "få", "ge", "30", "ska", "vill", "kommer", "bara", "får", "finns", "gör", "går", "helt", "väl", "också", "även", "borde", "hela", "dom", "alltså", "kanske", "gå", "sitt", "nog", "genom", "skall", "annat", "kunna", "sätt", "ens", "just", "bör", "ändå", "sen", "både", "vore", "därför", "ännu", "pga", "får", "gör", "få", "går", "tycker", "väl", "tror", "ser", "lite", "göra", "också", "även", "tar", "vet", "behöver", "två", "alltså", "igen", "står", "verkar", "redan", "gå", "dags", "inför", "håller", "lika", "fram", "del", "enligt", "ger", "verkligen", "säga", "sätt", "visar", "gäller", "undrar", "bör", "ändå", "all", "gång", "förstår", "kom", "gjort", "fick", "fått", "handlar", "sagt", "vissa", "både", "därför", "precis", "riktigt", "ännu", "väldigt", "hos", "samtidigt", "sitter", "menar", "komma", "låter", "låt", "hålla", "egen", "sak", "stå", "hej", "nästa"],
                   "fi": []}
    for token in doc:
        lemma = token.lemma_
        pos = token.pos_
        if pos in ["VERB", "ADJ", "ADV", "NOUN"]:
            if lang in skip_tokens:
                if lemma.lower() not in skip_tokens[lang]:
                    if len(lemma) > 1:
                        stem = stemmer.stem(lemma)
                        ret.append(stem)
    return ret

def get_labels_nlp(doc):
    labels = []
    for entity in doc.ents:
        label = entity.label_
        text = entity.text
        if label in ["ORG", "GPE", "PERSON", "NORP"]:
            if len(text) > 1:
                labels.append(text)
    return labels

def get_hashtags_nlp(sentence):
    ret = []
    words = re.split(r'(\s+)', sentence)
    for w in words:
        if re.search("^\#[a-zA-Z0-9]+$", w):
            if w not in ret:
                ret.append(w)
    return ret

def process_sentence(sentence, lang, nlp, stemmer, stopwords):
    if nlp is not None and stemmer is not None:
        return process_sentence_nlp(sentence, lang, nlp, stemmer)
    else:
        return tokenize_sentence(sentence, stopwords)

def process_sentence_nlp(sentence, lang, nlp, stemmer):
    tags = []
    doc = nlp(sentence)
    # get tags using spacy
    tokens = get_tokens_nlp(doc, stemmer, lang)
    for t in tokens:
        if t not in tags:
            tags.append(t)
    labels = get_labels_nlp(doc)
    for l in labels:
        if l not in tags:
            tags.append(l)
    hashtags = get_hashtags_nlp(sentence)
    for h in hashtags:
        if h not in tags:
            tags.append(h)
    # lowercase and remove duplicates
    cons = []
    for t in tags:
        t = t.lower()
        t = t.strip()
        if t not in cons:
            cons.append(t)
    return cons

def vectorize_item(tags, vocab):
    row = []
    for word in vocab:
        if word in tags:
            row.append(1)
        else:
            row.append(0)
    return row

def get_freq_dist(tag_map, lang="en"):
    skip_tokens = {"en": ["just", "think", "how", "need", "only", "all", "still", "even", "why", "look", "let", "most", "way", "more", "mean", "new", "must", "talk", "try", "back", "have", "seem", "will", "see", "use", "tell", "would", "should", "could", "can", "go", "are", "do", "'s", "be", "make", "want", "know", "come", "is", "https//", "#", "-pron-", "when", "here", "say", "there", "also", "quite", "so", "get", "perhaps", "as", "that", "now", "not", "then", "who", "very", "which", "then", "thing", "what", "take", "give", "show", "really", "keep", "other", "people", "man"],
                   "sv": ["t", "s", "o", "#", "m", "2", "c", "1", "3", "4", "03", "000", "a", "in", "ta", "nr", "se", "fö", "få", "ge", "30", "ska", "vill", "kommer", "bara", "får", "finns", "gör", "går", "helt", "väl", "också", "även", "borde", "hela", "dom", "alltså", "kanske", "gå", "sitt", "nog", "genom", "skall", "annat", "kunna", "sätt", "ens", "just", "bör", "ändå", "sen", "både", "vore", "därför", "ännu", "pga", "får", "gör", "få", "går", "tycker", "väl", "tror", "ser", "lite", "göra", "också", "även", "tar", "vet", "behöver", "två", "alltså", "igen", "står", "verkar", "redan", "gå", "dags", "inför", "håller", "lika", "fram", "del", "enligt", "ger", "verkligen", "säga", "sätt", "visar", "gäller", "undrar", "bör", "ändå", "all", "gång", "förstår", "kom", "gjort", "fick", "fått", "handlar", "sagt", "vissa", "både", "därför", "precis", "riktigt", "ännu", "väldigt", "hos", "samtidigt", "sitter", "menar", "komma", "låter", "låt", "hålla", "egen", "sak", "stå", "hej", "nästa"],
                   "fi": []}
    dist = Counter()
    tag_map_size = len(tag_map)
    for tweet, tags in tag_map.iteritems():
        for t in tags:
            t = t.lower()
            t = t.strip()
            if len(t) > 0:
                if lang in skip_tokens:
                    if t not in skip_tokens[lang]:
                        dist[t] += 1
                else:
                    dist[t] += 1
    print
    print("Total unique tags: " + str(len(dist)))
    return dist

def get_spacy_supported_langs():
    return ["en", "de", "es", "pt", "fr", "it", "nl"]

def get_stemmer_supported_langs():
    lang_map = {"da": "danish",
                "nl": "dutch",
                "en": "english",
                "fi": "finnish",
                "fr": "french",
                "de": "german",
                "hu": "hungarian",
                "it": "italian",
                "no": "norwegian",
                "pt": "portuguese",
                "ro": "romanian",
                "ru": "russian",
                "es": "spanish",
                "sv": "swedish"}
    return lang_map

def init_nlp_multi_lang(langs=["en"]):
    nlp = {}
    stemmer = {}
    spacy_supported_langs = get_spacy_supported_langs()
    lang_map = get_stemmer_supported_langs()
    for l in langs:
        if l in spacy_supported_langs:
            nlp[l] = spacy.load(l)
            if nlp[l] is not None:
                print("Loaded NLP processor for language: " + l)
        if l in lang_map.keys():
            stemmer[l] = SnowballStemmer(lang_map[l])
            if stemmer[l] is not None:
                print("Loaded stemmer for language: " + l)
    return nlp, stemmer

def init_nlp_single_lang(lang="en"):
    nlp = None
    stemmer = None
    spacy_supported_langs = get_spacy_supported_langs()
    if lang in spacy_supported_langs:
        nlp = spacy.load(lang)
    stemmer_lang_map = get_stemmer_supported_langs()
    if lang in stemmer_lang_map:
        stemmer = SnowballStemmer(stemmer_lang_map[lang])
    return nlp, stemmer




