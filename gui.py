import contextlib
import io
from pathlib import Path
import tkinter as tk
from tkinter import ttk

from main import Ally, PHASE_NAMES, build_game, format_card


CARD_WIDTH = 132
CARD_HEIGHT = 184
CARD_GAP = 10
HAND_HEIGHT = 270


ZONE_TARGETS = {
    0: "gold",
    1: "defense",
    2: "support",
    3: "support",
    4: "defense",
}


ZONE_LABELS = {
    "deck": "Castillo",
    "gold": "Reserva de oros",
    "paid_gold": "Oros pagados",
    "defense": "Linea de defensa",
    "attack": "Linea de ataque",
    "support": "Linea de apoyo",
    "graveyard": "Cementerio",
    "exile": "Destierro",
}


CARD_COLORS = {
    0: ("#f4d35e", "#5d4800"),
    1: ("#8ecae6", "#12384a"),
    2: ("#adb5bd", "#212529"),
    3: ("#b7e4c7", "#1b4332"),
    4: ("#cdb4db", "#3c1642"),
}


class GameGui:
    def __init__(self, root):
        self.root = root
        self.root.title("MyL TCG")
        self.root.geometry("1920x1080")
        self.root.minsize(1366, 768)

        output = io.StringIO()
        with contextlib.redirect_stdout(output):
            self.game = build_game()
        self.initial_log = output.getvalue().strip()
        self.drag = None
        self.card_widgets = {}
        self.zone_frames = {}
        self.zone_data = {}
        self.manual_image = None

        self._build_layout()
        self._new_turn_started = True
        self.refresh()

    def _build_layout(self):
        self.root.configure(bg="#22312b")
        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_rowconfigure(0, weight=0)
        self.root.grid_rowconfigure(1, weight=1)
        self.root.grid_rowconfigure(2, weight=0)

        self.header = ttk.Frame(self.root, padding=(12, 8))
        self.header.grid(row=0, column=0, sticky="ew")

        self.turn_label = ttk.Label(self.header, font=("Segoe UI", 13, "bold"))
        self.turn_label.pack(side=tk.LEFT)

        self.end_turn_button = ttk.Button(
            self.header,
            text="Terminar turno",
            command=self.end_turn,
        )
        self.end_turn_button.pack(side=tk.RIGHT)

        self.reference_button = ttk.Button(
            self.header,
            text="Campo oficial",
            command=self.show_field_reference,
        )
        self.reference_button.pack(side=tk.RIGHT, padx=(0, 8))

        self.content = tk.Frame(self.root, bg="#22312b")
        self.content.grid(row=1, column=0, sticky="nsew", padx=12, pady=8)

        self.opponent_area = self._make_player_area(self.content, "Rival", top=True)
        self.opponent_area.pack(side=tk.TOP, fill=tk.X)

        self.board_area = tk.Frame(self.content, bg="#22312b")
        self.board_area.pack(side=tk.TOP, fill=tk.BOTH, expand=True, pady=8)

        self.log_box = tk.Text(
            self.board_area,
            height=9,
            width=34,
            bg="#111a17",
            fg="#d7f2e6",
            insertbackground="#d7f2e6",
            relief=tk.FLAT,
            wrap=tk.WORD,
            font=("Consolas", 9),
        )
        self.log_box.pack(side=tk.RIGHT, fill=tk.Y, padx=(10, 0))
        self.log("Arrastra cartas desde tu mano a su zona correcta.")
        if self.initial_log:
            self.log(self.initial_log)

        self.player_area = self._make_player_area(self.board_area, "Jugador", top=False)
        self.player_area.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.hand_container = tk.Frame(self.root, bg="#18231f", height=HAND_HEIGHT)
        self.hand_container.grid(row=2, column=0, sticky="ew", padx=12, pady=(0, 12))
        self.hand_container.pack_propagate(False)
        self.hand_container.grid_propagate(False)

        hand_title = tk.Label(
            self.hand_container,
            text="Mano",
            bg="#18231f",
            fg="#f2f7f4",
            font=("Segoe UI", 11, "bold"),
        )
        hand_title.pack(anchor="w", padx=10, pady=(8, 0))

        self.hand_canvas = tk.Canvas(
            self.hand_container,
            bg="#18231f",
            highlightthickness=0,
            height=210,
        )
        self.hand_scrollbar = ttk.Scrollbar(
            self.hand_container,
            orient=tk.HORIZONTAL,
            command=self.hand_canvas.xview,
        )
        self.hand_canvas.configure(xscrollcommand=self.hand_scrollbar.set)
        self.hand_scrollbar.pack(side=tk.BOTTOM, fill=tk.X, padx=10, pady=(0, 6))
        self.hand_canvas.pack(side=tk.TOP, fill=tk.BOTH, expand=True, padx=10, pady=6)

        self.hand_frame = tk.Frame(self.hand_canvas, bg="#18231f")
        self.hand_canvas.create_window((0, 0), window=self.hand_frame, anchor="nw")
        self.hand_frame.bind(
            "<Configure>",
            lambda event: self.hand_canvas.configure(scrollregion=self.hand_canvas.bbox("all")),
        )
        self.hand_canvas.bind("<Shift-MouseWheel>", self.scroll_hand)
        self.hand_canvas.bind("<MouseWheel>", self.scroll_hand)

    def _make_player_area(self, parent, title, top):
        wrapper = tk.Frame(parent, bg="#22312b")
        if top:
            wrapper.configure(height=265)
            wrapper.pack_propagate(False)

        name = tk.Label(
            wrapper,
            text=title,
            bg="#22312b",
            fg="#f2f7f4",
            font=("Segoe UI", 12, "bold"),
        )
        name.pack(anchor="w")

        stats = tk.Label(
            wrapper,
            text="",
            bg="#22312b",
            fg="#d7e4dc",
            font=("Segoe UI", 9),
        )
        stats.pack(anchor="w", pady=(0, 6))

        zones = tk.Frame(wrapper, bg="#22312b")
        zones.pack(fill=tk.BOTH, expand=True)
        zones.grid_columnconfigure(0, weight=0, minsize=300)
        zones.grid_columnconfigure(1, weight=1)
        for row in range(3):
            zones.grid_rowconfigure(row, weight=1, uniform="field_rows")

        prefix = "opponent" if top else "player"

        paid_gold = self._make_zone(zones, ZONE_LABELS["paid_gold"], compact_box=True)
        paid_gold.grid(row=0, column=0, sticky="nsew", padx=(0, 8), pady=4)
        self._register_zone(prefix, "paid_gold", paid_gold)

        middle_stack = tk.Frame(zones, bg="#22312b")
        middle_stack.grid(row=1, column=0, sticky="nsew", padx=(0, 8), pady=4)
        middle_stack.grid_columnconfigure(0, weight=1, uniform="left_middle")
        middle_stack.grid_columnconfigure(1, weight=1, uniform="left_middle")
        middle_stack.grid_rowconfigure(0, weight=1)

        graveyard = self._make_zone(middle_stack, ZONE_LABELS["graveyard"], compact_box=True)
        graveyard.grid(row=0, column=0, sticky="nsew", padx=(0, 4))
        self._register_zone(prefix, "graveyard", graveyard)

        deck = self._make_zone(middle_stack, ZONE_LABELS["deck"], compact_box=True)
        deck.grid(row=0, column=1, sticky="nsew", padx=(4, 0))
        self._register_zone(prefix, "deck", deck)

        bottom_stack = tk.Frame(zones, bg="#22312b")
        bottom_stack.grid(row=2, column=0, sticky="nsew", padx=(0, 8), pady=4)
        bottom_stack.grid_columnconfigure(0, weight=1, uniform="left_bottom")
        bottom_stack.grid_columnconfigure(1, weight=1, uniform="left_bottom")
        bottom_stack.grid_rowconfigure(0, weight=1)

        exile = self._make_zone(bottom_stack, ZONE_LABELS["exile"], compact_box=True)
        exile.grid(row=0, column=0, sticky="nsew", padx=(0, 4))
        self._register_zone(prefix, "exile", exile)

        gold = self._make_zone(bottom_stack, ZONE_LABELS["gold"], compact_box=True)
        gold.grid(row=0, column=1, sticky="nsew", padx=(4, 0))
        self._register_zone(prefix, "gold", gold)

        attack = self._make_zone(zones, ZONE_LABELS["attack"], large=True)
        attack.grid(row=0, column=1, sticky="nsew", pady=4)
        self._register_zone(prefix, "attack", attack)

        defense = self._make_zone(zones, ZONE_LABELS["defense"], large=True)
        defense.grid(row=1, column=1, sticky="nsew", pady=4)
        self._register_zone(prefix, "defense", defense)

        support = self._make_zone(zones, ZONE_LABELS["support"], large=True)
        support.grid(row=2, column=1, sticky="nsew", pady=4)
        self._register_zone(prefix, "support", support)

        wrapper.stats_label = stats
        return wrapper

    def _register_zone(self, prefix, zone_key, frame):
        zone_id = f"{prefix}_{zone_key}"
        self.zone_frames[zone_id] = frame
        frame.zone_id = zone_id
        self._bind_zone_click(frame)

    def _make_zone(self, parent, title, large=False, compact_box=False):
        frame = tk.Frame(
            parent,
            bg="#31463d",
            highlightthickness=2,
            highlightbackground="#678174",
            width=560 if large else 148,
            height=170 if large else 120,
        )
        frame.pack_propagate(False)
        frame.grid_propagate(False)

        label = tk.Label(
            frame,
            text=title,
            bg="#31463d",
            fg="#ecf5ef",
            font=("Segoe UI", 9, "bold"),
        )
        label.pack(anchor="w", padx=8, pady=(6, 2))

        cards = tk.Frame(frame, bg="#31463d")
        cards.pack(fill=tk.BOTH, expand=True, padx=8 if large else 5, pady=(0, 6))
        frame.cards_area = cards
        frame.large_zone = large
        frame.compact_box = compact_box
        return frame

    def _bind_zone_click(self, frame):
        widgets = [frame, frame.cards_area]
        widgets.extend(frame.winfo_children())
        for widget in widgets:
            widget.bind("<Button-1>", lambda event, zone_id=frame.zone_id: self.show_zone_cards(zone_id))

    def refresh(self):
        player = self.game.active_player
        opponent = self.game.defender_player

        self.turn_label.config(
            text=(
                f"Turno {self.game.actual_turn} - {PHASE_NAMES.get(self.game.actual_phase)} "
                f"- juega {player.name}"
            )
        )
        if self.game.game_over:
            self.turn_label.config(
                text=f"Partida terminada - gana {self.game.winner.name}"
            )
            self.end_turn_button.configure(state=tk.DISABLED)
        else:
            self.end_turn_button.configure(state=tk.NORMAL)
        self.player_area.stats_label.config(
            text=(
                f"Mazo {len(player.deck.cards)} | Mano {len(player.hand.cards)} | "
                f"Cementerio {len(player.graveyard.cards)}"
            )
        )
        self.opponent_area.stats_label.config(
            text=(
                f"Mazo {len(opponent.deck.cards)} | Mano {len(opponent.hand.cards)} | "
                f"Cementerio {len(opponent.graveyard.cards)}"
            )
        )

        for frame in self.zone_frames.values():
            for child in frame.cards_area.winfo_children():
                child.destroy()

        for child in self.hand_frame.winfo_children():
            child.destroy()

        self.card_widgets = {}
        self.zone_data = {
            "player_deck": player.deck.cards,
            "player_graveyard": player.graveyard.cards,
            "player_exile": player.exile.cards,
            "player_gold": player.gold_reserve.cards,
            "player_paid_gold": player.paid_gold_zone.cards,
            "player_support": player.support_line.cards,
            "player_defense": player.defense_line.cards,
            "player_attack": player.attack_line.cards,
            "opponent_deck": opponent.deck.cards,
            "opponent_graveyard": opponent.graveyard.cards,
            "opponent_exile": opponent.exile.cards,
            "opponent_gold": opponent.gold_reserve.cards,
            "opponent_paid_gold": opponent.paid_gold_zone.cards,
            "opponent_support": opponent.support_line.cards,
            "opponent_defense": opponent.defense_line.cards,
            "opponent_attack": opponent.attack_line.cards,
        }

        self._draw_zone("player_deck", player.deck.cards, compact=True, hidden=True)
        self._draw_zone("player_graveyard", player.graveyard.cards)
        self._draw_zone("player_exile", player.exile.cards)
        self._draw_zone("player_gold", player.gold_reserve.cards)
        self._draw_zone("player_paid_gold", player.paid_gold_zone.cards)
        self._draw_zone("player_support", player.support_line.cards)
        self._draw_zone("player_defense", player.defense_line.cards)
        self._draw_zone("player_attack", player.attack_line.cards)

        self._draw_zone("opponent_deck", opponent.deck.cards, compact=True, hidden=True)
        self._draw_zone("opponent_paid_gold", opponent.paid_gold_zone.cards, compact=True)
        self._draw_zone("opponent_gold", opponent.gold_reserve.cards, compact=True)
        self._draw_zone("opponent_graveyard", opponent.graveyard.cards, compact=True)
        self._draw_zone("opponent_exile", opponent.exile.cards, compact=True)
        self._draw_zone("opponent_support", opponent.support_line.cards, compact=True)
        self._draw_zone("opponent_defense", opponent.defense_line.cards, compact=True)
        self._draw_zone("opponent_attack", opponent.attack_line.cards, compact=True)

        self._draw_hand(player.hand.cards)
        self.hand_canvas.configure(scrollregion=self.hand_canvas.bbox("all"))

    def _draw_zone(self, zone_id, cards, compact=False, hidden=False):
        frame = self.zone_frames[zone_id].cards_area
        if not cards:
            placeholder = tk.Label(
                frame,
                text="-",
                bg="#31463d",
                fg="#9fb6aa",
                font=("Segoe UI", 16),
            )
            placeholder.pack(expand=True)
            return

        visible_limit = 7 if getattr(self.zone_frames[zone_id], "large_zone", False) else 1
        visible_cards = cards[-visible_limit:]
        for card in visible_cards:
            widget = self._create_card_widget(frame, card, compact=compact, hidden=hidden)
            widget.pack(side=tk.LEFT, padx=3, pady=3)
        if len(cards) > len(visible_cards):
            count = tk.Label(
                frame,
                text=f"+{len(cards) - len(visible_cards)}",
                bg="#31463d",
                fg="#ecf5ef",
                font=("Segoe UI", 10, "bold"),
            )
            count.pack(side=tk.LEFT, padx=4)

    def _draw_hand(self, cards):
        if not cards:
            empty = tk.Label(
                self.hand_frame,
                text="Sin cartas en mano",
                bg="#18231f",
                fg="#b8c8bf",
                font=("Segoe UI", 11),
            )
            empty.pack(side=tk.LEFT, padx=12, pady=70)
            return

        for card in cards:
            widget = self._create_card_widget(self.hand_frame, card)
            widget.pack(side=tk.LEFT, padx=(0, CARD_GAP), pady=2)
            self.card_widgets[widget] = card
            self._bind_drag(widget, card)

    def scroll_hand(self, event):
        direction = -1 if event.delta > 0 else 1
        self.hand_canvas.xview_scroll(direction * 3, "units")

    def _create_card_widget(self, parent, card, compact=False, hidden=False):
        bg, fg = CARD_COLORS.get(card.type, ("#f8f9fa", "#212529"))
        width = 15 if compact else 17
        height = 5 if compact else 9

        frame = tk.Frame(
            parent,
            bg=bg,
            width=CARD_WIDTH if not compact else 86,
            height=CARD_HEIGHT if not compact else 100,
            relief=tk.RAISED,
            borderwidth=2,
        )
        frame.pack_propagate(False)

        title = "Carta" if hidden else card.name
        name = tk.Label(
            frame,
            text=title,
            bg=bg,
            fg=fg,
            font=("Segoe UI", 10 if not compact else 8, "bold"),
            wraplength=110 if not compact else 78,
        )
        name.pack(anchor="n", fill=tk.X, padx=6, pady=(8, 2))

        body_lines = ["Castillo"] if hidden else [card.type_name]
        if hidden:
            pass
        elif card.cost:
            body_lines.append(f"Coste {card.cost}")
        if not hidden and isinstance(card, Ally):
            body_lines.append(f"Fuerza {card.strength}")
        if not hidden and card.text and not compact:
            body_lines.append(card.text)

        body = tk.Label(
            frame,
            text="\n".join(body_lines),
            bg=bg,
            fg=fg,
            font=("Segoe UI", 8),
            wraplength=112,
            justify=tk.CENTER,
        )
        body.pack(expand=True, fill=tk.BOTH, padx=6, pady=4)

        frame.card = card
        return frame

    def _bind_drag(self, widget, card):
        for child in widget.winfo_children():
            child.bind("<ButtonPress-1>", lambda event, w=widget, c=card: self.start_drag(event, w, c))
            child.bind("<B1-Motion>", self.move_drag)
            child.bind("<ButtonRelease-1>", self.release_drag)

        widget.bind("<ButtonPress-1>", lambda event, w=widget, c=card: self.start_drag(event, w, c))
        widget.bind("<B1-Motion>", self.move_drag)
        widget.bind("<ButtonRelease-1>", self.release_drag)

    def start_drag(self, event, widget, card):
        if self.game.game_over:
            self.log("La partida ya terminó.")
            return
        if card not in self.game.active_player.hand.cards:
            return

        ghost = self._create_card_widget(self.root, card)
        ghost.place(
            x=self.root.winfo_pointerx() - self.root.winfo_rootx() - CARD_WIDTH // 2,
            y=self.root.winfo_pointery() - self.root.winfo_rooty() - CARD_HEIGHT // 2,
        )
        ghost.lift()

        self.drag = {
            "card": card,
            "ghost": ghost,
        }

    def move_drag(self, event):
        if not self.drag:
            return
        ghost = self.drag["ghost"]
        ghost.place(
            x=self.root.winfo_pointerx() - self.root.winfo_rootx() - CARD_WIDTH // 2,
            y=self.root.winfo_pointery() - self.root.winfo_rooty() - CARD_HEIGHT // 2,
        )

    def release_drag(self, event):
        if not self.drag:
            return

        card = self.drag["card"]
        ghost = self.drag["ghost"]
        ghost.destroy()
        self.drag = None

        target = self._target_under_pointer()
        if target is None:
            self.log("Suelta la carta sobre una zona de juego.")
            return

        self.try_play_card(card, target)

    def _target_under_pointer(self):
        pointer_x = self.root.winfo_pointerx()
        pointer_y = self.root.winfo_pointery()

        for target in ("gold", "support", "defense", "attack", "graveyard"):
            frame = self.zone_frames.get(f"player_{target}")
            if frame and self._contains_pointer(frame, pointer_x, pointer_y):
                return target
        return None

    def _contains_pointer(self, widget, pointer_x, pointer_y):
        left = widget.winfo_rootx()
        top = widget.winfo_rooty()
        right = left + widget.winfo_width()
        bottom = top + widget.winfo_height()
        return left <= pointer_x <= right and top <= pointer_y <= bottom

    def try_play_card(self, card, target):
        if self.game.game_over:
            self.log("La partida ya terminó.")
            return

        expected = ZONE_TARGETS.get(card.type, "support")
        if target != expected:
            self.log(
                f"{card.name} debe jugarse en {ZONE_LABELS[expected]}, "
                f"no en {ZONE_LABELS[target]}."
            )
            self.refresh()
            return

        output = io.StringIO()
        with contextlib.redirect_stdout(output):
            played = self.game.play_card_from_hand(card)

        text = output.getvalue().strip()
        if text:
            self.log(text)
        if not played:
            self.log(f"No se pudo jugar {card.name}.")
        if self.game.game_over and self.game.winner:
            self.log(f"{self.game.winner.name} gana la partida.")
        self.refresh()

    def show_zone_cards(self, zone_id):
        cards = self.zone_data.get(zone_id, [])
        title = self.zone_frames[zone_id].winfo_children()[0].cget("text")

        window = tk.Toplevel(self.root)
        window.title(title)
        window.geometry("760x420")
        window.configure(bg="#17211d")

        header = tk.Label(
            window,
            text=f"{title} - {len(cards)} carta(s)",
            bg="#17211d",
            fg="#f2f7f4",
            font=("Segoe UI", 13, "bold"),
        )
        header.pack(anchor="w", padx=12, pady=(10, 6))

        canvas = tk.Canvas(window, bg="#17211d", highlightthickness=0)
        scrollbar = ttk.Scrollbar(window, orient=tk.HORIZONTAL, command=canvas.xview)
        canvas.configure(xscrollcommand=scrollbar.set)
        scrollbar.pack(side=tk.BOTTOM, fill=tk.X)
        canvas.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        content = tk.Frame(canvas, bg="#17211d")
        canvas.create_window((0, 0), window=content, anchor="nw")

        if not cards:
            empty = tk.Label(
                content,
                text="Esta zona esta vacia.",
                bg="#17211d",
                fg="#b8c8bf",
                font=("Segoe UI", 11),
            )
            empty.pack(padx=20, pady=30)
        else:
            hidden = zone_id.endswith("_deck")
            for card in cards:
                widget = self._create_card_widget(content, card, hidden=hidden)
                widget.pack(side=tk.LEFT, padx=8, pady=10)

        content.update_idletasks()
        canvas.configure(scrollregion=canvas.bbox("all"))

    def show_field_reference(self):
        image_path = Path(__file__).resolve().parent / "assets" / "campo_myl.png"
        if not image_path.exists():
            self.log("No se encontro la imagen local del campo oficial.")
            return

        window = tk.Toplevel(self.root)
        window.title("Campo oficial MyL")
        window.configure(bg="#17211d")

        image = tk.PhotoImage(file=str(image_path))
        while image.width() > 900 or image.height() > 560:
            image = image.subsample(2, 2)
        self.manual_image = image

        label = tk.Label(window, image=image, bg="#17211d")
        label.pack(padx=12, pady=12)

    def end_turn(self):
        if self.game.game_over:
            self.log("La partida ya terminó.")
            return

        output = io.StringIO()
        with contextlib.redirect_stdout(output):
            self.game.final_draw()
            if not self.game.game_over:
                self.game.regroup_phase()

        text = output.getvalue().strip()
        if text:
            self.log(text)
        if self.game.game_over and self.game.winner:
            self.log(f"{self.game.winner.name} gana la partida.")
        else:
            self.log(f"Comienza el turno de {self.game.active_player.name}.")
        self.refresh()

    def log(self, message):
        self.log_box.configure(state=tk.NORMAL)
        self.log_box.insert(tk.END, f"{message}\n")
        self.log_box.see(tk.END)
        self.log_box.configure(state=tk.DISABLED)


def run_gui():
    root = tk.Tk()
    style = ttk.Style(root)
    style.theme_use("clam")
    style.configure("TFrame", background="#22312b")
    style.configure("TLabel", background="#22312b", foreground="#f2f7f4")
    style.configure("TButton", padding=(12, 6))

    GameGui(root)
    root.mainloop()


if __name__ == "__main__":
    run_gui()
