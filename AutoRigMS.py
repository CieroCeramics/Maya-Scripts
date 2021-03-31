import maya.cmds as mc
import sys
sys.path.append(r'C:/Users/red_w/Documents/maya/scripts/MacSturrup')
import FKCtrlCreator
import IkFkSwitch
reload(IkFkSwitch)


# Import the Maya commands library
# Create a window using the cmds.window command
# give it a title, icon and dimensions
window = mc.window( title="Spine Control Creation", iconName='Short Name', widthHeight=(320, 100) )
# As we add contents to the window, align them vertically
#mc.columnLayout( adjustableColumn=True )
mc.columnLayout ("SpineIKColumn", adj = True)
mc.iconTextStaticLabel( st='textOnly', l='Select the root of the Spine' )


siz =0.5
IKSizeField = mc.floatFieldGrp( numberOfFields=1, label='IK Control Scale', value=(0.5,0,0,0))

mc.button ( "createSpineIKButton",
        label = "Make Spine IK",
        command = "SplineIKCreator(MakeChange(siz, IKSizeField))")
#button( label='Make Spine IK', command=("SplineIKCreator(MakeChange(siz, IKSizeField))"))


mc.iconTextStaticLabel( st='textOnly', l='Select 4 spine joints' )
mc.columnLayout ("FKSpineColumn", adj = True)
FKSizeField = mc.floatFieldGrp( numberOfFields=1, label='FK Control Scale', value=(0.5,0,0,0), cc= 'MakeChange(siz, FKSizeField)')


mc.button ( "createSpineFKButton",
        label = "Make SpineFK",
        command = "FKSpineControlCreator(MakeChange(siz, FKSizeField))")
#mc.button( label='Make Spine FK', command=('FKSpineControlCreator(MakeChange(siz, FKSizeField))') )


mc.columnLayout()
mc.iconTextStaticLabel( st='textOnly', l='Select the FK joints' )
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
        command = "makeFKMS(controlSize, controlColor)")

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
