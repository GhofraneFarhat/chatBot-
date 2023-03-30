from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.svm import SVC
import jsonlines

# Charger les données d'entraînement
with jsonlines.open("dataensi_prepared (2).jsonl") as f:
    data = list(f)

# Diviser les données en entrées (X) et sorties (y)
X = [d['prompt'] for d in data]
y = [d['completion'] for d in data]

# Créer le vecteur Tfidf
vectorizer = TfidfVectorizer()
X = vectorizer.fit_transform(X)

# Entraîner le modèle SVM
model = SVC(kernel='linear', C=1.0, gamma='scale')
model.fit(X, y)

# Fonction pour prédire la réponse à une question donnée
def predict_answer(question):
    question_vec = vectorizer.transform([question])
    answer = model.predict(question_vec)
    return answer[0]

# Exemple d'utilisation
while True:
    question = input("Posez votre question : ")
    answer = predict_answer(question)
    print(answer)
