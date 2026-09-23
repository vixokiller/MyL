# Estado del proyecto

Fecha de corte: 23 de septiembre de 2026.

## Estado real

Existe un núcleo ejecutable y probado para recorrer la etapa 4 de la guía. El
alcance actual es un simulador mínimo: no pretende cubrir todavía todas las
ventanas, blancos, respuestas ni habilidades del reglamento completo.

| Área | Estado |
|---|---|
| Especificación de reglas | Disponible |
| Catálogo provisional | Disponible: 36 identidades, 50 copias |
| Configuración de legalidad | Disponible y contrastada externamente |
| Modelo de cartas y zonas | Implementado y separado por responsabilidades |
| Movimientos e invariantes | Implementado y probado |
| Turnos y fases | Ciclo y Fase Final ordenada implementados |
| Preparación y mazos | Operación coordinada, Oro Inicial, mano de 8 y mulligan |
| Comandos, pagos y eventos | Pago, pila pendiente, respuesta, anulación y prevención |
| Combate | Múltiples atacantes, bloqueo 1:1, Furia, excedente y derrota |
| Habilidades de cartas | Primera versión y segunda etapa implementadas por registro |
| Interfaz | Primer cliente local por consola implementado |
| Serialización | No iniciada |
| Pruebas automatizadas | 58 pruebas ejecutables |

## Diseño implementado

- `cartas.py` contiene zonas, fases, definiciones, copias físicas, modificadores,
  validación y construcción de mazos.
- `jugadores.py` conserva las zonas y decisiones de preparación de cada jugador.
- `eventos.py` define el historial inmutable y `JugadaPendiente`, con estados
  pendiente, resuelta, anulada y prevenida.
- `habilidades.py` registra funciones por nombre y momento (entrada, salida o
  activación). `Partida` ya no contiene una cadena de `if` por carta.
- `partida.py` coordina reglas y transiciones. `modelo.py` reexporta la API para
  no romper clientes existentes.

La preparación valida ambos mazos y ambos Oros Iniciales antes de mutar zonas;
luego coloca los Oros, baraja y roba ocho para los dos jugadores. Cada mulligan
devuelve toda la Mano, baraja y roba una menos; el primer turno solo comienza
cuando ambos jugadores conservaron.

La Fase Final expira modificadores de turno, aplica la excepción de robo del
primer turno, roba en los demás, descarta el exceso sobre ocho una sola vez,
cierra ventanas y formaliza el cambio de jugador. El daño al Castillo se procesa
carta por carta y declara ganador y perdedor cuando el Mazo queda vacío.

Las cartas de segunda etapa implementadas son Almas de Estigia, Astreo, Aceite de
Oliva, Atenea, Alastor, Comus, Trono Dorado, Olímpicos, Hilo de Ariadna y El Gran
Zeus. Sus decisiones opcionales se pasan como argumentos explícitos, de modo que
una futura interfaz pueda solicitarlas sin incrustar entrada/salida en el motor.

En combate pueden declararse varios atacantes, cada bloqueador solo puede
asignarse una vez, se verifica Furia, el exceso de Fuerza daña el Castillo y los
modificadores temporales/permanentes se calculan sin mutar la Fuerza impresa. La
Guerra de Talismanes comienza con el defensor, alterna prioridad y concluye con
dos cesiones consecutivas.

La etapa posterior comenzó con Ares, Helios, Focea, Lyssa, Fénix, Thanatos y
Titanes. Su alcance y las aclaraciones normativas pendientes están en
`docs/etapa_5_consola_y_cartas_posteriores.md`.

## Fuentes conservadas

- `reglas_primer_bloque.md`: especificación normativa y técnica.
- `catalog/catalogo_cartas_helenica_olimpico.xlsx`: fuente editable del catálogo.
- `catalog/cards.provisional.json`: representación provisional de los datos.
- `catalog/formats/racial-edicion-2026-09-05.json`: configuración versionada del
  formato.
- `catalog/decks/` y `catalog/prototypes/`: mazo y alcance del prototipo.

## Criterio para completar un paso de aprendizaje

Un paso se considera terminado cuando:

1. el responsable escribió el ejercicio;
2. puede explicar con sus palabras qué hace;
3. lo ejecutó y observó el resultado esperado;
4. probó al menos un dato diferente;
5. entiende el error más probable de ese ejercicio.

## Próximo hito

Completar las nueve cartas restantes de la etapa posterior, añadir menús
contextuales de objetivos a la consola, las relaciones de Armas y las capas
completas de efectos continuos/reemplazos. También falta serializar partidas
reproducibles.
