from PyQt6.QtCore import QSize, Qt
from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton

import sys

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("My App")

        self.button = QPushButton("Press Me!")
        self.button.setCheckable(True)
        self.button.clicked.connect(self.the_button_was_clicked)
        self.button.clicked.connect(self.the_button_was_toggled)

        self.setMinimumSize(QSize(400, 300))

        self.setCentralWidget(self.button)

    def the_button_was_clicked(self):
        print("Clicked!")

    def the_button_was_toggled(self, checked):
        self.button.setText("You clicked me")
        self.button.setEnabled(False)
        self.button_is_checked = checked
        
        print(self.button_is_checked)

# Remove the sys and sys.argv replace [] if I dont end up using CLA
app = QApplication(sys.argv)

window = MainWindow()
window.show()

app.exec()