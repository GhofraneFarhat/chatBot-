import pandas as pd
import pymysql.cursors

# Connexion à la base de données
connection = pymysql.connect(
    host='localhost',
    user='root',
    password='Ghofrane123!',
    db='professeur',
    charset='utf8mb4',
    cursorclass=pymysql.cursors.DictCursor)

try:
    # Création des tables 1 et 2 en utilisant des requêtes SQL
    with connection.cursor() as cursor:
        # Table 1
        sql = "SELECT question, reponse FROM table1"
        cursor.execute(sql)
        result_table1 = cursor.fetchall()
        table1 = pd.DataFrame(result_table1)

        # Table 2
        sql = "SELECT question, reponse FROM table2"
        cursor.execute(sql)
        result_table2 = cursor.fetchall()
        table2 = pd.DataFrame(result_table2)

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
    with connection.cursor() as cursor:
        sql = "DELETE FROM table1 WHERE question='hey'"
        cursor.execute(sql)
    connection.commit()

    # Suppression des lignes correspondantes de la table 3
    with connection.cursor() as cursor:
        sql = "SELECT question, reponse FROM table1"
        cursor.execute(sql)
        result_table1 = cursor.fetchall()
        table1 = pd.DataFrame(result_table1)

        sql = "SELECT question, reponse FROM table2"
        cursor.execute(sql)
        result_table2 = cursor.fetchall()
        table2 = pd.DataFrame(result_table2)

    table3 = pd.merge(table1, table2, on=['question', 'reponse'], how='outer')

    # Affichage des tables après la suppression
    print("\nTable 1 (après la suppression) :")
    print(table1)
    print("\nTable 3 (après la suppression) :")
    print(table3)

finally:
    # Fermeture de la connexion à la base de données
    connection.close()
