import sys
from logging import getLogger

import qdarktheme
from PySide6.QtCore import QFile, QIODevice, QTextStream
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QApplication

import app_rc
from lib.view.root_view import MainWindow
from loggerconfig import load_yaml_config

logger = getLogger(__name__)


# Uncaughtな例外をログで表示するハンドラ
def handle_unhandled_exception(exc_type, exc_value, exc_traceback):
    if issubclass(exc_type, KeyboardInterrupt):
        sys.__excepthook__(exc_type, exc_value, exc_traceback)
        return
    logger.critical("Unhandled exception", exc_info=(exc_type, exc_value, exc_traceback))


sys.excepthook = handle_unhandled_exception

if __name__ == "__main__":
    # Config logger
    load_yaml_config(":/config/logger.yaml")

    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon(":/assets/app_icon.png"))

    stylefile = QFile(":/styles/app.qss")

    if not stylefile.open(QIODevice.ReadOnly | QIODevice.Text):
        logger.critical("Failed to apply qss styles")
    qsstext = QTextStream(stylefile).readAll()

    qdarktheme.setup_theme(custom_colors={"primary": "#D0BCFF"}, additional_qss=qsstext)

    window = MainWindow()
    window.show()
    app.exec()
