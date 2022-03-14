import wx
import os
import sys
import flavours
from flavours.gui import fonts, shell, appframe
from io import StringIO

# # Path to open
# path_to_open = os.path.abspath(sys.argv[-1])
# print("path_to_open", path_to_open)

# Icons
if flavours.MAC:
    from AppKit import NSImage, NSString, NSApp

__app = wx.App()

# Fonts
MONO_FONT = fonts.font("IBM Plex Mono", "Regular")
MONO_FONT_BOLD = fonts.font("IBM Plex Mono", "Bold")

# Main Window
__frame = appframe.AppFrame(None, title="wxPython Frame", size=(1000, 800))
__frame.SetFont(MONO_FONT)

# Set app icon
if flavours.MAC:
    __icon = NSImage.alloc().initByReferencingFile_(
        NSString.alloc().initWithString_(os.path.join(flavours.BASE_DIR, "resources", "icons", "app.png"))
    )
    NSApp.setApplicationIconImage_(__icon)


# Window content
__panel = wx.Panel(__frame)
__panel.SetBackgroundColour("#ffffff")
__panel.SetFont(MONO_FONT)

__main_panel = wx.Panel(__panel)
# __main_panel.SetBackgroundColour("#000000")  # black
__toolbar_panel = wx.Panel(__panel)
# __toolbar_panel.SetBackgroundColour("#FF0000")  # red
__main_horizontal_box = wx.BoxSizer(wx.HORIZONTAL)
__main_horizontal_box.Add(__main_panel, wx.ID_ANY, wx.EXPAND | wx.ALL, 0)
__main_horizontal_box.Add(__toolbar_panel, wx.ID_ANY, wx.EXPAND | wx.ALL, 20)

__toolbar_box = wx.BoxSizer(wx.VERTICAL)
__upper_toolbar_panel = wx.Panel(__toolbar_panel)
# __upper_toolbar_panel.SetBackgroundColour("#00FF00")  # green
__lower_toolbar_panel = wx.Panel(__toolbar_panel)
# __lower_toolbar_panel.SetBackgroundColour("#0000FF")  # blue
__toolbar_box.Add(__upper_toolbar_panel, wx.ID_ANY, wx.EXPAND | wx.ALL, 0)
__toolbar_box.Add(__lower_toolbar_panel, wx.ID_ANY, wx.EXPAND | wx.TOP, 20)

__shell_box = wx.BoxSizer(wx.VERTICAL)
__frame.shell = shell.Shell(__lower_toolbar_panel)
__shell_box.Add(__frame.shell, wx.ID_ANY, wx.EXPAND | wx.ALL, 0)

__toolbar_panel.SetSizer(__toolbar_box)
__lower_toolbar_panel.SetSizer(__shell_box)

__panel.SetSizer(__main_horizontal_box)

__frame.Show(True)
__frame.SetMenus()
__frame.SetStyle()
__frame.shell.SetFocus()


class ShellIO(StringIO):
    def write(self, text):
        __frame.shell.SetCurrentPos(__frame.shell.GetTextLength())
        if __frame.shell.GetText()[-1] != "\n":
            __frame.shell.write("\n")
        __frame.shell.write(text)
        if __frame.shell.GetText()[-1] == "\n":
            __frame.shell.SetText(__frame.shell.GetText()[:-1])
        __frame.shell.ScrollToEnd()


sys.stdout = ShellIO()
__frame.shell.redirectStderr(True)

__app.MainLoop()
