# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'test.ui'
##
## Created by: Qt User Interface Compiler version 6.4.0
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QHBoxLayout, QLabel, QSizePolicy,
    QWidget)

from qfluentwidgets import SpinBox

class Ui_Form(object):
    def setupUi(self, Form):
        if not Form.objectName():
            Form.setObjectName(u"Form")
        Form.resize(263, 552)
        self.widget = QWidget(Form)
        self.widget.setObjectName(u"widget")
        self.widget.setGeometry(QRect(20, 240, 213, 35))
        self.horizontalLayout = QHBoxLayout(self.widget)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.label_font_size = QLabel(self.widget)
        self.label_font_size.setObjectName(u"label_font_size")
        self.label_font_size.setMinimumSize(QSize(92, 16))
        self.label_font_size.setMaximumSize(QSize(92, 16))
        font = QFont()
        font.setFamilies([u"Segoe UI"])
        font.setPointSize(12)
        self.label_font_size.setFont(font)

        self.horizontalLayout.addWidget(self.label_font_size)

        self.spinbox_font_size = SpinBox(self.widget)
        self.spinbox_font_size.setObjectName(u"spinbox_font_size")
        self.spinbox_font_size.setMinimum(5)
        self.spinbox_font_size.setMaximum(12)

        self.horizontalLayout.addWidget(self.spinbox_font_size)


        self.retranslateUi(Form)

        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"Form", None))
        self.label_font_size.setText(QCoreApplication.translate("Form", u"Font size -> ", None))
    # retranslateUi

