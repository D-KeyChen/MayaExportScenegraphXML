# -*- coding: utf-8 -*-
import json
from PySide2 import QtCore, QtWidgets

if not __name__ == "__main__":
    from maya import cmds
    import mainUI
    import listUI
    import FileFunction
    import mayaExportScenegraphXML

    reload(mainUI)
    reload(listUI)
    reload(FileFunction)
    reload(mayaExportScenegraphXML)
    import mayaExportScenegraphXML as mesx
from mainUI import Ui_MainWindow
from listUI import Ui_ListWindow


class export_window(Ui_MainWindow, QtWidgets.QMainWindow):
    parentUI = QtWidgets.QApplication.activeWindow()

    def __init__(self, parent=parentUI):
        # 执行 QWidget 的 __init__
        super(export_window, self).__init__(parent)
        # 从 Ui_Form 继承的方法，可以直接将ui生成出来
        self.setupUi(self)
        # self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
        if __name__ == "__main__":
            self.move(200, 300)
        else:
            self.move(parent.pos().x() + 200,
                      parent.pos().y() + 300)
        # self.show()

        ################

        self.toolButton_extra.pressed.connect(self.on_pressed)
        self.toggle_animation = QtCore.QParallelAnimationGroup(self)

        self.checkBox_Verbose.hide()
        self.checkBox_RenderableOnly.hide()
        self.checkBox_StripNamespaces.hide()
        self.checkBox_WriteColorSets.hide()
        self.checkBox_WriteFaceSets.hide()
        self.checkBox_WholeFrameGeo.hide()
        self.checkBox_WriteVisibility.hide()
        self.checkBox_FilterEulerRotations.hide()
        self.checkBox_WriteCreases.hide()

        ################

        # list window button
        self.pushButt_Com_List.clicked.connect(lambda: self.list_win('Com'))
        self.pushButt_Ass_List.clicked.connect(lambda: self.list_win('Ass'))

        # export button
        self.Button_Export.clicked.connect(self.export_button)
        self.Button_Path.clicked.connect(self.path_button)

        # component assembly button
        self.pushButt_Com_AddSel.clicked.connect(self.com_butt_add)
        self.pushButt_Com_GetSel.clicked.connect(self.com_butt_get)
        self.pushButt_Com_DelSel.clicked.connect(self.com_butt_del)
        self.pushButt_Ass_AddSel.clicked.connect(self.ass_butt_add)
        self.pushButt_Ass_GetSel.clicked.connect(self.ass_butt_get)
        self.pushButt_Ass_DelSel.clicked.connect(self.ass_butt_del)

        self.pushButt_proxy.clicked.connect(self.proxy_butt)

        # root get select button
        self.pushButt_RootName_GetSel.clicked.connect(self.root_butt)

        # Options action
        self.action_Reset.triggered.connect(self.reset_action)
        self.action_Help.triggered.connect(self.help_action)
        self.actionLoad.triggered.connect(self.load_action)
        self.actionSave.triggered.connect(self.save_action)

    def on_pressed(self):
        checked = self.toolButton_extra.isChecked()
        self.toolButton_extra.setArrowType(
            QtCore.Qt.DownArrow
            if not checked
            else QtCore.Qt.RightArrow
        )
        self.toggle_animation.setDirection(
            QtCore.QAbstractAnimation.Forward
            if not checked
            else QtCore.QAbstractAnimation.Backward
        )
        self.toggle_animation.start()

    def message_dialog(self):
        QtWidgets.QMessageBox.warning(self, 'Warning', 'Not running in Maya!')

    def list_win(self, obj):
        self.chile_Win = list_window()
        if obj == 'Com':
            self.chile_Win.labelList.setText('Component List')
            strlist = self.lineEdit_Com.text()
            strlist = strlist.split()
            strlist = '\r'.join(strlist)
            self.chile_Win.textBrowserList.setText(strlist)
        if obj == 'Ass':
            self.chile_Win.labelList.setText('Assembly List')
            strlist = self.lineEdit_Ass.text()
            strlist = strlist.split()
            strlist = '\r'.join(strlist)
            self.chile_Win.textBrowserList.setText(strlist)
            # print(type(text))
        self.chile_Win.move(self.pos().x() + 100,
                            self.pos().y() + 50)
        self.chile_Win.show()

    def process_obj_name(self, obj):
        if obj:
            obj = ", ".join(obj)
            obj = obj + ', '
            str(obj)
        return obj

    def remov_obj(self, obj, old_obj):
        old_obj = [i for i in old_obj.split(', ') if i != '']
        obj = [i for i in obj.split(', ') if i != '']
        for x in obj:
            if x in old_obj:
                old_obj.remove(x)
        if len(old_obj) == 0:
            old_obj = ['empty']
        return old_obj

    def root_butt(self):
        if __name__ == "__main__":
            self.message_dialog()
            return
        obj_sel = cmds.ls(selection=True, long=True)
        if obj_sel:
            self.lineEdit_RootName.setText(obj_sel[-1])
        test_text = self.lineEdit_RootName.text()
        print('Roor Butt Get: ' + test_text)

    # Component
    def com_butt_add(self):
        if __name__ == "__main__":
            self.message_dialog()
            return
        obj_sel = self.process_obj_name(cmds.ls(selection=True))
        if obj_sel:
            old_text = self.lineEdit_Com.text()
            self.lineEdit_Com.setText(old_text + obj_sel)
            print('Com Butt Add: ' + obj_sel)
        else:
            print('Com Butt Add: ')

    def com_butt_get(self):
        if __name__ == "__main__":
            self.message_dialog()
            return
        reply = QtWidgets.QMessageBox.question(
            self, 'Get Select', 'Confirm Get?',
            QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.Cancel,
            QtWidgets.QMessageBox.Cancel)
        if reply == QtWidgets.QMessageBox.Yes:
            obj_sel = self.process_obj_name(cmds.ls(selection=True))
            if obj_sel:
                self.lineEdit_Com.setText(obj_sel)
                print('Com Butt Get: ' + obj_sel)
            else:
                print('Com Butt Get: ')

    def com_butt_del(self):
        old_text = str(self.lineEdit_Com.text())
        sel_obj = self.process_obj_name(cmds.ls(selection=True))
        if sel_obj:
            new_text = self.remov_obj(sel_obj, old_text)
            new_text = self.process_obj_name(new_text)
            if new_text == 'empty, ':
                self.lineEdit_Com.clear()
                print('Com Butt Del: ' + sel_obj)
            elif new_text:
                self.lineEdit_Com.setText(new_text)
                print('Com Butt Del: ' + sel_obj)
            else:
                print('Com Butt Del: ')
        else:
            print('Com Butt Del: ')

    # Assembly
    def ass_butt_add(self):
        if __name__ == "__main__":
            self.message_dialog()
            return
        obj_sel = self.process_obj_name(cmds.ls(selection=True))
        if obj_sel:
            old_text = self.lineEdit_Ass.text()
            self.lineEdit_Ass.setText(old_text + obj_sel)
            print('Ass Butt Add: ' + obj_sel)
        else:
            print('Ass Butt Add: ')

    def ass_butt_get(self):
        if __name__ == "__main__":
            self.message_dialog()
            return
        reply = QtWidgets.QMessageBox.question(
            self, 'Get Select', 'Confirm Get?',
            QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.Cancel,
            QtWidgets.QMessageBox.Cancel)
        if reply == QtWidgets.QMessageBox.Yes:
            obj_sel = self.process_obj_name(cmds.ls(selection=True))
            if obj_sel:
                self.lineEdit_Ass.setText(obj_sel)
                print('Ass Butt Get: ' + obj_sel)
            else:
                print('Ass Butt Get: ')

    def ass_butt_del(self):
        old_text = str(self.lineEdit_Ass.text())
        sel_obj = self.process_obj_name(cmds.ls(selection=True))
        if sel_obj:
            new_text = self.remov_obj(sel_obj, old_text)
            new_text = self.process_obj_name(new_text)
            if new_text == 'empty, ':
                self.lineEdit_Ass.clear()
                print('Ass Butt Del: ' + sel_obj)
            elif new_text:
                self.lineEdit_Ass.setText(new_text)
                print('Ass Butt Del: ' + sel_obj)
            else:
                print('Ass Butt Del: ')
        else:
            print('Ass Butt Del: ')

    def proxy_butt(self):
        if cmds.ls(sl=1):
            proxy_name = cmds.ls(sl=1)[0][cmds.ls(sl=1)[0].rfind('_') + 0:]
            self.lineEdit_proxy.setText(proxy_name)
            print('Pick Postfix: ' + proxy_name)
        else:
            cmds.warning('Pick Postfix: There is no object selected!')

    def path_button(self):
        export_path = QtWidgets.QFileDialog.getExistingDirectory(self, '', '')
        if export_path:
            self.Line_Path.setText(export_path + r'\outXML')

    def export_button(self):
        reply = QtWidgets.QMessageBox.question(
            self, 'Export', 'Confirm export?',
            QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.Cancel,
            QtWidgets.QMessageBox.Cancel)
        if reply == QtWidgets.QMessageBox.Yes:
            # mayaSelection
            root_name = self.lineEdit_RootName.text()
            # exportDirectory
            path_name = self.Line_Path.text()
            # componentName
            com_name = self.lineEdit_Com.text()
            if root_name and com_name and path_name:
                com_name = com_name.split(', ')
                com_name = [i for i in com_name if i != '']
                com_name = map(str, com_name)

                # geoAttr
                geo_attr = ''
                if self.checkBox_UVWrite.isChecked():
                    geo_attr = geo_attr + '-uvWrite '
                if self.checkBox_WorldSpace.isChecked():
                    geo_attr = geo_attr + '-worldSpace '
                if self.checkBox_WritsUvSets.isChecked():
                    geo_attr = geo_attr + '-writeUVSets '
                if self.checkBox_NoNormals.isChecked():
                    geo_attr = geo_attr + '-noNormals '
                if self.checkBox_Verbose.isChecked():
                    geo_attr = geo_attr + '-verbose '
                if self.checkBox_RenderableOnly.isChecked():
                    geo_attr = geo_attr + '-renderableOnly '
                if self.checkBox_StripNamespaces.isChecked():
                    geo_attr = geo_attr + '-stripNamespaces '
                if self.checkBox_WriteColorSets.isChecked():
                    geo_attr = geo_attr + '-writeColorSets '
                if self.checkBox_WriteFaceSets.isChecked():
                    geo_attr = geo_attr + '-writeFaceSets '
                if self.checkBox_WholeFrameGeo.isChecked():
                    geo_attr = geo_attr + '-wholeFrameGeo '
                if self.checkBox_WriteVisibility.isChecked():
                    geo_attr = geo_attr + '-writeVisibility '
                if self.checkBox_FilterEulerRotations.isChecked():
                    geo_attr = geo_attr + '-eulerFilter '
                if self.checkBox_WriteCreases.isChecked():
                    geo_attr = geo_attr + '-autoSubd '

                # animation
                start_frame = None
                end_frame = None
                if self.checkBox_Ani.isChecked():
                    start_frame = int(self.spinBox_Ani_Start.text())
                    end_frame = int(self.spinBox_Ani_End.text())
                # print(start_frame, end_frame)
                # print(type(start_frame), type(end_frame))

                # AssemblyName
                ass_name = self.lineEdit_Ass.text()
                if ass_name.startswith('optional', 0, 8):
                    cmds.warning('The assembly parameter \'optional\' is the default value')
                    ass_name = []
                else:
                    ass_name = ass_name.split(', ')
                    ass_name = [i for i in ass_name if i != '']
                    ass_name = map(str, ass_name)

                # Proxy
                proxy_name = None
                proxy_obj = None
                if self.checkBox_proxy.isChecked():
                    proxy_name = self.lineEdit_proxy.text()
                    proxy_obj = cmds.ls('*' + proxy_name)

                # Cleanup all the attributes that were written on the nodes for the export
                clean_attr = False
                if self.checkBox_cleanAttr.isChecked():
                    clean_attr = True

                if self.checkBox_fileName.isChecked():
                    xml_name = self.lineEdit_fileName.text()
                    if xml_name.find('.') > 0:
                        xml_name = xml_name[:xml_name.find('.')]
                    xml_name = xml_name + '.xml'
                else:
                    xml_name = root_name + '.xml'
                    xml_name = xml_name[xml_name.rfind('|') + 1:]

                if not __name__ == "__main__":
                    mesx.exportScene(maya_root=root_name, export_path=path_name,
                                     xml_name=xml_name,
                                     component_name=com_name, geo_attr=geo_attr,
                                     start_frame=start_frame, end_frame=end_frame,
                                     assembly_name=ass_name,
                                     proxy_name=proxy_name, proxy_obj=proxy_obj,
                                     clean_attr=clean_attr)
                    QtWidgets.QMessageBox.information(self, 'Export receipt',
                                                      ('Successfully exported !\n\nexport directory: ' + path_name))
            else:
                cmds.error('Lack of necessary conditions!')

    # Options action def
    def reset_action(self):
        pass

    def help_action(self):
        QtWidgets.QMessageBox.about(self, 'About', '相关使用说明\n')
        pass

    def save_action(self):
        # save data
        save_file = QtWidgets.QFileDialog.getSaveFileName(None, 'Export as JSON', '',
                                                          'User data in JSON format(*.json)')
        if save_file[0]:
            attribute = {
                self.lineEdit_RootName.objectName(): self.lineEdit_RootName.text(),
                self.checkBox_fileName.objectName(): self.checkBox_fileName.isChecked(),
                self.lineEdit_fileName.objectName(): self.lineEdit_fileName.text(),
                self.lineEdit_Ass.objectName(): self.lineEdit_Ass.text(),
                self.lineEdit_Com.objectName(): self.lineEdit_Com.text(),
                self.checkBox_cleanAttr.objectName(): self.checkBox_cleanAttr.isChecked(),
                self.checkBox_proxy.objectName(): self.checkBox_proxy.isChecked(),
                self.lineEdit_proxy.objectName(): self.lineEdit_proxy.text(),
                self.label_ABCOption.objectName(): {
                    self.checkBox_UVWrite.objectName(): self.checkBox_UVWrite.isChecked(),
                    self.checkBox_WorldSpace.objectName(): self.checkBox_WorldSpace.isChecked(),
                    self.checkBox_NoNormals.objectName(): self.checkBox_NoNormals.isChecked(),
                    self.checkBox_WritsUvSets.objectName(): self.checkBox_WritsUvSets.isChecked(),
                    self.checkBox_Verbose.objectName(): self.checkBox_Verbose.isChecked(),
                    self.checkBox_RenderableOnly.objectName(): self.checkBox_RenderableOnly.isChecked(),
                    self.checkBox_StripNamespaces.objectName(): self.checkBox_StripNamespaces.isChecked(),
                    self.checkBox_WriteColorSets.objectName(): self.checkBox_WriteColorSets.isChecked(),
                    self.checkBox_WriteFaceSets.objectName(): self.checkBox_WriteFaceSets.isChecked(),
                    self.checkBox_WholeFrameGeo.objectName(): self.checkBox_WholeFrameGeo.isChecked(),
                    self.checkBox_WriteVisibility.objectName(): self.checkBox_WriteVisibility.isChecked(),
                    self.checkBox_FilterEulerRotations.objectName(): self.checkBox_FilterEulerRotations.isChecked(),
                    self.checkBox_WriteCreases.objectName(): self.checkBox_WriteCreases.isChecked(),
                },
                self.checkBox_arbAtt.objectName(): self.checkBox_arbAtt.isChecked(),
                self.Line_arbAtt.objectName(): self.Line_arbAtt.text(),
                self.checkBox_Ani.objectName(): self.checkBox_Ani.isChecked(),
                self.spinBox_Ani_Start.objectName(): self.spinBox_Ani_Start.text(),
                self.spinBox_Ani_End.objectName(): self.spinBox_Ani_End.text(),
                self.Line_Path.objectName(): self.Line_Path.text(),

            }
            with open(save_file[0], 'w') as file_obj:
                json.dump(attribute, file_obj, sort_keys=True, indent=4, separators=(',', ': '))
            print('Save the data: ' + save_file[0])

    def load_action(self):
        reply = QtWidgets.QMessageBox.question(
            self, 'Load data', 'Confirm Load?',
            QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.Cancel,
            QtWidgets.QMessageBox.Cancel)
        if reply == QtWidgets.QMessageBox.Yes:
            load_file = QtWidgets.QFileDialog.getOpenFileName(None, 'Import from JSON', '',
                                                              'User data in JSON format(*.json)')
            FileFunction.load_file(self, load_file)


class list_window(Ui_ListWindow, QtWidgets.QWidget):
    def __init__(self):
        super(list_window, self).__init__()
        self.setupUi(self)
        self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)


if __name__ == '__main__':
    import ctypes
    import sys

    ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID("myappid")
    app = QtWidgets.QApplication(sys.argv)
    fromObj = QtWidgets.QMainWindow()
    exp = export_window()
    exp.setupUi(fromObj)
    fromObj.show()
    sys.exit(app.exec_())
