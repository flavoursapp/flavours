import wx
import os
import sys
import plistlib

app = wx.App()
path = os.path.abspath(os.path.join(wx.StandardPaths.Get().GetResourcesDir(), "..", "Info.plist"))

with open(path, "rb") as f:
    plist = plistlib.load(f)

if sys.argv[-1] == "change":
    plist["CFBundleName"] = "Flavours"
    plist["CFBundleExecutable"] = "Flavours"

elif sys.argv[-1] == "revert":
    plist["CFBundleName"] = "Python"
    plist["CFBundleExecutable"] = "Python"

with open(path, "wb") as f:
    plistlib.dump(plist, f)

# Move app
path_original = os.path.abspath(os.path.join(wx.StandardPaths.Get().GetResourcesDir(), "..", ".."))
if sys.argv[-1] == "change":
    path_new = path_original.replace("Python.app", "Flavours.app")
elif sys.argv[-1] == "revert":
    path_new = path_original.replace("Flavours.app", "Python.app")

# os.system(f"mv {path_original} {path_new}")
