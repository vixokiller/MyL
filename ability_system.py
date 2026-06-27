from ability_effects import discard_cards, draw_cards, mill_cards


class AbilitySystem:
    def __init__(self, game):
        self.game = game
        self.effects = {
            "discard": discard_cards,
            "draw": draw_cards,
            "mill": mill_cards,
        }

    def resolve(self, card, event, controller=None):
        controller = controller or card.controller
        if controller is None:
            return

        for ability in card.abilities:
            ability_type = ability.get("type")
            trigger = ability.get("trigger")

            if event == "on_enter_play":
                if ability_type != "triggered" or trigger != event:
                    continue
            elif event == "on_play":
                if ability_type not in ("activated", "triggered"):
                    continue
                if trigger and trigger != event:
                    continue
            else:
                continue

            self._apply_ability(card, ability, controller)

    def _apply_ability(self, card, ability, controller):
        effect_name = ability.get("effect")
        effect = self.effects.get(effect_name)
        if effect is None:
            print(f"{card.name} tiene un efecto desconocido: {effect_name}.")
            return

        target = self._resolve_target(ability.get("target", "self"), controller)
        amount = int(ability.get("amount", 1))

        print(f"Resolviendo efecto de {card.name}: {effect_name} {amount}.")
        effect(self.game, target, amount)

    def _resolve_target(self, target, controller):
        if target in ("opponent", "oponente"):
            return self.game.get_opponent(controller)
        return controller
