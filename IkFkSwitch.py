import maya.cmds as mc
import sys
def IkFkSwitch():
    jroots= mc.ls(sl=True)
    jchains = []
    for i, root in enumerate(jroots):
        name= "chain{}".format(i)
        mc.select(root)
        thischain = []
        thischain.insert(0,root)
        #thischain.insert()
        jchains.insert (i, thischain+mc.listRelatives(ad=True,typ="joint"))
  #  mc.select(cl=True)
  #  mc.select(jchains[0],r=True)


    fkIkBlendName = mc.joint(jroots[0],q=True, n=True)
    fkIkBlend = mc.shadingNode("blendColors",asShader=True, n=fkIkBlendName+"FKblend" )

    if len(jroots)==3:

        ikTypeBlendName = mc.joint(jroots[1],q=True, n=True)
        ikTypeBlend = mc.shadingNode("blendColors",asShader=True, n=ikTypeBlendName+"Typeblend" )

        FKR1 = fkIkBlend+".color1R"; FKG1 = fkIkBlend+".color1G" ;FKB1 = fkIkBlend+".color1B"
        FKR2 = fkIkBlend+".color2R"; FKG2 = fkIkBlend+".color2G" ;FKB2 = fkIkBlend+".color2B"

        TBR1 = ikTypeBlend+".color1R"; TBG1 = ikTypeBlend+".color1G" ;TBB1 = ikTypeBlend+".color1B"
        TBR2 = ikTypeBlend+".color2R"; TBG2 = ikTypeBlend+".color2G" ;TBB2 = ikTypeBlend+".color2B"

        FKOutR= fkIkBlend+".outputR"; FKOutG = fkIkBlend+".outputG" ;FKOutB = fkIkBlend+".outputB"
        TBOut = ikTypeBlend+ ".output"

        FKc2 = fkIkBlend +".color2"
    jts1=jchains[1]; jts2 =jchains[2]
    for i, jts in enumerate(jchains[0]):
        mc.setAttr(FKR1, 1); mc.setAttr(FKG1, 0); mc.setAttr(FKB1, 0)
        mc.setAttr(TBR1, 0); mc.setAttr(TBG1, 1); mc.setAttr(TBB1, 0)
        mc.setAttr(TBR2, 0); mc.setAttr(TBG2, 0); mc.setAttr(TBB2, 1)

        Oweights0= jts+"_orientConstraint1."+jts+"_CTRLW0"
        Pweights0 = jts+"_pointConstraint1."+jts+"_CTRLW0"
        
        Oweights1= jts+"_orientConstraint1."+jts1[i]+"W1"
        Pweights1 = jts+"_pointConstraint1."+jts1[i]+"W1"

        Oweights2= jts+"_orientConstraint1."+jts2[i]+"W2"
        Pweights2 = jts+"_pointConstraint1."+jts2[i]+"W2"

        mc.connectAttr (FKOutR, Oweights0, f=True); mc.connectAttr(FKOutR, Pweights0, f=True)
        mc.connectAttr (FKOutG, Oweights1, f=True); mc.connectAttr(FKOutG, Pweights1, f=True)
        mc.connectAttr (FKOutB, Oweights2, f=True); mc.connectAttr(FKOutB, Pweights2, f=True)
    mc.connectAttr(TBOut, FKc2, f=True)
    

def jointBlend():
    jroots= mc.ls(sl=True)
    jchains = []
    for i, root in enumerate(jroots):
        name= "chain{}".format(i)
        mc.select(root)
        thischain = []
        thischain.insert(0,root)
        #thischain.insert()
        jchains.insert (i, thischain+mc.listRelatives(ad=True,typ="joint"))
    mc.select(cl=True)

    for i, jts in enumerate(jchains[0]):
        Oconst = jts+"orientConstraint"; Pconst =jts+"pointConstraint"
        toJointArray1=jchains[1]
        toJointArray2=jchains[2]

        mc.pointConstraint(toJointArray1[i],jts)
        mc.orientConstraint(toJointArray1[i],jts)
        
        mc.pointConstraint(toJointArray2[i],jts)
        mc.orientConstraint(toJointArray2[i],jts)
    mc.select(jroots[0]) ;  mc.select(jroots[1], add=1) ;  mc.select(jroots[2], add=1) 
    IkFkSwitch()
        


    
        

#ointBlend()
