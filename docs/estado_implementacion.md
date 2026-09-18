# Estado del proyecto

Fecha de corte: 17 de septiembre de 2026.

## Estado real

No existe código de implementación. El repositorio contiene únicamente reglas,
datos provisionales, decisiones de diseño y una guía de trabajo.

| Área | Estado |
|---|---|
| Especificación de reglas | Disponible |
| Catálogo provisional | Disponible: 36 identidades, 50 copias |
| Configuración de legalidad | Disponible y contrastada externamente |
| Modelo de cartas y zonas | No iniciado |
| Movimientos e invariantes | No iniciado |
| Turnos y fases | No iniciado |
| Preparación y mazos | No iniciado |
| Comandos, pagos y eventos | No iniciado |
| Combate | No iniciado |
| Habilidades de cartas | No iniciado |
| Serialización e interfaz | No iniciado |
| Pruebas automatizadas | No iniciado |

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

No crear todavía una estructura de paquete. El próximo paso será crear un único
archivo `main.py`, mostrar un mensaje y aprender a ejecutarlo desde la raíz del
proyecto. Después se representará una carta primero con variables, luego con un
diccionario y finalmente con una clase sencilla.

Las carpetas `src/` y `tests/`, `Enum`, `dataclass`, inmutabilidad y pruebas con
`pytest` aparecerán más adelante, después de comprender el problema que resuelve
cada herramienta. La secuencia completa está en `docs/guia_de_desarrollo.md`.
