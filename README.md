# Simulador MyL — Primer Bloque

Repositorio de especificación y planificación para construir un simulador de
Mitos y Leyendas Primer Bloque.

## Estado actual

El proyecto contiene un motor Python modular y una suite automatizada. Cubre la
preparación de dos jugadores, mulligan tradicional, turnos y Fase Final,
recursos, jugadas pendientes, ventanas de respuesta, combate y las dos primeras
etapas del mazo Helénica/Olímpico.

`src/myl/modelo.py` continúa siendo la fachada pública compatible. La
implementación se divide en `cartas.py`, `jugadores.py`, `eventos.py`,
`habilidades.py` y `partida.py`.

## Documentos principales

1. `reglas_primer_bloque.md`: especificación funcional y normativa del motor.
2. `docs/guia_de_desarrollo.md`: itinerario para comenzar a programar.
3. `docs/estado_implementacion.md`: estado real y checklist de hitos.
4. `catalog/README.md`: significado y mantenimiento de los datos del catálogo.
5. `catalog/reviews/implementation-stages-helenica-olimpico-v1.md`: orden sugerido
   para incorporar las cartas.

## Datos conservados

Se conserva el catálogo provisional Helénica/Olímpico, el mazo espejo, la
instantánea de legalidad y las revisiones que justifican su clasificación. Estos
archivos son material de referencia; no implican que exista comportamiento
programado.
informacion
Las fuentes externas de reglas y legalidad fueron contrastadas el 17 de
septiembre de 2026. El 18 de septiembre de 2026 se incorporaron producto y URL
para las 36 fichas y se contrastaron con Mazos.cl como fuente secundaria; el
catálogo sigue siendo provisional y no una base oficial.

## Ejecutar las pruebas

Desde la raíz del repositorio:

```bash
pytest -q
```

## Jugar por consola

```bash
python main.py --jugador-1 Alicia --jugador-2 Bruno
```

Escribe `ayuda` dentro de la partida para ver los comandos. El cliente actual es
un primer modo local y todavía omite menús para habilidades con elecciones
complejas; el alcance y los siguientes incrementos se describen en
`docs/etapa_5_consola_y_cartas_posteriores.md`.

La explicación del diseño y sus extensiones siguientes está en
`docs/estado_implementacion.md` y `docs/guia_de_desarrollo.md`.
