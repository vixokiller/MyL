"""Eventos auditables y elementos pendientes de resolución."""

from dataclasses import dataclass, field
from enum import Enum


@dataclass(frozen=True)
class Evento:
    tipo: str
    jugador: str | None = None
    carta_id: str | int | None = None
    detalles: dict = field(default_factory=dict)


class EstadoPendiente(Enum):
    PENDIENTE = "pendiente"
    RESUELTA = "resuelta"
    ANULADA = "anulada"
    PREVENIDA = "prevenida"


@dataclass
class JugadaPendiente:
    identificador: int
    tipo: str
    controlador: object
    fuente: object | None = None
    efecto: object | None = None
    objetivos: tuple = ()
    estado: EstadoPendiente = EstadoPendiente.PENDIENTE
    datos: dict = field(default_factory=dict)

    def anular(self):
        if self.estado is not EstadoPendiente.PENDIENTE:
            raise ValueError("La jugada ya no está pendiente")
        self.estado = EstadoPendiente.ANULADA

    def prevenir(self):
        if self.estado is not EstadoPendiente.PENDIENTE:
            raise ValueError("La jugada ya no está pendiente")
        self.estado = EstadoPendiente.PREVENIDA
