import sys
from math import cos, sin, pi

from PySide6.QtCore import Qt, QSize, QPointF
from PySide6.QtGui import QPainter, QPolygonF
from PySide6.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout, QSizePolicy


PAINTING_SCALE_FACTOR = 20

class StarRating(QWidget):
    def __init__(self, star_count=5, max_star_count=5, parent=None):
        super().__init__(parent)
        self.star_count = star_count
        self.max_star_count = max_star_count

        self.setSizePolicy(
            QSizePolicy.Policy.Fixed,
            QSizePolicy.Policy.Fixed
        )
        #self.setSizePolicy(QWidget.sizePolicy.Fixed, QWidget.sizePolicy.Fixed)
        self.setMouseTracking(True)

    def sizeHint(self):
        return QSize(PAINTING_SCALE_FACTOR * self.max_star_count, PAINTING_SCALE_FACTOR)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        painter.setPen(Qt.NoPen)

        diamond = QPolygonF()
        for i in range(5):
            angle = pi / 5 * (i * 2 + 1)
            diamond << QPointF(0.5 + 0.4 * cos(angle), 0.5 + 0.4 * sin(angle))

        painter.translate(0, self.height() / 2)
        painter.scale(PAINTING_SCALE_FACTOR, PAINTING_SCALE_FACTOR)

        for i in range(self.max_star_count):
            painter.save()
            painter.translate(i + 0.5, 0.5)
            if i < self.star_count:
                painter.setBrush(Qt.yellow)  # Filled star
            else:
                painter.setBrush(Qt.gray)    # Empty star
            painter.drawPolygon(diamond)
            painter.restore()

    def mouseMoveEvent(self, event):
        x = event.position().x()
        star = int(x / (self.sizeHint().width() / self.max_star_count)) + 1
        if 0 < star <= self.max_star_count:
            self.star_count = star
            self.update()
        super().mouseMoveEvent(event)

    def mousePressEvent(self, event):
        # Could lock the rating here if needed
        pass


class RatingApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("PySide6 5-Star Rating Example")
        layout = QVBoxLayout(self)

        self.rating = StarRating(star_count=3)  # Initial rating: 3 stars
        self.label = QLabel("Current rating: 3")
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        layout.addWidget(self.rating)
        layout.addWidget(self.label)

        self.rating.star_count_changed = lambda: self.label.setText(f"Current rating: {self.rating.star_count}")

        # Connect hover for live update
        def update_label():
            self.label.setText(f"Current rating: {self.rating.star_count}")
        self.rating.update = lambda: (QWidget.update(self.rating), update_label())

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = RatingApp()
    window.resize(400, 200)
    window.show()
    sys.exit(app.exec())


