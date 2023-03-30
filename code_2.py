from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.svm import SVC
import jsonlines
import pyttsx3 
import numpy as np
from sklearn.metrics import precision_score
import mysql.connector
from sklearn.model_selection import train_test_split


# Connect to MySQL database
'''db = mysql.connector.connect(
    host="localhost",
    port=3306,
    user="root",
    password ="Ghofrane123!",
    database="pcd"
)'''


# Get teacher information data from MySQL database
query = '''SELECT question, reponse FROM professeur 
            UNION
            SELECT question , reponse FROM etudiant
            Union
            SELECT question , reponse FROM event
            '''


cursor = db.cursor()
cursor.execute("SELECT Nom, Info FROM professeur")
result = cursor.fetchall()

# Charger les données d'entraînement
with jsonlines.open("event.jsonl") as f:
    data = list(f)
# Diviser les données en entrées (X) et sorties (y)
questions = [d['question'] for d in data]
reponses = [d['reponse'] for d in data]


# Définir les hyperparamètres
C = 10.0  # Paramètre de régularisation
kernel = 'linear'  # Noyau SVM
gamma = 'scale'

# Préparez les données pour l'entraînement SVM
#X = np.array(questions)
'''y = np.array(reponses)    
x=X'''


# Préparez les données pour l'entraînement SVM
X = []
y = []
for row in result:
    X.append(row[0])
    y.append(row[1])  
x=X

# Divisez les données en ensembles d'entraînement et de test
from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Préparez les données pour l'entraînement SVM en utilisant NLP
vectorizer = TfidfVectorizer()
X_train_tfidf = vectorizer.fit_transform(X_train)

# Créer le vecteur Tfidf
#vectorizer = TfidfVectorizer()
#X = vectorizer.fit_transform(X)

# Entraînez SVM
#clf = SVC(kernel='linear')
#clf.fit(X_train_tfidf, y_train)

# Entraîner le modèle SVM
model = SVC(kernel='linear', C=10.0, gamma='scale')
model.fit(X_train_tfidf, y_train)




# Testez le chatbot
X_test_tfidf = vectorizer.transform(X_test)
y_pred = model.predict(X_test_tfidf)

# Évaluez les performances du chatbot
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
print("Accuracy:", accuracy_score(y_test, y_pred))
print("Precision:", precision_score(y_test, y_pred, average='macro'))
print("Recall:", recall_score(y_test, y_pred, average='macro'))
print("F1 score:", f1_score(y_test, y_pred, average='macro'))

# Initialiser le moteur de synthèse vocale
engine = pyttsx3.init()

# engine.setProperty('voice', voices[2h].id)  # Set to a French voice
engine.setProperty('rate', 125)     # setting up new voice rate
engine.setProperty('volume',1.0)    # setting up volume level  between 0 and 1

voices = engine.getProperty('voices')       #getting details of current voice
engine.setProperty('voice', voices[0].id)  #changing index, changes voices. o for male
#engine.setProperty('voice', voices[1].id)   #changing index, changes voices. 1 for female




# Fonction pour prédire la réponse à une question donnée
def predict_answer(question):
    question_vec = vectorizer.transform([question])
    if question_vec.nnz == 0:
        return {"question": question,"question_data":"unknown", "answer": "unknown"}
    answer = model.predict(question_vec)
    pos=0
    for a in y:
        if a==answer:
            question_data=x[pos]
            break
        pos+=1
    return {"question": question,"question_data":question_data, "answer": answer[0]}

# Fonction pour parler la réponse prédite
def speak_answer(answer):
    engine.say(answer)
    engine.runAndWait()

# Exemple d'utilisation
while True:
    speak_answer("Give your question")
    question = input("Posez votre question : ")
    result = predict_answer(question)
    print("Question :", result["question"])
    print("Question Proposed:", result["question_data"])
    print("Answer:", result["answer"])
    speak_answer("Question is")
    speak_answer(result["question"])
    speak_answer("Question Proposed is")
    speak_answer(result["question_data"])
    speak_answer("Answer is")
    speak_answer(result["answer"])
    

