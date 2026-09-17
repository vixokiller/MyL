# Estado de implementación del primer prototipo

Fecha de corte: 17 de septiembre de 2026.

## Fuentes revisadas

- `reglas_primer_bloque.md`: especificación normativa del motor.
- `catalog/catalogo_cartas_helenica_olimpico.xlsx`: catálogo de 36 identidades y
  50 copias del mazo espejo.
- `catalog/cards.provisional.json`: representación técnica reproducible del Excel.

El catálogo declara `user_transcription`. Ninguna de sus 36 fichas está
verificada oficialmente. Producto y URL siguen ausentes en todas las filas. La
implementación no rellena esos campos ni eleva su estado de verificación.

## Primera versión

| Carta | Comportamiento incluido | Límite actual |
|---|---|---|
| Lira | Definición de Oro Inicial sin habilidad inventada | Texto y producto sin fuente verificable |
| Eros | Disparo opcional de entrada en turno 1; busca hasta 2 Oros y baraja | No implementa una cola general de disparos |
| Ofrenda a los Dioses | Continua de +1 a Aliados Olímpicos mientras está en Reserva | Solo cálculo de Fuerza del prototipo |
| Panteón | Continua condicional de +2 a Aliados propios | Sin orden de dependencias entre continuas |
| Festín | En Vigilia, descarta 2 de la Mano y roba 1 | Sin ventanas de respuesta |
| Gaia | En Vigilia, busca hasta 1 Aliado; una vez por turno; baraja | Límite ligado a la instancia actual |
| Hemera | Mira y reordena hasta las 3 cartas superiores | La interfaz debe aportar el orden elegido |
| Sileno | En Vigilia, paga 2 Oros físicos y baraja 1 carta del Cementerio | No implementa Oros virtuales ni reemplazos |
| Tritón | Robo opcional al entrar o salir del juego | El llamador informa el evento de salida |
| Templo de la Cazadora | Continua de +1 a Aliados propios mientras está en juego | Solo cálculo de Fuerza del prototipo |

Las otras 26 cartas se cargan para consulta, pero `myl.cards` las rechaza como
comportamiento no soportado. Esto evita interpretar su texto libre o resolver
silenciosamente reglas todavía pendientes.

## Correspondencia con la especificación

El modelo inicial separa `CardDefinition` (datos compartidos e inmutables) de
`CardInstance` (identidad, propietario y zona mutable), deriva `in_play` de la
zona y mantiene el controlador igual al propietario mientras el cambio de
control permanezca fuera de alcance. El estado mínimo incluye jugadores, zonas,
turno, fase, semilla determinista, pagos de Oro físico y contadores por turno.

Todavía no implementa la máquina completa de comandos/eventos descrita en la
sección 12, preparación de mazos, combate, prioridad, serialización ni una partida
de principio a fin. Esas omisiones son explícitas y no se simulan con reglas
inventadas.

