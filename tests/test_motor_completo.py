import pytest

from src.myl.modelo import (CartaEnPartida, DefinicionCarta, EstadoPendiente,
                            Fase, Jugador, Modificador, Partida, Zona)


def carta(jugador, identificador, nombre="Carta", tipo="Aliado", zona=Zona.MAZO,
          coste=0, fuerza=1, raza=None, texto=None, legalidad=None):
    c = CartaEnPartida(identificador, DefinicionCarta(nombre, tipo, coste, fuerza,
        raza=raza, texto=texto, legalidad=legalidad), jugador.nombre, zona)
    jugador.zonas[zona].append(c)
    return c


def partida():
    a, b = Jugador("A"), Jugador("B")
    return a, b, Partida(a, b, semilla=7)


def llenar_preparacion(jugador):
    oro = carta(jugador, f"{jugador.nombre}-oro", "Lira", "Oro",
                 coste=None, fuerza=None, legalidad="Oro Inicial confirmado")
    for i in range(49): carta(jugador, f"{jugador.nombre}-{i}")
    return oro


def test_preparacion_coordinada_y_mulligan():
    a, b, juego = partida(); llenar_preparacion(a); llenar_preparacion(b)
    juego.preparar_partida()
    assert all(len(j.zonas[Zona.MANO]) == 8 for j in (a, b))
    assert all(len(j.zonas[Zona.MAZO]) == 41 for j in (a, b))
    juego.mulligan(a)
    assert len(a.zonas[Zona.MANO]) == 7 and len(a.zonas[Zona.MAZO]) == 42
    juego.mulligan(a, conservar=True); juego.mulligan(b, conservar=True)
    juego.iniciar_primer_turno()
    assert juego.fase is Fase.VIGILIA


def test_fase_final_expira_descarta_roba_y_cierra_turno():
    a, b, juego = partida(); juego.iniciar_primer_turno(a)
    juego.numero_turno = 2; juego.fase = Fase.FINAL
    fuente = carta(a, "fuente", zona=Zona.LINEA_DEFENSA)
    fuente.modificadores.append(Modificador("fuerza", 2, "turno"))
    for i in range(9): carta(a, f"mano-{i}", zona=Zona.MANO)
    carta(a, "robo")
    juego.finalizar_turno()
    assert len(a.zonas[Zona.MANO]) == 8
    assert not fuente.modificadores
    assert juego.jugador_activo is b and juego.fase is Fase.AGRUPACION


def test_daño_excedente_vacia_castillo_y_declara_derrota():
    a, b, juego = partida(); juego.iniciar_primer_turno(a); juego.avanzar_fase(True)
    atacante = carta(a, "a", zona=Zona.LINEA_DEFENSA, fuerza=4)
    bloqueador = carta(b, "b", zona=Zona.LINEA_DEFENSA, fuerza=1)
    for i in range(3): carta(b, f"m-{i}")
    juego.declarar_atacante(a, atacante); juego.declarar_bloqueo(b, bloqueador, atacante)
    juego.resolver_combate(atacante)
    assert juego.terminada and juego.ganador is a and juego.perdedor is b


def test_pendiente_puede_anularse_sin_devolver_coste():
    a, _, juego = partida(); juego.iniciar_primer_turno(a)
    oro = carta(a, "oro", "Oro", "Oro", Zona.RESERVA_ORO, None, None)
    talisman = carta(a, "t", "Talismán", "Talismán", Zona.MANO, 1, None)
    pendiente = juego.jugar_carta(a, talisman, resolver=False)
    juego.anular_pendiente(pendiente); juego.resolver_pendiente(pendiente)
    assert pendiente.estado is EstadoPendiente.ANULADA
    assert oro in a.zonas[Zona.ORO_PAGADO] and talisman in a.zonas[Zona.CEMENTERIO]


def test_guerra_prioridad_al_defensor_y_dos_cesiones_la_cierran():
    a, b, juego = partida(); juego.iniciar_primer_turno(a); juego.avanzar_fase(True)
    juego.iniciar_guerra_talismanes()
    assert juego.prioridad is b
    assert juego.ceder_prioridad(b)
    assert not juego.ceder_prioridad(a)
    assert juego.ventana is None


def test_furia_y_multiples_atacantes():
    a, _, juego = partida(); juego.iniciar_primer_turno(a); juego.avanzar_fase(True)
    furia = carta(a, "furia", zona=Zona.LINEA_DEFENSA,
                  texto="Puede atacar cuando entra en juego")
    normal = carta(a, "normal", zona=Zona.LINEA_DEFENSA)
    furia.turno_entrada_en_juego = normal.turno_entrada_en_juego = juego.numero_turno
    juego.declarar_atacante(a, furia)
    with pytest.raises(ValueError, match="Furia"): juego.declarar_atacante(a, normal)


def test_zeus_es_indestructible_y_roba_solo_una_vez():
    a, _, juego = partida(); juego.iniciar_primer_turno(a)
    zeus = carta(a, "zeus", "El Gran Zeus", zona=Zona.LINEA_DEFENSA, fuerza=5)
    carta(a, "m1"); carta(a, "m2")
    assert juego.destruir(zeus) is False
    assert len(juego.usar_habilidad(a, zeus)) == 2
    with pytest.raises(ValueError, match="una vez"): juego.usar_habilidad(a, zeus)


def test_hilo_destruye_fuente_y_destierra_dos_cartas():
    a, b, juego = partida(); juego.iniciar_primer_turno(a)
    hilo = carta(a, "hilo", "Hilo de Ariadna", "Oro", Zona.RESERVA_ORO, None, None)
    objetivos = [carta(b, f"c{i}", zona=Zona.CEMENTERIO) for i in range(2)]
    juego.usar_habilidad(a, hilo, cartas_cementerio=objetivos)
    assert hilo in a.zonas[Zona.CEMENTERIO]
    assert all(c in b.zonas[Zona.DESTIERRO] for c in objetivos)


def test_alastor_debilita_permanentemente_a_quien_lo_destruye():
    a, b, juego = partida(); juego.iniciar_primer_turno(a); juego.avanzar_fase(True)
    alastor = carta(a, "alastor", "Alastor", zona=Zona.LINEA_DEFENSA, fuerza=2)
    bloqueador = carta(b, "bloq", zona=Zona.LINEA_DEFENSA, fuerza=3)
    juego.declarar_atacante(a, alastor); juego.declarar_bloqueo(b, bloqueador, alastor)
    juego.resolver_combate(alastor)
    assert juego.fuerza_actual(bloqueador) == 2


def test_almas_responde_a_la_salida_y_baraja_el_aliado():
    a, _, juego = partida(); juego.iniciar_primer_turno(a)
    for i in range(2): carta(a, f"oro-{i}", "Oro", "Oro", Zona.RESERVA_ORO, None, None)
    almas = carta(a, "almas", "Almas de Estigia", "Talismán", Zona.MANO, 2, None)
    aliado = carta(a, "aliado", zona=Zona.LINEA_DEFENSA)
    juego.destruir(aliado)
    salida = juego.pila[-1]
    respuesta = juego.jugar_respuesta(a, almas, salida, aliado=aliado)
    juego.resolver_pendiente(respuesta)
    assert aliado in a.zonas[Zona.MAZO]
    assert almas in a.zonas[Zona.CEMENTERIO]
