"""Estado que pertenece a cada jugador."""

from .cartas import Zona


class Jugador:
    def __init__(self, nombre):
        if not isinstance(nombre, str) or not nombre.strip():
            raise ValueError("El nombre del jugador no puede estar vacío")
        self.nombre = nombre
        self.zonas = {zona: [] for zona in Zona}
        self.mano_conservada = False

