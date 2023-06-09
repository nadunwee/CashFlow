import mysql.connector

mydb = mysql.connector.connect(
    host='localhost',
    user='root',
    passwd= 'password123',
)

cursor = mydb.cursor()

cursor.execute("CREATE DATABASE users")