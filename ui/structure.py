# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'structure.ui'
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
from PySide6.QtWidgets import (QApplication, QGraphicsView, QHBoxLayout, QSizePolicy,
    QSpacerItem, QVBoxLayout, QWidget)

class Ui_Form(object):
    def setupUi(self, Form):
        if not Form.objectName():
            Form.setObjectName(u"Form")
        Form.resize(618, 600)
        self.verticalLayout = QVBoxLayout(Form)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.layout_menu = QHBoxLayout()
        self.layout_menu.setObjectName(u"layout_menu")
        self.layout_settings = QHBoxLayout()
        self.layout_settings.setObjectName(u"layout_settings")

        self.layout_menu.addLayout(self.layout_settings)

        self.spacer_menu = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.layout_menu.addItem(self.spacer_menu)

        self.layou_tools = QHBoxLayout()
        self.layou_tools.setObjectName(u"layou_tools")

        self.layout_menu.addLayout(self.layou_tools)


        self.verticalLayout.addLayout(self.layout_menu)

        self.layout_graphics = QHBoxLayout()
        self.layout_graphics.setObjectName(u"layout_graphics")
        self.graphics_view = QGraphicsView(Form)
        self.graphics_view.setObjectName(u"graphics_view")

        self.layout_graphics.addWidget(self.graphics_view)

        self.layout_graphics_tools = QVBoxLayout()
        self.layout_graphics_tools.setObjectName(u"layout_graphics_tools")

        self.layout_graphics.addLayout(self.layout_graphics_tools)


        self.verticalLayout.addLayout(self.layout_graphics)


        self.retranslateUi(Form)

        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"Form", None))
    # retranslateUi

