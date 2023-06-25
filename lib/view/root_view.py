import math

from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtWidgets import *

from ..core.raw_mouse_monitor import MouseMonitor


class MainWindow(QWidget):
    def __init__(self) -> None:
        super().__init__()
        self.setWindowFlag(Qt.WindowType.WindowStaysOnTopHint)
        vbox = QVBoxLayout()
        self.mouse_label = QLabel()
        vbox.addWidget(self.mouse_label)
        self.mouse_sqrt_label = QLabel()
        vbox.addWidget(self.mouse_sqrt_label)
        self.mouse_total_move_label = QLabel()
        vbox.addWidget(self.mouse_total_move_label)
        self.mouse_total_left_clicks_label = QLabel()
        vbox.addWidget(self.mouse_total_left_clicks_label)
        hbox = QHBoxLayout()
        self.start_button = QPushButton("start")
        self.start_button.clicked.connect(self.start_monitor)
        self.cancel_monitor = QPushButton("cancel")
        hbox.addWidget(self.start_button)
        hbox.addWidget(self.cancel_monitor)
        vbox.addLayout(hbox)
        self.setLayout(vbox)

        self._total_move = 0
        self._total_left_clicks = 0

    @Slot()
    def start_monitor(self):
        self._thread = QThread()
        self._worker = MouseMonitor()
        self._worker.moveToThread(self._thread)
        self._thread.started.connect(self._worker.run)
        self.cancel_monitor.clicked.connect(self.stop)
        self._worker.mouseMoved.connect(self.change_mouse_text)
        self._worker.mouseLeftClicked.connect(self.change_mouse_left_click_text)
        self._worker.finished.connect(self._thread.quit)
        self._thread.finished.connect(self._worker.deleteLater)
        self._thread.finished.connect(self._thread.deleteLater)
        self._thread.start()

    @Slot()
    def change_mouse_text(self, x, y):
        self.mouse_label.setText(f"x: {x}, y: {y}")
        dist = math.sqrt(x**2 + y**2)
        self.mouse_sqrt_label.setText(f"dist: {dist}")
        self._total_move += dist
        self.mouse_total_move_label.setText(f"total: {int(self._total_move)}")

    @Slot()
    def change_mouse_left_click_text(self):
        self._total_left_clicks += 1
        self.mouse_total_left_clicks_label.setText(f"left click: {self._total_left_clicks}")

    @Slot()
    def stop(self):
        self._worker.cancel()
