import os
import wx
import flavours
from functools import partial
import threading


def MakeScriptsMenu(event):

    path = os.path.join(flavours.working_directory, "scripts")

    frame = flavours.app.frames[0]
    menu = wx.Menu()
    for root, dir, files in os.walk(path):
        for file in files:
            m_script = menu.Append(
                wx.NewIdRef(count=1),
                file,
            )
            frame.Bind(
                wx.EVT_MENU,
                partial(
                    OnScriptExecute,
                    file_path=os.path.join("scripts", file),
                ),
                m_script,
            )

    i = frame.menuBar.FindMenu("&Scripts")
    frame.menuBar.Remove(i)
    frame.menuBar.Insert(i, menu, "&Scripts")


def OnScriptExecute(event, file_path):
    flavours.app.frames[0].shell.run(f'run("{file_path}")', prompt=False)
    flavours.app.frames[0].shell.MakePrompt()


def run(file_path):
    if not file_path.startswith("/"):
        file_path = os.path.join(flavours.working_directory, file_path)
    with open(file_path, "r") as file:

        # TODO
        # Make this run from a thread so that the GUI shell updates on prints
        # t = threading.Thread(target=exec, args=(file.read(),))
        # t.start()
        exec(file.read())
