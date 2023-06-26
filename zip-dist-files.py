import shutil
import zipfile
from pathlib import Path

DIST_PATH = "dist"
SETTING_INI = "setting.ini"

Path(DIST_PATH).mkdir(exist_ok=True)

with zipfile.ZipFile(
    Path(DIST_PATH) / "MouseActivityMonitor.zip", "w", compression=zipfile.ZIP_DEFLATED, compresslevel=9
) as zf:
    zf.write(Path(DIST_PATH) / "Mouse Activity Monitor.exe", arcname="Mouse Activity Monitor.exe")
    zf.write(SETTING_INI, arcname="setting.ini")
