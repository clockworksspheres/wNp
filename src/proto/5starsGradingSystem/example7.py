import sys
import json  # For saving data
from math import pi, cos, sin

from PySide6.QtCore import Qt, QSize, QPointF, QAbstractTableModel, QModelIndex, QEvent
from PySide6.QtGui import QPainter, QColor, QPolygonF
from PySide6.QtWidgets import (
    QApplication, QWidget, QTableView, QVBoxLayout, QPushButton,
    QStyledItemDelegate, QMessageBox, QFileDialog
)

class StarRatingDelegate(QStyledItemDelegate):
    def __init__(self, parent=None):
        super().__init__(parent)
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

        for i in range(5):
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
            painter.setBrush(QColor("#FFD700"))
            painter.setPen(QColor("#B8860B"))
        else:
            painter.setBrush(Qt.BrushStyle.NoBrush)
            painter.setPen(QColor("#666666"))

        painter.drawPolygon(polygon)

    def sizeHint(self, option, index):
        return QSize(240, 50)

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
        new_rating = max(0, min(int(rel_x / cell_rect.height()) + 1, 5))

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


class RatingTableModel(QAbstractTableModel):
    def __init__(self):
        super().__init__()
        self.data_list = [
            ["The Shawshank Redemption", 5],
            ["The Godfather", 5],
            ["Inception", 4],
            ["Pulp Fiction", 4],
            ["The Matrix", 3],
            ["Forrest Gump", 0],
        ]
        self.headers = ["Movie Title", "Rating"]

    def rowCount(self, parent=QModelIndex()):
        return len(self.data_list)

    def columnCount(self, parent=QModelIndex()):
        return 2

    def data(self, index, role=Qt.ItemDataRole.DisplayRole):
        if not index.isValid():
            return None
        value = self.data_list[index.row()][index.column()]
        if role in (Qt.ItemDataRole.DisplayRole, Qt.ItemDataRole.EditRole):
            return value
        return None

    def setData(self, index, value, role=Qt.ItemDataRole.EditRole):
        if index.isValid() and role == Qt.ItemDataRole.EditRole and index.column() == 1:
            self.data_list[index.row()][1] = value
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
        """Return a copy of the current data for saving"""
        return [{"title": row[0], "rating": row[1]} for row in self.data_list]


class TableApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("PySide6 Table with Interactive 5-Star Ratings + Save")

        layout = QVBoxLayout(self)

        self.table_view = QTableView()
        self.model = RatingTableModel()
        self.table_view.setModel(self.model)

        delegate = StarRatingDelegate(self.table_view)
        self.table_view.setItemDelegateForColumn(1, delegate)

        self.table_view.resizeColumnsToContents()
        self.table_view.setColumnWidth(1, 260)
        self.table_view.horizontalHeader().setStretchLastSection(True)

        # Save Button
        self.save_button = QPushButton("Save Ratings to File")
        self.save_button.clicked.connect(self.save_ratings)

        layout.addWidget(self.table_view)
        layout.addWidget(self.save_button)

    def save_ratings(self):
        file_name, _ = QFileDialog.getSaveFileName(
            self, "Save Ratings", "", "JSON Files (*.json);;All Files (*)"
        )
        if not file_name:
            return  # User canceled

        data = self.model.get_all_data()

        try:
            with open(file_name, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=4)
            QMessageBox.information(self, "Saved", f"Ratings successfully saved to:\n{file_name}")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to save file:\n{str(e)}")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = TableApp()
    window.resize(700, 450)
    window.show()
    sys.exit(app.exec())

