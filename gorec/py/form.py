# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'form.ui'
#
# Created: Wed Jan 30 08:47:27 2013
#      by: PyQt4 UI code generator 4.9.6
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui
from model import *
from datetime import timedelta, datetime


try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName(_fromUtf8("Form"))
        Form.setWindowModality(QtCore.Qt.WindowModal)
        Form.resize(917, 487)
        self.lineEdit = QtGui.QLineEdit(Form)
        self.lineEdit.setGeometry(QtCore.QRect(20, 290, 301, 21))
        self.lineEdit.setObjectName(_fromUtf8("lineEdit"))
        self.listWidget = QtGui.QListWidget(Form)
        self.listWidget.setGeometry(QtCore.QRect(20, 10, 191, 231))
        self.listWidget.setObjectName(_fromUtf8("listWidget"))
        self.pushButton = QtGui.QPushButton(Form)
        self.pushButton.setGeometry(QtCore.QRect(340, 290, 75, 23))
        self.pushButton.setObjectName(_fromUtf8("pushButton"))
        self.tableWidget = QtGui.QTableWidget(Form)
        self.tableWidget.setGeometry(QtCore.QRect(230, 10, 621, 231))
        self.tableWidget.setObjectName(_fromUtf8("tableWidget"))
        self.tableWidget.setColumnCount(6)
        self.tableWidget.setRowCount(0)
        item = QtGui.QTableWidgetItem()
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Monaco"))
        font.setPointSize(9)
        item.setFont(font)
        self.tableWidget.setHorizontalHeaderItem(0, item)
        item = QtGui.QTableWidgetItem()
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Monaco"))
        font.setPointSize(9)
        item.setFont(font)
        self.tableWidget.setHorizontalHeaderItem(1, item)
        item = QtGui.QTableWidgetItem()
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Monaco"))
        font.setPointSize(9)
        item.setFont(font)
        self.tableWidget.setHorizontalHeaderItem(2, item)
        item = QtGui.QTableWidgetItem()
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Monaco"))
        font.setPointSize(9)
        item.setFont(font)
        self.tableWidget.setHorizontalHeaderItem(3, item)
        item = QtGui.QTableWidgetItem()
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Monaco"))
        font.setPointSize(9)
        item.setFont(font)
        self.tableWidget.setHorizontalHeaderItem(4, item)
        item = QtGui.QTableWidgetItem()
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Monaco"))
        font.setPointSize(9)
        item.setFont(font)
        self.tableWidget.setHorizontalHeaderItem(5, item)
        self.pushButton_2 = QtGui.QPushButton(Form)
        self.pushButton_2.setGeometry(QtCore.QRect(440, 290, 75, 23))
        self.pushButton_2.setObjectName(_fromUtf8("pushButton_2"))
        self.pushButton_3 = QtGui.QPushButton(Form)
        self.pushButton_3.setGeometry(QtCore.QRect(540, 290, 75, 23))
        self.pushButton_3.setObjectName(_fromUtf8("pushButton_3"))

        self.retranslateUi(Form)
        QtCore.QObject.connect(self.pushButton, QtCore.SIGNAL(_fromUtf8("clicked()")), self.listWidget.clear)
        QtCore.QObject.connect(self.lineEdit, QtCore.SIGNAL(_fromUtf8("editingFinished()")), self.additem)

        #self.listWidget.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        #self.listWidget.connect(self.listWidget, QtCore.SIGNAL("CustomContextMenuRequested(QPoint)"), self.onContext)

        #QtCore.QObject.connect(self.pushButton_2, QtCore.SIGNAL(_fromUtf8("released()")), self.tableWidget.clearSelection)
        QtCore.QObject.connect(self.pushButton_2, QtCore.SIGNAL(_fromUtf8("released()")), self.addrow2tab)
        QtCore.QObject.connect(self.pushButton_3, QtCore.SIGNAL(_fromUtf8("released()")), self.addrow2tab)
        QtCore.QObject.connect(self.tableWidget, QtCore.SIGNAL(_fromUtf8("currentCellChanged(int,int,int,int)")), self.update2db)

        QtCore.QMetaObject.connectSlotsByName(Form)


    def getdatetimenow(self):
        td = timedelta(hours = 8)
        return datetime.datetime.utcnow() + td


    def retranslateUi(self, Form):
        Form.setWindowTitle(_translate("Form", "Form", None))
        self.pushButton.setText(_translate("Form", "X", None))
        item = self.tableWidget.horizontalHeaderItem(0)
        item.setText(_translate("Form", "id", None))
        item = self.tableWidget.horizontalHeaderItem(1)
        item.setText(_translate("Form", "name", None))
        item = self.tableWidget.horizontalHeaderItem(2)
        item.setText(_translate("Form", "person", None))
        item = self.tableWidget.horizontalHeaderItem(3)
        item.setText(_translate("Form", "unit", None))
        item = self.tableWidget.horizontalHeaderItem(4)
        item.setText(_translate("Form", "Qty", None))
        item = self.tableWidget.horizontalHeaderItem(5)
        item.setText(_translate("Form", "date", None))
        self.pushButton_2.setText(_translate("Form", "Insert", None))
        self.pushButton_3.setText(_translate("Form", "Update", None))


    def additem(self):
        self.listWidget.addItem(self.lineEdit.text())

    def onContext(self):
        menu = QtGui.QMenu("Menu", self)
        menu.addAction("Inert")
        menu.exec_(self.view.mapToGlobal(point))

    def addrow2tab(self):
        self.tableWidget.insertRow(self.tableWidget.rowCount())
        

        recdb = Testdb()
        seqid = str(recdb.getCurrSequence())
        print seqid
        item = QtGui.QTableWidgetItem(seqid)
        self.tableWidget.setItem(self.tableWidget.rowCount() - 1, 0, item)

        item = QtGui.QTableWidgetItem()

    def update2db(self, row, col, orow, ocol):
        if row == orow:
            return

        itemid = self.tableWidget.item(orow, 0)

        recdb = Testdb()
        recdb.upserRecord()

