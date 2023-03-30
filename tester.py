import pandas as pd

# Création des tables 1 et 2
table1 = pd.DataFrame({'question': ['Quel est votre nom ?', 'Quel âge avez-vous ?', 'Où habitez-vous ?'], 'reponse': ['Je m\'appelle Jean', 'J\'ai 30 ans', 'J\'habite à Paris']})
table2 = pd.DataFrame({'question': ['Quel est votre sport préféré ?', 'Quel est votre plat préféré ?', 'Aimez-vous voyager ?'], 'reponse': ['Mon sport préféré est le football', 'Mon plat préféré est la pizza', 'Oui, j\'adore voyager']})

# Jointure des tables en utilisant les colonnes "question" et "reponse"
table3 = pd.merge(table1, table2, on=['question', 'reponse'], how='outer')

# Affichage des tables avant la suppression
print("Table 1 :")
print(table1)
print("\nTable 2 :")
print(table2)
print("\nTable 3 (avant la suppression) :")
print(table3)

# Suppression d'une ligne de la table 1
table1 = table1.drop(1)

# Suppression des lignes correspondantes de la table 3
table3 = pd.merge(table1, table2, on=['question', 'reponse'], how='outer')

# Affichage des tables après la suppression
print("\nTable 1 (après la suppression) :")
print(table1)
print("\nTable 3 (après la suppression) :")
print(table3)
