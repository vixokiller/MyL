import pytest
from dataclasses import FrozenInstanceError

from src.myl.modelo import (
    CartaEnPartida,
    DefinicionCarta,
    Jugador,
    Partida,
    Zona,
    barajar_mazo,
    cargar_definicion,
    construir_mazo,
    validar_datos_carta,
)

def test_carta_conserva_zona_inicial():
    eros = DefinicionCarta(
        "Eros",
        "Aliado",
        2,
        2,
    )

    carta = CartaEnPartida(
        1,
        eros,
        "Jugador_1",
        Zona.MAZO,
    )

    assert carta.zona_actual is Zona.MAZO

def test_cambiar_zona_conserva_propietario():
    eros = DefinicionCarta(
        "Eros",
        "Aliado",
        2,
        2,
    )

    carta = CartaEnPartida(
        1,
        eros,
        "Jugador_1",
        Zona.MAZO,
    )

    propietario_original = carta.propietario

    carta.cambiar_de_zona(Zona.MANO)

    assert carta.zona_actual is Zona.MANO
    assert carta.propietario == propietario_original

def test_dos_copias_comparten_definicion_pero_no_identidad():
    eros = DefinicionCarta(
        "Eros",
        "Aliado",
        2,
        2,
    )

    primera_copia = CartaEnPartida(
        1,
        eros,
        "Jugador_1",
        Zona.MAZO,
    )

    segunda_copia = CartaEnPartida(
        2,
        eros,
        "Jugador_1",
        Zona.MAZO,
    )

    assert primera_copia.ID != segunda_copia.ID
    assert primera_copia.definicion is segunda_copia.definicion
    assert primera_copia is not segunda_copia

def test_partida_conserva_dos_jugadores_diferentes():
    jugador_1 = Jugador("Jugador_1")
    jugador_2 = Jugador("Jugador_2")

    partida = Partida(jugador_1, jugador_2)

    assert len(partida.jugadores) == 2
    assert partida.jugadores[0] is jugador_1
    assert partida.jugadores[1] is jugador_2

def test_partida_rechaza_jugadores_con_mismo_nombre():
    jugador_1 = Jugador("Nombre repetido")
    jugador_2 = Jugador("Nombre repetido")

    with pytest.raises(ValueError):
        Partida(jugador_1, jugador_2)

def test_partida_mueve_carta_del_mazo_a_la_mano():
    eros = DefinicionCarta(
        "Eros",
        "Aliado",
        2,
        2,
    )

    jugador_1 = Jugador("Jugador_1")
    jugador_2 = Jugador("Jugador_2")
    partida = Partida(jugador_1, jugador_2)

    carta = CartaEnPartida(
        1,
        eros,
        jugador_1.nombre,
        Zona.MAZO,
    )

    jugador_1.zonas[Zona.MAZO].append(carta)

    identificador_original = carta.ID
    propietario_original = carta.propietario

    partida.mover_carta(carta, Zona.MANO)

    assert carta not in jugador_1.zonas[Zona.MAZO]
    assert carta in jugador_1.zonas[Zona.MANO]
    assert carta.zona_actual is Zona.MANO

    assert carta.ID == identificador_original
    assert carta.propietario == propietario_original
    apariciones = 0

    for jugador in partida.jugadores:
        for cartas_de_una_zona in jugador.zonas.values():
            apariciones += cartas_de_una_zona.count(carta)

    assert apariciones == 1

def test_partida_rechaza_carta_ajena_sin_modificarla():
    eros = DefinicionCarta(
        "Eros",
        "Aliado",
        2,
        2,
    )

    jugador_1 = Jugador("Jugador_1")
    jugador_2 = Jugador("Jugador_2")
    partida = Partida(jugador_1, jugador_2)

    carta_ajena = CartaEnPartida(
        1,
        eros,
        jugador_1.nombre,
        Zona.MAZO,
    )

    with pytest.raises(
        ValueError,
        match="no pertenece",
    ):
        partida.mover_carta(
            carta_ajena,
            Zona.MANO,
        )

    assert carta_ajena.zona_actual is Zona.MAZO
    assert carta_ajena not in jugador_1.zonas[Zona.MAZO]
    assert carta_ajena not in jugador_1.zonas[Zona.MANO]

def test_partida_rechaza_carta_en_dos_zonas_sin_modificar_estado():
    eros = DefinicionCarta(
        "Eros",
        "Aliado",
        2,
        2,
    )

    jugador_1 = Jugador("Jugador_1")
    jugador_2 = Jugador("Jugador_2")
    partida = Partida(jugador_1, jugador_2)

    carta = CartaEnPartida(
        1,
        eros,
        jugador_1.nombre,
        Zona.MAZO,
    )

    jugador_1.zonas[Zona.MAZO].append(carta)
    jugador_1.zonas[Zona.MANO].append(carta)

    mazo_antes = list(jugador_1.zonas[Zona.MAZO])
    mano_antes = list(jugador_1.zonas[Zona.MANO])
    zona_declarada_antes = carta.zona_actual

    with pytest.raises(
        ValueError,
        match="más de una zona",
    ):
        partida.mover_carta(
            carta,
            Zona.CEMENTERIO,
        )

    assert jugador_1.zonas[Zona.MAZO] == mazo_antes
    assert jugador_1.zonas[Zona.MANO] == mano_antes
    assert jugador_1.zonas[Zona.CEMENTERIO] == []
    assert carta.zona_actual is zona_declarada_antes

def test_definicion_carta_es_inmutable():
    eros = DefinicionCarta(
        "Eros",
        "Aliado",
        2,
        2,
    )

    with pytest.raises(FrozenInstanceError):
        eros.coste = 3

def datos_validos_de_eros():
    return {
        "card_id": "helenica-eros",
        "quantity_in_mirror_deck": 3,
        "name": "Eros",
        "type": "Aliado",
        "cost": 2,
        "strength": 2,
    }

def test_cargar_definicion_acepta_datos_validos():
    datos = datos_validos_de_eros()

    eros = cargar_definicion(datos)

    assert eros.nombre == "Eros"
    assert eros.tipo == "Aliado"
    assert eros.coste == 2
    assert eros.fuerza == 2

def test_validacion_rechaza_campo_faltante():
    datos = datos_validos_de_eros()
    del datos["strength"]

    with pytest.raises(
        ValueError,
        match="Falta el campo obligatorio: strength",
    ):
        validar_datos_carta(datos)

def test_validacion_rechaza_cantidad_cero():
    datos = datos_validos_de_eros()
    datos["quantity_in_mirror_deck"] = 0

    with pytest.raises(
        ValueError,
        match="mayor que cero",
    ):
        validar_datos_carta(datos)

def test_validacion_permite_coste_y_fuerza_ausentes():
    datos = {
        "card_id": "helenica-lira",
        "quantity_in_mirror_deck": 1,
        "name": "Lira",
        "type": "Oro",
        "cost": None,
        "strength": None,
    }

    lira = cargar_definicion(datos)

    assert lira.coste is None
    assert lira.fuerza is None

def datos_de_mazo_pequeno():
    return [
        {
            "card_id": "carta-uno",
            "quantity_in_mirror_deck": 2,
            "name": "Carta Uno",
            "type": "Aliado",
            "cost": 1,
            "strength": 1,
        },
        {
            "card_id": "carta-dos",
            "quantity_in_mirror_deck": 1,
            "name": "Carta Dos",
            "type": "Oro",
            "cost": None,
            "strength": None,
        },
    ]

def test_construir_mazo_crea_todas_las_copias():
    datos = datos_de_mazo_pequeno()

    mazo = construir_mazo(
        datos,
        "Jugador_1",
        cantidad_esperada=3,
    )

    assert len(mazo) == 3

    identificadores = {
        carta.ID
        for carta in mazo
    }

    assert len(identificadores) == 3

    for carta in mazo:
        assert carta.propietario == "Jugador_1"
        assert carta.zona_actual is Zona.MAZO

def test_copias_de_una_carta_comparten_definicion():
    datos = datos_de_mazo_pequeno()

    mazo = construir_mazo(
        datos,
        "Jugador_1",
        cantidad_esperada=3,
    )

    primera_copia = mazo[0]
    segunda_copia = mazo[1]

    assert primera_copia is not segunda_copia

    assert (
        primera_copia.definicion
        is segunda_copia.definicion
    )

def test_construir_mazo_rechaza_cantidad_incorrecta():
    datos = datos_de_mazo_pequeno()

    with pytest.raises(
        ValueError,
        match="debe contener 4 cartas",
    ):
        construir_mazo(
            datos,
            "Jugador_1",
            cantidad_esperada=4,
        )

def test_barajar_mazo_conserva_todas_las_cartas():
    datos = datos_de_mazo_pequeno()

    mazo = construir_mazo(
        datos,
        "Jugador_1",
        cantidad_esperada=3,
    )

    identificadores_antes = {
        carta.ID
        for carta in mazo
    }

    barajar_mazo(
        mazo,
        semilla=123,
    )

    identificadores_despues = {
        carta.ID
        for carta in mazo
    }

    assert len(mazo) == 3

    assert (
        identificadores_despues
        == identificadores_antes
    )

def test_barajar_mazo_cambia_el_orden():
    datos = datos_de_mazo_pequeno()

    mazo = construir_mazo(
        datos,
        "Jugador_1",
        cantidad_esperada=3,
    )

    orden_antes = [
        carta.ID
        for carta in mazo
    ]

    barajar_mazo(
        mazo,
        semilla=123,
    )

    orden_despues = [
        carta.ID
        for carta in mazo
    ]

    assert orden_despues != orden_antes

def test_misma_semilla_produce_mismo_orden():
    datos = datos_de_mazo_pequeno()

    primer_mazo = construir_mazo(
        datos,
        "Jugador_1",
        cantidad_esperada=3,
    )

    segundo_mazo = construir_mazo(
        datos,
        "Jugador_1",
        cantidad_esperada=3,
    )

    barajar_mazo(
        primer_mazo,
        semilla=123,
    )

    barajar_mazo(
        segundo_mazo,
        semilla=123,
    )

    primer_orden = [
        carta.ID
        for carta in primer_mazo
    ]

    segundo_orden = [
        carta.ID
        for carta in segundo_mazo
    ]

    assert primer_orden == segundo_orden

def test_barajar_rechaza_mazo_vacio():
    with pytest.raises(
        ValueError,
        match="mazo vacío",
    ):
        barajar_mazo([])

def test_robar_carta_mueve_la_superior_a_la_mano():
    jugador_1 = Jugador("Jugador_1")
    jugador_2 = Jugador("Jugador_2")

    partida = Partida(
        jugador_1,
        jugador_2,
    )

    mazo = construir_mazo(
        datos_de_mazo_pequeno(),
        jugador_1.nombre,
        cantidad_esperada=3,
    )

    jugador_1.zonas[Zona.MAZO].extend(mazo)

    carta_superior = jugador_1.zonas[
        Zona.MAZO
    ][-1]

    carta_robada = partida.robar_carta(
        jugador_1
    )

    assert carta_robada is carta_superior

    assert len(
        jugador_1.zonas[Zona.MAZO]
    ) == 2

    assert len(
        jugador_1.zonas[Zona.MANO]
    ) == 1

    assert carta_robada not in jugador_1.zonas[
        Zona.MAZO
    ]

    assert carta_robada in jugador_1.zonas[
        Zona.MANO
    ]

    assert carta_robada.zona_actual is Zona.MANO

def test_robar_carta_conserva_identidad_y_propietario():
    jugador_1 = Jugador("Jugador_1")
    jugador_2 = Jugador("Jugador_2")
    partida = Partida(jugador_1, jugador_2)

    mazo = construir_mazo(
        datos_de_mazo_pequeno(),
        jugador_1.nombre,
        cantidad_esperada=3,
    )

    jugador_1.zonas[Zona.MAZO].extend(mazo)

    carta_superior = mazo[-1]
    identificador_original = carta_superior.ID
    propietario_original = carta_superior.propietario
    definicion_original = carta_superior.definicion

    carta_robada = partida.robar_carta(
        jugador_1
    )

    assert carta_robada.ID == identificador_original

    assert (
        carta_robada.propietario
        == propietario_original
    )

    assert (
        carta_robada.definicion
        is definicion_original
    )

def test_robar_carta_rechaza_mazo_vacio():
    jugador_1 = Jugador("Jugador_1")
    jugador_2 = Jugador("Jugador_2")
    partida = Partida(jugador_1, jugador_2)

    with pytest.raises(
        ValueError,
        match="mazo vacío",
    ):
        partida.robar_carta(jugador_1)

    assert jugador_1.zonas[Zona.MAZO] == []
    assert jugador_1.zonas[Zona.MANO] == []

def test_robar_carta_rechaza_jugador_ajeno():
    jugador_1 = Jugador("Jugador_1")
    jugador_2 = Jugador("Jugador_2")
    jugador_ajeno = Jugador("Jugador_3")

    partida = Partida(
        jugador_1,
        jugador_2,
    )

    with pytest.raises(
        ValueError,
        match="no pertenece",
    ):
        partida.robar_carta(
            jugador_ajeno
        )


    
