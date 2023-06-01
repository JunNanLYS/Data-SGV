from typing import Union

from PySide6.QtCore import Signal, Qt
from PySide6.QtGui import QFont
from PySide6.QtWidgets import QVBoxLayout, QWidget, QLayout, QLayoutItem, QHBoxLayout, QSpacerItem, QSizePolicy, QLabel
from qfluentwidgets import ToolButton, FluentIcon, LineEdit, ComboBox

from src.widgets.graphics_view import MyGraphicsView, BinaryTreeView, GraphView
from src.widgets.settings import DefaultSettings, GraphSettings, TreeSettings
from windows import RoundedWindow
from log import LogWidget


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

    def layout_group(self, layout_cls, widgets) -> Union[QLayout, QHBoxLayout, QVBoxLayout]:
        layout = layout_cls(self)
        for widget in widgets:
            if isinstance(widget, QWidget):
                layout.addWidget(widget)
            elif isinstance(widget, QLayoutItem):
                layout.addItem(widget)
        return layout

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
        self.graphics_view: GraphView
        # init widget
        self.__init_graphics_tool_widget()
        self.switch_model(0)

        # signal connect slot
        self.graphics_view.log.connect(self.log_widget.add)
        self.graphics_view.clickedItem.connect(self.switch_model)
        self.graphics_view.itemInfo.connect(self.set_info)

        self.combobox_edge.currentTextChanged.connect(self.graphics_view.change_line_type)

        self.line_edit_name.textEdited.connect(self.graphics_view.set_node_name)
        self.line_edit_weight.textEdited.connect(self.graphics_view.set_line_weight)

    def switch_model(self, model: int) -> None:
        """
        if model is 0, show edge info
        if model is 1, show node info
        """
        def show_widget(widgets: list[QWidget]):
            for widget in widgets:
                widget.show()

        def hide_widget(widgets: list[QWidget]):
            for widget in widgets:
                widget.hide()

        # edge info widgets
        edge = [self.label_start, self.label_end, self.label_edge, self.label_weight,
                self.line_edit_start, self.line_edit_end, self.line_edit_weight, self.combobox_edge]
        # node info widgets
        node = [self.label_name, self.line_edit_name]

        if model == 0:
            show_widget(edge)
            hide_widget(node)
        elif model == 1:
            show_widget(node)
            hide_widget(edge)

    def set_info(self, start: str, end: str, weight: str, edge: str, name: str):
        self.line_edit_start.setText(start)
        self.line_edit_end.setText(end)
        self.line_edit_weight.setText(weight)
        self.combobox_edge.setText(edge)
        self.line_edit_name.setText(name)

    def __init_menu_widget(self):
        pass

    def __init_graphics_tool_widget(self):
        def set_label_size(lab: QLabel):
            fm = lab.fontMetrics()
            width = fm.horizontalAdvance(lab.text())
            height = fm.height() + 10
            lab.setMinimumSize(width, height)
            lab.setMaximumHeight(height)

        # init font
        font_title = QFont()
        font_title.setFamily("Segoe")
        font_title.setPointSize(20)
        font_title.setBold(True)
        font = QFont()
        font.setFamily("Segoe")
        font.setPointSize(15)

        # init widget
        self.label_log = QLabel("Log", self)  # label log
        self.label_log.setFont(font_title)
        self.label_log.setAlignment(Qt.AlignCenter)
        set_label_size(self.label_log)
        self.log_widget = LogWidget(self)

        self.layout_info = QVBoxLayout()
        self.widget_info = QWidget(self)
        self.widget_info.setLayout(self.layout_info)

        self.label_info = QLabel("Info", self.widget_info)  # label info
        self.label_info.setAlignment(Qt.AlignCenter)
        self.label_info.setFont(font_title)
        set_label_size(self.label_info)

        self.label_name = QLabel("Name  ", self.widget_info)  # label name

        self.label_start = QLabel("Start ", self.widget_info)  # edge start
        self.label_end = QLabel("End   ", self.widget_info)  # edge end
        self.label_weight = QLabel("Weight", self.widget_info)  # edge weight
        self.label_edge = QLabel("Edge  ", self.widget_info)  # edge type
        labels = [self.label_name, self.label_weight, self.label_edge, self.label_start, self.label_end]
        for label in labels:
            set_label_size(label)
            label.setFont(font)

        self.line_edit_name = LineEdit(self.widget_info)
        self.line_edit_start = LineEdit(self.widget_info)
        self.line_edit_end = LineEdit(self.widget_info)
        self.line_edit_weight = LineEdit(self.widget_info)
        self.combobox_edge = ComboBox(self.widget_info)

        # init line edit
        self.line_edit_name.setPlaceholderText("name")
        self.line_edit_start.setPlaceholderText("start")
        self.line_edit_start.setReadOnly(True)
        self.line_edit_end.setPlaceholderText("end")
        self.line_edit_end.setReadOnly(True)
        self.line_edit_weight.setPlaceholderText("weight")

        # init combobox
        self.combobox_edge.addItems(["Line", "LineWithWeight", "ArrowLine", "ArrowLineWithWeight"])  # edge type
        self.combobox_edge.setText("ArrowLineWithWeight")

        # init layout group
        layout_start = self.layout_group(QHBoxLayout, [self.label_start, self.line_edit_start])
        layout_end = self.layout_group(QHBoxLayout, [self.label_end, self.line_edit_end])
        layout_weight = self.layout_group(QHBoxLayout, [self.label_weight, self.line_edit_weight])
        layout_edge = self.layout_group(QHBoxLayout, [self.label_edge,
                                                      self.combobox_edge,
                                                      QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)])
        layout_name = self.layout_group(QHBoxLayout, [self.label_name, self.line_edit_name])

        # add to layout
        self.add_to_graphics_tool_layout(self.widget_info)
        self.layout_info.addWidget(self.label_info)
        self.layout_info.addLayout(layout_start)
        self.layout_info.addLayout(layout_end)
        self.layout_info.addLayout(layout_weight)
        self.layout_info.addLayout(layout_edge)
        self.layout_info.addLayout(layout_name)

        self.add_to_graphics_tool_layout(self.label_log)  # log
        self.add_to_graphics_tool_layout(self.log_widget)


if __name__ == '__main__':
    import sys
    from PySide6.QtWidgets import QApplication

    app = QApplication(sys.argv)
    window = GraphDataStructure()
    window.show()
    sys.exit(app.exec())
