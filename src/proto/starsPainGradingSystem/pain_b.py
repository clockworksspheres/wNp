import sys
import json
from math import pi, cos, sin

from PySide6.QtCore import Qt, QSize, QPointF, QAbstractTableModel, QModelIndex, QEvent
from PySide6.QtGui import QPainter, QColor, QPolygonF
from PySide6.QtWidgets import (
    QApplication, QWidget, QTableView, QVBoxLayout, QPushButton,
    QStyledItemDelegate, QMessageBox, QFileDialog, QLabel
)

class PainStarDelegate(QStyledItemDelegate):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.hover_rating = {}  # index → temporary hover stars

    def paint(self, painter, option, index):
        pain_level = index.data(Qt.ItemDataRole.DisplayRole) or 0
        temp = self.hover_rating.get(index, 0)
        display_level = temp if temp > 0 else pain_level

        painter.save()
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        cell_rect = option.rect.adjusted(10, 5, -10, -5)
        star_size = cell_rect.height()
        radius = star_size // 2

        for i in range(10):
            cx = cell_rect.left() + i * star_size + star_size // 2
            cy = cell_rect.center().y()
            filled = i < display_level
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
            painter.setBrush(QColor("#FF4500"))      # Orange-red for pain
            painter.setPen(QColor("#B22222"))
        else:
            painter.setBrush(Qt.BrushStyle.NoBrush)
            painter.setPen(QColor("#666666"))

        painter.drawPolygon(polygon)

    def sizeHint(self, option, index):
        return QSize(30 * 10 + 20, 50)  # Wide enough for 10 stars

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
        new_level = max(0, min(int(rel_x / cell_rect.height()) + 1, 10))

        if event.type() == QEvent.Type.MouseMove:
            if self.hover_rating.get(index) != new_level:
                self.hover_rating[index] = new_level
                option.widget.update(option.rect)
            return True

        if event.type() == QEvent.Type.MouseButtonPress and event.button() == Qt.MouseButton.LeftButton:
            current = index.data(Qt.ItemDataRole.DisplayRole) or 0
            if new_level == current and current > 0:
                new_level = 0  # Re-click clears
            model.setData(index, new_level, Qt.ItemDataRole.EditRole)
            self.hover_rating.pop(index, None)
            option.widget.update(option.rect)
            return True

        return super().editorEvent(event, model, option, index)


class PainTableModel(QAbstractTableModel):
    def __init__(self):
        super().__init__()
        self.data_list = [
            ["Head / Migraine", 0],
            ["Neck", 0],
            ["Shoulders", 0],
            ["Upper Back", 0],
            ["Lower Back", 0],
            ["Chest", 0],
            ["Abdomen / Stomach", 0],
            ["Hips", 0],
            ["Left Knee", 0],
            ["Right Knee", 0],
            ["Left Ankle", 0],
            ["Right Ankle", 0],
            ["Hands / Wrists", 0],
            ["Feet", 0],
        ]
        self.headers = ["Body Part", "Pain Level (0–10)"]

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
        return [{"body_part": row[0], "pain_level": row[1]} for row in self.data_list]


class PainTrackerApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Pain Tracker – Rate Your Body Parts (0–10 Stars)")

        layout = QVBoxLayout(self)

        # Table
        self.table_view = QTableView()
        self.model = PainTableModel()
        self.table_view.setModel(self.model)

        delegate = PainStarDelegate(self.table_view)
        self.table_view.setItemDelegateForColumn(1, delegate)

        self.table_view.resizeColumnsToContents()
        self.table_view.setColumnWidth(1, 350)  # Wide for 10 stars
        self.table_view.horizontalHeader().setStretchLastSection(True)

        # Legend
        legend = QLabel(
            "<b>Pain Rating Guide (0–10 stars):</b><br>"
            "0 ★ – No pain at all<br>"
            "1–3 ★ – Mild pain (noticeable but manageable)<br>"
            "4–6 ★ – Moderate pain (interferes with normal activities)<br>"
            "7–9 ★ – Severe pain (very difficult to function)<br>"
            "10 ★ – Worst possible pain (unbearable)"
        )
        legend.setAlignment(Qt.AlignmentFlag.AlignCenter)
        legend.setStyleSheet("QLabel { color: #444; font-size: 13px; margin: 12px; background: #f8f8f8; border: 1px solid #ddd; padding: 8px; }")

        # Save button
        self.save_button = QPushButton("Save Pain Ratings to File")
        self.save_button.clicked.connect(self.save_ratings)

        layout.addWidget(self.table_view)
        layout.addWidget(legend)
        layout.addWidget(self.save_button)

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
            QMessageBox.information(self, "Success", f"Pain ratings saved to:\n{file_name}")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Could not save:\n{str(e)}")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = PainTrackerApp()
    window.resize(800, 650)
    window.show()
    sys.exit(app.exec())


