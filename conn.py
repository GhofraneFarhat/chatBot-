import mysql.connector
import jsonlines
# Connect to MySQL database
db = mysql.connector.connect(
    host="localhost",
    port=3306,
    user="root",
    password ="Ghofrane123!",
    database="pcd"
)

# Create a cursor object
cursor = db.cursor()

# Insert a question and its response into the table
query = "INSERT INTO professeur (question, reponse) VALUES (%s, %s)"

with jsonlines.open("ensidata2.jsonl") as f:
    data = list(f)
# Diviser les données en entrées (X) et sorties (y)
questions = [d['prompt'] for d in data]
reponses = [d['completion'] for d in data]
for d in data:
    question=d['prompt']
    response=d['completion']
    values = (question, response)
    cursor.execute(query, values)
    db.commit()
# Close the cursor and database connections
cursor.close()
db.close()