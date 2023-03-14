import re
import pickle

import nltk
nltk.download('stopwords')

from nltk.corpus import stopwords
from nltk.stem import SnowballStemmer
from nltk.tokenize import WhitespaceTokenizer


def prep_data(text: str) -> str:
    """
    Clear comment from urls, digits and special symbols.
    Change comment with stemming, tokenizating and dropping stop words.
    """
    text = text.lower()
    text = re.sub('http\S+|http.\S+', '', text)
    text = re.sub('\d+', '', text)
    text = re.sub('[^\w\s]', '', text)
    text = re.sub('[\n]', '', text)

    tokenizing = WhitespaceTokenizer()
    stemming = SnowballStemmer("russian")
    sw = stopwords.words('russian')

    text = ' '.join([stemming.stem(word) for word in tokenizing.tokenize(text) if word not in sw])

    return text

def get_estimation(text: str) -> float:
    """
    Predict toxic probability of the comment.
    """
    vectorizer = pickle.load(open('models/vectorizer.pkl', 'rb'))
    model = pickle.load(open('models/model.pkl', 'rb'))

    text = prep_data(text)
    if text:
        vector = vectorizer.transform([text])

        prediction = model.predict_proba(vector)
        prob_toxic = prediction[0][1]
    else:
        prob_toxic = 0.0
    return prob_toxic