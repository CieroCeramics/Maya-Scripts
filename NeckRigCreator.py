def MakeChange(val, field):
    val= mc.floatFieldGrp(field, query=True, value=True)[0]
    return val

