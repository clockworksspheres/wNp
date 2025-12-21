import sys
import json
from math import pi, cos, sin

from PySide6.QtCore import Qt, QSize, QPointF, QAbstractTableModel, QModelIndex, QEvent
from PySide6.QtGui import QPainter, QColor, QPolygonF
from PySide6.QtWidgets import (
    QApplication, QWidget, QTableView, QVBoxLayout, QPushButton,
    QStyledItemDelegate, QMessageBox, QFileDialog, QLabel
)

class StarRatingDelegate(QStyledItemDelegate):
    def __init__(self, max_stars=10, parent=None):
        super().__init__(parent)
        self.max_stars = max_stars
        self.hover_rating = {}  # Temporary hover per cell

    def paint(self, painter, option, index):
        rating = index.data(Qt.ItemDataRole.DisplayRole) or 0
        temp = self.hover_rating.get(index, 0)
        display_rating = temp if temp > 0 else rating

        painter.save()
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        cell_rect = option.rect.adjusted(10, 5, -10, -5)
        star_size = cell_rect.height()
        radius = star_size // 2

        for i in range(self.max_stars):
            cx = cell_rect.left() + i * star_size + star_size // 2
            cy = cell_rect.center().y()
            filled = i < display_rating
            self.draw_star(painter, cx, cy, radius, filled)

        painter.restore()

    def draw_star(self, painter, cx, cy, radius, filled):
        outer = radius
        inner = radius * 0.382

        points = []
        for i in range(10):
            r = outer if i % 2 == 0 else inner
            angle = i * (pi / 5) - (pi / 2)
            points.append(QPointF(cx + r * cos(angle), cy + r * sin(angle)))

        polygon = QPolygonF(points)

        if filled:
            # Color gradient: green → yellow → red as pain increases
            if filled <= 3:
                painter.setBrush(QColor("#4CAF50"))  # Green (mild)
            elif filled <= 6:
                painter.setBrush(QColor("#FFC107"))  # Yellow (moderate)
            else:
                painter.setBrush(QColor("#F44336"))  # Red (severe)
            painter.setPen(QColor("#333333"))
        else:
            painter.setBrush(Qt.BrushStyle.NoBrush)
            painter.setPen(QColor("#888888"))

        painter.drawPolygon(polygon)

    def sizeHint(self, option, index):
        return QSize(30 * self.max_stars + 40, 50)  # Wider for 10 stars

    def editorEvent(self, event, model, option, index):
        if event.type() == QEvent.Type.Leave:
            if index in self.hover_rating:
                del self.hover_rating[index]
                option.widget.update(option.rect)
            return False

        if event.type() not in (QEvent.Type.MouseMove, QEvent.Type.MouseButtonPress):
            return False

        if not option.rect.contains(event.position().toPoint()):
            if index in self.hover_rating:
                del self.hover_rating[index]
                option.widget.update(option.rect)
            return False

        cell_rect = option.rect.adjusted(10, 5, -10, -5)
        rel_x = event.position().x() - cell_rect.left()
        new_rating = max(0, min(int(rel_x / cell_rect.height()) + 1, self.max_stars))

        if event.type() == QEvent.Type.MouseMove:
            if self.hover_rating.get(index) != new_rating:
                self.hover_rating[index] = new_rating
                option.widget.update(option.rect)
            return True

        if event.type() == QEvent.Type.MouseButtonPress and event.button() == Qt.MouseButton.LeftButton:
            current = index.data(Qt.ItemDataRole.DisplayRole) or 0
            if new_rating == current and current > 0:
                new_rating = 0  # Re-click to clear
            model.setData(index, new_rating, Qt.ItemDataRole.EditRole)
            self.hover_rating.pop(index, None)
            option.widget.update(option.rect)
            return True

        return super().editorEvent(event, model, option, index)


class PainRatingModel(QAbstractTableModel):
    def __init__(self):
        super().__init__()
        self.body_parts = [
            ["Head", 0],
            ["Neck", 0],
            ["Shoulders", 0],
            ["Upper Back", 0],
            ["Lower Back", 0],
            ["Chest", 0],
            ["Abdomen", 0],
            ["Left Arm", 0],
            ["Right Arm", 0],
            ["Left Leg", 0],
            ["Right Leg", 0],
            ["Hands", 0],
            ["Feet", 0],
        ]
        self.headers = ["Body Part", "Pain Level (0–10)"]

    def rowCount(self, parent=QModelIndex()):
        return len(self.body_parts)

    def columnCount(self, parent=QModelIndex()):
        return 2

    def data(self, index, role=Qt.ItemDataRole.DisplayRole):
        if not index.isValid():
            return None
        value = self.body_parts[index.row()][index.column()]
        if role in (Qt.ItemDataRole.DisplayRole, Qt.ItemDataRole.EditRole):
            return value
        return None

    def setData(self, index, value, role=Qt.ItemDataRole.EditRole):
        if index.isValid() and role == Qt.ItemDataRole.EditRole and index.column() == 1:
            self.body_parts[index.row()][1] = value
            self.dataChanged.emit(index, index)
            return True
        return False

    def headerData(self, section, orientation, role=Qt.ItemDataRole.DisplayRole):
        if role == Qt.ItemDataRole.DisplayRole and orientation == Qt.Orientation.Horizontal:
            return self.headers[section]
        return super().headerData(section, orientation, role)

    def flags(self, index):
        flags = super().flags(index)
        if index.column() == 1:
            flags |= Qt.ItemFlag.ItemIsEditable
        return flags

    def get_all_data(self):
        return [{"body_part": row[0], "pain_level": row[1]} for row in self.body_parts]


class PainTrackerApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Body Pain Tracker (0–10 Scale)")

        layout = QVBoxLayout(self)

        # Table
        self.table_view = QTableView()
        self.model = PainRatingModel()
        self.table_view.setModel(self.model)

        delegate = StarRatingDelegate(max_stars=10, parent=self.table_view)
        self.table_view.setItemDelegateForColumn(1, delegate)

        self.table_view.resizeColumnsToContents()
        self.table_view.setColumnWidth(1, 380)  # Wide enough for 10 stars
        self.table_view.horizontalHeader().setStretchLastSection(True)

        # Pain scale legend
        legend = QLabel(
            "<b>Pain Scale (0–10):</b><br>"
            "0 = No pain<br>"
            "1–3 = Mild pain (nagging, annoying)<br>"
            "4–6 = Moderate pain (interferes with tasks)<br>"
            "7–10 = Severe pain (debilitating, worst imaginable)<br><br>"
            "<i>Click stars to rate pain. Click again on the selected star to clear.</i>"
        )
        legend.setAlignment(Qt.AlignmentFlag.AlignCenter)
        legend.setStyleSheet("QLabel { color: #333; font-size: 13px; margin: 10px; }")

        # Save button
        save_button = QPushButton("Save Pain Ratings to File")
        save_button.clicked.connect(self.save_ratings)

        # Add to layout
        layout.addWidget(QLabel("<h2>Rate Your Pain by Body Part</h2>", alignment=Qt.AlignmentFlag.AlignCenter))
        layout.addWidget(self.table_view)
        layout.addWidget(legend)
        layout.addWidget(save_button)

    def save_ratings(self):
        file_name, _ = QFileDialog.getSaveFileName(
            self, "Save Pain Ratings", "", "JSON Files (*.json);;All Files (*)"
        )
        if not file_name:
            return

        data = self.model.get_all_data()
        try:
            with open(file_name, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=4)
            QMessageBox.information(self, "Saved", f"Pain ratings saved to:\n{file_name}")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to save:\n{str(e)}")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = PainTrackerApp()
    window.resize(800, 700)
    window.show()
    sys.exit(app.exec())


