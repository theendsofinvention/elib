# coding=utf-8
"""
Utilities to control the console window
"""

import ctypes


def set_title(title: str):
    ctypes.windll.kernel32.SetConsoleTitleW(title)
