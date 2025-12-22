import sys
from math import pi, cos, sin

from PySide6.QtCore import Qt, QSize, QPointF, QAbstractTableModel, QModelIndex
from PySide6.QtGui import QPainter, QColor, QPolygonF
from PySide6.QtWidgets import (
    QApplication, QWidget, QTableView, QVBoxLayout,
    QStyledItemDelegate, QSizePolicy
)

class StarRatingDelegate(QStyledItemDelegate):
    def __init__(self, parent=None):
        super().__init__(parent)

    def paint(self, painter, option, index):
        rating = index.data(Qt.ItemDataRole.DisplayRole)
        if rating is None:
            rating = 0
        
        painter.save()
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        
        star_size = min(option.rect.width() // 5, option.rect.height())
        radius = star_size // 2
        
        for i in range(5):
            cx = option.rect.x() + i * star_size + star_size // 2
            cy = option.rect.y() + option.rect.height() // 2
            filled = i < rating
            self.draw_star(painter, cx, cy, radius, filled)
        
        painter.restore()

    def draw_star(self, painter, cx, cy, radius, filled):
        outer_radius = radius
        inner_radius = radius * 0.382
        
        points = []
        for i in range(10):
            r = outer_radius if i % 2 == 0 else inner_radius
            angle = i * (pi / 5) - (pi / 2)
            points.append(QPointF(cx + r * cos(angle), cy + r * sin(angle)))
        
        polygon = QPolygonF(points)
        
        if filled:
            painter.setBrush(QColor("#FFD700"))
            painter.setPen(QColor("#B8860B"))
        else:
            painter.setBrush(Qt.BrushStyle.NoBrush)
            painter.setPen(QColor("#555555"))
        
        painter.drawPolygon(polygon)

    def sizeHint(self, option, index):
        return QSize(40 * 5, 40)

    def createEditor(self, parent, option, index):
        # For editing, we can return a custom widget if needed, but here we handle in editorEvent
        return None

    def editorEvent(self, event, model, option, index):
        if event.type() in (event.Type.MouseButtonPress, event.Type.MouseMove):
            star_size = option.rect.width() // 5
            x = event.position().x() - option.rect.x()
            new_rating = max(0, min(int(x / star_size) + 1, 5))
            
            if event.type() == event.Type.MouseButtonPress:
                model.setData(index, new_rating, Qt.ItemDataRole.EditRole)
                return True
            
            # Hover preview (optional: update display temporarily)
            # For simplicity, we only set on click
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
            ["Forrest Gump", 0],  # Unrated
        ]
        self.headers = ["Movie Title", "Rating"]

    def rowCount(self, parent=QModelIndex()):
        return len(self.data_list)

    def columnCount(self, parent=QModelIndex()):
        return 2

    def data(self, index, role=Qt.ItemDataRole.DisplayRole):
        if not index.isValid():
            return None
        row = index.row()
        col = index.column()
        if role in (Qt.ItemDataRole.DisplayRole, Qt.ItemDataRole.EditRole):
            if col == 1:
                return self.data_list[row][1]  # Rating as int
            return self.data_list[row][col]
        return None

    def setData(self, index, value, role=Qt.ItemDataRole.EditRole):
        if index.isValid() and role == Qt.ItemDataRole.EditRole and index.column() == 1:
            self.data_list[index.row()][1] = value
            self.dataChanged.emit(index, index)
            return True
        return False

    def headerData(self, section, orientation, role=Qt.ItemDataRole.DisplayRole):
        if orientation == Qt.Orientation.Horizontal and role == Qt.ItemDataRole.DisplayRole:
            return self.headers[section]
        return super().headerData(section, orientation, role)

    def flags(self, index):
        if index.column() == 1:
            return Qt.ItemFlag.ItemIsEnabled | Qt.ItemFlag.ItemIsEditable
        return Qt.ItemFlag.ItemIsEnabled


class TableApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("PySide6 Table with 5-Star Ratings")
        
        layout = QVBoxLayout(self)
        
        self.table_view = QTableView()
        self.model = RatingTableModel()
        self.table_view.setModel(self.model)
        
        # Set delegate only for rating column
        delegate = StarRatingDelegate(self.table_view)
        self.table_view.setItemDelegateForColumn(1, delegate)
        
        self.table_view.resizeColumnsToContents()
        self.table_view.horizontalHeader().setStretchLastSection(True)
        
        layout.addWidget(self.table_view)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = TableApp()
    window.resize(600, 400)
    window.show()
    sys.exit(app.exec())


