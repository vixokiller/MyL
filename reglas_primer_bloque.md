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

- Confirmar el formato competitivo exacto que se implementará primero: Racial
  Edición, Racial Libre u otro formato oficial de Primer Bloque.

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
