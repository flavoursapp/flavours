import os
import wx
import shutil
import flavours


def font(family_name, font_name):
    # https://docs.wxpython.org/wx.Font.html#wx.Font.AddPrivateFont
    file_name = family_name.replace(" ", "") + "-" + font_name.replace(" ", "") + ".ttf"
    font_source_path = os.path.join(flavours.BASE_DIR, "resources", "fonts", file_name)
    font_destination_path = os.path.join(wx.StandardPaths.Get().GetResourcesDir(), "Fonts", file_name)

    # Create resource folder
    if not os.path.exists(os.path.dirname(font_destination_path)):
        os.makedirs(os.path.dirname(font_destination_path))

    # Copy font
    shutil.copy2(font_source_path, font_destination_path)

    font = wx.Font(wx.FontInfo(12))
    font.SetFaceName(family_name)
    return font
