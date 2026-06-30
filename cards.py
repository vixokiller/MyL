from dataclasses import dataclass, replace

@dataclass
class Card:
    name: str
    type: str
    cost: int
    frequency: str
    ability: str
    strength: int
    race: str
    code: str
    illustrator: str
    edition: str
    epic_text: str
    product: str
    image: str
    valid: bool = True

    @classmethod
    def from_row(cls, row):
        """
        Convierte una fila de la base de datos en un objeto Carta.
        """
        return cls(
            name=row["name"],
            type=row["type"],
            cost=row["cost"],
            frequency=row["frequency"],
            ability=row["ability"],
            strength=row["strength"],
            race=row["race"],
            code=row["code"],
            illustrator=row["illustrator"],
            edition=row["edition"],
            epic_text=row["epic_text"],
            product=row["product"],
            image=row["image"],
            valid=bool(row["valid"])
        )

    def copy(self):
        """
        Crea una copia de la carta.
        Sirve para que un mazo pueda tener varias copias de la misma carta.
        """
        return replace(self)

    def show(self):
        print("---------------------------")
        print(f"Nombre: {self.name}")
        print(f"Tipo: {self.type}")
        print(f"Coste: {self.cost}")
        print(f"Código: {self.code}")
        print("---------------------------")