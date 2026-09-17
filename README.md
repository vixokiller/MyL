# Simulador MyL — Primer Bloque

Primer prototipo del motor descrito en `reglas_primer_bloque.md`. El alcance
actual carga el catálogo provisional Helénica/Olímpico y ejecuta escenarios
aislados para las diez cartas marcadas como **Primera versión**.

El detalle de cobertura y límites está en `docs/estado_implementacion.md`.

Los datos de las cartas no se presentan como oficiales. Provienen de una
transcripción del usuario y conservan `verification_status: partial`, además de
`null` en producto y URL mientras no puedan contrastarse.

## Ejecutar las pruebas

```bash
python -m pytest
```

## Regenerar el catálogo provisional

```bash
python tools/generate_cards_provisional.py \
  catalog/catalogo_cartas_helenica_olimpico.xlsx \
  catalog/cards.provisional.json
```

El generador usa solo la biblioteca estándar de Python. No convierte los datos
en verificados ni completa campos ausentes.

## Límites intencionales

- No existe todavía una partida completa ni una interfaz.
- Las habilidades opcionales reciben las elecciones de forma explícita.
- Buscar siempre baraja el Castillo, incluso si no encuentra una carta.
- No se interpreta texto libre: las diez cartas se vinculan a comportamiento
  compilado mediante su `card_id`.
- Las cartas fuera de la primera versión se cargan como datos, pero no tienen
  comportamiento ejecutable.
