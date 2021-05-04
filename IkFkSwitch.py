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
        exec ("print '3'")
        ikTypeBlendName = mc.joint(jroots[1],q=True, n=True)
        ikTypeBlend = mc.shadingNode("blendColors",asShader=True, n=ikTypeBlendName+"Typeblend" )


        jts1=jchains[1]; jts2 =jchains[2]
        for i, jts in enumerate(jchains[0]):
            mc.setAttr(fkIkBlend + ".color1", 1, 0, 0)
            mc.setAttr(ikTypeBlend +".color1", 0,1,0)
            mc.setAttr(ikTypeBlend +".color2", 0, 0, 1)

            
            Oweights0= jts+"_orientConstraint."+jts+"_CTRLW0"
            Pweights0 = jts+"_pointConstraint."+jts+"_CTRLW0"
            
            Oweights1= jts+"_orientConstraint."+jts1[i]+"W1"
            Pweights1 = jts+"_pointConstraint."+jts1[i]+"W1"

            Oweights2= jts+"_orientConstraint."+jts2[i]+"W2"
            Pweights2 = jts+"_pointConstraint."+jts2[i]+"W2"

            mc.connectAttr(fkIkBlend+".outputR", Oweights0)
            mc.connectAttr(fkIkBlend+".outputG", Oweights1)
            mc.connectAttr(fkIkBlend+".outputB", Oweights2)
            mc.connectAttr(fkIkBlend+".outputR", Pweights0)
            mc.connectAttr(fkIkBlend+".outputG", Pweights1)
            mc.connectAttr(fkIkBlend+".outputB", Pweights2)
        mc.connectAttr(ikTypeBlend+".output", fkIkBlend +".color2", f=True)
    if len(jroots)==2:
        
        mc.setAttr(fkIkBlend + ".color1", 1, 0, 0)
        mc.setAttr(fkIkBlend + ".color2", 0, 1, 0)
        #exec ("print '2'")
        jts2=jchains[1]
        for i, jts in enumerate(jchains[0]):
            mc.setAttr(fkIkBlend+".color1", 1,0,0) 
            # for att in mc.listAttr(jts+"_orientConstraint1"):
            #     if "WO" in att:
            #         Oweights0=att
            #     if "W1" in att:
            #         Oweights1=att
            # for att in mc.listAttr(jts+"_pointConstraint1"):
            #     if "WO" in att:
            #         Pweights0=att
            #     if "W1" in att:
            #         Pweights1=att    
                    

            Oweights0= jts+"_orientConstraint1."+jts+"_CTRLW0"
            Pweights0 = jts+"_pointConstraint1."+jts+"_CTRLW0"
        
            Oweights1= jts+"_orientConstraint1."+jts2[i]+"W1"
            Pweights1 = jts+"_pointConstraint1."+jts2[i]+"W1"

            mc.connectAttr(fkIkBlend+".outputR", Oweights0)
            mc.connectAttr(fkIkBlend+".outputG", Oweights1)
            mc.connectAttr(fkIkBlend+".outputR", Pweights0)
            mc.connectAttr(fkIkBlend+".outputG", Pweights1)
            
         






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

    if len(jroots)==3:
        for i, jts in enumerate(jchains[0]):
            Oconst = jts+"_orientConstraint"; Pconst =jts+"_pointConstraint"

        
            toJointArray1=jchains[1]
            toJointArray2=jchains[2]

            mc.pointConstraint(toJointArray1[i],jts, n=Pconst)
            mc.orientConstraint(toJointArray1[i],jts, n=Oconst)
            
            mc.pointConstraint(toJointArray2[i],jts, n=Pconst)
            mc.orientConstraint(toJointArray2[i],jts, n=Oconst)
        mc.select(jroots[0]) ;  mc.select(jroots[1], add=1) ;  mc.select(jroots[2], add=1) 
    if len(jroots)==2:
        for i, jts in enumerate(jchains[0]):
            Oconst = jts+"_orientConstraint1"; Pconst =jts+"_pointConstraint1"

        
            toJointArray1=jchains[1]

            mc.pointConstraint(toJointArray1[i],jts, n=Pconst)
            mc.orientConstraint(toJointArray1[i],jts, n=Oconst)
        mc.select(jroots[0]) ;  mc.select(jroots[1], add=1) 
    IkFkSwitch()
        


    
        

#jointBlend()
#L_Front_Tentacle_FK1_orientConstraint.L_Front_Wiggle_IK1W1
#L_Front_Tentacle_FK1_orientConstraint.L_Front_Wiggle_IK1W1