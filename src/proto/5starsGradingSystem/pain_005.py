import sys
import json
from math import pi, cos, sin
from datetime import datetime

from PySide6.QtCore import Qt, QSize, QPointF, QAbstractTableModel, QModelIndex, QEvent
from PySide6.QtGui import QPainter, QColor, QPolygonF
from PySide6.QtWidgets import (
    QApplication, QWidget, QTableView, QVBoxLayout, QPushButton,
    QStyledItemDelegate, QMessageBox, QFileDialog, QLabel
)

class PainStarDelegate(QStyledItemDelegate):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.hover_rating = {}

    def paint(self, painter, option, index):
        pain_level = index.data(Qt.ItemDataRole.DisplayRole) or 0
        temp = self.hover_rating.get(index, 0)
        display_level = temp if temp > 0 else pain_level

        painter.save()
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        cell_rect = option.rect.adjusted(10, 5, -10, -5)
        star_size = cell_rect.height()
        radius = star_size // 2

        # Color based on displayed level
        if display_level == 0:
            fill_color = None
            outline_color = QColor("#666666")
        elif display_level <= 3:
            fill_color = QColor("#32CD32")      # Mild – Green
            outline_color = QColor("#228B22")
        elif display_level <= 6:
            fill_color = QColor("#FFD700")      # Moderate – Yellow
            outline_color = QColor("#B8860B")
        else:
            fill_color = QColor("#FF4500")      # Severe – Red
            outline_color = QColor("#B22222")

        for i in range(10):
            cx = cell_rect.left() + i * star_size + star_size // 2
            cy = cell_rect.center().y()
            filled = i < display_level
            self.draw_star(painter, cx, cy, radius, filled, fill_color, outline_color)

        painter.restore()

    def draw_star(self, painter, cx, cy, radius, filled, fill_color, outline_color):
        outer = radius
        inner = radius * 0.382

        points = []
        for i in range(10):
            r = outer if i % 2 == 0 else inner
            angle = i * (pi / 5) - (pi / 2)
            points.append(QPointF(cx + r * cos(angle), cy + r * sin(angle)))

        polygon = QPolygonF(points)

        if filled and fill_color:
            painter.setBrush(fill_color)
            painter.setPen(outline_color)
        else:
            painter.setBrush(Qt.BrushStyle.NoBrush)
            painter.setPen(outline_color if filled else QColor("#666666"))

        painter.drawPolygon(polygon)

    def sizeHint(self, option, index):
        return QSize(30 * 10 + 40, 55)

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
                new_level = 0
            model.setData(index, new_level, Qt.ItemDataRole.EditRole)
            self.hover_rating.pop(index, None)
            option.widget.update(option.rect)
            return True

        return super().editorEvent(event, model, option, index)


class PainTableModel(QAbstractTableModel):
    def __init__(self):
        super().__init__()
        self.body_parts = [
            "Head / Migraine",
            "Neck",
            "Shoulders",
            "Upper Back",
            "Lower Back",
            "Chest",
            "Abdomen / Stomach",
            "Hips",
            "Left Knee",
            "Right Knee",
            "Left Ankle",
            "Right Ankle",
            "Hands / Wrists",
            "Feet",
        ]
        self.data_list = [[part, 0] for part in self.body_parts]
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
        return [
            {"body_part": row[0], "pain_level": row[1]}
            for row in self.data_list
        ]


class PainTrackerApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Pain Tracker – Body Parts (0–10 Scale)")

        layout = QVBoxLayout(self)

        # Current date and time label
        self.datetime_label = QLabel()
        self.datetime_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.datetime_label.setStyleSheet("""
            QLabel {
                font-size: 16px;
                font-weight: bold;
                color: #333;
                margin: 10px;
                padding: 8px;
                background: #e8f4f8;
                border: 1px solid #aaa;
            }
        """)
        self.update_datetime()

        # Table
        self.table_view = QTableView()
        self.model = PainTableModel()
        self.table_view.setModel(self.model)

        delegate = PainStarDelegate(self.table_view)
        self.table_view.setItemDelegateForColumn(1, delegate)

        self.table_view.resizeColumnsToContents()
        self.table_view.setColumnWidth(1, 380)
        self.table_view.horizontalHeader().setStretchLastSection(True)

        # Legend
        legend = QLabel(
            "<b>Pain Rating Guide (0–10 stars):</b><br><br>"
            "<span style='color:#32CD32; font-weight:bold;'>●●●</span> 1–3 stars – <b>Mild pain</b> (noticeable but manageable)<br>"
            "<span style='color:#FFD700; font-weight:bold;'>●●●</span> 4–6 stars – <b>Moderate pain</b> (interferes with activities)<br>"
            "<span style='color:#FF4500; font-weight:bold;'>●●●</span> 7–10 stars – <b>Severe pain</b> (very difficult to function)<br><br>"
            "0 stars – No pain"
        )
        legend.setAlignment(Qt.AlignmentFlag.AlignCenter)
        legend.setStyleSheet("""
            QLabel {
                color: #333;
                font-size: 14px;
                background: #f9f9f9;
                border: 1px solid #ccc;
                padding: 12px;
                margin: 8px;
            }
        """)
        legend.setWordWrap(True)

        # Save button
        self.save_button = QPushButton("Save Pain Ratings to File")
        self.save_button.clicked.connect(self.save_ratings)

        # Layout assembly
        layout.addWidget(self.datetime_label)
        layout.addWidget(self.table_view)
        layout.addWidget(legend)
        layout.addWidget(self.save_button)

    def update_datetime(self):
        now = datetime.now()
        formatted = now.strftime("%A, %B %d, %Y – %I:%M %p")
        self.datetime_label.setText(f"Current Assessment Time:\n{formatted}")

    def save_ratings(self):
        self.update_datetime()  # Refresh just before saving

        file_name, _ = QFileDialog.getSaveFileName(
            self,
            "Save Pain Ratings",
            f"pain_ratings_{datetime.now().strftime('%Y-%m-%d_%H-%M')}.json",
            "JSON Files (*.json);;All Files (*)"
        )
        if not file_name:
            return

        save_time = datetime.now().isoformat()

        data = {
            "assessment_datetime": save_time,
            "formatted_datetime": self.datetime_label.text().replace("Current Assessment Time:\n", ""),
            "ratings": self.model.get_all_data()
        }

        try:
            with open(file_name, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=4)
            QMessageBox.information(
                self,
                "Success",
                f"Pain ratings saved with timestamp!\n\nFile: {file_name}"
            )
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Could not save file:\n{str(e)}")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = PainTrackerApp()
    window.resize(850, 750)
    window.show()
    sys.exit(app.exec())


