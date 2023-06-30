from typing import Union

from PySide6.QtCore import Signal, Qt, QSize
from PySide6.QtGui import QFont, QColor, QPainter
from PySide6.QtWidgets import QVBoxLayout, QWidget, QLayout, QLayoutItem, QHBoxLayout, QSpacerItem, QSizePolicy, QLabel, \
    QGraphicsDropShadowEffect
from qfluentwidgets import ToolButton, FluentIcon, LineEdit, ComboBox, PushButton, Dialog, MessageBox

from src.widgets.graphics_view import MyGraphicsView, BinaryTreeView, GraphView, SegmentTreeView
from src.widgets.settings import DefaultSettings, GraphSettings, TreeSettings, SegmentTreeSettings
from src.widgets.window import RoundMainWindow
from src.widgets.log import LogWidget

from src.auxiliary_function import layout_add_obj, layout_add_bojs, label_minimum_size

font_title = QFont()
font_title.setFamily("Segoe")
font_title.setPointSize(20)
font_title.setBold(True)
font = QFont()
font.setFamily("Segoe")
font.setPointSize(13)


class DataStructureWidget(RoundMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)

    def __init_graphics_tool_widget(self):
        """init graphics tool widget"""
        raise NotImplementedError


class DataStructureWindow(DataStructureWidget):
    openSetting = Signal()
    closeSetting = Signal()

    def __init__(self, parent=None, setting_w=DefaultSettings, graphics_w=MyGraphicsView):
        super().__init__(parent)
        # init widget
        self.setting_widget = setting_w(self)
        self.setting_widget.hide()
        self.graphics_view = graphics_w()
        self.__init_graphics_widget()
        self.setMinimumSize(QSize(800, 600))
        self.resize(1000, 600)

        # init title bar widget
        self.t_setting = ToolButton(FluentIcon.SETTING, self.title_bar)
        self.i_setting = ToolButton(FluentIcon.INFO, self.title_bar)

        # signal connect slot
        self.t_setting.clicked.connect(self.maskShow)
        self.t_setting.clicked.connect(self.openSetting)
        self.maskHide.connect(self.closeSetting)

        # add to title bar layout
        self.title_bar.left_add_obj(self.t_setting)
        self.title_bar.left_add_obj(self.i_setting)

    def add_to_graphics_tool_layout(self, obj: Union[QWidget, QLayout, QLayoutItem]):
        layout_add_obj(self.layout_graphics_tools, obj)

    def layout_group(self, layout_cls, widgets) -> Union[QLayout, QHBoxLayout, QVBoxLayout]:
        layout = layout_cls(self)
        for widget in widgets:
            if isinstance(widget, QWidget):
                layout.addWidget(widget)
            elif isinstance(widget, QLayoutItem):
                layout.addItem(widget)
        return layout

    def show_dialog(self, title, text):
        dialog = Dialog(title, text)
        dialog.show()

    def show_messagebox(self, title, text):
        messagebox = MessageBox(title, text, self)
        messagebox.show()

    def __init_graphics_widget(self):
        # init layout
        self.layout_title = QHBoxLayout()
        self.layout_title.setContentsMargins(10, 10, 10, 10)
        self.layout_graphics = QHBoxLayout()
        self.layout_graphics.setContentsMargins(10, 10, 10, 10)
        self.layout_graphics_tools = QVBoxLayout()
        self.layout_graphics_tools.setSpacing(10)
        self.layout_graphics_tools.setContentsMargins(10, 0, 0, 0)

        # init graphics view
        self.graphics_view.setParent(self)

        # add to layout
        self.layout_graphics.addWidget(self.graphics_view, 3)
        self.layout_graphics.addLayout(self.layout_graphics_tools, 1)
        self.layout_main.addLayout(self.layout_title)
        self.layout_main.addLayout(self.layout_graphics)

    def __init_graphics_tool_widget(self):
        raise NotImplementedError


class TreeDataStructure(DataStructureWindow):
    def __init__(self, parent=None):
        super().__init__(parent, TreeSettings, BinaryTreeView)
        self.graphics_view: BinaryTreeView

        self.__init_title()
        self.__init_graphics_tool_widget()

        # signal connect slot
        self.line_edit_add.editingFinished.connect(self.button_add.clicked)
        self.line_edit_delete.editingFinished.connect(self.button_delete.clicked)
        self.line_edit_search.editingFinished.connect(self.button_search.clicked)

        self.button_add.clicked.connect(self._add_node)
        self.button_delete.clicked.connect(self._delete_node)
        self.button_search.clicked.connect(self._search_node)

        self.graphics_view.diaLog.connect(self.show_dialog)
        self.graphics_view.log.connect(self.log_widget.add)

        self.setting_widget.saved.connect(self.graphics_view.config)

    def _add_node(self):
        self.graphics_view: BinaryTreeView

        self.graphics_view.redraw()
        val = self.line_edit_add.text()
        val = val.split(',')
        self.line_edit_add.clear()
        self.graphics_view.add_node(val)

    def _delete_node(self):
        self.graphics_view: BinaryTreeView

        self.graphics_view.redraw()
        val = self.line_edit_delete.text()
        self.line_edit_delete.clear()
        self.graphics_view.delete_node(val)

    def _search_node(self):
        self.graphics_view: BinaryTreeView

        self.graphics_view.redraw()
        val = self.line_edit_search.text()
        self.line_edit_search.clear()
        self.graphics_view.search_node(val)

    def __init_menu_widget(self):
        pass

    def __init_title(self):
        label = QLabel("Binary Search Tree", self)
        font = QFont("Segoe", 30)
        font.setBold(True)
        label.setFont(font)
        self.layout_title.addWidget(label)

    def __init_graphics_tool_widget(self):
        # init font
        font = QFont("Segoe", 15)
        font_title = QFont("Segoe", 20)
        font_title.setBold(True)

        # init widget
        label_add = QLabel("Add Node", self)
        label_add.setFont(font)
        self.line_edit_add = LineEdit(self)
        self.line_edit_add.setPlaceholderText("Val")
        self.button_add = PushButton("Add", self)
        layout_add = self.layout_group(QHBoxLayout, [label_add, self.line_edit_add, self.button_add])

        label_delete = QLabel("Delete Node", self)
        label_delete.setFont(font)
        self.line_edit_delete = LineEdit(self)
        self.line_edit_delete.setPlaceholderText("Val")
        self.button_delete = PushButton("Delete", self)
        layout_delete = self.layout_group(QHBoxLayout, [label_delete, self.line_edit_delete, self.button_delete])

        label_search = QLabel("Search Node", self)
        label_search.setFont(font)
        self.line_edit_search = LineEdit(self)
        self.line_edit_search.setPlaceholderText("Val")
        self.button_search = PushButton("Search", self)
        layout_search = self.layout_group(QHBoxLayout, [label_search, self.line_edit_search, self.button_search])

        self.button_preorder = PushButton("Preorder", self)

        self.button_inorder = PushButton("Inorder", self)

        self.button_postorder = PushButton("Postorder", self)

        self.button_bfs = PushButton("BFS", self)

        label_log = QLabel("Log", self)
        label_log.setFont(font_title)
        label_log.setAlignment(Qt.AlignCenter)
        self.log_widget = LogWidget(self)

        # add to layout
        self.add_to_graphics_tool_layout(layout_add)
        self.add_to_graphics_tool_layout(layout_delete)
        self.add_to_graphics_tool_layout(layout_search)
        self.add_to_graphics_tool_layout(self.button_preorder)
        self.add_to_graphics_tool_layout(self.button_inorder)
        self.add_to_graphics_tool_layout(self.button_postorder)
        self.add_to_graphics_tool_layout(self.button_bfs)
        self.add_to_graphics_tool_layout(label_log)
        self.add_to_graphics_tool_layout(self.log_widget)


class GraphDataStructure(DataStructureWindow):
    def __init__(self, parent=None):
        super().__init__(parent, GraphSettings, GraphView)
        self.graphics_view: GraphView
        # init widget
        self.__init_graphics_tool_widget()
        self.__init_title()
        self.switch_model(0)

        # signal connect slot
        self.graphics_view.log.connect(self.log_widget.add)
        self.graphics_view.clickedItem.connect(self.switch_model)
        self.graphics_view.nodeInfo.connect(self.set_info)
        self.graphics_view.edgeInfo.connect(self.set_info)
        self.graphics_view.diaLog.connect(self.show_dialog)

        self.combobox_edge.currentTextChanged.connect(self.graphics_view.change_edge_type)

        self.line_edit_name.textEdited.connect(self.graphics_view.set_node_name)
        self.line_edit_weight.textEdited.connect(self.graphics_view.set_line_weight)

        self.button_delete.clicked.connect(self.graphics_view.delete)

        self.button_dfs.clicked.connect(self.log_widget.clear)
        self.button_dfs.clicked.connect(self.graphics_view.dfs)

        self.button_bfs.clicked.connect(self.log_widget.clear)
        self.button_bfs.clicked.connect(self.graphics_view.bfs)

        self.button_dijkstra.clicked.connect(self.log_widget.clear)
        self.button_dijkstra.clicked.connect(self.graphics_view.dijkstra)

        self.setting_widget.saved.connect(self.graphics_view.config)

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
        node = [self.label_name, self.line_edit_name,
                self.button_dfs, self.button_bfs, self.button_dijkstra]

        if model == 0:
            show_widget(edge)
            hide_widget(node)
        elif model == 1:
            show_widget(node)
            hide_widget(edge)

    def set_info(self, typ, *args):
        if typ == 0:
            name, *_ = args
            self.line_edit_name.setText(name)
        elif typ == 1:
            start, end, weight, edge = args
            self.line_edit_start.setText(start)
            self.line_edit_end.setText(end)
            self.line_edit_weight.setText(weight)
            self.combobox_edge.setCurrentText(edge)

    def __init_menu_widget(self):
        pass

    def __init_title(self):
        _font_title = QFont()
        _font_title.setPointSize(30)
        _font_title.setFamily("Segoe")
        _font_title.setBold(True)
        title = QLabel(" Graph", self)
        title.setFont(_font_title)
        self.layout_title.addWidget(title)

    def __init_graphics_tool_widget(self):
        # init widget
        self.label_log = QLabel("Log", self)  # label log
        self.label_log.setFont(font_title)
        self.label_log.setAlignment(Qt.AlignCenter)
        label_minimum_size(self.label_log)
        self.log_widget = LogWidget(self)

        self.layout_info = QVBoxLayout()
        self.widget_info = QWidget(self)
        self.widget_info.setLayout(self.layout_info)
        self.widget_info.setStyleSheet("""
        border-radius:8px;
        background-color: rgb(255, 255, 255);
        """)

        self.label_info = QLabel("Info", self)  # label info
        self.label_info.setAlignment(Qt.AlignCenter)
        self.label_info.setFont(font_title)
        label_minimum_size(self.label_info)

        self.label_name = QLabel("Name  ", self.widget_info)  # label name

        self.label_start = QLabel("Start ", self.widget_info)  # edge start
        self.label_end = QLabel("End   ", self.widget_info)  # edge end
        self.label_weight = QLabel("Weight", self.widget_info)  # edge weight
        self.label_edge = QLabel("Edge  ", self.widget_info)  # edge type
        labels = [self.label_name, self.label_weight, self.label_edge, self.label_start, self.label_end]
        for label in labels:
            label_minimum_size(label)
            label.setFont(font)

        self.line_edit_name = LineEdit(self.widget_info)
        self.line_edit_start = LineEdit(self.widget_info)
        self.line_edit_end = LineEdit(self.widget_info)
        self.line_edit_weight = LineEdit(self.widget_info)
        self.combobox_edge = ComboBox(self.widget_info)

        self.button_delete = PushButton(self.widget_info)
        self.button_dfs = PushButton(self.widget_info)
        self.button_bfs = PushButton(self.widget_info)
        self.button_dijkstra = PushButton(self.widget_info)

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

        # init button
        self.button_delete.setText("Delete")
        self.button_dfs.setText("DFS")
        self.button_bfs.setText("BFS")
        self.button_dijkstra.setText("Dijkstra")

        # init layout group
        layout_start = self.layout_group(QHBoxLayout, [self.label_start, self.line_edit_start])
        layout_end = self.layout_group(QHBoxLayout, [self.label_end, self.line_edit_end])
        layout_weight = self.layout_group(QHBoxLayout, [self.label_weight, self.line_edit_weight])
        layout_edge = self.layout_group(QHBoxLayout, [self.label_edge,
                                                      self.combobox_edge,
                                                      QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)])
        layout_name = self.layout_group(QHBoxLayout, [self.label_name, self.line_edit_name])

        # add to layout
        self.add_to_graphics_tool_layout(self.label_info)
        self.add_to_graphics_tool_layout(self.widget_info)
        self.layout_info.addLayout(layout_start)
        self.layout_info.addLayout(layout_end)
        self.layout_info.addLayout(layout_weight)
        self.layout_info.addLayout(layout_edge)
        self.layout_info.addLayout(layout_name)
        self.layout_info.addWidget(self.button_delete)
        self.layout_info.addWidget(self.button_dfs)
        self.layout_info.addWidget(self.button_bfs)
        self.layout_info.addWidget(self.button_dijkstra)

        self.add_to_graphics_tool_layout(self.label_log)  # log
        self.add_to_graphics_tool_layout(self.log_widget)


class SegmentTreeDataStructure(DataStructureWindow):
    def __init__(self, parent=None):
        super().__init__(parent, SegmentTreeSettings, SegmentTreeView)
        self.__init_title()
        self.__init_menu_widget()
        self.__init_graphics_tool_widget()

        # connect signal to slot
        self.button_create.clicked.connect(self.create_tree)
        self.button_create.clicked.connect(self.line_edit_create.clear)

        self.button_query.clicked.connect(self.range_query)
        self.button_query.clicked.connect(self.line_edit_l_query.clear)
        self.button_query.clicked.connect(self.line_edit_r_query.clear)

        self.button_update.clicked.connect(self.range_update)
        self.button_update.clicked.connect(self.line_edit_l_update.clear)
        self.button_update.clicked.connect(self.line_edit_r_update.clear)
        self.button_update.clicked.connect(self.line_edit_v_update.clear)

        self.graphics_view.log.connect(self.log_widget.append)

    def create_tree(self):
        self.graphics_view: SegmentTreeView
        arr = self.line_edit_create.text()
        arr = arr.replace("[", "")
        arr = arr.replace("]", "")
        try:
            arr = list(map(int, arr.split(",")))
        except ValueError:
            self.show_messagebox(
                title="Error",
                text="please input a number, split by comma. you can input 1,2,3, or 1, 2, 3, or [1, 2, 3]"
            )
            return
        self.graphics_view.make(arr)

    def range_query(self):
        self.graphics_view: SegmentTreeView
        left = self.line_edit_l_query.text()
        right = self.line_edit_r_query.text()

        if not self._check(left, right):
            return

        self.graphics_view.get_sum(int(left), int(right))

    def range_update(self):
        self.graphics_view: SegmentTreeView
        left = self.line_edit_l_update.text()
        right = self.line_edit_r_update.text()
        val = self.line_edit_v_update.text()

        if not self._check(left, right) and not val.isdigit():
            return

        self.graphics_view.update_tree(int(left), int(right), int(val))

    def _check(self, left, right) -> bool:
        self.graphics_view: SegmentTreeView
        if self.graphics_view.built is False:
            self._not_tree_message()
            return False
        if left == "" or right == "":
            self._empty_message()
            return False
        if not (left.isdigit() and right.isdigit()):
            self._not_a_number()
            return False

        return True

    def _empty_message(self):
        self.show_messagebox(
            title="Error",
            text="left or right can't empty"
        )

    def _not_tree_message(self):
        self.show_messagebox(
            title="Error",
            text="you must create a tree"
        )

    def _not_a_number(self):
        self.show_messagebox(
            title="Error",
            text="left or right is not a number"
        )

    def __init_menu_widget(self):
        pass

    def __init_graphics_tool_widget(self):
        # create tree
        layout_create = QHBoxLayout()
        self.line_edit_create = LineEdit(self)
        layout_create.addWidget(self.line_edit_create)

        self.button_create = PushButton("Create Tree", self)
        layout_create.addWidget(self.button_create)

        # range query
        layout_query = QHBoxLayout()
        label_l_query = QLabel("Left:", self)
        label_l_query.setFont(font)
        label_r_query = QLabel("Right:", self)
        label_r_query.setFont(font)

        self.line_edit_l_query = LineEdit(self)
        self.line_edit_r_query = LineEdit(self)

        self.button_query = PushButton("Range Query  ", self)

        layout_query.addWidget(label_l_query)
        layout_query.addWidget(self.line_edit_l_query)
        layout_query.addWidget(label_r_query)
        layout_query.addWidget(self.line_edit_r_query)
        layout_query.addWidget(self.button_query)

        # range update
        layout_update = QHBoxLayout()
        label_l_update = QLabel("Left:", self)
        label_l_update.setFont(font)
        label_r_update = QLabel("Right:", self)
        label_r_update.setFont(font)
        label_v_update = QLabel("Val:", self)
        label_v_update.setFont(font)

        self.line_edit_l_update = LineEdit(self)
        self.line_edit_r_update = LineEdit(self)
        self.line_edit_v_update = LineEdit(self)

        self.button_update = PushButton("Range Update", self)

        layout_update.addWidget(label_l_update)
        layout_update.addWidget(self.line_edit_l_update)
        layout_update.addWidget(label_r_update)
        layout_update.addWidget(self.line_edit_r_update)
        layout_update.addWidget(label_v_update)
        layout_update.addWidget(self.line_edit_v_update)
        layout_update.addWidget(self.button_update)

        # log widget
        layout_log = QVBoxLayout()
        label_log = QLabel("Log", self)
        label_log.setFont(font_title)
        label_log.setAlignment(Qt.AlignCenter)

        self.log_widget = LogWidget(self)

        layout_log.addWidget(label_log)
        layout_log.addWidget(self.log_widget)

        # set label mini size
        labels = [label_log, label_r_update, label_l_update, label_r_query, label_l_query]
        for label in labels:
            label_minimum_size(label)

        # add to layout
        self.add_to_graphics_tool_layout(layout_create)
        self.add_to_graphics_tool_layout(layout_query)
        self.add_to_graphics_tool_layout(layout_update)
        self.add_to_graphics_tool_layout(layout_log)

    def __init_title(self):
        _font_title = QFont()
        _font_title.setPointSize(30)
        _font_title.setFamily("Segoe")
        _font_title.setBold(True)
        title = QLabel("Segment Tree", self)
        title.setFont(_font_title)
        self.layout_title.addWidget(title)


if __name__ == '__main__':
    import sys
    from PySide6.QtWidgets import QApplication

    app = QApplication(sys.argv)
    window1 = SegmentTreeDataStructure()
    window1.show()
    # window2 = GraphDataStructure()
    # window2.show()
    sys.exit(app.exec())
