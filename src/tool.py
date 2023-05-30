import json
import os

from PySide6.QtCore import QTime, QCoreApplication, QEventLoop
from PySide6.QtGui import QColor
from typing import Optional

import path


class ColorTool:
    __string_to_QColor = {
        'red': QColor(255, 0, 0),
        'black': QColor(0, 0, 0),
        'yellow': QColor(255, 255, 0),
        'white': QColor(255, 255, 255),
        'gray': QColor(192, 192, 192),
        'cyan': QColor(0, 255, 255),
        'blue': QColor(58, 143, 192),
        'green': QColor(0, 255, 0)
    }

    @classmethod
    def string_to_QColor(cls, name: str) -> QColor:
        """将字符串转换成对应的QColor"""
        if name not in cls.__string_to_QColor:
            raise TypeError(f"{name} not in dictionary")
        return cls.__string_to_QColor[name]


class PathTool:
    root_path = os.path.abspath(__file__)  # 根目录
    while (name := root_path.split("\\"))[-1] != "Data-SGV":
        root_path = os.path.dirname(root_path)

    @classmethod
    def get_setting_json_path(cls) -> str:
        return path.setting_json_path

    @classmethod
    def get_setting_json(cls) -> dict:
        with open(cls.get_setting_json_path(), 'r') as f:
            file = json.load(f)
        return file


class JsonTool:
    pass


class JsonSettingTool(JsonTool):
    @classmethod
    def save_json(cls, dic: dict):
        with open(PathTool.get_setting_json_path(), 'w') as f:
            json.dump(dic, f)

    @classmethod
    def animation_speed(cls) -> float:
        """返回秒"""
        with open(PathTool.get_setting_json_path(), 'r') as f:
            file = json.load(f)
        time = file['global']['animation_speed']
        return time

    @classmethod
    def log_animation_speed(cls) -> float:
        """返回秒"""
        with open(PathTool.get_setting_json_path(), 'r') as f:
            file = json.load(f)
        time = file['global']['log_animation_speed']
        return time


def stop_time(second: Optional[int] = None, millisecond: Optional[int] = None) -> None:
    """state: False -> second, True -> millisecond"""
    if second:
        end_time = QTime.currentTime().addSecs(second)
        while QTime.currentTime() < end_time:
            QCoreApplication.processEvents(QEventLoop.AllEvents, 100)
    elif millisecond:
        end_time = QTime.currentTime().addMSecs(millisecond)
        while QTime.currentTime() < end_time:
            QCoreApplication.processEvents(QEventLoop.AllEvents, 100)
    else:
        raise AttributeError("Must enter seconds or milliseconds")


if __name__ == "__main__":
    print(JsonSettingTool.animation_speed())
