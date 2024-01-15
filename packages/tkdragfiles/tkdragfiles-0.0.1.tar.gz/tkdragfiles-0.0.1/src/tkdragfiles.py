import tkinter as tk
import win32gui, win32api, win32con

_callback = None
_root = None
def wndProc(hwnd, msg, wParam, lParam):
    global _callback
    global _root
    if msg == win32con.WM_DROPFILES:
        hdrop = wParam
        num_files = win32api.DragQueryFile(hdrop, -1)
        file_paths = []
        for i in range(num_files):
            file_path = win32api.DragQueryFile(hdrop, i)
            file_paths.append(file_path)
        win32api.DragFinish(hdrop)
        if callable(_callback):
            _callback(file_paths)
    elif msg == win32con.WM_DESTROY:
        win32gui.PostQuitMessage(0)
        _root.destroy()
    elif msg == win32con.WM_SIZE:
        if wParam == win32con.SIZE_MINIMIZED:
            pass
    else:
        return win32gui.DefWindowProc(hwnd, msg, wParam, lParam)
    return 0

def _start_dragfiles_event(root,callback):
    global _callback
    global _root
    _callback = callback
    _root = root
    window_handle = get_window_handle(root.title())
    win32gui.SetWindowLong(window_handle, win32con.GWL_WNDPROC, wndProc)
    win32gui.DragAcceptFiles(window_handle, True)

def get_window_handle(title):
    return win32gui.FindWindow("TkTopLevel",title)

def start_dragfiles_event(root,callback):
    root.after(100,lambda:_start_dragfiles_event(root,callback))
