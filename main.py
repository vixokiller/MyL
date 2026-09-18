from src.myl.modelo import(DefinicionCarta, 
                           CartaEnPartida, 
                           Zona,
                           Jugador
                        )


eros = DefinicionCarta('Eros', 'Aliado', 2, 2)
jugador_1 = Jugador("Jugador_1")
jugador_2 = Jugador("Jugador_2")
eros_1 = CartaEnPartida(1, eros, jugador_1.nombre, Zona.MAZO)
eros_2 = CartaEnPartida(2, eros, jugador_2.nombre, Zona.LINEA_DEFENSA)

jugador_1.zonas[Zona.MAZO].append(eros_1)

print("Mazo:", len(jugador_1.zonas[Zona.MAZO]))
print("Mano:", len(jugador_1.zonas[Zona.MANO]))
print("Cementerio:", len(jugador_1.zonas[Zona.CEMENTERIO]))
carta_del_mazo = jugador_1.zonas[Zona.MAZO][0]

print(carta_del_mazo.definicion.nombre)

print("Mazo jugador 1:", len(jugador_1.zonas[Zona.MAZO]))
print("Mazo jugador 2:", len(jugador_2.zonas[Zona.MAZO]))