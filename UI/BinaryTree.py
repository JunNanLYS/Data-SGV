# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'BinaryTree.ui'
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
from PySide6.QtWidgets import (QApplication, QHBoxLayout, QLabel, QMainWindow,
                               QPushButton, QSizePolicy, QSpacerItem, QVBoxLayout,
                               QWidget)

from DataStructView.Class.MyWidget import MyWidget
from DataStructView.Buildinin.TreeView import TreeView
from DataStructView.res import resource_rc


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(1000, 800)
        MainWindow.setMinimumSize(QSize(1000, 800))
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        MainWindow.setWindowFlag(Qt.FramelessWindowHint)
        MainWindow.setAttribute(Qt.WA_TranslucentBackground)
        self.widget = MyWidget(self.centralwidget)
        self.widget.setObjectName(u"widget")
        self.widget.setGeometry(QRect(0, 0, 1000, 800))
        self.widget.setMinimumSize(QSize(1000, 800))
        self.widget.setStyleSheet(u"background-color: rgb(245, 245, 245);\n"
                                  "border-radius:15px;")
        self.verticalLayout_2 = QVBoxLayout(self.widget)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.button_setting = QPushButton(self.widget)
        self.button_setting.setObjectName(u"button_setting")
        self.button_setting.setMinimumSize(QSize(41, 41))
        self.button_setting.setStyleSheet(u"image: url(:/icon/icons/setting.png);\n"
                                          "border:none;")

        self.horizontalLayout.addWidget(self.button_setting)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer)

        self.button_enlarge = QPushButton(self.widget)
        self.button_enlarge.setObjectName(u"button_enlarge")
        self.button_enlarge.setMinimumSize(QSize(41, 41))
        self.button_enlarge.setStyleSheet(u"image: url(:/icon/icons/enlarge.png);\n"
                                          "border:none;")

        self.horizontalLayout.addWidget(self.button_enlarge)

        self.button_colose = QPushButton(self.widget)
        self.button_colose.setObjectName(u"button_colose")
        self.button_colose.setMinimumSize(QSize(41, 41))
        self.button_colose.setStyleSheet(u"image: url(:/icon/icons/close.png);\n"
                                         "border:none;")

        self.horizontalLayout.addWidget(self.button_colose)

        self.verticalLayout_2.addLayout(self.horizontalLayout)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.graphicsView = TreeView(self.widget)
        self.graphicsView.setObjectName(u"graphicsView")
        self.graphicsView.setMinimumSize(QSize(740, 720))
        self.graphicsView.setStyleSheet(u"\n"
                                        "border-radius: 20px;\n"
                                        "background-color: rgb(255, 255, 255);")

        self.horizontalLayout_2.addWidget(self.graphicsView)

        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.label_tree = QLabel(self.widget)
        self.label_tree.setObjectName(u"label_tree")
        font = QFont()
        font.setPointSize(20)
        font.setBold(True)
        self.label_tree.setFont(font)
        self.label_tree.setAlignment(Qt.AlignCenter)

        self.verticalLayout.addWidget(self.label_tree)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout.addItem(self.verticalSpacer)

        self.button_preorder = QPushButton(self.widget)
        self.button_preorder.setObjectName(u"button_preorder")
        self.button_preorder.setMinimumSize(QSize(210, 70))
        font1 = QFont()
        font1.setFamilies([u"Modern No. 20"])
        font1.setPointSize(20)
        font1.setBold(False)
        font1.setItalic(False)
        self.button_preorder.setFont(font1)
        self.button_preorder.setStyleSheet(u"QPushButton{\n"
                                           "	background-color: rgb(255, 255, 255);\n"
                                           "	border-radius:10px;\n"
                                           "}\n"
                                           "\n"
                                           "QPushButton:hover {\n"
                                           "	background-color: rgb(250, 250, 250);\n"
                                           "}")

        self.verticalLayout.addWidget(self.button_preorder)

        self.button_inorder = QPushButton(self.widget)
        self.button_inorder.setObjectName(u"button_inorder")
        self.button_inorder.setMinimumSize(QSize(210, 70))
        font2 = QFont()
        font2.setFamilies([u"Modern No. 20"])
        font2.setPointSize(20)
        font2.setBold(False)
        self.button_inorder.setFont(font2)
        self.button_inorder.setStyleSheet(u"QPushButton{\n"
                                          "	background-color: rgb(255, 255, 255);\n"
                                          "	border-radius:10px;\n"
                                          "}\n"
                                          "\n"
                                          "QPushButton:hover {\n"
                                          "	background-color: rgb(250, 250, 250);\n"
                                          "}")

        self.verticalLayout.addWidget(self.button_inorder)

        self.button_postorder = QPushButton(self.widget)
        self.button_postorder.setObjectName(u"button_postorder")
        self.button_postorder.setMinimumSize(QSize(210, 70))
        self.button_postorder.setFont(font2)
        self.button_postorder.setStyleSheet(u"QPushButton{\n"
                                            "	background-color: rgb(255, 255, 255);\n"
                                            "	border-radius:10px;\n"
                                            "}\n"
                                            "\n"
                                            "QPushButton:hover {\n"
                                            "	background-color: rgb(250, 250, 250);\n"
                                            "}")

        self.verticalLayout.addWidget(self.button_postorder)

        self.verticalSpacer_2 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout.addItem(self.verticalSpacer_2)

        self.horizontalLayout_2.addLayout(self.verticalLayout)

        self.verticalLayout_2.addLayout(self.horizontalLayout_2)

        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        self.button_colose.clicked.connect(MainWindow.close)

        QMetaObject.connectSlotsByName(MainWindow)

    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.button_setting.setText("")
        self.button_enlarge.setText("")
        self.button_colose.setText("")
        self.label_tree.setText(QCoreApplication.translate("MainWindow", u"Binary Tree View", None))
        self.button_preorder.setText(QCoreApplication.translate("MainWindow", u"Preorder traversal", None))
        self.button_inorder.setText(QCoreApplication.translate("MainWindow", u"Inorder traversal", None))
        self.button_postorder.setText(QCoreApplication.translate("MainWindow", u"Postorder traversal", None))
    # retranslateUi
