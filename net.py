import re
import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from textblob import TextBlob
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.svm import LinearSVC

nltk.download('stopwords')
nltk.download('wordnet')

# Fonction de prétraitement des données
def preprocess(text):
    # Supprimer les caractères spéciaux
    text = re.sub('[^a-zA-Z]', ' ', text)
    
    # Supprimer les espaces supplémentaires
    text = re.sub(r'\s+', ' ', text)
    
    # Convertir tous les caractères en minuscule
    text = text.lower()
    
    # Supprimer les mots inutiles (stopwords)
    words = text.split()
    words = [word for word in words if word not in stopwords.words('english')]
    text = ' '.join(words)
    
    # Correction d'orthographe
    text = str(TextBlob(text).correct())
    
    # Supprimer les balises HTML
    text = BeautifulSoup(text, 'html.parser').get_text()
    
    # Élimination des doublons
    text_list = list(set(text.split()))
    text = ' '.join(text_list)
    
    # Lemmatisation
    lemmatizer = WordNetLemmatizer()
    words = text.split()
    words = [lemmatizer.lemmatize(word) for word in words]
    text = ' '.join(words)
    
    return text

# Données d'entraînement
train_data = [
    ("Bonjour", "salutation"),
    ("Comment vas-tu ?", "salutation"),
    ("Quel est ton nom ?", "nom"),
    ("Je m'appelle Paul", "nom"),
    ("Quel temps fait-il aujourd'hui ?", "météo"),
    ("Il fait beau et chaud", "météo"),
    ("Quelle est la capitale de la France ?", "géographie"),
    ("La capitale de la France est Paris", "géographie")
]

# Prétraitement des données d'entraînement
X_train = []
y_train = []

for sentence, intent in train_data:
    X_train.append(preprocess(sentence))
    y_train.append(intent)

# Vectorisation des données d'entraînement
vectorizer = TfidfVectorizer()
X_train = vectorizer.fit_transform(X_train)

# Entraînement du modèle SVM
model = LinearSVC()
model.fit(X_train, y_train)

# Données de test
test_data = [
    "Bonjour, comment ça va ?",
    "Quel est le nom de ton créateur ?",
    "Il pleut aujourd'hui ?",
    "Où se trouve la tour Eiffel ?"
]

# Prétraitement des données de test
X_test = []
for sentence in test_data:
    X_test.append(preprocess(sentence))

# Vectorisation des données de test
X_test = vectorizer.transform(X_test)

# Prédiction des intentions
y_pred = model.predict(X_test)

# Affichage des résultats
for i in range(len(test_data)):
    print("Phrase : " + test_data[i])
    print("Intention : " + y_pred[i])
    print("\n")
