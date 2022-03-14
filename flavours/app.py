import wx
import os
import flavours
from flavours.gui import fonts, shell, appframe

# # Path to open
# path_to_open = os.path.abspath(sys.argv[-1])
# print("path_to_open", path_to_open)

# Icons
if flavours.MAC:
    from AppKit import NSImage, NSString, NSApp

app = wx.App()

# Fonts
MONO_FONT = fonts.font("IBM Plex Mono", "Regular")
MONO_FONT_BOLD = fonts.font("IBM Plex Mono", "Bold")

# Main Window
frame = appframe.AppFrame(None, title="wxPython Frame", size=(1000, 800))
frame.SetFont(MONO_FONT)
frame.SetMenus()

# Set app icon
if flavours.MAC:
    icon = NSImage.alloc().initByReferencingFile_(
        NSString.alloc().initWithString_(os.path.join(flavours.BASE_DIR, "resources", "icons", "app.png"))
    )
    NSApp.setApplicationIconImage_(icon)
    # NSApp.setName_("helo")


# Window content
panel = wx.Panel(frame)
panel.SetBackgroundColour("#ffffff")
panel.SetFont(MONO_FONT)

toolbarbox = wx.BoxSizer(wx.HORIZONTAL)
shell = shell.Shell(panel)
toolbarbox.Add(shell, wx.ID_ANY, wx.EXPAND | wx.ALL, 20)

panel.SetSizer(toolbarbox)

frame.Show(True)
frame.SetStyle()
app.MainLoop()
