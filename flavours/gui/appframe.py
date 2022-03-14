import wx
import flavours


class AppFrame(wx.Frame):
    # def __init__(self, *args, **kwargs):
    #     super(AppFrame, self).__init__(*args, **kwargs)

    def SetMenus(self):

        menuBar = wx.MenuBar()

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
        menuBar.Append(menu, "&File")

        # EDIT
        editMenu = wx.Menu()
        editMenu.Append(wx.ID_UNDO, "Undo\tCtrl-Z")
        editMenu.AppendSeparator()
        m_select_all = editMenu.Append(wx.ID_SELECTALL, "Select All\tCtrl-A")
        m_copy = editMenu.Append(wx.ID_COPY, "Copy\tCtrl-C")
        m_cut = editMenu.Append(wx.ID_CUT, "Cut\tCtrl-X")
        m_paste = editMenu.Append(wx.ID_PASTE, "Paste\tCtrl-V")
        menuBar.Append(editMenu, "&Edit")
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
        menuBar.Append(menu, "&Shell")

        self.SetMenuBar(menuBar)

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
            from AppKit import (
                NSApp,
                NSView,
                NSPoint,
                NSMakeRect,
                NSToolbar,
                NSProcessInfo,
                NSString,
            )

            w = NSApp().mainWindow()
            w.setMovable_(False)

            from AppKit import (
                NSLeftMouseDraggedMask,
                NSLeftMouseUpMask,
                NSScreen,
                NSLeftMouseUp,
            )

            class MyView(NSView):
                # def mouseDragged_(self, event):
                # 	event.window().setFrameOrigin_(NSPoint(event.window().frame().origin.x + event.deltaX(), event.window().frame().origin.y - event.deltaY()))

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

                # def drawRect_(self, rect):
                # 	NSColor.yellowColor().set()
                # 	NSRectFill(rect)

            self.dragView = MyView.alloc().initWithFrame_(NSMakeRect(0, 0, self.GetSize()[0], 40))
            w.contentView().addSubview_(self.dragView)

            # self.javaScript("$('#sidebar').css('padding-top', '32px');")
            # self.SetTitle("Flavours")
            # NSProcessInfo.alloc().init().setProcessName_(NSString.alloc().initWithString_("Flavours"))
            # menu = NSApp.mainMenu()
            # menu.setTitle_("Flavours")
            # submenu = menu.itemAtIndex_(0)
            # submenu.setTitle_(NSString.alloc().initWithString_("Flavours"))
            # submenu.setTitle_("Flavours")

            w.setStyleMask_(1 << 0 | 1 << 1 | 1 << 2 | 1 << 3 | 1 << 15)
            w.setTitlebarAppearsTransparent_(1)

            w.setTitleVisibility_(1)
            toolbar = NSToolbar.alloc().init()
            toolbar.setShowsBaselineSeparator_(0)
            w.setToolbar_(toolbar)
