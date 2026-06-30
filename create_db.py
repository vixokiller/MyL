import sqlite3

connection = sqlite3.connect("cards.db")
cursor = connection.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS cards (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    type TEXT NOT NULL,
    cost INTEGER,
    frequency TEXT,
    ability TEXT,
    strength INTEGER,
    race TEXT,
    code TEXT,
    illustrator TEXT,
    edition TEXT,
    epic_text TEXT,
    product TEXT,
    image TEXT
)
""")

initials_cards = [
    (
        "Dragón Dorado",
        "Talismán",
        0,
        "Rework",
        "Cuando juegues Dragón Dorado, destiérralo. Dragón Dorado puede ser jugado en cualquier momento para anular una carta. Carta Unica.",
        None,
        None,
        "TK1-01-13",
        "Chaman",
        "Espada Sagrada",
        "Algunos lo llaman leyenda, otros fantasía, pero sólo él guarda la clave de la vida eterna, alejado de los mundanales problemas de los vivos.",
        "Toolkit 2022: Red de Plata",
        "assets/Toolkit 2022: Red de Plata/Dragon-dorado-rework-rework.webp-1762835071291"
    ),
    (
        "Gaitas",
        "Oro",
        None,
        "Real",
        "En la Fase Final puedes agrupar este Oro.",
        None,
        None,
        "TK1-02-13",
        "Waldo Retamales",
        "Hijos de Daana",
        "Tu música llama a mi alma, sé donde pertenezco, sé donde debo volver.",
        "Toolkit 2022: Red de Plata",
        "assets/Toolkit 2022: Red de Plata/Gaitas-promocional.webp-1762835190253"
    )
]

cursor.executemany("""
INSERT OR IGNORE INTO cards
(name, type, cost, frequency, ability, strength, race, code, illustrator, edition, epic_text, product, image)
VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
""", initials_cards)

connection.commit()
connection.close()

print("Base de datos creada correctamente.")