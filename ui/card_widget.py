from pathlib import Path

from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import QFrame, QLabel, QVBoxLayout


BASE_DIR = Path(__file__).resolve().parent.parent


class CardWidget(QFrame):
    clicked = Signal(dict)

    def __init__(self, card):
        super().__init__()
        self.card = card

        self.setFixedSize(180, 290)
        self.setCursor(Qt.PointingHandCursor)

        self.setStyleSheet("""
            QFrame {
                background-color: #222;
                border: 2px solid #555;
                border-radius: 10px;
            }

            QFrame:hover {
                border: 2px solid #d6b15d;
                background-color: #2d2d2d;
            }

            QLabel {
                color: white;
                background: transparent;
            }
        """)

        layout = QVBoxLayout()
        layout.setContentsMargins(8, 8, 8, 8)

        self.image_label = QLabel()
        self.image_label.setFixedSize(160, 220)
        self.image_label.setAlignment(Qt.AlignCenter)

        image_path = BASE_DIR / card["image"]

        if image_path.exists():
            pixmap = QPixmap(str(image_path))
            pixmap = pixmap.scaled(
                160,
                220,
                Qt.KeepAspectRatio,
                Qt.SmoothTransformation
            )
            self.image_label.setPixmap(pixmap)
        else:
            self.image_label.setText("Sin imagen")

        self.name_label = QLabel(card["name"])
        self.name_label.setAlignment(Qt.AlignCenter)
        self.name_label.setWordWrap(True)

        self.type_label = QLabel(f'Tipo: {card["type"]}')
        self.type_label.setAlignment(Qt.AlignCenter)

        layout.addWidget(self.image_label)
        layout.addWidget(self.name_label)
        layout.addWidget(self.type_label)

        self.setLayout(layout)

    def mousePressEvent(self, event):
        self.clicked.emit(self.card)