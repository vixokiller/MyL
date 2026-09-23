"""Registro de habilidades de cartas.

Las funciones reciben la partida, el controlador y la fuente. Agregar una carta
ya no requiere añadir ramas por nombre dentro de :class:`Partida`.
"""

from .cartas import Modificador, Zona, barajar_mazo


ENTRADA = {}
SALIDA = {}
ACTIVADAS = {}


def habilidad(registro, *nombres):
    def decorar(funcion):
        for nombre in nombres:
            registro[nombre] = funcion
        return funcion
    return decorar


@habilidad(ENTRADA, "Eros")
def entrada_eros(partida, jugador, fuente, **opciones):
    encontradas = []
    if partida.numero_turno in (0, 1):
        encontradas = partida.buscar_en_mazo(
            jugador, lambda c: c.definicion.tipo == "Oro", cantidad=2
        )
    return encontradas


@habilidad(ENTRADA, "Tritón")
def entrada_triton(partida, jugador, fuente, **opciones):
    return partida.robar_carta(jugador) if jugador.zonas[Zona.MAZO] else None


@habilidad(ENTRADA, "Hemera")
def entrada_hemera(partida, jugador, fuente, **opciones):
    return list(jugador.zonas[Zona.MAZO][-3:])


@habilidad(ENTRADA, "Astreo")
def entrada_astreo(partida, jugador, fuente, *, descarte=None, **opciones):
    if descarte is None:
        return []
    partida.descartar(jugador, descarte)
    return partida.buscar_en_mazo(
        jugador,
        lambda c: c.definicion.tipo == "Aliado"
        and c.definicion.raza == "Olímpico"
        and c.definicion.fuerza is not None
        and c.definicion.fuerza <= 1,
    )


@habilidad(ENTRADA, "Atenea")
def entrada_atenea(partida, jugador, fuente, *, cartas_cementerio=None, **opciones):
    cartas = list(cartas_cementerio or [])
    if len(cartas) > 4 or any(c not in jugador.zonas[Zona.CEMENTERIO] for c in cartas):
        raise ValueError("Atenea permite elegir hasta cuatro cartas del Cementerio")
    for carta in cartas:
        partida.mover_carta(carta, Zona.MAZO)
    if cartas:
        barajar_mazo(jugador.zonas[Zona.MAZO], partida._nueva_semilla())
    return cartas


@habilidad(ENTRADA, "Comus")
def entrada_comus(partida, jugador, fuente, *, carta_cementerio=None, **opciones):
    if carta_cementerio is None:
        return None
    if carta_cementerio not in jugador.zonas[Zona.CEMENTERIO]:
        raise ValueError("La carta debe estar en tu Cementerio")
    d = carta_cementerio.definicion
    if d.tipo not in ("Aliado", "Tótem") or d.coste is None or d.coste > 3:
        raise ValueError("Comus requiere un Aliado o Tótem de coste 3 o menos")
    partida.mover_carta(carta_cementerio, Zona.MAZO)
    return carta_cementerio


@habilidad(ENTRADA, "Olímpicos")
@habilidad(SALIDA, "Olímpicos")
def mirar_superior(partida, jugador, fuente, **opciones):
    return jugador.zonas[Zona.MAZO][-1] if jugador.zonas[Zona.MAZO] else None


@habilidad(ENTRADA, "Focea")
def entrada_focea(partida, jugador, fuente, *, objetivo=None, **opciones):
    if objetivo is None:
        return None
    oponente = partida.oponente(jugador)
    zonas = (Zona.LINEA_DEFENSA, Zona.LINEA_ATAQUE, Zona.LINEA_APOYO)
    if objetivo.definicion.tipo == "Oro" or not any(objetivo in oponente.zonas[z] for z in zonas):
        raise ValueError("Focea requiere una carta oponente en juego que no sea Oro")
    partida.mover_carta(objetivo, Zona.MAZO, causa="Focea")
    return objetivo


@habilidad(ACTIVADAS, "Gaia")
def activar_gaia(partida, jugador, fuente, *, nombre_objetivo=None, **opciones):
    partida.requerir_en_juego(fuente, Zona.LINEA_DEFENSA)
    partida.usar_una_vez_por_turno(fuente, "Gaia")
    return partida.buscar_en_mazo(
        jugador,
        lambda c: c.definicion.tipo == "Aliado"
        and (nombre_objetivo is None or c.definicion.nombre == nombre_objetivo),
    )


@habilidad(ACTIVADAS, "Festín")
def activar_festin(partida, jugador, fuente, *, descartes=None, **opciones):
    partida.requerir_en_juego(fuente, Zona.RESERVA_ORO)
    cartas = list(descartes or [])
    if len(cartas) != 2 or any(c not in jugador.zonas[Zona.MANO] for c in cartas):
        raise ValueError("Festín requiere descartar dos cartas de la Mano")
    if not jugador.zonas[Zona.MAZO]:
        raise ValueError("No se puede robar de un mazo vacío")
    for carta in cartas:
        partida.descartar(jugador, carta)
    return partida.robar_carta(jugador)


@habilidad(ACTIVADAS, "Sileno")
def activar_sileno(partida, jugador, fuente, *, carta_cementerio=None, **opciones):
    partida.requerir_en_juego(fuente, Zona.LINEA_DEFENSA)
    if carta_cementerio not in jugador.zonas[Zona.CEMENTERIO]:
        raise ValueError("La carta debe estar en el Cementerio")
    partida.pagar_oros(jugador, 2)
    partida.mover_carta(carta_cementerio, Zona.MAZO)
    barajar_mazo(jugador.zonas[Zona.MAZO], partida._nueva_semilla())
    return carta_cementerio


@habilidad(ACTIVADAS, "Aceite de Oliva")
def activar_aceite(partida, jugador, fuente, **opciones):
    partida.requerir_en_juego(fuente, Zona.RESERVA_ORO)
    partida.mover_carta(fuente, Zona.DESTIERRO)
    oros = partida.buscar_en_mazo(jugador, lambda c: c.definicion.tipo == "Oro")
    if oros:
        partida.mover_carta(oros[0], Zona.RESERVA_ORO)
    return oros[0] if oros else None


@habilidad(ACTIVADAS, "Trono Dorado")
def activar_trono(partida, jugador, fuente, *, carta_cementerio=None, robar=True, **opciones):
    partida.requerir_en_juego(fuente, Zona.RESERVA_ORO)
    oponente = partida.oponente(jugador)
    if carta_cementerio not in oponente.zonas[Zona.CEMENTERIO]:
        raise ValueError("Trono Dorado requiere una carta del Cementerio oponente")
    partida.mover_carta(fuente, Zona.MAZO)
    barajar_mazo(jugador.zonas[Zona.MAZO], partida._nueva_semilla())
    partida.mover_carta(carta_cementerio, Zona.DESTIERRO)
    return partida.robar_carta(jugador) if robar and jugador.zonas[Zona.MAZO] else None


@habilidad(ACTIVADAS, "Hilo de Ariadna")
def activar_hilo(partida, jugador, fuente, *, cartas_cementerio=None, **opciones):
    partida.requerir_en_juego(fuente, Zona.RESERVA_ORO)
    cartas = list(cartas_cementerio or [])
    oponente = partida.oponente(jugador)
    if len(cartas) != 2 or any(c not in oponente.zonas[Zona.CEMENTERIO] for c in cartas):
        raise ValueError("Hilo de Ariadna requiere dos cartas del Cementerio oponente")
    partida.destruir(fuente)
    for carta in cartas:
        partida.mover_carta(carta, Zona.DESTIERRO)
    return cartas


@habilidad(ACTIVADAS, "El Gran Zeus")
def activar_zeus(partida, jugador, fuente, *, cantidad=2, **opciones):
    partida.requerir_en_juego(fuente, Zona.LINEA_DEFENSA, Zona.LINEA_ATAQUE)
    partida.usar_una_vez_por_turno(fuente, "El Gran Zeus")
    if type(cantidad) is not int or not 0 <= cantidad <= 2:
        raise ValueError("El Gran Zeus permite robar entre cero y dos cartas")
    return [partida.robar_carta(jugador) for _ in range(min(cantidad, len(jugador.zonas[Zona.MAZO])))]


@habilidad(ACTIVADAS, "Almas de Estigia")
def responder_almas(partida, jugador, fuente, *, aliado=None, pendiente=None, **opciones):
    if aliado is None or aliado not in jugador.zonas[Zona.CEMENTERIO]:
        raise ValueError("Almas de Estigia requiere tu Aliado que acaba de salir")
    if pendiente is not None and pendiente.datos.get("carta_salida") is not aliado:
        raise ValueError("La respuesta no corresponde a esa salida del juego")
    partida.mover_carta(aliado, Zona.MAZO)
    barajar_mazo(jugador.zonas[Zona.MAZO], partida._nueva_semilla())
    return aliado


@habilidad(ACTIVADAS, "Ares")
def activar_ares(partida, jugador, fuente, *, atacante=None, **opciones):
    partida.requerir_en_juego(fuente, Zona.LINEA_DEFENSA, Zona.LINEA_ATAQUE)
    if partida.ventana != "guerra_talismanes":
        raise ValueError("Ares solo puede usar esta habilidad en Guerra de Talismanes")
    partida.usar_una_vez_por_turno(fuente, "Ares")
    partida.pagar_oros(jugador, 2)
    if atacante is None:
        partida.cancelar_ataque()
        return "ataque"
    bloqueador = partida.bloqueos.pop(atacante.ID, None)
    if bloqueador is None:
        raise ValueError("Ese atacante no posee un bloqueo que cancelar")
    partida.registrar_evento("bloqueo_cancelado", jugador, fuente, atacante=atacante.ID)
    return bloqueador


@habilidad(ACTIVADAS, "Focea")
def activar_focea(partida, jugador, fuente, *, descarte=None, **opciones):
    partida.requerir_en_juego(fuente, Zona.LINEA_APOYO)
    if partida.ventana != "guerra_talismanes":
        raise ValueError("Focea solo puede usarse en Guerra de Talismanes")
    if descarte not in jugador.zonas[Zona.MANO]:
        raise ValueError("Debes elegir la carta que descartarás después de robar")
    partida.destruir(fuente, causa="coste_Focea")
    robadas = [partida.robar_carta(jugador) for _ in range(min(2, len(jugador.zonas[Zona.MAZO])))]
    partida.descartar(jugador, descarte)
    return robadas


@habilidad(ACTIVADAS, "Lyssa")
def activar_lyssa(partida, jugador, fuente, *, atacante=None, **opciones):
    partida.requerir_en_juego(fuente, Zona.LINEA_DEFENSA)
    if partida.ventana != "guerra_talismanes":
        raise ValueError("Lyssa solo puede usarse en Guerra de Talismanes")
    if atacante not in partida.oponente(jugador).zonas[Zona.LINEA_ATAQUE]:
        raise ValueError("Lyssa requiere un Aliado atacante oponente")
    partida.destruir(fuente, causa="coste_Lyssa")
    partida.bloqueos.pop(atacante.ID, None)
    partida.mover_carta(atacante, Zona.LINEA_DEFENSA, causa="Lyssa")
    if atacante in partida.atacantes:
        partida.atacantes.remove(atacante)
    return atacante


@habilidad(ACTIVADAS, "Fénix")
def activar_fenix(partida, jugador, fuente, **opciones):
    if fuente not in jugador.zonas[Zona.CEMENTERIO]:
        raise ValueError("Fénix debe estar en tu Cementerio")
    partida.pagar_oros(jugador, fuente.definicion.coste or 0)
    partida.mover_carta(fuente, Zona.LINEA_DEFENSA, causa="Fénix")
    return fuente


@habilidad(ACTIVADAS, "Thanatos")
def activar_thanatos(partida, jugador, fuente, *, nombre_objetivo=None, **opciones):
    partida.requerir_en_juego(fuente, Zona.LINEA_DEFENSA, Zona.LINEA_ATAQUE)
    partida.usar_una_vez_por_turno(fuente, "Thanatos")
    if not nombre_objetivo:
        raise ValueError("Thanatos requiere nombrar un Aliado")
    destruidos = []
    for participante in partida.jugadores:
        for zona in (Zona.LINEA_DEFENSA, Zona.LINEA_ATAQUE):
            for carta in list(participante.zonas[zona]):
                if carta.definicion.tipo == "Aliado" and carta.definicion.nombre == nombre_objetivo:
                    if partida.destruir(carta, causa="Thanatos"):
                        destruidos.append(carta)
    return destruidos


@habilidad(ACTIVADAS, "Titanes")
def activar_titanes(partida, jugador, fuente, *, objetivo=None, **opciones):
    partida.requerir_en_juego(fuente, Zona.RESERVA_ORO)
    if objetivo not in partida.oponente(jugador).zonas[Zona.LINEA_DEFENSA] + partida.oponente(jugador).zonas[Zona.LINEA_ATAQUE]:
        raise ValueError("Titanes requiere un Aliado oponente")
    if partida.fuerza_actual(objetivo) < 3:
        raise ValueError("Titanes requiere un Aliado de fuerza 3 o más")
    partida.mover_carta(fuente, Zona.DESTIERRO, causa="coste_Titanes")
    objetivo.modificadores.append(Modificador("fuerza_fija", 0, "fase_final", fuente.ID))
    return objetivo


@habilidad(ACTIVADAS, "Aceite de Oliva", "Trono Dorado", "Hilo de Ariadna", "El Gran Zeus")
def _no_op():
    # Este nombre solo evita que herramientas de documentación consideren vacío
    # el registro; las funciones concretas anteriores se vuelven a asignar abajo.
    raise AssertionError


# El decorador apilado anterior no se usa para despachar: restablece las entradas
# concretas luego de que Python crea la función auxiliar.
ACTIVADAS.update({
    "Aceite de Oliva": activar_aceite,
    "Trono Dorado": activar_trono,
    "Hilo de Ariadna": activar_hilo,
    "El Gran Zeus": activar_zeus,
})
