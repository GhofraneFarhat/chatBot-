from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.svm import SVC
import pyttsx3 
import speech_recognition as sr
from sklearn.model_selection import train_test_split
import jsonlines
import webbrowser

etudiant = "https://ensi.rnu.tn/"
event= "https://www.facebook.com/"
result = "https://miktex.org/download"
prof = "https://github.com/"
with jsonlines.open("eventt.jsonl") as f:
    data = list(f)
# Diviser les données en entrées (X) et sorties (y)

X = [d['question'] for d in data]
y = [d['reponse'] for d in data]
x=X
# Définir les hyperparamètres
C = 10.0  # Paramètre de régularisation
kernel = 'linear'  # Noyau SVM
gamma = 'scale'
# Divisez les données en ensembles d'entraînement et de test
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


def rec():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        try:
            print('En français svp...')
            audio = r.listen(source,  phrase_time_limit=5)
            text = r.recognize_google(audio, language='fr-FR')
            print(text)
            return text
        except sr.WaitTimeoutError:
            print("Je suis désolé, mais j'ai rien entendu, pourriez vous répéter svp")
        except sr.UnknownValueError:
            print("Je suis désolé, jai rien compris, essayer une autre fois svp")
        except sr.RequestError:
            print("erreur, essayer une autre fois, svp.")
        except sr.MicrophoneError:
            print("Désolé, votre microphone n'est pas connecté, essayer de corriger l'erreur, svp.")
        except sr.AudioTimeoutError:
            print("Désolé, vous avez dépassez le temps.")


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
    question = rec()
    #question=input("Votre question:   ")
    result = predict_answer(question)
    print("Question Proposée est:", result["question_data"])
    print("reponse :", result["answer"])
    speak_answer(result["answer"])
    if result['answer']=='events':
        webbrowser.open(event)
        break
    '''elif result['answer']=="result_exam":
        webbrowser.open(result_pcd)
        break
    '''