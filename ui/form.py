# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'form.ui'
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
from PySide6.QtWidgets import (QApplication, QSizePolicy, QWidget)

from qfluentwidgets import (ComboBox, DateTimeEdit, IndeterminateProgressBar, LineEdit, ProgressBar, ProgressRing,
                            PushButton,
                            RadioButton, SearchLineEdit, SplitPushButton, SwitchButton)


class Ui_Form(object):
    def setupUi(self, Form):
        if not Form.objectName():
            Form.setObjectName(u"Form")
        Form.resize(534, 433)
        self.DateTimeEdit = DateTimeEdit(Form)
        self.DateTimeEdit.setObjectName(u"DateTimeEdit")
        self.DateTimeEdit.setGeometry(QRect(10, 10, 206, 33))
        self.SearchLineEdit = SearchLineEdit(Form)
        self.SearchLineEdit.setObjectName(u"SearchLineEdit")
        self.SearchLineEdit.setGeometry(QRect(120, 100, 187, 33))
        self.ProgressRing = ProgressRing(Form)
        self.ProgressRing.setObjectName(u"ProgressRing")
        self.ProgressRing.setGeometry(QRect(360, 90, 100, 100))
        self.ProgressRing.setMinimum(50)
        self.ProgressRing.setTextVisible(True)
        self.ProgressRing.setInvertedAppearance(False)
        self.IndeterminateProgressBar = IndeterminateProgressBar(Form)
        self.IndeterminateProgressBar.setObjectName(u"IndeterminateProgressBar")
        self.IndeterminateProgressBar.setGeometry(QRect(160, 250, 87, 4))
        self.SwitchButton = SwitchButton(Form)
        self.SwitchButton.setObjectName(u"SwitchButton")
        self.SwitchButton.setGeometry(QRect(30, 280, 76, 37))
        self.RadioButton = RadioButton(Form)
        self.RadioButton.setObjectName(u"RadioButton")
        self.RadioButton.setGeometry(QRect(30, 360, 113, 24))
        self.SplitPushButton = SplitPushButton(Form)
        self.SplitPushButton.setObjectName(u"SplitPushButton")
        self.SplitPushButton.setGeometry(QRect(200, 370, 164, 32))
        self.PushButton = PushButton(Form)
        self.PushButton.setObjectName(u"PushButton")
        self.PushButton.setGeometry(QRect(30, 160, 102, 32))
        self.ComboBox = ComboBox(Form)
        self.ComboBox.setObjectName(u"ComboBox")
        self.ComboBox.setGeometry(QRect(400, 260, 77, 32))

        self.retranslateUi(Form)

        QMetaObject.connectSlotsByName(Form)

    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"Form", None))
        self.RadioButton.setText(QCoreApplication.translate("Form", u"Radio button", None))
        self.SplitPushButton.setProperty("text_", QCoreApplication.translate("Form", u"Split push button", None))
        self.PushButton.setText(QCoreApplication.translate("Form", u"Push button", None))
    # retranslateUi
