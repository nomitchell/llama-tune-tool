from PyQt6.QtCore import QSize, Qt, pyqtSignal
from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, QTableWidget, QTableWidgetItem, QHBoxLayout, QWidget, QPlainTextEdit, QVBoxLayout, QFileDialog

class editWindow(QWidget):
    
    confirmClicked = pyqtSignal(list)

    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        layout = QVBoxLayout()
        self.editInput = QPlainTextEdit()
        self.editOutput = QPlainTextEdit()
        self.editInput.setPlainText(self.parent.table.item(self.parent.currentRow, 0).text())
        self.editOutput.setPlainText(self.parent.table.item(self.parent.currentRow, 1).text())
        print(self.parent.table.item(self.parent.currentRow, 0).text())

        self.confirmButton = QPushButton('Confirm')
        self.confirmButton.clicked.connect(self.updateText)
        layout.addWidget(self.editInput)
        layout.addWidget(self.editOutput)
        layout.addWidget(self.confirmButton)
        self.setLayout(layout)

    def updateText(self, instance):
        self.confirmClicked.emit([self.editInput.toPlainText(), self.editOutput.toPlainText(), self.parent.currentRow])
        

class MainWindow(QMainWindow):
    
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Llama Fine Tune Tool")
        self.setMinimumSize(1000, 300)
    
        layout = QHBoxLayout()
        layout2 = QVBoxLayout()
        layout3 = QHBoxLayout()

        self.table = QTableWidget()
        self.table.setMinimumWidth(350)
        self.table.setColumnCount(4)
        self.table.setSelectionMode(QTableWidget.SelectionMode.NoSelection)
        self.table.setRowCount(0)

        self.textInput = QPlainTextEdit()
        self.textOutput = QPlainTextEdit()

        self.appendButton = QPushButton('Append')
        self.appendButton.clicked.connect(self.getText)
        self.appendButton.setMinimumHeight(50)

        self.submitButton = QPushButton('Save')
        self.submitButton.clicked.connect(self.makeCSV)
        self.submitButton.setMinimumHeight(30)

        self.openButton = QPushButton('Open')
        self.openButton.clicked.connect(self.openFile)
        self.openButton.setMinimumHeight(30)

        self.editButton = QPushButton('Edit')
        self.editButton.clicked.connect(self.editButtonClicked)

        self.deleteButton = QPushButton('Delete')
        self.deleteButton.clicked.connect(self.deleteButtonClicked)

        layout.addWidget(self.table)
        layout.addLayout(layout2)

        layout2.addWidget(self.textInput)
        layout2.addWidget(self.textOutput)
        layout2.addWidget(self.appendButton)
        layout2.addLayout(layout3)

        layout3.addWidget(self.submitButton)
        layout3.addWidget(self.openButton)
        
        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)

    def editButtonClicked(self):
        self.currentRow = self.table.currentRow()
        self.w = editWindow(parent=self)
        self.w.confirmClicked.connect(self.updateTableText)
        self.w.show()

    def deleteButtonClicked(self):
        self.table.removeRow(self.table.currentRow())

    def getText(self):
        index = self.table.rowCount()
        
        inputText = self.textInput.toPlainText().replace(",", "").replace("\n", " ")
        outputText = self.textOutput.toPlainText().replace(",", "").replace("\n", " ")

        self.table.insertRow(self.table.rowCount())
        self.table.setItem(index, 0, QTableWidgetItem(inputText))
        self.table.setItem(index, 1, QTableWidgetItem(outputText))
        
        self.editButton = QPushButton('Edit')
        self.editButton.clicked.connect(self.editButtonClicked)
        self.table.setCellWidget(index,2,self.editButton)

        self.deleteButton = QPushButton('Delete')
        self.deleteButton.clicked.connect(self.deleteButtonClicked)
        self.table.setCellWidget(index,3,self.deleteButton)

        self.textInput.setPlainText("")
        self.textOutput.setPlainText("")

    def updateTableText(self, text):
        inputText = text[0].replace(",", "").replace('\n', ' ')
        outputText = text[1].replace(",", "").replace('\n', ' ')
        
        self.table.setItem(text[2], 0, QTableWidgetItem(text[0].replace(",", "")))
        self.table.setItem(text[2], 1, QTableWidgetItem(text[1].replace(",", "")))
        self.w.close()

    def makeCSV(self):
        fileName = QFileDialog.getSaveFileName(self, 'Save file', 'c:\\',"CSV file (*.csv)")
        try:
            f = open(fileName[0], 'w')
            for index in range(self.table.rowCount()):
                f.write(self.table.item(index, 0).text() + "," + self.table.item(index, 1).text() + "\n")
            f.close()
            print("file written at", fileName)
        except:
            pass

    def openFile(self):
        try:
            fileName = QFileDialog.getOpenFileName(self, 'Open file', 'c:\\','CSV file (*.csv)')
            while self.table.rowCount() > 0:
                self.table.removeRow(0)

            f = open(fileName[0], 'r')
            for index, row in enumerate(f):
                self.table.insertRow(self.table.rowCount())
                entries = row.split(",")
                print(entries)
                entries[0] = entries[0].replace('\n', ' ').replace(',', '')
                entries[1] = entries[1].replace('\n', ' ').replace(',', '')
                print(entries)

                self.table.setItem(index, 0, QTableWidgetItem(entries[0]))
                self.table.setItem(index, 1, QTableWidgetItem(entries[1]))
            
                self.editButton = QPushButton('Edit')
                self.editButton.clicked.connect(self.editButtonClicked)
                self.table.setCellWidget(index,2,self.editButton)

                self.deleteButton = QPushButton('Delete')
                self.deleteButton.clicked.connect(self.deleteButtonClicked)
                self.table.setCellWidget(index,3,self.deleteButton)

            f.close()
        except:
            pass
        

app = QApplication([])

window = MainWindow()
window.show()

app.exec()