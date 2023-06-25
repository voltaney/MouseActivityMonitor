import ctypes as cts
import ctypes.wintypes as wts

# set dlls
kernel32 = cts.WinDLL("Kernel32")
user32 = cts.WinDLL("User32")

# 用意されていない型のDefine
HCURSOR = cts.c_void_p
LRESULT = cts.c_ssize_t

# WNDPROC コールバック関数
# https://learn.microsoft.com/ja-jp/windows/win32/api/winuser/nc-winuser-wndproc
LRESULT = cts.c_ssize_t
wndproc_args = (wts.HWND, wts.UINT, wts.WPARAM, wts.LPARAM)
WNDPROC = cts.CFUNCTYPE(LRESULT, *wndproc_args)


# RegisterClassではなく、より新しいバージョンの*Ex系推奨
# ExAはANSI、ExWはUnicodeを取り扱うため、ExWを使用
# https://learn.microsoft.com/ja-jp/windows/win32/api/winuser/nf-winuser-registerclassexw
class WNDCLASSEX(cts.Structure):
    _fields_ = [
        ("cbSize", wts.UINT),
        ("style", wts.UINT),
        ("lpfnWndProc", WNDPROC),
        ("cbClsExtra", cts.c_int),
        ("cbWndExtra", cts.c_int),
        ("hInstance", wts.HINSTANCE),
        ("hIcon", wts.HICON),
        ("hCursor", HCURSOR),
        ("hbrBackground", wts.HBRUSH),
        ("lpszMenuName", wts.LPCWSTR),
        ("lpszClassName", wts.LPCWSTR),
        ("hIconSm", wts.HICON),
    ]


# https://learn.microsoft.com/ja-jp/windows/win32/api/winuser/ns-winuser-rawinputdevice
class RawInputDevice(cts.Structure):
    _fields_ = (
        ("usUsagePage", wts.USHORT),
        ("usUsage", wts.USHORT),
        ("dwFlags", wts.DWORD),
        ("hwndTarget", wts.HWND),
    )


# RawInputDeviceのポインタ
PRawInputDevice = cts.POINTER(RawInputDevice)


# https://learn.microsoft.com/ja-jp/windows/win32/api/winuser/ns-winuser-rawinputheader
class RAWINPUTHEADER(cts.Structure):
    _fields_ = (
        ("dwType", wts.DWORD),
        ("dwSize", wts.DWORD),
        ("hDevice", wts.HANDLE),
        ("wParam", wts.WPARAM),
    )


# ulButtonsは下記２つでULONG
# USHORT usButtonFlags;
# USHORT usButtonData;
# https://learn.microsoft.com/ja-jp/windows/win32/api/winuser/ns-winuser-rawinput
class RAWMOUSE(cts.Structure):
    _fields_ = (
        ("usFlags", wts.USHORT),
        ("ulButtons", wts.ULONG),
        ("ulRawButtons", wts.ULONG),
        ("lLastX", wts.LONG),
        ("lLastY", wts.LONG),
        ("ulExtraInformation", wts.ULONG),
    )


# https://learn.microsoft.com/ja-jp/windows/win32/api/winuser/ns-winuser-rawhid
class RAWHID(cts.Structure):
    _fields_ = (
        ("dwSizeHid", wts.DWORD),
        ("dwCount", wts.DWORD),
        (
            "bRawData",
            wts.BYTE * 1,
        ),  # @TODO - cfati: https://docs.microsoft.com/en-us/windows/win32/api/winuser/ns-winuser-rawhid, but not very usable via CTypes
    )


# https://learn.microsoft.com/ja-jp/windows/win32/api/winuser/ns-winuser-rawkeyboard
class RAWKEYBOARD(cts.Structure):
    _fields_ = (
        ("MakeCode", wts.USHORT),
        ("Flags", wts.USHORT),
        ("Reserved", wts.USHORT),
        ("VKey", wts.USHORT),
        ("Message", wts.UINT),
        ("ExtraInformation", wts.ULONG),
    )


# RAWINPUTでUnionとして使われる
class RAWINPUT_UNI(cts.Union):
    _fields_ = (
        ("mouse", RAWMOUSE),
        ("keyboard", RAWKEYBOARD),
        ("hid", RAWHID),
    )


# https://learn.microsoft.com/ja-jp/windows/win32/api/winuser/ns-winuser-rawinput
class RAWINPUT(cts.Structure):
    _fields_ = (
        ("header", RAWINPUTHEADER),
        ("data", RAWINPUT_UNI),
    )


PRAWINPUT = cts.POINTER(RAWINPUT)


# 使用メソッドの引数と返り値の定義
GetLastError = kernel32.GetLastError
GetLastError.argtypes = ()
GetLastError.restype = wts.DWORD

GetModuleHandle = kernel32.GetModuleHandleW
GetModuleHandle.argtypes = (wts.LPWSTR,)
GetModuleHandle.restype = wts.HMODULE


DefWindowProc = user32.DefWindowProcW
DefWindowProc.argtypes = wndproc_args
DefWindowProc.restype = LRESULT

RegisterClassEx = user32.RegisterClassExW
RegisterClassEx.argtypes = (cts.POINTER(WNDCLASSEX),)
RegisterClassEx.restype = wts.ATOM

CreateWindowEx = user32.CreateWindowExW
CreateWindowEx.argtypes = (
    wts.DWORD,
    wts.LPCWSTR,
    wts.LPCWSTR,
    wts.DWORD,
    cts.c_int,
    cts.c_int,
    cts.c_int,
    cts.c_int,
    wts.HWND,
    wts.HMENU,
    wts.HINSTANCE,
    wts.LPVOID,
)
CreateWindowEx.restype = wts.HWND


RegisterRawInputDevices = user32.RegisterRawInputDevices
RegisterRawInputDevices.argtypes = (PRawInputDevice, wts.UINT, wts.UINT)
RegisterRawInputDevices.restype = wts.BOOL

GetRawInputData = user32.GetRawInputData
GetRawInputData.argtypes = (PRAWINPUT, wts.UINT, wts.LPVOID, wts.PUINT, wts.UINT)
GetRawInputData.restype = wts.UINT

GetMessage = user32.GetMessageW
GetMessage.argtypes = (wts.LPMSG, wts.HWND, wts.UINT, wts.UINT)
GetMessage.restype = wts.BOOL

PeekMessage = user32.PeekMessageW
PeekMessage.argtypes = (wts.LPMSG, wts.HWND, wts.UINT, wts.UINT, wts.UINT)
PeekMessage.restype = wts.BOOL

TranslateMessage = user32.TranslateMessage
TranslateMessage.argtypes = (wts.LPMSG,)
TranslateMessage.restype = wts.BOOL

DispatchMessage = user32.DispatchMessageW
DispatchMessage.argtypes = (wts.LPMSG,)
DispatchMessage.restype = LRESULT

PostQuitMessage = user32.PostQuitMessage
PostQuitMessage.argtypes = (cts.c_int,)
PostQuitMessage.restype = None
