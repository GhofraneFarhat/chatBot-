import pandas as pd
import mysql.connector

# Connecter à la base de données MySQL
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Ghofrane123!",
    database="professeur"
)

# Lire les données depuis une requête SQL
query = "SELECT question, reponse FROM table1 UNION SELECT question , reponse FROM table2"


cursor = conn.cursor()
cursor.execute(query)

# Récupérer les résultats de la requête SQL
results = cursor.fetchall()



df = pd.read_sql(query, conn)

# Afficher les noms des colonnes
print(df.columns)

# Insérer les données dans une table MySQL
cursor = conn.cursor()
for _, row in df.iterrows():
    cursor.execute("INSERT INTO table3 (question, reponse) VALUES (%s, %s)", (row['question'], row['reponse']))
conn.commit()

# Fermer la connexion
cursor.close()
conn.close()
