import sys
import wx
import flavours
from flavours.gui import fonts, shell, appframe, scripts
from io import StringIO

if flavours.MAC:
    from AppKit import (
        NSApp,
        NSView,
        NSPoint,
        NSMakeRect,
        NSToolbar,
        # NSProcessInfo,
        # NSString,
        NSLeftMouseDraggedMask,
        NSLeftMouseUpMask,
        NSScreen,
        NSLeftMouseUp,
    )


def MakeFrame():

    # Fonts
    MONO_FONT = fonts.font("IBM Plex Mono", "Regular")
    MONO_FONT_BOLD = fonts.font("IBM Plex Mono", "Bold")

    # Main Window
    frame = appframe.AppFrame(None, title="wxPython Frame", size=(1000, 800))
    frame.SetFont(MONO_FONT)

    # Window content
    panel = wx.Panel(frame)
    panel.SetBackgroundColour("#ffffff")
    panel.SetFont(MONO_FONT)

    main_panel = wx.Panel(panel)
    # main_panel.SetBackgroundColour("#000000")  # black
    toolbar_panel = wx.Panel(panel)
    # toolbar_panel.SetBackgroundColour("#FF0000")  # red
    main_horizontal_box = wx.BoxSizer(wx.HORIZONTAL)
    main_horizontal_box.Add(main_panel, wx.ID_ANY, wx.EXPAND | wx.ALL, 0)
    main_horizontal_box.Add(toolbar_panel, wx.ID_ANY, wx.EXPAND | wx.ALL, 20)

    toolbar_box = wx.BoxSizer(wx.VERTICAL)
    upper_toolbar_panel = wx.Panel(toolbar_panel)
    # upper_toolbar_panel.SetBackgroundColour("#00FF00")  # green
    lower_toolbar_panel = wx.Panel(toolbar_panel)
    # lower_toolbar_panel.SetBackgroundColour("#0000FF")  # blue
    toolbar_box.Add(upper_toolbar_panel, wx.ID_ANY, wx.EXPAND | wx.ALL, 0)
    toolbar_box.Add(lower_toolbar_panel, wx.ID_ANY, wx.EXPAND | wx.TOP, 20)

    shell_box = wx.BoxSizer(wx.VERTICAL)
    frame.shell = shell.Shell(lower_toolbar_panel)
    shell_box.Add(frame.shell, wx.ID_ANY, wx.EXPAND | wx.ALL, 0)

    toolbar_panel.SetSizer(toolbar_box)
    lower_toolbar_panel.SetSizer(shell_box)

    panel.SetSizer(main_horizontal_box)

    frame.Show(True)
    frame.SetMenus()
    frame.SetStyle()
    frame.shell.SetFocus()

    class ShellIO(StringIO):
        def writeCallAfter(self, text):
            frame.shell.SetCurrentPos(frame.shell.GetTextLength())
            if frame.shell.GetText()[-1] != "\n":
                frame.shell.write("\n")
            frame.shell.write(text)
            if frame.shell.GetText()[-1] == "\n":
                frame.shell.SetText(frame.shell.GetText()[:-1])
            frame.shell.ScrollToEnd()

        def write(self, text):
            wx.CallAfter(self.writeCallAfter, text)

    sys.stdout = ShellIO()
    # frame.shell.redirectStdout(True)
    frame.shell.redirectStderr(True)

    return frame


class AppFrame(wx.Frame):
    # def __init__(self, *args, **kwargs):
    #     super(AppFrame, self).__init__(*args, **kwargs)

    def SetMenus(self):

        self.menuBar = wx.MenuBar()

        menu = wx.Menu()
        if flavours.MAC:
            m_exit = menu.Append(
                wx.ID_EXIT,
                "Quit",
                "Ctrl-Q" if flavours.MAC else "Alt-F4",
            )
            self.Bind(wx.EVT_MENU, self.OnQuit, m_exit)
        m_get_flavours = menu.Append(
            wx.NewIdRef(count=1),
            "Get Flavours",
        )
        self.Bind(wx.EVT_MENU, self.OnGetFlavours, m_get_flavours)
        self.menuBar.Append(menu, "&File")

        # EDIT
        editMenu = wx.Menu()
        editMenu.Append(wx.ID_UNDO, "Undo\tCtrl-Z")
        editMenu.AppendSeparator()
        m_select_all = editMenu.Append(wx.ID_SELECTALL, "Select All\tCtrl-A")
        m_copy = editMenu.Append(wx.ID_COPY, "Copy\tCtrl-C")
        m_cut = editMenu.Append(wx.ID_CUT, "Cut\tCtrl-X")
        m_paste = editMenu.Append(wx.ID_PASTE, "Paste\tCtrl-V")
        self.menuBar.Append(editMenu, "&Edit")
        self.Bind(wx.EVT_MENU, self.OnSelectAll, m_select_all)
        self.Bind(wx.EVT_MENU, self.OnCopy, m_copy)
        self.Bind(wx.EVT_MENU, self.OnPaste, m_paste)
        self.Bind(wx.EVT_MENU, self.OnCut, m_cut)

        # SHELL MENU
        menu = wx.Menu()
        m_shell_clear = menu.Append(
            wx.NewIdRef(count=1),
            "&Focus or Clear Shell\tCtrl-K",
        )
        self.Bind(wx.EVT_MENU, self.OnShellClear, m_shell_clear)
        # m_shell_print = menu.Append(
        #     wx.NewIdRef(count=1),
        #     "&Print\tCtrl-P",
        # )
        # self.Bind(wx.EVT_MENU, self.OnShellPrint, m_shell_print)
        self.menuBar.Append(menu, "&Shell")

        # SCRIPTS MENU
        self.scripts_menu = wx.Menu()
        self.menuBar.Append(self.scripts_menu, "&Scripts")

        self.SetMenuBar(self.menuBar)

    def print(self, text):
        print(text)

    def OnQuit(self, event, withExitCode=None):
        self.Destroy()

    def OnShellClear(self, event):
        self.shell.ClearOrFocus()

    # def OnShellPrint(self, event):
    #     assert abc

    def OnGetFlavours(self, event):
        self.shell.clear()

    def OnSelectAll(self, event):

        # Shell
        if self.shell.HasFocus():
            if self.shell.GetCurrentLine() == self.shell.GetLineCount() - 1:
                count_till_last_line = self.shell.GetTextLength()
                last_line_count = len(self.shell.GetText().splitlines()[-1])
                selection_start = count_till_last_line - last_line_count
                if ">>>" in self.shell.GetText().splitlines()[-1]:
                    selection_start += 4
                self.shell.SetSelectionStart(selection_start)
                self.shell.SetSelectionEnd(count_till_last_line)

    def OnCopy(self, event):

        # Shell
        if self.shell.HasFocus():
            self.shell.Copy()

    def OnPaste(self, event):

        # Shell
        if self.shell.HasFocus():
            self.shell.Paste()

    def OnCut(self, event):

        # Shell
        if self.shell.HasFocus():
            if self.shell.GetCurrentLine() == self.shell.GetLineCount() - 1:
                self.shell.Cut()

    def SetStyle(self):
        # Window Styling
        if flavours.MAC:

            class MyView(NSView):
                def mouseDown_(self, event):

                    _initialLocation = event.locationInWindow()

                    while True:

                        theEvent = w.nextEventMatchingMask_(NSLeftMouseDraggedMask | NSLeftMouseUpMask)
                        point = theEvent.locationInWindow()
                        screenVisibleFrame = NSScreen.mainScreen().visibleFrame()
                        windowFrame = w.frame()
                        newOrigin = windowFrame.origin

                        # Get the mouse location in window coordinates.
                        currentLocation = point

                        # Update the origin with the difference between the new mouse location and the old mouse location.
                        newOrigin.x += currentLocation.x - _initialLocation.x
                        newOrigin.y += currentLocation.y - _initialLocation.y

                        # Don't let window get dragged up under the menu bar
                        if (newOrigin.y + windowFrame.size.height) > (
                            screenVisibleFrame.origin.y + screenVisibleFrame.size.height
                        ):
                            newOrigin.y = screenVisibleFrame.origin.y + (
                                screenVisibleFrame.size.height - windowFrame.size.height
                            )

                        # Move the window to the new location
                        w.setFrameOrigin_(newOrigin)

                        if theEvent.type() == NSLeftMouseUp:
                            break

                    event.window().setFrameOrigin_(
                        NSPoint(
                            event.window().frame().origin.x + event.deltaX(),
                            event.window().frame().origin.y - event.deltaY(),
                        )
                    )

            w = NSApp().mainWindow()
            w.setMovable_(False)

            self.dragView = MyView.alloc().initWithFrame_(NSMakeRect(0, 0, self.GetSize()[0], 40))
            w.contentView().addSubview_(self.dragView)

            w.setStyleMask_(1 << 0 | 1 << 1 | 1 << 2 | 1 << 3 | 1 << 15)
            w.setTitlebarAppearsTransparent_(1)

            w.setTitleVisibility_(1)
            toolbar = NSToolbar.alloc().init()
            toolbar.setShowsBaselineSeparator_(0)
            w.setToolbar_(toolbar)
