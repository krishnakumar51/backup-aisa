"""
Enhanced Utilities Package for Multi-Agent Automation Framework
Contains device management, terminal management, and other utility classes
"""

from .device_manager import DeviceManager, detect_android_devices
from .terminal_manager import TerminalManager, ensure_testing_environment

__all__ = [
    "DeviceManager",
    "detect_android_devices", 
    "TerminalManager",
    "ensure_testing_environment"
]

# Package metadata
__version__ = "3.0.0-enhanced"
__author__ = "Enhanced Multi-Agent Framework"
__description__ = "Utility classes for terminal isolation, device detection, and automation support"