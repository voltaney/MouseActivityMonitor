<?
// パッケージパス
$package_path = 'dist/MouseActivityMonitor.zip';
if (!is_readable($package_path)) {
    die($package_path);
}
// バージョン番号取得
$version_file = 'version.txt';
if (!is_readable($version_file)) {
    die($version_file);
}
$f = fopen($version_file, 'r');
$line = fgets($f);
fclose($f);
$version = trim($line);
$package_path_parts = pathinfo($package_path);
$download_filename = $package_path_parts["filename"] . "-" . $version . ".zip";
header('Content-Type: application/zip');
header('Content-Length: ' . filesize($package_path));
header('Content-Disposition:attachment;filename="' . $download_filename . '"');
readfile($package_path);
