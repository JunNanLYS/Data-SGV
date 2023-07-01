from typing import Union

from PySide6.QtWidgets import QLayout, QWidget, QLayoutItem, QLabel


def layout_add_obj(layout: QLayout, obj: Union[QWidget, QLayout, QLayoutItem]):
    if isinstance(obj, QWidget):
        layout.addWidget(obj)
    elif isinstance(obj, QLayout):
        layout.addLayout(obj)
    elif isinstance(obj, QLayoutItem):
        layout.addItem(obj)


def layout_add_bojs(layout: QLayout, objs: list):
    for obj in objs:
        layout_add_obj(layout, obj)


def layout_group(layout_cls, objs: list):
    """
    layout_cls: Union[QHBoxLayout, QVBoxLayout]
    objs: list
    return: QLayout
    """
    layout = layout_cls()
    layout_add_bojs(layout, objs)
    return layout


def label_minimum_size(lab: QLabel):
    """Set label to the minimum state that does not affect the font"""
    fm = lab.fontMetrics()
    width = fm.horizontalAdvance(lab.text())
    height = fm.height() + 10
    lab.setMinimumSize(width, height)
    lab.setMaximumHeight(height)
