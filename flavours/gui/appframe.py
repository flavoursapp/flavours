import wx
import flavours


class AppFrame(wx.Frame):
    # def __init__(self, *args, **kwargs):
    #     super(AppFrame, self).__init__(*args, **kwargs)

    def SetMenus(self):

        menuBar = wx.MenuBar()

        menu = wx.Menu()

        m_exit = menu.Append(
            wx.ID_EXIT,
            "Quit",
            "Ctrl-Q" if flavours.MAC else "Alt-F4",
        )
        self.Bind(wx.EVT_MENU, self.OnQuit, m_exit)
        menuBar.Append(menu, "&File")

        if flavours.MAC:
            menu = wx.Menu()

        self.SetMenuBar(menuBar)
        # menuBar.SetMenuLabel(0, "Hello")

    def OnQuit(self, event, withExitCode=None):
        self.Destroy()

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
            self.SetTitle("Flavours")
            NSProcessInfo.alloc().init().setProcessName_(NSString.alloc().initWithString_("Flavours"))
            menu = NSApp.mainMenu()
            menu.setTitle_("Flavours")
            print(menu)
            submenu = menu.itemAtIndex_(0)
            print(submenu)
            submenu.setTitle_(NSString.alloc().initWithString_("Flavours"))
            submenu.setTitle_("Flavours")

            w.setStyleMask_(1 << 0 | 1 << 1 | 1 << 2 | 1 << 3 | 1 << 15)
            w.setTitlebarAppearsTransparent_(1)

            w.setTitleVisibility_(1)
            toolbar = NSToolbar.alloc().init()
            toolbar.setShowsBaselineSeparator_(0)
            w.setToolbar_(toolbar)
