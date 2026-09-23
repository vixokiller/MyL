# Etapa 5 — Cliente de consola y cartas posteriores

## Objetivo

Convertir el motor probado en una aplicación local que dos personas puedan usar
desde una terminal y ampliar el catálogo sin volver a concentrar reglas de cartas
en `Partida`.

## Incremento 5.1 — Partida local por consola

Estado: implementado.

El punto de entrada es `main.py` y la interfaz vive en `src/myl/consola.py`. Al
iniciar, carga dos copias del mazo espejo, ejecuta la preparación coordinada,
solicita los mulligans de cada jugador y comienza el primer turno.

La consola permite:

- consultar estado público, Mano y mesa;
- poner el Oro de turno;
- jugar Aliados, Tótems y Talismanes que no requieran una elección adicional;
- activar habilidades sin objetivos;
- declarar múltiples atacantes;
- asignar bloqueadores;
- resolver todos los combates y avanzar fases.

Se ejecuta con:

```bash
python main.py --jugador-1 Alicia --jugador-2 Bruno
```

`--semilla 7` permite reproducir los barajados durante pruebas o depuración.

### Límites actuales de la consola

El motor acepta objetivos y elecciones, pero el cliente todavía no pregunta por
todos ellos. Por eso Astreo, Atenea, Comus, Almas de Estigia, Hilo de Ariadna,
Trono Dorado, Titanes, Thanatos y otras cartas complejas deben probarse mediante
la API hasta añadir menús contextuales. Tampoco hay ocultamiento físico entre
dos personas que comparten terminal; se confía en que cada una solo consulte su
Mano durante su turno.

## Incremento 5.2 — Primer bloque posterior

Estado: implementado y probado.

- **Ares:** paga dos Oros en Guerra de Talismanes y cancela el ataque o un
  bloqueo; conserva el límite de una vez por turno.
- **Helios:** aporta dos de Fuerza a los Aliados Olímpicos de su controlador.
- **Focea:** devuelve una carta oponente no Oro al Castillo al entrar; en Guerra
  puede destruirse para robar dos y descartar una.
- **Lyssa:** se destruye en Guerra para devolver un atacante oponente a Defensa.
- **Fénix:** puede jugarse desde el Cementerio pagando su coste durante Vigilia.
- **Thanatos:** una vez por turno destruye todos los Aliados con el nombre
  elegido, respetando Indestructible.
- **Titanes:** se destierra para fijar en cero la Fuerza de un Aliado oponente de
  Fuerza tres o más hasta la Fase Final.

## Incremento 5.3 — Pendiente

1. Menús contextuales de objetivos, costes opcionales y respuestas.
2. Oros virtuales para Arcas del Imperio.
3. Pérdida temporal de habilidades para Figuras Negras y Águila Imperial.
4. Cambio temporal de tipo para Ave de Hera.
5. Cambio de control y obligación de atacar para El Oscuro Hades.
6. Juego gratuito y desde zonas distintas para Zagreus, Afrodita y Dionisio
   Zagreo.
7. Prevención reactiva completa para Hera.
8. Guardado/carga de partidas y una IA básica opcional.

## Datos o aclaraciones que mejorarían la fidelidad

El catálogo contiene texto suficiente para prototipar, pero las siguientes
interacciones necesitan una FAQ, Oráculo o fallo oficial para evitar asumir:

- si Ares puede cancelar cualquier ataque completo o una declaración individual;
- cómo se define exactamente «afectado por una habilidad oponente» para Hera;
- qué componentes conserva Ave de Hera al convertirse temporalmente en Aliado;
- qué sucede si El Oscuro Hades gana control cuando ya terminó la declaración de
  atacantes;
- si Águila Imperial considera Fuerza impresa o Fuerza actual.

Para aportar esos datos, abre `catalog/catalogo_cartas_helenica_olimpico.xlsx` y,
en la fila de la carta, agrega el texto oficial o de Oráculo en `Texto efectivo`,
la URL en `URL fuente` y una explicación breve en `Notas`. Si la fuente no es
oficial, marca la verificación como `Parcial`. También puedes pegar directamente
en una conversación una fotografía legible o el enlace a la resolución.
