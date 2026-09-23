"""Cliente de consola para jugar una partida local de dos personas."""

from __future__ import annotations

import json
from pathlib import Path

from .cartas import Fase, Zona
from .jugadores import Jugador
from .partida import Partida


AYUDA = """Comandos:
  estado                 resumen público de la partida
  mano                   muestra tu mano numerada
  mesa                   muestra las cartas en juego
  oro N                  pone la carta N de tu mano como Oro de turno
  jugar N                juega la carta N de tu mano (habilidades opcionales se omiten)
  habilidad Z:N          usa una habilidad sin objetivos; Z es defensa, apoyo u oro
  batalla N[,N...]       inicia Batalla y declara atacantes por índice de Defensa
  bloquear B:A           asigna bloqueador B al atacante A
  resolver               resuelve todos los combates declarados
  pasar                  avanza a la fase siguiente o termina el turno
  ayuda                   muestra esta ayuda
  salir                   abandona la sesión
"""


class JuegoConsola:
    def __init__(self, partida, entrada=input, salida=print):
        self.partida = partida
        self.entrada = entrada
        self.salida = salida
        self.en_ejecucion = True

    @classmethod
    def desde_catalogo(cls, ruta_catalogo, nombres=("Jugador 1", "Jugador 2"),
                       semilla=None, entrada=input, salida=print):
        datos = json.loads(Path(ruta_catalogo).read_text(encoding="utf-8"))
        jugadores = [Jugador(nombre) for nombre in nombres]
        partida = Partida(*jugadores, semilla=semilla)
        partida.preparar_partida([datos["cards"], datos["cards"]])
        return cls(partida, entrada, salida)

    def preparar_mulligans(self):
        for jugador in self.partida.jugadores:
            while not jugador.mano_conservada:
                self._mostrar_mano(jugador)
                respuesta = self.entrada(
                    f"{jugador.nombre}: ¿conservar Mano de {len(jugador.zonas[Zona.MANO])} cartas? [s/n] "
                ).strip().lower()
                if respuesta in ("s", "si", "sí", "y", "yes"):
                    self.partida.mulligan(jugador, conservar=True)
                elif respuesta in ("n", "no"):
                    self.partida.mulligan(jugador)
                else:
                    self.salida("Responde 's' para conservar o 'n' para mulligan.")
        self.partida.iniciar_primer_turno()

    def ejecutar(self):
        if not self.partida.numero_turno:
            self.preparar_mulligans()
        self.salida(AYUDA)
        while self.en_ejecucion and not self.partida.terminada:
            if self.partida.fase is Fase.AGRUPACION:
                self.partida.avanzar_fase()
            activo = self.partida.jugador_activo
            linea = self.entrada(
                f"T{self.partida.numero_turno} · {activo.nombre} · {self.partida.fase.value}> "
            )
            try:
                self.ejecutar_comando(linea)
            except (ValueError, IndexError) as error:
                self.salida(f"No se pudo ejecutar: {error}")
        if self.partida.terminada:
            self.salida(f"Ganador: {self.partida.ganador.nombre} (Castillo oponente vacío)")

    def ejecutar_comando(self, linea):
        partes = linea.strip().split(maxsplit=1)
        if not partes:
            return
        comando = partes[0].lower()
        argumento = partes[1] if len(partes) == 2 else ""
        jugador = self.partida.jugador_activo
        if comando == "ayuda": self.salida(AYUDA)
        elif comando == "estado": self._mostrar_estado()
        elif comando == "mano": self._mostrar_mano(jugador)
        elif comando == "mesa": self._mostrar_mesa()
        elif comando == "oro":
            self.partida.poner_oro_en_reserva(jugador, self._por_indice(jugador.zonas[Zona.MANO], argumento))
        elif comando == "jugar":
            self.partida.jugar_carta(jugador, self._por_indice(jugador.zonas[Zona.MANO], argumento))
        elif comando == "habilidad": self._usar_habilidad(jugador, argumento)
        elif comando == "batalla": self._iniciar_batalla(jugador, argumento)
        elif comando == "bloquear": self._bloquear(argumento)
        elif comando == "resolver": self._resolver_batalla()
        elif comando == "pasar": self._pasar()
        elif comando == "salir": self.en_ejecucion = False
        else: raise ValueError("comando desconocido; escribe 'ayuda'")

    def _por_indice(self, cartas, texto):
        try: indice = int(texto) - 1
        except ValueError as error: raise ValueError("se requiere un índice numérico") from error
        if indice < 0 or indice >= len(cartas): raise IndexError("índice de carta fuera de rango")
        return cartas[indice]

    def _linea(self, cartas):
        return ", ".join(f"{i}: {c.definicion.nombre}" for i, c in enumerate(cartas, 1)) or "—"

    def _mostrar_mano(self, jugador): self.salida(f"Mano de {jugador.nombre}: {self._linea(jugador.zonas[Zona.MANO])}")

    def _mostrar_estado(self):
        self.salida(f"Turno {self.partida.numero_turno} · {self.partida.fase.value} · activo: {self.partida.jugador_activo.nombre}")
        for j in self.partida.jugadores:
            self.salida(f"{j.nombre}: Castillo {len(j.zonas[Zona.MAZO])}, Mano {len(j.zonas[Zona.MANO])}, Cementerio {len(j.zonas[Zona.CEMENTERIO])}")

    def _mostrar_mesa(self):
        for j in self.partida.jugadores:
            self.salida(f"{j.nombre} · Oros: {self._linea(j.zonas[Zona.RESERVA_ORO])}")
            self.salida(f"{j.nombre} · Defensa: {self._linea(j.zonas[Zona.LINEA_DEFENSA])}")
            self.salida(f"{j.nombre} · Ataque: {self._linea(j.zonas[Zona.LINEA_ATAQUE])}")
            self.salida(f"{j.nombre} · Apoyo: {self._linea(j.zonas[Zona.LINEA_APOYO])}")

    def _usar_habilidad(self, jugador, argumento):
        zonas = {"defensa": Zona.LINEA_DEFENSA, "apoyo": Zona.LINEA_APOYO, "oro": Zona.RESERVA_ORO}
        try: nombre_zona, indice = argumento.lower().split(":", 1); zona = zonas[nombre_zona]
        except (ValueError, KeyError) as error: raise ValueError("usa habilidad defensa:N, apoyo:N u oro:N") from error
        resultado = self.partida.usar_habilidad(jugador, self._por_indice(jugador.zonas[zona], indice))
        self.salida(f"Habilidad resuelta: {resultado}")

    def _iniciar_batalla(self, jugador, argumento):
        if self.partida.fase is Fase.VIGILIA: self.partida.avanzar_fase(iniciar_batalla=True)
        if self.partida.fase is not Fase.BATALLA: raise ValueError("no se puede iniciar Batalla ahora")
        indices = [int(x.strip()) for x in argumento.split(",") if x.strip()]
        defensa = list(jugador.zonas[Zona.LINEA_DEFENSA])
        atacantes = [self._por_indice(defensa, str(i)) for i in indices]
        self.partida.declarar_atacantes(jugador, atacantes)
        self.salida("Ataque declarado. El oponente puede usar 'bloquear B:A'.")

    def _bloquear(self, argumento):
        if self.partida.fase is not Fase.BATALLA: raise ValueError("no hay una Batalla activa")
        try: texto_b, texto_a = argumento.split(":", 1)
        except ValueError as error: raise ValueError("usa bloquear B:A") from error
        defensor = self.partida._jugador_inactivo()
        bloqueador = self._por_indice(defensor.zonas[Zona.LINEA_DEFENSA], texto_b)
        atacante = self._por_indice(self.partida.jugador_activo.zonas[Zona.LINEA_ATAQUE], texto_a)
        self.partida.declarar_bloqueo(defensor, bloqueador, atacante)

    def _resolver_batalla(self):
        if self.partida.fase is not Fase.BATALLA: raise ValueError("no hay una Batalla activa")
        self.partida.resolver_combates(); self.partida.avanzar_fase()

    def _pasar(self):
        if self.partida.fase is Fase.BATALLA and self.partida.jugador_activo.zonas[Zona.LINEA_ATAQUE]:
            raise ValueError("resuelve los combates antes de pasar")
        self.partida.avanzar_fase()
