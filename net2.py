import json
import re
from bs4 import BeautifulSoup
from textblob import TextBlob

# Lecture des données du fichier JSONL
with open("dataensi.jsonl", "r") as f:
    data = f.readlines()

# Traitement des données
for line in data:
    # Analyse de la ligne JSON
    record = json.loads(line)

    # Extraction du texte à partir de la clé "prompt"
    text = record["prompt"]

    # Suppression des balises HTML
    text = BeautifulSoup(text, "html.parser").get_text()

    # Correction des fautes d'orthographe
    text = str(TextBlob(text).correct())

    # Suppression des mots inutiles
    text = re.sub(r'\b\w{1,2}\b', '', text)

    # Affichage du texte nettoyé
    print(text)
