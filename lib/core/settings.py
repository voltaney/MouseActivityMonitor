from PySide6.QtCore import QSettings


class SETTINGS:
    RUNTIME_INI_PATH: str = "runtime.ini"
    SETTING_INI_PATH: str = "setting.ini"
    MOUSE_DPI: int = 1000

    @classmethod
    def load_setting_file(cls):
        qset = QSettings(cls.SETTING_INI_PATH, QSettings.Format.IniFormat)
        val = qset.value("MOUSE_DPI", type=int)
        if val != 0:
            cls.MOUSE_DPI = val
