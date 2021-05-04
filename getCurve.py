import maya.cmds as mc
from decimal import *

getcontext().prec = 5

shp = mc.listRelatives(mc.ls(sl=1)[0],s=1)[0]
cvs = mc.getAttr(shp+'.cv[*]')
cvsSimple = []
for c in cvs:
    cvsSimple.append([float(Decimal("%.3f" % c[0])),float(Decimal("%.3f" % c[1])),float(Decimal("%.3f" % c[2]))])


out = '\n\n### run python: #################\n\nimport maya.cmds as mc\nmc.curve(p='  
out += '[%s]' % ', '.join(map(str, cvsSimple))
out += ',d='+str(mc.getAttr(shp+'.degree'))+')\n\n#################################'

#print out