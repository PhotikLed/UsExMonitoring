# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'cpu_monitoring.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(937, 649)
        self.verticalLayout = QtWidgets.QVBoxLayout(Form)
        self.verticalLayout.setObjectName("verticalLayout")
        self.label = QtWidgets.QLabel(Form)
        font = QtGui.QFont()
        font.setPointSize(11)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.verticalLayout.addWidget(self.label)
        self.CPU_graphicsView = PlotWidget(Form)
        self.CPU_graphicsView.setObjectName("CPU_graphicsView")
        self.verticalLayout.addWidget(self.CPU_graphicsView)
        self.label_2 = QtWidgets.QLabel(Form)
        font = QtGui.QFont()
        font.setPointSize(11)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        self.verticalLayout.addWidget(self.label_2)
        self.GPU_graphicsView = PlotWidget(Form)
        self.GPU_graphicsView.setObjectName("GPU_graphicsView")
        self.verticalLayout.addWidget(self.GPU_graphicsView)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Мониторинг температур процессора и видеокарты"))
        self.label.setText(_translate("Form", "Температура процессора"))
        self.label_2.setText(_translate("Form", "Температутра видеокарты"))
from pyqtgraph import PlotWidget
