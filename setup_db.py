import sqlite3

conn = sqlite3.connect("qa_log.db")
cursor = conn.cursor()

cursor.execute('''
    CREATE TABLE IF NOT EXISTS interactions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        timestamp TEXT DEFAULT CURRENT_TIMESTAMP,
        query TEXT NOT NULL,
        retrieved_chunks TEXT,
        response TEXT,
        answered BOOLEAN DEFAULT 1,
        correctness_score INTEGER,
        completeness_score INTEGER,
        hallucination_flag BOOLEAN DEFAULT 0
    )
''')

conn.commit()
conn.close()
print("Database created successfully: qa_log.db")