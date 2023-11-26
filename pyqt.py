import sys
from PyQt5 import QtWidgets
import design

class ExampleApp(QtWidgets.QMainWindow,  design.Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.button = QtWidgets.QPushButton("pushButton", self)
        self.pushButton.clicked.connect(self.hello)

    def hello(self):
        print("Hello")




app = QtWidgets.QApplication(sys.argv)
window = ExampleApp()
window.show()
app.exec_()