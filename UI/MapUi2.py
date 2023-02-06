# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'Graph.ui'
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
                               QPushButton, QSizePolicy, QSpacerItem, QTextBrowser,
                               QVBoxLayout, QWidget)

from DataStructView.Buildinin.GraphView import GraphView
from DataStructView.Class.MyWidget import MyWidget
from DataStructView.res import resource_rc


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(1000, 800)
        MainWindow.setMinimumSize(QSize(1000, 800))
        MainWindow.setWindowFlag(Qt.FramelessWindowHint)
        MainWindow.setAttribute(Qt.WA_TranslucentBackground)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.widget = MyWidget(self.centralwidget)
        self.widget.setObjectName(u"widget")
        self.widget.setGeometry(QRect(0, 0, 1000, 800))
        self.widget.setMinimumSize(QSize(1000, 800))
        self.widget.setStyleSheet(u"QWidget#widget {\n"
                                  "color: rgb(230, 230, 230);\n"
                                  "	background-color: rgb(230, 230, 230);\n"
                                  "	border-radius: 20px;\n"
                                  "}")
        # MainWindow.setCentralWidget(self.widget)
        self.verticalLayout_3 = QVBoxLayout(self.widget)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.horizontalSpacer_4 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_3.addItem(self.horizontalSpacer_4)

        self.button_back = QPushButton(self.widget)
        self.button_back.setObjectName(u"button_back")
        self.button_back.setMinimumSize(QSize(31, 31))
        self.button_back.setStyleSheet(u"#button_back{\n"
                                       "	image: url(:/icon/icons/back.png);\n"
                                       "	border:none;\n"
                                       "}")

        self.horizontalLayout_3.addWidget(self.button_back)

        self.button_enlarge = QPushButton(self.widget)
        self.button_enlarge.setObjectName(u"button_enlarge")
        self.button_enlarge.setMinimumSize(QSize(31, 31))
        self.button_enlarge.setStyleSheet(u"#button_enlarge{\n"
                                          "	image: url(:/icon/icons/enlarge.png);\n"
                                          "	border:none;\n"
                                          "}")

        self.horizontalLayout_3.addWidget(self.button_enlarge)

        self.button_close = QPushButton(self.widget)
        self.button_close.setObjectName(u"button_close")
        self.button_close.setMinimumSize(QSize(31, 31))
        self.button_close.setStyleSheet(u"#button_close{\n"
                                        "	border:none;\n"
                                        "	image: url(:/icon/icons/close.png);\n"
                                        "}\n"
                                        "")

        self.horizontalLayout_3.addWidget(self.button_close)

        self.verticalLayout_3.addLayout(self.horizontalLayout_3)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.button_setting = QPushButton(self.widget)
        self.button_setting.setObjectName(u"button_setting")
        self.button_setting.setMinimumSize(QSize(31, 31))
        self.button_setting.setStyleSheet(u"#button_setting{\n"
                                          "	image: url(:/icon/icons/setting.png);\n"
                                          "	border:none;\n"
                                          "}")

        self.horizontalLayout_2.addWidget(self.button_setting)

        self.button_layer = QPushButton(self.widget)
        self.button_layer.setObjectName(u"button_layer")
        self.button_layer.setMinimumSize(QSize(31, 31))
        self.button_layer.setStyleSheet(u"#button_layer{\n"
                                        "	image: url(:/icon/icons/layer.png);\n"
                                        "	border:none;\n"
                                        "}")

        self.horizontalLayout_2.addWidget(self.button_layer)

        self.label_view = QLabel(self.widget)
        self.label_view.setObjectName(u"label_view")
        self.label_view.setMinimumSize(QSize(321, 51))
        font = QFont()
        font.setFamilies([u"Microsoft YaHei"])
        font.setPointSize(31)
        font.setBold(False)
        font.setKerning(True)
        self.label_view.setFont(font)
        self.label_view.setStyleSheet(u"#label_view{\n"
                                      "	color: rgb(80, 241, 241);\n"
                                      "}")

        self.horizontalLayout_2.addWidget(self.label_view)

        self.horizontalSpacer_3 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_2.addItem(self.horizontalSpacer_3)

        self.verticalLayout_3.addLayout(self.horizontalLayout_2)

        self.horizontalLayout_4 = QHBoxLayout()
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.graphicsView = GraphView(self.widget)
        self.graphicsView.setObjectName(u"graphicsView")
        self.graphicsView.setMinimumSize(QSize(700, 680))
        self.graphicsView.setStyleSheet(u"QGraphicsView#graphicsView\n"
                                        "{\n"
                                        "	background-color: rgb(255, 255, 255);\n"
                                        " 	border-radius: 25px;\n"
                                        "}")

        self.horizontalLayout_4.addWidget(self.graphicsView)

        self.verticalLayout_2 = QVBoxLayout()
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer)

        self.label_info = QLabel(self.widget)
        self.label_info.setObjectName(u"label_info")
        self.label_info.setMinimumSize(QSize(101, 51))
        self.label_info.setFont(font)
        self.label_info.setStyleSheet(u"#label_info{\n"
                                      "	color: rgb(80, 241, 241);\n"
                                      "}")

        self.horizontalLayout.addWidget(self.label_info)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer_2)

        self.verticalLayout.addLayout(self.horizontalLayout)

        self.textBrowser = QTextBrowser(self.widget)
        self.textBrowser.setObjectName(u"textBrowser")
        self.textBrowser.setMinimumSize(QSize(280, 270))
        font1 = QFont()
        font1.setFamilies([u"Microsoft YaHei UI Light"])
        font1.setPointSize(16)
        font1.setBold(False)
        self.textBrowser.setFont(font1)
        self.textBrowser.setStyleSheet(u"#textBrowser{\n"
                                       "	border-radius:20px;\n"
                                       "	background-color: rgb(255, 255, 255);\n"
                                       "}")

        self.verticalLayout.addWidget(self.textBrowser)

        self.verticalLayout_2.addLayout(self.verticalLayout)

        self.button_bfs = QPushButton(self.widget)
        self.button_bfs.setObjectName(u"button_bfs")
        self.button_bfs.setMinimumSize(QSize(280, 100))
        font2 = QFont()
        font2.setFamilies([u"Microsoft JhengHei Light"])
        font2.setPointSize(50)
        font2.setBold(True)
        self.button_bfs.setFont(font2)
        self.button_bfs.setCursor(QCursor(Qt.ArrowCursor))
        self.button_bfs.setStyleSheet(u"#button_bfs{\n"
                                      "	background-color: rgb(255, 255, 255);\n"
                                      "	border-radius: 24px;\n"
                                      "}")

        self.verticalLayout_2.addWidget(self.button_bfs)

        self.button_dfs = QPushButton(self.widget)
        self.button_dfs.setObjectName(u"button_dfs")
        self.button_dfs.setMinimumSize(QSize(280, 100))
        self.button_dfs.setFont(font2)
        self.button_dfs.setStyleSheet(u"#button_dfs{\n"
                                      "	background-color: rgb(255, 255, 255);\n"
                                      "	border-radius: 24px;\n"
                                      "}")

        self.verticalLayout_2.addWidget(self.button_dfs)

        self.horizontalLayout_4.addLayout(self.verticalLayout_2)

        self.verticalLayout_3.addLayout(self.horizontalLayout_4)

        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        self.button_close.clicked.connect(MainWindow.close)

        QMetaObject.connectSlotsByName(MainWindow)

    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.button_back.setText("")
        self.button_enlarge.setText("")
        self.button_close.setText("")
        self.button_setting.setText("")
        self.button_layer.setText("")
        self.label_view.setText(QCoreApplication.translate("MainWindow", u"Data struct view", None))
        self.label_info.setText(QCoreApplication.translate("MainWindow", u"INFO", None))
        self.textBrowser.setHtml(QCoreApplication.translate("MainWindow",
                                                            u"<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
                                                            "<html><head><meta name=\"qrichtext\" content=\"1\" /><meta charset=\"utf-8\" /><style type=\"text/css\">\n"
                                                            "p, li { white-space: pre-wrap; }\n"
                                                            "hr { height: 1px; border-width: 0; }\n"
                                                            "li.unchecked::marker { content: \"\\2610\"; }\n"
                                                            "li.checked::marker { content: \"\\2612\"; }\n"
                                                            "</style></head><body style=\" font-family:'Microsoft YaHei UI Light'; font-size:16pt; font-weight:400; font-style:normal;\">\n"
                                                            "<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p></body></html>",
                                                            None))
        self.button_bfs.setText(QCoreApplication.translate("MainWindow", u"BFS", None))
        self.button_dfs.setText(QCoreApplication.translate("MainWindow", u"DFS", None))
    # retranslateUi
