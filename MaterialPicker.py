import maya.cmds as mc
from pymel.core import *
from pymel.core.datatypes import *
import maya.OpenMaya as om
import maya.OpenMayaUI as omui
import pymel.core as pm
import maya.mel as mel


#---------------------------------------------

class picker():
	ctx = cmds.currentCtx()
	ctxInfo = cmds.contextInfo(ctx,c=1)
	
	
	def __init__(self):
		pass
	
	def pickerContext(self, *args):
		maya3DViewHandle = omui.M3dView()
		activeView = maya3DViewHandle.active3dView()
		self.Context = 'Context'
		self.meshSelection = cmds.ls(g=1)
		if cmds.draggerContext( self.Context, ex=1 ):
			cmds.deleteUI( self.Context )
		cmds.draggerContext( self.Context, name=self.Context, pressCommand=self.onPress, releaseCommand=self.onRelease, cursor='crossHair' )
		cmds.setToolTo( self.Context)	

#---------------------------------------------

	def onPress(self,*args):
		self.Context = 'Context'
		vpX, vpY, _ = cmds.draggerContext(self.Context, query=True, anchorPoint=True)

		pos = om.MPoint()
		dir = om.MVector()
		hitpoint = om.MFloatPoint()
		omui.M3dView().active3dView().viewToWorld(int(vpX), int(vpY), pos, dir)
		pos2 = om.MFloatPoint(pos.x, pos.y, pos.z)
		for mesh in cmds.ls(type='mesh'):
			selectionList = om.MSelectionList()
			selectionList.add(mesh)
			dagPath = om.MDagPath()
			selectionList.getDagPath(0, dagPath)
			fnMesh = om.MFnMesh(dagPath)
			intersection = fnMesh.closestIntersection(
			om.MFloatPoint(pos2),om.MFloatVector(dir),None,None,False,om.MSpace.kWorld,99999,False,None,hitpoint,None,None,None,None,None)
			if intersection:
				picked = (fnMesh.name())
				print picked
				connections = cmds.listConnections(picked, s=False, d=True, t="shadingEngine")
				result = list()
				for connection in connections :
				    shaders = cmds.listConnections(connection+".surfaceShader", s=True, d=False)
				    for shader in shaders :
				        result.append(shader)
				cmds.select(result)
				cmds.HypershadeWindow()
				mel.eval('hyperShadePanelGraphCommand("hyperShadePanel1", "showUpAndDownstream");')

#---------------------------------------------

	def onRelease(self):
		if(self.ctxInfo=='manipMove'):
			cmds.setToolTo('moveSuperContext')
		elif(self.ctxInfo=='manipRotate'):
			cmds.setToolTo('RotateSuperContext')
		elif(self.ctxInfo=='manipScale'):
			cmds.setToolTo('scaleSuperContext')
		elif(self.ctxInfo=='selectTool'):
			cmds.setToolTo('selectSuperContext')		

#---------------------------------------------		

picker().pickerContext()
