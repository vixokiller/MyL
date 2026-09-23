"""Punto de entrada del juego local por consola."""
import argparse
from pathlib import Path

from src.myl.consola import JuegoConsola


def crear_parser():
    parser = argparse.ArgumentParser(description="Mitos y Leyendas — partida local")
    parser.add_argument("--catalogo", type=Path,
                        default=Path("catalog/cards.provisional.json"))
    parser.add_argument("--jugador-1", default="Jugador 1")
    parser.add_argument("--jugador-2", default="Jugador 2")
    parser.add_argument("--semilla", type=int, default=None,
                        help="semilla reproducible para barajados")
    return parser


def main(argumentos=None):
    opciones = crear_parser().parse_args(argumentos)
    juego = JuegoConsola.desde_catalogo(
        opciones.catalogo,
        nombres=(opciones.jugador_1, opciones.jugador_2),
        semilla=opciones.semilla,
    )
    juego.ejecutar()


if __name__ == "__main__":
    main()
