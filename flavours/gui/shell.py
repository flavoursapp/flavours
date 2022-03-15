import sys
import wx
from wx import stc
import wx.py.shell
from wx.py import dispatcher

# https://github.com/wxWidgets/Phoenix/blob/272990b1319ffb7ce99a359ee7d2d64a707e0428/wx/py/editwindow.py

FACES = {
    "times": "Lucida Grande",
    "mono": "IBM Plex Mono",
    "helv": "Geneva",
    "other": "new century schoolbook",
    "size": 12,
    "lnsize": 10,
    "backcol": "#FFFFFF",
    "calltipbg": "#FFFFB8",
    "calltipfg": "#404040",
}


class Shell(wx.py.shell.Shell):
    def __init__(self, *args, **kwargs):
        super(Shell, self).__init__(*args, **kwargs)

        # self.Bind(wx.EVT_LEFT_UP, self.OnMouseUp)
        # self.Bind(wx.EVT_LEFT_DOWN, self.OnMouseDown)
        # self.Bind(wx.EVT_MOTION, self.OnMove)

        self.SetUseVerticalScrollBar(False)
        self.SetEndAtLastLine(True)

        size = 12

        black = "#444444"
        dark_blue = "#1D70B7"
        light_blue = "#009EE2"
        red = "#ff465e"
        purple = "#875bf4"
        light_gray = "#9C9B9B"
        white = "#FFFFFF"

        # Default style
        self.StyleSetSpec(stc.STC_STYLE_DEFAULT, f"face:{FACES['mono']},size:{size},fore:{black},back:{white}")

        self.StyleClearAll()
        self.SetSelForeground(True, wx.SystemSettings.GetColour(wx.SYS_COLOUR_HIGHLIGHTTEXT))
        self.SetSelBackground(True, wx.SystemSettings.GetColour(wx.SYS_COLOUR_HIGHLIGHT))

        # Built in styles
        self.StyleSetSpec(stc.STC_STYLE_LINENUMBER, f"back:#C0C0C0,face:{FACES['mono']},size:12")
        self.StyleSetSpec(stc.STC_STYLE_CONTROLCHAR, f"face:{FACES['mono']}")
        self.StyleSetSpec(stc.STC_STYLE_BRACELIGHT, "fore:#0000FF,back:#FFFF88")
        self.StyleSetSpec(stc.STC_STYLE_BRACEBAD, "fore:#FF0000,back:#FFFF88")

        # Python styles
        self.StyleSetSpec(stc.STC_P_DEFAULT, f"fore:#555555,face:{FACES['mono']}")
        self.StyleSetSpec(stc.STC_P_COMMENTLINE, f"fore:{light_gray},face:{FACES['mono']}")
        self.StyleSetSpec(stc.STC_P_NUMBER, f"fore:{light_blue}")
        self.StyleSetSpec(stc.STC_P_STRING, f"fore:{dark_blue},face:{FACES['mono']}")
        self.StyleSetSpec(stc.STC_P_CHARACTER, f"fore:{dark_blue},face:{FACES['mono']}")
        self.StyleSetSpec(stc.STC_P_WORD, f"fore:{red},bold")
        self.StyleSetSpec(stc.STC_P_TRIPLE, "fore:#7F0000")
        self.StyleSetSpec(stc.STC_P_TRIPLEDOUBLE, "fore:#000033,back:#FFFFE8")
        self.StyleSetSpec(stc.STC_P_CLASSNAME, f"fore:{purple},bold")
        self.StyleSetSpec(stc.STC_P_DEFNAME, f"fore:{purple},bold")
        self.StyleSetSpec(stc.STC_P_OPERATOR, "")
        self.StyleSetSpec(stc.STC_P_IDENTIFIER, "")
        self.StyleSetSpec(stc.STC_P_COMMENTBLOCK, f"fore:{light_gray}")
        self.StyleSetSpec(stc.STC_P_STRINGEOL, f"fore:#000000,face:{FACES['mono']},back:#E0C0E0,eolfilled")

        # Remove border on the left
        self.SetMarginType(1, 0)
        self.SetMarginWidth(1, 0)

    # def OnMove(self, event):
    #     self.MakePrompt()

    def MakePrompt(self):
        wx.CallAfter(self.CallAfterMakePrompt)

    def CallAfterMakePrompt(self):
        if ">>>" not in self.GetText().splitlines()[-1]:
            self.SetCurrentPos(self.GetTextLength())
            self.prompt()
        self.SetFocus()

    def ClearOrFocus(self):
        wx.CallAfter(self.CallAfterClearOrFocus)

    def CallAfterClearOrFocus(self):
        dispatcher.send(signal="FontDefault")
        if self.HasFocus():
            if (
                self.GetCurrentPos() == 0
                or self.GetCurrentPos() == self.GetTextLength()
                and ">>>" not in self.GetText().splitlines()[-1]
            ):
                self.MakePrompt()
            else:
                self.clear()
                self.prompt()
                self.setFocus()
        else:
            self.MakePrompt()
