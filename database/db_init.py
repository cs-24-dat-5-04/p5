import sqlite3

connection = sqlite3.connect("database.db")
cursor = connection.cursor()

cursor.execute("PRAGMA foreign_keys = ON;")
with open('database/schema.sql', 'r') as schema:
    createSchema = schema.read()
cursor.executescript(createSchema)
with open('database/boilerplate.sql', 'r') as boilerplate:
    populateDatabase = boilerplate.read()
cursor.executescript(populateDatabase)
connection.commit()
connection.close()