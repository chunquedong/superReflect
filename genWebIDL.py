import sys
import json

def visitMethod(method):
    paramStr = ""
    for param in method["param"]:
        if paramStr:
            paramStr += ", "
        paramStr += param["type"] + " " + param["name"]

    static = "";
    if method.get("static"):
        static = "static "
    print("  "+static+method["type"]+ " " + method["name"] + "("+paramStr+");")

def visitField(field):
    static = "";
    if field.get("static"):
        static = "static "
    print("  "+static+"attribute "+field["type"]+ " " + field["name"] + ";")

def visitEnum(parent, enum):
    name = enum["name"]
    if parent:
        name = parent + "::"+name
    mname = name.replace("::", "_")
    print("enum "+mname + " {")

    for value in enum["values"]:
        print("  \""+name+"::"+value["name"]+"\",")

    print('};')

def visitClass(clazz):

    name = clazz["name"]
    nsp = name.rfind("::")
    if nsp >=0:
        namespace = name[:nsp+2]
        name = name[nsp+2:]
    else:
        namespace = ""

    for enum in clazz["enum"]:
        if namespace:
            print("[Prefix=\""+namespace+"\"]")
        visitEnum(name, enum)

    
    desc = clazz.get("desc");
    if desc:
        print("//"+desc)
    
    if namespace:
        print("[Prefix=\""+namespace+"\"]")

    base_class = ""
    if clazz.get("base"):
        base_class = " : "+clazz.get("base").join(", ")
    
    print("interface "+name + base_class +" {")

    for field in clazz["field"]:
        visitField(field)

    for method in clazz["method"]:
        visitMethod(method)


    print("};")


file = open(sys.argv[1])
input = json.load(file)
file.close()

for clazz in input:
    print("")
    visitClass(clazz)
