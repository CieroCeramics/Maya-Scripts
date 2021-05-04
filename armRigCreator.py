import maya.cmds as mc
import sys
sys.path.append(r'C:/Users/red_w/Documents/maya/scripts/MacSturrup/')
import stretchy
import MSCurves

import AutoRigMS
def createArmIK(col, shp, siz):
    shoulder = mc.ls(sl=True)[0]
    AutoRigMS.CharRig.setArm(shoulder)
    hand = mc.ls(sl=True)[1]
    elbow= mc.ls(sl=True)[2]
    mc.select(cl=True)
    mc.select(shoulder, hi=True)
    armJts=mc.ls(sl=True)
    for jts in armJts:
        mc.select(jts, r=True)
        mc.joint(e=True, oj="xzy", sao="xup", ch=True, zso=True)
    mc.select(shoulder)
    IKArmJts=mc.duplicate(shoulder, n=shoulder+"_IK", rc=True)
    for i, jt in enumerate (IKArmJts):
        mc.rename(jt, armJts[i]+"_IK" )
    ArmIK = mc.ikHandle(sol="ikRPsolver", sj=shoulder+"_IK", ee=hand+"_IK", n=hand+"_IKHandle")
    ArmCtrl =MSCurves.getCurve(shp,hand+"_IK_CTRL" ) 
    # mc.circle(c= [0,0,0], nr= [0,1,0], sw=360, r=2, d= 3, ut =0, tol= 0.01, s=8, ch= 1, n=hand+"_IK_CTRL")
    mc.setAttr (ArmCtrl+ ".overrideEnabled", 1)
    mc.setAttr (ArmCtrl + ".overrideColor", col)
    mc.select(ArmCtrl)
    mc.CenterPivot
    mc.xform(cpc=True)
    mc.scale(siz, siz, siz)
    mc.select (hand, add=True)
    mc.matchTransform(pos=True, rot=1)
    mc.select(cl=1)
    armGrp = mc.group(n="arm_GRP", em=True)
    mc.select(ArmCtrl, add=True)
    mc.matchTransform(pos=True, rot=1)
    mc.parent(ArmCtrl, armGrp)
    mc.select(ArmCtrl, r=True)
    mc.makeIdentity(a=True, s=True, t=True, r=True)
    mc.select(cl=True)
    mc.select(ArmIK[0])
    mc.select(ArmCtrl, add=1)
    mc.parent()
    handLoc=mc.spaceLocator(n=hand+"Loc")
    mc.select(ArmCtrl, add=True)
    mc.matchTransform(pos=True)
    mc.select(handLoc)
    mc.select(ArmCtrl, add=True)
    mc.parent()

    ElbowLoc= mc.spaceLocator(n=elbow+"Loc")
    mc.select(elbow, add=True)
    mc.matchTransform(pos=True)
    mc.select(ElbowLoc)
   
    mc.makeIdentity(a=True, s=True, t=True)
    mc.xform(t=(0,0,-2))
    mc.makeIdentity(a=True, s=True, t=True)
    mc.select(cl=True)
    mc.poleVectorConstraint(ElbowLoc, ArmIK[0])
    HipLoc=mc.spaceLocator(n=shoulder+"Loc")
    mc.select(shoulder, add=True)
    mc.matchTransform(pos=True)
    mc.select(cl=True)

    mc.select(HipLoc)
    mc.select(handLoc, add=True)
    dist= mc.distanceDimension()
    mc.select(cl=True)
    mc.select( dist)
    for jts in armJts:
        if jts != hand:
            mc.select(jts+"_IK", add=True)
        else:
            mc.select(jts+"_IK", add=True)

            break
     
    #mc.select(shoulder, hand,add=True ko)
    mc.select(shoulder+"_IK", d=True)
    stretchy.stretch()
    mc.select(cl=True)
    for jts in armJts:
        if jts != hand:
            mc.select(jts+"_IK", add=True)
            mc.selectKey(jts+"_IK.translateX", add=True, k=True)
           # mc.selectKey(jts+"_translateX"add=True, k=True)


        else:
            mc.select(jts+"_IK", add=True)
            mc.selectKey(jts+"_IK.translateX", add=True, k=True)

            break
    mc.keyTangent(e=True, itt="linear", ott="linear")

    mc.setInfinity(poi="cycleRelative")
    mc.orientConstraint(ArmCtrl, hand+"_IK", mo=True)
    mc.select(cl=True)
    mc.select(HipLoc, shoulder+"Loc", dist, shoulder+"_IK")
    mc.select(armGrp, add=True)
    mc.parent()
def HandIK(siz, shp, col):
    fingers = mc.listRelatives(c=True)
    hand = mc.ls(sl=True, typ="joint")[0]
    mc.group(hand, n=hand+"_Grp")
    
   # mc.select(wrist)
    for i, fJt in enumerate(fingers):
        mc.select (fJt, hi=True)
        finger = mc.ls(sl=True, typ="joint")
        root=finger[0] 
        end = finger[len(finger)-1]
        
        fingerIK=mc.ikHandle(sol="ikSCsolver", sj=root, ee=end, n=fJt+"_IK")
        fingCurve= MSCurves.getCurve(shp, root+"_Ctrl")
        mc.setAttr (fingCurve+ ".overrideEnabled", 1)
        mc.setAttr (fingCurve+ ".overrideColor", col)
        mc.select(fingCurve)
        mc.CenterPivot
        mc.xform(cpc=True)
        mc.scale(siz, siz, siz)
        mc.select (fingerIK, add=True)
        mc.matchTransform(pos=True)
        mc.makeIdentity(a=True, s=True, t=True)
        mc.select(cl=True)
        mc.select(fingerIK[0])
        mc.select(fingCurve, add=1)
        mc.parent()

        mc.select(hand+"_Grp", add=True)
        mc.parent()
def ShoulderIK(siz, shp, col):
    Clav = mc.ls(sl=True)[0]
    should= AutoRigMS.CharRig.getArm(len(AutoRigMS.CharRig.arm)-1)
    ShoulderCtrl =MSCurves.getCurve(shp,Clav+"_IK_CTRL" ) 
    mc.select(ShoulderCtrl, r =True)
    mc.setAttr (ShoulderCtrl+ ".overrideEnabled", 1)
    mc.setAttr (ShoulderCtrl + ".overrideColor", col)
    mc.select(ShoulderCtrl)
    mc.CenterPivot
    mc.xform(cpc=True)
    mc.scale(siz, siz, siz)
    mc.select (Clav, add=True)
    mc.matchTransform(pos=True, rot=1)
    mc.select(cl=1)
    mc.select(ShoulderCtrl, r=1)
    mc.makeIdentity(a=True, s=True, t=True, r=True)
    mc.select(cl=True)
    mc.parentConstraint(ShoulderCtrl, Clav)