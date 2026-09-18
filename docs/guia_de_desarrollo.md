# Guía de desarrollo para comenzar desde cero

Esta guía está pensada para una persona que cursa su primer año de programación
y conoce lo básico de Python: variables, condiciones, ciclos, funciones, clases,
métodos e importaciones.

No tienes que comprender desde el comienzo palabras como «inmutable», «evento»,
«arquitectura» o «serialización». Las introduciremos cuando exista un problema
concreto que ayuden a resolver.

## Cómo trabajaremos

Tú escribirás el código. Codex te dará una tarea pequeña cada vez y podrá:

- explicar un concepto con ejemplos sencillos;
- ayudarte a pensar antes de programar;
- revisar lo que escribiste sin modificarlo;
- ayudarte a interpretar un error;
- proponerte pruebas manuales;
- escribir código solo cuando tú lo pidas expresamente.

No avances si el paso actual funciona pero no puedes explicar con tus propias
palabras qué hace cada parte.

## Antes de comenzar: las carpetas

Ahora mismo no necesitas carpetas de código. Las crearemos cuando sean útiles:

| Momento | Elemento | Para qué sirve |
|---|---|---|
| Paso 1 | `main.py` | Experimentar en un único archivo fácil de ejecutar |
| Paso 8 | carpeta `src/` | Separar el código del resto de documentos y datos |
| Paso 8 | carpeta `src/myl/` | Guardar únicamente el código del simulador |
| Paso 9 | varios archivos `.py` | Separar clases cuando un solo archivo resulte incómodo |
| Paso 12 | carpeta `tests/` | Guardar pruebas automáticas separadas del programa |

No crees toda la estructura de una vez. Una carpeta debe aparecer porque ya
tenemos algo concreto que guardar en ella.

---

## Etapa 1 — Aprender modelando una sola carta

### Paso 1 — Crear el primer archivo

Cuando estés listo, crea `main.py` en la raíz del proyecto.

Objetivo: comprobar que puedes ejecutar Python desde este proyecto.

Escribe solo una línea que muestre un mensaje. Ejecútala y confirma que ves el
mensaje. Después explica qué es el archivo, qué instrucción ejecutó Python y
desde qué carpeta ejecutaste el programa.

No crees todavía `src/`, `tests/` ni ninguna clase.

### Paso 2 — Representar una carta con variables

En `main.py`, usa variables para representar el nombre, tipo, coste y fuerza de
una carta. Muestra esos valores. Usa Eros como ejemplo consultando el catálogo.

Conceptos practicados: variables, cadenas, números y `print`.

Pregunta: ¿qué inconveniente aparecería si quisiéramos representar veinte cartas
usando variables separadas?

### Paso 3 — Agrupar los datos en un diccionario

Reemplaza las variables separadas por un diccionario. Accede a sus valores por
clave y modifica temporalmente la Fuerza para observar qué ocurre.

Conceptos practicados: diccionarios, claves y valores. Todavía no estamos creando
el diseño definitivo; estamos descubriendo qué datos necesita una carta.

### Paso 4 — Crear una clase sencilla `Carta`

Crea una clase normal con `__init__`. Guarda nombre, tipo, coste y fuerza usando
`self`. Crea dos objetos distintos y muestra sus datos.

Preguntas:

- ¿Cuál es la diferencia entre la clase y cada objeto creado?
- Si cambias la Fuerza de un objeto, ¿cambia también la del otro?
- ¿Qué representa `self`?

No uses todavía `dataclass`, herencia, propiedades ni tipos avanzados.

### Paso 5 — Diferenciar definición y copia física

Dos copias de Eros comparten información, pero son dos cartas distintas durante
una partida.

Crea una clase `DefinicionCarta` con nombre, tipo, coste y fuerza. Luego crea una
clase `CartaEnPartida` que guarde un identificador único, una referencia a su
definición, el propietario y la zona actual.

Crea una sola definición de Eros y dos cartas en partida que utilicen esa misma
definición, pero tengan identificadores diferentes.

### Paso 6 — Qué significa «inmutable»

Una cosa es inmutable cuando no debería cambiar después de ser creada.

El coste impreso de Eros pertenece a su definición. Mover una copia desde el Mazo
a la Mano no debería cambiar ese coste. En cambio, la zona de la copia sí cambia.

Por ahora no necesitas impedir técnicamente los cambios. Solo separa:

- datos que conceptualmente no cambian: nombre, tipo, coste y Fuerza impresos;
- datos que sí cambian: zona, controlador o participación en combate.

Más adelante aprenderás `dataclass(frozen=True)`, que permite pedirle a Python que
proteja los datos que decidimos tratar como inmutables.

### Paso 7 — Mover una carta

Agrega a `CartaEnPartida` un método sencillo para cambiar su zona. Mueve una carta
del Mazo a la Mano y muestra la zona antes y después.

Luego agrega una condición que rechace una zona desconocida. Por ahora puedes
guardar las zonas válidas en una lista de cadenas.

Conceptos practicados: métodos, `if`, listas y cambio de atributos.

---

## Etapa 2 — Organizar el proyecto cuando ya sea necesario

### Paso 8 — Crear `src/` y `src/myl/`

Solo realiza este paso cuando entiendas los anteriores.

- `src` significa *source* o código fuente. Separa el programa de documentos y
  datos.
- `myl` identifica nuestro programa dentro de `src`.

Crea ambas carpetas y mueve el código útil desde `main.py` a un único archivo
`src/myl/modelo.py`. Mantén `main.py` pequeño: solo importa las clases y crea
ejemplos.

Aquí practicarás `import`. Si falla, no copies configuraciones sin entenderlas;
revisaremos juntos cómo busca módulos Python.

### Paso 9 — Separar archivos solo cuando moleste tener uno

Cuando `modelo.py` sea difícil de leer, sepáralo gradualmente:

```text
src/myl/
├── cartas.py
├── jugadores.py
└── partida.py
```

La razón para separar archivos es comprender y encontrar el código con facilidad,
no cumplir una estructura decorativa.

### Paso 10 — Reemplazar cadenas por `Enum`

Escribir `"mano"`, `"Mano"` o `"mano "` produce tres textos diferentes. Aprende
`Enum` con un ejemplo pequeño y luego úsalo para representar las zonas válidas.

### Paso 11 — Representar un jugador

Crea una clase `Jugador` con nombre y un diccionario de zonas. Comienza solamente
con Mazo, Mano y Cementerio.

Agrega las demás zonas después de que puedas añadir una carta al Mazo, encontrarla,
quitarla, agregarla a la Mano y comprobar que no quedó repetida.

---

## Etapa 3 — Aprender a comprobar el programa

### Paso 12 — Pruebas manuales con `assert`

Ahora crea `tests/`, porque ya existen comportamientos que comprobar varias veces.
Antes de instalar una biblioteca, usa `assert` para verificar:

- que una carta nueva está en la zona indicada;
- que moverla cambia la zona;
- que su propietario no cambia;
- que dos copias tienen identificadores diferentes.

Un `assert` expresa: «esto debe ser verdadero; si no, hay un problema».

### Paso 13 — Primera clase `Partida`

Crea una partida con exactamente dos jugadores. No implementes turnos todavía.
Haz que rechace jugadores con el mismo nombre.

Luego agrega un método de movimiento que actualice las listas del jugador. La
partida debe comprobar que la carta existe y no aparece en dos zonas.

### Paso 14 — Introducir `pytest`

Solo ahora crea la configuración del proyecto e instala `pytest`. Antes de copiar
configuración, pide una explicación de cada sección y comando.

Convierte los `assert` manuales en pruebas automáticas. Aprende primero a ejecutar
una prueba, después un archivo y finalmente toda la suite.

### Paso 15 — Introducir `dataclass`

Cuando las clases tengan mucho código repetitivo en `__init__`, compara una clase
normal con otra que use `@dataclass`.

Después podrás usar `@dataclass(frozen=True)` en `DefinicionCarta`. `frozen=True`
hace que Python impida cambiar sus atributos después de crearla. En ese momento
«inmutable» tendrá un ejemplo concreto dentro de tu propio programa.

---

## Etapa 4 — Construir el núcleo poco a poco

Después de dominar las etapas anteriores, avanza así:

1. cargar una carta desde un diccionario;
2. leer un JSON pequeño creado por ti;
3. cargar el catálogo provisional;
4. validar campos y cantidades;
5. construir un mazo de 50 cartas;
6. barajar con `random`;
7. robar una carta;
8. formar una mano de ocho cartas;
9. implementar el Oro Inicial;
10. introducir fases y turnos;
11. pagar Oros;
12. jugar una carta sencilla;
13. registrar eventos;
14. programar combate básico;
15. recién entonces programar habilidades.

Cada número volverá a dividirse en tareas pequeñas cuando lleguemos a él.

## Regla para saber si puedes avanzar

Antes del siguiente paso, intenta responder:

1. ¿Qué problema resuelve el código?
2. ¿Qué representa cada clase y objeto?
3. ¿Qué datos cambian y cuáles no deberían cambiar?
4. ¿Qué pasaría si elimino cada método?
5. ¿Cómo comprobé que funciona?
6. ¿Qué error espero con datos inválidos?

Si una respuesta no está clara, no significa que hayas fallado. Significa que el
paso actual necesita otro ejemplo o una explicación diferente.

## Cómo pedirme el siguiente paso

- «Quiero comenzar el paso 1. Explícamelo sin escribir código.»
- «Ya escribí el paso 3. Revísalo, pero no modifiques mis archivos.»
- «No entiendo la diferencia entre clase y objeto; dame otro ejemplo.»
- «Este error apareció al importar. Ayúdame paso a paso.»
- «Ya entendí el ejercicio; ahora sí escribe un ejemplo mínimo para compararlo.»
