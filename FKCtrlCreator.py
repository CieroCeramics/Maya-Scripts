import maya.cmds as mc
import sys
def makeFKMS(ControlSize, color):
    #sets up fk controls to a joint
    
    selection = mc.ls(sl=True)
    size = len(selection)

    if ( size ==0):
        mc.error ("please select one or more objects")
    #controlSize = mc.floatSliderGrp("controlSize")

    ControlSize =  mc.floatSliderGrp ("controlSize", q = True, v = True)
   # color = mc.colorIndexSliderGrp("controlColor")
    color = mc.colorIndexSliderGrp ("controlColor", q=True, v=True )
    color = color - 1

    controlStuff = mc.textFieldGrp("controlName", q = True, text = True)

    for a in range (size):
        if mc.objExists(selection[0]+controlStuff)==1:
            mc.error("please enter a unique suffix")
    if controlStuff == "":
        mc.error ("Please enter a suffix. ")
    i=0
    for b in range (size):

        circle1 = mc.circle(nr=(1,0,0), ch=0)
        circleShape1 = mc.pickWalk (d="down")

        mc.setAttr (circleShape1[0] + ".overrideEnabled", 1)
        mc.setAttr (circleShape1[0] + ".overrideColor", color)
        sizename = selection[b]+"{}"
        mc.rename (circle1[0], selection[b]+controlStuff)
        mc.select (selection[b] + controlStuff)
        mc.scale  (ControlSize,ControlSize, ControlSize, r=True)
        mc.makeIdentity(apply=True, t=1, r=1, s=1, n=0)
        
        mc.group(em=True, n=selection[b] +"_offset")
        tempConstraint = mc.orientConstraint(selection[b], selection[b]+"_offset")
        mc.delete(tempConstraint)
        tempConstraint= mc.pointConstraint(selection[b], selection[b]+"_offset")
        mc.delete (tempConstraint)

        mc.parent(selection[b]+controlStuff, selection[b]+"_offset")

        if b>=1:
            mc.parent (selection[b]+"_offset", selection[b-1]+controlStuff)

        mc.setAttr(selection[b]+controlStuff+".tx", 0)
        mc.setAttr(selection[b]+controlStuff+".ty", 0)
        mc.setAttr(selection[b]+controlStuff+".tz", 0)

        mc.setAttr(selection[b]+controlStuff+".rx", 0)
        mc.setAttr(selection[b]+controlStuff+".ry", 0)
        mc.setAttr(selection[b]+controlStuff+".rz", 0)

        mc.orientConstraint (selection[b]+controlStuff, selection[b], mo=True)
        mc.pointConstraint (selection[b]+controlStuff, selection[b], mo=True)
        
        selectionParent = "noParent"
        i=i+1
    j = 0;
    for c in range(size):
            parent = mc.listRelatives (selection[c], parent = True)
            if parent != None:
                if len(parent)>0 :
                    parentCheck = parent[0]
                    check = any(parentCheck in s for s in selection)
                   # check = mc.stringArrayIntersector(parentCheck, selection )
                    if check ==0:
                        selectionParent = parentCheck

                
            
    if selectionParent != "noParent":
        mc.parentConstraint (selectionParent, selection[0]+"_offset", mo=True)

def createFKControls():
    if mc.window("makeFKWindow", ex = True):
        mc.deleteUI("makeFKWindow")
    
    sel = mc.ls(sl=True)

    if len(sel)>= 1:
        
        text = sel[0];

        mc.window ("makeFKWindow", title= "Create FK Controls")
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

        originalSelection = mc.ls(sl = True)

        mc.select(originalSelection, r=True)

        mc.showWindow("makeFKWindow")
        mc.window("makeFKWindow", edit = True, wh=(310 ,90))

        if len(sel)>=1:
            mc.textFieldGrp("controlName", e = True, text="_CTRL", editable = True )
            
            
#createFKControls()