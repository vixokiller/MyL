"""Motor y coordinación de una partida."""
import random

from .cartas import Fase, Modificador, Zona, ZONAS_EN_JUEGO, barajar_mazo, construir_mazo
from .eventos import EstadoPendiente, Evento, JugadaPendiente
from . import habilidades


class Partida:
    def __init__(self, jugador_1, jugador_2, semilla=None):
        if jugador_1.nombre == jugador_2.nombre:
            raise ValueError("Los jugadores deben tener nombres diferentes")
        self.jugadores = [jugador_1, jugador_2]
        self.eventos = []
        self.jugador_activo = self.primer_jugador = None
        self.numero_turno = 0
        self.fase = None
        self.oro_de_turno_disponible = False
        self.bloqueos, self.atacantes, self.usos_habilidad = {}, [], set()
        self.preparada = self.terminada = False
        self.ganador = self.perdedor = None
        self.pila = []
        self.ventana = self.prioridad = None
        self.cesiones_consecutivas = 0
        self.ataque_cancelado = False
        self.prevencion_castillo = {j.nombre: 0 for j in self.jugadores}
        self._azar, self._secuencia = random.Random(semilla), 0

    def _nueva_semilla(self): return self._azar.randrange(2**63)

    def registrar_evento(self, tipo, jugador=None, carta=None, **detalles):
        evento = Evento(tipo, getattr(jugador, "nombre", None), getattr(carta, "ID", None), detalles)
        self.eventos.append(evento)
        return evento

    def _validar_jugador(self, jugador):
        if jugador not in self.jugadores: raise ValueError("El jugador no pertenece a esta partida")

    def oponente(self, jugador):
        self._validar_jugador(jugador)
        return self.jugadores[1] if jugador is self.jugadores[0] else self.jugadores[0]

    def _jugador_inactivo(self): return self.oponente(self.jugador_activo)
    def _buscar_ubicaciones(self, carta):
        return [(j, z) for j in self.jugadores for z, cs in j.zonas.items() if carta in cs]
    def propietario_de(self, carta):
        return next(j for j in self.jugadores if j.nombre == carta.propietario)

    def mover_carta(self, carta, destino, *, causa="regla"):
        if not isinstance(destino, Zona): raise ValueError("La zona de destino no es válida")
        ubicaciones = self._buscar_ubicaciones(carta)
        if not ubicaciones: raise ValueError("La carta no pertenece a esta partida")
        if len(ubicaciones) > 1: raise ValueError("La carta aparece en más de una zona")
        contenedor, origen = ubicaciones[0]
        if carta.zona_actual is not origen: raise ValueError("La zona de la carta no coincide con su ubicación")
        if origen is destino: return carta
        dueño = self.propietario_de(carta)
        receptor = contenedor if destino in ZONAS_EN_JUEGO else dueño
        contenedor.zonas[origen].remove(carta); receptor.zonas[destino].append(carta); carta.cambiar_de_zona(destino)
        salio, entro = origen in ZONAS_EN_JUEGO and destino not in ZONAS_EN_JUEGO, origen not in ZONAS_EN_JUEGO and destino in ZONAS_EN_JUEGO
        if salio:
            carta.controlador = carta.propietario
            carta.modificadores[:] = [m for m in carta.modificadores if m.duracion == "permanente"]
        if entro: carta.turno_entrada_en_juego = self.numero_turno
        self.registrar_evento("carta_movida", receptor, carta, origen=origen.value, destino=destino.value, causa=causa)
        if salio:
            self._resolver_registrada(habilidades.SALIDA, dueño, carta)
            self.crear_pendiente("salida", dueño, carta, datos={"carta_salida": carta})
            if carta.definicion.nombre == "Tritón" and dueño.zonas[Zona.MAZO]: self.robar_carta(dueño)
        return carta

    def destruir(self, carta, *, causa="destruccion"):
        if carta.indestructible and carta.zona_actual in ZONAS_EN_JUEGO:
            self.registrar_evento("destruccion_prevenida", self.propietario_de(carta), carta); return False
        self.mover_carta(carta, Zona.CEMENTERIO, causa=causa); return True

    def descartar(self, jugador, carta):
        if carta not in jugador.zonas[Zona.MANO]: raise ValueError("Solo se puede descartar una carta de la Mano")
        self.mover_carta(carta, Zona.CEMENTERIO, causa="descarte")
        self.registrar_evento("carta_descartada", jugador, carta); return carta

    def robar_carta(self, jugador):
        self._validar_jugador(jugador)
        if not jugador.zonas[Zona.MAZO]: raise ValueError("No se puede robar de un mazo vacío")
        carta = jugador.zonas[Zona.MAZO][-1]; self.mover_carta(carta, Zona.MANO, causa="robo")
        self.registrar_evento("carta_robada", jugador, carta); return carta

    def formar_mano_inicial(self, jugador, cantidad=8):
        self._validar_jugador(jugador)
        if jugador.zonas[Zona.MANO]: raise ValueError("La Mano debe estar vacía antes de formar la mano inicial")
        if len(jugador.zonas[Zona.MAZO]) < cantidad: raise ValueError("No hay suficientes cartas para formar la mano inicial")
        cartas = [self.robar_carta(jugador) for _ in range(cantidad)]
        self.registrar_evento("mano_inicial_formada", jugador, cantidad=cantidad); return cartas

    def seleccionar_oro_inicial(self, jugador, carta):
        self._validar_jugador(jugador)
        if jugador.zonas[Zona.RESERVA_ORO]: raise ValueError("El jugador ya tiene un Oro Inicial")
        if carta not in jugador.zonas[Zona.MAZO]: raise ValueError("El Oro Inicial debe estar en el Mazo")
        if not carta.definicion.es_oro_inicial: raise ValueError("La carta no es elegible como Oro Inicial")
        self.mover_carta(carta, Zona.RESERVA_ORO, causa="oro_inicial")
        self.registrar_evento("oro_inicial_colocado", jugador, carta); return carta

    def preparar_partida(self, mazos=None, oros_iniciales=None, *, primer_jugador=None):
        if self.preparada or self.numero_turno: raise ValueError("La partida ya fue preparada o iniciada")
        if mazos is not None:
            if len(mazos) != 2 or any(j.zonas[Zona.MAZO] for j in self.jugadores): raise ValueError("Se requieren dos mazos y zonas vacías")
            construidos = [construir_mazo(d, j.nombre) for j, d in zip(self.jugadores, mazos)]
        else:
            construidos = [list(j.zonas[Zona.MAZO]) for j in self.jugadores]
            if any(len(m) != 50 for m in construidos): raise ValueError("Cada jugador debe comenzar con 50 cartas")
        elegidos = []
        for i, mazo in enumerate(construidos):
            pedido = None if oros_iniciales is None else oros_iniciales[i]
            candidatos = [c for c in mazo if c.definicion.es_oro_inicial]
            carta = next((c for c in candidatos if pedido in (c, c.ID, c.definicion.nombre)), None) if pedido is not None else (candidatos[0] if candidatos else None)
            if carta is None: raise ValueError(f"{self.jugadores[i].nombre} no tiene un Oro Inicial válido")
            elegidos.append(carta)
        if mazos is not None:
            for j, mazo in zip(self.jugadores, construidos): j.zonas[Zona.MAZO].extend(mazo)
        for j, oro in zip(self.jugadores, elegidos):
            self.seleccionar_oro_inicial(j, oro); barajar_mazo(j.zonas[Zona.MAZO], self._nueva_semilla()); self.formar_mano_inicial(j)
            j.mano_conservada = False; self.registrar_evento("mazo_barajado", j, cantidad=49)
        self.primer_jugador = primer_jugador or self.jugadores[0]; self._validar_jugador(self.primer_jugador)
        self.preparada = True; self.registrar_evento("partida_preparada", self.primer_jugador); return self

    preparar = preparar_partida

    def mulligan(self, jugador, *, conservar=False):
        self._validar_jugador(jugador)
        if not self.preparada or self.numero_turno: raise ValueError("El mulligan solo ocurre antes del primer turno")
        if jugador.mano_conservada: raise ValueError("El jugador ya conservó su Mano")
        if conservar:
            jugador.mano_conservada = True; self.registrar_evento("mulligan_conservado", jugador, cantidad=len(jugador.zonas[Zona.MANO])); return list(jugador.zonas[Zona.MANO])
        cantidad = len(jugador.zonas[Zona.MANO])
        if cantidad <= 1: raise ValueError("Una Mano de una carta no puede reducirse")
        for c in list(jugador.zonas[Zona.MANO]): self.mover_carta(c, Zona.MAZO, causa="mulligan")
        barajar_mazo(jugador.zonas[Zona.MAZO], self._nueva_semilla()); nueva = self.formar_mano_inicial(jugador, cantidad - 1)
        self.registrar_evento("mulligan_realizado", jugador, cantidad=len(nueva)); return nueva

    def iniciar_primer_turno(self, jugador=None):
        if self.numero_turno: raise ValueError("La partida ya tiene un turno iniciado")
        jugador = jugador or self.primer_jugador or self.jugadores[0]; self._validar_jugador(jugador)
        if self.preparada and not all(j.mano_conservada for j in self.jugadores): raise ValueError("Ambos jugadores deben conservar su Mano")
        self.primer_jugador = self.jugador_activo = jugador; self.numero_turno = 1; self.fase = Fase.VIGILIA; self.oro_de_turno_disponible = True
        self.registrar_evento("turno_iniciado", jugador, numero=1, fase=self.fase.value)

    def avanzar_fase(self, iniciar_batalla=False, descartes=None):
        if self.fase is None: raise ValueError("No hay un turno iniciado")
        if self.fase is Fase.AGRUPACION: self.agrupar(self.jugador_activo); self.fase = Fase.VIGILIA
        elif self.fase is Fase.VIGILIA: self.fase = Fase.BATALLA if iniciar_batalla else Fase.FINAL
        elif self.fase is Fase.BATALLA: self.fase = Fase.FINAL
        else: self.finalizar_turno(descartes=descartes); return self.fase
        self.registrar_evento("fase_iniciada", self.jugador_activo, numero_turno=self.numero_turno, fase=self.fase.value); return self.fase

    def finalizar_turno(self, *, descartes=None):
        if self.fase is not Fase.FINAL: raise ValueError("Solo se puede finalizar durante la Fase Final")
        activo = self.jugador_activo; self.registrar_evento("paso_final_disparos", activo)
        for j in self.jugadores:
            for cartas in j.zonas.values():
                for c in cartas: c.modificadores[:] = [m for m in c.modificadores if m.duracion not in ("turno", "fase_final")]
        self.registrar_evento("modificadores_temporales_expirados", activo)
        if self.numero_turno != 1 and activo.zonas[Zona.MAZO]: self.robar_carta(activo)
        exceso = max(0, len(activo.zonas[Zona.MANO]) - 8)
        elegidos = list(descartes) if descartes is not None else list(activo.zonas[Zona.MANO][:exceso])
        if len(elegidos) != exceso or any(c not in activo.zonas[Zona.MANO] for c in elegidos): raise ValueError(f"Deben descartarse exactamente {exceso} cartas")
        for c in elegidos: self.descartar(activo, c)
        self.registrar_evento("limite_mano_aplicado", activo, descartadas=exceso); self.cerrar_ventana()
        self.jugador_activo = self.oponente(activo); self.numero_turno += 1; self.fase = Fase.AGRUPACION; self.oro_de_turno_disponible = True
        self.bloqueos.clear(); self.atacantes.clear(); self.usos_habilidad.clear(); self.ataque_cancelado = False
        self.registrar_evento("turno_finalizado", activo, numero=self.numero_turno - 1)
        self.registrar_evento("fase_iniciada", self.jugador_activo, numero_turno=self.numero_turno, fase=self.fase.value)

    def agrupar(self, jugador):
        self._validar_jugador(jugador)
        for c in list(jugador.zonas[Zona.ORO_PAGADO]): self.mover_carta(c, Zona.RESERVA_ORO, causa="agrupacion")
        for c in list(jugador.zonas[Zona.LINEA_ATAQUE]): self.mover_carta(c, Zona.LINEA_DEFENSA, causa="agrupacion")
        self.registrar_evento("jugador_agrupado", jugador)

    def poner_oro_en_reserva(self, jugador, carta):
        if jugador is not self.jugador_activo or self.fase is not Fase.VIGILIA: raise ValueError("Solo el jugador activo puede poner Oro durante Vigilia")
        if not self.oro_de_turno_disponible: raise ValueError("El Oro de turno ya fue utilizado")
        if carta not in jugador.zonas[Zona.MANO] or carta.definicion.tipo != "Oro": raise ValueError("La carta debe ser un Oro en la Mano")
        self.mover_carta(carta, Zona.RESERVA_ORO); self.oro_de_turno_disponible = False; return carta

    def pagar_oros(self, jugador, cantidad):
        if type(cantidad) is not int or cantidad < 0: raise ValueError("La cantidad de Oros debe ser un entero no negativo")
        if len(jugador.zonas[Zona.RESERVA_ORO]) < cantidad: raise ValueError("No hay suficientes Oros disponibles")
        oros = list(jugador.zonas[Zona.RESERVA_ORO][:cantidad])
        for o in oros: self.mover_carta(o, Zona.ORO_PAGADO, causa="pago")
        self.registrar_evento("coste_pagado", jugador, cantidad=cantidad, oros=[o.ID for o in oros]); return oros

    def crear_pendiente(self, tipo, jugador, fuente=None, efecto=None, objetivos=(), datos=None):
        self._secuencia += 1; p = JugadaPendiente(self._secuencia, tipo, jugador, fuente, efecto, tuple(objetivos), datos=dict(datos or {})); self.pila.append(p)
        self.registrar_evento("jugada_pendiente", jugador, fuente,
                              pendiente=p.identificador, clase=tipo); return p

    def resolver_pendiente(self, pendiente=None):
        p = pendiente or (self.pila[-1] if self.pila else None)
        if p is None or p not in self.pila: raise ValueError("No existe esa jugada pendiente")
        if p is not self.pila[-1]: raise ValueError("Las jugadas pendientes se resuelven en orden inverso")
        self.pila.pop(); resultado = None
        if p.estado is EstadoPendiente.PENDIENTE: resultado = p.efecto() if callable(p.efecto) else None; p.estado = EstadoPendiente.RESUELTA
        elif p.tipo == "carta" and p.fuente in p.controlador.zonas[Zona.MANO]:
            self.mover_carta(p.fuente, Zona.CEMENTERIO, causa=p.estado.value)
        self.registrar_evento("jugada_resuelta", p.controlador, p.fuente, pendiente=p.identificador, estado=p.estado.value); return resultado

    def anular_pendiente(self, p): p.anular(); self.registrar_evento("jugada_anulada", p.controlador, p.fuente, pendiente=p.identificador)
    def prevenir_pendiente(self, p): p.prevenir(); self.registrar_evento("jugada_prevenida", p.controlador, p.fuente, pendiente=p.identificador)

    def jugar_carta(self, jugador, carta, *, resolver=True, **opciones):
        en_guerra = self.ventana == "guerra_talismanes" and carta.definicion.tipo == "Talismán"
        if (jugador is not self.jugador_activo or self.fase is not Fase.VIGILIA) and not en_guerra: raise ValueError("El jugador no puede jugar esa carta ahora")
        if en_guerra and jugador is not self.prioridad: raise ValueError("El jugador no tiene prioridad")
        if carta not in jugador.zonas[Zona.MANO] or carta.definicion.tipo == "Oro": raise ValueError("La carta debe estar en la Mano y no ser Oro")
        destinos = {"Aliado": Zona.LINEA_DEFENSA, "Tótem": Zona.LINEA_APOYO, "Talismán": Zona.CEMENTERIO}
        if carta.definicion.tipo not in destinos: raise ValueError("El tipo de carta todavía no es jugable")
        if carta.definicion.nombre == "El Gran Zeus" and any(
            c.definicion.nombre == carta.definicion.nombre
            for zona in (Zona.LINEA_DEFENSA, Zona.LINEA_ATAQUE)
            for c in jugador.zonas[zona]
        ): raise ValueError("Solo puede haber una copia de una carta Única en juego")
        coste = carta.definicion.coste
        if coste is None or len(jugador.zonas[Zona.RESERVA_ORO]) < coste: raise ValueError("No hay suficientes Oros disponibles")
        self.registrar_evento("intento_jugar_carta", jugador, carta, coste=coste); self.pagar_oros(jugador, coste)
        def efecto():
            self.mover_carta(carta, destinos[carta.definicion.tipo], causa="resolucion"); self.registrar_evento("carta_jugada", jugador, carta)
            if carta.definicion.tipo in ("Aliado", "Tótem"):
                self.registrar_evento("carta_entrada_en_juego", jugador, carta); self._resolver_registrada(habilidades.ENTRADA, jugador, carta, **opciones)
            return carta
        p = self.crear_pendiente("carta", jugador, carta, efecto)
        if en_guerra: self.accion_en_ventana(jugador)
        if resolver: self.resolver_pendiente(p); return carta
        return p

    def buscar_en_mazo(self, jugador, condicion, cantidad=1):
        encontradas = []
        for c in list(jugador.zonas[Zona.MAZO]):
            if condicion(c):
                self.mover_carta(c, Zona.MANO, causa="busqueda"); encontradas.append(c)
                if len(encontradas) == cantidad: break
        if jugador.zonas[Zona.MAZO]: barajar_mazo(jugador.zonas[Zona.MAZO], self._nueva_semilla())
        return encontradas

    _buscar_desde_mazo = buscar_en_mazo
    def _resolver_registrada(self, registro, jugador, carta, **opciones):
        funcion = registro.get(carta.definicion.nombre)
        if funcion is None: return None
        resultado = funcion(self, jugador, carta, **opciones); self.registrar_evento("habilidad_resuelta", jugador, carta, habilidad=carta.definicion.nombre); return resultado
    def _resolver_habilidad_entrada(self, jugador, carta, **opciones): return self._resolver_registrada(habilidades.ENTRADA, jugador, carta, **opciones)

    def ordenar_tres_superiores(self, jugador, orden_ids):
        mazo = jugador.zonas[Zona.MAZO]
        if len(mazo) < 3 or not isinstance(orden_ids, list) or len(orden_ids) != 3: raise ValueError("Se requieren exactamente tres identificadores")
        por_id = {c.ID: c for c in mazo[-3:]}
        if set(orden_ids) != set(por_id): raise ValueError("Solo se pueden ordenar las tres cartas superiores")
        mazo[-3:] = [por_id[i] for i in orden_ids]

    def requerir_en_juego(self, fuente, *zonas):
        if fuente.zona_actual not in zonas or not self._buscar_ubicaciones(fuente): raise ValueError("La fuente debe estar en una zona válida de juego")
    def usar_una_vez_por_turno(self, fuente, nombre):
        clave = (self.numero_turno, fuente.ID, nombre)
        if clave in self.usos_habilidad: raise ValueError(f"{nombre} solo puede usarse una vez por turno")
        self.usos_habilidad.add(clave)
    def usar_habilidad(self, jugador, fuente, *, resolver=True, **opciones):
        funcion = habilidades.ACTIVADAS.get(fuente.definicion.nombre)
        if funcion is None: raise ValueError("La carta no posee una habilidad activada implementada")
        if self.ventana != "guerra_talismanes" and (jugador is not self.jugador_activo or self.fase is not Fase.VIGILIA): raise ValueError("La habilidad solo puede usarse en tu Vigilia")
        if self.ventana == "guerra_talismanes" and jugador is not self.prioridad: raise ValueError("El jugador no tiene prioridad")
        p = self.crear_pendiente("habilidad", jugador, fuente, lambda: funcion(self, jugador, fuente, **opciones), datos=opciones)
        self.registrar_evento("habilidad_activada", jugador, fuente, habilidad=fuente.definicion.nombre)
        return self.resolver_pendiente(p) if resolver else p

    def responder_habilidad(self, jugador, fuente, pendiente, *, resolver=False, **opciones):
        """Crea una respuesta ligada a un elemento que aún está pendiente."""
        if pendiente not in self.pila or pendiente.estado is not EstadoPendiente.PENDIENTE:
            raise ValueError("La ventana del elemento al que se responde ya terminó")
        funcion = habilidades.ACTIVADAS.get(fuente.definicion.nombre)
        if funcion is None: raise ValueError("La fuente no posee una respuesta implementada")
        opciones = {**opciones, "pendiente": pendiente}
        respuesta = self.crear_pendiente("respuesta", jugador, fuente,
            lambda: funcion(self, jugador, fuente, **opciones),
            objetivos=(pendiente,), datos=opciones)
        return self.resolver_pendiente(respuesta) if resolver else respuesta

    def jugar_respuesta(self, jugador, carta, pendiente, *, resolver=False, **opciones):
        """Juega un Talismán cuya condición es responder a otro elemento."""
        if pendiente not in self.pila or pendiente.estado is not EstadoPendiente.PENDIENTE:
            raise ValueError("La ventana de respuesta ya terminó")
        if carta not in jugador.zonas[Zona.MANO] or carta.definicion.tipo != "Talismán":
            raise ValueError("La respuesta debe ser un Talismán en la Mano")
        coste = carta.definicion.coste
        if coste is None or len(jugador.zonas[Zona.RESERVA_ORO]) < coste:
            raise ValueError("No hay suficientes Oros disponibles")
        funcion = habilidades.ACTIVADAS.get(carta.definicion.nombre)
        if funcion is None: raise ValueError("El Talismán no posee una respuesta implementada")
        self.pagar_oros(jugador, coste)
        opciones = {**opciones, "pendiente": pendiente}
        def efecto():
            resultado = funcion(self, jugador, carta, **opciones)
            if carta in jugador.zonas[Zona.MANO]:
                self.mover_carta(carta, Zona.CEMENTERIO, causa="talisman_resuelto")
            return resultado
        respuesta = self.crear_pendiente("respuesta", jugador, carta, efecto,
                                         objetivos=(pendiente,), datos=opciones)
        return self.resolver_pendiente(respuesta) if resolver else respuesta

    def declarar_atacante(self, jugador, carta):
        if jugador is not self.jugador_activo or self.fase is not Fase.BATALLA: raise ValueError("Solo el jugador activo puede atacar durante Batalla")
        if carta not in jugador.zonas[Zona.LINEA_DEFENSA] or carta.definicion.tipo != "Aliado": raise ValueError("El atacante debe ser un Aliado en Línea de Defensa")
        if carta.turno_entrada_en_juego == self.numero_turno and not carta.tiene_furia: raise ValueError("El Aliado no puede atacar el turno en que entró sin Furia")
        self.mover_carta(carta, Zona.LINEA_ATAQUE, causa="ataque"); self.atacantes.append(carta); self.registrar_evento("atacante_declarado", jugador, carta); return carta
    def declarar_atacantes(self, jugador, cartas):
        if len({id(c) for c in cartas}) != len(cartas): raise ValueError("Un Aliado no puede declararse dos veces")
        return [self.declarar_atacante(jugador, c) for c in cartas]
    def declarar_bloqueo(self, jugador, bloqueador, atacante):
        if jugador is self.jugador_activo or self.fase is not Fase.BATALLA: raise ValueError("Solo el defensor puede bloquear durante Batalla")
        if bloqueador not in jugador.zonas[Zona.LINEA_DEFENSA]: raise ValueError("El bloqueador debe estar en Línea de Defensa")
        if atacante not in self.jugador_activo.zonas[Zona.LINEA_ATAQUE]: raise ValueError("La carta indicada no es un atacante")
        if atacante.ID in self.bloqueos or bloqueador in self.bloqueos.values(): raise ValueError("Atacante o bloqueador ya asignado")
        self.bloqueos[atacante.ID] = bloqueador; self.registrar_evento("bloqueo_declarado", jugador, bloqueador, atacante=atacante.ID)

    def iniciar_guerra_talismanes(self):
        if self.fase is not Fase.BATALLA: raise ValueError("La Guerra de Talismanes pertenece a Batalla")
        self.ventana = "guerra_talismanes"; self.prioridad = self._jugador_inactivo(); self.cesiones_consecutivas = 0
    def ceder_prioridad(self, jugador):
        if self.ventana != "guerra_talismanes" or jugador is not self.prioridad: raise ValueError("El jugador no tiene prioridad")
        self.cesiones_consecutivas += 1
        if self.cesiones_consecutivas == 2:
            while self.pila: self.resolver_pendiente()
            self.cerrar_ventana(); return False
        self.prioridad = self.oponente(jugador); return True
    def accion_en_ventana(self, jugador):
        if self.ventana != "guerra_talismanes" or jugador is not self.prioridad: raise ValueError("El jugador no tiene prioridad")
        self.cesiones_consecutivas = 0; self.prioridad = self.oponente(jugador)
    def cerrar_ventana(self): self.ventana = self.prioridad = None; self.cesiones_consecutivas = 0
    def cancelar_ataque(self):
        self.ataque_cancelado = True
        for c in list(self.jugador_activo.zonas[Zona.LINEA_ATAQUE]): self.mover_carta(c, Zona.LINEA_DEFENSA, causa="ataque_cancelado")
        self.bloqueos.clear(); self.atacantes.clear(); self.registrar_evento("ataque_cancelado", self.jugador_activo)
    def prevenir_daño_castillo(self, jugador, cantidad):
        if type(cantidad) is not int or cantidad < 0: raise ValueError("La prevención debe ser no negativa")
        self.prevencion_castillo[jugador.nombre] += cantidad

    def fuerza_actual(self, carta):
        if carta.definicion.fuerza is None: raise ValueError("La carta no posee Fuerza")
        fuerza = carta.definicion.fuerza + sum(m.valor for m in carta.modificadores if m.atributo == "fuerza")
        ubicaciones = self._buscar_ubicaciones(carta)
        if len(ubicaciones) != 1: return max(0, fuerza)
        jugador, _ = ubicaciones[0]; aliados = jugador.zonas[Zona.LINEA_DEFENSA] + jugador.zonas[Zona.LINEA_ATAQUE]
        if carta.definicion.tipo == "Aliado":
            if carta.definicion.raza == "Olímpico" and any(o.definicion.nombre == "Ofrenda a los Dioses" for o in jugador.zonas[Zona.RESERVA_ORO]): fuerza += 1
            if any(a.definicion.nombre == "Templo de la Cazadora" for a in jugador.zonas[Zona.LINEA_APOYO]): fuerza += 1
            if any(a.definicion.nombre == "Panteón" for a in jugador.zonas[Zona.LINEA_APOYO]) and any(a.definicion.raza == "Olímpico" for a in aliados): fuerza += 2
            if carta.definicion.raza == "Olímpico" and any(
                a.definicion.nombre == "Helios"
                for a in jugador.zonas[Zona.LINEA_DEFENSA] + jugador.zonas[Zona.LINEA_ATAQUE]
            ): fuerza += 2
        fijos = [m.valor for m in carta.modificadores if m.atributo == "fuerza_fija"]
        if fijos: fuerza = fijos[-1]
        return max(0, fuerza)

    def _dañar_castillo(self, defensor, cantidad, atacante):
        prevenido = min(cantidad, self.prevencion_castillo[defensor.nombre]); cantidad -= prevenido; self.prevencion_castillo[defensor.nombre] -= prevenido
        botadas = []
        for _ in range(min(cantidad, len(defensor.zonas[Zona.MAZO]))):
            c = defensor.zonas[Zona.MAZO][-1]; self.mover_carta(c, Zona.CEMENTERIO, causa="daño_castillo"); botadas.append(c)
        self.registrar_evento("daño_al_castillo", self.jugador_activo, atacante, cantidad=len(botadas), prevenido=prevenido)
        if not defensor.zonas[Zona.MAZO]:
            self.terminada = True; self.perdedor = defensor; self.ganador = self.oponente(defensor)
            self.registrar_evento("partida_terminada", self.ganador, razon="castillo_vacio", perdedor=defensor.nombre)
        return botadas

    def resolver_combate(self, atacante):
        if self.fase is not Fase.BATALLA or atacante not in self.jugador_activo.zonas[Zona.LINEA_ATAQUE]: raise ValueError("La carta indicada no es un atacante")
        bloqueador = self.bloqueos.pop(atacante.ID, None)
        if bloqueador is None or bloqueador not in self._jugador_inactivo().zonas[Zona.LINEA_DEFENSA]: return self._dañar_castillo(self._jugador_inactivo(), self.fuerza_actual(atacante), atacante)
        fa, fb = self.fuerza_actual(atacante), self.fuerza_actual(bloqueador)
        if fb >= fa:
            destruido = self.destruir(atacante, causa="combate")
            if destruido and atacante.definicion.nombre == "Alastor": bloqueador.modificadores.append(Modificador("fuerza", -1, "permanente", atacante.ID))
        if fa >= fb:
            destruido = self.destruir(bloqueador, causa="combate")
            if destruido and bloqueador.definicion.nombre == "Alastor": atacante.modificadores.append(Modificador("fuerza", -1, "permanente", bloqueador.ID))
        botadas = self._dañar_castillo(self._jugador_inactivo(), fa - fb, atacante) if fa > fb else []
        self.registrar_evento("combate_resuelto", self.jugador_activo, atacante, bloqueador=bloqueador.ID, fuerza_atacante=fa, fuerza_bloqueador=fb, daño_castillo=len(botadas)); return atacante, bloqueador
    def resolver_combates(self, orden=None):
        resultados = []
        for atacante in list(orden or self.jugador_activo.zonas[Zona.LINEA_ATAQUE]):
            if self.terminada: break
            resultados.append(self.resolver_combate(atacante))
        return resultados
