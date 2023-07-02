import time
from queue import Queue

from PySide6.QtCore import Qt, Signal, Slot, QPropertyAnimation, Property, QPoint, QMutexLocker, QMutex, \
    QAbstractAnimation, QCoreApplication, QEventLoop
from PySide6.QtGui import QFont, QTextCharFormat, QTextCursor, QColor
from PySide6.QtWidgets import QApplication, QWidget
from qfluentwidgets import PlainTextEdit, Dialog
from threading import Lock

from src.tool import stop_time
from src.animation_queue import AnimationQueue
from src import thread_pool


class LogWidget(PlainTextEdit):
    add = Signal(str)
    added = Signal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setReadOnly(True)  # only read
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setMinimumSize(50, 50)
        self.setMaximumSize(1000, 500)
        self.lock = QMutex()

        self.anim = QPropertyAnimation(self)
        self.animation_cursor = self.textCursor()

        # init font
        fmt = QTextCharFormat()
        fmt.setFontPointSize(12)
        self.mergeCurrentCharFormat(fmt)

        # signal connect slot
        self.add.connect(self.receive_message)

    def append(self, text):
        """新增Log"""
        self.append_animation(text)

        # signal transmit
        self.added.emit()

    @Slot(str)
    def receive_message(self, message: str):
        self.append(message)

    def append_animation(self, text):
        while self.anim.state() == QAbstractAnimation.Running:
            QCoreApplication.processEvents(QEventLoop.AllEvents, 100)
        cursor = self.textCursor()
        cursor.movePosition(QTextCursor.Start)
        cursor.insertText(text + '\n')
        cursor = self.textCursor()
        cursor.movePosition(QTextCursor.Start)
        cursor.movePosition(QTextCursor.EndOfLine, QTextCursor.KeepAnchor)
        self.animation(cursor)

    @Property(int)
    def transparency_animation(self):
        pass

    @transparency_animation.setter
    def transparency_animation(self, new):
        fmt = QTextCharFormat()
        fmt.setFontPointSize(12)
        fmt.setForeground(QColor(0, 0, 0, new))
        self.animation_cursor.mergeCharFormat(fmt)

    def animation(self, cursor):
        with QMutexLocker(self.lock):
            self.animation_cursor = cursor
            self.anim = QPropertyAnimation(self, b'transparency_animation')
            self.anim.setStartValue(0)
            self.anim.setEndValue(180)
            self.anim.setDuration(200)
            self.anim.start()


if __name__ == "__main__":
    app = QApplication([])
    window = QWidget()
    window.resize(800, 600)
    dig = Dialog("Error", "Type Error", window)
    log_widget = LogWidget(window)
    nums = [x for x in range(1, 50)]
    window.show()
    for num in nums:
        log_widget.add.emit(f"log{num}")
    app.exec()
