import sqlite3

connection = sqlite3.connect("database.db")
cursor = connection.cursor()

cursor.execute("PRAGMA foreign_keys = ON;")
with open('database/schema.sql', 'r') as schema:
    script = schema.read()
cursor.executescript(script)
connection.commit()
connection.close()