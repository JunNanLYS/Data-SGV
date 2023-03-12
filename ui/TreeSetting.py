# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'TreeSetting.ui'
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

from src.MyClass.MyWidget import (IconButton, MyScrollArea, ScrollAreaWidget, StyleButton,
                                  StyleSlider)
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
        self.layoutWidget = QWidget(self.scroll_widget)
        self.layoutWidget.setObjectName(u"layoutWidget")
        self.layoutWidget.setGeometry(QRect(20, 20, 191, 181))
        self.verticalLayout_5 = QVBoxLayout(self.layoutWidget)
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.button_close = IconButton(self.layoutWidget)
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

        self.label_setting = QLabel(self.layoutWidget)
        self.label_setting.setObjectName(u"label_setting")
        self.label_setting.setAlignment(Qt.AlignCenter)

        self.horizontalLayout.addWidget(self.label_setting)

        self.verticalLayout_5.addLayout(self.horizontalLayout)

        self.verticalLayout_3 = QVBoxLayout()
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.label_theme = QLabel(self.layoutWidget)
        self.label_theme.setObjectName(u"label_theme")
        self.label_theme.setAlignment(Qt.AlignCenter)

        self.verticalLayout_3.addWidget(self.label_theme)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.button_theme_white = QRadioButton(self.layoutWidget)
        self.button_theme_white.setObjectName(u"button_theme_white")

        self.horizontalLayout_2.addWidget(self.button_theme_white)

        self.button_theme_dark = QRadioButton(self.layoutWidget)
        self.button_theme_dark.setObjectName(u"button_theme_dark")
        self.button_theme_dark.setCheckable(True)
        self.button_theme_dark.setAutoRepeat(False)

        self.horizontalLayout_2.addWidget(self.button_theme_dark)

        self.verticalLayout_3.addLayout(self.horizontalLayout_2)

        self.verticalLayout_5.addLayout(self.verticalLayout_3)

        self.verticalLayout_2 = QVBoxLayout()
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.label_animation = QLabel(self.layoutWidget)
        self.label_animation.setObjectName(u"label_animation")
        self.label_animation.setAlignment(Qt.AlignCenter)

        self.verticalLayout_2.addWidget(self.label_animation)

        self.slider_animation = StyleSlider(self.layoutWidget)
        self.slider_animation.setObjectName(u"slider_animation")
        self.slider_animation.setOrientation(Qt.Horizontal)

        self.verticalLayout_2.addWidget(self.slider_animation)

        self.verticalLayout_5.addLayout(self.verticalLayout_2)

        self.layoutWidget1 = QWidget(self.scroll_widget)
        self.layoutWidget1.setObjectName(u"layoutWidget1")
        self.layoutWidget1.setGeometry(QRect(20, 210, 191, 71))
        self.verticalLayout = QVBoxLayout(self.layoutWidget1)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.label = QLabel(self.layoutWidget1)
        self.label.setObjectName(u"label")
        self.label.setAlignment(Qt.AlignCenter)

        self.verticalLayout.addWidget(self.label)

        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.radioButton = QRadioButton(self.layoutWidget1)
        self.radioButton.setObjectName(u"radioButton")

        self.horizontalLayout_3.addWidget(self.radioButton)

        self.radioButton_2 = QRadioButton(self.layoutWidget1)
        self.radioButton_2.setObjectName(u"radioButton_2")

        self.horizontalLayout_3.addWidget(self.radioButton_2)

        self.radioButton_3 = QRadioButton(self.layoutWidget1)
        self.radioButton_3.setObjectName(u"radioButton_3")
        self.radioButton_3.setAutoRepeat(True)

        self.horizontalLayout_3.addWidget(self.radioButton_3)

        self.verticalLayout.addLayout(self.horizontalLayout_3)

        self.button_avl = StyleButton(self.scroll_widget)
        self.button_avl.setObjectName(u"button_avl")
        self.button_avl.setGeometry(QRect(10, 590, 211, 81))
        self.button_avl.setCheckable(True)
        self.button_avl.setChecked(False)
        self.button_avl.setAutoRepeat(False)
        self.button_avl.setAutoExclusive(True)
        self.button_search_tree = StyleButton(self.scroll_widget)
        self.button_search_tree.setObjectName(u"button_search_tree")
        self.button_search_tree.setGeometry(QRect(10, 460, 211, 81))
        self.button_search_tree.setCheckable(True)
        self.button_search_tree.setChecked(False)
        self.button_search_tree.setAutoRepeat(False)
        self.button_search_tree.setAutoExclusive(True)
        self.button_tree = StyleButton(self.scroll_widget)
        self.button_tree.setObjectName(u"button_tree")
        self.button_tree.setGeometry(QRect(10, 330, 211, 71))
        self.button_tree.setCheckable(True)
        self.button_tree.setChecked(True)
        self.button_tree.setAutoRepeat(False)
        self.button_tree.setAutoExclusive(True)
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
        self.label.setText(QCoreApplication.translate("Form", u"Node Color", None))
        self.radioButton.setText(QCoreApplication.translate("Form", u"\u84dd\u8272", None))
        self.radioButton_2.setText(QCoreApplication.translate("Form", u"\u9ec4\u8272", None))
        self.radioButton_3.setText(QCoreApplication.translate("Form", u"\u9ed1\u8272", None))
        self.button_avl.setText(QCoreApplication.translate("Form", u"AVL", None))
        self.button_search_tree.setText(QCoreApplication.translate("Form", u"SearchTree", None))
        self.button_tree.setText(QCoreApplication.translate("Form", u"Tree", None))
    # retranslateUi
