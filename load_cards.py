from database import create_tables, add_valid_column_if_not_exists, insert_card

create_tables()
add_valid_column_if_not_exists()

print("Cartas cargadas correctamente.")