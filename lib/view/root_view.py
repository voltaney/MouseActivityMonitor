import math
from logging import getLogger

from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtGui import QCloseEvent
from PySide6.QtWidgets import *

from ..core.raw_mouse_monitor import MouseMonitor
from .frameless_window import FramelessWindow

logger = getLogger(__name__)


class MainWindow(FramelessWindow):
    def __init__(self) -> None:
        super().__init__()
        self.setWindowFlag(Qt.WindowType.WindowStaysOnTopHint)
        info_vbox = QVBoxLayout()
        info_vbox.setSpacing(0)
        self._mouse_label = QLabel("0")
        self._mouse_label.setObjectName("mouseData")
        self._mouse_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self._mouse_label.setFixedHeight(60)
        m_unit_label = QLabel("[cm]")
        m_unit_label.setObjectName("mouseUnit")
        m_head = QLabel("Mouse move distance")
        m_head.setObjectName("mouseHeader")
        m_head.setAlignment(Qt.AlignmentFlag.AlignCenter)
        info_vbox.addWidget(m_head)
        mouse_box = QHBoxLayout()
        mouse_box.setContentsMargins(0, 0, 0, 0)
        mouse_box.addWidget(self._mouse_label)
        mouse_box.addWidget(m_unit_label)
        mouse_box.setAlignment(Qt.AlignmentFlag.AlignCenter)
        info_vbox.addLayout(mouse_box)

        self._left_click_label = QLabel("0")
        self._left_click_label.setObjectName("leftClickData")
        self._left_click_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self._left_click_label.setFixedHeight(60)
        lc_head = QLabel("Left click")
        lc_head.setObjectName("leftClickHeader")
        lc_head.setAlignment(Qt.AlignmentFlag.AlignCenter)
        info_vbox.addWidget(lc_head)
        info_vbox.addWidget(self._left_click_label)

        self.stacked_layout = QStackedLayout()
        hbox = QHBoxLayout()
        self.start_button = QPushButton("Start")
        self.start_button.setObjectName("startButton")
        self.start_button.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        self.start_button.clicked.connect(self.start_monitor)
        hbox.addWidget(self.start_button)

        info_wrapper = QWidget()
        info_wrapper.setLayout(info_vbox)
        btn_wrapper = QWidget()
        btn_wrapper.setLayout(hbox)
        self.stacked_layout.addWidget(info_wrapper)
        self.stacked_layout.addWidget(btn_wrapper)
        self.stacked_layout.setCurrentIndex(1)

        self.setLayout(self.stacked_layout)

        self._total_move = 0
        self._total_left_clicks = 0
        self._worker = None

    @Slot()
    def start_monitor(self):
        self.stacked_layout.setCurrentIndex(0)
        self._thread = QThread()
        self._worker = MouseMonitor()
        self._worker.moveToThread(self._thread)
        self._thread.started.connect(self._worker.run)
        self._worker.mouseMoved.connect(self.change_mouse_text)
        self._worker.mouseLeftClicked.connect(self.change_mouse_left_click_text)
        self._worker.finished.connect(self._thread.quit)
        self._thread.finished.connect(self._worker.deleteLater)
        self._thread.finished.connect(self._thread.deleteLater)
        self._thread.start()

    @Slot()
    def change_mouse_text(self, x, y):
        dpi = 1600
        dist = math.sqrt(x**2 + y**2)
        self._total_move += dist
        self._mouse_label.setText("{:,.0f}".format(float(self._total_move) / dpi * 2.54))

    @Slot()
    def change_mouse_left_click_text(self):
        self._total_left_clicks += 1
        self._left_click_label.setText(f"{self._total_left_clicks}")

    def closeEvent(self, event: QCloseEvent) -> None:
        super().closeEvent(event)
        if self._worker is not None:
            self._worker.cancel()
            # threadが終了するのを待つ
            logger.info("Waiting thread to be finished")
            self._thread.wait()
