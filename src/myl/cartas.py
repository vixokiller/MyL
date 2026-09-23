"""Definiciones e instancias de cartas, zonas y fases del motor."""

from __future__ import annotations

import random
from dataclasses import dataclass, field
from enum import Enum


class Zona(Enum):
    MAZO = "Mazo"
    MANO = "Mano"
    CEMENTERIO = "Cementerio"
    DESTIERRO = "Destierro"
    RESERVA_ORO = "Reserva de Oro"
    ORO_PAGADO = "Oro Pagado"
    LINEA_APOYO = "Linea de Apoyo"
    LINEA_DEFENSA = "Linea de Defensa"
    LINEA_ATAQUE = "Linea de Ataque"


class Fase(Enum):
    AGRUPACION = "Agrupación"
    VIGILIA = "Vigilia"
    BATALLA = "Batalla Mitológica"
    FINAL = "Final"


ZONAS_EN_JUEGO = frozenset(
    {
        Zona.RESERVA_ORO,
        Zona.ORO_PAGADO,
        Zona.LINEA_APOYO,
        Zona.LINEA_DEFENSA,
        Zona.LINEA_ATAQUE,
    }
)


@dataclass(frozen=True)
class DefinicionCarta:
    nombre: str
    tipo: str
    coste: int | None
    fuerza: int | None
    card_id: str | None = None
    raza: str | None = None
    texto: str | None = None
    legalidad: str | None = None

    @property
    def es_oro_inicial(self):
        return (
            self.tipo == "Oro"
            and self.legalidad is not None
            and "Oro Inicial" in self.legalidad
        )

    def __str__(self):
        return (
            f"Nombre: {self.nombre}\nTipo: {self.tipo}\n"
            f"Coste: {self.coste}\nFuerza: {self.fuerza}"
        )


@dataclass
class Modificador:
    atributo: str
    valor: int
    duracion: str = "permanente"
    fuente_id: str | int | None = None


class CartaEnPartida:
    def __init__(self, ID, definicion, propietario, zona_actual):
        self.ID = ID
        self.definicion = definicion
        self.propietario = propietario
        self.controlador = propietario
        self.zona_actual = zona_actual
        self.modificadores: list[Modificador] = []
        self.turno_entrada_en_juego: int | None = None

    def cambiar_de_zona(self, zona_a_cambiar):
        if not isinstance(zona_a_cambiar, Zona):
            raise ValueError("Zona desconocida")
        self.zona_actual = zona_a_cambiar

    @property
    def indestructible(self):
        return self.definicion.nombre == "El Gran Zeus"

    @property
    def tiene_furia(self):
        texto = self.definicion.texto or ""
        return "Puede atacar cuando entra en juego" in texto or "Furia" in texto


def validar_datos_carta(datos):
    if not isinstance(datos, dict):
        raise TypeError("Los datos de la carta deben ser un diccionario")
    obligatorios = ("card_id", "quantity_in_mirror_deck", "name", "type", "cost", "strength")
    for campo in obligatorios:
        if campo not in datos:
            raise ValueError(f"Falta el campo obligatorio: {campo}")
    for campo in ("card_id", "name", "type"):
        valor = datos[campo]
        if not isinstance(valor, str):
            raise TypeError(f"El campo {campo} debe ser texto")
        if not valor.strip():
            raise ValueError(f"El campo {campo} no puede estar vacío")
    cantidad = datos["quantity_in_mirror_deck"]
    if type(cantidad) is not int:
        raise TypeError("La cantidad de copias debe ser un número entero")
    if cantidad <= 0:
        raise ValueError("La cantidad de copias debe ser mayor que cero")
    for campo in ("cost", "strength"):
        valor = datos[campo]
        if valor is not None and type(valor) is not int:
            raise TypeError(f"El campo {campo} debe ser entero o None")
        if valor is not None and valor < 0:
            raise ValueError(f"El campo {campo} no puede ser negativo")


def cargar_definicion(datos):
    validar_datos_carta(datos)
    return DefinicionCarta(
        nombre=datos["name"], tipo=datos["type"], coste=datos["cost"],
        fuerza=datos["strength"], card_id=datos["card_id"], raza=datos.get("race"),
        texto=datos.get("effective_text"), legalidad=datos.get("legality"),
    )


def construir_mazo(datos_cartas, propietario, cantidad_esperada=50):
    if not isinstance(datos_cartas, list):
        raise TypeError("Los datos del mazo deben ser una lista")
    if not isinstance(propietario, str):
        raise TypeError("El propietario debe ser texto")
    if not propietario.strip():
        raise ValueError("El propietario no puede estar vacío")
    if type(cantidad_esperada) is not int:
        raise TypeError("La cantidad esperada debe ser un entero")
    if cantidad_esperada <= 0:
        raise ValueError("La cantidad esperada debe ser mayor que cero")
    mazo = []
    for datos in datos_cartas:
        definicion = cargar_definicion(datos)
        for _ in range(datos["quantity_in_mirror_deck"]):
            mazo.append(CartaEnPartida(f"{propietario}-{len(mazo) + 1}", definicion, propietario, Zona.MAZO))
    if len(mazo) != cantidad_esperada:
        raise ValueError(f"El mazo debe contener {cantidad_esperada} cartas, pero contiene {len(mazo)}")
    return mazo


def barajar_mazo(mazo, semilla=None):
    if not isinstance(mazo, list):
        raise TypeError("El mazo debe ser una lista")
    if not mazo:
        raise ValueError("No se puede barajar un mazo vacío")
    random.Random(semilla).shuffle(mazo)
