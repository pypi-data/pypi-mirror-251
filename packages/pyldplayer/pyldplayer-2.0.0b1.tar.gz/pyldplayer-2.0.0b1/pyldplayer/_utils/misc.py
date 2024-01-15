import functools
import os
import numpy as np
import pygetwindow as gw
import psutil
from PIL import Image,ImageGrab, ImageDraw
from screeninfo import get_monitors
import pyautogui as pg

pg.FAILSAFE = False
internal_dir = os.path.dirname(os.path.realpath(__file__))
mod_dir = os.path.dirname(internal_dir)


_overlooking_processes = ["dnmultiplayerex.exe", "dnplayer.exe", "dnmultiplayer.exe"]

def find_ldconsole():
    """
    Find the path to the ldconsole.exe process.

    Returns:
        str: The path to the ldconsole.exe process if it is found.
        None: If the ldconsole.exe process is not found.
    """
    for process in psutil.process_iter():
        if process.name() == "ldconsole.exe":
            return process.exe()

        if process.name() not in _overlooking_processes:
            continue

        suspected_directory = os.path.dirname(process.exe())

        if process.name() == _overlooking_processes[0]:
            suspected_directory = os.path.dirname(suspected_directory)

        suspected_path =os.path.join(suspected_directory, "ldconsole.exe")

        if not os.path.exists(suspected_path):
            continue

        return suspected_path

    return None

def hasAndEqual(a, b, v):
    if not hasattr(a, b):
        return False
    
    return getattr(a, b) == v
    
    
def is_window_valid(window):
    try:
        # Attempt to access a property of the window
        _ = window.title
        # Check if the window is in the list of all windows
        return window in gw.getAllWindows()
    except Exception:
        # If an error occurs, the window is likely invalid
        return False
    
def find_word_coordinates(image, search_word, languages):
    import easyocr
    # Create a reader object
    reader = easyocr.Reader(languages)  # 'en' denotes English language

    # Perform OCR on the image
    results = reader.readtext(image)

    # List to store coordinates of found words
    found_word_coordinates = []

    # Iterate over OCR results
    for result in results:
        # Each result has this format: (bbox, text, confidence)
        bbox, text, _ = result

        # Check if the detected text matches the search word
        if text.lower() == search_word.lower():
            # bbox is in the format [(top_left), (top_right), (bottom_right), (bottom_left)]
            # You can format it as you like, here's a simple conversion to (x, y, width, height)
            top_left = bbox[0]
            bottom_right = bbox[2]
            x, y = top_left
            width = bottom_right[0] - top_left[0]
            height = bottom_right[1] - top_left[1]

            found_word_coordinates.append((x, y, width, height))

    return found_word_coordinates


_primary_monitor = None

def get_primary_monitor():
    global _primary_monitor
    if _primary_monitor is None:
        # Get primary monitor dimensions
        for m in get_monitors():
            if m.is_primary:
                _primary_monitor = m
                break
            
    return _primary_monitor

def is_window_in_primary_monitor(window : gw.Window):
            
    primary_monitor = get_primary_monitor()
        
    # Check if the window is within the primary monitor
    if window.left < primary_monitor.x or window.top < primary_monitor.y:
        return False
    if window.left + window.width > primary_monitor.width or window.top + window.height > primary_monitor.height:
        return False

    # If all checks passed, the window is within the primary monitor
    return True

def wnd_in_monitor(window : gw.Window):
    monitors = get_monitors()

    # Calculate the center of the window
    window_center_x = window.left + window.width // 2
    window_center_y = window.top + window.height // 2

    for i, monitor in enumerate(monitors):
        # Check if the window center is within the monitor's bounds
        if (monitor.x <= window_center_x < monitor.x + monitor.width and
            monitor.y <= window_center_y < monitor.y + monitor.height):
            return i + 1, monitor

    return None

def screenshot_by_monitor(monitor_num : int):
    monitor_num = monitor_num - 1
    monitor = get_monitors()[monitor_num]
    return ImageGrab.grab(bbox=(monitor.x, monitor.y, monitor.x + monitor.width, monitor.y + monitor.height), all_screens=True)

def screenshot(wnd : gw.Window, region : tuple[int, int, int, int]):
    if is_window_in_primary_monitor(wnd):
        im = ImageGrab.grab()
        mnumber = 1
    else:
        mnumber, monitor = wnd_in_monitor(wnd)
        region = (wnd.left - monitor.x, wnd.top - monitor.y, wnd.width, wnd.height)
        im = screenshot_by_monitor(mnumber)
    
    if region is not None:
        assert len(region) == 4, 'region argument must be a tuple of four ints'
        assert isinstance(region[0], int) and isinstance(region[1], int) and isinstance(region[2], int) and isinstance(region[3], int), 'region argument must be a tuple of four ints'
        im = im.crop((region[0], region[1], region[2] + region[0], region[3] + region[1]))

    return im, mnumber

def getMonitor(id):
    return get_monitors()[id - 1]

def multiToggle(func):
    @functools.wraps(func)
    def wrapper(*args, multi: bool= True, **kwargs):
        res = func(*args, **kwargs)
        if res is None or len(res) == 0:
            return None
        if multi:
            return res
        else:
            return res[0]
            
    return wrapper

def draw_bounding_boxes(
    image : Image,
    boxes : list[tuple[int, int, int, int]]
):
    if isinstance(image, np.ndarray):
        image = Image.fromarray(image)
    
    draw = ImageDraw.Draw(image)
    
    for box in boxes:
        draw.rectangle((box[0], box[1], box[0] + box[2], box[1] + box[3]), outline="red")

    return image


