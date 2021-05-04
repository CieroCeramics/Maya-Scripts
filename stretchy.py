import maya.cmds as mc

def stretch():
    sjts= mc.ls(sl=True, typ="joint")
    mc.select(hi=True)
    dist= mc.ls(sl=True, typ="distanceDimShape")
    total=0
    mc.select(cl=True)
    exec("print dist[0]+'.distance'")
    for jts in sjts:
        jLen= mc.getAttr(jts+".translateX")
        total = total+jLen
    for jts in sjts:
        jLen= mc.getAttr(jts+".translateX")
        mc.select(jts)
        mc.setDrivenKeyframe(jts, cd=dist[0]+".distance",dv=abs(total), at="translateX", v=jLen)
        mc.select(jts)
        mc.setDrivenKeyframe(jts, cd=dist[0]+".distance", dv=abs(total)*2,at="translateX", v=jLen*2)
        mc.select(cl=True)

