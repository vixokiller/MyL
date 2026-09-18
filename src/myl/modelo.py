from enum import Enum

class Zona(Enum):
    MAZO = "Mazo"
    MANO = "Mano"
    CEMENTERIO = "Cementerio"
    DESTIERRO = "Destierro"
    LINEA_APOYO = "Linea de Apoyo"
    LINEA_DEFENSA = "Linea de Defensa"
    LINEA_ATAQUE = "Linea de Ataque"

class DefinicionCarta:
    def __init__(self, nombre, tipo, coste, fuerza):
        self.nombre = nombre
        self.tipo = tipo
        self.coste = coste
        self.fuerza = fuerza

    def __str__(self):
        return (
            f"Nombre: {self.nombre}\nTipo: {self.tipo}\n"
            + f"Coste: {self.coste}\nFuerza: {self.fuerza}"
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