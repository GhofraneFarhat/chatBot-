import jsonlines
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn import svm

# Lire les données à partir du fichier JSONL
with jsonlines.open('dataensi_prepared (2).jsonl') as f:
    data = f.read()

# Séparer les données en features et labels
features = [d['prompt'] for d in data]
labels = [d['completion'] for d in data]

# Vectoriser les données textuelles en utilisant TF-IDF
vectorizer = TfidfVectorizer()
X = vectorizer.fit_transform(features)

# Entrainement du classifieur SVM
clf = svm.SVC()
clf.fit(X, labels)

# Utilisation du classifieur pour prédire une étiquette pour une nouvelle question
new_question = "Where is cpc of the ENSI located?"
X_new = vectorizer.transform([new_question])
predicted_label = clf.predict(X_new)

print(predicted_label)
