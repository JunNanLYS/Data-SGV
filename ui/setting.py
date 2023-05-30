# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'setting.ui'
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
from PySide6.QtWidgets import (QApplication, QHBoxLayout, QLabel, QLayout,
    QSizePolicy, QSlider, QSpacerItem, QVBoxLayout,
    QWidget)

from qfluentwidgets import (ComboBox, PushButton, Slider, SmoothScrollArea)

class UiSetting(object):
    def setupUi(self, Form):
        if not Form.objectName():
            Form.setObjectName(u"Form")
        Form.resize(250, 627)
        Form.setMinimumSize(QSize(250, 0))
        self.verticalLayout = QVBoxLayout(Form)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.scroll_area = SmoothScrollArea(Form)
        self.scroll_area.setObjectName(u"scroll_area")
        self.scroll_area.setEnabled(True)
        self.scroll_area.setStyleSheet(u"border:none;")
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)
        self.scroll_area_widget = QWidget()
        self.scroll_area_widget.setObjectName(u"scroll_area_widget")
        self.scroll_area_widget.setGeometry(QRect(0, 0, 232, 609))
        self.layout_main = QVBoxLayout(self.scroll_area_widget)
        self.layout_main.setObjectName(u"verticalLayout_3")
        self.label_global = QLabel(self.scroll_area_widget)
        self.label_global.setObjectName(u"label_global")
        self.label_global.setMaximumSize(QSize(16777215, 40))
        font = QFont()
        font.setFamilies([u"\u5fae\u8f6f\u96c5\u9ed1 Light"])
        font.setPointSize(25)
        font.setBold(True)
        self.label_global.setFont(font)
        self.label_global.setAlignment(Qt.AlignHCenter|Qt.AlignTop)

        self.layout_main.addWidget(self.label_global)

        self.layout_global = QVBoxLayout()
        self.layout_global.setObjectName(u"layout_global")
        self.node_color_layout = QHBoxLayout()
        self.node_color_layout.setSpacing(6)
        self.node_color_layout.setObjectName(u"node_color_layout")
        self.node_color_layout.setContentsMargins(-1, -1, 0, -1)
        self.label_node_color = QLabel(self.scroll_area_widget)
        self.label_node_color.setObjectName(u"label_node_color")
        self.label_node_color.setMinimumSize(QSize(82, 21))
        self.label_node_color.setMaximumSize(QSize(16777215, 30))
        font1 = QFont()
        font1.setFamilies([u"Segoe UI"])
        font1.setPointSize(12)
        self.label_node_color.setFont(font1)

        self.node_color_layout.addWidget(self.label_node_color)

        self.combobox_node_color = ComboBox(self.scroll_area_widget)
        self.combobox_node_color.setObjectName(u"combobox_node_color")
        font2 = QFont()
        font2.setFamilies([u"Segoe UI"])
        font2.setBold(False)
        font2.setItalic(False)
        self.combobox_node_color.setFont(font2)

        self.node_color_layout.addWidget(self.combobox_node_color)


        self.layout_global.addLayout(self.node_color_layout)

        self.layout_animation_speed = QVBoxLayout()
        self.layout_animation_speed.setSpacing(0)
        self.layout_animation_speed.setObjectName(u"layout_animation_speed")
        self.layout_animation_speed.setSizeConstraint(QLayout.SetDefaultConstraint)
        self.layout_animation_speed.setContentsMargins(-1, -1, -1, 0)
        self.label_animation_speed = QLabel(self.scroll_area_widget)
        self.label_animation_speed.setObjectName(u"label_animation_speed")
        self.label_animation_speed.setMaximumSize(QSize(16777215, 20))
        font3 = QFont()
        font3.setFamilies([u"Segoe UI"])
        font3.setPointSize(12)
        font3.setBold(False)
        self.label_animation_speed.setFont(font3)
        self.label_animation_speed.setLineWidth(1)

        self.layout_animation_speed.addWidget(self.label_animation_speed)

        self.slider_animation_speed = Slider(self.scroll_area_widget)
        self.slider_animation_speed.setObjectName(u"slider_animation_speed")
        self.slider_animation_speed.setMaximumSize(QSize(16777215, 20))
        self.slider_animation_speed.setOrientation(Qt.Horizontal)
        self.slider_animation_speed.setTickPosition(QSlider.NoTicks)
        self.slider_animation_speed.setTickInterval(0)

        self.layout_animation_speed.addWidget(self.slider_animation_speed)


        self.layout_global.addLayout(self.layout_animation_speed)


        self.layout_main.addLayout(self.layout_global)

        self.label_current = QLabel(self.scroll_area_widget)
        self.label_current.setObjectName(u"label_current")
        self.label_current.setMaximumSize(QSize(16777215, 40))
        self.label_current.setFont(font)
        self.label_current.setAlignment(Qt.AlignHCenter|Qt.AlignTop)

        self.layout_main.addWidget(self.label_current)

        self.layout_current = QVBoxLayout()
        self.layout_current.setSpacing(10)
        self.layout_current.setObjectName(u"layout_current")
        self.layout_current.setContentsMargins(-1, -1, -1, 10)

        self.layout_main.addLayout(self.layout_current)

        self.button_save = PushButton(self.scroll_area_widget)
        self.button_save.setObjectName(u"button_save")
        self.button_save.setFont(font1)

        self.layout_main.addWidget(self.button_save)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.layout_main.addItem(self.verticalSpacer)

        self.scroll_area.setWidget(self.scroll_area_widget)

        self.verticalLayout.addWidget(self.scroll_area)


        self.retranslateUi(Form)

        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"Form", None))
        self.label_global.setText(QCoreApplication.translate("Form", u"Global", None))
        self.label_node_color.setText(QCoreApplication.translate("Form", u"Node color -> ", None))
        self.combobox_node_color.setText(QCoreApplication.translate("Form", u"Blue", None))
        self.label_animation_speed.setText(QCoreApplication.translate("Form", u"Animation speed: 1.0", None))
        self.label_current.setText(QCoreApplication.translate("Form", u"Current", None))
        self.button_save.setText(QCoreApplication.translate("Form", u"Save", None))
    # retranslateUi

