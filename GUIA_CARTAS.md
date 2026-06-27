# Guia rapida para agregar cartas

Las cartas viven en `card.json`. Cada entrada necesita un `id` unico, `name`,
`type`, `cost` y `text`. Los aliados tambien necesitan `strength`.

Tipos soportados:

- `Oro`
- `Aliado`
- `Arma`
- `Totem`
- `Talisman`

Ejemplo de aliado:

```json
{
  "id": "ally_nuevo_001",
  "name": "Guerrero Nuevo",
  "type": "Aliado",
  "cost": 2,
  "strength": 2,
  "text": "Cuando entra en juego, el oponente bota 1 carta.",
  "abilities": [
    {
      "type": "triggered",
      "trigger": "on_enter_play",
      "effect": "mill",
      "target": "opponent",
      "amount": 1
    }
  ]
}
```

Ejemplo de talisman:

```json
{
  "id": "talisman_nuevo_001",
  "name": "Rayo del Alba",
  "type": "Talisman",
  "cost": 2,
  "text": "El oponente bota 2 cartas.",
  "abilities": [
    {
      "type": "activated",
      "effect": "mill",
      "target": "opponent",
      "amount": 2
    }
  ]
}
```

Efectos disponibles:

- `mill`: bota cartas desde el Castillo al Cementerio.
- `draw`: roba cartas desde el Castillo a la Mano.
- `discard`: descarta cartas desde la Mano al Cementerio.

Targets disponibles:

- `self`: el controlador de la carta.
- `opponent`: el rival.

Para agregar una carta al mazo, edita `deck_player1.json` o
`deck_player2.json` y agrega su `id`:

```json
{
  "card_id": "ally_nuevo_001",
  "count": 3
}
```

Despues guarda los archivos y ejecuta:

```powershell
python main.py
```
