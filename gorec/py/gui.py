from PyQt4.QtGui import *
from PyQt4.QtCore import *
from form import Ui_Form

import sys


print "asdf"
app = QApplication(sys.argv)
window = QDialog()
ui = Ui_Form()
ui.setupUi(window)


window.show()
sys.exit(app.exec_())