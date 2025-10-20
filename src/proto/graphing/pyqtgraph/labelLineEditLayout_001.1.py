import sys
from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit

# Create the main application window
app = QApplication(sys.argv)
window = QWidget()
window.setWindowTitle("Label and LineEdit Example")

# Create the main vertical layout
main_layout = QVBoxLayout()

# Create a horizontal layout for label and line edit
h_layout = QHBoxLayout()
label = QLabel("Name:")
line_edit = QLineEdit()
line_edit.setPlaceholderText("Enter your name")

# Add widgets to the horizontal layout
h_layout.addWidget(label)
h_layout.addWidget(line_edit)

# Add the horizontal layout to the vertical layout
main_layout.addLayout(h_layout)

# Set the layout on the main window
window.setLayout(main_layout)
window.show()

sys.exit(app.exec())   

