from database import create_tables, add_valid_column_if_not_exists


create_tables()
add_valid_column_if_not_exists()

print("Migration completed.")