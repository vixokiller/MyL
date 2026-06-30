import sqlite3
from pathlib import Path

BASE_DIR = Path(__file__).parent
DB_PATH = BASE_DIR / "cards.db"


def connect():
    connection = sqlite3.connect(DB_PATH)
    connection.row_factory = sqlite3.Row
    return connection


def get_cards(search_text=""):
    connection = connect()
    cursor = connection.cursor()

    if search_text:
        cursor.execute("""
            SELECT 
                id,
                name,
                type,
                cost,
                frequency,
                ability,
                strength,
                race,
                code,
                illustrator,
                edition,
                epic_text,
                product,  
                image,
                valid
            FROM cards
            WHERE valid = 1
            AND (
                name LIKE ?
                OR type LIKE ?
                OR ability LIKE ?
            )
            ORDER BY id DESC
        """, (f"%{search_text}%", f"%{search_text}%", f"%{search_text}%"))
    else:
        cursor.execute("""
            SELECT 
                id,
                name,
                type,
                cost,
                frequency,
                ability,
                strength,
                race,
                code,
                illustrator,
                edition,
                epic_text,
                product,  
                image,
                valid
            FROM cards
            WHERE valid = 1
            ORDER BY id DESC
        """)

    cards = [dict(row) for row in cursor.fetchall()]
    connection.close()
    return cards