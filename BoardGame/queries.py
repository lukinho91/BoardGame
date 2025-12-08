import sqlite3

conn = sqlite3.connect("game.db")
c = conn.cursor()

# SQL lekérdezés: összes pont lekérése
c.execute("SELECT * FROM positions")
rows = c.fetchall()

for row in rows:
    print(row)

conn.close()