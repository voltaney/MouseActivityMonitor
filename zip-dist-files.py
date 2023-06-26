import shutil
import zipfile
from pathlib import Path

DIST_PACKAGE_PATH = "dist-php/public_html/dist"
DIST_PATH = "dist"

Path(DIST_PACKAGE_PATH).mkdir(exist_ok=True)

with zipfile.ZipFile(
    Path(DIST_PACKAGE_PATH) / "MouseActivityMonitor.zip", "w", compression=zipfile.ZIP_DEFLATED, compresslevel=9
) as zf:
    zf.write(Path(DIST_PATH) / "Mouse Activity Monitor.exe", arcname="Mouse Activity Monitor.exe")
