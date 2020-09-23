# -*- coding: UTF-8 -*-

import os.path
import shutil
import maya2scenegraphXML

reload(maya2scenegraphXML)
from maya import cmds, mel


def attribute_exists(att, obj):
    """
    Use attributeExists to check whether a given attribute exists on a node. 
    使用 attributeExists 检查节点上是否存在给定属性。
    """
    return mel.eval('attributeExists %s %s' % (att, obj))


def set_children_com(obj):
    '''
    Set the children of "ass" to "com"
    将“ ass”的子级设置为“ com”
    '''
    child_nodes = cmds.listRelatives(obj, fullPath=True, children=True)
    if child_nodes is not None:
        for mayaChildPath in child_nodes:
            maya2scenegraphXML.setComponent([mayaChildPath], refType='abc') if not attribute_exists(
                'sgxml_nodeGroupType', mayaChildPath) else False
            maya2scenegraphXML.deleteSgxmlAttr(mayaChildPath, 'sgxml_nodeType') if attribute_exists(
                'sgxml_nodeGroupType', mayaChildPath) else False
            maya2scenegraphXML.deleteSgxmlAttr(mayaChildPath, 'sgxml_refType') if attribute_exists(
                'sgxml_nodeGroupType', mayaChildPath) else False


def set_parent_ass(obj):
    '''
    Set the parent of "com" to "ass"
    将“ com”的父级设置为“ ass”
    '''
    obj = cmds.listRelatives(obj, fullPath=True, parent=True)[0]
    maya2scenegraphXML.setAssembly([obj]) if not attribute_exists('sgxml_nodeGroupType', obj) else False
    maya2scenegraphXML.deleteSgxmlAttr(obj, 'sgxml_nodeType') if attribute_exists('sgxml_nodeType', obj) else False
    maya2scenegraphXML.deleteSgxmlAttr(obj, 'sgxml_refType') if attribute_exists('sgxml_refType', obj) else False
    set_children_com(obj)


# exportScene
def exportScene(maya_root, export_path, xml_name, component_name,
                assembly_name=None, start_frame=None,
                end_frame=None, user_arb=None, geo_attr='',
                proxy_name=None, proxy_obj=None,
                clean_attr=False):
    # geoAttr = ' '.join(geoAttr)
    xml_path_name = os.path.join(export_path, xml_name)
    maya_root = [maya_root]

    # Make sure we will have a clean directory
    # 确保我们将有一个干净的目录
    if export_path and os.path.exists(export_path):
        shutil.rmtree(export_path)

    # Mark the house node as an assembly
    # 将house节点标记为assembly
    maya2scenegraphXML.setAssembly(assembly_name)

    # Mark the tree, ground, smoke and both parts of the house as components
    # 把树、地面、烟和房子的两个部分都标记为组件
    maya2scenegraphXML.setComponent(component_name, refType='abc')

    # Component/Assembly add judgment, Priority retention of Assembly
    # Component / Assembly 添加判断, 优先保留Assembly
    [set_parent_ass(x) for x in component_name]
    [set_children_com(x) for x in assembly_name]

    if proxy_obj and proxy_name:
        maya2scenegraphXML.setStaticComponent(proxy_obj, refType='abc')
        for x in proxy_obj:
            maya2scenegraphXML.setProxy([x[:-len(proxy_name)]], x + '.abc')

    # Export the scene
    # 导出的场景
    # print(mayaSelection, xmlPathName, geoAttr)
    maya2scenegraphXML.maya2ScenegraphXML(mayaSelection=maya_root,
                                          xmlFileName=xml_path_name,
                                          startFrame=start_frame,
                                          endFrame=end_frame,
                                          arbAttrs=user_arb,
                                          geoFileOptions=geo_attr)

    # Export proxies geometry
    if proxy_obj and proxy_name:
        for proxyGroup in proxy_obj:
            proxy_file_name = proxyGroup[:-len(proxy_name)] + "_proxy.abc"
            proxy_file_path = os.path.join(export_path, proxy_file_name)
            print("Exporting Proxy: %s" % proxy_file_path)
            cmds.AbcExport(j="-uv -root %s -file %s" % (proxyGroup, proxy_file_path))

    # Cleanup all the attributes that were written on the nodes for the export
    # (this is optional)
    # 清除为导出写入节点上的所有属性
    # (这是可选的)
    if clean_attr:
        maya2scenegraphXML.deleteSgxmlAttrs(maya_root)
        maya2scenegraphXML.deleteSgxmlAttrs(proxy_obj)
