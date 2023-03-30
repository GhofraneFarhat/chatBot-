import jsonlines
import numpy as np
from sklearn.svm import SVC
from sklearn.feature_extraction.text import TfidfVectorizer

# Ouvrez le fichier JSONL contenant les questions et les réponses
with jsonlines.open('ensidata.jsonl') as f:
    data = list(f)

# Séparez les questions et les réponses en deux listes distinctes
questions = [d['prompt'] for d in data]
reponses = [d['completion'] for d in data]


# Définir les hyperparamètres
C = 10.0  # Paramètre de régularisation
kernel = 'linear'  # Noyau SVM
gamma = 'scale'

# Préparez les données pour l'entraînement SVM
X = np.array(questions)
y = np.array(reponses)

# Divisez les données en ensembles d'entraînement et de test
from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Préparez les données pour l'entraînement SVM en utilisant NLP
vectorizer = TfidfVectorizer()
X_train_tfidf = vectorizer.fit_transform(X_train)

# Entraînez SVM
clf = SVC(kernel='linear')
clf.fit(X_train_tfidf, y_train)

# Testez le chatbot
X_test_tfidf = vectorizer.transform(X_test)
y_pred = clf.predict(X_test_tfidf)

# Évaluez les performances du chatbot
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
print("Accuracy:", accuracy_score(y_test, y_pred))
print("Precision:", precision_score(y_test, y_pred, average='macro'))
print("Recall:", recall_score(y_test, y_pred, average='macro'))
print("F1 score:", f1_score(y_test, y_pred, average='macro'))

# Utilisez le modèle SVM pour répondre aux questions de l'utilisateur
def get_response(question):
    question_tfidf = vectorizer.transform([question])
    response = clf.predict(question_tfidf)
    return response[0]

# Testez le chatbot en répondant aux questions de l'utilisateur
print(get_response("Who is Imed?"))
print(get_response("Who is nesrine ben yahya?"))
print(get_response("Who is laila horchani?"))
