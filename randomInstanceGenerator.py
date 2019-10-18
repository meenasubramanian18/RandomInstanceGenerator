#random field generator with material application
import maya.cmds as cmds
import random
import functools

#function to create UI window
def createUI(windowTitle, pApplyCallback):
	windowID = 'winID'
	
	if cmds.window(windowID, exists = True):
		cmds.deleteUI(windowID)
		
	cmds.window(windowID, title=windowTitle,sizeable=False, resizeToFitChildren = True)

	cmds.rowColumnLayout(numberOfColumns = 4, columnWidth =[(1,120),(2,60),(3,60),(4,60)],columnOffset = [(1,'right',3)])
	
	#row 1
	cmds.text(label = 'Number of Instances:') #total number of flowers/objects that will be created

	totalInstances = cmds.intField(value=50)

	cmds.separator(h=10, style='none')
	cmds.separator(h=10, style='none')
	
	#row 2
	cmds.text(label = 'Materials:')
	
	inputMaterials = cmds.textField(text = "Purple,Blue,Green,Yellow,Orange,Pink")
	
	cmds.separator(h=10, style='none')
	cmds.separator(h=10, style='none')
	
	#row 3
	cmds.text(label = 'Field Size XYZ:')
	
	fieldX = cmds.intField(value=60)
	fieldY = cmds.intField(value=0)
	fieldZ = cmds.intField(value=60)
	
	#row 4
	cmds.text(label = 'Rotation Range X:')
	
	rotXmin = cmds.intField(value=-10)
	rotXmax = cmds.intField(value=10)
	
	cmds.separator(h=10, style='none')
	
	#row 5
	cmds.text(label = 'Rotation Range Y:')
	
	rotYmin = cmds.intField(value=0)
	rotYmax = cmds.intField(value=360)
	
	cmds.separator(h=10, style='none')
	
	#row 6
	cmds.text(label = 'Rotation Range Z:')
	
	rotZmin = cmds.intField(value=-10)
	rotZmax = cmds.intField(value=10)
	
	cmds.separator(h=10, style='none')
	
	#row 7
	cmds.text(label = 'Scale Range:')
	
	scaleMin = cmds.floatField(value=.7)
	scaleMax = cmds.floatField(value=1.3)
	
	cmds.separator(h=10, style='none')
	
	#row 8 - empty row
	cmds.separator(h=10, style='none')
	cmds.separator(h=10, style='none')
	cmds.separator(h=10, style='none')
	cmds.separator(h=10, style='none')
	
	#row 9 - buttons
	
	cmds.separator(h=10, style='none')
	cmds.separator(h=10, style='none')
	
	cmds.button(label = 'Apply', command = functools.partial(pApplyCallback, totalInstances, inputMaterials, fieldX, fieldY, fieldZ, rotXmin, rotXmax, rotYmin, rotYmax, rotZmin, rotZmax, scaleMin, scaleMax))
	
	def cancelCallback (*pArgs):
		if cmds.window(windowID, exists = True):
		    cmds.deleteUI(windowID)
	
	cmds.button( label = 'Cancel', command = cancelCallback)
		
	cmds.showWindow()
	
def applyCallback(ptotalInstances, pinputMaterials, pfieldX, pfieldY, pfieldZ, protXmin, protXmax, protYmin, protYmax, protZmin, protZmax, pscaleMin, pscaleMax,*pArgs):
	#print 'apply pressed'
	totalInstances = cmds.intField(ptotalInstances, query = True, value = True)
	inputMaterials = cmds.textField(pinputMaterials, query = True, text = True)
	fieldX = cmds.intField(pfieldX, query = True, value = True)
	fieldY = cmds.intField(pfieldY, query = True, value = True)
	fieldZ = cmds.intField(pfieldZ, query = True, value = True)
	rotXmin = cmds.intField(protXmin, query = True, value = True)
	rotXmax = cmds.intField(protXmax, query = True, value = True)
	rotYmin = cmds.intField(protYmin, query = True, value = True)
	rotYmax = cmds.intField(protYmax, query = True, value = True)
	rotZmin = cmds.intField(protZmin, query = True, value = True)
	rotZmax = cmds.intField(protZmax, query = True, value = True)
	scaleMin = cmds.floatField(pscaleMin, query = True, value = True)
	scaleMax = cmds.floatField(pscaleMax, query = True, value = True)
	
	randomGenerator(totalInstances, inputMaterials, fieldX,fieldY, fieldZ, rotXmin,rotXmax,rotYmin, rotYmax, rotZmin, rotZmax, scaleMin, scaleMax)
	
def randomGenerator(totalInstances, inputMaterials, fieldX,fieldY, fieldZ, rotXmin,rotXmax,rotYmin, rotYmax, rotZmin, rotZmax, scaleMin, scaleMax):

	random.seed(1218)

	selectedObjs = cmds.ls(orderedSelection = True)

	print 'result: %s' % (selectedObjs)

	objectName = selectedObjs[0]
	#calculate how many instances to make per object that was selected
	numObjs = len(selectedObjs)

	instancesPerObj = totalInstances/numObjs #totalInstances is an Input field, how many total flowers/objects do you want

	instanceGroupName = cmds.group(empty=True, name = 'randomFieldGenerator_GRP_#')

	#get the materials split up into individual strings, and get number of materials
	
	materialCount = inputMaterials.split(",", 4)
	numberOfMaterials = len(materialCount)
	
	fillstring = ",null,null,null,null,null,null"
	inputMaterials = inputMaterials + fillstring
	print 'mats: %s' % (inputMaterials)
	materials = inputMaterials.split(",", 5) #max of five materials, take the first five strings
	materials.pop(5) #actually takes 6 strings and deletes the last one so there's five proper strings
	print materials
	#numberOfMaterials = len(materials)
	
	'''for m in range(0,numberOfMaterials):
		x = 'SG'
		x.join(materials[m])'''
		
	for m in range(0,5):
		materials[m] = materials[m] + 'SG'
	
	print materials

	#go through each of the numObjs selected objects and create instancesPerObj # of instances
	
	for i in range(0,numObjs):
	   
		objectName = selectedObjs[i]
		ObjectGroupName = cmds.group(empty=True, name = objectName + '_GRP_#')
		for j in range(0,instancesPerObj):
		
			instanceResult = cmds.instance( objectName, name = objectName + '_instance#')
			
			cmds.parent(instanceResult, ObjectGroupName)
			#cmds.parent(instanceResult, instanceGroupName)
			
			#print 'instanceResult: ' + str(instanceResult)
			
			x = random.uniform(-1 * fieldX/2,fieldX/2)
			y = random.uniform(-1 * fieldY/2,fieldY/2)
			z = random.uniform(-1 * fieldZ/2,fieldZ/2)
			
			cmds.move(x,y,z, instanceResult) #only place them randomly on xz plane (not y bc should be flat on "water" plane)
			
			xr = random.uniform(rotXmin,rotXmax)
			yr = random.uniform(rotYmin,rotYmax)
			zr = random.uniform(rotZmin,rotZmax)
			
			cmds.rotate(xr,yr,zr, instanceResult)
			
			scaleFactor = random.uniform(scaleMin,scaleMax) #make them slightly different in size
			
			cmds.scale(scaleFactor,scaleFactor,scaleFactor,instanceResult) 
		
			matNumber = random.uniform(0,numberOfMaterials) #NEED A MAX NUMBER OF MATERIALS so you don't have a million if else statements, let's do five 

			if matNumber >= 0 and matNumber <1:
				cmds.sets( e=True, forceElement= materials[0] )
			elif matNumber >= 1 and matNumber < 2:
				cmds.sets( e=True, forceElement= materials[1] )
			elif matNumber >= 2 and matNumber < 3:
				cmds.sets( e=True, forceElement= materials[2] )
			elif matNumber >= 3 and matNumber < 4:
				cmds.sets( e=True, forceElement= materials[3] )
			else:
				cmds.sets( e=True, forceElement= materials[4] )
		
		cmds.parent(ObjectGroupName, instanceGroupName)	
		cmds.hide(objectName)

	#cmds.parent(instanceGroupName, leader) #parent all instanced objects to leader

	cmds.xform(instanceGroupName, centerPivots=True )
	#cmds.xform(leader, centerPivots=True )
	#mc.sets( e=True, forceElement= myBlinn + 'SG' )	

createUI('Field Generator', applyCallback)