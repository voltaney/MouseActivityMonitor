from pathlib import Path

from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtWidgets import *

from ..core.settings import SETTINGS


class FramelessWindow(QWidget):
    def __init__(self) -> None:
        super().__init__()
        self.resize(800, 600)
        self._is_moving = False
        self._is_frameless = False
        self._is_always_on_top = False

        if Path(SETTINGS.RUNTIME_INI_PATH).is_file():
            settings = QSettings(SETTINGS.RUNTIME_INI_PATH, QSettings.Format.IniFormat)
            self.restoreGeometry(settings.value("windowGeometry"))
            self._set_always_on_top(settings.value("alwaysOnTop", type=bool))
            self._set_frameless(settings.value("frameless", type=bool))

    # 左クリックによるウィンドウの移動制御
    def mousePressEvent(self, event: QMouseEvent) -> None:
        if event.button() == Qt.MouseButton.LeftButton:
            self._press_pos = event.position()
            self._is_moving = True

    def mouseMoveEvent(self, event: QMouseEvent) -> None:
        if self._is_moving:
            diff = event.position() - self._press_pos
            self.move(self.pos() + diff.toPoint())

    def mouseReleaseEvent(self, event: QMouseEvent) -> None:
        if event.button() == Qt.MouseButton.LeftButton:
            self._is_moving = False

    def _create_context_menu(self):
        self._menu = QMenu()
        # Util menu
        frameless_act = QAction("Frameless(can't resize)", self)
        frameless_act.setCheckable(True)
        frameless_act.setChecked(self._is_frameless)
        frameless_act.triggered.connect(lambda checked: self._set_frameless(checked))
        self._menu.addAction(frameless_act)
        always_top_act = QAction("Always on top", self)
        always_top_act.setCheckable(True)
        always_top_act.setChecked(self._is_always_on_top)
        always_top_act.triggered.connect(lambda checked: self._set_always_on_top(checked))
        self._menu.addAction(always_top_act)
        close_act = QAction("Quit", self)
        close_act.triggered.connect(lambda: self.close())
        self._menu.addAction(close_act)

    def _set_always_on_top(self, on_top: bool):
        self._is_always_on_top = on_top
        # WindowFlag系の内部で呼ばれるgetParent()によりinvisibleになるため、
        # show()の呼び出し必須。
        if on_top:
            geo = self.geometry()
            self.setWindowFlag(Qt.WindowType.WindowStaysOnTopHint)
            self.setGeometry(geo)
            self.show()
        else:
            geo = self.geometry()
            self.setWindowFlags(self.windowFlags() & ~Qt.WindowType.WindowStaysOnTopHint)
            self.setGeometry(geo)
            self.show()

    def _set_frameless(self, frameless: bool):
        self._is_frameless = frameless
        # WindowFlag系の内部で呼ばれるgetParent()によりinvisibleになるため、
        # show()の呼び出し必須。
        if frameless:
            geo = self.geometry()
            self.setWindowFlag(Qt.WindowType.FramelessWindowHint)
            self.setGeometry(geo)
            self.show()
        else:
            geo = self.geometry()
            self.setWindowFlags(self.windowFlags() & ~Qt.WindowType.FramelessWindowHint)
            self.setGeometry(geo)
            self.show()

    def contextMenuEvent(self, event: QContextMenuEvent) -> None:
        self._create_context_menu()
        self._menu.popup(event.globalPos())

    def closeEvent(self, event: QCloseEvent) -> None:
        settings = QSettings(SETTINGS.RUNTIME_INI_PATH, QSettings.Format.IniFormat)
        settings.setValue("windowGeometry", self.saveGeometry())
        settings.setValue("alwaysOnTop", self._is_always_on_top)
        settings.setValue("frameless", self._is_frameless)


if __name__ == "__main__":
    app = QApplication()
    win = FramelessWindow()
    win.show()
    app.exec()
