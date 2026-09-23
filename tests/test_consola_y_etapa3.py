import pytest

from src.myl.consola import JuegoConsola
from src.myl.modelo import CartaEnPartida, DefinicionCarta, Fase, Jugador, Partida, Zona


def poner(jugador, identificador, nombre, tipo="Aliado", zona=Zona.LINEA_DEFENSA,
          coste=0, fuerza=1, raza=None, texto=None):
    carta = CartaEnPartida(identificador,
        DefinicionCarta(nombre, tipo, coste, fuerza, raza=raza, texto=texto),
        jugador.nombre, zona)
    jugador.zonas[zona].append(carta)
    return carta


def juego():
    a, b = Jugador("A"), Jugador("B")
    partida = Partida(a, b, semilla=1)
    partida.iniciar_primer_turno(a)
    return a, b, partida


def test_consola_ejecuta_comandos_sin_acoplar_input_global():
    a, _, partida = juego(); mensajes = []
    oro = poner(a, "oro", "Oro", "Oro", Zona.MANO, None, None)
    consola = JuegoConsola(partida, entrada=lambda _: "", salida=mensajes.append)
    consola.ejecutar_comando("oro 1")
    consola.ejecutar_comando("estado")
    assert oro in a.zonas[Zona.RESERVA_ORO]
    assert any("Turno 1" in mensaje for mensaje in mensajes)


def test_helios_suma_dos_a_olimpicos():
    a, _, partida = juego()
    aliado = poner(a, "aliado", "Aliado", fuerza=2, raza="Olímpico")
    poner(a, "helios", "Helios", fuerza=2, raza="Olímpico")
    assert partida.fuerza_actual(aliado) == 4


def test_fenix_vuelve_del_cementerio_pagando_su_coste():
    a, _, partida = juego()
    fenix = poner(a, "fenix", "Fénix", zona=Zona.CEMENTERIO, coste=2, fuerza=2)
    for i in range(2): poner(a, f"oro-{i}", "Oro", "Oro", Zona.RESERVA_ORO, None, None)
    partida.usar_habilidad(a, fenix)
    assert fenix in a.zonas[Zona.LINEA_DEFENSA]
    assert len(a.zonas[Zona.ORO_PAGADO]) == 2


def test_titanes_fija_fuerza_cero_hasta_fase_final():
    a, b, partida = juego()
    titanes = poner(a, "titanes", "Titanes", "Oro", Zona.RESERVA_ORO, None, None)
    objetivo = poner(b, "objetivo", "Objetivo", fuerza=4)
    partida.usar_habilidad(a, titanes, objetivo=objetivo)
    assert partida.fuerza_actual(objetivo) == 0
    partida.fase = Fase.FINAL
    partida.finalizar_turno()
    assert partida.fuerza_actual(objetivo) == 4


def test_thanatos_destruye_todos_los_aliados_del_nombre_salvo_indestructible():
    a, b, partida = juego()
    thanatos = poner(a, "thanatos", "Thanatos", fuerza=2)
    copias = [poner(a, "x1", "Guardián"), poner(b, "x2", "Guardián")]
    destruidos = partida.usar_habilidad(a, thanatos, nombre_objetivo="Guardián")
    assert destruidos == copias
    assert copias[0] in a.zonas[Zona.CEMENTERIO]
    assert copias[1] in b.zonas[Zona.CEMENTERIO]


def test_lyssa_retira_atacante_durante_guerra():
    a, b, partida = juego(); partida.avanzar_fase(True)
    atacante = poner(a, "atacante", "Atacante", fuerza=2)
    lyssa = poner(b, "lyssa", "Lyssa", fuerza=2)
    partida.declarar_atacante(a, atacante); partida.iniciar_guerra_talismanes()
    partida.usar_habilidad(b, lyssa, atacante=atacante)
    assert atacante in a.zonas[Zona.LINEA_DEFENSA]
    assert lyssa in b.zonas[Zona.CEMENTERIO]


def test_ares_cancela_ataque_pagando_dos():
    a, b, partida = juego(); partida.avanzar_fase(True)
    atacante = poner(a, "atacante", "Atacante", fuerza=2)
    ares = poner(b, "ares", "Ares", fuerza=2)
    for i in range(2): poner(b, f"oro-{i}", "Oro", "Oro", Zona.RESERVA_ORO, None, None)
    partida.declarar_atacante(a, atacante); partida.iniciar_guerra_talismanes()
    partida.usar_habilidad(b, ares)
    assert partida.ataque_cancelado
    assert atacante in a.zonas[Zona.LINEA_DEFENSA]


def test_fenix_rechaza_activacion_fuera_del_cementerio():
    a, _, partida = juego(); fenix = poner(a, "fenix", "Fénix", coste=2, fuerza=2)
    with pytest.raises(ValueError, match="Cementerio"):
        partida.usar_habilidad(a, fenix)
