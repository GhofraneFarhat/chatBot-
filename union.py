import mysql.connector
import jsonlines

# Connect to MySQL database
db = mysql.connector.connect(
    host="127.0.0.1",
    port=3306,
    user="root",
    password="Ghofrane123!",
    database="pcd"
)

# Create a cursor object
cursor = db.cursor()



def jsonl_update():
    table=input("donner le nom de la table\n")
# Select all rows from the table
    query = '''SELECT question, reponse FROM professeur 
            UNION
            SELECT question , reponse FROM etudiant
            Union
            SELECT question , reponse FROM event
            
            '''
    cursor.execute(query)
    rows = cursor.fetchall()
    # Get the column names from the cursor description
    column_names = [x[0] for x in cursor.description]

    # Create a list of dictionaries to store the rows
    data = []
    for row in rows:
        row_dict = {}
        for i in range(len(column_names)):
            row_dict[column_names[i]] = row[i]
        data.append(row_dict)

    # Write the data to a JSONL file
    with jsonlines.open(f"{table}.jsonl", mode='w') as writer:
        writer.write_all(data)
        

jsonl_update()
print("jsonl updated")    
# Close the cursor and database connections
cursor.close()
db.close()