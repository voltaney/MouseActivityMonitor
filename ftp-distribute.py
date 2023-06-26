import ftplib

import yaml

with open("ftp-info.yaml", "r", encoding="utf-8") as f:
    data = yaml.safe_load(f)

ftp = ftplib.FTP(data["host"], data["username"], data["password"])
ftp.set_pasv(True)

target_base_dir = "MouseActivityMonitor"
version_txt = "version.txt"
zip_data = "dist-php/public_html/dist/MouseActivityMonitor.zip"
target_zip_name = "MouseActivityMonitor.zip"


with open(version_txt, "rb") as f:
    ftp.storlines(f"STOR /{target_base_dir}/{version_txt}", f)
with open(zip_data, "rb") as f:
    ftp.storlines(f"STOR /{target_base_dir}/dist/{target_zip_name}", f)

ftp.close()
