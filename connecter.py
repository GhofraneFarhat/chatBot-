import pandas as pd
import mysql.connector

# Se connecter à la base de données
connection = mysql.connector.connect(
    host='localhost',
    user="root",
    password ="Ghofrane123!",
    database="pcd"
)

# Exécuter la requête SQL pour joindre les tables
query = '''
SELECT Nom, Info, NULL as Email
FROM professeur
UNION
SELECT Name, Email as Info, NULL as Info
FROM etudiant
'''



cursor = connection.cursor()
cursor.execute(query)

# Récupérer les résultats de la requête SQL
results = cursor.fetchall()

# Créer un DataFrame pandas à partir des résultats
df = pd.DataFrame(results, columns=['question', 'reponse'])

# Insérer les résultats dans une nouvelle table
df.to_sql('table3', connection, if_exists='replace', index=False)

# Fermer la connexion à la base de données
cursor.close()
connection.close()
