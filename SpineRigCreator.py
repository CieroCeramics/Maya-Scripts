import maya.cmds as mc
def MakeChange(val, field):
    val= mc.floatFieldGrp(field, query=True, value=True)[0]
    return val
def SplineIKCreator(ctrlScale):
    mc.select(hi=True)
    SpineJts= mc.ls(sl=True)

    mc.select(clear=True)
    root= SpineJts[0]
   
    rootCoords = mc.xform(root, ws=True,q=True, t=True)
    HipCtrlJt=mc.joint(p=rootCoords, n="HipCtrlJoint")
    mc.select(clear=True)
    
    end = SpineJts[len(SpineJts)-1]
    endCoords = mc.xform(end, ws=True,q=True, t=True)
    ShoulderCtrlJt=mc.joint(p=endCoords, n="ShoulderCtrlJoint")
    
    mc.select(clear=True)
    ShoulderCtrlCurve = mc.curve(n="ShoulderCtrl", p=[[-2.103, 5.022, -2.864], [-2.617, 7.232, -3.451], [2.617, 7.232, -3.451], [2.617, 7.232, 2.05], [-2.617, 7.232, 2.05], [-2.617, 7.232, -3.451], [-2.617, 7.232, 2.05], [-2.103, 5.022, 1.477], [-2.103, 5.022, -2.864],[-2.103, 5.022, 1.477], [2.103, 5.022, 1.477], [2.617, 7.232, 2.05], [2.103, 5.022, 1.477], [2.103, 5.022, -2.864], [2.617, 7.232, -3.451], [2.103, 5.022, -2.864], [-2.103, 5.022, -2.864], [-2.617, 7.232, -3.451]], d=1)
    mc.select(ShoulderCtrlCurve)
    mc.CenterPivot
    mc.xform(cpc=True)
    mc.scale(ctrlScale,ctrlScale,ctrlScale)
   
    mc.select(end, add=True)
    mc.matchTransform(pos=True)
    mc.makeIdentity(a=True, s=True, t=True)
    mc.select(ShoulderCtrlCurve, r=True)
    HipCtrlCurve = mc.duplicate(n="HipCtrl")
    mc.scale(1,-1,1)
    mc.select(root, add=True)
    mc.matchTransform(pos=True)
    mc.makeIdentity(a=True, s=True, t=True)

    mc.select(clear=True)
    mc.select(root)
    mc.joint(e=True, oj="xzy", sao="xup", ch=True, zso=True)
    mc.select(root)
    
    mc.select(end,add=True)
    spineIK=mc.ikHandle (sol="ikSplineSolver", scv=False, ns=3, n="spineIKHandle")
    

    mc.select(clear=True)
    mc.select(HipCtrlJt, ShoulderCtrlJt) 
    mc.select(spineIK[2], add=True)
    mc.skinCluster(bm=0, sm=0, nw=1, mi=2, dr=3)
    mc.rename(spineIK[2] ,'SpineCurve')
    mc.select(clear=True)

    mc.parentConstraint(HipCtrlCurve, HipCtrlJt,mo=0)
    mc.parentConstraint(ShoulderCtrlCurve, ShoulderCtrlJt,mo=0)
    
    mc.setAttr("spineIKHandle.dTwistControlEnable", 1)
    mc.setAttr ("spineIKHandle.dWorldUpType", 4)
    mc.connectAttr('HipCtrlJoint.xformMatrix', 'spineIKHandle.dWorldUpMatrix', f=True)
    mc.connectAttr('ShoulderCtrlJoint.xformMatrix', 'spineIKHandle.dWorldUpMatrixEnd', f=True)
    mc.setAttr ("spineIKHandle.dWorldUpType", 4)
    mc.setAttr ("spineIKHandle.dWorldUpVectorY", 0)
    mc.setAttr ("spineIKHandle.dWorldUpVectorEndY", 0)
    mc.setAttr ("spineIKHandle.dWorldUpVectorZ", -1)
    mc.setAttr ("spineIKHandle.dWorldUpVectorEndZ", -1)
    mc.setAttr ("spineIKHandle.dWorldUpAxis", 1)

    mc.select(cl=True)
    mc.select('SpineCurveShape')
    spinelen=mc.arclen(ch=True)
    mc.rename(spinelen, "spineInfo")
    SpineStretchDiv=mc.shadingNode("multiplyDivide",au=True,n="spineStretchDiv")
    mc.setAttr("spineStretchDiv.operation",2)
    mc.connectAttr ("spineInfo.arcLength", "spineStretchDiv.input1X", f=True)
    arlen= mc.getAttr('spineInfo.arcLength')
    mc.setAttr("spineStretchDiv.input2X", float(arlen))
    i=0
    for jts in SpineJts:
        if i < len(SpineJts)-1:
            mc.connectAttr("spineStretchDiv.outputX", jts+".scaleX")
        i+=1
    #mc.parentConstraint()
def FKSpineControlCreator(ctrlScale):
    i=0
    FKSpineJts = mc.ls(sl=True)
    mc.select(clear=True)
    for jts in FKSpineJts:
        Coords = mc.xform(jts, ws=True,q=True, t=True)
        jointname = "SpineFKJoint{}"
        ctrlname= "SpineFkCtrl{}"
        
  #      circle -c 0 0 0 -nr 0 1 0 -sw 360 -r 1 -d 3 -ut 0 -tol 0.01 -s 8 -ch 1;
        if(i>0):
            mc.select(jointname.format(i-1))
        jt = mc.joint(p=Coords, n=jointname.format(i))
        mc.joint(e=True, oj="xzy", sao="xup", ch=True, zso=True)
        if(i>0 and i<3):
            circ = mc.circle(c= [0,0,0], nr= [0,1,0], sw=360, r=ctrlScale, d= 3, ut =0, tol= 0.01, s=8, ch= 1, n=ctrlname.format(i))
            mc.select(ctrlname.format(i)+"Shape",r=True)
            mc.select(jt, add=True)
            mc.parent(r=True, s=True)
        i+=1
    mc.select("SpineFKJoint0")
    #mc.joint(e=True, oj="xzy", sao="xup", ch=True, zso=True)
    hipFKConstGrp = mc.group('HipCtrl', n='HipFKConstGroup')
    shldrFkConstGrp= mc.group('ShoulderCtrl', n='ShoulderFKConstGroup')
    mc.parentConstraint("SpineFKJoint0", hipFKConstGrp, mo=True)
    
    mc.parentConstraint("SpineFKJoint3", shldrFkConstGrp, mo=True)



# Import the Maya commands library
# Create a window using the cmds.window command
# give it a title, icon and dimensions
window = mc.window( title="Spine Control Creation", iconName='Short Name', widthHeight=(320, 100) )
# As we add contents to the window, align them vertically
#mc.columnLayout( adjustableColumn=True )
mc.columnLayout()
mc.iconTextStaticLabel( st='textOnly', l='Select the root of the Spine' )
mc.rowColumnLayout(numberOfColumns=1)

siz =0.5
IKSizeField = mc.floatFieldGrp( numberOfFields=1, label='IK Control Scale', value=(0.5,0,0,0))


mc.button( label='Make Spine IK', command=("SplineIKCreator(MakeChange(siz, IKSizeField))"))

mc.columnLayout()
mc.iconTextStaticLabel( st='textOnly', l='Select 4 spine joints' )
mc.rowColumnLayout(numberOfColumns=1)
FKSizeField = mc.floatFieldGrp( numberOfFields=1, label='FK Control Scale', value=(0.5,0,0,0), cc= 'MakeChange(siz, FKSizeField)')

mc.button( label='Make Spine FK', command=('FKControlCreator(MakeChange(siz, FKSizeField))') )
# Close button with a command to delete the UI
mc.button( label='Close', command=('cmds.deleteUI(\"' + window + '\", window=True)') )
# Set its parent to the Maya window (denoted by '..')
mc.setParent( '..' )
# Show the window that we created (window)
mc.showWindow( window )
#FKControlCreator()
