import sys
from cx_Freeze import setup, Executable

base = None
if sys.platform == "win32":
    base = "Win32GUI"

# Список файлов для включения в дистрибутив
additional_files = [
    ('config.json', ''),
    ('temp\\', 'temp\\'),
    ('icons\\Icon19.ico', 'icons\\Icon19.ico'),
    ('NotoSansMono_ExtraCondensed-Regular.ttf', ''),
    ('Roboto-Medium.ttf', '')
]

dlls = [
    # ("path_to_wx_dlls\\*.dll", ""),
    ('.venv\\Lib\\site-packages\\pywin32_system32\\pywintypes39.dll', ""),
    ('.venv\\Lib\\site-packages\\pywin32_system32\\pythoncom39.dll', "")
]

executables = [
    Executable("BarCodePrinter.py", icon='icons\\Icon19.ico', base=base)
]

setup(
    name="BarCodePrinter",
    version="1.0",
    description="Сервер друку етикеток",
    options={
        "build_exe": {
            "include_files": dlls+additional_files,
            "includes": ["wx"],   # Указание на включение библиотеки wxPython
            'packages': ['wx'],
        }
    },
    executables=executables
)
