import maya.cmds as mc
import sys

def createAnimClips(fileRef):
    fileN =  mc.file(q=True, sn=True) 
    exec ("print fileN")
    for i, f in enumerate(fileRef):
        if i <len(fileRef)-1:
            mc.file(new=True, force=True)
           
            mc.file(fileN, o=1)
            importFile(f)
            root = "Root_M"
            mc.select(root, hi=True)
            mc.BakeSimulation()
            mc.select ("boy", r = True)
            tempN=f.split("/")
            fNameTemp = tempN[len(tempN)-1]
            fNameAlmost=fNameTemp.split(".")
            fName = fNameAlmost[0]
            fname = fName.replace(" ", "")
            exec ("print fName")
            mc.clip (n=fname+"clip", sc=1, animCurveRange=True)
            #mc.select(fname+"clip", r=True)
           # exec("doExportClipArgList 1 {'clipEditorPanel1ClipEditor'}")
            mc.file("C:/Users/red_w/Documents/maya/projects/default/clips/boy/"+fName+".ma", es=True, type="mayaAscii")
        #mc.undo()
        #mc.undo()
       # mc.undo()
      #  mc.undo()
     #   mc.undo()
def importClips(files):
    
    for i, f in enumerate(files):
        mc.file(f, i=True)
        clip =  mc.timeEditorClip(showAnimSourceRemapping =True,importOption = "connect", track = "Composition1:-1" , importMayaFile = f, startTime = 18 )
        mc.file (f, preserveUndo = true, r =True,  rnn = True, ns= "CTEImportTemporaryReference" )
        exec ("fileCmdCallback")
        st = mc.timeEditorClip(clip, q = 1, s = 1)

#select -r Crouch_Idle:CrouchIdleclipSource ;
#clip -copy Crouch_Idle:CrouchIdleclipSource; doPasteClipArgList 6 {"byMapOrNodeName", "specify", "Ruth1", "0", "16", "-1", "", " -defaultAbsolute"};
#clip  -defaultAbsolute -pasteInstance -sc 1 -startTime 16 -mapMethod "byMapOrNodeName" Ruth1;
        #tempN=f.split("/")
        #fNameTemp = tempN[len(tempN)-1]
        #fNameAlmost=fNameTemp.split(".")
       # fName = fNameAlmost[0]
      #  fname = fName.replace(" ", "_")
        #exec("print fname")
     #   mc.clipSchedule("CroneScheduler1", start = 1, ra= True, instance = fName+"CroneClips1" )
def test():
    s=mc.ls(sl=True)[0]
    tfbt = mc.textFieldButtonGrp( "tbg", q=1, tx=1 )[0]
    print (tfbt)
    mc.textFieldButtonGrp( "tbg", e=1, tx= s)
    #mc.textFieldButtonGrp( label='Label', text='Text', buttonLabel='Button' )
def getFiles():
    filefilters = "FBX (*.fbx);; mayaAscii (*.ma)"
    file = mc.fileDialog2(startingDirectory ="/C://users/red_w/documents/maya/projects/defaut/scenes", fileFilter=filefilters,dialogStyle=1, rf=True,fileMode=4)
   # res = re.findall(r'u\'.*?\'', file)
    mc.textFieldButtonGrp ( "setFile",e=True, text=file[0])
    typ= file[1]
    fr = mc.textFieldButtonGrp("setFile", q=True, tx=True)
    return file

def importFile(fName):
    mc.file(fName, i=True)

window = mc.window (title ="Anim Clip Macro", iconName = 'Short Name', widthHeight=(320, 700) )

mc.columnLayout ("ClipMacro", adj=True, cal="left")

fr="c:/"
mc.iconTextStaticLabel( st='textOnly', l='choose Files' )
mc.textFieldButtonGrp ( "setFile",
        buttonLabel = "Explore",
        cl2= ["left", "left"],
        adj=True,
        text =fr,
        buttonCommand = "fr=getFiles()")
mc.showWindow( window )

tb = mc.textFieldButtonGrp( "tbg", label='Label', text='Text', buttonLabel='Button', p=window)
mc.textFieldButtonGrp( "tbg", e=1, bc="test()" )

mc.button("test",label= "export clip files", command ="createAnimClips(fr)" )
mc.button("test2",label= "import clip files", command ="importClips(fr)" )
##createAnimClips()
