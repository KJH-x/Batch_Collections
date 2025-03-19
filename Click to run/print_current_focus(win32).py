import time

import win32gui


def get_active_window_title_and_hwnd():
    hwnd = win32gui.GetForegroundWindow()
    if hwnd:
        window_title = win32gui.GetWindowText(hwnd)
        return hwnd, window_title
    return None, None

def main():
    last_hwnd = None  # To store the last window handle
    while True:
        hwnd, window_title = get_active_window_title_and_hwnd()
        if hwnd != last_hwnd:  # Check if the window has changed
            if hwnd:  # Ensure a valid window handle
                print(f"Window Title: {window_title}, HWND: {hwnd}")
            last_hwnd = hwnd
        # time.sleep(0.5)  # Add a delay to reduce CPU usage

if __name__ == "__main__":
    main()
