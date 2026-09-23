import pytest

from src.myl.modelo import (
    CartaEnPartida,
    DefinicionCarta,
    Fase,
    Jugador,
    Partida,
    Zona,
)


def crear_carta(
    identificador,
    nombre,
    tipo,
    propietario,
    zona,
    *,
    coste=0,
    fuerza=None,
    raza=None,
    legalidad=None,
):
    definicion = DefinicionCarta(
        nombre,
        tipo,
        coste,
        fuerza,
        card_id=f"prueba-{identificador}",
        raza=raza,
        legalidad=legalidad,
    )
    return CartaEnPartida(
        identificador,
        definicion,
        propietario.nombre,
        zona,
    )


def colocar(jugador, carta):
    jugador.zonas[carta.zona_actual].append(carta)
    return carta


def crear_partida():
    jugador_1 = Jugador("Jugador_1")
    jugador_2 = Jugador("Jugador_2")
    return jugador_1, jugador_2, Partida(jugador_1, jugador_2)


def test_formar_mano_inicial_roba_ocho_sin_duplicar():
    jugador_1, _, partida = crear_partida()
    for numero in range(8):
        colocar(
            jugador_1,
            crear_carta(
                f"carta-{numero}",
                f"Carta {numero}",
                "Aliado",
                jugador_1,
                Zona.MAZO,
                fuerza=1,
            ),
        )

    superior = jugador_1.zonas[Zona.MAZO][-1]
    mano = partida.formar_mano_inicial(jugador_1)

    assert len(mano) == 8
    assert mano[0] is superior
    assert jugador_1.zonas[Zona.MAZO] == []
    assert jugador_1.zonas[Zona.MANO] == mano
    assert len({carta.ID for carta in mano}) == 8
    assert all(carta.zona_actual is Zona.MANO for carta in mano)


def test_mano_inicial_insuficiente_no_modifica_estado():
    jugador_1, _, partida = crear_partida()
    for numero in range(3):
        colocar(
            jugador_1,
            crear_carta(
                numero,
                "Carta",
                "Aliado",
                jugador_1,
                Zona.MAZO,
                fuerza=1,
            ),
        )
    mazo_antes = list(jugador_1.zonas[Zona.MAZO])

    with pytest.raises(ValueError, match="suficientes"):
        partida.formar_mano_inicial(jugador_1)

    assert jugador_1.zonas[Zona.MAZO] == mazo_antes
    assert jugador_1.zonas[Zona.MANO] == []


def test_oro_inicial_valido_pasa_a_reserva():
    jugador_1, _, partida = crear_partida()
    lira = colocar(
        jugador_1,
        crear_carta(
            "lira",
            "Lira",
            "Oro",
            jugador_1,
            Zona.MAZO,
            coste=None,
            legalidad="Oro Inicial confirmado",
        ),
    )

    partida.seleccionar_oro_inicial(jugador_1, lira)

    assert lira not in jugador_1.zonas[Zona.MAZO]
    assert lira in jugador_1.zonas[Zona.RESERVA_ORO]
    assert lira.zona_actual is Zona.RESERVA_ORO


def test_oro_inicial_rechaza_un_oro_no_elegible():
    jugador_1, _, partida = crear_partida()
    oro = colocar(
        jugador_1,
        crear_carta(
            "oro",
            "Oro común",
            "Oro",
            jugador_1,
            Zona.MAZO,
            coste=None,
        ),
    )

    with pytest.raises(ValueError, match="no es elegible"):
        partida.seleccionar_oro_inicial(jugador_1, oro)

    assert oro in jugador_1.zonas[Zona.MAZO]


def test_primer_turno_comienza_en_vigilia_y_alterna_jugador():
    jugador_1, jugador_2, partida = crear_partida()

    partida.iniciar_primer_turno(jugador_1)
    assert partida.fase is Fase.VIGILIA
    assert partida.numero_turno == 1

    partida.avanzar_fase()
    assert partida.fase is Fase.FINAL
    partida.avanzar_fase()

    assert partida.jugador_activo is jugador_2
    assert partida.numero_turno == 2
    assert partida.fase is Fase.AGRUPACION


def test_pagar_oros_es_atomico_y_luego_agrupar_los_recupera():
    jugador_1, _, partida = crear_partida()
    for numero in range(2):
        colocar(
            jugador_1,
            crear_carta(
                f"oro-{numero}",
                "Oro",
                "Oro",
                jugador_1,
                Zona.RESERVA_ORO,
                coste=None,
            ),
        )

    with pytest.raises(ValueError, match="suficientes"):
        partida.pagar_oros(jugador_1, 3)
    assert len(jugador_1.zonas[Zona.RESERVA_ORO]) == 2
    assert jugador_1.zonas[Zona.ORO_PAGADO] == []

    pagados = partida.pagar_oros(jugador_1, 2)
    assert len(pagados) == 2
    assert jugador_1.zonas[Zona.RESERVA_ORO] == []
    partida.agrupar(jugador_1)
    assert len(jugador_1.zonas[Zona.RESERVA_ORO]) == 2
    assert jugador_1.zonas[Zona.ORO_PAGADO] == []


def test_jugar_aliado_paga_coste_mueve_y_registra_eventos():
    jugador_1, _, partida = crear_partida()
    partida.iniciar_primer_turno(jugador_1)
    for numero in range(2):
        colocar(
            jugador_1,
            crear_carta(
                f"oro-{numero}",
                "Oro",
                "Oro",
                jugador_1,
                Zona.RESERVA_ORO,
                coste=None,
            ),
        )
    aliado = colocar(
        jugador_1,
        crear_carta(
            "aliado",
            "Aliado sencillo",
            "Aliado",
            jugador_1,
            Zona.MANO,
            coste=2,
            fuerza=2,
        ),
    )

    partida.jugar_carta(jugador_1, aliado)

    assert aliado in jugador_1.zonas[Zona.LINEA_DEFENSA]
    assert len(jugador_1.zonas[Zona.ORO_PAGADO]) == 2
    tipos = [evento.tipo for evento in partida.eventos]
    assert "coste_pagado" in tipos
    assert "carta_jugada" in tipos
    assert "carta_entrada_en_juego" in tipos


def test_combate_igual_destruye_atacante_y_bloqueador():
    jugador_1, jugador_2, partida = crear_partida()
    partida.iniciar_primer_turno(jugador_1)
    partida.avanzar_fase(iniciar_batalla=True)
    atacante = colocar(
        jugador_1,
        crear_carta(
            "atacante",
            "Atacante",
            "Aliado",
            jugador_1,
            Zona.LINEA_DEFENSA,
            fuerza=2,
        ),
    )
    bloqueador = colocar(
        jugador_2,
        crear_carta(
            "bloqueador",
            "Bloqueador",
            "Aliado",
            jugador_2,
            Zona.LINEA_DEFENSA,
            fuerza=2,
        ),
    )

    partida.declarar_atacante(jugador_1, atacante)
    partida.declarar_bloqueo(jugador_2, bloqueador, atacante)
    partida.resolver_combate(atacante)

    assert atacante in jugador_1.zonas[Zona.CEMENTERIO]
    assert bloqueador in jugador_2.zonas[Zona.CEMENTERIO]


def test_ataque_sin_bloqueo_bota_cartas_del_castillo():
    jugador_1, jugador_2, partida = crear_partida()
    partida.iniciar_primer_turno(jugador_1)
    partida.avanzar_fase(iniciar_batalla=True)
    atacante = colocar(
        jugador_1,
        crear_carta(
            "atacante",
            "Atacante",
            "Aliado",
            jugador_1,
            Zona.LINEA_DEFENSA,
            fuerza=2,
        ),
    )
    for numero in range(3):
        colocar(
            jugador_2,
            crear_carta(
                f"mazo-{numero}",
                "Carta",
                "Aliado",
                jugador_2,
                Zona.MAZO,
                fuerza=1,
            ),
        )

    partida.declarar_atacante(jugador_1, atacante)
    botadas = partida.resolver_combate(atacante)

    assert len(botadas) == 2
    assert len(jugador_2.zonas[Zona.MAZO]) == 1
    assert len(jugador_2.zonas[Zona.CEMENTERIO]) == 2


def test_habilidades_continuas_modifican_fuerza_sin_mutar_base():
    jugador_1, _, partida = crear_partida()
    aliado = colocar(
        jugador_1,
        crear_carta(
            "eros",
            "Eros",
            "Aliado",
            jugador_1,
            Zona.LINEA_DEFENSA,
            fuerza=2,
            raza="Olímpico",
        ),
    )
    for identificador, nombre, zona in (
        ("ofrenda", "Ofrenda a los Dioses", Zona.RESERVA_ORO),
        ("templo", "Templo de la Cazadora", Zona.LINEA_APOYO),
        ("panteon", "Panteón", Zona.LINEA_APOYO),
    ):
        colocar(
            jugador_1,
            crear_carta(
                identificador,
                nombre,
                "Oro" if zona is Zona.RESERVA_ORO else "Tótem",
                jugador_1,
                zona,
                coste=None if zona is Zona.RESERVA_ORO else 3,
            ),
        )

    assert aliado.definicion.fuerza == 2
    assert partida.fuerza_actual(aliado) == 6


def test_eros_busca_dos_oros_al_entrar_en_primer_turno():
    jugador_1, _, partida = crear_partida()
    partida.iniciar_primer_turno(jugador_1)
    eros = colocar(
        jugador_1,
        crear_carta(
            "eros",
            "Eros",
            "Aliado",
            jugador_1,
            Zona.MANO,
            coste=0,
            fuerza=2,
        ),
    )
    for numero in range(2):
        colocar(
            jugador_1,
            crear_carta(
                f"oro-{numero}",
                "Oro",
                "Oro",
                jugador_1,
                Zona.MAZO,
                coste=None,
            ),
        )

    partida.jugar_carta(jugador_1, eros)

    assert len(jugador_1.zonas[Zona.MANO]) == 2
    assert all(
        carta.definicion.tipo == "Oro"
        for carta in jugador_1.zonas[Zona.MANO]
    )


def test_gaia_busca_aliado_y_solo_se_usa_una_vez_por_turno():
    jugador_1, _, partida = crear_partida()
    partida.iniciar_primer_turno(jugador_1)
    gaia = colocar(
        jugador_1,
        crear_carta(
            "gaia",
            "Gaia",
            "Aliado",
            jugador_1,
            Zona.LINEA_DEFENSA,
            coste=4,
            fuerza=2,
        ),
    )
    objetivo = colocar(
        jugador_1,
        crear_carta(
            "objetivo",
            "Eros",
            "Aliado",
            jugador_1,
            Zona.MAZO,
            coste=2,
            fuerza=2,
        ),
    )

    encontradas = partida.usar_habilidad(
        jugador_1,
        gaia,
        nombre_objetivo="Eros",
    )

    assert encontradas == [objetivo]
    assert objetivo in jugador_1.zonas[Zona.MANO]
    with pytest.raises(ValueError, match="una vez por turno"):
        partida.usar_habilidad(jugador_1, gaia)


def test_hemera_permite_reordenar_solo_las_tres_superiores():
    jugador_1, _, partida = crear_partida()
    cartas = []
    for numero in range(4):
        cartas.append(
            colocar(
                jugador_1,
                crear_carta(
                    f"mazo-{numero}",
                    "Carta",
                    "Aliado",
                    jugador_1,
                    Zona.MAZO,
                    fuerza=1,
                ),
            )
        )

    partida.ordenar_tres_superiores(
        jugador_1,
        [cartas[3].ID, cartas[2].ID, cartas[1].ID],
    )

    assert jugador_1.zonas[Zona.MAZO][0] is cartas[0]
    assert jugador_1.zonas[Zona.MAZO][-1] is cartas[1]


def test_festin_descarta_dos_y_roba_una():
    jugador_1, _, partida = crear_partida()
    partida.iniciar_primer_turno(jugador_1)
    festin = colocar(
        jugador_1,
        crear_carta(
            "festin",
            "Festín",
            "Oro",
            jugador_1,
            Zona.RESERVA_ORO,
            coste=None,
        ),
    )
    descartes = []
    for numero in range(2):
        descartes.append(
            colocar(
                jugador_1,
                crear_carta(
                    f"descarte-{numero}",
                    "Descarte",
                    "Aliado",
                    jugador_1,
                    Zona.MANO,
                    fuerza=1,
                ),
            )
        )
    carta_a_robar = colocar(
        jugador_1,
        crear_carta(
            "robo",
            "Robo",
            "Aliado",
            jugador_1,
            Zona.MAZO,
            fuerza=1,
        ),
    )

    robada = partida.usar_habilidad(
        jugador_1,
        festin,
        descartes=descartes,
    )

    assert robada is carta_a_robar
    assert all(
        carta in jugador_1.zonas[Zona.CEMENTERIO]
        for carta in descartes
    )
    assert jugador_1.zonas[Zona.MANO] == [carta_a_robar]


def test_sileno_paga_dos_y_baraja_carta_del_cementerio():
    jugador_1, _, partida = crear_partida()
    partida.iniciar_primer_turno(jugador_1)
    sileno = colocar(
        jugador_1,
        crear_carta(
            "sileno",
            "Sileno",
            "Aliado",
            jugador_1,
            Zona.LINEA_DEFENSA,
            coste=3,
            fuerza=1,
        ),
    )
    for numero in range(2):
        colocar(
            jugador_1,
            crear_carta(
                f"oro-{numero}",
                "Oro",
                "Oro",
                jugador_1,
                Zona.RESERVA_ORO,
                coste=None,
            ),
        )
    objetivo = colocar(
        jugador_1,
        crear_carta(
            "cementerio",
            "Carta recuperada",
            "Aliado",
            jugador_1,
            Zona.CEMENTERIO,
            fuerza=1,
        ),
    )

    partida.usar_habilidad(
        jugador_1,
        sileno,
        carta_cementerio=objetivo,
    )

    assert objetivo in jugador_1.zonas[Zona.MAZO]
    assert len(jugador_1.zonas[Zona.ORO_PAGADO]) == 2


def test_triton_roba_al_salir_del_juego():
    jugador_1, _, partida = crear_partida()
    triton = colocar(
        jugador_1,
        crear_carta(
            "triton",
            "Tritón",
            "Aliado",
            jugador_1,
            Zona.LINEA_DEFENSA,
            coste=3,
            fuerza=1,
        ),
    )
    superior = colocar(
        jugador_1,
        crear_carta(
            "superior",
            "Carta superior",
            "Aliado",
            jugador_1,
            Zona.MAZO,
            fuerza=1,
        ),
    )

    partida.mover_carta(triton, Zona.CEMENTERIO)

    assert triton in jugador_1.zonas[Zona.CEMENTERIO]
    assert superior in jugador_1.zonas[Zona.MANO]
