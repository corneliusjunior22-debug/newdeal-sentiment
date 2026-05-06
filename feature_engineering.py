from sklearn.feature_extraction.text import TfidfVectorizer

vectorizer = TfidfVectorizer(max_features=3000)

def fit_transform(texts):
    return vectorizer.fit_transform(texts)

def transform(texts):
    return vectorizer.transform(texts)
