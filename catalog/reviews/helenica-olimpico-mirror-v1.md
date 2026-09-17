# Revisión del mazo Helénica–Olímpico espejo v1

Fecha de revisión: 2026-09-17

## Resultado de la primera pasada

- Total: 50 cartas, incluyendo el Oro Inicial.
- Oro Inicial declarado: Lira.
- Identidades diferentes: 36, contando Lira.
- Cartas prohibidas detectadas por nombre: ninguna.
- Límites comprobados: Aceite de Oliva 1/1; Afrodita 2/2; Helios 2/2;
  Panteón 2/2.
- El usuario confirmó que el mazo contiene más de 16 Aliados; queda registrar el
  tipo y la raza de cada impresión para que el validador pueda demostrarlo.
- Validación de todas las impresiones y textos: pendiente de catálogo.

`Candidata` significa que la grafía debe confirmarse contra la ficha de la carta;
no implica que se haya modificado el nombre aportado por el usuario.

| Cantidad | Nombre recibido | Nombre oficial candidato | Legalidad preliminar | Estado de catálogo | Motor inicial |
|---:|---|---|---|---|---|
| 1 | Lira | Lira | confirmada como Oro Inicial | pendiente | candidata básica |
| 2 | Almas de estigia | Almas de Estigia | máximo general | pendiente | pendiente |
| 1 | Astreo | Astreo | máximo general | pendiente | pendiente |
| 3 | Eros | Eros | máximo general | pendiente | pendiente |
| 3 | Ofrenda a los Dioses | Ofrenda a los Dioses | máximo general | coincidencia visible | candidata: continua simple |
| 1 | Aceite de Oliva | Aceite de Oliva | limitada a 1; cumple | pendiente | pendiente |
| 2 | Ares | Ares | máximo general | pendiente | pendiente |
| 3 | Atenea | Atenea | máximo general | pendiente | pendiente |
| 2 | Panteon | Panteón | limitada a 2; cumple | pendiente | pendiente |
| 1 | Alastor | Alastor | máximo general | pendiente | pendiente |
| 1 | Comus | Comus | máximo general | pendiente | pendiente |
| 1 | Festin | Festín | máximo general | pendiente | pendiente |
| 1 | Figuras Negras | Figuras Negras | máximo general | coincidencia visible | posterior: destierro y pérdida de habilidad |
| 1 | Gaia | Gaia | máximo general | confirmada como carta distinta de `Gea` | pendiente |
| 2 | Helios | Helios | limitada a 2; cumple | pendiente | pendiente |
| 1 | El Oscuro Hades | El Oscuro Hades | máximo general | pendiente | pendiente |
| 2 | Zagreus | Zagreus | máximo general | pendiente | pendiente |
| 2 | Arcas del Imperio | Arcas del Imperio | máximo general | pendiente | pendiente |
| 1 | Trono dorado | Trono Dorado | máximo general | pendiente | pendiente |
| 1 | Ave de Hera | Ave de Hera | máximo general | pendiente | pendiente |
| 1 | Hemera | Hemera | máximo general | pendiente | pendiente |
| 2 | Olimpicos | Olímpicos | máximo general | pendiente | pendiente |
| 1 | Sileno | Sileno | máximo general | pendiente | pendiente |
| 2 | Afrodita | Afrodita | limitada a 2; cumple | pendiente | pendiente |
| 1 | Triton | Tritón | máximo general | pendiente | pendiente |
| 1 | Hilo de Ariadna | Hilo de Ariadna | máximo general | pendiente | pendiente |
| 1 | Dionisio zagreo | Dionisio Zagreo | máximo general | pendiente | pendiente |
| 1 | Focea | Focea | máximo general | coincidencia visible | posterior: retorno, robo, descarte y Guerra de Talismanes |
| 1 | Templo de la Cazadora | Templo de la Cazadora | máximo general | pendiente | pendiente |
| 1 | Lyssa | Lyssa | máximo general | pendiente | pendiente |
| 1 | Fenix | Fénix | máximo general | pendiente | pendiente |
| 1 | Hera | Hera | máximo general | pendiente | pendiente |
| 1 | Thanatos | Thanatos | máximo general | pendiente | pendiente |
| 1 | Aguila Imperial | Águila Imperial | máximo general | pendiente | pendiente |
| 1 | Titanes | Titanes | máximo general | pendiente | pendiente |
| 1 | El Gran Zeus | El Gran Zeus | Única; una copia, cumple | coincidencia visible | segunda etapa: reglas ya definidas, falta compilar y probar |

## Aclaraciones resueltas

1. Lira es elegible como Oro Inicial.
2. `Gaia` y `Gea` son cartas diferentes.
3. El mazo contiene más de 16 Aliados.
4. «Hasta 2» permite elegir cero, uno o dos.
5. Indestructible impide destrucción por reglas, efectos, habilidades y Asignación
   de Daño, pero no impide otras formas de salida del juego.
6. Única limita la construcción a una copia; no limita cuántas veces esa misma
   copia puede volver a jugarse durante la partida.

## Dudas activas restantes

El usuario no necesita resolverlas todavía:

1. registrar el tipo y la raza de cada impresión para validar automáticamente el
   mínimo de Aliados;
2. implementar cambios de zona y ventanas de Guerra de Talismanes antes de Focea;
3. implementar destierro y pérdida temporal de habilidades antes de Figuras Negras.

## Próxima pasada

Consultar cada ficha en Mazos.cl, registrar impresión, producto, tipo, coste,
Fuerza, raza y texto. Una carta solo pasará a `verified` cuando todos esos campos
tengan fuente y su comportamiento tenga pruebas.

## Segunda pasada: datos transcritos por el usuario

El archivo `catalogo_cartas_helenica_olimpico.xlsx` fue completado manualmente y
revisado el 17 de septiembre de 2026.

### Composición comprobada

- 28 cartas de Aliado, todas declaradas de raza Olímpico;
- 16 Oros contando Lira;
- 4 Tótems;
- 2 Talismanes;
- 0 Armas;
- 50 cartas en total.

El requisito de al menos 16 Aliados queda demostrado por los datos del catálogo.

### Tratamiento de campos vacíos

- En Oros, `cost`, `strength` y `race` son `null` porque no aplican.
- En Tótems y Talismanes, `strength` y `race` son `null` porque no aplican.
- Lira no posee texto, por lo que `printed_text` y `effective_text` son `null`
  válidos y no datos faltantes.
- `product` y `source_url` continúan pendientes debido a la indisponibilidad de la
  fuente. Esto no impide modelar las reglas de las cartas, pero sí impide marcar
  la impresión como completamente verificada.

Los textos y características aportados se consideran `user_transcription` y no
fuente oficial. Las filas deben mantenerse como `Parcial` hasta contrastarlas.

### Hallazgos de revisión

- Thanatos contiene la frase `Carta única`; su legalidad debe cambiar de máximo
  general a una copia. La lista actual cumple porque contiene una sola copia.
- `Sólo puedes tener un Titanes en juego` es una restricción del estado de juego,
  no una restricción de una copia durante la construcción.
- Deben contrastarse posibles errores de transcripción en Comus (`Cuenado`),
  Zagreus (`barajas`) y Titanes (`fuerzza`). No deben corregirse silenciosamente
  en el texto impreso.

### Próximo hito

Crear definiciones provisionales con procedencia `user_transcription`, clasificar
la complejidad de cada habilidad y seleccionar el primer conjunto de cartas para
pruebas unitarias. Producto y URL pueden completarse posteriormente sin bloquear
este hito.
