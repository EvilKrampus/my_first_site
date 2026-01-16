import sqlite3

conn = sqlite3.connect("database.db")
cursor = conn.cursor()

cursor.execute(
    "INSERT INTO users (username, password) VALUES (?, ?)",
    ("Mozart", "Admin1147")
)

conn.commit()
conn.close()

print("Пользователь добавлен!")
