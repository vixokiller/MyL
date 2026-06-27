import json


CARD_TYPE_VALUES = {
    "Oro": 0,
    "Aliado": 1,
    "Arma": 2,
    "Tótem": 3,
    "Totem": 3,
    "Talismán": 4,
    "Talisman": 4,
}

def load_card_database(filename):
    with open(filename, "r", encoding="utf-8") as file:
        card_data = json.load(file)

    database = {}
    
    for data in card_data:
        database[data["id"]] = data
        
    return database

def create_card_from_data(data, card_classes):
    Card = card_classes["Card"]
    Ally = card_classes["Ally"]
    Gold = card_classes["Gold"]
    card_type = data["type"]

    if card_type == "Oro":
        card = Gold(
            name=data["name"],
            type=0,
            cost=data.get("cost", 0)
        )

    elif card_type == "Aliado":
        card = Ally(
            name=data["name"],
            type=1,
            cost=data["cost"],
            strength=data["strength"]
        )

    else:
        card = Card(
            name=data["name"],
            type=CARD_TYPE_VALUES.get(card_type, card_type),
            cost=data.get("cost", 0)
        )

    card.id = data["id"]
    card.text = data.get("text", "")
    card.abilities = data.get("abilities", [])

    return card


def create_card_by_id(database, card_id, card_classes):
    data = database[card_id]
    return create_card_from_data(data, card_classes)

def load_deck(filename, database, card_classes):
    with open(filename, "r", encoding="utf-8") as file:
        deck_data = json.load(file)

    deck_cards = []

    for item in deck_data:
        card_id = item["card_id"]
        count = item["count"]

        for _ in range(count):
            card = create_card_by_id(database, card_id, card_classes)
            deck_cards.append(card)

    return deck_cards
