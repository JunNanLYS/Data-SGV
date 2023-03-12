# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'BinarySearchTree.ui'
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
                               QLineEdit, QPushButton, QSizePolicy, QSpacerItem,
                               QVBoxLayout, QWidget)

from src.MyClass.MyWidget import (IconButton, MyButton, MyGroupBox)
from src.View.TreeView import BinarySearchTreeView
from res import resource_rc


class Ui_widget_background(object):
    def setupUi(self, widget_background):
        if not widget_background.objectName():
            widget_background.setObjectName(u"widget_background")
        widget_background.resize(1000, 800)
        widget_background.setMinimumSize(QSize(1000, 800))
        self.verticalLayout_7 = QVBoxLayout(widget_background)
        self.verticalLayout_7.setObjectName(u"verticalLayout_7")
        self.horizontalLayout_5 = QHBoxLayout()
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.button_setting = IconButton(widget_background)
        self.button_setting.setObjectName(u"button_setting")
        self.button_setting.setMinimumSize(QSize(41, 41))
        self.button_setting.setStyleSheet(u"image: url(:/icon/icons/setting.png);\n"
                                          "border:none;")

        self.horizontalLayout_5.addWidget(self.button_setting)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_5.addItem(self.horizontalSpacer)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.button_back = IconButton(widget_background)
        self.button_back.setObjectName(u"button_back")
        self.button_back.setMinimumSize(QSize(41, 41))
        self.button_back.setStyleSheet(u"image: url(:/icon/icons/back.png);\n"
                                       "border:none;")

        self.horizontalLayout.addWidget(self.button_back)

        self.button_enlarge = IconButton(widget_background)
        self.button_enlarge.setObjectName(u"button_enlarge")
        self.button_enlarge.setMinimumSize(QSize(41, 41))
        self.button_enlarge.setStyleSheet(u"image: url(:/icon/icons/enlarge.png);\n"
                                          "border:none;")

        self.horizontalLayout.addWidget(self.button_enlarge)

        self.button_close = IconButton(widget_background)
        self.button_close.setObjectName(u"button_close")
        self.button_close.setMinimumSize(QSize(41, 41))
        self.button_close.setStyleSheet(u"image: url(:/icon/icons/close.png);\n"
                                        "border:none;")

        self.horizontalLayout.addWidget(self.button_close)

        self.horizontalLayout_5.addLayout(self.horizontalLayout)

        self.verticalLayout_7.addLayout(self.horizontalLayout_5)

        self.line = QFrame(widget_background)
        self.line.setObjectName(u"line")
        self.line.setFrameShape(QFrame.HLine)
        self.line.setFrameShadow(QFrame.Sunken)

        self.verticalLayout_7.addWidget(self.line)

        self.horizontalLayout_7 = QHBoxLayout()
        self.horizontalLayout_7.setObjectName(u"horizontalLayout_7")
        self.label_title = QLabel(widget_background)
        self.label_title.setObjectName(u"label_title")
        self.label_title.setMinimumSize(QSize(0, 60))
        font = QFont()
        font.setFamilies([u"Microsoft Sans Serif"])
        font.setPointSize(40)
        font.setBold(True)
        font.setKerning(True)
        font.setStyleStrategy(QFont.PreferAntialias)
        self.label_title.setFont(font)
        self.label_title.setAlignment(Qt.AlignLeading | Qt.AlignLeft | Qt.AlignVCenter)

        self.horizontalLayout_7.addWidget(self.label_title)

        self.horizontalSpacer_2 = QSpacerItem(979, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_7.addItem(self.horizontalSpacer_2)

        self.verticalLayout_7.addLayout(self.horizontalLayout_7)

        self.horizontalLayout_6 = QHBoxLayout()
        self.horizontalLayout_6.setObjectName(u"horizontalLayout_6")
        self.graphicsView = BinarySearchTreeView(widget_background)
        self.graphicsView.setObjectName(u"graphicsView")
        self.graphicsView.setMinimumSize(QSize(670, 660))
        self.graphicsView.setFocusPolicy(Qt.NoFocus)
        self.graphicsView.setContextMenuPolicy(Qt.DefaultContextMenu)
        self.graphicsView.setStyleSheet(u"background-color: rgb(250, 250, 250);\n"
                                        "border-radius:20px;")

        self.horizontalLayout_6.addWidget(self.graphicsView)

        self.verticalLayout_6 = QVBoxLayout()
        self.verticalLayout_6.setObjectName(u"verticalLayout_6")
        self.groupBox_node = MyGroupBox(widget_background)
        self.groupBox_node.setObjectName(u"groupBox_node")
        self.groupBox_node.setMinimumSize(QSize(300, 300))
        font1 = QFont()
        font1.setPointSize(22)
        self.groupBox_node.setFont(font1)
        self.groupBox_node.setFocusPolicy(Qt.NoFocus)
        self.groupBox_node.setStyleSheet(u"background-color: rgb(230, 230, 230);")
        self.groupBox_node.setAlignment(Qt.AlignCenter)
        self.groupBox_node.setFlat(True)
        self.verticalLayout_5 = QVBoxLayout(self.groupBox_node)
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.verticalLayout_2 = QVBoxLayout()
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.label_add = QLabel(self.groupBox_node)
        self.label_add.setObjectName(u"label_add")
        self.label_add.setMinimumSize(QSize(175, 20))
        font2 = QFont()
        font2.setFamilies([u"\u65b0\u5b8b\u4f53"])
        font2.setPointSize(12)
        font2.setItalic(False)
        self.label_add.setFont(font2)
        self.label_add.setAlignment(Qt.AlignCenter)

        self.verticalLayout_2.addWidget(self.label_add)

        self.horizontalLayout_4 = QHBoxLayout()
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.lineEdit_add = QLineEdit(self.groupBox_node)
        self.lineEdit_add.setObjectName(u"lineEdit_add")
        self.lineEdit_add.setMinimumSize(QSize(0, 35))
        font3 = QFont()
        font3.setPointSize(10)
        self.lineEdit_add.setFont(font3)
        self.lineEdit_add.setStyleSheet(u"background-color: rgb(250,250,250);")

        self.horizontalLayout_4.addWidget(self.lineEdit_add)

        self.button_add = QPushButton(self.groupBox_node)
        self.button_add.setObjectName(u"button_add")
        self.button_add.setMinimumSize(QSize(41, 21))
        self.button_add.setStyleSheet(u"QPushButton{\n"
                                      "background-color: rgb(250, 250, 250);\n"
                                      "border-radius:10px;\n"
                                      "border-style:solid;\n"
                                      "border-width:1px;\n"
                                      "border-color:rgb(0, 0, 0);\n"
                                      "}\n"
                                      "QPushButton:hover{\n"
                                      "background-color:#ecf5ff;\n"
                                      "border-style:solid;\n"
                                      "border-width:1px;\n"
                                      "border-color:#409eff;\n"
                                      "}")

        self.horizontalLayout_4.addWidget(self.button_add)

        self.verticalLayout_2.addLayout(self.horizontalLayout_4)

        self.verticalLayout_5.addLayout(self.verticalLayout_2)

        self.verticalLayout_3 = QVBoxLayout()
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.label_delete = QLabel(self.groupBox_node)
        self.label_delete.setObjectName(u"label_delete")
        font4 = QFont()
        font4.setFamilies([u"\u65b0\u5b8b\u4f53"])
        font4.setPointSize(12)
        font4.setUnderline(False)
        self.label_delete.setFont(font4)
        self.label_delete.setAlignment(Qt.AlignCenter)

        self.verticalLayout_3.addWidget(self.label_delete)

        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.lineEdit_delete = QLineEdit(self.groupBox_node)
        self.lineEdit_delete.setObjectName(u"lineEdit_delete")
        self.lineEdit_delete.setMinimumSize(QSize(0, 35))
        self.lineEdit_delete.setFont(font3)
        self.lineEdit_delete.setStyleSheet(u"background-color: rgb(250,250,250);")

        self.horizontalLayout_3.addWidget(self.lineEdit_delete)

        self.button_delete = QPushButton(self.groupBox_node)
        self.button_delete.setObjectName(u"button_delete")
        self.button_delete.setMinimumSize(QSize(41, 21))
        self.button_delete.setStyleSheet(u"QPushButton{\n"
                                         "background-color: rgb(250, 250, 250);\n"
                                         "border-radius:10px;\n"
                                         "border-style:solid;\n"
                                         "border-width:1px;\n"
                                         "border-color:rgb(0, 0, 0);\n"
                                         "}\n"
                                         "QPushButton:hover{\n"
                                         "background-color:#ecf5ff;\n"
                                         "border-style:solid;\n"
                                         "border-width:1px;\n"
                                         "border-color:#409eff;\n"
                                         "}")

        self.horizontalLayout_3.addWidget(self.button_delete)

        self.verticalLayout_3.addLayout(self.horizontalLayout_3)

        self.verticalLayout_5.addLayout(self.verticalLayout_3)

        self.verticalLayout_4 = QVBoxLayout()
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.label_search = QLabel(self.groupBox_node)
        self.label_search.setObjectName(u"label_search")
        font5 = QFont()
        font5.setFamilies([u"\u65b0\u5b8b\u4f53"])
        font5.setPointSize(12)
        self.label_search.setFont(font5)
        self.label_search.setAlignment(Qt.AlignCenter)

        self.verticalLayout_4.addWidget(self.label_search)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.lineEdit_search = QLineEdit(self.groupBox_node)
        self.lineEdit_search.setObjectName(u"lineEdit_search")
        self.lineEdit_search.setMinimumSize(QSize(0, 35))
        self.lineEdit_search.setFont(font3)
        self.lineEdit_search.setStyleSheet(u"background-color: rgb(250,250,250);")

        self.horizontalLayout_2.addWidget(self.lineEdit_search)

        self.button_search = QPushButton(self.groupBox_node)
        self.button_search.setObjectName(u"button_search")
        self.button_search.setMinimumSize(QSize(41, 21))
        self.button_search.setMaximumSize(QSize(16777215, 16777215))
        self.button_search.setStyleSheet(u"QPushButton{\n"
                                         "background-color: rgb(250, 250, 250);\n"
                                         "border-radius:10px;\n"
                                         "border-style:solid;\n"
                                         "border-width:1px;\n"
                                         "border-color:rgb(0, 0, 0);\n"
                                         "}\n"
                                         "QPushButton:hover{\n"
                                         "background-color:#ecf5ff;\n"
                                         "border-style:solid;\n"
                                         "border-width:1px;\n"
                                         "border-color:#409eff;\n"
                                         "}")

        self.horizontalLayout_2.addWidget(self.button_search)

        self.verticalLayout_4.addLayout(self.horizontalLayout_2)

        self.verticalLayout_5.addLayout(self.verticalLayout_4)

        self.verticalLayout_6.addWidget(self.groupBox_node)

        self.groupBox_traversal = MyGroupBox(widget_background)
        self.groupBox_traversal.setObjectName(u"groupBox_traversal")
        self.groupBox_traversal.setMinimumSize(QSize(300, 300))
        self.groupBox_traversal.setFont(font1)
        self.groupBox_traversal.setStyleSheet(u"background-color: rgb(230, 230, 230);")
        self.groupBox_traversal.setAlignment(Qt.AlignCenter)
        self.groupBox_traversal.setFlat(True)
        self.groupBox_traversal.setCheckable(False)
        self.verticalLayout = QVBoxLayout(self.groupBox_traversal)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.button_pre = MyButton(self.groupBox_traversal)
        self.button_pre.setObjectName(u"button_pre")
        self.button_pre.setMinimumSize(QSize(0, 50))

        self.verticalLayout.addWidget(self.button_pre)

        self.button_in = MyButton(self.groupBox_traversal)
        self.button_in.setObjectName(u"button_in")
        self.button_in.setMinimumSize(QSize(0, 50))

        self.verticalLayout.addWidget(self.button_in)

        self.button_post = MyButton(self.groupBox_traversal)
        self.button_post.setObjectName(u"button_post")
        self.button_post.setMinimumSize(QSize(0, 50))

        self.verticalLayout.addWidget(self.button_post)

        self.verticalLayout_6.addWidget(self.groupBox_traversal)

        self.horizontalLayout_6.addLayout(self.verticalLayout_6)

        self.verticalLayout_7.addLayout(self.horizontalLayout_6)

        self.retranslateUi(widget_background)
        self.button_close.clicked.connect(widget_background.close)

        QMetaObject.connectSlotsByName(widget_background)

    # setupUi

    def retranslateUi(self, widget_background):
        widget_background.setWindowTitle(QCoreApplication.translate("widget_background", u"Form", None))
        self.button_setting.setText("")
        self.button_back.setText("")
        self.button_enlarge.setText("")
        self.button_close.setText("")
        self.label_title.setText(QCoreApplication.translate("widget_background", u"Binary Search Tree", None))
        self.groupBox_node.setTitle(QCoreApplication.translate("widget_background", u"Node", None))
        self.label_add.setText(QCoreApplication.translate("widget_background",
                                                          u"\u6dfb\u52a0\u5355\u4e2a\u8282\u70b9 \u6216 \u6dfb\u52a0\u4e00\u7ec4\u8282\u70b9",
                                                          None))
        self.lineEdit_add.setPlaceholderText(
            QCoreApplication.translate("widget_background", u"[1, 2, 3, 4] or 1", None))
        self.button_add.setText(QCoreApplication.translate("widget_background", u"A", None))
        self.label_delete.setText(QCoreApplication.translate("widget_background",
                                                             u"\u5220\u9664\u5355\u4e2a\u8282\u70b9 \u6216\u5220\u9664\u4e00\u7ec4\u8282\u70b9",
                                                             None))
        self.lineEdit_delete.setPlaceholderText(
            QCoreApplication.translate("widget_background", u"[1, 2, 3, 4] or 1", None))
        self.button_delete.setText(QCoreApplication.translate("widget_background", u"D", None))
        self.label_search.setText(
            QCoreApplication.translate("widget_background", u"\u641c\u7d22\u5355\u4e2a\u8282\u70b9", None))
        self.lineEdit_search.setPlaceholderText(QCoreApplication.translate("widget_background", u"1", None))
        self.button_search.setText(QCoreApplication.translate("widget_background", u"S", None))
        self.groupBox_traversal.setTitle(QCoreApplication.translate("widget_background", u"Traversal", None))
        self.button_pre.setText(QCoreApplication.translate("widget_background", u"Preorder", None))
        self.button_in.setText(QCoreApplication.translate("widget_background", u"Inorder", None))
        self.button_post.setText(QCoreApplication.translate("widget_background", u"Postorder", None))
    # retranslateUi
