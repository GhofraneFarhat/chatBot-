# Importation des bibliothèques nécessaires

import pandas as pd
import numpy as np
import re
import nltk
from sklearn.feature_extraction.text import CountVectorizer
from sklearn import svm

# Collecte des données

data = pd.read_csv('test.csv')

# Prétraitement des données

def preprocess_text(text):
    text = re.sub('[^a-zA-Z]', ' ', text)
    text = text.lower()
    text = nltk.word_tokenize(text)
    text = [word for word in text if not word in set(nltk.corpus.stopwords.words('english'))]
    text = ' '.join(text)
    return text

data['Question'] = data['Question'].apply(preprocess_text)

# Création des vecteurs

vectorizer = CountVectorizer()
X = vectorizer.fit_transform(data['Question'])

# Entraînement du SVM

clf = svm.SVC(kernel='linear')
clf.fit(X, data['Réponse'])

# Fonction de prédiction

def predict(text):
    text = preprocess_text(text)
    x = vectorizer.transform([text])
    return clf.predict(x)[0]

# Interface utilisateur

print('Bienvenue dans notre chatbot étudiant !')
while True:
    question = input('Posez votre question : ')
    réponse = predict(question)
    print(réponse)
