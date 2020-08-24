# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'list.ui',
# licensing of 'list.ui' applies.
#
# Created: Mon Aug 24 23:34:14 2020
#      by: pyside2-uic  running on PySide2 5.13.2
#
# WARNING! All changes made in this file will be lost!

from PySide2 import QtCore, QtGui, QtWidgets

class Ui_ListWindow(object):
    def setupUi(self, ListWindow):
        ListWindow.setObjectName("ListWindow")
        ListWindow.resize(200, 310)
        ListWindow.setMinimumSize(QtCore.QSize(200, 310))
        self.verticalLayout = QtWidgets.QVBoxLayout(ListWindow)
        self.verticalLayout.setObjectName("verticalLayout")
        self.labelList = QtWidgets.QLabel(ListWindow)
        self.labelList.setMinimumSize(QtCore.QSize(0, 20))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.labelList.setFont(font)
        self.labelList.setObjectName("labelList")
        self.verticalLayout.addWidget(self.labelList)
        self.line = QtWidgets.QFrame(ListWindow)
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.verticalLayout.addWidget(self.line)
        self.textBrowserList = QtWidgets.QTextBrowser(ListWindow)
        self.textBrowserList.setMinimumSize(QtCore.QSize(182, 256))
        self.textBrowserList.setObjectName("textBrowserList")
        self.verticalLayout.addWidget(self.textBrowserList)

        self.retranslateUi(ListWindow)
        QtCore.QMetaObject.connectSlotsByName(ListWindow)

    def retranslateUi(self, ListWindow):
        ListWindow.setWindowTitle(QtWidgets.QApplication.translate("ListWindow", "List", None, -1))
        self.labelList.setText(QtWidgets.QApplication.translate("ListWindow", "<html><head/><body><p>List</p></body></html>", None, -1))
        self.textBrowserList.setHtml(QtWidgets.QApplication.translate("ListWindow", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'SimSun\'; font-size:9pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'SimSun\';\">Current pick list</span></p></body></html>", None, -1))

