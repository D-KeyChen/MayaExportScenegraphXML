# -*- coding: UTF-8 -*-
# Copyright (c) 2012 The Foundry Visionmongers Ltd. All Rights Reserved.

import maya.cmds as cmds
import os.path
import scenegraphXML

reload(scenegraphXML)

# Make sure the Alembic plugin is loaded
cmds.loadPlugin('AbcExport', quiet=True)

# Module level global used to hold animating bounds data from alembic callbacks
animBoundsData = {}


# Main function called to actually export from Maya to ScenegraphXML format
# 调用主函数来实际导出从Maya到ScenegraphXML格式
def maya2ScenegraphXML(mayaSelection, xmlFileName, startFrame=None, endFrame=None,
                       arbAttrs=None, geoFileOptions=''):
    # Strip xmlFileName into directory and file name components
    # 将xmlFileName剥离到目录和文件名组件中
    fileDir, fileStem = os.path.split(xmlFileName)

    # Strip fileStem of .xml extension if it has one
    # 删除.xml扩展名的fileStem(如果有的话)
    if fileStem.endswith('.xml'):
        fileStem = fileStem[:-4]

    # Clear the animBoundsData
    # 清除animBoundsData
    animBoundsData = {}

    # Construct python classes to represent Maya Hierarchy using scenegraphXML.py
    # 使用scenegraphXML.py构造python类来表示Maya层次结构
    sgxmlHandler = MayaSgxmlHandler(mayaSelection=mayaSelection,
                                    fileDir=fileDir,
                                    fileStem=fileStem,
                                    startFrame=startFrame,
                                    endFrame=endFrame,
                                    arbAttrs=arbAttrs,
                                    geoFileOptions=geoFileOptions)

    sgxmlHandler.writeChannelData()

    # Write the scenegraphXML files for the hierarchical components
    # 编写用于层次结构组件的scenegraphXML文件
    sgxmlHandler.writeSgxml()

    # Write the accompanying animating channel data files
    # 编写随附的动画通道数据文件
    # sgxmlHandler.writeChannelData()


def addAnimBoundsData(mayaNode, frame, bounds):
    # Adds an entry in animBoundsData for mayaNode for the current frame.
    # 为当前帧的mayaNode在animBoundsData中添加一个条目
    if not mayaNode in animBoundsData:
        animBoundsData[mayaNode] = {}
    animBoundsData[mayaNode][frame] = bounds


def maya2abcCallback(mayaNode, frame, bounds):
    # Callback used to store animating bounds information calculated when exporting using Alembic.
    # Needs to convert order of bounds data from [minx, miny, minz, maxx, maxy, maxz] to [minx, maxx, miny, maxy, minz, maxz]
    # 回调函数用于存储在使用Alembic导出时计算出的动画边界信息
    # 需要将边界数据的顺序从[minx, miny, minz, maxx, maxy, maxz]转换为[minx, maxx, miny, maxy, minz, maxz]
    addAnimBoundsData(mayaNode, frame, [
                      bounds[0], bounds[3], bounds[1], bounds[4], bounds[2], bounds[5]])


def maya2Abc(mayaParent, mayaSelection, filepath, startFrame=None, endFrame=None, abcOptions=''):
    # check that we actually have elements in the mayaSelection
    if mayaSelection:
        # create the directory if it doesn't exist
        dir = os.path.dirname(filepath)
        if not os.path.isdir(dir):
            os.makedirs(dir)
        abcCommandString = abcOptions + ' -root ' + \
            ' -root '.join(mayaSelection) + ' -file ' + filepath
        # add Python callback to store bounding box information
        # abcCommandString = 'pythonPerFrameCallback=maya2scenegraphXML.maya2abcCallback(mayaNode="'+mayaParent+'",frame=#FRAME#,bounds=#BOUNDSARRAY#) ' + abcCommandString
        abcCommandString = '-pythonPerFrameCallback maya2scenegraphXML.maya2abcCallback(mayaNode="' + \
            mayaParent+'",frame=#FRAME#,bounds=#BOUNDSARRAY#) ' + abcCommandString
        if startFrame is not None and endFrame is not None:
            abcCommandString = '-frameRange ' + \
                str(startFrame) + ' ' + str(endFrame) + ' ' + abcCommandString
            #abcCommandString = 'range ' + str(startFrame) + ' ' + str(endFrame) + ' ' + abcCommandString

        print("Command string: %s" % abcCommandString)
        cmds.AbcExport(j=abcCommandString)
    else:
        cmds.warning("%s doesn't have any children to export as a component"
                     % mayaParent)


def getMayaNodeName(mayaPath):
    nameParts = mayaPath.rstrip('|').rsplit('|', 1)
    return nameParts[-1]


def mayaNode2FileStem(mayaPath):
    return mayaPath.lstrip('|').replace('_', '__').replace('|', '_')


def mayaNode2FilePath(mayaPath, directory, extension=None, relativePath=True):
    # check if the node explicitly defines a file path
    if cmds.listAttr(mayaPath, st=['sgxml_filepath']):
        return cmds.getAttr(mayaPath + '.sgxml_filepath', x=True)
    else:
        basePath = mayaPath.lstrip('|').replace('_', '__').replace('|', '_')
        if not relativePath:
            basePath = os.path.join(directory, basePath)
        if extension is None:
            return basePath
        else:
            return basePath + '.' + extension


def getValidChildren(mayaElementPath):
    validChildren = []
    childNodes = cmds.listRelatives(mayaElementPath, fullPath=True)
    if childNodes is not None:
        for mayaChildPath in childNodes:
            # check if the node is set to 'ignore'
            if cmds.listAttr(mayaChildPath, st=['sgxml_ignore']) is None:
                # check if this is a valid instance node. We only process transform nodes
                curNodeType = cmds.nodeType(mayaChildPath)
                if curNodeType == 'transform':
                    validChildren.append(mayaChildPath)
    return validChildren


def getAttrOrNone(mayaPath, attrName):
    if cmds.listAttr(mayaPath, st=[attrName]):
        return cmds.getAttr(mayaPath + '.' + attrName)
    else:
        return None


def getAttrOrZero(mayaPath, attrName):
    if cmds.listAttr(mayaPath, st=[attrName]):
        return cmds.getAttr(mayaPath + '.' + attrName)
    else:
        return 0


def isAnimated(mayaPath, attrName):
    return cmds.connectionInfo(mayaPath+'.'+attrName, isDestination=True)


def isXformAnimated(mayaPath):
    if isAnimated(mayaPath, 'tx') or isAnimated(mayaPath, 'ty') or \
       isAnimated(mayaPath, 'tz') or isAnimated(mayaPath, 'rx') or \
       isAnimated(mayaPath, 'ry') or isAnimated(mayaPath, 'rz') or \
       isAnimated(mayaPath, 'sx') or isAnimated(mayaPath, 'sy') or \
       isAnimated(mayaPath, 'sz'):
        return True
    else:
        return False


def getAnimBoundsData(mayaPath, frameNumber):
    # check if we have bounds data for this maya node in animBoundsData
    if mayaPath in animBoundsData.keys():
        curAnimBounds = animBoundsData[mayaPath]
        # check if we have animating values or not
        if len(curAnimBounds) == 1:
            # bounds are static, so take the value from the single element in the dictionary
            return curAnimBounds.values()[0]
        else:
            # bounds are animated so we should have a matching value for this frame
            if frameNumber in curAnimBounds:
                return curAnimBounds[frameNumber]
            else:
                raise ValueError, 'matching anim bounds value not found'
    else:
        return None


def deleteSgxmlAttr(mayaPath, attrName):
    # 删除属性
    if cmds.listAttr(mayaPath, st=[attrName]):
        cmds.deleteAttr(mayaPath, at=attrName)


def deleteSgxmlAttrs(mayaPath):
    # 删除所有子集的所有下列全部属性
    deleteSgxmlAttr(mayaPath, 'sgxml_assembly')
    deleteSgxmlAttr(mayaPath, 'sgxml_component')
    deleteSgxmlAttr(mayaPath, 'sgxml_reference')
    deleteSgxmlAttr(mayaPath, 'sgxml_nodeType')
    deleteSgxmlAttr(mayaPath, 'sgxml_filepath')
    deleteSgxmlAttr(mayaPath, 'sgxml_refType')
    deleteSgxmlAttr(mayaPath, 'sgxml_ignore')
    deleteSgxmlAttr(mayaPath, 'sgxml_boundsWriteMode')
    deleteSgxmlAttr(mayaPath, 'sgxml_lodTag')
    deleteSgxmlAttr(mayaPath, 'sgxml_lodWeight')
    deleteSgxmlAttr(mayaPath, 'sgxml_proxyName')
    deleteSgxmlAttr(mayaPath, 'sgxml_proxyFile')
    childNodes = cmds.listRelatives(mayaPath, fullPath=True)
    if childNodes is not None:
        for mayaChildPath in childNodes:
            deleteSgxmlAttrs(mayaChildPath)


def mayaAddStringAttribute(curItem, attrName, attrVal):
    if curItem is not None:
        # check that the cmpt attribute doesn't aleady exist
        if not cmds.listAttr(curItem, st=[attrName]):
            cmds.addAttr(curItem, ln=attrName, dt='string')
            cmds.setAttr(curItem + '.' + attrName, keyable=True)
        cmds.setAttr(curItem + '.' + attrName, attrVal, type='string')


def mayaAddStringAttributeToShape(curItem, attrName, attrVal):
    # get shapes node for current item
    # 获取当前项的形状节点
    shapes = cmds.listRelatives(curItem, shapes=True)
    if shapes is not None:
        # we assume there is only one shape
        # 我们假设只有一个形状
        curShape = shapes[0]
        # check that the cmpt attribute doesn't aleady exist
        # 检查 cmpt (传入的 attrName) 属性是否存在, 不存在即添加
        if not cmds.listAttr(curShape, st=[attrName]):
            cmds.addAttr(curShape, ln=attrName, dt='string')
            cmds.setAttr(curShape + '.' + attrName, keyable=True)
        # 修改属性值: 名 attrName 值 attrVal
        cmds.setAttr(curShape + '.' + attrName, attrVal, type='string')


def mayaAssignTag(selection, tagName, tagValue):
    if selection is None:
        selection = cmds.ls(selection=True)
    if selection is not None:
        for curItem in selection:
            mayaAddStringAttribute(curItem, tagName, tagValue)


def mayaAssignTagToShape(selection, tagName, tagValue):
    if selection is None:
        selection = cmds.ls(selection=True)
    if selection is not None:
        for curItem in selection:
            mayaAddStringAttributeToShape(curItem, tagName, tagValue)


class ChannelHandler:
    # holds data for animated channels prior to export as ScenegraphXML channel files
    # 在导出为ScenegraphXML通道文件之前，保存动画通道的数据

    def __init__(self, channelData):
        self.xmlChannelData = channelData
        self.mayaChannelData = []

    def addMayaChannel(self, mayaPath, attrName, channelIndex):
        newChannelData = [mayaPath, attrName, channelIndex]
        self.mayaChannelData.append(newChannelData)


class MayaSgxmlHandler:
    # creates python classes using scenegraphXML.py to represent Maya hierarchy data
    # 使用scenegraphXML.py创建python类来表示Maya层次结构数据

    def __init__(self, mayaSelection, fileDir, fileStem, startFrame=None, endFrame=None,
                 arbAttrs=None, geoFileOptions=None, boundsWriteMode='all', mayaParent=None):
        self.mayaSelection = mayaSelection
        self.mayaParent = mayaParent
        self.fileDir = fileDir
        self.fileStem = fileStem
        self.startFrame = startFrame
        self.endFrame = endFrame
        self.arbAttrs = arbAttrs
        self.geoFileOptions = geoFileOptions
        self.boundsWriteMode = boundsWriteMode
        self.childHandlers = []
        self.mayaChannelData = []
        self.numChannels = 0
        self.rangeMaxBoundsList = []

        # iterate over the hierachy and create scenegraphXML element to hold data for
        # any Maya nodes that need to be written out to scenegraphXML
        # 遍历层次结构并创建scenegraphXML元素来保存需要写入scenegraphXML的任何Maya节点的数据

        # create root element for scenegraphXML data
        # 为scenegraphXML数据创建根元素
        self.root = scenegraphXML.ScenegraphRoot()

        # if required, create channel data handler for animation data
        # 如果需要，为动画数据创建通道数据处理程序
        # if startFrame is not None and endFrame is not None:
        # 如果startFrame不为None且endFrame不为None
        chanPath = self.fileStem
        if self.fileDir is not None:
            chanPath = os.path.join(self.fileDir, chanPath)

        if self.isStatic():
            frameNo = self.getStaticFrameNo()
            self.root.channelData = scenegraphXML.ChannelData(frameNo, frameNo)
        else:
            self.root.channelData = scenegraphXML.ChannelData(
                startFrame, endFrame, chanPath)

        # iterate through the Maya selection list creating a SgXML hierarchy for each
        # instance and add them to the root SgXML element
        # 遍历Maya选择列表，为每个实例创建SgXML层次结构并将其添加到根SgXML元素
        for curMayaElement in self.mayaSelection:
            curInstance = self.createSgXMLHierarchy(curMayaElement)
            self.root.addInstance(curInstance)

    def isStatic(self):
        return self.startFrame == self.endFrame

    def getStaticFrameNo(self):
        if self.startFrame == None:
            return 1

        return self.startFrame

    def createSgXMLHierarchy(self, mayaElementPath):
        curNodeName = getMayaNodeName(mayaElementPath)

        nodeType = getAttrOrNone(mayaElementPath, 'sgxml_nodeType')
        newElement = None

        nodeGroupType = getAttrOrNone(mayaElementPath, 'sgxml_nodeGroupType')

        dirUsed = self.fileDir
        stemUsed = ''

        if nodeType == 'xmlReference':
            # The hierarchy under here needs to be written out as another SgXML file.
            # We create a new MayaSgxmlHandler for the sub hierarchy and add it to the
            # list child handlers on this class so that we can later write our all the
            # SgXML files together

            # Allow to overwrite the name and path of the destination file
            nodeFilepath = getAttrOrNone(mayaElementPath, 'sgxml_filepath')
            if nodeFilepath:
                fileDir = os.path.dirname(nodeFilepath)
                if fileDir:
                    dirUsed = fileDir
                fileBase = os.path.basename(nodeFilepath)
                stemUsed = os.path.splitext(fileBase)[0]
            else:
                stemUsed = mayaNode2FileStem(mayaElementPath)

            filepath = mayaNode2FilePath(
                mayaElementPath, self.fileDir, 'xml', relativePath=True)
            newElement = scenegraphXML.Reference(
                curNodeName, refFile=filepath, groupType=nodeGroupType)
            elementChildList = getValidChildren(mayaElementPath)
            newChildHandler = MayaSgxmlHandler(mayaSelection=elementChildList,
                                               fileDir=dirUsed,
                                               fileStem=stemUsed,
                                               startFrame=self.startFrame,
                                               endFrame=self.endFrame,
                                               arbAttrs=self.arbAttrs,
                                               geoFileOptions=self.geoFileOptions,
                                               boundsWriteMode=self.boundsWriteMode,
                                               mayaParent=mayaElementPath)
            self.childHandlers.append(newChildHandler)

        elif nodeType == 'component' or nodeType == 'staticComponent':
            # This is a component, so write out the maya node tree under this node as a
            # alembic format .abc file
            # (Would be nice to generalise this later)

            refType = getAttrOrNone(mayaElementPath, 'sgxml_refType')

            elementChildList = getValidChildren(mayaElementPath)
            if not elementChildList and mayaElementPath:
                elementChildList = [mayaElementPath]

            if refType == 'abc':
                filepath = mayaNode2FilePath(
                    mayaElementPath, self.fileDir, 'abc', relativePath=True)
                newElement = scenegraphXML.Reference(
                    curNodeName, refType='abc', refFile=filepath, groupType=nodeGroupType)
                abcFilePath = mayaNode2FilePath(
                    mayaElementPath, self.fileDir, 'abc', relativePath=False)

                # if staticComponent force no writing of animation in the abc file
                if nodeType == 'staticComponent':
                    maya2Abc(mayaElementPath, elementChildList,
                             abcFilePath, None, None, self.geoFileOptions)
                else:
                    maya2Abc(mayaElementPath, elementChildList, abcFilePath,
                             self.startFrame, self.endFrame, self.geoFileOptions)

        elif nodeType == 'reference':
            # This is a reference to an already existing .abc or .xml file
            newElement = scenegraphXML.Reference(curNodeName)
            refType = getAttrOrNone(mayaElementPath, 'sgxml_refType')
            if refType == 'abc':
                filepath = mayaNode2FilePath(
                    mayaElementPath, self.fileDir, 'abc', relativePath=True)
            else:
                filepath = mayaNode2FilePath(
                    mayaElementPath, self.fileDir, 'xml', relativePath=True)

            newElement = scenegraphXML.Reference(
                curNodeName, refType=refType, refFile=filepath, groupType=nodeGroupType)

        else:
            # group node type
            newElement = scenegraphXML.Group(curNodeName)
            if nodeType is not None:
                newElement.groupType = nodeType
            else:
                relShapes = cmds.listRelatives(curNodeName, shapes=True)
                if relShapes is not None:
                    cmds.warning("'%s' is not defined. The geometry will not "
                                 "be included in the scenegraph."
                                 % curNodeName)

            if nodeGroupType is not None:  # Overrides type if set explicitly
                newElement.groupType = nodeGroupType

            childNodes = cmds.listRelatives(mayaElementPath, fullPath=True)
            if childNodes is not None:
                for mayaChildPath in childNodes:
                    # check if the node isn't set to 'ignore'
                    if cmds.listAttr(mayaChildPath, st=['sgxml_ignore']) is None:
                        # check if this is a valid instance node. For now we only
                        # process transform nodes
                        curNodeType = cmds.nodeType(mayaChildPath)
                        if curNodeType == 'transform':
                            childElement = self.createSgXMLHierarchy(
                                mayaChildPath)
                            newElement.addInstance(childElement)

        # process xform
        # In the instances where a component has shape nodes i.e. it's Maya geometry
        # we are not going to export the transform to the scenegraph XML as it is
        # also exported to the Alembic file and we can't currently specify to the
        # Alembic exporter to leave the root node transform out of the export so for
        # the time being we are going to just leave it out of the scenegraph file.
        #
        # test if xform is animating
        refType = getAttrOrNone(mayaElementPath, 'sgxml_refType')
        if cmds.listRelatives(mayaElementPath, shapes=True) and refType == 'abc':
            cmds.warning("%s contains a shape node. Transforms will be stored "
                         "in the Alembic file to prevent double transforms."
                         % mayaElementPath)
        else:
            if self.isFrameRangeSet() and isXformAnimated(mayaElementPath):
                newChannelIndex = self.newAnimChannel(
                    mayaElementPath, 'xform', 16)
                newElement.setXform(channelIndex=newChannelIndex)
            else:
                xform = cmds.xform(mayaElementPath, query=True,
                                   matrix=True, objectSpace=True)
                newElement.setXform(value=xform)

        # process bounds
        # Check if local override has been set to force the boundsWriteMode on this node
        processBounds = getAttrOrNone(mayaElementPath, 'sgxml_boundsWriteMode')
        if processBounds is None:
            if self.boundsWriteMode == 'all':
                processBounds = True
            elif self.boundWritesMode == 'none':
                processBounds = False
            else:
                # by default we only write bounds for assembly, component of reference nodes
                # Now supporting static components (no animation)
                processBounds = nodeType in (
                    'assembly', 'component', 'staticComponent', 'reference')

        customBounds = getAttrOrNone(mayaElementPath, 'sgxml_customBounds')
        if customBounds:
            newChannelIndex = self.newAnimChannel(
                mayaElementPath, 'customBounds', 6)

        if processBounds:
            newChannelIndex = self.newAnimChannel(mayaElementPath, 'bounds', 6)

            if self.isStatic():
                self.root.addChannelMapping(newChannelIndex, newElement)
                newElement.setBounds(channelIndex=newChannelIndex)
            else:
                newElement.setBounds(channelIndex=newChannelIndex)

        # process lodData
        lodTag = getAttrOrNone(mayaElementPath, 'sgxml_lodTag')
        lodWeight = getAttrOrNone(mayaElementPath, 'sgxml_lodWeight')
        if lodTag is not None or lodWeight is not None:
            newElement.setLodData(tag=lodTag, weight=lodWeight)

        # process proxyList
        # 进程proxyList
        # note: currently only supports single proxy in proxyList
        # 注意：目前仅支持proxyList中的单个代理
        proxyName = getAttrOrNone(mayaElementPath, 'sgxml_proxyName')
        proxyFile = getAttrOrNone(mayaElementPath, 'sgxml_proxyFile')
        if proxyName is not None and proxyFile is not None:
            newElement.addProxy(name=proxyName, ref=proxyFile)

        # process arbitrary attributes
        if self.arbAttrs is not None:
            for attrName in self.arbAttrs:
                curVal = getAttrOrNone(mayaElementPath, 'arbAttr_' + attrName)
                if curVal is not None:
                    if isinstance(curVal, float):
                        # animated float attribute case
                        if self.isFrameRangeSet() and isAnimated(mayaElementPath, 'arbAttr_'+attrName):
                            newChannelIndex = self.newAnimChannel(mayaElementPath,
                                                                  'arbAttr_' + attrName, 1)
                            newElement.addArbitraryAttribute(name=attrName, dataType='float',
                                                             channelIndex=newChannelIndex)
                        # static float attribute case
                        else:
                            newElement.addArbitraryAttribute(name=attrName, dataType='float',
                                                             value=curVal)
                    # string case
                    elif isinstance(curVal, str) or isinstance(curVal, unicode):
                        newElement.addArbitraryAttribute(name=attrName, dataType='string',
                                                         value=curVal)
                    else:
                        print(type(curVal))
                        raise ValueError(
                            'unsupported arbitrary attribute type')

        return newElement

    def isFrameRangeSet(self):
        if self.startFrame is None or self.endFrame is None or self.startFrame == self.endFrame:
            return False
        else:
            return True

    def newAnimChannel(self, mayaPath, attrName, numChannels):
        channelIndex = self.numChannels
        self.mayaChannelData.append(
            [mayaPath, attrName, channelIndex, numChannels])
        self.numChannels += numChannels
        return channelIndex

    def newRangeMaxBounds(self, mayaPath, sgxmlElement):
        self.rangeMaxBoundsList.append([mayaPath, sgxmlElement])

    def writeSgxml(self):
        # construct full file path for ScenegraphXML file
        fullFilePath = self.fileStem + '.xml'
        if self.fileDir is not None:
            fullFilePath = os.path.join(self.fileDir, fullFilePath)

        # write our file for the SgXML handler
        self.root.writeXMLFile(fullFilePath)

        # write out files for child SgXML handlers
        for curChildHandler in self.childHandlers:
            curChildHandler.writeSgxml()

    def writeChannelData(self):
        # write the channel data for the animation range for this and any child handlers
        # note: we should only get here if a valid animation range has been set
        # 为此和所有子处理程序编写动画范围的通道数据
        # 注意：只有在设置了有效的动画范围后，我们才能到达此处
        try:
            if self.isStatic():
                curFrame = self.getStaticFrameNo()
                cmds.currentTime(curFrame)
                self.writeChannelDataForFrame(curFrame)
            else:
                for curFrame in range(self.startFrame, self.endFrame+1):
                    cmds.currentTime(curFrame)
                    self.writeChannelDataForFrame(curFrame)
        except Exception as e:
            cmds.error("Exception: %s (MayaSgxmlHandler.writeChannelData)" % e)

    def writeChannelDataForFrame(self, frameNumber):
        # recurse through each child handler writing the channel data for this frame
        # 通过每个子处理程序递归，为该帧写入通道数据
        for curChildHandler in self.childHandlers:
            curChildHandler.writeChannelDataForFrame(frameNumber)

        # copy the values for the animated values from maya to the sgxml channels
        # 将动画值的值从maya复制到sgxml通道
        for mayaPath, attrName, channelIndex, numChannels in self.mayaChannelData:
            vals = []
            #print("mayaPath = %s" % mayaPath)
            #print("attrName = %s" % attrName)
            if attrName is 'bounds':
                vals = getAnimBoundsData(mayaPath, frameNumber)
            elif attrName is 'xform':
                vals = cmds.xform(mayaPath, query=True,
                                  matrix=True, objectSpace=True)
            elif attrName is 'customBounds':
                sgxml_boundMinX = getAttrOrZero(mayaPath, 'sgxml_boundMinX')
                sgxml_boundMaxX = getAttrOrZero(mayaPath, 'sgxml_boundMaxX')
                sgxml_boundMinY = getAttrOrZero(mayaPath, 'sgxml_boundMinY')
                sgxml_boundMaxY = getAttrOrZero(mayaPath, 'sgxml_boundMaxY')
                sgxml_boundMinZ = getAttrOrZero(mayaPath, 'sgxml_boundMinZ')
                sgxml_boundMaxZ = getAttrOrZero(mayaPath, 'sgxml_boundMaxZ')

                addAnimBoundsData(mayaPath, frameNumber, [
                                  sgxml_boundMinX, sgxml_boundMaxX, sgxml_boundMinY, sgxml_boundMaxY, sgxml_boundMinZ, sgxml_boundMaxZ])
            else:
                if numChannels == 1:
                    vals = [cmds.getAttr(mayaPath + '.' + attrName)]
                else:
                    vals = cmds.getAttr(mayaPath + '.' + attrName)
            # note: vals can be none for bounds that are to be automatically calculated
            if vals is not None:
                for i, curVal in enumerate(vals):
                    fle = channelIndex + i
                    self.root.setChannelDataValue(channelIndex + i, curVal)

        # force any automatic calculation of bounds of parents based on children needed
        curBounds = self.root.calcBounds()

        # if this SgXML handler has a mayaParent, place the top level bounds data into
        # animBoundsData for use by the parent handler
        if self.mayaParent is not None:
            addAnimBoundsData(self.mayaParent, frameNumber, curBounds)

        # write out the XML file for the channel data
        if not self.isStatic():
            "Writing XML channel file..."
            self.root.writeXMLChannelFile(frameNumber)


def setSgxmlAttr(attrName, selection=None, value=None, attrType='bool'):
    if selection is None:
        selection = cmds.ls(selection=True)
    if selection is not None:
        for curItem in selection:
            # create the attribute if it doesn't already exist
            if not cmds.listAttr(curItem, st=[attrName]):
                if attrType is 'bool':
                    cmds.addAttr(curItem, ln=attrName, at='bool')
                elif attrType == 'float':
                    cmds.addAttr(curItem, ln=attrName, at='double')
                    cmds.setAttr(curItem + "." + attrName, keyable=True)
                elif attrType == 'string':
                    cmds.addAttr(curItem, ln=attrName, dt='string')
                else:
                    raise ValueError, 'unsupported attrType'

            # set the value of the attribute
            if value is not None:
                if attrType is None or attrType == 'float' or attrType == 'bool':
                    cmds.setAttr(curItem + "." + attrName, value)
                elif attrType == 'string':
                    cmds.setAttr(curItem + "." + attrName,
                                 value, type='string')
                else:
                    raise ValueError, 'unsupported attrType'


def setComponent(selection, filepath=None, refType='abc',
                 componentKeyword='component'):
    # create the attribute if it doesn't already exist
    # 如果属性不存在，则创建该属性
    setSgxmlAttr('sgxml_nodeType', selection, componentKeyword,
                 'string')
    if filepath is not None:
        setSgxmlAttr('sgxml_filepath', selection, filepath, 'string')

    setSgxmlAttr('sgxml_refType', selection, refType, 'string')


def setStaticComponent(selection, filepath=None, refType='abc'):
    setComponent(selection, filepath=None, refType='abc',
                 componentKeyword='staticComponent')


def setXMLReference(selection, filepath=None, groupType='assembly'):
    setSgxmlAttr('sgxml_nodeType', selection, 'xmlReference', 'string')
    setSgxmlAttr('sgxml_nodeGroupType', selection, groupType, 'string')
    if filepath is not None:
        setSgxmlAttr('sgxml_filepath', selection, filepath, 'string')


def setAssembly(selection):
    setSgxmlAttr('sgxml_nodeGroupType', selection, 'assembly', 'string')


def setReference(selection, filepath, refType='xml'):
    setSgxmlAttr('sgxml_nodeType', selection, 'reference', 'string')
    setSgxmlAttr('sgxml_filepath', selection, filepath, 'string')
    if refType is not None:
        setSgxmlAttr('sgxml_refType', selection, refType, 'string')


def setLodGroup(selection):
    setSgxmlAttr('sgxml_nodeType', selection, 'lodGroup', 'string')


def setIgnore(selection):
    setSgxmlAttr('sgxml_ignore', selection)


def setBoundsWriteMode(selection, value=True):
    setSgxmlAttr('sgxml_boundsWriteMode', selection, value, 'bool')


def enableCustomBounds(selection, value=True):
    setSgxmlAttr('sgxml_customBounds', selection, value, 'bool')


def setLodNode(selection, lodTag=None, lodWeight=None):
    if lodTag is not None:
        setSgxmlAttr('sgxml_lodTag', selection, lodTag, 'string')
    if lodWeight is not None:
        setSgxmlAttr('sgxml_lodWeight', selection, lodWeight, 'float')
    setSgxmlAttr('sgxml_nodeType', selection, 'lodNode', 'string')


def setProxy(selection, proxyFile, proxyName='viewer'):
    setSgxmlAttr('sgxml_proxyName', selection, proxyName, 'string')
    setSgxmlAttr('sgxml_proxyFile', selection, proxyFile, 'string')


def setArbAttr(selection, attrName, value, attrType='float'):
    setSgxmlAttr('arbAttr_' + attrName, selection, value, attrType)
