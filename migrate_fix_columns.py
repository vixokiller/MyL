import sqlite3
from pathlib import Path
import shutil


DB_PATH = Path(__file__).with_name("cards.db")
BACKUP_PATH = Path(__file__).with_name("cards_backup.db")


def get_columns(cursor):
    cursor.execute("PRAGMA table_info(cards)")
    columns = cursor.fetchall()
    return [column["name"] for column in columns]


def migrate():
    if not DB_PATH.exists():
        print("Database file not found.")
        return

    shutil.copy(DB_PATH, BACKUP_PATH)
    print(f"Backup created: {BACKUP_PATH}")

    connection = sqlite3.connect(DB_PATH)
    connection.row_factory = sqlite3.Row
    cursor = connection.cursor()

    columns = get_columns(cursor)

    if "strenght" in columns and "strength" not in columns:
        cursor.execute("""
        ALTER TABLE cards
        RENAME COLUMN strenght TO strength
        """)
        print("Column renamed: strenght → strength")
    else:
        print("Column strength already fixed or old column not found.")

    columns = get_columns(cursor)

    if "ilustrator" in columns and "illustrator" not in columns:
        cursor.execute("""
        ALTER TABLE cards
        RENAME COLUMN ilustrator TO illustrator
        """)
        print("Column renamed: ilustrator → illustrator")
    else:
        print("Column illustrator already fixed or old column not found.")

    connection.commit()
    connection.close()

    print("Migration completed successfully.")


migrate()