import sys
sys.path.append(
    r'C:\Users\Administrator\OneDrive\myScripts\Python\maya_to_katana\MayaExportScenegraphXML'
)
import XMLExportUI
reload(XMLExportUI)
import maya2scenegraphXML
reload(maya2scenegraphXML)
if 'exp_win' in globals():
    exp_win.close()
exp_win = XMLExportUI.export_window()
exp_win.show()
