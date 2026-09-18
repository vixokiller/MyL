import json

from src.myl.modelo import (
    Jugador,
    Partida,
    Zona,
    barajar_mazo,
    construir_mazo,
)

with open(
    "catalog/cards.provisional.json",
    encoding="utf-8",
) as archivo:
    datos_catalogo = json.load(archivo)


if not isinstance(datos_catalogo, dict):
    raise TypeError(
        "El catálogo debe contener un objeto JSON"
    )

if "cards" not in datos_catalogo:
    raise ValueError(
        "El catálogo no contiene el campo cards"
    )

if not isinstance(datos_catalogo["cards"], list):
    raise TypeError(
        "El campo cards debe contener una lista"
    )


cartas_del_catalogo = datos_catalogo["cards"]

if len(cartas_del_catalogo) == 0:
    raise ValueError(
        "El catálogo no puede estar vacío"
    )


datos_scope = datos_catalogo["scope"]
cantidad_esperada = datos_scope["total_copies"]
definiciones_esperadas = datos_scope["distinct_cards"]

if len(cartas_del_catalogo) != definiciones_esperadas:
    raise ValueError(
        "La cantidad de definiciones no coincide con scope"
    )


jugador_1 = Jugador("Jugador_1")
jugador_2 = Jugador("Jugador_2")

partida = Partida(
    jugador_1,
    jugador_2,
)

mazo = construir_mazo(
    cartas_del_catalogo,
    jugador_1.nombre,
)

jugador_1.zonas[Zona.MAZO].extend(mazo)

barajar_mazo(
    jugador_1.zonas[Zona.MAZO]
)

cantidad_mazo_antes = len(
    jugador_1.zonas[Zona.MAZO]
)

cantidad_mano_antes = len(
    jugador_1.zonas[Zona.MANO]
)

carta_superior_antes = (
    jugador_1.zonas[Zona.MAZO][-1]
)

carta_robada = partida.robar_carta(
    jugador_1
)

assert carta_robada is carta_superior_antes

assert len(
    jugador_1.zonas[Zona.MAZO]
) == cantidad_mazo_antes - 1

assert len(
    jugador_1.zonas[Zona.MANO]
) == cantidad_mano_antes + 1

assert carta_robada not in jugador_1.zonas[Zona.MAZO]
assert carta_robada in jugador_1.zonas[Zona.MANO]
assert carta_robada.zona_actual is Zona.MANO

apariciones = 0

for cartas_de_una_zona in jugador_1.zonas.values():
    apariciones += cartas_de_una_zona.count(
        carta_robada
    )

assert apariciones == 1

print(
    "Carta robada:",
    carta_robada.definicion.nombre,
)

print(
    "Cartas en el Mazo:",
    len(jugador_1.zonas[Zona.MAZO]),
)

print(
    "Cartas en la Mano:",
    len(jugador_1.zonas[Zona.MANO]),
)