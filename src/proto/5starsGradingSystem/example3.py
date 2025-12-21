import sys
from math import pi, cos, sin  # For star geometry

from PySide6.QtCore import Qt, QSize, QPointF
from PySide6.QtGui import QPainter, QColor, QPolygonF  # <-- QPolygonF added here!
from PySide6.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout, QSizePolicy

class StarRating(QWidget):
    def __init__(self, max_stars=5, parent=None):
        super().__init__(parent)
        self.max_stars = max_stars
        self._rating = 0          # Permanent rating
        self._hover_rating = 0    # Hover preview
        
        self.setSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed)
        self.setMouseTracking(True)

    def sizeHint(self):
        return QSize(40 * self.max_stars, 40)  # Larger for better visibility

    def rating(self):
        return self._rating

    def setRating(self, rating):
        self._rating = max(0, min(rating, self.max_stars))
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        
        star_size = 40
        for i in range(self.max_stars):
            x = i * star_size
            filled = (i < self._hover_rating) or (self._hover_rating == 0 and i < self._rating)
            self.draw_star(painter, x + star_size // 2, self.height() // 2, star_size // 2, filled)

    def draw_star(self, painter, cx, cy, radius, filled):
        outer_radius = radius
        inner_radius = radius * 0.382  # Golden ratio for classic star shape
        
        points = []
        for i in range(10):
            r = outer_radius if i % 2 == 0 else inner_radius
            angle = i * (pi / 5) - (pi / 2)
            points.append(QPointF(cx + r * cos(angle), cy + r * sin(angle)))
        
        polygon = QPolygonF(points)  # Now this works!
        
        if filled:
            painter.setBrush(QColor("#FFD700"))  # Gold fill
            painter.setPen(QColor("#B8860B"))    # Outline
        else:
            painter.setBrush(Qt.BrushStyle.NoBrush)
            painter.setPen(QColor("#555555"))    # Visible gray outline
        
        painter.drawPolygon(polygon)

    def mouseMoveEvent(self, event):
        x = event.position().x()
        star_index = int(x / 40)
        if 0 <= star_index < self.max_stars:
            self._hover_rating = star_index + 1
        else:
            self._hover_rating = 0
        self.update()

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            x = event.position().x()
            star_index = int(x / 40)
            if 0 <= star_index < self.max_stars:
                self.setRating(star_index + 1)
                self._hover_rating = 0
                self.update()

    def leaveEvent(self, event):
        self._hover_rating = 0
        self.update()


class RatingApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("PySide6 Interactive 5-Star Rating")
        
        layout = QVBoxLayout(self)
        
        self.star_widget = StarRating(max_stars=5)
        self.star_widget.setRating(0)
        
        self.label = QLabel("Click the stars to rate!")
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        layout.addWidget(self.star_widget, alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.label)
        
        def update_label():
            r = self.star_widget.rating()
            self.label.setText(f"Your rating: {'★' * r}{'☆' * (5 - r)} ({r}/5)")
        
        original_update = self.star_widget.update
        self.star_widget.update = lambda: (original_update(), update_label())
        update_label()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = RatingApp()
    window.resize(500, 250)
    window.show()
    sys.exit(app.exec())

