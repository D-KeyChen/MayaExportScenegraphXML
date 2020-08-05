# MayaExportScenegraphXML
 Maya export Scenegraph format to Katana

### Installation

1. Quit Maya

2. Clone MayaExportScenegraphXML repository (or download zip, extract and rename directory from "MayaExportScenegraphXML-master" to "MayaExportScenegraphXML") and place it to:
    ```
    Windows: \Users\<username>\Documents\maya\scripts
    ```

3. Open Script Editor and paste the following code to Python tab:
    ```python
    import MayaExportScenegraphXML
    import MayaExportScenegraphXML.XMLExportUI
    reload(MayaExportScenegraphXML.XMLExportUI)
    import MayaExportScenegraphXML.maya2scenegraphXML
    reload(MayaExportScenegraphXML.maya2scenegraphXML)
    if 'exp_win' in globals():
        exp_win.close()
    exp_win = MayaExportScenegraphXML.XMLExportUI.export_window()
    exp_win.show()
    ```
4. To create a shelf button select the code and middle-mouse-drag it to your shelf
