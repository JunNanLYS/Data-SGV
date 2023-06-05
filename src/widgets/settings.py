from typing import Optional

from PySide6.QtCore import QSize, Signal, Qt, Slot, QPropertyAnimation, Property
from PySide6.QtGui import QFont, QColor, QBrush

from PySide6.QtWidgets import QApplication, QWidget, QLayout, QLabel, QHBoxLayout, QVBoxLayout, QSpacerItem, \
    QSizePolicy, QGraphicsDropShadowEffect
from src.tool import PathTool, JsonSettingTool, stop_time

from qfluentwidgets import SpinBox, ComboBox, SmoothScrollArea, Slider, PushButton
from windows import DefaultWidget


class UiSetting(DefaultWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.set_widget_brush(QBrush(QColor(240, 240, 240)))

    def save(self):
        """save setting"""
        raise NotImplementedError

    def __config(self):
        """config widget"""
        raise NotImplementedError

    def __init_local_setting(self):
        """init local setting layout widget"""
        raise NotImplementedError

    def __init_global_setting(self):
        """init global setting layout widget"""
        raise NotImplementedError


class DefaultSettings(UiSetting):
    saved = Signal(dict)  # 保存信号
    opened = Signal()  # 打开信号
    closed = Signal()  # 关闭信号

    def __init__(self, parent=None):
        super().__init__(parent)
        self.layout_local: Optional[QLayout] = None
        self.layout_global: Optional[QLayout] = None
        self.resize(250, 630)
        self.setMinimumWidth(250)
        self.vertical_layout = QVBoxLayout(self)
        self.scroll_area = SmoothScrollArea(self)
        self.scroll_area.setEnabled(True)
        self.scroll_area.setStyleSheet("border:none;")
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setGeometry(self.rect())
        self.scroll_area_widget = QWidget(self.scroll_area)
        self.scroll_area.setWidget(self.scroll_area_widget)
        self.layout_main = QVBoxLayout(self.scroll_area_widget)

        # init setting config
        self.settings_dict = {
            "global": {
                "version": 0.1,
                "animation_speed": 1.0
            },
            "tree": {},
            "graph": {
                "font_size": 8,
                "font_color": "black",
                "font_family": "SimSum",
                "edge": "ArrowLineWithWeight"
            }
        }

        # init widget
        self.__init_global_setting()
        self.__init_local_setting()
        self.__config()
        self.vertical_layout.addWidget(self.scroll_area)
        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        self.layout_main.addItem(self.verticalSpacer)

        # signal connect slot
        self.parent().sizeChanged.connect(self.parent_changed)
        self.parent().closeSetting.connect(self.close)
        self.parent().openSetting.connect(self.open)
        self.button_save.clicked.connect(self.save)
        self.saved.connect(self.parent().hide_mask)

        # size
        self.resize(parent.width() // 4, parent.height())

        # property animation init
        self.anim = QPropertyAnimation()

    @Property(int)
    def close_animation(self):
        return self.x()

    @close_animation.setter
    def close_animation(self, x):
        self.move(x, 0)

    @Slot()
    def close(self):
        """close animation"""
        print("---close animation---")
        self.anim.setTargetObject(self)
        self.anim.setPropertyName(b"close_animation")
        self.anim.setStartValue(0)
        self.anim.setEndValue(0 - self.width() - 10)
        self.anim.setDuration(500)
        self.anim.start()
        stop_time(millisecond=500)
        self.hide()

        self.setGraphicsEffect(None)

    def local_add_widget(self, widget: QWidget):
        self.layout_local.addWidget(widget)

    def local_add_layout(self, layout: QLayout):
        self.layout_local.addLayout(layout)

    def global_add_widget(self, widget: QWidget):
        self.layout_global.addWidget(widget)

    def global_add_layout(self, layout: QLayout):
        self.layout_global.addLayout(layout)

    @Property(int)
    def open_animation(self):
        return self.x()

    @open_animation.setter
    def open_animation(self, x):
        self.move(x, 0)

    @Slot()
    def open(self):
        """open animation"""
        print("---open animation---")
        self.show()
        self.raise_()
        self.anim.setTargetObject(self)
        self.anim.setPropertyName(b"open_animation")
        self.anim.setStartValue(self.x() - self.width())
        self.anim.setEndValue(0)
        self.anim.setDuration(500)
        self.anim.start()
        stop_time(millisecond=500)

        # shadow
        shadow = QGraphicsDropShadowEffect(self)
        shadow.setOffset(8, 3)
        shadow.setColor(Qt.gray)
        self.setGraphicsEffect(shadow)

    def save(self):
        """save to json file"""
        animation_speed = self.label_animation_speed.text().split(": ")[1]
        self.settings_dict["animation_speed"] = animation_speed

    @Slot(int, int)
    def parent_changed(self, width, height):
        self.resize(width // 4 + 30, height)

    def __config(self):
        # read
        global_config = self.settings_dict["global"]
        animation_speed = global_config["animation_speed"]
        version = global_config["version"]

        # load
        self.label_animation_speed.setText(f"Animation speed: {animation_speed}")
        self.label_version.setText(f"Version: {version}")
        return

    def __init_local_setting(self):
        # font
        font_title = QFont()
        font_title.setFamilies(["Segoe UI"])
        font_title.setPointSize(25)
        font_title.setBold(True)

        # label init
        self.label_local = QLabel(self.scroll_area_widget)
        self.label_local.setText("Local")
        self.label_local.setMaximumSize(QSize(16777215, 40))
        self.label_local.setFont(font_title)
        self.label_local.setAlignment(Qt.AlignHCenter | Qt.AlignTop)

        # button init
        self.button_save = PushButton(self.scroll_area_widget)
        self.button_save.setText("Save")

        # layout init
        self.layout_local = QVBoxLayout()

        # add to layout
        self.layout_main.addWidget(self.label_local)
        self.layout_main.addLayout(self.layout_local)
        self.layout_main.addWidget(self.button_save)

    def __init_global_setting(self):
        # font
        font_title = QFont()
        font_title.setFamilies(["Segoe UI"])
        font_title.setPointSize(25)
        font_title.setBold(True)

        font = QFont()
        font.setFamilies(["Segoe UI"])
        font.setPointSize(12)

        # label init
        self.label_global = QLabel(self.scroll_area_widget)
        self.label_global.setText("Global")
        self.label_global.setMaximumHeight(40)
        self.label_global.setFont(font_title)
        self.label_global.setAlignment(Qt.AlignHCenter | Qt.AlignTop)

        self.label_version = QLabel(self.scroll_area_widget)
        self.label_version.setText("Version: 0.1")
        self.label_version.setFont(font)

        self.label_animation_speed = QLabel(self.scroll_area_widget)
        self.label_animation_speed.setText("Animation speed: 1.0")
        self.label_animation_speed.setMaximumSize(QSize(16777215, 20))
        self.label_animation_speed.setFont(font)

        # slider init
        self.slider_animation_speed = Slider(self.scroll_area_widget)
        self.slider_animation_speed.setMaximumSize(QSize(16777215, 20))
        self.slider_animation_speed.setOrientation(Qt.Horizontal)

        # layout init
        self.layout_global = QVBoxLayout()
        self.layout_animation_speed = QVBoxLayout()

        # add to layout
        self.layout_main.addWidget(self.label_global)

        self.layout_global.addWidget(self.label_version)

        self.layout_animation_speed.addWidget(self.label_animation_speed)
        self.layout_animation_speed.addWidget(self.slider_animation_speed)
        self.layout_global.addLayout(self.layout_animation_speed)

        self.layout_main.addLayout(self.layout_global)


class TreeSettings(DefaultSettings):
    def __init__(self, parent=None):
        super().__init__(parent)

    def save(self):
        self.saved.emit()  # 触发信号
        pass

    def __config(self):
        pass

    def __init_local_setting(self):
        pass


class GraphSettings(DefaultSettings):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.__init_local_setting()  # 载入Local所需的控件
        self.__config()  # 根据配置文件设置

    def save(self):
        super().save()
        config = self.settings_dict["graph"]
        font_color = self.combobox_font_color.text()
        font_size = self.spinbox_font_size.text()
        font_family = self.combobox_font_family.text()
        edge = self.combobox_edge.text()
        config["font_color"] = font_color
        config["font_size"] = int(font_size)
        config["font_family"] = font_family
        config["edge"] = edge
        self.saved.emit(self.settings_dict)

    def __init_local_setting(self):
        font = QFont()
        font.setFamilies(["Segoe UI"])
        font.setPointSize(12)

        # Font size
        layout_font_size = QHBoxLayout(self.scroll_area_widget)
        self.label_font_size = QLabel("Font size -> ", self.scroll_area_widget)
        self.label_font_size.setMinimumSize(QSize(92, 16))
        self.label_font_size.setFont(font)
        layout_font_size.addWidget(self.label_font_size)

        self.spinbox_font_size = SpinBox(self.scroll_area_widget)
        self.spinbox_font_size.setMinimum(5)
        self.spinbox_font_size.setMaximum(12)
        layout_font_size.addWidget(self.spinbox_font_size)

        # Font color
        layout_font_color = QHBoxLayout(self.scroll_area_widget)
        self.label_font_color = QLabel("Font color -> ", self.scroll_area_widget)
        self.label_font_color.setMinimumSize(QSize(91, 16))
        self.label_font_color.setFont(font)
        layout_font_color.addWidget(self.label_font_color)

        self.combobox_font_color = ComboBox(self.scroll_area_widget)
        self.combobox_font_color.addItems(["black", "blue", "yellow", "gray"])
        layout_font_color.addWidget(self.combobox_font_color)

        # Font family
        layout_font_family = QHBoxLayout(self.scroll_area_widget)
        label_font_family = QLabel("Font family -> ", self.scroll_area_widget)
        label_font_family.setFont(font)
        layout_font_family.addWidget(label_font_family)

        self.combobox_font_family = ComboBox(self.scroll_area_widget)
        self.combobox_font_family.addItems(["Segoe", "SimSum"])
        layout_font_family.addWidget(self.combobox_font_family)

        # Edge
        layout_edge = QHBoxLayout(self.scroll_area_widget)
        label_edge = QLabel("Edge -> ", self.scroll_area_widget)
        label_edge.setFont(font)
        layout_edge.addWidget(label_edge)

        self.combobox_edge = ComboBox(self.scroll_area_widget)
        self.combobox_edge.addItems(["Line", "LineWithWeight", "ArrowLine", "ArrowLineWithWeight"])
        layout_edge.addWidget(self.combobox_edge)

        # add to local layout
        self.local_add_layout(layout_font_size)
        self.local_add_layout(layout_font_color)
        self.local_add_layout(layout_font_family)
        self.local_add_layout(layout_edge)

    def __config(self):
        # read
        setting = self.settings_dict["graph"]
        font_size = setting['font_size']
        font_color = setting['font_color']
        font_family = setting["font_family"]
        edge = setting["edge"]

        # load
        self.spinbox_font_size.setValue(font_size)
        self.combobox_font_color.setCurrentText(font_color)
        self.combobox_font_family.setCurrentText(font_family)
        self.combobox_edge.setCurrentText(edge)
        return


if __name__ == "__main__":
    from src.widgets.windows import RoundedWindow

    app = QApplication()

    window = RoundedWindow()
    settings = GraphSettings(window)
    # settings.set_widget_brush(Qt.gray)
    button = PushButton(window)
    button.setText("test")
    button.move(window.width() // 2, window.height() // 2)
    button.clicked.connect(settings.close)
    window.show()

    app.exec()
