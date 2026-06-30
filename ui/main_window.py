from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QGridLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QMainWindow,
    QPushButton,
    QScrollArea,
    QTextEdit,
    QVBoxLayout,
    QWidget
)

from db import get_cards
from ui.card_widget import CardWidget


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Mi TCG - Colección de Cartas")
        self.resize(1100, 700)

        self.cards = []

        main_container = QWidget()
        main_layout = QHBoxLayout()

        left_layout = QVBoxLayout()

        title = QLabel("Colección de Cartas")
        title.setStyleSheet("font-size: 24px; font-weight: bold;")

        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Buscar por nombre, tipo o habilidad...")
        self.search_input.textChanged.connect(self.load_cards)

        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)

        self.cards_container = QWidget()
        self.cards_grid = QGridLayout()
        self.cards_grid.setAlignment(Qt.AlignTop)

        self.cards_container.setLayout(self.cards_grid)
        self.scroll_area.setWidget(self.cards_container)

        left_layout.addWidget(title)
        left_layout.addWidget(self.search_input)
        left_layout.addWidget(self.scroll_area)

        right_layout = QVBoxLayout()

        detail_title = QLabel("Detalle de la carta")
        detail_title.setStyleSheet("font-size: 20px; font-weight: bold;")

        self.detail_box = QTextEdit()
        self.detail_box.setReadOnly(True)

        self.edit_button = QPushButton("Editar carta")
        self.edit_button.setEnabled(False)

        right_layout.addWidget(detail_title)
        right_layout.addWidget(self.detail_box)
        right_layout.addWidget(self.edit_button)

        main_layout.addLayout(left_layout, 3)
        main_layout.addLayout(right_layout, 1)

        main_container.setLayout(main_layout)
        self.setCentralWidget(main_container)

        self.selected_card = None

        self.load_cards()

    def clear_grid(self):
        while self.cards_grid.count():
            item = self.cards_grid.takeAt(0)
            widget = item.widget()

            if widget:
                widget.deleteLater()

    def load_cards(self):
        search_text = self.search_input.text().strip()
        self.cards = get_cards(search_text)

        self.clear_grid()

        row = 0
        col = 0
        max_columns = 4

        for card in self.cards:
            card_widget = CardWidget(card)
            card_widget.clicked.connect(self.show_card_detail)

            self.cards_grid.addWidget(card_widget, row, col)

            col += 1

            if col >= max_columns:
                col = 0
                row += 1

    def show_card_detail(self, card):
        self.selected_card = card
        self.edit_button.setEnabled(True)

        text = f"""
Nombre: {card["name"]}

Tipo: {card["type"]}

Coste: {card["cost"]}

Fuerza: {card["strength"]}

Habilidad:
{card["ability"]}

Edición: {card["edition"]}

Número de serie: {card["code"]}

Válida: {"Sí" if card["valid"] else "No"}
        """

        self.detail_box.setText(text.strip())