import nltk

def ensure_wordnet():
    try:
        nltk.data.find("corpora/wordnet")
        return True
    except LookupError:
        nltk.download("wordnet")
        return False

if ensure_wordnet():
    print("WordNet available ✅")
