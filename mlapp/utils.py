import pandas as pd
import numpy as np
import nltk
from sklearn.preprocessing import LabelEncoder
from sklearn.feature_extraction.text import TfidfVectorizer
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
import joblib
from .minio_client import download_file

nltk.download('punkt')
nltk.download('stopwords')
nltk.download('wordnet')

stop_words = set(stopwords.words('english'))
lemmatizer = WordNetLemmatizer()

def preprocess_text(text):
    tokens = word_tokenize(text.lower())
    tokens = [lemmatizer.lemmatize(token) for token in tokens if token.isalpha() and token not in stop_words]
    return ' '.join(tokens)


tfidf_vectorizer_path = 'tfidf_vectorizer_v1_0.pkl'
label_encoder_path = 'label_encoder_v1_0.pkl'

download_file('models', 'tfidf_vectorizer_v1_0.pkl', tfidf_vectorizer_path)
download_file('models', 'label_encoder_v1_0.pkl', label_encoder_path)

tfidf_vectorizer = joblib.load(tfidf_vectorizer_path)
label_encoder = joblib.load(label_encoder_path)