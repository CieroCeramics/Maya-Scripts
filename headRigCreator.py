import maya.cmds as mc
import sys
sys.path.append(r'C:/Users/red_w/Documents/maya/scripts/MacSturrup/')
import MSCurves


def MakeChange(val, field):
    val= mc.floatFieldGrp(field, query=True, value=True)[0]
    return val
def NeckIKCreator(ctrlScale, cType, col):
    mc.select(hi=True)
    neckJts= mc.ls(sl=True)
  #  num = 0



    mc.select(clear=True)
    root= neckJts[0]
   

    rootCoords = mc.xform(root, ws=True,q=True, t=True)
    neckBaseCtrlJt=mc.joint(p=rootCoords, n=root+"BaseCtrlJoint")
    mc.select(clear=True)
    
    end = neckJts[len(neckJts)-1]
    endCoords = mc.xform(end, ws=True,q=True, t=True)
    neckEndCtrlJt=mc.joint(p=endCoords, n=root+"EndCtrlJoint")
    

    mc.select(clear=True)
    
    headctrlCurve = MSCurves.getCurve(cType, root+"CtrlCurve")
 
    mc.setAttr (root+"CtrlCurve"+ ".overrideEnabled", 1)
    mc.setAttr (root+"CtrlCurve"+ ".overrideColor", col)
    mc.select(clear = True)
    #mc.rename(headctrlCurve, root+"CtrlCurve")
    mc.select(headctrlCurve)
    mc.CenterPivot
    mc.xform(cpc=True)
    mc.scale(ctrlScale,ctrlScale,ctrlScale)

    mc.select(end, add=True)
    mc.matchTransform(pos=True)
    mc.makeIdentity(a=True, s=True, t=True)


### make spline solver
    mc.select(root)
    mc.select(end,add=True)
    neckIK=mc.ikHandle (sol="ikSplineSolver", scv=False, ns=3, n=root+"IKHandle")
    
    mc.select(neckBaseCtrlJt, neckEndCtrlJt) 
    mc.select(neckIK[2], add=True)
    mc.skinCluster(bm=0, sm=0, nw=1, mi=2, dr=3)
   
    mc.select(clear=True)

    mc.parentConstraint(headctrlCurve,neckEndCtrlJt, mo=0)

    mc.rename(neckIK[2] ,root+'neckCurve')
    mc.setAttr(root+"IKHandle.dTwistControlEnable", 1)
    mc.setAttr (root+"IKHandle.dWorldUpType", 4)
    mc.connectAttr(root+'BaseCtrlJoint.xformMatrix', root+'IKHandle.dWorldUpMatrix', f=True)
    mc.connectAttr(root+'EndCtrlJoint.xformMatrix', root+'IKHandle.dWorldUpMatrixEnd', f=True)
    mc.setAttr (root+"IKHandle.dWorldUpType", 4)
    mc.setAttr (root+"IKHandle.dWorldUpVectorY", 0)
    mc.setAttr (root+"IKHandle.dWorldUpVectorEndY", 0)
    mc.setAttr (root+"IKHandle.dWorldUpVectorZ", -1)
    mc.setAttr (root+"IKHandle.dWorldUpVectorEndZ", -1)
    mc.setAttr (root+"IKHandle.dWorldUpAxis", 1)

    mc.select(cl=True)
    mc.select(root+'neckCurveShape')
    necklen=mc.arclen(ch=True)
    mc.rename(necklen, root+"neckInfo")
    neckStretchDiv=mc.shadingNode("multiplyDivide",au=True,n=root+"neckStretchDiv")

    mc.setAttr(root+"neckStretchDiv.operation",2)
    mc.connectAttr (root+"neckInfo.arcLength", root+"neckStretchDiv.input1X", f=True)
    arlen= mc.getAttr(root+'neckInfo.arcLength')
    mc.setAttr(root+"neckStretchDiv.input2X", float(arlen))
    i=0
    for jts in neckJts:
        if i < len(neckJts)-1:
            mc.connectAttr(root+"neckStretchDiv.outputX", jts+".scaleX")
        i+=1
    #mc.parentConstraint()


def FKNeckControlCreator(ctrlScale, col):
    FKNeckJts = mc.ls(sl=True, typ= "joint")
    root = FKNeckJts[0]
    mc.select(root, hi=True)
    otherJts = mc.ls(sl=True, typ="joint")
    end= otherJts[len(otherJts)-1]
    Coord1 = mc.xform(root, ws= True, q=True, t=True)
    Coord2 = mc.xform(end, ws= True, q=True, t=True)
    
    rootjointname = root+"FKJoint"
    rootctrlname = root+"FKCtrl"
    endjointname = end +"FKJoint"
    rootctrlname = end+"FKCtr"
    mc.select(cl=True)
    neckBaseJoint = mc.joint(p=Coord1, n= rootjointname)
    mc.joint(e=1, oj='xyz', sao='xup', ch=1, zso = 1)
    neckEndJoint = mc.joint(p=Coord2, n = endjointname)
    mc.joint(e=1, oj='xyz', sao='xup', ch=1, zso=1)
    circ = mc.circle(c= [0,0,0], nr= [0,1,0], sw=360, r=ctrlScale, d= 3, ut =0, tol= 0.01, s=8, ch= 1, n=rootctrlname)
    circshp=mc.pickWalk (d="down")
    #mc.select(rootctrlname,r=True)
    mc.setAttr (circshp[0]+ ".overrideEnabled", 1)
    mc.setAttr (circshp[0]+ ".overrideColor", col)
    mc.select(rootctrlname+"Shape",r=True)
    mc.select(root+"FKJoint", add=True)
    mc.parent(r=True, s=True)
    mc.select (root + "CtrlCurve")
    headGrp = mc.group(root+"CtrlCurve", n="headNeckGroup")
    mc.parentConstraint(end+"FKJoint", headGrp) 
    
    
    

def spaceSwitching():
    root=mc.ls(sl=True)[0]
    shoulderCtrlJt= mc.ls(sl=True)[1]
    mc.spaceLocator(n="neckShoulderConstLoc")
    mc.select(root, add=True)
    mc.matchTransform(pos=1)
   
    mc.select(cl=True)
    mc.parent("neckShoulderConstLoc", shoulderCtrlJt)
    mc.select(root+"FKJoint")
    mc.group(n="neckFKGrp")
    mc.select(cl=True)
    #mc.select (root+"BaseCtrlJoint", add=True)
    #mc.select("neckShoulderConstLoc", add=True)
    mc.parentConstraint("neckShoulderConstLoc", root+"BaseCtrlJoint", mo=1)
    mc.parentConstraint("neckShoulderConstLoc", "neckFKGrp", mo=1)
    mc.select(cl=1)
    mc.select(root+"CtrlCurve")
    mc.addAttr(sn="headspace", ln="head_space", at="enum", en="Neck:Shoulders:root", h=0)

