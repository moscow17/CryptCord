Nimport os
import sys
from PyQt5 import QtWidgets, uic

from src.decoration import Application
from src.protocol import make_key

make_key()

app = QtWidgets.QApplication(sys.argv)
main = Application()
app.exec_()
