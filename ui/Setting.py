# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'Setting.ui'
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
from PySide6.QtWidgets import (QApplication, QFrame, QHBoxLayout, QLabel,
                               QRadioButton, QSizePolicy, QVBoxLayout, QWidget)

from src.MyClass.MyWidget import (MyScrollArea, ScrollAreaWidget, StyleButton, StyleSlider)
from res import resource_rc


class Ui_Form(object):
    def setupUi(self, Form):
        if not Form.objectName():
            Form.setObjectName(u"Form")
        Form.resize(250, 800)
        Form.setMinimumSize(QSize(250, 800))
        Form.setStyleSheet(u"")
        self.verticalLayout_4 = QVBoxLayout(Form)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.scrollArea = MyScrollArea(Form)
        self.scrollArea.setObjectName(u"scrollArea")
        self.scrollArea.setFocusPolicy(Qt.NoFocus)
        self.scrollArea.setStyleSheet(u"")
        self.scrollArea.setFrameShape(QFrame.NoFrame)
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setAlignment(Qt.AlignLeading | Qt.AlignLeft | Qt.AlignVCenter)
        self.scroll_widget = ScrollAreaWidget()
        self.scroll_widget.setObjectName(u"scroll_widget")
        self.scroll_widget.setGeometry(QRect(0, 0, 232, 782))
        self.widget = QWidget(self.scroll_widget)
        self.widget.setObjectName(u"widget")
        self.widget.setGeometry(QRect(20, 30, 201, 51))
        self.horizontalLayout = QHBoxLayout(self.widget)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.button_close = StyleButton(self.widget)
        self.button_close.setObjectName(u"button_close")
        self.button_close.setMinimumSize(QSize(31, 31))
        self.button_close.setFocusPolicy(Qt.ClickFocus)
        self.button_close.setStyleSheet(u"QPushButton {\n"
                                        "image: url(:/icon/icons/back.png);\n"
                                        "border-radius:1px;\n"
                                        "background-color:rgb(245, 245, 245);\n"
                                        "}\n"
                                        "QPushButton:hover{\n"
                                        "background-color:#ecf5ff;\n"
                                        "border-style:solid;\n"
                                        "border-width:1px;\n"
                                        "border-color:#409eff;\n"
                                        "}\n"
                                        "QPushButton:pressed{\n"
                                        "margin:2px;\n"
                                        "}")
        self.button_close.setIconSize(QSize(16, 16))

        self.horizontalLayout.addWidget(self.button_close)

        self.label_setting = QLabel(self.widget)
        self.label_setting.setObjectName(u"label_setting")
        self.label_setting.setAlignment(Qt.AlignCenter)

        self.horizontalLayout.addWidget(self.label_setting)

        self.widget1 = QWidget(self.scroll_widget)
        self.widget1.setObjectName(u"widget1")
        self.widget1.setGeometry(QRect(20, 160, 191, 61))
        self.verticalLayout_3 = QVBoxLayout(self.widget1)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.label_theme = QLabel(self.widget1)
        self.label_theme.setObjectName(u"label_theme")
        self.label_theme.setAlignment(Qt.AlignCenter)

        self.verticalLayout_3.addWidget(self.label_theme)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.button_theme_white = QRadioButton(self.widget1)
        self.button_theme_white.setObjectName(u"button_theme_white")

        self.horizontalLayout_2.addWidget(self.button_theme_white)

        self.button_theme_dark = QRadioButton(self.widget1)
        self.button_theme_dark.setObjectName(u"button_theme_dark")

        self.horizontalLayout_2.addWidget(self.button_theme_dark)

        self.verticalLayout_3.addLayout(self.horizontalLayout_2)

        self.widget2 = QWidget(self.scroll_widget)
        self.widget2.setObjectName(u"widget2")
        self.widget2.setGeometry(QRect(20, 350, 191, 91))
        self.verticalLayout_2 = QVBoxLayout(self.widget2)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.label_animation = QLabel(self.widget2)
        self.label_animation.setObjectName(u"label_animation")
        self.label_animation.setAlignment(Qt.AlignCenter)

        self.verticalLayout_2.addWidget(self.label_animation)

        self.slider_animation = StyleSlider(self.widget2)
        self.slider_animation.setObjectName(u"slider_animation")
        self.slider_animation.setMinimumSize(QSize(0, 21))
        self.slider_animation.setOrientation(Qt.Horizontal)

        self.verticalLayout_2.addWidget(self.slider_animation)

        self.scrollArea.setWidget(self.scroll_widget)

        self.verticalLayout_4.addWidget(self.scrollArea)

        self.retranslateUi(Form)

        QMetaObject.connectSlotsByName(Form)

    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"Form", None))
        self.button_close.setText("")
        self.label_setting.setText(QCoreApplication.translate("Form", u"Setting", None))
        self.label_theme.setText(QCoreApplication.translate("Form", u"Theme", None))
        self.button_theme_white.setText(QCoreApplication.translate("Form", u"white", None))
        self.button_theme_dark.setText(QCoreApplication.translate("Form", u"dark", None))
        self.label_animation.setText(QCoreApplication.translate("Form", u"Animation speed", None))
    # retranslateUi
