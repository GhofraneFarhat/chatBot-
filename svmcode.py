from sklearn import svm
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

# Charger les données à partir du fichier jsonl
import jsonlines
with jsonlines.open('data.jsonl') as f:
    data = list(f)

# Séparer les données en ensembles d'entraînement et de test
train_data, test_data, train_labels, test_labels = train_test_split([x['text'] for x in data], [x['label'] for x in data], test_size=0.2, random_state=42)

# Définir les hyperparamètres
C = 1.0  # Paramètre de régularisation
kernel = 'linear'  # Noyau SVM
gamma = 'scale'  # Coefficient du noyau pour 'rbf', 'poly' et 'sigmoid'

# Entraîner le modèle SVM avec les hyperparamètres spécifiés
clf = svm.SVC(C=C, kernel=kernel, gamma=gamma)
clf.fit(train_data, train_labels)

# Faire des prédictions sur l'ensemble de test
predictions = clf.predict(test_data)

# Calculer l'exactitude des prédictions
accuracy = accuracy_score(test_labels, predictions)
print("Accuracy:", accuracy)
