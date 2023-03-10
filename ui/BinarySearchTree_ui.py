# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading ui file 'BinarySearchTree_ui.ui'
##
## Created by: Qt User Interface Compiler version 6.4.0
##
## WARNING! All changes made in this file will be lost when recompiling ui file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
                            QMetaObject, QObject, QPoint, QRect,
                            QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
                           QFont, QFontDatabase, QGradient, QIcon,
                           QImage, QKeySequence, QLinearGradient, QPainter,
                           QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QHBoxLayout, QLabel, QLineEdit,
                               QMainWindow, QPushButton, QSizePolicy, QSpacerItem,
                               QVBoxLayout, QWidget)

from src.View.TreeView import BinarySearchTreeView
from src.MyClass.MyWidget import MyWidget
from res import resource_rc


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(1000, 800)
        MainWindow.setMinimumSize(QSize(1000, 800))
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.widget = MyWidget(self.centralwidget)
        self.widget.setObjectName(u"widget")
        self.widget.setGeometry(QRect(0, 0, 1000, 800))
        self.widget.setMinimumSize(QSize(1000, 800))
        self.verticalLayout_4 = QVBoxLayout(self.widget)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.horizontalLayout_4 = QHBoxLayout()
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.button_setting = QPushButton(self.widget)
        self.button_setting.setObjectName(u"button_setting")
        self.button_setting.setMinimumSize(QSize(41, 41))
        self.button_setting.setStyleSheet(u"image: url(:/icon/icons/setting.png);\n"
                                          "border:none;")

        self.horizontalLayout_4.addWidget(self.button_setting)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_4.addItem(self.horizontalSpacer)

        self.button_enlarge = QPushButton(self.widget)
        self.button_enlarge.setObjectName(u"button_enlarge")
        self.button_enlarge.setMinimumSize(QSize(41, 41))
        self.button_enlarge.setStyleSheet(u"image: url(:/icon/icons/enlarge.png);\n"
                                          "border:none;")

        self.horizontalLayout_4.addWidget(self.button_enlarge)

        self.button_close = QPushButton(self.widget)
        self.button_close.setObjectName(u"button_close")
        self.button_close.setMinimumSize(QSize(41, 41))
        self.button_close.setStyleSheet(u"image: url(:/icon/icons/close.png);\n"
                                        "border:none;")

        self.horizontalLayout_4.addWidget(self.button_close)

        self.verticalLayout_4.addLayout(self.horizontalLayout_4)

        self.horizontalLayout_5 = QHBoxLayout()
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.graphicsView = BinarySearchTreeView(self.widget)
        self.graphicsView.setObjectName(u"graphicsView")
        self.graphicsView.setMinimumSize(QSize(640, 620))
        self.graphicsView.setStyleSheet(u"background-color: rgb(255, 255, 255);\n"
                                        "border-radius:10px;")

        self.horizontalLayout_5.addWidget(self.graphicsView)

        self.verticalLayout_3 = QVBoxLayout()
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.verticalLayout_2 = QVBoxLayout()
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.label_title = QLabel(self.widget)
        self.label_title.setObjectName(u"label_title")
        font = QFont()
        font.setFamilies([u"\u5fae\u8f6f\u96c5\u9ed1"])
        font.setPointSize(20)
        font.setBold(False)
        self.label_title.setFont(font)
        self.label_title.setAlignment(Qt.AlignCenter)

        self.verticalLayout_2.addWidget(self.label_title)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.label_add = QLabel(self.widget)
        self.label_add.setObjectName(u"label_add")
        self.label_add.setMinimumSize(QSize(31, 31))
        font1 = QFont()
        font1.setFamilies([u"\u534e\u6587\u6977\u4f53"])
        font1.setPointSize(14)
        font1.setBold(True)
        font1.setItalic(True)
        self.label_add.setFont(font1)

        self.horizontalLayout.addWidget(self.label_add)

        self.lineEdit_add = QLineEdit(self.widget)
        self.lineEdit_add.setObjectName(u"lineEdit_add")
        self.lineEdit_add.setMinimumSize(QSize(160, 40))
        font2 = QFont()
        font2.setPointSize(10)
        self.lineEdit_add.setFont(font2)
        self.lineEdit_add.setStyleSheet(u"QLineEdit{\n"
                                        "	\n"
                                        "	background-color: rgb(255, 255, 255);\n"
                                        "	border-radius: 5px;\n"
                                        "}")

        self.horizontalLayout.addWidget(self.lineEdit_add)

        self.button_add = QPushButton(self.widget)
        self.button_add.setObjectName(u"button_add")
        self.button_add.setMinimumSize(QSize(70, 20))
        self.button_add.setFont(font2)
        self.button_add.setStyleSheet(u"QPushButton{\n"
                                      "	background-color: rgb(255, 255, 255);\n"
                                      "	border-radius:8px;\n"
                                      "}\n"
                                      "QPushButton:hover {\n"
                                      "	background-color: rgb(250, 250, 250);\n"
                                      "}")

        self.horizontalLayout.addWidget(self.button_add)

        self.verticalLayout_2.addLayout(self.horizontalLayout)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.label_delet = QLabel(self.widget)
        self.label_delet.setObjectName(u"label_delet")
        self.label_delet.setFont(font1)
        self.label_delet.setAlignment(Qt.AlignCenter)

        self.horizontalLayout_2.addWidget(self.label_delet)

        self.lineEdit_delete = QLineEdit(self.widget)
        self.lineEdit_delete.setObjectName(u"lineEdit_delete")
        self.lineEdit_delete.setMinimumSize(QSize(160, 40))
        font3 = QFont()
        font3.setPointSize(10)
        font3.setBold(False)
        self.lineEdit_delete.setFont(font3)
        self.lineEdit_delete.setStyleSheet(u"QLineEdit{\n"
                                           "	background-color: rgb(255, 255, 255);\n"
                                           "	border-radius: 5px;\n"
                                           "}")

        self.horizontalLayout_2.addWidget(self.lineEdit_delete)

        self.button_delete = QPushButton(self.widget)
        self.button_delete.setObjectName(u"button_delete")
        self.button_delete.setMinimumSize(QSize(70, 20))
        self.button_delete.setFont(font2)
        self.button_delete.setStyleSheet(u"QPushButton{\n"
                                         "	background-color: rgb(255, 255, 255);\n"
                                         "	border-radius:8px;\n"
                                         "}\n"
                                         "QPushButton:hover {\n"
                                         "	background-color: rgb(250, 250, 250);\n"
                                         "}")

        self.horizontalLayout_2.addWidget(self.button_delete)

        self.verticalLayout_2.addLayout(self.horizontalLayout_2)

        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.label_search = QLabel(self.widget)
        self.label_search.setObjectName(u"label_search")
        self.label_search.setMinimumSize(QSize(31, 31))
        self.label_search.setFont(font1)
        self.label_search.setAlignment(Qt.AlignCenter)

        self.horizontalLayout_3.addWidget(self.label_search)

        self.lineEdit_search = QLineEdit(self.widget)
        self.lineEdit_search.setObjectName(u"lineEdit_search")
        self.lineEdit_search.setMinimumSize(QSize(160, 40))
        font4 = QFont()
        font4.setFamilies([u"Microsoft YaHei ui"])
        font4.setPointSize(10)
        font4.setBold(False)
        self.lineEdit_search.setFont(font4)
        self.lineEdit_search.setStyleSheet(u"QLineEdit{\n"
                                           "	background-color: rgb(255, 255, 255);\n"
                                           "	border-radius: 5px;\n"
                                           "}")

        self.horizontalLayout_3.addWidget(self.lineEdit_search)

        self.button_search = QPushButton(self.widget)
        self.button_search.setObjectName(u"button_search")
        self.button_search.setMinimumSize(QSize(70, 20))
        self.button_search.setFont(font2)
        self.button_search.setStyleSheet(u"QPushButton{\n"
                                         "	background-color: rgb(255, 255, 255);\n"
                                         "	border-radius:8px;\n"
                                         "}\n"
                                         "QPushButton:hover {\n"
                                         "	background-color: rgb(250, 250, 250);\n"
                                         "}")

        self.horizontalLayout_3.addWidget(self.button_search)

        self.verticalLayout_2.addLayout(self.horizontalLayout_3)

        self.verticalLayout_3.addLayout(self.verticalLayout_2)

        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.label_traversal = QLabel(self.widget)
        self.label_traversal.setObjectName(u"label_traversal")
        self.label_traversal.setMinimumSize(QSize(200, 50))
        font5 = QFont()
        font5.setFamilies([u"\u9ed1\u4f53"])
        font5.setPointSize(40)
        font5.setBold(True)
        font5.setItalic(False)
        self.label_traversal.setFont(font5)
        self.label_traversal.setAlignment(Qt.AlignCenter)

        self.verticalLayout.addWidget(self.label_traversal)

        self.button_preorder = QPushButton(self.widget)
        self.button_preorder.setObjectName(u"button_preorder")
        self.button_preorder.setMinimumSize(QSize(250, 80))
        font6 = QFont()
        font6.setFamilies([u"\u534e\u6587\u6977\u4f53"])
        font6.setPointSize(40)
        font6.setBold(True)
        self.button_preorder.setFont(font6)
        self.button_preorder.setStyleSheet(u"QPushButton{\n"
                                           "	background-color: rgb(255, 255, 255);\n"
                                           "	border-radius:8px;\n"
                                           "}\n"
                                           "QPushButton:hover {\n"
                                           "	background-color: rgb(250, 250, 250);\n"
                                           "}")

        self.verticalLayout.addWidget(self.button_preorder)

        self.button_inorder = QPushButton(self.widget)
        self.button_inorder.setObjectName(u"button_inorder")
        self.button_inorder.setMinimumSize(QSize(250, 80))
        font7 = QFont()
        font7.setFamilies([u"\u534e\u6587\u6977\u4f53"])
        font7.setPointSize(40)
        font7.setBold(True)
        font7.setItalic(False)
        self.button_inorder.setFont(font7)
        self.button_inorder.setStyleSheet(u"QPushButton{\n"
                                          "	background-color: rgb(255, 255, 255);\n"
                                          "	border-radius:8px;\n"
                                          "}\n"
                                          "QPushButton:hover {\n"
                                          "	background-color: rgb(250, 250, 250);\n"
                                          "}")

        self.verticalLayout.addWidget(self.button_inorder)

        self.button_postorder = QPushButton(self.widget)
        self.button_postorder.setObjectName(u"button_postorder")
        self.button_postorder.setMinimumSize(QSize(250, 80))
        self.button_postorder.setFont(font6)
        self.button_postorder.setStyleSheet(u"QPushButton{\n"
                                            "	background-color: rgb(255, 255, 255);\n"
                                            "	border-radius:8px;\n"
                                            "}\n"
                                            "QPushButton:hover {\n"
                                            "	background-color: rgb(250, 250, 250);\n"
                                            "}")

        self.verticalLayout.addWidget(self.button_postorder)

        self.verticalLayout_3.addLayout(self.verticalLayout)

        self.horizontalLayout_5.addLayout(self.verticalLayout_3)

        self.verticalLayout_4.addLayout(self.horizontalLayout_5)

        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        self.button_close.clicked.connect(MainWindow.close)

        QMetaObject.connectSlotsByName(MainWindow)

    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.button_setting.setText("")
        self.button_enlarge.setText("")
        self.button_close.setText("")
        self.label_title.setText(QCoreApplication.translate("MainWindow", u"Binary Search Tree", None))
        self.label_add.setText(QCoreApplication.translate("MainWindow", u"V=", None))
        self.lineEdit_add.setPlaceholderText(QCoreApplication.translate("MainWindow", u"15 or 15,13,12", None))
        self.button_add.setText(QCoreApplication.translate("MainWindow", u"Add", None))
        self.label_delet.setText(QCoreApplication.translate("MainWindow", u"V=", None))
        self.lineEdit_delete.setPlaceholderText(
            QCoreApplication.translate("MainWindow", u"Please enter the number", None))
        self.button_delete.setText(QCoreApplication.translate("MainWindow", u"Delete", None))
        self.label_search.setText(QCoreApplication.translate("MainWindow", u"V=", None))
        self.lineEdit_search.setText("")
        self.lineEdit_search.setPlaceholderText(
            QCoreApplication.translate("MainWindow", u"Please enter the number", None))
        self.button_search.setText(QCoreApplication.translate("MainWindow", u"Search", None))
        self.label_traversal.setText(QCoreApplication.translate("MainWindow", u"Traversal", None))
        self.button_preorder.setText(QCoreApplication.translate("MainWindow", u"Preorder", None))
        self.button_inorder.setText(QCoreApplication.translate("MainWindow", u"Inorder", None))
        self.button_postorder.setText(QCoreApplication.translate("MainWindow", u"Postorder", None))
    # retranslateUi
