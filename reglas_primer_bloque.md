# ESPECIFICACIÓN DEL MOTOR — MITOS Y LEYENDAS PRIMER BLOQUE

## 0. Alcance y definiciones

### 0.1 Alcance de la especificación

#### Definición

Esta especificación describe las reglas vigentes del formato Mitos y Leyendas
Primer Bloque al 17 de septiembre de 2026.

#### Fuentes normativas

El simulador utilizará, en orden de aplicación según su vigencia, las reglas
oficiales, los documentos actualizados de reglas, las FAQ, los Oráculos, las
erratas y las demás aclaraciones oficiales aplicables a Primer Bloque.

Cuando dos fuentes oficiales sean incompatibles, deberá documentarse cuál es la
más reciente o específica antes de implementar una resolución.

Fuentes principales utilizadas en esta revisión:

- Documento Actualizado de Reglas, revisión de julio de 2024;
- FAQ oficial de Primer Bloque, versión 1.1 de mayo de 2026;
- Oráculos, erratas y listas de legalidad oficiales vigentes.

#### Configuración inicial

El conjunto inicial de cartas implementadas se basará en el entorno vigente
durante la temporada de Leyendas Primer Bloque 4.0.

La legalidad y el límite de copias de las cartas deberán tratarse como datos
versionados del formato, porque pueden cambiar sin que cambien las reglas básicas
del motor.

#### Mantenimiento

Debido a que las reglas, aclaraciones y cartas legales pueden modificarse con el
tiempo, la especificación será revisada periódicamente.

A partir de enero de 2027 se realizará una revisión cada tres meses.
Hasta cada revisión, el simulador continuará utilizando la última versión
documentada de las reglas.

#### Implicancias para el motor

El motor debe poder identificar la versión de reglas y la configuración de
legalidad utilizadas por cada partida.

#### Dudas pendientes

- Determinar qué formatos adicionales se incorporarán después de Racial Edición.

### 0.2 Jugador

#### Definición

Un jugador es uno de los participantes de la partida.

#### Propiedades relevantes

- Participa utilizando un Mazo Castillo legal para el formato seleccionado.
- Posee cartas y zonas propias.
- Puede controlar cartas dentro de sus zonas del Campo de Batalla.
- Realiza acciones y toma decisiones cuando las reglas se lo permiten.

#### Relaciones

El jugador se relaciona con:

- su Mazo Castillo;
- su Mano;
- sus zonas del Campo de Batalla;
- su Cementerio y Zona de Destierro;
- las cartas de las que es propietario;
- las cartas que controla;
- el jugador oponente;
- el turno, las fases, las acciones y los efectos del juego.

#### Implicancias para el motor

El motor debe poder identificar de forma inequívoca a cada jugador y asociar a este:

- sus cartas;
- sus zonas;
- sus recursos;
- su estado actual;
- las acciones y decisiones que tiene permitido realizar.

#### Dudas pendientes

- Determinar todos los componentes del estado de un jugador.
- Documentar las reglas de derrota, rendición y desconexión cuando se diseñe el
  flujo completo de partida.

### 0.3 Carta

#### Definición

Una carta es uno de los elementos fundamentales del juego y representa un objeto,
personaje, recurso o efecto que puede participar en una partida.

Las cartas forman parte inicialmente de los mazos utilizados por los jugadores y
pueden desplazarse entre distintas zonas de juego durante la partida.

#### Propiedades relevantes

Una carta posee características base, asociaciones de partida y características
variables.

Las características base corresponden a la información propia de la carta o a
los datos de referencia asociados a ella. Algunas aparecen impresas en la carta
y otras, como su legalidad, dependen del formato documentado.
Una carta puede poseer, dependiendo de su tipo:

- nombre;
- coste de oro;
- símbolo de la carta;
- fuerza, cuando corresponda;
- caja de texto;
- raza;
- frecuencia;
- texto épico;
- código de coleccionista;
- ilustración;
- legalidad;
- edición.

Las asociaciones y características del estado de partida pueden incluir:

- propietario;
- controlador;
- zona actual;
- orientación;
- modificadores;
- relaciones con otras cartas;
- participación en acciones o procesos del juego.

No todas estas propiedades necesariamente existen en todos los tipos de carta.

#### Relaciones

Una carta siempre pertenece a un jugador como propietario.

Durante la partida puede existir una diferencia entre el propietario de una carta
y el jugador que actualmente la controla.

Una carta siempre debe encontrarse en alguna zona válida del juego.


#### Implicancias para el motor

El motor debe poder:

- identificar individualmente cada carta;
- distinguir sus características base de su estado durante la partida;
- conocer su propietario;
- conocer su controlador actual;
- conocer su zona actual;
- consultar sus características y habilidades;
- modificar su estado cuando una regla o efecto lo requiera;
- moverla entre zonas.

#### Dudas pendientes

Determinar cuáles de las características de una carta son universales y cuáles
dependen exclusivamente de su tipo.

### 0.4 Estado de una carta

#### Definición

El estado de una carta es el conjunto de condiciones, asociaciones y
características que describen su situación actual durante una partida. Algunos
componentes pueden cambiar y otros, como el propietario, permanecen constantes.

El estado de una carta puede cambiar como consecuencia de acciones realizadas
por los jugadores, cambios de zona, reglas del juego, habilidades, efectos,
procesos de combate o cambios de controlador.

El estado actual de una carta debe poder consultarse para determinar qué reglas,
acciones y efectos pueden aplicarse sobre ella.

#### Componentes posibles del estado

El estado de una carta puede incluir, entre otros:

- zona actual;
- propietario;
- controlador;
- posición u orientación;
- participación en un ataque o combate;
- modificaciones temporales o permanentes;
- habilidades o efectos que actualmente la afectan;
- relaciones con otras cartas;
- restricciones aplicadas sobre ella.

Esta lista es provisional y será ampliada o modificada a medida que se documenten
las reglas del juego.

#### Estado almacenado y estado derivado

Algunas características del estado deberán almacenarse directamente, mientras
que otras podrán calcularse a partir de información ya conocida por el motor.

Por ejemplo, si una carta se encuentra en una zona perteneciente al Campo de
Batalla, el motor podrá determinar que es una carta en juego sin almacenar esa
condición de manera independiente.

La especificación debe identificar progresivamente qué componentes se almacenan
y cuáles se derivan, con el fin de evitar estados contradictorios.

#### Propiedades relevantes

- El estado de una carta puede cambiar varias veces durante una partida.
- Los cambios de estado pueden ser consecuencia de reglas, acciones o efectos.
- Algunos componentes del estado pueden ser temporales.
- Algunos componentes pueden permanecer mientras la carta continúe en una zona
  determinada.
- El estado puede determinar qué acciones puede realizar una carta y qué efectos
  pueden aplicarse sobre ella.
- Un cambio de zona puede eliminar o reiniciar componentes del estado anterior.

#### Relaciones

El estado de una carta está relacionado con:

- su zona actual;
- su propietario;
- su controlador;
- los efectos que actualmente la afectan;
- otras cartas con las que mantenga una relación;
- la fase o etapa actual del juego;
- las acciones en las que participe o haya participado.

La zona actual puede determinar automáticamente parte del estado de una carta.

#### Implicancias para el motor

El motor debe:

- mantener actualizado el estado de cada carta;
- permitir consultar su estado actual;
- modificarlo cuando una regla, acción o efecto lo requiera;
- determinar qué acciones son válidas según dicho estado;
- eliminar o reiniciar componentes cuando la carta cambie de zona, cuando
  corresponda;
- gestionar estados temporales y determinar cuándo expiran;
- impedir estados incompatibles o imposibles.

#### Dudas pendientes

- Determinar todos los componentes posibles del estado de una carta.
- Determinar cuáles son universales y cuáles dependen del tipo de carta.
- Determinar cuáles deben almacenarse y cuáles pueden calcularse.
- Determinar cuáles se eliminan o reinician cuando una carta cambia de zona.
- Determinar cómo se representan y cuándo expiran los estados temporales.
- Determinar qué estados son mutuamente excluyentes.

### 0.5 Propietario

#### Definición

El propietario de una carta —denominado «dueño» en las reglas oficiales— es el
jugador que comenzó la partida con dicha carta en su Mazo Castillo, incluyendo el
Oro Inicial.

El propietario de una carta no cambia durante la partida.

#### Propiedades relevantes

- Toda carta utilizada en una partida posee un propietario.
- El propietario se determina al comienzo de la partida.
- El propietario permanece asociado a la carta aunque otro jugador obtenga
  su control.

#### Relaciones

El propietario de una carta determina a qué zonas del jugador debe enviarse
la carta cuando una regla o efecto indique que debe volver a una zona
correspondiente a su dueño.

Por ejemplo:

- Una carta destruida es enviada al Cementerio de su propietario.
- Una carta desterrada es enviada a la Zona de Destierro de su propietario.
- Una carta que debe ser barajada en un Mazo Castillo se envía al Mazo
  Castillo de su propietario.

#### Implicancias para el motor

El motor debe:

- Asociar permanentemente cada carta con un jugador propietario.
- Mantener esta asociación aunque cambie el controlador de la carta.
- Poder determinar las zonas pertenecientes al propietario.
- Utilizar el propietario para resolver movimientos de cartas cuando una
  regla lo requiera.

#### Dudas pendientes

- Determinar si existe alguna regla capaz de modificar el propietario de una carta.

### 0.6 Controlador

#### Definición

El controlador de una carta es el jugador en cuyas zonas del Campo de Batalla
se encuentra actualmente dicha carta.

Una carta ubicada en el Campo de Batalla de un jugador es una carta controlada
por ese jugador. Para el otro jugador, dicha carta se considera una carta
oponente.

Las cartas situadas fuera del Campo de Batalla tienen propietario, pero no se
consideran controladas por un jugador.

#### Propiedades relevantes

- Solo las cartas en juego poseen un controlador.
- El controlador se determina a partir de la zona del Campo de Batalla en la que
  se encuentra la carta.
- El controlador y el propietario pueden ser jugadores distintos.
- El controlador puede cambiar durante la partida por efecto de una carta o
  habilidad.
- Un cambio de controlador no modifica al propietario de la carta.
- Salvo que el efecto indique una duración diferente, el cambio de controlador
  permanece mientras la carta continúe en juego.
- Al ganar el control de una carta, el nuevo controlador puede utilizar sus
  habilidades conforme a las demás reglas y restricciones del juego.

#### Cambio de controlador

Cuando un efecto hace que un jugador gane el control de una carta, la carta debe
pasar a la zona correspondiente del Campo de Batalla del nuevo controlador y
quedar Agrupada, salvo que el efecto indique otra cosa.

En los casos definidos expresamente por las reglas:

- un Oro cuyo controlador cambia se mueve a la Reserva de Oro del nuevo
  controlador;
- un Aliado cuyo controlador cambia se mueve a la Línea de Defensa del nuevo
  controlador, salvo que el efecto indique otra zona o condición.

El cambio de controlador no constituye una salida del juego, porque la carta
permanece dentro del Campo de Batalla.

Cuando la carta sale del juego, debe ser enviada a la zona correspondiente de su
propietario y deja de tener controlador.

#### Relaciones

El controlador de una carta está relacionado con:

- la zona del Campo de Batalla que ocupa;
- las acciones que el jugador puede realizar con ella;
- el uso de sus habilidades;
- las decisiones que deban tomar sus efectos;
- la identificación de cartas propias y cartas oponentes;
- los efectos que cambian el control de una carta.

Una carta de Arma jugada sobre un Aliado oponente es controlada por el controlador
de dicho Aliado. Por lo tanto, el controlador del Aliado es quien resulta afectado
por la habilidad del Arma, de acuerdo con las reglas aplicables a este tipo de
carta.

#### Implicancias para el motor

El motor debe:

- determinar el controlador de una carta en juego a partir de su zona actual;
- representar que una carta fuera del Campo de Batalla no tiene controlador;
- distinguir permanentemente entre propietario y controlador;
- permitir cambios de controlador sin modificar al propietario;
- mover la carta a la zona válida del nuevo controlador;
- aplicar la condición de Agrupada al cambiar el control, salvo excepción;
- conceder al nuevo controlador las acciones y decisiones permitidas sobre la
  carta;
- conservar la duración del efecto de cambio de control;
- enviar la carta a una zona de su propietario cuando salga del juego;
- impedir combinaciones incoherentes entre controlador y zona.

Siempre que sea posible, el controlador debe calcularse a partir de la zona de
la carta y no almacenarse como un dato independiente. De esta forma, una carta no
puede quedar asociada a una zona de un jugador y, simultáneamente, indicar que es
controlada por otro.

#### Dudas pendientes

- Determinar el procedimiento exacto cuando varios efectos sucesivos cambian el
  controlador de una misma carta.
- Determinar cómo se resuelve el fin de un efecto temporal de cambio de control
  si existieron otros cambios de controlador durante su duración.
- Verificar las zonas de destino y reglas particulares para cambios de control
  de Tótems y otros tipos de carta.
- Documentar por separado las restricciones para atacar o utilizar una carta
  inmediatamente después de que cambie de controlador.
### 0.7 Zona

#### Definición

Una Zona de Juego es un espacio definido por las reglas en el que pueden
encontrarse cartas durante una partida.

Las zonas se clasifican en zonas del Campo de Batalla y zonas fuera del Campo de
Batalla. Cada zona determina qué cartas puede contener, qué información es
visible y qué movimientos pueden realizarse desde ella o hacia ella.

#### Propiedades relevantes

- Toda carta debe encontrarse en una zona válida.
- Cada zona pertenece a un jugador, salvo que una regla futura establezca una
  zona compartida.
- Una zona puede ser pública o privada.
- Algunas zonas conservan un orden relevante de sus cartas.
- Una zona puede restringir los tipos de carta que admite.
- Una carta cambia de zona únicamente mediante una regla, acción o efecto válido.

#### Relaciones

La zona actual de una carta determina si está en juego, quién la controla y qué
reglas o efectos pueden interactuar con ella.

#### Implicancias para el motor

El motor debe representar para cada zona su propietario, clasificación,
visibilidad, orden, cartas admitidas y contenido actual. Todo movimiento debe
validar origen, destino y restricciones, y generar un cambio de estado de juego.

#### Dudas pendientes

- Confirmar si alguna regla de Primer Bloque crea zonas compartidas o temporales.
- Documentar, para cada zona ordenada, quién puede consultar o modificar el orden.

### 0.8 Campo de Batalla

#### Definición

El Campo de Batalla es el conjunto de zonas donde se encuentran las cartas que
controlan los jugadores. Sus cartas son públicas, permanecen visibles y se
consideran cartas en juego.

Salvo que una regla o efecto especifique otra zona, los efectos interactúan
únicamente con cartas del Campo de Batalla.

#### Propiedades relevantes

El Campo de Batalla comprende, para cada jugador:

- Reserva de Oro;
- Zona de Oro Pagado;
- Línea de Defensa;
- Línea de Ataque;
- Línea de Apoyo.

Cuando una carta sale del Campo de Batalla y llega a su destino, deja de
considerarse la misma carta para los efectos que seguían a la instancia anterior.

#### Relaciones

La ubicación dentro del Campo de Batalla determina el controlador y parte del
estado de una carta. Salir de él implica salir del juego, pero no necesariamente
ser destruida.

#### Implicancias para el motor

El motor debe derivar `en juego` y el controlador desde la zona actual. Al salir
una carta, debe cerrar relaciones y efectos ligados a la instancia anterior y
reiniciar los componentes de estado que no sobrevivan al cambio de zona, sin
perder su identidad física ni su propietario.

#### Dudas pendientes

- Enumerar exactamente qué modificadores y relaciones se eliminan al salir del
  Campo de Batalla.

### 0.9 Mazo Castillo

#### Definición

El Mazo Castillo es la zona ordenada que contiene el mazo de un jugador y recibe
el daño dirigido a su Castillo.

#### Propiedades relevantes

- Comienza la partida con 50 cartas, incluido el Oro Inicial antes de colocarlo
  en la Reserva de Oro.
- Es una zona privada y se encuentra fuera del Campo de Batalla.
- Sus cartas tienen propietario, pero no controlador.
- Por cada punto de daño recibido, la carta superior se coloca en el Cementerio
  de su propietario, salvo que una regla modifique ese procedimiento.
- Si queda sin cartas, su propietario pierde la partida; esta condición se
  comprueba en cada cambio de estado de juego.
- La regla general permite hasta tres copias de una carta con el mismo nombre;
  los Oros básicos y las restricciones vigentes se rigen por sus reglas propias.

#### Relaciones

Se relaciona con robar, buscar, barajar, botar cartas, recibir daño y comprobar
la derrota. Las cartas devueltas a un Mazo Castillo se envían al de su propietario.

#### Implicancias para el motor

El motor debe conservar su orden, restringir su información, identificar la
carta superior, barajarlo cuando corresponda y comprobar la derrota después de
cada cambio de estado pertinente.

#### Dudas pendientes

- Trasladar las reglas completas de construcción y legalidad a una sección de
  configuración de formatos.

### 0.10 Mano

#### Definición

La Mano es la zona privada donde se colocan las cartas que un jugador roba y
desde la cual se juegan normalmente las cartas.

#### Propiedades relevantes

- Se encuentra fuera del Campo de Batalla.
- Sus cartas tienen propietario, pero no controlador.
- El contenido es privado para el oponente, aunque la cantidad de cartas debe
  poder consultarse.
- El tamaño máximo normal es de ocho cartas y se comprueba en el momento indicado
  de la Fase Final; una regla o efecto puede modificarlo.

#### Relaciones

Recibe cartas robadas o subidas a la Mano y permite jugar, descartar o pagar
cartas cuando una regla o efecto lo autoriza.

#### Implicancias para el motor

El motor debe proteger la identidad de las cartas frente al oponente, hacer
pública su cantidad y aplicar el descarte por exceso solamente en el momento
reglamentario.

#### Dudas pendientes

- Documentar la preparación de la mano inicial y cualquier procedimiento de
  reemplazo o mulligan en la sección de preparación de partida.

### 0.11 Reserva de Oro

#### Definición

La Reserva de Oro es la zona del Campo de Batalla que contiene los Oros
disponibles para pagar costes de cartas y habilidades.

#### Propiedades relevantes

- Es pública y sus cartas están en juego.
- Comienza con el Oro Inicial del jugador.
- Los Oros pueden incorporarse desde la Mano según las reglas del turno o por
  efectos que lo permitan.
- Pagar un Oro normalmente lo mueve a la Zona de Oro Pagado.

#### Relaciones

Se relaciona con costes, generación de recursos, Zona de Oro Pagado y Fase de
Agrupación.

#### Implicancias para el motor

El motor debe distinguir Oros disponibles de Oros pagados, validar pagos y mover
las cartas empleadas a la zona correspondiente.

#### Dudas pendientes

- Documentar por separado Oros virtuales, costes alternativos y modificadores de
  coste.

### 0.12 Zona de Oro Pagado

#### Definición

La Zona de Oro Pagado es la zona del Campo de Batalla a la que se mueven los
Oros utilizados para pagar costes.

#### Propiedades relevantes

- Es pública y sus cartas continúan en juego.
- Sus Oros no están disponibles para un nuevo pago mientras permanezcan allí.
- En la Fase de Agrupación vuelven a la Reserva de Oro, salvo que una regla o
  efecto lo impida.

#### Relaciones

Se relaciona con la Reserva de Oro, el pago de costes y Agrupar.

#### Implicancias para el motor

El motor debe mover a esta zona cada Oro pagado y agruparlo automáticamente en
el momento correspondiente, respetando prohibiciones y efectos de reemplazo.

#### Dudas pendientes

- Precisar cómo se representan pagos parciales o simultáneos de varios Oros.

### 0.13 Línea de Defensa

#### Definición

La Línea de Defensa es la zona del Campo de Batalla donde entran normalmente los
Aliados y desde la cual pueden atacar al Mazo Castillo o bloquear ataques.

#### Propiedades relevantes

- Es pública y contiene principalmente Aliados en juego.
- Los Aliados que dejan de atacar regresan a esta zona al Agruparse.
- Un Aliado cuyo controlador cambia entra normalmente Agrupado en la Línea de
  Defensa del nuevo controlador.

#### Relaciones

Se relaciona con jugar Aliados, declarar ataques, bloquear y la Línea de Ataque.

#### Implicancias para el motor

El motor debe validar qué cartas pueden ocuparla y qué Aliados están habilitados
para atacar o bloquear según su estado y las reglas del turno.

#### Dudas pendientes

- Definir todas las condiciones de habilitación para atacar y bloquear.

### 0.14 Línea de Ataque

#### Definición

La Línea de Ataque es la zona del Campo de Batalla a la que se mueven los Aliados
declarados atacantes durante la Batalla Mitológica.

#### Propiedades relevantes

- Es pública y contiene Aliados atacantes.
- Un Aliado en esta zona no puede bloquear ataques oponentes.
- En la Fase de Agrupación, sus Aliados regresan a la Línea de Defensa, salvo
  que una regla o efecto lo impida.

#### Relaciones

Se relaciona con declaración de ataque, bloqueo, asignación de daño y Agrupar.

#### Implicancias para el motor

El motor debe conservar la participación de cada Aliado en el combate y sus
relaciones con bloqueadores hasta que la secuencia correspondiente termine.

#### Dudas pendientes

- Definir cuándo se eliminan las relaciones de ataque y bloqueo si una carta
  cambia de zona durante el combate.

### 0.15 Línea de Apoyo

#### Definición

La Línea de Apoyo es la zona del Campo de Batalla donde entran en juego y
permanecen normalmente las cartas de Tótem.

#### Propiedades relevantes

- Es pública y sus cartas están en juego.
- Los Tótems permanecen allí hasta que una regla, habilidad o efecto los mueva.

#### Relaciones

Se relaciona con jugar o poner en juego Tótems y con sus habilidades activadas,
disparadas o continuas.

#### Implicancias para el motor

El motor debe validar los tipos admitidos y mantener activos los efectos de sus
cartas mientras correspondan.

#### Dudas pendientes

- Verificar si algún tipo adicional de carta puede ocupar esta zona.

### 0.16 Cementerio

#### Definición

El Cementerio es la zona pública que recibe cartas descartadas, destruidas,
anuladas o botadas desde el Mazo Castillo, además de otras cartas enviadas allí
por reglas o efectos.

#### Propiedades relevantes

- Se encuentra fuera del Campo de Batalla.
- Sus cartas tienen propietario, pero no controlador.
- Cada carta se envía al Cementerio de su propietario.
- Su contenido es visible para ambos jugadores.

#### Relaciones

Se relaciona con destruir, descartar, anular, botar, pagar costes, barajar y
efectos que interactúan expresamente con el Cementerio.

#### Implicancias para el motor

El motor debe mantener públicamente su contenido y registrar la causa y el
origen de cada movimiento cuando sean relevantes para habilidades disparadas.

#### Dudas pendientes

- Confirmar si el orden del Cementerio tiene relevancia reglamentaria y si puede
  modificarse libremente.

### 0.17 Destierro

#### Definición

La Zona de Destierro es la zona pública a la que se envían cartas cuando una
regla, habilidad o efecto las destierra.

#### Propiedades relevantes

- Se encuentra fuera del Campo de Batalla.
- Sus cartas tienen propietario, pero no controlador.
- Una carta desterrada no puede abandonar esta zona salvo que una regla,
  habilidad o efecto lo permita expresamente.
- Cada carta se envía a la Zona de Destierro de su propietario.

#### Relaciones

Puede recibir cartas desde el Campo de Batalla, Mazo Castillo, Mano, Cementerio u
otra zona permitida por el efecto que produce el destierro.

#### Implicancias para el motor

El motor debe impedir movimientos no autorizados desde esta zona y distinguir
el destierro de la destrucción y de otros cambios de zona.

#### Dudas pendientes

- Determinar si el orden de las cartas desterradas tiene relevancia.

### 0.18 Zonas fuera del Campo de Batalla

#### Definición

Las zonas fuera del Campo de Batalla son los espacios donde se encuentran cartas
de las que los jugadores son propietarios, pero que no controlan.

Esta categoría comprende:

- Mazo Castillo;
- Mano;
- Cementerio;
- Zona de Destierro.

No constituye una zona adicional que contenga físicamente esas cuatro zonas.

#### Propiedades relevantes

- Sus cartas no están en juego.
- Sus cartas no tienen controlador.
- Pueden ser públicas o privadas según la zona específica.
- Los efectos no interactúan con ellas salvo que una regla o texto lo permita.

#### Relaciones

Una carta que pasa desde el Campo de Batalla a una de estas zonas sale del juego.
Una carta que abandona una de estas zonas no entra necesariamente en juego: eso
depende de la zona de destino y del procedimiento que produjo el movimiento.

#### Implicancias para el motor

El motor debe representar esta clasificación como una propiedad de las zonas,
no como un contenedor adicional. También debe eliminar el controlador y aplicar
el reinicio de estado correspondiente cuando una carta salga del Campo de Batalla.

#### Dudas pendientes

- Adoptar en todo el proyecto una expresión técnica inequívoca para distinguir
  `fuera del Campo de Batalla` de efectos que eventualmente usen la frase
  `fuera del juego` con otro significado.

## 1. Preparación de la partida

### 1.1 Objetivo y resultado

#### Definición

La preparación de la partida es el proceso que transforma dos configuraciones de
jugador y sus mazos en un estado de juego válido, listo para comenzar el primer
turno.

#### Resultado esperado

Al finalizar la preparación:

- existen dos jugadores identificados;
- cada jugador posee sus zonas de juego;
- cada carta posee una identidad individual y un propietario;
- cada jugador tiene un Oro Inicial en su Reserva de Oro;
- cada Mazo Castillo está barajado;
- cada jugador conserva una mano inicial aceptada;
- se conoce qué jugador tendrá el primer turno;
- ninguna acción del primer turno se ha realizado todavía.

#### Implicancias para el motor

La preparación debe ejecutarse como una secuencia controlada. Si una validación
obligatoria falla, la partida no debe comenzar y el motor debe informar la causa.

### 1.2 Selección del formato y versión de reglas

#### Procedimiento

Antes de validar los mazos, la partida debe seleccionar una configuración que
incluya:

- formato de Primer Bloque;
- fecha o versión de legalidad;
- versión de reglas;
- lista de cartas permitidas, limitadas y prohibidas;
- excepciones de construcción aplicables;
- reglas opcionales de preparación, si existen.

#### Implicancias para el motor

La configuración seleccionada debe permanecer asociada a la partida y formar
parte de su registro reproducible.

#### Formato inicial del simulador

El primer formato implementado será **Racial Edición**, denominado también
`Racial soporte edición` en la documentación oficial.

Para construir un mazo de este formato, el jugador debe:

- elegir una raza disponible de Primer Bloque;
- utilizar Aliados de la raza elegida;
- seleccionar la edición original a la que pertenece la raza;
- utilizar cartas de soporte pertenecientes a esa edición o a sus productos
  derivados permitidos;
- incluir al menos 16 cartas de Aliado;
- respetar la lista de cartas prohibidas y limitadas vigente para la fecha de la
  configuración.

Espada Sagrada, Helénica, Hijos de Daana y Dominios de Ra son **ediciones**, no
razas. Las razas de Primer Bloque son Caballero, Dragón, Faerie, Titán, Olímpico,
Héroe, Defensor, Sombra, Desafiante, Sacerdote, Eterno y Faraón.

Las asociaciones principales entre edición original y producto de soporte son:

- Espada Sagrada / Cruzadas;
- Helénica / Imperio;
- Hijos de Daana / Tierras Altas;
- Dominios de Ra / Encrucijada.

Las cartas de productos externos a estas líneas no son legales salvo que una
reimpresión o resolución oficial las incorpore expresamente al formato. Esta
legalidad debe representarse por carta y versión, porque dos impresiones con el
mismo nombre pueden tener condiciones de legalidad diferentes.

La configuración inicial utilizará la lista oficial de Racial Edición vigente al
17 de septiembre de 2026, cuya actualización comenzó a regir el 5 de septiembre
de 2026. Las modificaciones posteriores deben crear una nueva versión de la
configuración y no alterar partidas ya iniciadas o guardadas.

### 1.3 Validación de jugadores y mazos

#### Precondiciones

Cada jugador debe proporcionar una identidad y un mazo completo antes de iniciar
la preparación.

#### Procedimiento

El motor debe comprobar, como mínimo:

1. que participen exactamente dos jugadores distintos;
2. que cada mazo tenga exactamente 50 cartas, contando el Oro Inicial;
3. que todas las cartas sean legales para la configuración seleccionada;
4. que se cumplan los límites de copias por nombre;
   una carta con la habilidad **Única** tiene un límite de una copia en el Mazo
   Castillo;
5. que exista al menos una carta elegible como Oro Inicial;
6. que todos los Aliados pertenezcan a la raza seleccionada;
7. que esa raza pertenezca a la edición seleccionada;
8. que las cartas de soporte correspondan a la edición seleccionada o a un producto
   derivado autorizado;
9. que el mazo contenga al menos 16 Aliados;
10. que se cumpla cualquier otra restricción de Racial Edición vigente en la
   configuración seleccionada.

La restricción Única se aplica durante la construcción del mazo. No limita el
número de veces que la misma copia puede jugarse durante la partida si vuelve a
la Mano, al Cementerio o a otra zona desde la cual exista autorización para
jugarla.

#### Resultado

La validación produce un resultado válido o una lista de infracciones. Una
partida competitiva no puede comenzar con infracciones pendientes.

#### Dudas pendientes

- Convertir la lista oficial de cartas prohibidas y limitadas de septiembre de
  2026 en datos estructurados cuando se cree el catálogo de cartas.
- Determinar si el simulador permitirá un modo de prueba que omita algunas
  restricciones de construcción sin modificar las reglas de resolución.

### 1.4 Creación del estado inicial

#### Procedimiento

Una vez validados los mazos, el motor debe:

1. crear la partida y los dos jugadores;
2. crear las zonas pertenecientes a cada jugador;
3. crear una instancia individual para cada carta física del mazo;
4. asignar permanentemente el propietario de cada instancia;
5. colocar inicialmente las 50 cartas en el Mazo Castillo de su propietario;
6. inicializar el resto de las zonas vacías;
7. establecer que todavía no existe un jugador activo ni un turno iniciado.

#### Invariantes

- Cada carta existe una sola vez dentro del estado de la partida.
- Cada carta ocupa exactamente una zona.
- Ninguna carta tiene controlador mientras todas permanezcan en los Castillos.
- No existen efectos, modificadores ni relaciones de combate activos.

#### Implicancias para el motor

Las definiciones de carta compartidas por varias copias no sustituyen a sus
instancias. Dos copias con el mismo nombre deben conservar identificadores
individuales durante toda la partida.

### 1.5 Determinación del primer jugador

#### Procedimiento

Antes de elegir los Oros Iniciales, debe determinarse al azar qué jugador tendrá
el primer turno. Puede utilizarse cualquier método imparcial acordado por los
jugadores.

En una partida simulada, el resultado debe obtenerse mediante el generador de
azar de la partida y quedar registrado.

#### Resultado

El jugador seleccionado se registra como `primer jugador`, pero todavía no se
convierte en jugador activo hasta que comience formalmente el primer turno.

#### Implicancias para el motor

El motor debe permitir reproducir el resultado usando la semilla o el registro
de eventos de la partida.

### 1.6 Selección y colocación del Oro Inicial

#### Procedimiento

Después de determinar quién comienza, cada jugador elige de su Mazo Castillo una
carta legal como Oro Inicial y la coloca en su Reserva de Oro.

Ambas cartas:

- conservan a su propietario;
- pasan a estar en juego;
- quedan bajo el control del propietario de su Reserva de Oro;
- se consideran disponibles para pagar costes cuando las reglas lo permitan.

#### Validación

La carta elegida debe cumplir las condiciones de Oro Inicial establecidas por la
configuración del formato. El motor no debe asumir que cualquier Oro es elegible.

#### Resultado

Cada Reserva de Oro contiene exactamente un Oro Inicial y cada Mazo Castillo
contiene 49 cartas antes de barajar y formar las manos.

#### Dudas pendientes

- Incorporar a la configuración la lista o condición exacta de Oros Iniciales
  permitidos en el formato seleccionado.
- Determinar si la identidad del Oro Inicial es información que debe declararse
  simultáneamente o siguiendo un orden entre jugadores.

### 1.7 Barajado de los Mazos Castillo

#### Procedimiento

Después de colocar los Oros Iniciales, cada jugador baraja las 49 cartas restantes
de su Mazo Castillo. El resultado debe ser un orden aleatorio no conocido por
ninguno de los jugadores.

#### Implicancias para el motor

El motor debe:

- utilizar una fuente de azar controlada por la partida;
- impedir que los jugadores consulten el orden resultante;
- registrar información suficiente para reproducir o auditar el barajado sin
  revelar el orden a quien no corresponda;
- mantener identificables la carta superior y la inferior internamente.

### 1.8 Formación de la mano inicial

#### Procedimiento

Después de barajar, cada jugador roba las ocho cartas superiores de su Mazo
Castillo y las coloca en su Mano.

#### Resultado

Antes de cualquier mulligan, cada jugador tiene:

- un Oro Inicial en su Reserva de Oro;
- ocho cartas en la Mano;
- 41 cartas en el Mazo Castillo;
- las demás zonas vacías.

#### Implicancias para el motor

Las cartas deben robarse respetando el orden del Castillo. La identidad de la
Mano solo es visible para su propietario, mientras su cantidad es pública.

### 1.9 Mulligan

#### Definición

El mulligan permite que un jugador rechace su mano inicial y obtenga una nueva
con una carta menos.

#### Procedimiento

Para cada jugador que decida realizarlo:

1. devuelve todas las cartas de su Mano al Mazo Castillo;
2. baraja el Mazo Castillo completo;
3. roba una nueva mano con una carta menos que la mano rechazada;
4. decide si conserva la nueva mano o repite el procedimiento.

El proceso puede repetirse hasta que el jugador conserve su mano o llegue a una
mano de una sola carta. Una mano de una carta no puede reducirse nuevamente por
el mulligan tradicional.

#### Información

La decisión de realizar mulligan y la cantidad de cartas de cada nueva mano son
públicas. La identidad de las cartas continúa siendo privada.

#### Implicancias para el motor

El motor debe registrar por separado las decisiones de ambos jugadores, impedir
que una decisión revele cartas privadas y permitir que cada jugador complete su
proceso antes de iniciar la partida.

#### Dudas pendientes

- Verificar si la regla de mulligan gratuito publicada en 2026 resulta aplicable
  al formato de Primer Bloque seleccionado. Hasta confirmarlo, solo se implementa
  el mulligan tradicional descrito en esta sección.
- Definir el protocolo exacto de alternancia o simultaneidad de las decisiones de
  mulligan en partidas competitivas.

### 1.10 Estado listo para comenzar

#### Condiciones de finalización

La preparación termina únicamente cuando:

- ambos mazos fueron validados;
- se determinó el primer jugador;
- ambos Oros Iniciales están en sus Reservas de Oro;
- ambos Castillos fueron barajados;
- ambos jugadores aceptaron su mano;
- todas las cartas se encuentran en zonas válidas;
- no existe ninguna infracción de preparación pendiente.

#### Transición al juego

Cumplidas las condiciones, el motor genera el evento de partida preparada. El
siguiente proceso será el comienzo del primer turno, donde se asignará el jugador
activo y se aplicarán las excepciones propias de ese turno.

#### Implicancias para el motor

El estado preparado debe poder serializarse, validarse y reproducirse. El motor
debe impedir acciones normales de turno antes de completar esta transición.

### 1.11 Casos de prueba derivados

La futura suite de pruebas debe comprobar, como mínimo:

1. rechazo de un mazo con cantidad incorrecta de cartas;
2. rechazo de cartas ilegales o exceso de copias;
3. creación de 100 instancias de carta distintas entre ambos jugadores;
4. asignación correcta y permanente de propietarios;
5. colocación de un Oro Inicial válido por jugador;
6. reducción de cada Castillo de 50 a 49 cartas antes del robo inicial;
7. formación de manos iniciales de ocho cartas y Castillos de 41;
8. mulligans sucesivos de ocho a siete, seis y hasta una carta;
9. retorno y barajado completo de la mano rechazada;
10. privacidad de las manos y del orden de los Castillos;
11. registro reproducible del primer jugador y de los barajados;
12. imposibilidad de iniciar el primer turno mientras falte una condición de
    preparación.

## 2. Sistema de turnos

### 2.1 Turno, jugador activo y jugador inactivo

#### Definición

Un turno es la secuencia ordenada de fases durante la cual uno de los jugadores
actúa como jugador activo. El otro jugador es el jugador inactivo.

La condición de jugador activo no equivale a tener prioridad para cualquier
acción. La fase, el paso y las reglas de prioridad determinan quién puede actuar
en cada momento.

#### Propiedades relevantes

- Los jugadores alternan sus turnos.
- Solo existe un jugador activo a la vez.
- El jugador que fue determinado primero durante la preparación es el jugador
  activo del primer turno.
- Cada cambio de fase o paso produce un cambio de estado de juego.
- Las habilidades continuas deben reevaluarse después de cada cambio de estado.
- Las condiciones de derrota deben comprobarse en los momentos exigidos por las
  reglas, incluido cada cambio de estado de juego pertinente.

#### Implicancias para el motor

El estado debe identificar el número de turno, jugador activo, jugador inactivo,
fase y paso actuales. Las acciones deben validarse contra todos esos datos.

### 2.2 Orden general del turno

#### Secuencia

Un turno normal sigue este orden:

1. Fase de Agrupación;
2. Fase de Vigilia;
3. Fase de Batalla Mitológica, si el jugador activo decide atacar;
4. Fase Final;
5. finalización del turno y cambio de jugador activo.

La Batalla Mitológica es opcional. Si no se inicia, la Fase de Vigilia transita
directamente a la Fase Final.

#### Reglas de transición

- Una fase no puede comenzar antes de concluir todos los pasos obligatorios de
  la fase anterior.
- Las habilidades y efectos pendientes deben resolverse según las reglas antes
  de completar una transición.
- Una decisión de pasar de fase es irreversible una vez realizada la transición,
  salvo que una regla disponga expresamente lo contrario.

#### Implicancias para el motor

El turno debe modelarse como una máquina de estados y no como una lista de
acciones que los jugadores puedan recorrer libremente.

### 2.3 Excepciones del primer turno

#### Reglas

En el primer turno de la partida:

- no existe Fase de Agrupación;
- el turno comienza en la Fase de Vigilia;
- el jugador activo no roba una carta durante la Fase Final.

Las demás fases y decisiones se conservan. Una acción solo puede omitirse si las
reglas generales, el estado de juego o una regla específica así lo determinan.

#### Implicancias para el motor

El motor debe representar estas excepciones mediante el número global del turno,
no mediante condiciones dispersas en las cartas o zonas.

### 2.4 Fase de Agrupación

#### Definición

La Fase de Agrupación es la primera fase de un turno normal. En ella se agrupan
automáticamente las cartas que deban y puedan agruparse.

#### Orden de resolución

La fase se desarrolla en este orden:

1. Los Aliados que deban y puedan agruparse se mueven de la Línea de Ataque a la
   Línea de Defensa del mismo controlador.
2. Los Oros que deban y puedan agruparse se mueven de la Zona de Oro Pagado a la
   Reserva de Oro del mismo controlador.
3. Se disparan y resuelven las habilidades que indiquen «en la Fase de
   Agrupación» o una condición equivalente.
4. Pueden jugarse las cartas autorizadas expresamente para esta fase.
5. Concluyen los efectos cuya duración indique «hasta la próxima Fase de
   Agrupación» o «hasta el próximo turno» y que estén vigentes desde turnos
   anteriores.

#### Restricciones

- Agrupar es automático, salvo que un efecto o habilidad lo impida.
- Una carta impedida de agruparse permanece en su zona actual.
- La ausencia de cartas que agrupar no elimina los demás pasos de la fase.
- Solo los Aliados en Línea de Ataque y los Oros en Zona de Oro Pagado son
  objetivos válidos de efectos que indiquen Agrupar, salvo regla expresa.

#### Implicancias para el motor

El motor debe procesar los movimientos de Agrupar, generar los cambios de estado
correspondientes y luego continuar con habilidades, acciones permitidas y
expiración de efectos en el orden indicado.

#### Dudas pendientes

- Precisar el orden entre múltiples habilidades disparadas en esta fase dentro
  de la sección futura de resolución de habilidades simultáneas.

### 2.5 Fase de Vigilia

#### Definición

La Fase de Vigilia es la fase principal en la que el jugador activo puede poner
un Oro de su Mano, jugar cartas y utilizar habilidades.

#### Orden de resolución

La fase se desarrolla en este orden:

1. Se disparan y resuelven las habilidades que indiquen «al comienzo de tu
   Vigilia» o una condición equivalente.
2. El jugador activo recibe una oportunidad para poner un Oro de su Mano en su
   Reserva de Oro.
3. El jugador activo puede jugar cartas o utilizar habilidades mientras conserve
   la facultad de hacerlo y cumpla sus condiciones y costes.
4. Como última decisión de la fase, si controla Aliados que pueden atacar, elige
   entre iniciar una Batalla Mitológica o pasar a la Fase Final. Si no puede
   iniciar un ataque, pasa a la Fase Final.

#### Regla del Oro de turno

La primera carta que el jugador activo puede poner desde su Mano durante la
Vigilia es un Oro. Si renuncia a esa oportunidad y realiza otra acción que haga
avanzar la fase, ya no puede poner normalmente un Oro de su Mano durante el resto
del turno.

Los efectos y habilidades que pongan Oros en juego constituyen excepciones y no
deben confundirse con la oportunidad normal de poner el Oro de turno.

#### Cartas y habilidades

Por regla general, Aliados, Armas, Tótems y Talismanes se juegan en esta fase.
Una carta o habilidad puede establecer otro momento permitido.

#### Implicancias para el motor

El turno debe registrar si la oportunidad de Oro está disponible, fue utilizada
o fue omitida. También debe validar el momento, zona de origen, costes, objetivos
y restricciones antes de aceptar cada acción.

#### Dudas pendientes

- Definir con precisión qué acción cierra la oportunidad normal de poner Oro si
  existen habilidades automáticas o respuestas antes de la primera acción
  voluntaria del jugador.

### 2.6 Fase de Batalla Mitológica

#### Definición

La Batalla Mitológica es una fase opcional que solo existe si el jugador activo
decide realizar un ataque. Una vez iniciada, todos sus pasos se ejecutan en orden,
aunque en alguno no se realicen acciones.

#### Pasos

La fase contiene:

1. Declaración de Ataque.
2. Declaración de Bloqueo.
3. Guerra de Talismanes.
4. Asignación de Daño.

#### Declaración de Ataque

El jugador activo selecciona los Aliados atacantes válidos y los mueve de su
Línea de Defensa a su Línea de Ataque. Luego se disparan y resuelven las
habilidades que interactúan con la declaración.

Por regla general, un Aliado debe haber permanecido en juego bajo el control de
su controlador desde la última Fase de Agrupación de ese jugador. Furia permite
ignorar este requisito en los términos definidos por dicha habilidad.

#### Declaración de Bloqueo

El jugador inactivo puede asignar Aliados de su Línea de Defensa para bloquear.
La asignación básica es de un bloqueador a un atacante y bloquear es opcional.
Después se disparan y resuelven las habilidades asociadas a la declaración.

#### Guerra de Talismanes

El jugador defensor recibe la primera prioridad. Los jugadores pueden jugar
Talismanes o utilizar habilidades permitidas y alternan la prioridad hasta que
ambos la ceden consecutivamente.

Si el ataque es cancelado, los Aliados atacantes regresan a la Línea de Defensa,
pero la Guerra de Talismanes no termina por ese solo hecho.

#### Asignación de Daño

Se aplican las reglas de daño de combate, se procesan las ventanas de prevención
y se resuelven las habilidades relacionadas con el daño y con los Aliados que
deban ser destruidos. El cálculo detallado se documentará en la sección de
combate.

#### Implicancias para el motor

El motor debe conservar atacantes, bloqueadores, emparejamientos, prioridad,
cesiones consecutivas y estado de cancelación del ataque. No debe saltar pasos
solo porque no existan acciones disponibles.

### 2.7 Fase Final

#### Definición

La Fase Final cierra el turno, tanto si ocurrió una Batalla Mitológica como si el
jugador activo decidió no atacar.

#### Orden de resolución

La fase se desarrolla en este orden:

1. Se disparan y resuelven las habilidades que indiquen «en la Fase Final».
2. Concluyen los efectos que indiquen «hasta la Fase Final», «durante el resto
   del turno» o «este turno».
3. Desaparecen los Oros virtuales.
4. El jugador activo roba una carta, excepto durante el primer turno de la
   partida.
5. Se disparan y resuelven los efectos que interactúan con Robar cartas.
6. Si la Mano del jugador activo supera su tamaño máximo, normalmente ocho,
   descarta hasta alcanzar ese límite.
7. Se disparan y resuelven las habilidades y efectos relacionados con las cartas
   descartadas en el paso anterior.
8. Termina el turno y comienza el turno del oponente.

#### Regla sobre el tamaño final de la Mano

Si una habilidad disparada por el descarte agrega cartas después de la
comprobación del límite, el jugador puede terminar el turno con más cartas que su
tamaño máximo. No se realiza una segunda comprobación salvo que una regla lo
indique.

#### Implicancias para el motor

Cada paso debe ejecutarse una sola vez y en el orden indicado. El robo, el
descarte y sus habilidades derivadas deben generar cambios de estado separados.

### 2.8 Finalización y comienzo del turno siguiente

#### Procedimiento

Al concluir la Fase Final, el motor debe:

1. cerrar las ventanas y relaciones que expiran con el turno;
2. incrementar el contador global de turnos;
3. convertir al anterior jugador inactivo en jugador activo;
4. convertir al anterior jugador activo en jugador inactivo;
5. iniciar la Fase de Agrupación del nuevo jugador activo;
6. comprobar las condiciones de finalización de la partida antes de aceptar una
   nueva acción.

#### Invariantes

- No puede haber dos fases o pasos activos simultáneamente.
- No puede cambiar el jugador activo en mitad de un turno salvo regla expresa.
- Ninguna acción puede ejecutarse después de terminar una fase usando permisos
  exclusivos de esa fase.
- Los efectos temporales deben expirar en el punto exacto indicado por su
  duración.

### 2.9 Estado técnico mínimo del turno

El estado del turno debe permitir consultar, como mínimo:

- número global de turno;
- jugador activo e inactivo;
- fase y paso actuales;
- si es el primer turno de la partida;
- disponibilidad de la oportunidad de Oro;
- si la Batalla Mitológica fue iniciada;
- jugador que posee la prioridad, cuando corresponda;
- número de cesiones consecutivas;
- atacantes, bloqueadores y sus asignaciones;
- acciones y habilidades pendientes de resolución;
- efectos temporales asociados al turno o a una fase.

Siempre que sea posible, los permisos de acción deben derivarse de este estado y
no almacenarse como indicadores independientes que puedan contradecirse.

### 2.10 Casos de prueba derivados

La futura suite de pruebas debe comprobar, como mínimo:

1. comienzo del primer turno directamente en Vigilia;
2. ausencia de robo durante la Fase Final del primer turno;
3. alternancia correcta del jugador activo;
4. Agrupación de Aliados y Oros en sus zonas correspondientes;
5. permanencia de una carta cuando un efecto impide Agruparla;
6. resolución ordenada de habilidades y expiraciones de Agrupación;
7. uso u omisión irreversible de la oportunidad normal de poner Oro;
8. tránsito directo de Vigilia a Fase Final cuando no se ataca;
9. ejecución de los cuatro pasos de Batalla aunque alguno no tenga acciones;
10. primera prioridad del defensor en Guerra de Talismanes;
11. finalización de la Guerra tras dos cesiones consecutivas;
12. continuidad de la Guerra cuando un ataque es cancelado;
13. orden completo de la Fase Final;
14. descarte hasta el tamaño máximo de Mano;
15. posibilidad de terminar con más cartas después de resolver habilidades
    disparadas por el descarte;
16. rechazo de acciones realizadas en una fase o paso incorrectos;
17. reevaluación de habilidades continuas después de cada cambio de estado;
18. expiración de efectos temporales en su punto reglamentario.

### 2.11 Dudas pendientes

- Integrar el orden completo de habilidades simultáneas cuando se documente el
  sistema de efectos.
- Precisar las ventanas de acciones permitidas fuera de Vigilia y Guerra de
  Talismanes.
- Determinar si alguna aclaración vigente de Primer Bloque modifica el orden de
  los pasos descrito por el Documento Actualizado de Reglas.

## 3. Jugar y poner cartas en juego

### 3.1 Diferencia entre jugar y poner en juego

#### Jugar una carta

Jugar una carta es iniciar el procedimiento reglamentario que incluye declarar
la carta, seleccionar objetivos cuando corresponda, calcular y pagar sus costes,
abrir las ventanas de interacción y, si no es anulada, resolverla.

Por regla general, las cartas se juegan desde la Mano durante la Fase de Vigilia.
Una regla, habilidad o efecto puede permitir jugarlas desde otra zona o en otro
momento.

#### Poner una carta en juego

Poner en juego es mover una carta al Campo de Batalla por una regla, habilidad o
efecto sin ejecutar el procedimiento de jugarla.

Una carta puesta en juego:

- no paga su coste de Oro, salvo que el efecto establezca otro coste;
- no puede ser anulada como carta jugada;
- no dispara habilidades que exijan que una carta sea jugada;
- sí entra en juego y dispara las habilidades asociadas a entrar en juego.

#### Implicancias para el motor

`Jugar` y `poner en juego` deben ser acciones diferentes. Ambas pueden terminar
con una carta en el Campo de Batalla, pero generan eventos y ventanas distintos.

### 3.2 Tipos de carta y forma de ingreso

#### Reglas generales

- Los Aliados, Armas, Tótems y Talismanes pueden jugarse.
- Los Oros se ponen en juego; no se consideran jugados y no pueden ser anulados.
- Un efecto que permita «jugar una carta sin pagar su coste» sigue jugando la
  carta y no permite elegir un Oro, salvo regla expresa.
- Una carta jugada sin pagar su coste debe satisfacer las demás condiciones,
  objetivos y costes adicionales aplicables.

#### Destino al resolverse

Si una carta jugada no es anulada:

- un Aliado entra normalmente en la Línea de Defensa de su controlador;
- un Arma entra en juego portada por el objetivo válido seleccionado;
- un Tótem entra normalmente en la Línea de Apoyo de su controlador;
- un Talismán aplica su efecto y después es enviado al Cementerio de su
  propietario, salvo que una regla indique otro destino.

#### Dudas pendientes

- Documentar todas las excepciones de destino impresas en cartas específicas.

### 3.3 Solicitud de jugar una carta

#### Precondiciones

Antes de iniciar el procedimiento, el motor debe comprobar:

- que la partida se encuentre en una fase, paso o ventana válida;
- que el jugador tenga permiso para realizar la acción;
- que la carta se encuentre en una zona desde la que pueda jugarse;
- que no exista una prohibición aplicable;
- que se cumplan las condiciones de juego de la carta;
- que existan todos los objetivos obligatorios válidos;
- que todos los costes obligatorios puedan pagarse completamente.

Si una precondición falla, la jugada no se inicia y no se paga ningún coste.

#### Implicancias para el motor

Validar una intención no debe modificar el estado. El cambio comienza solamente
cuando el motor acepta la declaración como una jugada legal.

### 3.4 Declaración y selección de objetivos

#### Procedimiento

El jugador declara la carta que jugará y selecciona sus objetivos obligatorios.
Los objetivos se fijan antes de pagar los costes.

Un elemento es objetivo cuando el texto permite elegir qué carta, jugador, zona,
habilidad u otro elemento será afectado. Si el texto exige elegir, el elemento
seleccionado se considera objetivo incluso cuando solo exista una opción válida.

#### Validación

Cada objetivo debe cumplir todos los requisitos en el momento de la declaración.
Una carta o habilidad que requiere una cantidad exacta de objetivos no puede
iniciarse si no existen suficientes objetivos válidos.

Que un objetivo sea válido al declarar no garantiza que el efecto vaya a
afectarlo al resolverse. El estado y las protecciones aplicables se vuelven a
considerar en la resolución cuando corresponda.

#### Cantidades expresadas como «hasta N»

Una instrucción que permita elegir **hasta N** cartas u objetivos permite elegir
cualquier cantidad entera entre cero y N, ambos incluidos. Por ejemplo, «hasta 2»
permite elegir cero, uno o dos.

#### Dudas pendientes

- Precisar cuándo un objetivo que deja de ser válido provoca que falle una parte
  o la totalidad del efecto.

### 3.5 Cálculo y pago de costes

#### Procedimiento

Después de seleccionar objetivos, el motor calcula el coste de la carta:

1. parte de su coste de Oro aplicable;
2. aplica las reducciones de coste;
3. incorpora los costes adicionales;
4. determina el total de Oros y demás recursos que deben pagarse;
5. verifica nuevamente que el pago completo sea posible;
6. ejecuta el pago como una operación indivisible.

El coste de Oro puede reducirse hasta cero. Los costes adicionales no desaparecen
por jugar una carta sin pagar su coste de Oro, salvo que la regla lo indique.

#### Restricciones

- Un coste debe poder pagarse completamente para iniciar la jugada.
- Pagar un coste no hace objetivo.
- Los recursos pagados no pueden utilizarse simultáneamente para otro pago.
- Una vez pagados legalmente, los costes no se devuelven porque la carta sea
  anulada o su efecto no produzca cambios, salvo regla expresa.
- Las restricciones que mencionan el coste de una carta pueden referirse al coste
  impreso; cada regla deberá indicar qué valor utiliza.

#### Implicancias para el motor

El motor debe separar coste impreso, coste modificado, costes alternativos y
costes adicionales, además de registrar cada recurso consumido.

### 3.6 Carta en proceso de ser jugada

#### Estado transitorio

Después del pago, la carta se considera jugada, pero permanece físicamente en su
zona de origen hasta su resolución.

Mientras está siendo jugada:

- solo puede interactuarse con ella mediante efectos que permitan anularla;
- no puede descartarse, barajarse, desterrarse ni usarse para pagar otro coste;
- queda reservada para impedir acciones incompatibles o dobles usos;
- puede generar habilidades que se disparen cuando se juega una carta.

#### Implicancias para el motor

El motor necesita representar una jugada pendiente sin retirar prematuramente la
carta de su zona. La reserva transitoria debe liberarse al anular o resolver.

### 3.7 Habilidades disparadas por jugar

Una vez que la carta se considera jugada, se disparan las habilidades que
interactúan con esa acción. Estas habilidades se resuelven en el orden establecido
para múltiples habilidades antes de continuar con la resolución de la carta.

El detalle del orden entre controlador activo, controlador inactivo y habilidades
nuevas generadas durante la resolución se documentará en la sección de efectos.

### 3.8 Ventanas de anulación, respuesta y prevención

#### Anulación

Después de declarar objetivos y pagar costes, el oponente puede utilizar cartas o
habilidades que anulen la carta jugada. Anular evita que un Aliado, Arma o Tótem
entre en juego y evita que un Talismán resuelva su efecto.

Una carta anulada se considera jugada, pero no se considera entrada en juego. Su
destino normal es el Cementerio de su propietario, salvo que una regla, su zona
de origen o un efecto establezca otro resultado.

#### Respuestas

Las respuestas y anulaciones deben respetar el orden, las condiciones y la
cantidad de acciones permitidas por la ventana correspondiente. La especificación
de esta sección no presupone todavía cómo se encadenan varias respuestas.

#### Prevención

Antes de aplicar la resolución no anulada, el oponente dispone de la oportunidad
de usar cartas o habilidades de prevención cuando sus condiciones se cumplan.

#### Implicancias para el motor

El motor debe identificar la fuente actual de cada ventana y evitar que una
acción se aplique a una jugada distinta de aquella a la que legalmente responde.

#### Dudas pendientes

- Formalizar la cadena completa y el límite de acciones por ventana usando las
  aclaraciones oficiales vigentes de Primer Bloque.
- Determinar el destino exacto de cartas anuladas jugadas desde zonas con reglas
  restrictivas, especialmente la Zona de Destierro.

### 3.9 Resolución de una carta jugada

#### Procedimiento

Si la carta no fue anulada, intenta resolverse sobre el estado de juego actual.

- Un Talismán ejecuta sus instrucciones en el orden escrito y luego va a su zona
  de destino.
- Un Aliado, Arma o Tótem entra al Campo de Batalla en su zona válida.
- Se aplican inmediatamente las reglas y habilidades continuas pertinentes.
- Se generan los eventos y habilidades de entrada en juego correspondientes.

Los efectos se resuelven en la mayor medida posible, desde cero hasta la totalidad
de sus instrucciones, salvo que una condición o requisito exija una resolución
completa de una parte determinada.

#### Estado actual

Los objetivos y demás elementos se evalúan contra el estado existente al resolver,
no contra una copia congelada del estado de la declaración. Sin embargo, los
objetivos originales no pueden sustituirse libremente salvo que una regla permita
redirigirlos o cambiarlos.

#### Resultado

Resolver una carta no garantiza que modifique el estado. Una carta puede
resolverse sin efecto si ninguna instrucción aplicable logra producir un cambio.

### 3.10 Poner una carta en juego por un efecto

#### Precondiciones

El efecto debe identificar una carta válida y debe existir una zona válida del
Campo de Batalla a la que pueda ingresar.

#### Procedimiento

1. Se selecciona o determina la carta según el efecto.
2. Se valida que pueda moverse desde su zona actual y entrar en la zona indicada.
3. Se mueve directamente al Campo de Batalla.
4. Se determina su controlador desde la zona de destino.
5. Se aplican habilidades continuas.
6. Se disparan las habilidades de entrada en juego.

No se ejecutan los pasos de jugar una carta, no existe ventana para anularla como
carta jugada y no se disparan habilidades de «cuando juegues».

### 3.11 Eventos e información que debe registrar el motor

El procedimiento debe poder generar y registrar, como mínimo:

- intento de jugar carta;
- jugada declarada;
- objetivos seleccionados;
- coste calculado;
- coste pagado;
- carta jugada;
- habilidad disparada por la jugada;
- ventana de anulación, respuesta o prevención;
- carta anulada;
- carta resuelta;
- carta entrada en juego;
- carta puesta en juego sin ser jugada;
- cambio de zona resultante;
- resolución sin cambio de estado.

Los eventos públicos no deben revelar información privada adicional a la que la
acción obliga a mostrar.

### 3.12 Invariantes del procedimiento

- Una carta no puede jugarse dos veces mediante la misma declaración.
- Un mismo recurso no puede pagar dos costes simultáneamente.
- Una carta anulada no entra en juego ni genera habilidades de entrada.
- Una carta puesta en juego no genera un evento de carta jugada.
- Un Oro puesto en juego no puede ser anulado como carta jugada.
- Toda carta que entra en juego termina en una zona válida de su controlador.
- Toda carta que sale de una zona queda registrada inmediatamente en su destino.
- Ninguna jugada puede quedar indefinidamente en estado transitorio.

### 3.13 Casos de prueba derivados

La futura suite de pruebas debe comprobar, como mínimo:

1. rechazo de una carta jugada en una fase incorrecta;
2. rechazo de una carta jugada desde una zona no autorizada;
3. rechazo por objetivos insuficientes o inválidos;
4. rechazo cuando un coste no puede pagarse completamente;
5. aplicación de reducciones hasta un coste mínimo de cero;
6. conservación de costes adicionales al jugar sin pagar el coste de Oro;
7. reserva de la carta y los recursos durante la jugada;
8. disparo de habilidades de «cuando juegues» después del pago;
9. anulación después de seleccionar objetivos y pagar costes;
10. ausencia de devolución de costes tras una anulación;
11. ausencia de habilidades de entrada para una carta anulada;
12. entrada de Aliados, Armas y Tótems en sus destinos válidos;
13. resolución y posterior envío de un Talismán al Cementerio;
14. resolución sin efecto cuando no puede modificarse el estado;
15. ingreso directo de una carta puesta en juego;
16. ausencia de evento `carta_jugada` al poner una carta en juego;
17. generación de habilidades de entrada al poner una carta en juego;
18. imposibilidad de anular un Oro puesto en juego;
19. conservación de información privada al jugar desde zonas ocultas;
20. liberación del estado transitorio después de anular o resolver.

### 3.14 Dudas pendientes

- Especificar completamente anulaciones, respuestas, prevención y cadenas.
- Definir el comportamiento de cada tipo de coste alternativo y adicional.
- Catalogar efectos que permiten jugar desde zonas distintas de la Mano.
- Documentar redirección, pérdida de objetivos y efectos de reemplazo.

## 4. Sistema de recursos y costes

### 4.1 Definición de coste

Un coste es un conjunto obligatorio de recursos o acciones que un jugador debe
pagar para jugar una carta o utilizar una habilidad.

Un coste puede exigir, entre otras posibilidades:

- pagar una cantidad de Oros;
- mover, descartar, destruir, desterrar, barajar o botar cartas;
- devolver cartas a la Mano;
- utilizar cartas de una zona determinada;
- cumplir varias obligaciones simultáneas.

Los costes se pagan para intentar realizar una acción. No forman parte del efecto
de la carta o habilidad y no dependen de que dicho efecto produzca un resultado.

### 4.2 Coste de Oro impreso

El coste de Oro impreso es el número de Oros requerido normalmente para jugar una
carta. Forma parte de sus características base y se conserva en todas las zonas.

Cuando una regla o habilidad hace referencia al coste de una carta sin otra
calificación, se refiere a su coste de Oro. Sin embargo, las reglas que restringen
cartas por coste pueden especificar si consideran el valor impreso o el valor
pagable modificado.

#### Implicancias para el motor

La definición de una carta debe conservar un `coste_impreso` inmutable. El coste
que se pagará debe calcularse para cada jugada y no sobrescribir ese valor.

### 4.3 Oros físicos disponibles

Un Oro físico está disponible para pagar cuando se encuentra en la Reserva de
Oro del jugador y ninguna regla impide utilizarlo.

Cada Oro físico seleccionado para un pago:

1. se reserva durante la validación;
2. aporta una unidad al pago, salvo regla expresa;
3. se mueve desde la Reserva de Oro a la Zona de Oro Pagado al confirmarse;
4. deja de estar disponible mientras permanezca en la Zona de Oro Pagado.

El hecho de que un Oro posea habilidades no modifica automáticamente la cantidad
que aporta al pago.

### 4.4 Oros virtuales

Un Oro virtual es una unidad temporal de recurso generada por una regla, habilidad
o efecto. No es una carta, no ocupa una zona y no tiene propietario ni controlador
como carta.

Cada generación de Oro virtual debe registrar:

- cantidad disponible;
- jugador que puede utilizarla;
- tipos de cartas, habilidades o costes para los que puede gastarse;
- momento inicial y duración;
- fuente que la generó;
- cualquier condición adicional.

Los Oros virtuales se consumen al pagar un coste válido y no se mueven a la Zona
de Oro Pagado. Los que permanezcan sin utilizar desaparecen en la Fase Final o en
el momento indicado por su fuente.

Que la fuente salga del juego no elimina por sí solo un recurso virtual ya
generado, salvo que la duración o el texto aplicable establezcan esa dependencia.

#### Dudas pendientes

- Catalogar las restricciones de cada generador de Oro virtual disponible en
  Racial Edición.
- Confirmar si existe alguna regla general de prioridad para elegir entre Oros
  físicos y virtuales al pagar.

### 4.5 Reducciones y aumentos del coste de Oro

#### Procedimiento

Para obtener el coste de Oro pagable de una carta, el motor debe:

1. comenzar con el coste de Oro correspondiente;
2. aplicar las reducciones válidas;
3. aplicar los aumentos que modifiquen el coste de Oro;
4. limitar el resultado mínimo a cero;
5. conservar por separado cualquier coste adicional.

Una reducción puede llevar el coste de Oro a cero, pero no genera Oros ni permite
aplicar el excedente a otro pago.

#### Dudas pendientes

- Confirmar el orden oficial cuando reducciones y aumentos múltiples producen
  resultados distintos según su orden de aplicación.
- Determinar si alguna carta de Primer Bloque establece mínimos distintos de cero.

### 4.6 Costes alternativos

Un coste alternativo permite realizar una obligación diferente en reemplazo del
coste de Oro de una carta.

#### Reglas

- El jugador debe elegir entre el coste normal y una alternativa disponible antes
  de pagar.
- Solo puede utilizar una alternativa para una misma jugada, salvo regla expresa.
- Pagar el coste alternativo no se considera pagar el coste de Oro.
- Los costes adicionales siguen siendo obligatorios.
- Un coste alternativo no hace objetivo.
- La alternativa debe poder pagarse completamente.

#### Implicancias para el motor

Cada opción de pago debe representarse explícitamente. El registro de la jugada
debe indicar cuál fue elegida para que los efectos posteriores puedan distinguir
si se pagó o no el coste de Oro.

### 4.7 Costes adicionales

Un coste adicional es una obligación que se suma al método principal de pago sin
reemplazar ni modificar por sí misma el coste de Oro.

Puede consistir en Oros adicionales, cartas u otras acciones de juego.

#### Reglas

- Debe pagarse junto con el coste normal o alternativo elegido.
- Sigue siendo obligatorio al jugar una carta sin pagar su coste de Oro.
- No hace objetivo.
- Todos los costes adicionales aplicables deben poder pagarse completamente.
- Si existen varias obligaciones, cada una debe utilizar recursos válidos que no
  hayan sido comprometidos por otra obligación incompatible.

### 4.8 Costes de habilidades

El controlador de una habilidad activada declara su utilización y paga el coste
indicado. La habilidad no puede utilizarse si el coste completo no es pagable.

Los costes de habilidades no son afectados por efectos de reemplazo. Si una
prevención o reemplazo impide ejecutar una acción exigida como coste, la habilidad
no puede utilizarse.

Pagar un coste puede mover la carta fuente fuera del Campo de Batalla. Si el pago
fue válido, la habilidad ya utilizada continúa su procedimiento aunque la fuente
esté en otra zona, salvo que una regla exija que permanezca en juego.

#### Dudas pendientes

- Clasificar las formas de redacción que separan una condición, un coste y un
  efecto en las cartas antiguas o con errata.

### 4.9 Jugar sin pagar el coste

Una autorización para jugar una carta «sin pagar su coste» elimina únicamente el
pago de su coste de Oro normal, salvo que el texto especifique algo diferente.

La carta:

- continúa siendo jugada;
- debe cumplir sus condiciones y poseer objetivos válidos;
- debe pagar sus costes adicionales;
- puede ser anulada;
- genera habilidades de carta jugada y de entrada en juego según corresponda;
- no puede ser un Oro, salvo regla expresa.

Esto se diferencia de poner una carta en juego, procedimiento que omite todos los
pasos de jugarla.

### 4.10 Validación del pago

Antes de modificar el estado, el motor debe construir un plan de pago que indique:

- método de pago elegido;
- coste de Oro calculado;
- Oros físicos seleccionados;
- Oros virtuales seleccionados y compatibilidad de sus restricciones;
- costes adicionales;
- cartas, zonas y acciones utilizadas por cada obligación;
- orden reglamentario de las operaciones, si es relevante.

El plan es válido únicamente si todas las obligaciones pueden completarse con el
estado actual. No existe pago parcial para iniciar una carta o habilidad.

### 4.11 Ejecución atómica del pago

Una vez validado el plan, el motor ejecuta el pago como una transacción:

1. reserva todos los recursos implicados;
2. vuelve a comprobar que continúan disponibles;
3. realiza los movimientos y consumos requeridos;
4. genera los eventos de pago correspondientes;
5. confirma el pago completo;
6. libera las reservas técnicas.

Si el pago no puede completarse, ninguna de sus partes debe permanecer aplicada.
Esta reversión técnica no representa una acción de juego y no debe generar
habilidades.

#### Implicancias para el motor

La atomicidad evita pagar una parte, descubrir que otra es imposible y dejar el
estado alterado. También impide utilizar una misma carta u Oro en dos costes.

### 4.12 Efectos de reemplazo y prevención sobre costes

Un coste solo puede declararse si las acciones exigidas pueden realizarse con
éxito. Si una prevención o efecto de reemplazo impide una de esas acciones, la
carta no puede jugarse o la habilidad no puede utilizarse.

Los costes de habilidades no son reemplazables. Las interacciones específicas
con costes de cartas deberán validarse contra la regla u Oráculo aplicable antes
de permitir una sustitución.

#### Dudas pendientes

- Determinar si algún coste de carta de Primer Bloque puede ser modificado por un
  efecto de reemplazo específico.
- Precisar la diferencia entre impedir un coste y reemplazar el destino de un
  recurso pagado.

### 4.13 Devolución y persistencia de costes

Una vez confirmado un pago legal:

- no se devuelve porque la carta sea anulada;
- no se devuelve porque la habilidad sea cancelada;
- no se devuelve porque el efecto se resuelva sin modificar el estado;
- no se devuelve porque sus objetivos cambien de condición durante la resolución;
- solo se devuelve si una regla o efecto lo ordena expresamente.

Los recursos movidos como coste permanecen en sus zonas de destino y pueden
generar las habilidades correspondientes a esos movimientos.

### 4.14 Información y eventos del pago

El motor debe registrar, como mínimo:

- coste base consultado;
- modificadores aplicados;
- coste pagable resultante;
- opción normal o alternativa elegida;
- costes adicionales identificados;
- recursos reservados y consumidos;
- movimientos de Oros físicos;
- consumo y expiración de Oros virtuales;
- pago confirmado o rechazado;
- causa concreta de cualquier rechazo.

La información pública debe mostrar lo necesario para verificar el pago sin
revelar cartas privadas que no deban mostrarse.

### 4.15 Invariantes del sistema

- El coste impreso de una carta nunca se sobrescribe.
- Un coste pagable nunca es menor que cero.
- Un mismo recurso no paga dos obligaciones incompatibles.
- Un Oro Pagado no está disponible como Oro de la Reserva.
- Un Oro virtual no aparece como carta en ninguna zona.
- No se inicia una carta o habilidad con un coste incompleto.
- Los costes adicionales sobreviven a un coste alternativo o gratuito.
- Una jugada anulada no devuelve automáticamente sus costes.
- Todo pago confirmado produce un registro reproducible.

### 4.16 Casos de prueba derivados

La futura suite de pruebas debe comprobar, como mínimo:

1. pago normal moviendo Oros de Reserva a Oro Pagado;
2. rechazo por cantidad insuficiente de Oros disponibles;
3. imposibilidad de utilizar un Oro ya pagado;
4. reducción de coste hasta cero sin generar excedentes;
5. aplicación de aumentos y reducciones múltiples;
6. selección y pago de un coste alternativo;
7. identificación de que no se pagó el coste de Oro al usar una alternativa;
8. conservación de costes adicionales con un coste alternativo;
9. conservación de costes adicionales al jugar sin pagar coste;
10. rechazo de un pago alternativo incompleto;
11. rechazo de una habilidad cuyo coste no puede ejecutarse;
12. continuidad de una habilidad cuya fuente salió del juego al pagar;
13. generación, restricción y consumo de Oros virtuales;
14. expiración de Oros virtuales no utilizados en la Fase Final;
15. combinación válida de Oros físicos y virtuales;
16. rechazo de un Oro virtual incompatible con el tipo de pago;
17. imposibilidad de reutilizar un recurso reservado;
18. reversión técnica completa de una transacción fallida;
19. persistencia de costes después de anular o cancelar;
20. conservación de información privada durante un pago.

### 4.17 Dudas pendientes

- Resolver el orden exacto de modificadores de coste múltiples.
- Catalogar costes alternativos y adicionales de las cartas implementadas.
- Catalogar generadores y restricciones de Oros virtuales de Racial Edición.
- Definir las interacciones excepcionales entre reemplazos, prevenciones y costes.
- Precisar qué valor de coste consultan las distintas restricciones y habilidades.

## 5. Habilidades y efectos

### 5.1 Composición de una habilidad

Una habilidad puede contener tres componentes:

- **condición:** circunstancia necesaria para utilizarla, dispararla o mantenerla;
- **coste:** recursos o acciones obligatorias que deben pagarse;
- **efecto:** instrucciones que intentan modificar o consultar el estado de juego.

No todas las habilidades contienen los tres componentes. La redacción y el
Oráculo vigente determinan cómo se clasifica cada parte.

Resolver un efecto significa ejecutar sus instrucciones sobre el estado actual,
incluso cuando ninguna consiga producir un cambio.

### 5.2 Controlador de una habilidad

Por regla general, el controlador de una habilidad es el controlador de su carta
fuente en el momento en que la habilidad se utiliza o dispara.

Cuando una habilidad se dispara porque una carta llega a una zona, se considera
disparada desde la zona de destino. Si esa zona está fuera del Campo de Batalla,
su controlador es el jugador al que pertenece la zona, según la regla aplicable.

El controlador de la habilidad:

- toma sus decisiones;
- selecciona sus objetivos cuando corresponda;
- paga sus costes;
- decide si utiliza una opción indicada por «puedes»;
- ordena sus habilidades simultáneas cuando las reglas se lo permiten.

#### Dudas pendientes

- Precisar el controlador de habilidades disparadas desde zonas que contengan
  cartas cuyo propietario sea el oponente.

### 5.3 Habilidades activadas

Una habilidad activada requiere una decisión del jugador, y puede exigir el pago
de un coste.

#### Reglas

- Solo su controlador puede declararla, salvo regla expresa.
- Se utiliza normalmente en la Fase de Vigilia de su controlador o durante una
  Guerra de Talismanes en la que pueda actuar.
- El texto puede autorizar otro momento.
- Utilizarla es opcional.
- Si posee coste, este debe pagarse completamente.
- Los costes de habilidades no son afectados por reemplazos.
- Si no indica un límite de usos, puede utilizarse nuevamente mientras sea legal
  y su coste pueda pagarse.

La palabra «puedes», un coste de activación o una cantidad de usos por turno son
indicios de una habilidad activada, pero el catálogo debe usar la clasificación
oficial y no depender únicamente de palabras aisladas.

### 5.4 Habilidades disparadas

Una habilidad disparada reacciona automáticamente a una condición o evento
específico. Suele identificarse mediante expresiones como «cuando».

#### Reglas

- La condición no depende de que el controlador elija producir el disparo.
- La habilidad se genera cuando ocurre el evento correspondiente.
- Si contiene «puedes», el disparo igualmente ocurre, pero su controlador decide
  si utiliza o aplica la opción en el momento reglamentario.
- Las habilidades que permiten anular una carta se consideran disparadas según
  la clasificación oficial aplicable.
- Una habilidad que se dispara al llegar a una zona se genera desde esa zona.

El evento debe coincidir con la condición completa. Un evento parecido pero no
equivalente no produce el disparo.

### 5.5 Habilidades continuas

Una habilidad continua modifica el estado de manera constante mientras su fuente
y sus condiciones sean válidas.

#### Reglas

- Normalmente requiere que la fuente esté en juego.
- Puede funcionar desde otra zona si el texto o la regla lo establece.
- No se activa ni dispara y no utiliza una cola de resolución.
- Se aplica o deja de aplicarse después de cada cambio de estado.
- Si una condición deja de cumplirse, su efecto cesa.
- Si posteriormente vuelve a cumplirse, comienza a aplicarse nuevamente.
- Las habilidades de palabra clave son continuas cuando así las clasifiquen las
  reglas.

Al reevaluar un estado, las continuas se aplican antes de procesar habilidades
activadas o disparadas pendientes.

#### Dudas pendientes

- Definir el orden de dependencia y antigüedad cuando varias habilidades
  continuas modifican la misma característica o se contradicen.
- Catalogar las habilidades que funcionan desde Mano, Cementerio, Castillo o
  Destierro.

### 5.6 Restricciones y contadores de uso

El texto de una habilidad puede limitar su utilización por turno, fase, carta,
evento u otra unidad temporal.

El motor debe registrar cada uso mediante una clave que identifique:

- instancia de la habilidad;
- carta o fuente correspondiente;
- controlador al momento del uso;
- periodo al que pertenece el límite;
- cantidad utilizada y cantidad máxima.

Un intento rechazado antes de declarar legalmente la habilidad no consume un uso.
Una habilidad declarada y pagada consume el uso aunque luego sea cancelada o se
resuelva sin efecto, salvo regla expresa.

#### Dudas pendientes

- Determinar si un cambio de controlador reinicia límites expresados como «una
  vez por turno».
- Determinar cómo se comportan los límites cuando una carta sale del juego y
  vuelve como una nueva instancia para efectos del juego.

### 5.7 Validación y declaración de una habilidad

Antes de declararla, el motor debe comprobar:

- que la fuente posea actualmente la habilidad;
- que se encuentre en una zona válida;
- que la fase, paso o ventana permitan utilizarla;
- que sus condiciones se cumplan;
- que no exista una prohibición aplicable;
- que existan los objetivos obligatorios válidos;
- que el coste completo pueda pagarse;
- que no se haya agotado su límite de usos.

Si es legal, el controlador declara si corresponde a una activación o disparo y
selecciona los objetivos necesarios antes de pagar los costes.

### 5.8 Pago y separación del efecto

Después de declarar la habilidad:

1. se pagan sus costes, que no hacen objetivo y no admiten respuestas durante el
   pago;
2. el efecto se separa de su fuente;
3. se considera que la habilidad fue utilizada;
4. se generan las habilidades que interactúan con la utilización o con el pago;
5. el efecto queda pendiente de intentar resolverse.

Una vez separado, el efecto no desaparece únicamente porque su fuente salga del
juego, cambie de controlador o pierda la habilidad. Puede fallar si una regla
exige información o elementos que ya no existen.

#### Implicancias para el motor

El efecto pendiente debe guardar una instantánea mínima de su origen,
controlador, objetivos, elecciones y valores fijados, sin congelar todo el estado
de la partida.

### 5.9 Ventana de prevención y cancelación

Las habilidades o cartas que cancelan una habilidad impiden que su efecto se
resuelva. Los costes ya pagados y los eventos ya generados no se revierten.

Antes de aplicar un efecto no cancelado, el oponente puede utilizar una carta o
habilidad de prevención cuando exista una ventana y se cumplan sus condiciones.

La estructura completa de respuestas, cancelaciones y prevenciones se desarrollará
en la sección de prioridad e interacciones.

### 5.10 Resolución en la medida de lo posible

Un efecto intenta ejecutar sus instrucciones en el orden escrito y en la mayor
medida posible, desde cero hasta la totalidad.

#### Reglas

- La imposibilidad de ejecutar una parte no cancela automáticamente las demás.
- Las elecciones y cantidades exactas exigidas como requisito deben poder
  satisfacerse para declarar la habilidad.
- Cada movimiento o modificación genera los cambios de estado correspondientes.
- Las continuas se reevaluan entre cambios de estado cuando las reglas lo exigen.
- Resolver sin producir cambios sigue siendo una resolución.
- Cuando el texto permite elegir «hasta N», el controlador elige una cantidad
  entre cero y N antes de ejecutar la instrucción correspondiente.

Si las instrucciones utilizan conectores como «luego», «si lo haces» o equivalentes,
la ejecución de una parte puede ser requisito de la siguiente. Estas dependencias
deben representarse explícitamente y no inferirse solo por la puntuación.

### 5.11 Duración de los efectos

La duración debe obtenerse del texto o de la regla aplicable.

#### Categorías

- **instantánea:** se aplica durante la resolución y no persiste;
- **hasta una fase o turno:** expira en el punto indicado;
- **mientras se cumpla una condición:** permanece vinculada a dicha condición;
- **hasta que la carta salga del juego:** termina al abandonar el Campo de
  Batalla;
- **permanente:** persiste mientras las reglas permitan conservar el cambio.

Cuando un efecto no indica duración, se considera permanente salvo regla
específica. Los modificadores de Fuerza sin duración indicada terminan en la
siguiente Fase Final.

Los efectos cuya duración diga «este turno», «durante el resto del turno» o
«hasta la Fase Final» concluyen en el paso correspondiente de la Fase Final.

#### Implicancias para el motor

Todo efecto persistente debe registrar condición de expiración, alcance, fuente,
objetos afectados y componentes que modifica.

### 5.12 Habilidades simultáneas

Cuando se disparan varias habilidades simultáneamente:

1. se agrupan las controladas por el jugador activo;
2. ese jugador elige el orden de resolución de las suyas;
3. se resuelven las habilidades del jugador activo en dicho orden;
4. el jugador inactivo elige el orden de las que controla;
5. se resuelven las habilidades del jugador inactivo en dicho orden.

Las habilidades nuevas que se disparen durante esta secuencia esperan hasta que
termine el grupo ya declarado y luego se procesan siguiendo la misma regla.

#### Implicancias para el motor

El motor necesita lotes de disparos simultáneos y una cola ordenable por cada
controlador. No debe intercalar libremente ambos grupos.

#### Dudas pendientes

- Confirmar si alguna aclaración vigente modifica la prioridad entre lotes
  generados durante la resolución.

### 5.13 Pérdida, copia y modificación de habilidades

Una carta puede ganar, perder, copiar o ver modificadas sus habilidades por reglas
o efectos.

El motor debe distinguir:

- texto base de la carta;
- errata u Oráculo que reemplaza ese texto;
- habilidades ganadas;
- habilidades copiadas;
- habilidades temporalmente perdidas;
- efectos ya separados de la fuente.

Perder una habilidad impide nuevos usos o disparos mientras dure la pérdida, pero
no cancela por sí mismo un efecto ya separado. Las habilidades continuas dejan de
aplicarse al perderse.

#### Dudas pendientes

- Definir el orden exacto entre perder habilidades, ganar habilidades y copiar
  texto cuando varios efectos se aplican simultáneamente.
- Definir si copiar una habilidad incluye elecciones, restricciones o
  modificadores asociados a su fuente original.

### 5.14 Concordancia de nombres

Algunas habilidades exigen que un nombre contenga una palabra destacada. La
condición se cumple cuando esa palabra aparece dentro del nombre de la carta,
independientemente del resto del nombre.

La concordancia debe realizarse sobre el nombre oficial normalizado y respetar
la palabra o expresión indicada por la habilidad. No debe resolverse mediante una
búsqueda aproximada ni por similitud semántica.

### 5.15 Eventos mínimos del subsistema

El motor debe registrar, como mínimo:

- condición disparadora detectada;
- habilidad disparada;
- habilidad activada;
- objetivos seleccionados;
- coste de habilidad pagado;
- efecto separado de su fuente;
- habilidad utilizada;
- habilidad cancelada;
- prevención aplicada;
- efecto resuelto;
- efecto resuelto sin cambio;
- habilidad continua aplicada o retirada;
- efecto persistente creado o expirado;
- límite de uso consumido;
- lote de habilidades simultáneas creado y ordenado.

### 5.16 Invariantes del subsistema

- Una habilidad activada no se utiliza sin decisión de su controlador.
- Una habilidad disparada se detecta aunque su opción sea «puedes».
- Una habilidad continua no entra en una cola de resolución.
- Los costes se pagan antes de separar el efecto.
- Un efecto separado no depende automáticamente de que su fuente permanezca.
- Una habilidad cancelada no devuelve sus costes.
- Cada efecto persistente posee una condición de expiración identificable.
- Las habilidades simultáneas respetan el orden de jugador activo e inactivo.
- Un límite de uso no se consume por un intento ilegal.

### 5.17 Casos de prueba derivados

La futura suite de pruebas debe comprobar, como mínimo:

1. activación legal durante Vigilia;
2. rechazo de una activación en una ventana incorrecta;
3. reutilización de una habilidad sin límite mientras pueda pagarse;
4. cumplimiento de límites de una o más veces por turno;
5. disparo obligatorio sin intervención del controlador;
6. disparo de una habilidad opcional seguido de su rechazo;
7. disparo desde la zona de destino de una carta destruida;
8. aplicación y cese automático de una habilidad continua;
9. reactivación de una continua cuando vuelve a cumplirse su condición;
10. selección de objetivos antes del pago;
11. imposibilidad de responder durante el pago del coste;
12. separación del efecto respecto de su fuente;
13. resolución después de que la fuente salga del juego;
14. cancelación sin devolución de costes;
15. resolución parcial en la mayor medida posible;
16. bloqueo de una instrucción posterior ligada mediante «si lo haces»;
17. expiración en Fase Final de un modificador de Fuerza sin duración;
18. persistencia de un efecto sin duración expresa que no sea modificador de
    Fuerza;
19. orden elegido por el controlador para disparos simultáneos;
20. resolución del lote activo antes del lote inactivo;
21. espera de nuevos disparos hasta terminar el lote actual;
22. pérdida de una continua y conservación de un efecto ya separado;
23. concordancia exacta de una palabra dentro del nombre oficial;
24. rechazo de una concordancia meramente aproximada.

### 5.18 Dudas pendientes

- Formalizar dependencias y conflictos entre habilidades continuas.
- Completar las reglas de cancelación, prevención y cadenas de respuesta.
- Resolver límites de uso ante cambios de controlador o reingresos al juego.
- Catalogar habilidades que funcionan desde zonas fuera del Campo de Batalla.
- Definir capas para ganar, perder, copiar y modificar habilidades.
- Confirmar el tratamiento de disparos nuevos durante lotes simultáneos.

## 6. Tipos de carta

### 6.1 Clasificación

La configuración inicial reconoce cinco tipos: Aliado, Arma, Tótem, Talismán y
Oro. Cada definición de carta posee un tipo base. Un efecto puede hacer que una
instancia gane, pierda o cambie tipos sin modificar su definición impresa.

El motor debe distinguir `tipo_base` y `tipos_actuales`, y recalcular permisos,
zonas y relaciones cuando cambien los tipos actuales.

### 6.2 Aliado

Un Aliado es una carta con Fuerza que puede atacar y bloquear. Normalmente entra
en la Línea de Defensa y permanece en juego hasta salir del Campo de Batalla.

- Puede poseer una raza.
- Debe cumplir el requisito temporal para atacar, salvo Furia u otra excepción.
- Puede portar Armas dentro de los límites aplicables.
- Su Fuerza actual se obtiene de su base y modificadores vigentes.

El motor debe registrar Fuerza, raza, habilitación para atacar, participación en
combate, Armas portadas y modificadores.

### 6.3 Arma

Un Arma entra en juego portada por un Aliado objetivo válido y permanece anexada
a él. Normalmente un Aliado porta como máximo un Arma, salvo regla expresa.

- El controlador del Arma es el controlador del portador.
- Si se juega sobre un Aliado oponente, el oponente controla el Arma.
- Si el portador sale del juego, sus Armas se destruyen y van al Cementerio de
  sus respectivos propietarios, salvo reemplazo.
- Si el portador deja de ser Aliado, el Arma es destruida.

La relación portador–Arma debe ser bidireccional, validada y eliminada de forma
atómica cuando cualquiera abandone la relación.

### 6.4 Tótem

Un Tótem entra normalmente en la Línea de Apoyo y permanece en juego. Puede
producir habilidades activadas, disparadas o continuas.

El motor debe mantener sus continuas mientras sean aplicables y retirar sus
aportaciones inmediatamente cuando pierda la habilidad o salga del juego.

### 6.5 Talismán

Un Talismán produce un efecto al resolverse y no permanece normalmente en el
Campo de Batalla. Puede jugarse en Vigilia o en otras ventanas autorizadas, como
la Guerra de Talismanes. Tras resolverse va al Cementerio de su propietario,
salvo destino distinto.

### 6.6 Oro

Un Oro es una carta de recurso. No se juega: se pone en juego en la Reserva de
Oro. Al pagar se mueve a Oro Pagado y vuelve a la Reserva al Agruparse.

Puede poseer habilidades; ser Oro no implica carecer de texto. Un Oro físico es
distinto de una unidad de Oro virtual.

### 6.7 Invariantes y pruebas

- Toda carta tiene un tipo base válido.
- Solo un Aliado válido puede portar Armas.
- Todo Arma en juego tiene portador.
- Un Talismán resuelto no queda en juego sin regla expresa.
- Un Oro normal nunca sigue el procedimiento de jugar carta.

Las pruebas deben cubrir destinos por tipo, Armas oponentes, salida del portador,
cambios de tipo, límites de Armas y separación entre Oro físico y virtual.

### 6.8 Dudas pendientes

- Catalogar excepciones de porte y cartas que cambian o combinan tipos.
- Confirmar qué propiedades impresas sobreviven a cada cambio de tipo.

## 7. Acciones fundamentales y cambios de zona

### 7.1 Movimiento de cartas

Todo movimiento debe indicar carta, origen, destino, causa, responsable y si
constituye salida o entrada al juego. Se valida antes de ejecutarse y deja a la
carta en una sola zona.

Al salir del Campo de Batalla, la carta pierde controlador y los componentes de
estado que no sobreviven; va a la zona correspondiente de su propietario. Al
volver, se considera una nueva instancia para los efectos que seguían a la
anterior, aunque conserva identidad física y propietario.

### 7.2 Robar

Robar mueve la carta superior del Castillo a la Mano de su propietario. Se hace
una carta por vez y la identidad permanece privada. El primer jugador no roba en
la Fase Final del primer turno.

### 7.3 Descartar

Descartar mueve una carta de la Mano al Cementerio de su propietario. Si un
efecto pide más cartas que las disponibles, se resuelve en la medida de lo
posible, salvo que el descarte sea coste o requisito exacto.

### 7.4 Destruir

Destruir mueve una carta del Campo de Batalla al Cementerio de su propietario y
constituye salida del juego. Una carta indestructible no puede ser destruida, pero
puede salir por otros procedimientos legales.

**Indestructible** es una habilidad que impide que una carta en juego sea
destruida por reglas, efectos o habilidades. En el caso de un Aliado, también
impide su destrucción durante la Asignación de Daño.

Un efecto que destruye cartas globalmente destruye en la medida de lo posible
todas las cartas afectadas que puedan ser destruidas. Las cartas indestructibles
permanecen en juego y no se consideran destruidas durante esa resolución. La
habilidad no impide desterrar, barajar, devolver a la Mano ni cualquier otra
salida del juego que no utilice explícitamente el procedimiento de destruir.

### 7.5 Desterrar

Desterrar mueve una carta desde una zona a la Zona de Destierro de su propietario.
Si estaba en el Campo de Batalla, sale del juego. No puede abandonar el Destierro
sin autorización expresa.

### 7.6 Barajar

Barajar una carta la mueve al Castillo de su propietario y aleatoriza el Castillo.
Intervenir un Castillo mediante búsqueda exige barajarlo después. Las cartas
barajadas desde Cementerio deben mostrarse cuando la regla lo exige para verificar
su identidad.

### 7.7 Buscar, mirar y mostrar

- Buscar examina un Castillo según criterios; no hace objetivo y puede fallarse
  voluntariamente en información privada cuando la regla lo permita.
- Mirar entrega información privada solo al jugador autorizado.
- Mostrar entrega información pública a ambos jugadores.

Una búsqueda con criterio debe revelar lo necesario para verificarlo y termina
barajando el Castillo, se encuentre o no la carta.

### 7.8 Botar y subir a la Mano

Botar cartas del Castillo representa daño o una acción equivalente y mueve las
cartas superiores, una a una, al Cementerio. Subir mueve una carta a la Mano de
su propietario; si sale del Campo de Batalla, sale del juego.

### 7.9 Motor de movimientos

Cada acción debe generar eventos `antes`, `intento`, `reemplazado`, `realizado` y
`después` cuando correspondan. Un reemplazo modifica el movimiento original; una
prevención puede impedirlo. No debe generarse simultáneamente el movimiento
original y su reemplazo.

### 7.10 Pruebas y dudas

Las pruebas cubrirán propietario correcto, privacidad, movimientos uno a uno,
salida y reingreso, Destierro restrictivo, búsquedas fallidas, barajado obligatorio
y prevención. Falta catalogar qué estado exacto se reinicia en cada movimiento y
resolver movimientos simultáneos de varias cartas.

## 8. Combate

### 8.1 Inicio

El jugador activo solo inicia Batalla Mitológica si controla al menos un Aliado
capaz de atacar. Iniciada la fase, se ejecutan Declaración de Ataque, Declaración
de Bloqueo, Guerra de Talismanes y Asignación de Daño, aunque algún paso no tenga
acciones.

### 8.2 Atacantes

Un atacante debe estar en Línea de Defensa, poder atacar y haber permanecido bajo
el control actual desde su última Agrupación, salvo Furia. Declararlo lo mueve a
Línea de Ataque y crea una relación de ataque contra el jugador defensor.

### 8.3 Bloqueadores

El defensor puede asignar un Aliado válido de su Línea de Defensa a un atacante.
La regla básica es uno a uno. No es obligatorio bloquear. Imbloqueable impide la
asignación salvo excepción expresa.

La condición de atacante o bloqueador persiste hasta terminar la Batalla o hasta
que una regla elimine la relación.

### 8.4 Guerra de Talismanes

El defensor recibe prioridad primero. Los jugadores alternan acciones y la Guerra
termina tras dos cesiones consecutivas. Cancelar el ataque devuelve atacantes a
Defensa, pero no termina por sí solo la Guerra.

### 8.5 Cálculo de daño

Para cada atacante:

- sin bloqueador válido, asigna su Fuerza al Castillo defensor;
- con bloqueador de menor Fuerza, destruye al bloqueador y la diferencia daña el
  Castillo;
- con igual Fuerza, ambos se destruyen y no hay daño al Castillo;
- con bloqueador de mayor Fuerza, el atacante se destruye y no hay daño al
  Castillo.

Antes de recibir daño se abren las prevenciones autorizadas. Por cada punto de
daño al Castillo se mueve su carta superior al Cementerio, una a una, salvo
reemplazo como daño al Destierro. Después se procesan destrucciones y disparos.

### 8.6 Cambios durante combate

Si un bloqueador sale del juego o deja la relación antes del daño, el atacante
asigna daño como no bloqueado. Ganar Imbloqueable después de ser bloqueado no
elimina el bloqueo ya declarado; perderlo después del paso de bloqueo no permite
crear un bloqueo tardío.

### 8.7 Estado, invariantes y pruebas

El motor debe guardar atacantes, bloqueadores, emparejamientos, Fuerzas efectivas,
ataque cancelado y ventanas de prevención. Ningún Aliado participa dos veces en
el mismo rol salvo excepción.

Las pruebas cubrirán cuatro comparaciones de Fuerza, Furia, Imbloqueable, salida
del bloqueador, cancelación, prevención, daño uno a uno y derrota por Castillo
vacío. Quedan pendientes bloqueos múltiples, redistribuciones y modificadores de
daño de cartas específicas.

## 9. Prioridad, respuestas, prevención y reemplazos

### 9.1 Prioridad

Prioridad es el permiso temporal para realizar una acción en una ventana. En
Guerra de Talismanes comienza el defensor y se alterna después de cada acción.
Ceder prioridad es una acción voluntaria; dos cesiones consecutivas cierran la
Guerra.

### 9.2 Respuestas y anulaciones

Una respuesta debe declarar el evento o efecto al que responde y cumplir su
ventana. Anular una carta evita su resolución o entrada; cancelar una habilidad
evita su efecto. Los costes y eventos anteriores permanecen.

Cada acción de respuesta crea un elemento identificable. El motor no debe permitir
que una carta responda retroactivamente a un elemento cuya ventana terminó.

### 9.3 Prevención

Una prevención se aplica antes del evento que evita y solo si su condición se
cumple. Evitar destrucción mantiene la carta en juego; no sale ni vuelve a entrar.
Prevenir no equivale a anular ni a reemplazar, aunque el resultado visible pueda
parecerse.

### 9.4 Reemplazo

Un efecto de reemplazo sustituye un evento antes de que ocurra. El evento original
no sucede y no dispara habilidades que dependan de él; se genera el evento
reemplazante. Los costes de habilidades no admiten reemplazo.

El motor debe detectar reemplazos aplicables, solicitar elecciones cuando haya
varios y evitar ciclos. La política exacta de elección y precedencia queda
pendiente de confirmación oficial.

### 9.5 Simultaneidad y bucles

Los disparos simultáneos se procesan por jugador activo y luego inactivo. Nuevos
disparos esperan al lote siguiente. Un bucle obligatorio sin cambio capaz de
terminarlo debe detectarse y resolverse según una política oficial aún pendiente;
el motor nunca debe quedar ejecutándolo indefinidamente.

### 9.6 Pruebas y dudas

Las pruebas cubrirán cesiones, ventanas vencidas, anulación, cancelación,
prevención, reemplazo único, reemplazos múltiples y detección de ciclos. Debe
verificarse con Juego Organizado el número exacto de acciones permitidas ante una
misma jugada y la resolución oficial de bucles infinitos.

## 10. Fin de partida

### 10.1 Derrota por Castillo vacío

Si un jugador no tiene cartas en su Mazo Castillo, pierde. La comprobación se
realiza después de cada cambio de estado pertinente, no solo cuando intenta robar.

### 10.2 Otras finalizaciones

La partida también puede terminar por concesión, decisión administrativa o causa
configurada para el entorno de juego. Desconexión y límite de tiempo pertenecen
a la aplicación o torneo, no a las reglas internas, salvo configuración expresa.

### 10.3 Procedimiento

Al detectar una condición final:

1. se detienen nuevas acciones ordinarias;
2. se completan solo comprobaciones simultáneas necesarias;
3. se determina ganador, perdedor o resultado especial;
4. se registra causa, estado y evento que la produjo;
5. la partida pasa a estado terminado e inmutable.

### 10.4 Simultaneidad, pruebas y dudas

El motor debe poder representar que ambos jugadores cumplen una condición de
derrota en el mismo cambio de estado, sin inventar un ganador. Falta confirmar la
resolución oficial de derrotas simultáneas y empates, además de reglas de match y
tiempo competitivo.

Las pruebas cubrirán Castillo vacío por daño, efecto, coste o robo; concesión;
doble condición; bloqueo de acciones posteriores y registro reproducible.

## 11. Catálogo, Oráculos, erratas y legalidad

### 11.1 Definición de carta

El catálogo almacena datos inmutables por impresión: identificador, nombre, tipo,
coste, Fuerza, raza, texto impreso, edición, código, arte y metadatos.

El texto efectivo se obtiene aplicando la errata u Oráculo vigente para la versión
de reglas seleccionada. Nunca debe sobrescribirse el texto histórico original.

### 11.2 Identidad y nombre

Copias físicas comparten definición pero tienen instancias distintas. Las reglas
de copias por nombre utilizan el nombre oficial normalizado. Dos impresiones con
el mismo nombre pueden compartir límite aunque difieran en texto o legalidad.

### 11.3 Legalidad versionada

Cada configuración debe guardar fecha de vigencia, formato, cartas permitidas,
prohibidas y límites de una, dos o tres copias, además de excepciones por versión.
Una actualización crea otra configuración y no modifica partidas guardadas.

La instantánea inicial será Racial Edición vigente al 17 de septiembre de 2026.

### 11.4 Compilación de habilidades

El texto efectivo debe transformarse en datos ejecutables: condiciones, costes,
objetivos, efectos, duración, ventanas y palabras clave. Si una carta no puede
compilarse sin interpretación humana, queda marcada como no implementada y no
puede entrar en una partida validada.

### 11.5 Procedencia y auditoría

Cada resolución debe enlazar fuente oficial, fecha y prioridad normativa. El
catálogo debe permitir explicar por qué una carta tiene cierto texto o legalidad.

### 11.6 Pruebas y pendientes

Las pruebas cubrirán nombres normalizados, reimpresiones, erratas por fecha,
banlists históricas y rechazo de cartas no compiladas. Queda construir el catálogo
real, importar la banlist de septiembre de 2026 y definir la prioridad exacta
entre DAR, FAQ, Oráculo y errata cuando entren en conflicto.

## 12. Modelo técnico Python y estrategia de pruebas

### 12.1 Principios

El motor será determinista, independiente de interfaz, serializable, auditable y
dirigido por comandos y eventos. Las reglas no deben depender de entrada gráfica,
red, reloj real ni azar global.

### 12.2 Módulos propuestos

```text
src/myl/
├── catalog/       # definiciones, Oráculos, legalidad
├── model/         # GameState, Player, CardInstance, Zone
├── commands/      # intenciones solicitadas por jugadores
├── validation/    # permisos, objetivos y costes
├── engine/        # aplicación atómica y máquina de estados
├── events/        # eventos, disparos y registro
├── effects/       # efectos compilados y duraciones
├── combat/        # Batalla Mitológica y daño
├── serialization/ # guardado, carga y reproducción
└── testing/       # constructores y escenarios de prueba
```

### 12.3 Entidades principales

- `GameConfig`: reglas, formato, catálogo y semilla.
- `GameState`: estado completo de la partida.
- `PlayerState`: zonas, recursos y estado del jugador.
- `CardDefinition`: datos compartidos e inmutables.
- `CardInstance`: identidad, propietario, zona y estado mutable.
- `Zone`: propietario, visibilidad, orden y contenido.
- `TurnState`: activo, fase, paso, prioridad y combate.
- `Command`: intención no validada.
- `Event`: hecho confirmado e inmutable.
- `PendingEffect`: efecto separado de su fuente.
- `ContinuousEffect`: regla recalculable.

El controlador y `en_juego` deben derivarse de la zona cuando sea posible.

### 12.4 Flujo de comandos

1. recibir comando con jugador y versión esperada del estado;
2. validar permisos, objetivos y costes sin mutar;
3. construir plan atómico;
4. aplicar eventos sobre una copia o transacción;
5. reevaluar continuas y detectar disparos;
6. comprobar invariantes y fin de partida;
7. confirmar nuevo estado y anexar eventos al registro.

Un comando inválido devuelve errores estructurados y no cambia el estado.

### 12.5 Determinismo y serialización

Todo azar usa una fuente incluida en `GameConfig`. Guardado y reproducción deben
preservar configuración, estado, decisiones, orden de cartas y registro, ocultando
información privada según el observador.

### 12.6 Estrategia de pruebas

- unitarias para reglas puras;
- de transición para comandos y eventos;
- de escenarios para interacciones de cartas;
- de propiedades para invariantes y movimientos aleatorios;
- de regresión para cada fallo corregido;
- de reproducción para verificar determinismo;
- de privacidad para vistas de cada jugador.

Cada regla numerada debe enlazar al menos un caso de prueba. Cada carta compilada
debe probar sus rutas principales, restricciones y Oráculo.

### 12.7 Criterio de inicio de implementación

Puede comenzar el núcleo cuando existan: modelos de zonas y cartas, máquina de
turnos, comandos de movimiento, pagos atómicos, registro de eventos y pruebas de
invariantes. Las cartas se incorporarán incrementalmente; ninguna interacción no
documentada debe resolverse mediante lógica especial silenciosa.

### 12.8 Pendientes antes del primer prototipo completo

- resolver solo las dudas clasificadas como bloqueantes en la sección 13;
- crear el catálogo mínimo y la instantánea de legalidad descritos en 13.5;
- seleccionar el conjunto inicial de cartas con la matriz de 13.7;
- definir la interfaz mínima de comandos del motor;
- convertir los escenarios del alcance mínimo en pruebas automatizadas.

## 13. Preparación del primer prototipo

### 13.1 Alcance mínimo adoptado

El primer prototipo será una partida local para dos jugadores, sin red ni interfaz
gráfica, con mazos de prueba preconstruidos para Racial Edición. Debe validar la
preparación, las zonas, el turno, el pago con Oro físico, el juego de cartas, un
combate básico, la destrucción, el daño al Castillo y una condición de derrota.

No es necesario que el primer prototipo interprete todas las cartas ni que permita
construir cualquier mazo legal. Una carta cuyo texto requiera una regla todavía no
resuelta se marca como `no_implementada` y se excluye de los mazos de prueba.

### 13.2 Criterio de clasificación de dudas

Las dudas se clasifican así:

- **Bloqueante:** impide construir o verificar una parte incluida en el alcance
  mínimo. Debe resolverse, evitarse explícitamente o recibir una regla provisional
  documentada antes de ejecutar partidas válidas.
- **Posterior:** corresponde a cartas, formatos o interacciones que pueden quedar
  fuera del conjunto inicial sin dañar el núcleo del prototipo.
- **Aplicación:** no requiere una interpretación oficial; es una decisión de diseño,
  datos o arquitectura que debe tomar el proyecto durante la implementación.

La clasificación depende del alcance. Una duda posterior pasa a ser bloqueante en
el momento en que se incorpore una carta que utilice esa interacción.

### 13.3 Dudas bloqueantes

| Código | Duda consolidada | Resolución necesaria para comenzar |
|---|---|---|
| B-01 | Texto efectivo y características de cada carta seleccionada | Registrar fuente, impresión, texto y cualquier errata antes de implementarla. |
| B-02 | Oros Iniciales permitidos en Racial Edición | Confirmar la condición oficial o usar mazos de prueba ya validados externamente. |
| B-03 | Vigencia del mulligan gratuito de 2026 | Mantener provisionalmente el mulligan tradicional ya documentado y marcar la configuración. |
| B-04 | Fin de la oportunidad normal de poner Oro | Para el prototipo, cerrarla con la primera acción voluntaria distinta de poner Oro; revisar antes de implementar disparos en esa ventana. |
| B-05 | Condiciones básicas para atacar y bloquear | Cerrar las reglas para los Aliados simples seleccionados y excluir excepciones. |
| B-06 | Destino y reinicio de estado al cambiar de zona | Definir el reinicio mínimo de modificadores, ataque, bloqueo y orientación para los casos implementados. |
| B-07 | Legalidad contradictoria de `Antorcha Olímpica` | La fuente de septiembre de 2026 la muestra prohibida y limitada a una copia. Excluirla hasta obtener aclaración oficial; nunca elegirla para el catálogo mínimo. |
| B-08 | Derrota por Castillo vacío y resultados simultáneos | Implementar primero la derrota individual; un resultado simultáneo debe quedar como `empate_no_resuelto`, nunca asignar un ganador arbitrario. |
| B-09 | Prioridad entre texto impreso, errata, Oráculo, FAQ y DAR | Para cada carta inicial debe existir una única fuente efectiva registrada; cualquier conflicto deja la carta no implementada. |

Estas dudas no obligan a detener todo el desarrollo. Las reglas provisionales de la
última columna permiten iniciar el núcleo, pero deben quedar visibles en la versión
de reglas y en los resultados de las pruebas.

### 13.4 Dudas posteriores y decisiones de aplicación

#### Posteriores

Pueden esperar mientras las cartas que dependan de ellas permanezcan excluidas:

- formatos posteriores a Racial Edición y zonas compartidas o temporales;
- cambio de propietario, cambios sucesivos o temporales de controlador y sus
  interacciones con límites de uso;
- relevancia y modificación del orden de Cementerio o Destierro;
- pagos parciales o simultáneos, Oros virtuales, costes alternativos o adicionales,
  mínimos de coste y múltiples aumentos o reducciones;
- cadenas completas, respuestas, prevención, reemplazos, anulaciones desde zonas
  restringidas y cartas jugadas desde fuera de la Mano;
- pérdida o redirección de objetivos;
- habilidades desde zonas fuera del Campo de Batalla;
- dependencias entre continuas, orden entre ganar, perder o copiar habilidades,
  y disparos nuevos durante lotes simultáneos;
- excepciones de porte, cambios de tipo y combinación de tipos;
- todas las excepciones de destino y redacciones antiguas que no aparezcan en el
  conjunto inicial.

#### Aplicación

Estas decisiones pertenecen al proyecto y pueden cerrarse al programar:

- componentes almacenados y calculados de `PlayerState` y `CardInstance`;
- representación de estados temporales y estados mutuamente excluyentes;
- expresión técnica `fuera_del_campo_de_batalla` frente al texto de cartas;
- modo de prueba que omita validación de construcción;
- protocolo de decisiones simultáneas en una interfaz futura;
- biblioteca de validación, serialización y API pública;
- identificadores estables, normalización de nombres y modelo de reimpresiones;
- proceso de importación, revisión y actualización del catálogo;
- conversión de escenarios documentados en pruebas automatizadas.

### 13.5 Catálogo mínimo y fuentes

El catálogo mínimo tendrá entre 24 y 36 definiciones de carta, suficientes para dos
mazos de prueba. Se mantendrán tres niveles separados:

1. `CardIdentity`: nombre normalizado al que se aplican límites y banlist;
2. `CardPrinting`: edición, producto, código, imagen y texto impreso de una copia;
3. `CardDefinition`: texto efectivo compilado que el motor puede ejecutar.

Los datos mínimos por impresión son:

| Campo | Uso |
|---|---|
| `card_id` | Identificador estable de la identidad por nombre. |
| `printing_id` | Identificador estable de la impresión. |
| `name` y `normalized_name` | Presentación y comparación de límites. |
| `type`, `cost`, `strength`, `race` | Reglas y filtros; los campos no aplicables usan `null`. |
| `edition`, `product`, `collector_number` | Procedencia de la impresión. |
| `printed_text`, `effective_text` | Texto histórico y texto que usa el motor. |
| `initial_gold_eligible` | Elegibilidad como Oro Inicial, con fuente. |
| `implementation_status` | `verified`, `pending_rules` o `not_implemented`. |
| `source_url`, `source_checked_at` | Auditoría del dato. |

La banlist se guarda aparte y se aplica a `normalized_name`, no a una imagen o
impresión concreta. Cada instantánea contiene `format_id`, fecha de vigencia,
fuente, asociaciones entre edición y productos, relación entre edición y raza,
mínimo de Aliados y límites por
nombre. Una partida conserva el identificador exacto de la instantánea usada.

Fuentes iniciales:

- banlist oficial de Mitos y Leyendas, actualización de septiembre de 2026:
  <https://blog.myl.cl/banlist-racial-edicion-primer-bloque/>;
- catálogo público de impresiones y filtros: <https://mazos.cl/cards>.

Mazos.cl debe tratarse como fuente secundaria de catálogo. Antes de automatizar
una extracción masiva hay que revisar sus condiciones de uso y preferir una API,
exportación o autorización proporcionada por el sitio. Para el prototipo se hará
una carga manual pequeña, registrando la URL de cada ficha y contrastando el texto
con una fuente oficial cuando exista. Las imágenes no se redistribuyen sin permiso.

### 13.6 Flujo de incorporación de cartas

1. Elegir una edición, una raza perteneciente a ella y los productos de soporte
   permitidos para esa edición.
2. Reunir candidatos en Mazos.cl usando los filtros de edición, producto y tipo.
3. Crear una fila por impresión y asociarla a una identidad normalizada.
4. Contrastar nombre, tipo, coste, Fuerza, raza y texto; registrar discrepancias.
5. Aplicar la instantánea de banlist por nombre normalizado.
6. Rechazar cartas prohibidas, conflictos de legalidad y textos no verificables.
7. Etiquetar las mecánicas requeridas por cada carta.
8. Elegir solo cartas cuyas mecánicas estén implementadas o sean el objetivo de una
   prueba concreta.
9. Compilar su comportamiento y crear al menos una prueba positiva y una negativa.
10. Validar ambos mazos y congelarlos como accesorios reproducibles del prototipo.

No deben inferirse campos ilegibles desde una imagen ni completarse textos por
memoria. Un valor desconocido se conserva como `null` y bloquea únicamente la
carta afectada.

### 13.7 Selección de cartas representativas

La primera selección debe cubrir reglas, no popularidad. Para el prototipo se ha
elegido **Helénica** como edición, **Olímpico** como raza y dos mazos espejo. Cada
candidato recibe una marca en esta matriz:

| Grupo | Cantidad orientativa | Qué debe probar |
|---|---:|---|
| Oro Inicial | 1 por mazo | Preparación y producción básica. |
| Oros sin habilidad compleja | 8-12 identidades/copias | Poner Oro, pagar y pasar entre Reserva y Oro Pagado. |
| Aliados simples de costes distintos | 8-12 identidades | Jugar, orientar, atacar, bloquear, destruir y hacer daño. |
| Talismán de efecto inmediato simple | 2-3 identidades | Objetivo, resolución y envío al Cementerio. |
| Arma de bonificación simple | 1-2 identidades | Porte, modificación de Fuerza y salida del portador. |
| Tótem continuo simple | 1-2 identidades | Efecto persistente y recálculo. |
| Carta con habilidad disparada simple | 1-2 identidades | Creación y resolución de un disparo sin cadena compleja. |

En la primera ronda deben excluirse cartas prohibidas o con conflicto, cambio de
control, juego desde Cementerio o Destierro, Oro virtual, costes alternativos,
prevención, reemplazo, copia de texto, cambio de tipo, múltiples objetivos o texto
que dependa de una aclaración pendiente.

La selección queda completa cuando cada regla del alcance mínimo tiene al menos
una carta que la ejercita, ninguna carta introduce una mecánica no documentada y
ambos mazos pueden jugar una partida determinista de principio a fin.

### 13.8 Trabajo manual requerido

Ya se encuentran completas las decisiones iniciales:

- edición: Helénica;
- raza: Olímpico;
- construcción de prueba: dos mazos espejo.

El responsable del proyecto solo debe:

1. facilitar una aclaración oficial de `Antorcha Olímpica` si se desea incorporarla;
2. confirmar las condiciones de uso o autorización de Mazos.cl antes de realizar
   una importación automatizada o redistribuir sus datos e imágenes.

El resto del catálogo mínimo puede construirse de forma incremental sin completar
primero todas las dudas posteriores.
