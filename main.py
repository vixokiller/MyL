from database import get_all_cards, get_card_code, create_tables
from deck import Deck

def main():
    create_tables()

    print("=== Cartas disponibles en la base de datos ===")

    available_cards = get_all_cards()

    for card in available_cards:
        card.show()

main()