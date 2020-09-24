# -*- coding: utf-8 -*-
"""
@version: python 2.7.11
@author: D-Key
@Email: Demon_Key@163.com
@TencentQQ: 1915417167
@file: FileFunction.py
@time: 20/8/3 17:38
"""
import json
from maya import cmds


def load_file(self, file_path):
    if file_path[0]:
        print('Load the data: ' + file_path[0])
        with open(file_path[0]) as file_obj:
            load_data = json.load(file_obj)

        if 'lineEdit_RootName' in load_data.keys():
            self.lineEdit_RootName.setText(load_data['lineEdit_RootName'])
        else:
            cmds.warning('There are no Root Name parameters')

        if 'checkBox_fileName' in load_data.keys():
            self.checkBox_fileName.setChecked(load_data['checkBox_fileName'])
            self.lineEdit_fileName.setText(load_data['lineEdit_fileName'])
        else:
            cmds.warning('There are no File Name parameters')

        if 'lineEdit_Ass' in load_data.keys():
            self.lineEdit_Ass.setText(load_data['lineEdit_Ass'])
        else:
            cmds.warning('There are no Assembly parameters')

        if 'lineEdit_Com' in load_data.keys():
            self.lineEdit_Com.setText(load_data['lineEdit_Com'])
        else:
            cmds.warning('There are no Component parameters')

        if 'checkBox_cleanAttr' in load_data.keys():
            self.checkBox_cleanAttr.setChecked(load_data['checkBox_cleanAttr'])
        else:
            cmds.warning('There are no Clean Attr parameters')

        if 'checkBox_proxy' in load_data.keys():
            self.checkBox_proxy.setChecked(load_data['checkBox_proxy'])
            self.label_proxy.setEnabled(load_data['checkBox_proxy'])
            self.lineEdit_proxy.setEnabled(load_data['checkBox_proxy'])
            self.pushButt_proxy.setEnabled(load_data['checkBox_proxy'])
            self.lineEdit_proxy.setText(load_data['lineEdit_proxy'])
        else:
            cmds.warning('There are no proxy parameters')

        if 'label_ABCOption' in load_data.keys():
            if 'checkBox_UVWrite' in load_data['label_ABCOption'].keys():
                self.checkBox_UVWrite.setChecked(load_data['label_ABCOption']['checkBox_UVWrite'])
            if 'checkBox_WorldSpace' in load_data['label_ABCOption'].keys():
                self.checkBox_WorldSpace.setChecked(load_data['label_ABCOption']['checkBox_WorldSpace'])
            if 'checkBox_NoNormals' in load_data['label_ABCOption'].keys():
                self.checkBox_NoNormals.setChecked(load_data['label_ABCOption']['checkBox_NoNormals'])
            if 'checkBox_WritsUvSets' in load_data['label_ABCOption'].keys():
                self.checkBox_WritsUvSets.setChecked(load_data['label_ABCOption']['checkBox_WritsUvSets'])
            if 'checkBox_Verbose' in load_data['label_ABCOption'].keys():
                self.checkBox_Verbose.setChecked(load_data['label_ABCOption']['checkBox_Verbose'])
            if 'checkBox_RenderableOnly' in load_data['label_ABCOption'].keys():
                self.checkBox_RenderableOnly.setChecked(load_data['label_ABCOption']['checkBox_RenderableOnly'])
            if 'checkBox_StripNamespaces' in load_data['label_ABCOption'].keys():
                self.checkBox_StripNamespaces.setChecked(
                    load_data['label_ABCOption']['checkBox_StripNamespaces'])
            if 'checkBox_WriteColorSets' in load_data['label_ABCOption'].keys():
                self.checkBox_WriteColorSets.setChecked(load_data['label_ABCOption']['checkBox_WriteColorSets'])
            if 'checkBox_WriteFaceSets' in load_data['label_ABCOption'].keys():
                self.checkBox_WriteFaceSets.setChecked(load_data['label_ABCOption']['checkBox_WriteFaceSets'])
            if 'checkBox_WholeFrameGeo' in load_data['label_ABCOption'].keys():
                self.checkBox_WholeFrameGeo.setChecked(load_data['label_ABCOption']['checkBox_WholeFrameGeo'])
            if 'checkBox_WriteVisibility' in load_data['label_ABCOption'].keys():
                self.checkBox_WriteVisibility.setChecked(
                    load_data['label_ABCOption']['checkBox_WriteVisibility'])
            if 'checkBox_FilterEulerRotations' in load_data['label_ABCOption'].keys():
                self.checkBox_FilterEulerRotations.setChecked(
                    load_data['label_ABCOption']['checkBox_FilterEulerRotations'])
            if 'checkBox_WriteCreases' in load_data['label_ABCOption'].keys():
                self.checkBox_WriteCreases.setChecked(load_data['label_ABCOption']['checkBox_WriteCreases'])
        else:
            cmds.warning('There are no Alembic Options parameters')

        if 'checkBox_arbAtt' in load_data.keys():
            self.checkBox_arbAtt.setChecked(load_data['checkBox_arbAtt'])
            self.Line_arbAtt.setText(load_data['Line_arbAtt'])

        if 'checkBox_Ani' in load_data.keys():
            self.checkBox_Ani.setChecked(load_data['checkBox_Ani'])
            self.label_Ani_Start.setEnabled(load_data['checkBox_Ani'])
            self.label_Ani_End.setEnabled(load_data['checkBox_Ani'])
            self.spinBox_Ani_Start.setEnabled(load_data['checkBox_Ani'])
            self.spinBox_Ani_End.setEnabled(load_data['checkBox_Ani'])
            if 'spinBox_Ani_Start' in load_data.keys():
                self.spinBox_Ani_Start.setValue(int(load_data['spinBox_Ani_Start']))
            if 'spinBox_Ani_End' in load_data.keys():
                self.spinBox_Ani_End.setValue(int(load_data['spinBox_Ani_End']))

        if 'Line_Path' in load_data.keys():
            self.Line_Path.setText(load_data['Line_Path'])
