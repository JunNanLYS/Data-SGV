from typing import Union, Optional

from PySide6.QtCore import Signal
from PySide6.QtWidgets import QVBoxLayout, QWidget, QLayout, QLayoutItem, QHBoxLayout, QSpacerItem, QSizePolicy
from qfluentwidgets import ToolButton, FluentIcon

from src.widgets.graphics_view import MyGraphicsView, BinaryTreeView, GraphView
from src.widgets.settings import DefaultSettings, GraphSettings, TreeSettings
from windows import RoundedWindow


class DataStructureWidget(RoundedWindow):
    def __init__(self, parent=None):
        super().__init__(parent)

    def __init_menu_widget(self):
        """init menu widget"""
        raise NotImplementedError

    def __init_graphics_tool_widget(self):
        """init graphics tool widget"""
        raise NotImplementedError


class DataStructureWindow(DataStructureWidget):
    openSetting = Signal()
    closeSetting = Signal()

    def __init__(self, parent=None, setting_w=DefaultSettings, graphics_w=MyGraphicsView):
        super().__init__(parent)
        self.layout_main = QVBoxLayout(self)

        # init widget
        self.setting_widget = setting_w(self)
        self.setting_widget.hide()
        self.graphics_view = graphics_w()
        self.__init_menu_widget()
        self.__init_graphics_widget()

        # init menu widget
        self.t_setting = ToolButton(FluentIcon.SETTING, self)
        self.t_close = ToolButton(FluentIcon.CLOSE, self)
        self.t_return = ToolButton(FluentIcon.RETURN, self)
        self.t_zoom = ToolButton(FluentIcon.ZOOM, self)

        # signal connect slot
        self.t_setting.clicked.connect(self.show_mask)
        self.t_setting.clicked.connect(self.openSetting)
        self.maskHide.connect(self.closeSetting)

        self.t_close.clicked.connect(self.close)
        self.t_zoom.clicked.connect(self.zoom)

        # add to layout
        self.add_to_settings_layout(self.t_setting)
        self.add_to_tools_layout(self.t_return)
        self.add_to_tools_layout(self.t_zoom)
        self.add_to_tools_layout(self.t_close)

    def add_to_settings_layout(self, obj: Union[QWidget, QLayout, QLayoutItem]):
        self.layout_add_ojb(self.layout_settings, obj)

    def add_to_tools_layout(self, obj: Union[QWidget, QLayout, QLayoutItem]):
        self.layout_add_ojb(self.layout_tools, obj)

    def add_to_graphics_tool_layout(self, obj: Union[QWidget, QLayout, QLayoutItem]):
        self.layout_add_ojb(self.layout_graphics_tools, obj)

    def layout_add_ojb(self, layout: Union[QLayout, QHBoxLayout, QVBoxLayout],
                       obj: Union[QWidget, QLayout, QLayoutItem]):
        if isinstance(obj, QLayout):
            layout.addLayout(obj)
        elif isinstance(obj, QWidget):
            layout.addWidget(obj)
        elif isinstance(obj, QLayoutItem):
            layout.addItem(obj)
        else:
            raise TypeError("obj not is Union[QWidget, QLayout, QLayoutItem]")

    def zoom(self):
        if self.isFullScreen():
            self.showNormal()
            return
        self.showFullScreen()

    def __init_menu_widget(self):
        # init layout
        self.layout_menu = QHBoxLayout()
        self.layout_settings = QHBoxLayout()
        self.layout_tools = QHBoxLayout()
        self.spacer_menu = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        # add to layout
        self.layout_menu.addLayout(self.layout_settings)
        self.layout_menu.addItem(self.spacer_menu)
        self.layout_menu.addLayout(self.layout_tools)
        self.layout_main.addLayout(self.layout_menu)

    def __init_graphics_widget(self):
        # init layout
        self.layout_graphics = QHBoxLayout()
        self.layout_graphics_tools = QVBoxLayout()

        # init graphics view
        self.graphics_view.setParent(self)

        # add to layout
        self.layout_graphics.addWidget(self.graphics_view)
        self.layout_graphics.addLayout(self.layout_graphics_tools)
        self.layout_main.addLayout(self.layout_graphics)

    def __init_graphics_tool_widget(self):
        raise NotImplementedError


class TreeDataStructure(DataStructureWindow):
    def __init__(self, parent=None):
        super().__init__(parent, TreeSettings, BinaryTreeView)

    def __init_menu_widget(self):
        pass

    def __init_graphics_tool_widget(self):
        pass


class GraphDataStructure(DataStructureWindow):
    def __init__(self, parent=None):
        super().__init__(parent, GraphSettings, GraphView)

    def __init_menu_widget(self):
        pass

    def __init_graphics_tool_widget(self):
        pass


if __name__ == '__main__':
    import sys
    from PySide6.QtWidgets import QApplication

    app = QApplication(sys.argv)
    window = GraphDataStructure()
    window.show()
    sys.exit(app.exec())
