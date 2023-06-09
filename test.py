from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.svm import SVC
import jsonlines
import pyttsx3 
import numpy as np
from sklearn.metrics import precision_score
import speech_recognition as sr
import mysql.connector

db = mysql.connector.connect(
    host="127.0.0.1",
    port=3306,
    user="root",
    password ="Ghofrane123!",
    database="pcd"
)

# Get teacher information data from MySQL database
cursor = db.cursor()
cursor.execute("SELECT Nom, info FROM professeur")
result = cursor.fetchall()
# Définir les hyperparamètres
C = 10.0  # Paramètre de régularisation
kernel = 'linear'  # Noyau SVM
gamma = 'scale'

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

# Entraîner le modèle SVM
model = SVC(kernel='linear', C=10.0, gamma='scale')
model.fit(X_train_tfidf, y_train)

# Testez le chatbot
X_test_tfidf = vectorizer.transform(X_test)
y_pred = model.predict(X_test_tfidf)


# Initialiser le moteur de synthèse vocale
engine = pyttsx3.init()

# engine.setProperty('voice', voices[2h].id)  # Set to a French voice
engine.setProperty('rate', 155)     # setting up new voice rate
engine.setProperty('volume',1.0)    # setting up volume level  between 0 and 1

voices = engine.getProperty('voices')       #getting details of current voice
engine.setProperty('voice', voices[0].id)  #changing index, changes voices. o for male
#engine.setProperty('voice', voices[1].id)   #changing index, changes voices. 1 for female
engine.setProperty('voice', voices[2].id)  # Set to a French voice
print(len(voices))
def rec():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        try:
            print('Say something...')
            audio = r.listen(source, timeout=5)
            text = r.recognize_google(audio)
            return text
        except sr.WaitTimeoutError:
            print("Sorry, I didn't hear anything. Please try again.")
        except sr.UnknownValueError:
            print("Sorry, I couldn't understand what you said. Please try again.")
        except sr.RequestError:
            print("Sorry, there was an issue with the speech recognition service. Please try again later.")
        except sr.MicrophoneError:
            print("Sorry, the microphone is not connected or is not working properly. Please check your microphone and try again.")
        except sr.AudioTimeoutError:
            print("Sorry, the audio input timed out. Please try again.")


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
    speak_answer("Proposer votre question")
    question = input()
    result = predict_answer(question)
    print("Question Proposée est:", result["question_data"])
    print("reponse :", result["answer"])
    speak_answer(result["answer"])
    
