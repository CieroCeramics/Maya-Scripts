import maya.cmds as mc
import sys
sys.path.append(r'C:/Users/red_w/Documents/maya/scripts/MacSturrup/')
import stretchy
import MSCurves

def createLegIK(siz, shp, col):
    hip = mc.ls(sl=True)[0]
    foot = mc.ls(sl=True)[1]
    knee= mc.ls(sl=True)[2]
    mc.select(cl=True)
    mc.select(hip, hi=True)
    legJts=mc.ls(sl=True)
    for jts in legJts:
        mc.select(jts, r=True)
        mc.joint(e=True, oj="xzy", sao="xup", ch=True, zso=True)
    mc.select(hip)
    IKLegJts=mc.duplicate(hip, n=hip+"_IK", rc=True)
    for i, jt in enumerate (IKLegJts):
        mc.rename(jt, legJts[i]+"_IK" )
    LegIK = mc.ikHandle(sol="ikRPsolver", sj=hip+"_IK", ee=foot+"_IK", n=foot+"_IKHandle")
    LegCtrl = MSCurves.getCurve(shp, foot+"_IK_CTRL")
    mc.setAttr (LegCtrl+ ".overrideEnabled", 1)
    mc.setAttr (LegCtrl+ ".overrideColor", col)
    mc.select(LegCtrl)
    mc.CenterPivot
    mc.xform(cpc=True)
    mc.scale(siz, siz, siz)
    mc.select (LegIK, add=True)
    mc.matchTransform(pos=True)
    mc.makeIdentity(a=True, s=True, t=True)
    mc.select(cl=True)
    mc.select(LegIK[0])
    mc.select(LegCtrl, add=1)
    mc.parent()
    footLoc=mc.spaceLocator(n=foot+"Loc")
    mc.select(LegCtrl, add=True)
    mc.matchTransform(pos=True)
    mc.select(footLoc)
    mc.select(LegCtrl, add=True)
    mc.parent()

    KneeLoc= mc.spaceLocator(n=knee+"Loc")
    mc.select(knee, add=True)
    mc.matchTransform(pos=True)
    mc.select(KneeLoc)
   
    mc.makeIdentity(a=True, s=True, t=True)
    mc.xform(t=(0,0,2))
    mc.makeIdentity(a=True, s=True, t=True)
    mc.select(cl=True)
    mc.poleVectorConstraint(KneeLoc, LegIK[0])
    HipLoc=mc.spaceLocator(n=hip+"Loc")
    mc.select(hip, add=True)
    mc.matchTransform(pos=True)
    mc.select(cl=True)

    mc.select(HipLoc)
    mc.select(footLoc, add=True)
    dist= mc.distanceDimension()
    mc.select(cl=True)
    mc.select( dist)
    for jts in legJts:
        if jts != foot:
            mc.select(jts+"_IK", add=True)
        else:
            mc.select(jts+"_IK", add=True)

            break
     
    #mc.select(hip, foot,add=True ko)
    mc.select(hip+"_IK", d=True)
    stretchy.stretch()
    mc.select(cl=True)
    for jts in legJts:
        if jts != foot:
            mc.select(jts+"_IK", add=True)
            mc.selectKey(jts+"_IK.translateX", add=True, k=True)
           # mc.selectKey(jts+"_translateX"add=True, k=True)


        else:
            mc.select(jts+"_IK", add=True)
            mc.selectKey(jts+"_IK.translateX", add=True, k=True)

            break
    mc.keyTangent(e=True, itt="linear", ott="linear")

    mc.setInfinity(poi="cycleRelative")
    
def makeRevFoot():
    foot= mc.ls(sl=True, typ="joint")
    mc.select(foot, hi=True)
    footJts= mc.ls(sl=True, typ="joint")
    toe= footJts[len(footJts)-1]
    mc.select(toe)
    toeTrans= mc.xform(q=True, t=True, ws=True)
    mc.select(foot, r=True)
    ankleTrans = mc.xform(q=True, t=True, ws=True)
    rHeel=mc.spaceLocator(n=foot[0]+"Revheel_Loc")
    mc.select(rHeel)

    mc.xform(t=(ankleTrans[0], toeTrans[1], ankleTrans[2]))  
    mc.makeIdentity(a=True, s=True, t=True)

    mc.parent(foot[0]+"Handle",rHeel)
       
    for i, jt in enumerate (footJts):

        if i>0:
            rJoint=mc.spaceLocator(n=jt+"Rev_Loc")
            mc.select(jt, add=True)
            mc.matchTransform(pos=True)
            
               ####################### 
            revFootIK = mc.ikHandle(sol="ikSCsolver", sj=footJts[i-1], ee=footJts[i], n=jt+"_Rev")

                ##############
            if i>1:
                mc.parent(footJts[i-1]+"Rev_Loc", footJts[i]+"Rev_Loc")
            if i== len(footJts)-1:
                mc.parent(jt+"Rev_Loc", rHeel)
            mc.select(cl=True)
            mc.select(revFootIK[0])
            mc.select(rJoint, add=True)
            mc.parent()
    mc.parent(rHeel, foot[0]+"_CTRL")
