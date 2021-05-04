import maya.cmds as mc
import sys
sys.path.append(r'C:\Users\red_w\Documents\maya\scripts\MacSturrup')
import FKCtrlCreator
import IkFkSwitch
import SpineRigCreator
import armRigCreator
import legRigCreator
import headRigCreator
import MSCurves
import stretchy


class AutoRigMS:

        def __init__(self, name):
                self.name = name
                self.arm = []
        def setArm(self, arm):
                self.arm.append(arm)
        def getArm(self, ite):
                return self.arm[ite] 
       
        
        def ArmRigProc(self):
                siz = mc.floatFieldGrp(IKSizeField, query=True, value=True )[0]
                shp = mc.optionMenu('Shape1Menu', q=1, v=1)
                col = mc.colorIndexSliderGrp("IKcontrolColor", q= 1, v= 1)
                armRigCreator.createArmIK(siz, shp, col)
                
        def LegRigProc(self):
                siz = mc.floatFieldGrp(IKSizeField, query=True, value=True )[0]
                shp = mc.optionMenu('Shape1Menu', q=1, v=1)
                col = mc.colorIndexSliderGrp("IKcontrolColor", q= 1, v= 1)     
                legRigCreator.createLegIK(siz, shp, col) 
        def NeckRigProc(self, kin):
                siz = mc.floatFieldGrp(IKSizeField, query=True, value=True )[0]
                shp = mc.optionMenu('Shape1Menu', q=1, v=1)
                col = mc.colorIndexSliderGrp("IKcontrolColor", q= 1, v= 1)
                if kin == "IK":
                        headRigCreator.NeckIKCreator(siz ,shp, col )
                if kin == "FK":
                        headRigCreator.FKNeckControlCreator(siz ,col) 
        def SpineRigProc(self,kin):
                siz = mc.floatFieldGrp(IKSizeField, query=True, value=True )[0]
                shp = mc.optionMenu('Shape1Menu', q=1, v=1)
                col = mc.colorIndexSliderGrp("IKcontrolColor", q= 1, v= 1)
                if kin =="IK":
                        SpineRigCreator.SplineIKCreator(siz ,shp, col )
                if kin =="FK":
                        SpineRigCreator.FKSpineControlCreator(siz ,col )

        def handRigProc(self):
                siz = mc.floatFieldGrp(IKSizeField, query=True, value=True )[0]
                shp = mc.optionMenu('Shape1Menu', q=1, v=1)
                col = mc.colorIndexSliderGrp("IKcontrolColor", q= 1, v= 1)
                armRigCreator.HandIK(siz, shp, col)
        def footRigProc(self):
                siz = mc.floatFieldGrp(IKSizeField, query=True, value=True )[0]
                shp = mc.optionMenu('Shape1Menu', q=1, v=1)
                col = mc.colorIndexSliderGrp("IKcontrolColor", q= 1, v= 1)
        def ShoulderRigProc(self):
                siz = mc.floatFieldGrp(IKSizeField, query=True, value=True )[0]
                shp = mc.optionMenu('Shape1Menu', q=1, v=1)
                col = mc.colorIndexSliderGrp("IKcontrolColor", q= 1, v= 1)
                armRigCreator.ShoulderIK(siz, shp, col)
CharRig = AutoRigMS("thisCharacter")
# CharRig.reloadScripts()
if mc.window("Jams Auto Rig",q=1, ex=True):
        mc.deleteUI("Jams Auto Rig")
# Import the Maya commands library
# Create a window using the cmds.window command
# give it a title, icon and dimensions
window = mc.window("Jams Auto Rig", title="Jams Auto Rig", iconName='Short Name', widthHeight=(320, 100) )
# As we add contents to the window, align them vertically
#mc.columnLayout( adjustableColumn=True )
mc.columnLayout ("SpineIKColumn")
mc.iconTextStaticLabel( st='textOnly',bgc=(0.1,0.1,0.1), l='Select the root of the Spine' )


siz =0.5
IKSizeField = mc.floatFieldGrp( numberOfFields=1, label='IK Control Scale', value=(0.5,0,0,0))
shapeType =  ''
mc.optionMenu("Shape1Menu", label='Shape')
mc.menuItem( label='circle' )
mc.menuItem( label= 'cube')
mc.menuItem( label='square' )
mc.menuItem( label='gear' )
mc.menuItem( label='pyramid' )
mc.menuItem( label='Arrow' )
mc.menuItem( label='Cross' )
mc.menuItem( label='sphere' )

IKCol = mc.colorIndexSliderGrp("IKcontrolColor",
        cw2 = (80, 40), 
        label ="Control Color",
        min = 0,
        max = 31, 
        value =5)

#############
mc.rowColumnLayout(nc=2, adj=1, p = window)
mc.button ( "createSpineIKButton",
        label = "Make Spine IK",
        command = "CharRig.SpineRigProc('IK')")
#button( label='Make Spine IK', command=("SplineIKCreator(MakeChange(siz, IKSizeField))"))
mc.button ( "createNeckIKButton",
        label = "Make Neck IK",
        command = "CharRig.NeckRigProc('IK')")
#mc.rowColumnLayout(nc=1,adj=True)

#button( label='Make Spine IK', command=("SplineIKCreator(MakeChange(siz, IKSizeField))"))

mc.columnLayout("SpineIKColumn", p = window)
mc.iconTextStaticLabel( st='textOnly', bgc=(0.1,0.1,0.1),l='Select 4 spine joints' )
mc.columnLayout ("FKSpineColumn")
FKSizeField = mc.floatFieldGrp( numberOfFields=1, label='FK Control Scale', value=(0.5,0,0,0), cc= 'MakeChange(siz, FKSizeField)')

mc.rowColumnLayout(nc=2, adj=1, p = window)
mc.button ( "createSpineFKButton",
        label = "Make SpineFK",
        command = "CharRig.SpineRigProc('FK')")
#mc.button( label='Make Spine FK', command=('FKSpineControlCreator(MakeChange(siz, FKSizeField))') )
mc.button ( "createneckfkbutton",
        label = "make neckfk",
        command = "CharRig.NeckRigProc('FK')")

mc.columnLayout("LegIKColumn",adj=True, p = window)
mc.iconTextStaticLabel( st='textOnly', bgc=(0.1,0.1,0.1), l='head Space' )

mc.button ( "createheadSpace",
        label = "make neck Space",
        command = "CharRig.headRigCreator.spaceSwitching()")
mc.iconTextStaticLabel( st='textOnly', bgc=(0.1,0.1,0.1), l='Leg / Arm IK' )
mc.rowColumnLayout(nc=4,  p = window)
mc.button ( "leg",
        label = "Leg",
        command = "CharRig.LegRigProc()")
mc.button ( "foot",
        label = "foot",
        command = "legRigCreator.makeRevFoot()")

mc.button ( "arm",
        label = "Arm",
        command = "CharRig.ArmRigProc()")
mc.button ( "hand",
        label = "Hand",
        command = "CharRig.handRigProc()")
mc.button ( "shoulder",
        label = "shoudler",
        command = "CharRig.ShoulderRigProc()")
mc.columnLayout("FKGeneralColumn", p = window)
mc.iconTextStaticLabel( st='textOnly', bgc=(0.1,0.1,0.1), l='Select the FK joints' )


mc.columnLayout ("makeFKColumn", adj = True)

controlSize = mc.floatSliderGrp("controlSize",
        label = "Control Size",
        field = True, 
        cw3 = (80,40, 150), 
        minValue = .01, 
        maxValue= 50,
        fieldMinValue = .1,
        fieldMaxValue = 50,
        value = 2)
        
controlColor = mc.colorIndexSliderGrp("controlColor",
        cw2 = (80, 40), 
        label ="Control Color",
        min = 0,
        max = 31, 
        value =5)
        
controlName = mc.textFieldGrp("controlName",
        cw2 = (80,200),
        label= "Control Suffix",
        text = "_CTRL")

mc.button ( "createFKButton",
        label = "CREATE CONTROL",
        command = "FKCtrlCreator.makeFKMS(controlSize, controlColor)")

mc.button ( "BlendFK",
        label = "BLEND FK",
        command = "IkFkSwitch.jointBlend()")




# Close button with a command to delete the UI
mc.button( label='Close', command=('cmds.deleteUI(\"' + window + '\", window=True)') )
# Set its parent to the Maya window (denoted by '..')
mc.setParent( '..' )
# Show the window that we created (window)
mc.showWindow( window )
#FKControlCreator()
def close():
        del CharRig
        mc.deleteUI("window", window = True)
    