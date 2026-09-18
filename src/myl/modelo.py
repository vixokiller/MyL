import random

from dataclasses import dataclass
from enum import Enum

class Zona(Enum):
    MAZO = "Mazo"
    MANO = "Mano"
    CEMENTERIO = "Cementerio"
    DESTIERRO = "Destierro"
    LINEA_APOYO = "Linea de Apoyo"
    LINEA_DEFENSA = "Linea de Defensa"
    LINEA_ATAQUE = "Linea de Ataque"

@dataclass(frozen=True)
class DefinicionCarta:
    nombre: str
    tipo: str
    coste: int | None
    fuerza: int | None

    def __str__(self):
        return (
            f"Nombre: {self.nombre}\nTipo: {self.tipo}\n"
            + f"Coste: {self.coste}\nFuerza: {self.fuerza}"
        )

def validar_datos_carta(datos):
    if not isinstance(datos, dict):
        raise TypeError(
            "Los datos de la carta deben ser un diccionario"
        )

    campos_obligatorios = (
        "card_id",
        "quantity_in_mirror_deck",
        "name",
        "type",
        "cost",
        "strength",
    )

    for campo in campos_obligatorios:
        if campo not in datos:
            raise ValueError (
                f"Falta el campo obligatorio: {campo}"
            )

    campos_de_texto = (
        "card_id",
        "name",
        "type",
    )

    for campo in campos_de_texto:
        valor = datos[campo]

        if not isinstance(valor, str):
            raise TypeError(
                f"El campo {campo} debe ser texto"
            )

        if valor.strip() == "":
            raise ValueError(
                f"El campo {campo} no puede estar vacío"
            )
        
    cantidad = datos["quantity_in_mirror_deck"]

    if type(cantidad) is not int:
        raise TypeError(
            "La cantidad de copias debe ser un número entero"
        )

    if cantidad <= 0:
        raise ValueError(
            "La cantidad de copias debe ser mayor que cero"
        )

    campos_numericos_opcionales = (
        "cost",
        "strength",
    )

    for campo in campos_numericos_opcionales:
        valor = datos[campo]

        if valor is not None and type(valor) is not int:
            raise TypeError(
                f"El campo {campo} debe ser entero o None"
            )

        if valor is not None and valor < 0:
            raise ValueError(
                f"El campo {campo} no puede ser negativo"
            )

def cargar_definicion(datos):
    validar_datos_carta(datos)

    return DefinicionCarta(
        nombre=datos["name"],
        tipo=datos["type"],
        coste=datos["cost"],
        fuerza=datos["strength"],
    )

class CartaEnPartida:
    def __init__(self, ID, definicion, propietario, zona_actual):
        self.ID = ID
        self.definicion = definicion
        self.propietario = propietario
        self.zona_actual = zona_actual

    def cambiar_de_zona(self, zona_a_cambiar):
        if isinstance(zona_a_cambiar, Zona):
            self.zona_actual = zona_a_cambiar        
        else:
            print("Zona desconocida.")

def construir_mazo(
    datos_cartas,
    propietario,
    cantidad_esperada=50,
):
    if not isinstance(datos_cartas, list):
        raise TypeError(
            "Los datos del mazo deben ser una lista"
        )

    if not isinstance(propietario, str):
        raise TypeError(
            "El propietario debe ser texto"
        )

    if propietario.strip() == "":
        raise ValueError(
            "El propietario no puede estar vacío"
        )

    if type(cantidad_esperada) is not int:
        raise TypeError(
            "La cantidad esperada debe ser un entero"
        )

    if cantidad_esperada <= 0:
        raise ValueError(
            "La cantidad esperada debe ser mayor que cero"
        )

    mazo = []
    siguiente_numero = 1
    for datos_carta in datos_cartas:
        definicion = cargar_definicion(datos_carta)
        cantidad = datos_carta[
            "quantity_in_mirror_deck"
        ]
        for _ in range(cantidad):
            identificador = (
                f"{propietario}-{siguiente_numero}"
            )

            carta = CartaEnPartida(
                identificador,
                definicion,
                propietario,
                Zona.MAZO,
            )

            mazo.append(carta)
            siguiente_numero += 1

    if len(mazo) != cantidad_esperada:
        raise ValueError(
            "El mazo debe contener "
            f"{cantidad_esperada} cartas, "
            f"pero contiene {len(mazo)}"
        )

    return mazo

def barajar_mazo(mazo, semilla=None):
    if not isinstance(mazo, list):
        raise TypeError(
            "El mazo debe ser una lista"
        )

    if len(mazo) == 0:
        raise ValueError(
            "No se puede barajar un mazo vacío"
        )

    generador = random.Random(semilla)
    generador.shuffle(mazo)
    
class Jugador:
    def __init__(self, nombre):
        self.nombre = nombre
        self.zonas = {
            Zona.MAZO: [],
            Zona.MANO: [],
            Zona.CEMENTERIO: [],
        }

class Partida:
    def __init__(self, jugador_1, jugador_2):
        if jugador_1.nombre == jugador_2.nombre:
            raise ValueError(
                "Los jugadores deben tener nombres diferentes"
            )

        self.jugadores = [jugador_1, jugador_2]
        
    def mover_carta(self, carta, zona_destino):
        if not isinstance(zona_destino, Zona):
            raise ValueError("La zona de destino no es válida")

        ubicaciones = []

        for jugador in self.jugadores:
            for zona, cartas in jugador.zonas.items():
                if carta in cartas:
                    ubicaciones.append((jugador, zona))

        if len(ubicaciones) == 0:
            raise ValueError("La carta no pertenece a esta partida")

        if len(ubicaciones) > 1:
            raise ValueError("La carta aparece en más de una zona")

        jugador, zona_origen = ubicaciones[0]

        if zona_destino not in jugador.zonas:
            raise ValueError(
                "El jugador no posee la zona de destino"
            )

        if carta.zona_actual is not zona_origen:
            raise ValueError(
                "La zona de la carta no coincide con su ubicación"
            )

        if zona_origen is zona_destino:
            return

        jugador.zonas[zona_origen].remove(carta)
        jugador.zonas[zona_destino].append(carta)
        carta.cambiar_de_zona(zona_destino)

    def robar_carta(self, jugador):
        if jugador not in self.jugadores:
            raise ValueError(
                "El jugador no pertenece a esta partida"
            )

        mazo = jugador.zonas[Zona.MAZO]

        if len(mazo) == 0:
            raise ValueError(
                "No se puede robar de un mazo vacío"
            )

        carta_superior = mazo[-1]

        self.mover_carta(
            carta_superior,
            Zona.MANO,
        )

        return carta_superior