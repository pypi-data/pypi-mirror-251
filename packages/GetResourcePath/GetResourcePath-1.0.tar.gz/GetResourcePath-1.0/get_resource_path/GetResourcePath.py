import os
import sys

def get_resource_path(relative_path):
    if hasattr(sys, '_MEIPASS'):
        base_path = sys._MEIPASS
    else:
        base_path = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(base_path, relative_path)

def get_persistent_path(relative_path, app_support_path):
    full_path = os.path.join(app_support_path, relative_path)
    directory = full_path if os.path.isdir(full_path) else os.path.dirname(full_path)

    os.makedirs(directory, exist_ok=True)
    return full_path
