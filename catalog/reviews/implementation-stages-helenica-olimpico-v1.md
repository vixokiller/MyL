# Etapas de implementación — Helénica / Olímpico

## Resultado

Las 36 cartas del mazo espejo se consideran utilizables como datos provisionales.
Producto y URL se contrastaron con Mazos.cl el 18 de septiembre de 2026 y las
fichas quedaron verificadas contra esa fuente secundaria.

## Primera versión — 10 cartas

Objetivo: probar el ciclo mínimo de partida con oro, aliados, robo, búsqueda,
descarte, modificación de fuerza y un tótem sencillo.

- Lira
- Eros
- Ofrenda a los Dioses
- Panteón
- Festín
- Gaia
- Hemera
- Sileno
- Tritón
- Templo de la Cazadora

Estas cartas deben implementarse primero como pruebas unitarias y escenarios
aislados. No forman por sí solas un reemplazo legal del mazo completo.

## Segunda etapa — 10 cartas

Objetivo: ampliar el motor con respuestas, búsqueda condicionada, prevención o
redirección, límites de uso, indestructibilidad y restricciones de construcción.

- Almas de Estigia
- Astreo
- Aceite de Oliva
- Atenea
- Alastor
- Comus
- Trono Dorado
- Olímpicos
- Hilo de Ariadna
- El Gran Zeus

Estado: implementada mediante el registro de `src/myl/habilidades.py`. Incluye
respuestas, búsquedas condicionadas, movimientos entre zonas, límites por turno,
modificadores permanentes e indestructibilidad. Las decisiones opcionales y los
objetivos se reciben explícitamente desde quien invoque el motor.

## Posterior — 16 cartas

Objetivo: dejar para después las interacciones que requieren ventanas de tiempo,
zonas o blancos complejos, efectos continuos globales, habilidades desde la
Reserva de Oro o cambios temporales difíciles de resolver en el núcleo inicial.

- Ares
- Figuras Negras
- Helios
- El Oscuro Hades
- Zagreus
- Arcas del Imperio
- Ave de Hera
- Afrodita
- Dionisio Zagreo
- Focea
- Lyssa
- Fénix
- Hera
- Thanatos
- Águila Imperial
- Titanes

Estado: en curso. Ares, Helios, Focea, Lyssa, Fénix, Thanatos y Titanes están
implementadas y probadas. Las nueve identidades restantes requieren los
incrementos de control, Oros virtuales, pérdida de habilidades, cambios de tipo,
juego gratuito o prevención reactiva descritos en
`docs/etapa_5_consola_y_cartas_posteriores.md`.

## Pendientes no bloqueantes

- Sustituir o complementar Mazos.cl con fuentes oficiales cuando estén
  disponibles.

## Siguiente paso técnico

Extender el mismo registro con la etapa posterior. Antes de cada grupo deben
añadirse pruebas de la ventana o relación nueva que utiliza (Armas, control,
efectos globales o reemplazos de movimiento).
