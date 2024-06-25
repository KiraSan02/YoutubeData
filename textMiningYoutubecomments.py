import re
import emoji
import gensim
from gensim.parsing.preprocessing import remove_stopwords, strip_punctuation, strip_numeric, strip_multiple_whitespaces, strip_short
from gensim.corpora import Dictionary
from gensim.models import TfidfModel
from pymongo import MongoClient
import pandas as pd

# Connexion à MongoDB
client = MongoClient('localhost', 27017)
db = client.youtubevidsdetails
collection = db.trending_videos

# Récupération des données de MongoDB
data = collection.find()
comments = []
for video in data:
    comments.extend(video['comments'])

# 1. Nettoyage des données
def clean_text(text):
    text = re.sub(r'http\S+', '', text)  # Suppression des liens
    text = strip_punctuation(text)  # Suppression de la ponctuation
    text = strip_numeric(text)  # Suppression des chiffres
    text = text.lower()  # Conversion en minuscules
    text = strip_multiple_whitespaces(text).strip()  # Suppression des espaces multiples
    text = ''.join([c for c in text if c not in emoji.UNICODE_EMOJI['en']])  # Suppression des émojis
    text = remove_stopwords(text)  # Suppression des stop words
    text = strip_short(text, minsize=3)  # Suppression des mots courts (moins de 3 caractères)
    return text

comments_cleaned = [clean_text(comment) for comment in comments]

# 2. Tokenisation
comments_tokenized = [gensim.utils.simple_preprocess(comment, deacc=True) for comment in comments_cleaned]

# 3. Normalisation (Lemmatisation)
lemmatizer = gensim.models.WordNetLemmatizer()
comments_lemmatized = [[lemmatizer.lemmatize(token) for token in tokens] for tokens in comments_tokenized]

# Reconstruire les commentaires nettoyés
comments_normalized_text = [' '.join(tokens) for tokens in comments_lemmatized]

# 4. Filtrage des commentaires répétés
comments_unique = list(set(comments_normalized_text))

# 5. Transformation en TF-IDF
# Créer un dictionnaire à partir des commentaires tokenisés
dictionary = Dictionary(comments_lemmatized)

# Créer un corpus: une liste de vecteurs bag-of-words
corpus = [dictionary.doc2bow(comment) for comment in comments_lemmatized]

# Appliquer le modèle TF-IDF
tfidf = TfidfModel(corpus)

# Transformez le corpus en TF-IDF
corpus_tfidf = tfidf[corpus]

