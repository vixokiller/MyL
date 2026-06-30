import sqlite3
from pathlib import Path
from cards import Card

DB_PATH = Path(__file__).with_name("cards.db")

def connect():
    connection = sqlite3.connect(DB_PATH)
    connection.row_factory = sqlite3.Row
    return connection

def create_tables():
    connection = connect()
    cursor = connection.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS cards (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    type TEXT NOT NULL,
    cost INTEGER,
    frequency TEXT NOT NULL,
    ability TEXT,
    strength INTEGER,
    race TEXT,
    code TEXT NOT NULL,
    illustrator TEXT NOT NULL,
    edition TEXT NOT NULL,
    epic_text TEXT,
    product TEXT NOT NULL,
    image TEXT
    valid INTEGER NOT NULL DEFAULT 1
)
""")

    connection.commit()
    connection.close()

def insert_card(card):
    connection = connect()
    cursor = connection.cursor()

    cursor.execute("""
    INSERT OR IGNORE INTO cards (
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
    )
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
    card["name"],
    card["type"],
    card["cost"],
    card["frequency"],
    card["ability"],
    card["strength"],
    card["race"],
    card["code"],
    card["illustrator"],
    card["edition"],
    card["epic_text"],
    card["product"],
    card["image"],
    int(card.get("valid", 1))
    ))

    connection.commit()
    connection.close()

def get_all_cards():
    connection = connect()
    cursor = connection.cursor()

    cursor.execute("SELECT * FROM cards")
    rows = cursor.fetchall()

    connection.close()

    cards = []

    for row in rows:
        card = Card.from_row(row)
        cards.append(card)

    return cards

def get_card_code(code):
    connection = connect()
    cursor = connection.cursor()

    cursor.execute("SELECT * FROM cards WHERE code = ?", (code,))
    row = cursor.fetchone()

    connection.close()

    if row is None:
        return None
    return Card.from_row(row)

def add_valid_column_if_not_exists():
    with connect() as connection:
        cursor = connection.cursor()

        cursor.execute("PRAGMA table_info(cards)")
        columns = cursor.fetchall()

        column_names = [column["name"] for column in columns]

        if "valid" not in column_names:
            cursor.execute("""
            ALTER TABLE cards
            ADD COLUMN valid INTEGER NOT NULL DEFAULT 1
            """)

            connection.commit()
            print("Column 'valid' added successfully.")
        else:
            print("Column 'valid' already exists.")

def update_card_field(code, field, new_value):
    allowed_fields = [
        "name",
        "type",
        "cost",
        "frequency",
        "ability",
        "strength",
        "race",
        "illustrator",
        "edition",
        "epic_text",
        "product",
        "image",
        "valid"
    ]

    if field not in allowed_fields:
        print("Field not allowed.")
        return

    with connect() as connection:
        cursor = connection.cursor()

        query = f"UPDATE cards SET {field} = ? WHERE code = ?"
        cursor.execute(query, (new_value, code))

        connection.commit()

        if cursor.rowcount == 0:
            print("No card found with that code.")
        else:
            print(f"Card field '{field}' updated successfully.")