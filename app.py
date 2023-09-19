from PyQt6.QtCore import QSize, Qt, pyqtSignal
from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, QTableWidget, QTableWidgetItem, QHBoxLayout, QWidget, QPlainTextEdit, QVBoxLayout, QFileDialog

import sys

'''If want to add changable number of inputs, use 
for i in range(1, 15):
    getattr(self, 'lineEdit_%s' % i).setReadOnly(True)

addition
continue from this link https://stackoverflow.com/questions/68453805/how-to-pass-values-from-one-window-to-another-pyqt
'''

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
        #self.currentRow.connect(self.updateText)

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
        
        self.table.insertRow(self.table.rowCount())
        self.table.setItem(index, 0, QTableWidgetItem(self.textInput.toPlainText().replace(",", "")))
        self.table.setItem(index, 1, QTableWidgetItem(self.textOutput.toPlainText().replace(",", "")))
        
        self.editButton = QPushButton('Edit')
        self.editButton.clicked.connect(self.editButtonClicked)
        self.table.setCellWidget(index,2,self.editButton)

        self.deleteButton = QPushButton('Delete')
        self.deleteButton.clicked.connect(self.deleteButtonClicked)
        self.table.setCellWidget(index,3,self.deleteButton)

        self.textInput.setPlainText("")
        self.textOutput.setPlainText("")

    def updateTableText(self, text):
        self.table.setItem(text[2], 0, QTableWidgetItem(text[0].replace(",", "")))
        self.table.setItem(text[2], 1, QTableWidgetItem(text[1].replace(",", "")))
        self.w.close()

    def makeCSV(self):
        fileName = QFileDialog.getSaveFileName(self, 'Save file', 'c:\\Documents',"CSV file (*.csv)")
        try:
            f = open(fileName[0], 'w')
            for index in range(self.table.rowCount()):
                f.write(self.table.item(index, 0).text() + "," + self.table.item(index, 1).text() + "\n")
            f.close()
            print("file written at", fileName)
        except:
            pass

    def openFile(self):
        fileName = QFileDialog.getOpenFileName(self, 'Open file', 'c:\\Documents','CSV file (*.csv)')
        while self.table.rowCount() > 0:
            self.table.removeRow(0)

        f = open(fileName[0], 'r')
        for index, row in enumerate(f):
            self.table.insertRow(self.table.rowCount())
            entries = row.split(",")
            self.table.setItem(index, 0, QTableWidgetItem(entries[0].replace(",", "")))
            self.table.setItem(index, 1, QTableWidgetItem(entries[1].replace("," or "\n", "")))
        f.close()
        

# Remove the sys and sys.argv replace [] if I dont end up using CLA
app = QApplication(sys.argv)

window = MainWindow()
window.show()

app.exec()