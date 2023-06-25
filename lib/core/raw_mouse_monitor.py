import ctypes as cts
import ctypes.wintypes as wts
from logging import getLogger

from PySide6.QtCore import *

from . import ctypes_wrappers as cws

WM_QUIT = 0x0012
WM_INPUT = 0x00FF
WM_CLOSE = 0x0010

HID_USAGE_PAGE_GENERIC = 0x01
HID_USAGE_GENERIC_MOUSE = 0x02

# https://learn.microsoft.com/ja-jp/windows/win32/api/winuser/ns-winuser-rawinputdevice
RIDEV_INPUTSINK = 0x00000100

# https://learn.microsoft.com/ja-jp/windows/win32/api/winuser/nf-winuser-getrawinputdata
RID_INPUT = 0x10000003

# マウスタイプ
RIM_TYPEMOUSE = 0


logger = getLogger(__name__)


def log_error_code(api_name: str):
    code = cws.GetLastError()
    logger.critical(f"{api_name} - error code: {code}")


class MouseMonitor(QObject):
    mouseMoved = Signal(int, int)
    finished = Signal()

    def __init__(self) -> None:
        super().__init__()
        # self._cancel = False

    def run(self):
        wnd_cls = "VOL_SIMPLE_MONITOR"
        wcx = cws.WNDCLASSEX()
        wcx.cbSize = cts.sizeof(cws.WNDCLASSEX)
        wcx.lpfnWndProc = cws.WNDPROC(self.wnd_proc)
        wcx.hInstance = cws.GetModuleHandle(None)
        wcx.lpszClassName = wnd_cls

        res = cws.RegisterClassEx(cts.byref(wcx))
        if not res:
            log_error_code("RegisterClassEx")
            self.finished.emit()
            return
        # ウィンドウなしmessage-window
        hwnd = cws.CreateWindowEx(0, wnd_cls, None, 0, 0, 0, 0, 0, 0, None, wcx.hInstance, None)
        self.hwnd = hwnd
        if not hwnd:
            log_error_code("CreateWindowEx")
            self.finished.emit()
            return
        if not self.register_devices(hwnd):
            self.finished.emit()
            return
        logger.info("window preparation done.")
        msg = wts.MSG()
        pmsg = cts.byref(msg)
        while res := cws.GetMessage(pmsg, None, 0, 0):
            if res < 0:
                log_error_code("GetMessage")
                break
            cws.TranslateMessage(pmsg)
            cws.DispatchMessage(pmsg)
        logger.info("monitoring finished!")
        self.finished.emit()

    def cancel(self):
        logger.info("cancelling...")
        # ブロッキングしないようにSendMessageではなくPostMessage
        cts.windll.user32.PostMessageW(self.hwnd, WM_QUIT, 0, 0)

    def register_devices(self, hwnd=None):
        flags = RIDEV_INPUTSINK
        # RawInputDeviceの配列
        # Ctypesの配列は(obj * len)(obj1,obj2,obj3)
        devices = (cws.RawInputDevice * 1)(
            cws.RawInputDevice(HID_USAGE_PAGE_GENERIC, HID_USAGE_GENERIC_MOUSE, flags, hwnd)
        )

        if cws.RegisterRawInputDevices(devices, 1, cts.sizeof(cws.RawInputDevice)):
            logger.info("Successfully registered input device(s)!")
            return True
        else:
            log_error_code("RegisterRawInputDevices")
            return False

    def wnd_proc(self, hwnd, msg, wparam, lparam):
        if msg == WM_INPUT:
            size = wts.UINT(0)
            res = cws.GetRawInputData(
                cts.cast(lparam, cws.PRAWINPUT), RID_INPUT, None, cts.byref(size), cts.sizeof(cws.RAWINPUTHEADER)
            )
            if res == wts.UINT(-1) or size == 0:
                log_error_code("GetRawInputData 0")
                return 0
            buf = cts.create_string_buffer(size.value)
            res = cws.GetRawInputData(
                cts.cast(lparam, cws.PRAWINPUT), RID_INPUT, buf, cts.byref(size), cts.sizeof(cws.RAWINPUTHEADER)
            )
            if res != size.value:
                log_error_code("GetRawInputData 1")
                return 0
            raw = cts.cast(buf, cws.PRAWINPUT).contents
            if raw.header.dwType == RIM_TYPEMOUSE:
                data = raw.data.mouse
                self.mouseMoved.emit(data.lLastX, data.lLastY)
        return cws.DefWindowProc(hwnd, msg, wparam, lparam)


if __name__ == "__main__":
    print("done")
