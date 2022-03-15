import wx
import os
import sys
import flavours
from flavours.gui.appframe import MakeFrame
from flavours.gui.scripts import MakeScriptsManager
import logging
import traceback
import threading

try:
    # # Path to open
    flavours.working_directory = os.path.abspath(sys.argv[-1])
    if not flavours.working_directory.startswith("/"):
        flavours.working_directory = os.path.abspath(os.path.join(os.getcwd(), flavours.working_directory))

    # Icons
    if flavours.MAC:
        from AppKit import NSImage, NSString, NSApp

    flavours.app = wx.App()
    flavours.app.frames = [MakeFrame()]

    # Set app icon
    if flavours.MAC:
        __icon = NSImage.alloc().initByReferencingFile_(
            NSString.alloc().initWithString_(os.path.join(flavours.BASE_DIR, "resources", "icons", "app.png"))
        )
        NSApp.setApplicationIconImage_(__icon)

    # Logging
    root = logging.getLogger()
    root.setLevel(logging.DEBUG)
    handler = logging.StreamHandler(sys.stdout)
    handler.setLevel(logging.DEBUG)
    formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    handler.setFormatter(formatter)
    root.addHandler(handler)

    # # Scripts Manager
    # flavours.app.scripts_manager_thread = threading.Thread(
    #     target=MakeScriptsManager, args=(os.path.join(flavours.working_directory, "scripts"),), daemon=True
    # )
    # flavours.app.scripts_manager_thread.start()

    flavours.app.MainLoop()
except:
    sys.__stdout__.stdout = sys.__stdout__
    traceback.print_exc()
