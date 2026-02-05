import sqlite3
from datetime import datetime

class QuizDatabase:
    def __init__(self, db_name="history.db"):
        self.conn = sqlite3.connect(db_name, check_same_thread=False)
        self.create_table()

    def create_table(self):
        """Crée la table des scores si elle n'existe pas."""
        query = """
        CREATE TABLE IF NOT EXISTS progress (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT,
            role TEXT,
            score INTEGER,
            topic TEXT
        )
        """
        self.conn.execute(query)
        self.conn.commit()

    def save_score(self, role: str, score: int, topic: str):
        """Enregistre une performance."""
        query = "INSERT INTO progress (date, role, score, topic) VALUES (?, ?, ?, ?)"
        self.conn.execute(query, (datetime.now().isoformat(), role, score, topic))
        self.conn.commit()

    def get_stats(self):
        """Récupère l'historique pour l'afficher dans Streamlit."""
        import pandas as pd
        return pd.read_sql_query("SELECT * FROM progress", self.conn)