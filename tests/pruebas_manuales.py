from src.myl.modelo import (
    CartaEnPartida,
    DefinicionCarta,
    Zona,
    Jugador,
    Partida,
)

eros = DefinicionCarta(
    "Eros",
    "Aliado",
    2,
    2,
)

eros_1 = CartaEnPartida(
    1,
    eros,
    "Jugador_1",
    Zona.MAZO,
)

eros_2 = CartaEnPartida(
    2,
    eros,
    "Jugador_1",
    Zona.MAZO,
)

assert eros_1.zona_actual is Zona.MAZO, (
    "Una carta nueva debe conservar la zona indicada"
)
propietario_original = eros_1.propietario
eros_1.cambiar_de_zona(Zona.MANO)
assert eros_1.zona_actual is Zona.MANO, (
    "Mover la carta debe actualizar su zona"
)
assert eros_1.propietario == propietario_original, (
    "Mover una carta no debe cambiar su propietario"
)
assert eros_1.ID != eros_2.ID, (
    "Dos copias físicas deben tener identificadores diferentes"
)
assert eros_1.definicion is eros_2.definicion, (
    "Las copias de Eros deberían compartir su definición"
)
assert eros_1 is not eros_2, (
    "Cada copia física debe ser un objeto diferente"
)
jugador_1 = Jugador("Jugador_1")
jugador_2 = Jugador("Jugador_2")

partida = Partida(jugador_1, jugador_2)
assert len(partida.jugadores) == 2, (
    "Una partida debe contener exactamente dos jugadores"
)

assert partida.jugadores[0] is jugador_1
assert partida.jugadores[1] is jugador_2
error_detectado = False

try:
    jugador_repetido_1 = Jugador("Jugador repetido")
    jugador_repetido_2 = Jugador("Jugador repetido")

    Partida(jugador_repetido_1, jugador_repetido_2)
except ValueError:
    error_detectado = True

assert error_detectado, (
    "La partida debe rechazar jugadores con el mismo nombre"
)
carta_para_mover = CartaEnPartida(
    3,
    eros,
    jugador_1.nombre,
    Zona.MAZO,
)

jugador_1.zonas[Zona.MAZO].append(carta_para_mover)

assert carta_para_mover in jugador_1.zonas[Zona.MAZO]
assert carta_para_mover not in jugador_1.zonas[Zona.MANO]
assert carta_para_mover.zona_actual is Zona.MAZO

propietario_antes_del_movimiento = (
    carta_para_mover.propietario
)

partida.mover_carta(
    carta_para_mover,
    Zona.MANO,
)
assert carta_para_mover not in jugador_1.zonas[Zona.MAZO], (
    "La carta debe desaparecer del Mazo"
)

assert carta_para_mover in jugador_1.zonas[Zona.MANO], (
    "La carta debe aparecer en la Mano"
)

assert carta_para_mover.zona_actual is Zona.MANO, (
    "La carta debe declarar su nueva zona"
)

assert (
    carta_para_mover.propietario
    == propietario_antes_del_movimiento
), "Mover la carta no debe cambiar su propietario"

apariciones = 0

for jugador in partida.jugadores:
    for cartas in jugador.zonas.values():
        apariciones += cartas.count(carta_para_mover)

assert apariciones == 1, (
    "Una carta debe aparecer exactamente en una zona"
)
carta_ajena = CartaEnPartida(
    4,
    eros,
    jugador_1.nombre,
    Zona.MAZO,
)
error_por_carta_ajena = False

try:
    partida.mover_carta(carta_ajena, Zona.MANO)
except ValueError:
    error_por_carta_ajena = True

assert error_por_carta_ajena, (
    "No debe moverse una carta ajena a la partida"
)
assert carta_ajena.zona_actual is Zona.MAZO
print("Todas las pruebas manuales pasaron.")