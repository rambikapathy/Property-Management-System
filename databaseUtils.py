import sqlite3

#Initialize connection between property window and property database.
def createConnection():
    conn = sqlite3.connect('properties.db')
    return conn
