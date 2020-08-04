# Copyright (c) 2012 The Foundry Visionmongers Ltd. All Rights Reserved.

"""
simple_sgxml.py
Simple example script using scenegraphXML.py
"""

import os
import tempfile

import scenegraphXML as sgxml

# declare the ScenegraphRoot
root = sgxml.ScenegraphRoot()

# declare elements for the hierarchy
group1 = sgxml.Group(name="group1")
group1.setBounds(value=[-1.0,1.0,-1.0,1.0,-1.0,2.0])
group1.setXform(value=[1,0,0,0,0,1,0,0,0,0,1,0,0,0,0,1])

group2 = sgxml.Group(name="group2")
group2.setXform(value=[1,0,0,0,0,1,0,0,0,0,1,0,1,2,3,1])

xmlref1 = sgxml.Reference(name='xmlref1', refFile=os.path.join(tempfile.gettempdir(), 'subscene1.xml'))

xmlref2 = sgxml.Reference(name='xmlref2', refFile=os.path.join(tempfile.gettempdir(), 'subscene2.xml'))
xmlref2.setXform(value=[1,0,0,0,0,1,0,0,0,0,1,0,10,20,30,1])

georef1 = sgxml.Reference(name='georef1', refType='abc', refFile='pony.abc')
georef1.setXform(value=[1,0,0,0,0,1,0,0,0,0,1,0,100,200,300,1])

georef2 = sgxml.Reference(name='georef2', refType='abc', refFile='primitives.abc')

# connect up the hierarchy
root.setInstanceList([group1, group2])
group1.setInstanceList([xmlref1, xmlref2])
group2.setInstanceList([georef1, georef2])

# write out the hierarchy
root.writeXMLFile(os.path.join(tempfile.gettempdir(), 'simpleSgXML.xml'))
