# Catálogo mínimo del prototipo

Este directorio contiene datos versionados; no contiene lógica del motor.

- `catalogo_cartas_helenica_olimpico.xlsx`: único archivo pensado para edición
  manual. La hoja `Guía` explica el flujo y la hoja `Cartas` contiene una fila por
  identidad del mazo.
- `cards.template.csv`: plantilla de captura y revisión de impresiones.
- `cards.provisional.json`: catálogo técnico generado desde el Excel. Puede ser
  consumido por el primer prototipo, aunque sus fichas sigan pendientes de una
  fuente oficial o identificable.
- `formats/racial-edicion-2026-09-05.json`: instantánea inicial de legalidad.
- `reviews/implementation-stages-helenica-olimpico-v1.md`: orden recomendado de
  implementación de las cartas y pendientes no bloqueantes.

## Orden de trabajo

1. Abrir `catalogo_cartas_helenica_olimpico.xlsx`.
2. Trabajar únicamente en las celdas amarillas de la hoja `Cartas`.
3. Registrar Tipo, Coste, Fuerza, Raza, Producto, textos y URL de fuente.
4. Marcar `Verificado = Sí` solo cuando todos los datos estén contrastados. Usar
   `Parcial` cuando exista información incompleta.
5. Entregar el archivo actualizado a Codex. Codex revisará la legalidad,
   trasladará la información a los archivos técnicos y clasificará la etapa del
   motor.
6. No editar manualmente los archivos JSON de `decks/`, `formats/` o
   `prototypes/`.

## Estado actual

- 36 cartas distintas y 50 copias registradas.
- 10 cartas clasificadas para la primera versión del motor.
- 10 cartas clasificadas para la segunda etapa.
- 16 cartas postergadas hasta que el núcleo tenga más mecánicas.
- Todas las fichas están en estado `Parcial` porque faltan producto y URL. Esto
  no bloquea las pruebas del prototipo; sí bloquea declararlas verificadas.

No es obligatorio que el usuario investigue las 36 fichas. Puede completar solo
los datos que ya conozca, pegar una URL o dejar una celda vacía; Codex continuará
la verificación desde ese punto.

`normalized_name` se escribe en minúsculas, sin tildes, con espacios simples y
conservando la letra `ñ`. No debe usarse como identificador único de impresión.

Mazos.cl es una fuente secundaria. No se deben descargar o redistribuir en masa
sus datos o imágenes hasta confirmar sus condiciones de uso o recibir permiso.
