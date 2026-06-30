from database import create_tables, add_valid_column_if_not_exists, insert_card, update_card_field

update_card_field("TK1-04-13", "name", "Forma de Toro")
update_card_field("ZOMBIE-TK-02", "valid", 0)