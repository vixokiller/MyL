# Catálogo mínimo del prototipo

Este directorio contiene datos versionados; no contiene lógica del motor.

- `catalogo_cartas_helenica_olimpico.xlsx`: único archivo pensado para edición
  manual. La hoja `Guía` explica el flujo y la hoja `Cartas` contiene una fila por
  identidad del mazo.
- `cards.template.csv`: plantilla de captura y revisión de impresiones.
- `cards.provisional.json`: representación técnica provisional del Excel. Se
  conserva como entrada para el futuro cargador del catálogo.
- `formats/racial-edicion-2026-09-05.json`: instantánea inicial de legalidad.
- `reviews/implementation-stages-helenica-olimpico-v1.md`: orden recomendado de
  implementación de las cartas y pendientes no bloqueantes.

## Orden de trabajo

1. Abrir `catalogo_cartas_helenica_olimpico.xlsx`.
2. Trabajar únicamente en las celdas amarillas de la hoja `Cartas`.
3. Registrar Tipo, Coste, Fuerza, Raza, Producto, textos y URL de fuente.
4. Marcar `Verificado = Sí` solo cuando todos los datos estén contrastados. Usar
   `Parcial` cuando exista información incompleta.
5. Revisar los cambios con Codex antes de trasladarlos a los archivos técnicos.
   El responsable del proyecto realizará la programación salvo petición expresa.
6. No editar manualmente los archivos JSON de `decks/`, `formats/` o
   `prototypes/`.

## Estado actual

- 36 cartas distintas y 50 copias registradas.
- 10 cartas clasificadas para la primera versión del motor.
- 10 cartas clasificadas para la segunda etapa.
- 16 cartas postergadas hasta que el núcleo tenga más mecánicas.
- Las 36 fichas incluyen producto y URL y están marcadas como verificadas contra
  Mazos.cl, fuente secundaria. Esta verificación no convierte el catálogo en una
  base oficial.
- Las fuentes externas de reglas y legalidad del formato fueron contrastadas el
  17 de septiembre de 2026. Esa verificación normativa es independiente del
  contraste de cada impresión con la fuente secundaria.
- La primera y segunda etapa cuentan con comportamiento programado. La etapa
  posterior ya incluye Ares, Helios, Focea, Lyssa, Fénix, Thanatos y Titanes;
  las restantes continúan pendientes.

No es obligatorio que el usuario investigue las 36 fichas. Puede completar solo
los datos que ya conozca, pegar una URL o dejar una celda vacía; Codex continuará
la verificación desde ese punto.

`normalized_name` se escribe en minúsculas, sin tildes, con espacios simples y
conservando la letra `ñ`. No debe usarse como identificador único de impresión.

Mazos.cl es una fuente secundaria. No se deben descargar o redistribuir en masa
sus datos o imágenes hasta confirmar sus condiciones de uso o recibir permiso.
Cuando una carta tenga más de un producto, `Producto` los conserva en una sola
celda separados por coma.
