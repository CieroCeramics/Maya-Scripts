#for rendering

import maya.cmds as mc

from mtoa.cmds.arnoldRender import arnoldRender

import maya.app.general.createImageFormats as createImageFormats

import re

def loadlights ():
    lts = mc.ls(sl=True)
    return lts

def setFile():
    fileilters = "PNG (*.png);;JPEG (*.jpg);;TIFF (*.tiff);;IFF (*.iff*)"
    file = mc.fileDialog2(startingDirectory ="/C://", fileFilter=fileilters,dialogStyle=1, rf=True,fileMode=2)
   # res = re.findall(r'u\'.*?\'', file)
    mc.textFieldButtonGrp ( "setFile",e=True, text=file[0])
    typ= file[1]
def test():
   mc.select(hi=True)
   meshshapes=mc.ls(sl=True,typ="mesh")
   mc.select(meshshapes[0])
   myshape=mc.ls(sl=True)
   exec("print myshape[0]")
   mc.setAttr(myshape[0]+".primaryVisibility",0)

def hideChildren(parent):
    mc.select(cl=True)
    mc.select(parent, hi=True)
    shapes=mc.ls(sl=True,typ="mesh")
    for sh in shapes:
        mc.setAttr(sh+".primaryVisibility",0)

def showChildren(parent):
    mc.select(cl=True)
    mc.select(parent, hi=True)
    shapes=mc.ls(sl=True,typ="mesh")
    for sh in shapes:
        mc.setAttr(sh+".primaryVisibility",1)
    #setAttr "model2:head_lowShapeDeformed.primaryVisibility" 1;
# Hide the preview pane.
   
def loadmeshes ():
    return mc.ls(sl=True)
      
def hyperRender():
    
    gamma = mc.floatSliderGrp("gamma", q=True, v=True)
    
    width = mc.intFieldGrp("Resolution", q=True, value1=True)
    height= mc.intFieldGrp("Resolution", q=True, value2=True)
    fr= mc.textFieldButtonGrp("setFile", q=True, text=True) +"/"

    mc.eval
    
    mc.select (lights)
    mc.select(meshes, add=True)
   

    mc.showHidden(a=True)
    for m in meshes:
        hideChildren(m)
    for l in lights:
        mc.hide(l)
    for mesh in meshes:
       # hideChildren(mesh)
        for light in lights:

            mc.select(cl=True)
            mc.select (mesh)
            mc.select(light, add=True)
            showChildren(mesh)
            mc.showHidden(light)
            name = mesh + light + "output"

            mc.setAttr("defaultArnoldDriver.ai_translator", "png", type="string")
            mc.setAttr("defaultArnoldDriver.pre", name, type="string")
            arnoldRender(width, height, True, True,'RenderCam_', ' -layer defaultRenderLayer')
            #render stuff here
            editor  = 'renderView'
            #render_output = mc.renderer(editor, e=True)


            
            # mc.eval('renderWindowRender redoPreviousRender renderView')
            # editor = 'renderView'
            formatManager = createImageFormats.ImageFormats()
            formatManager.pushRenderGlobalsForDesc("PNG")
            mc.renderWindowEditor(editor,  e=True, ga=gamma,  com=True, cme=True,writeImage=fr+name+'.png')
            exec("print 'file saved to' + fr+name+'.png'")
            formatManager.popRenderGlobals()


            
            
            mc.hide(light)
            hideChildren(mesh)
    
#hyperRender()


lights = []
meshes = []

typ= "png"
window = mc.window (title ="Hyper Render Options", iconName = 'Short Name', widthHeight=(320, 700) )

mc.columnLayout ("HyperRender", adj=True, cal="left")


mc.iconTextStaticLabel( st='textOnly', l='Select all the lights to render' )

mc.button ( "selectLightButton",
        label = "Load Selected Lights",
        command = "lights = loadlights()")

mc.iconTextStaticLabel( st='textOnly', l='Select all the meshes to render' )

mc.button ( "selectMeshButton",
        label = "Load Selected Meshes",
        command = "meshes = loadmeshes()")



mc.intFieldGrp("Resolution",cw=[1,50],  
                    ct3 = ["left", "left","left"], 
                    numberOfFields=2, 
                    label='Size', 
                    value1=200, 
                    value2=200)


mc.floatSliderGrp("gamma",
            label = "Gamma",
            field = True, 
            cw3 = (80,40, 150), 
            minValue = 0, 
            maxValue= 5,
            fieldMinValue = .0,
            fieldMaxValue = 5,
            value = 1)
basicFilter = "*.mb"
fr="c:/"


mc.iconTextStaticLabel( st='textOnly', l='Select folder to save images' )
mc.textFieldButtonGrp ( "setFile",
        buttonLabel = "Explore",
        cl2= ["left", "left"],
        adj=True,
        text =fr,
        buttonCommand = "fr=setFile()")

mc.button ( "Render",
        label = "Render",
        command = "hyperRender()")

mc.button ( "test",
        label = "test",
        command = "test()")
# Close button with a command to delete the UI
mc.button( label='Close', command=('cmds.deleteUI(\"' + window + '\", window=True)') )
# Set its parent to the Maya window (denoted by '..')
mc.setParent( '..' )
# Show the window that we created (window)
mc.showWindow( window )
