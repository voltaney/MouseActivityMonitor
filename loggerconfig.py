import logging.config

import yaml
from PySide6.QtCore import QFile, QIODevice, QTextStream


def load_yaml_config(yaml_path):
    logger_config_file = QFile(yaml_path)
    if not logger_config_file.open(QIODevice.ReadOnly | QIODevice.Text):
        raise RuntimeError("Failed to load logger config.")
    yaml_txt = QTextStream(logger_config_file).readAll()
    logging.config.dictConfig(yaml.safe_load(yaml_txt))