import sys
import json
import jinja2

typeDefs = {}


def getSimpleName(name):
    nsp = name.rfind("::")
    if nsp >=0:
        return name[nsp+2:]
    else:
        return name

def modifyType(member):
    type = member["type"].strip()

    if type in typeDefs:
        member["type_origin"] = type
        type = typeDefs[type]
        member["type"] = type
    
    primitives = {
        "int": 1,
        "bool": 1,
        "long": 1,
        "short": 1,
        "char": 1,
        "long long": 1,
        "unsigned int": 1,
        "unsigned long": 1,
        "unsigned short": 1,
        "unsigned char": 1,
        "float": 1,
        "double": 1,
        "uint8": 1,
        "uint16": 1,
        "uint32": 1,
        "uint64": 1,
        "int8": 1,
        "int16": 1,
        "int32": 1,
        "int64": 1,
    }

    if "const" in type:
        member["type_const"] = True
        type = type.replace("const", "").strip()

    if type in primitives:
        member["type_pass"] = type
        member["type_base"] = type
        member["type_kind"] = "primitive"
    elif type == "void":
        member["type_pass"] = "void"
        member["type_base"] = "void"
        member["type_kind"] = "void"
        pass
    elif type.endswith("&"):
        type_base = type[:len(type)-1].strip()
        member["type_pass"] = type_base+"*"
        member["type_base"] = type_base
        member["type_kind"] = "ref"
    elif type.endswith("*"):
        type_base = type[:len(type)-1].strip()
        member["type_pass"] = type_base+"*"
        member["type_base"] = type_base
        member["type_kind"] = "pointer"
    else:
        member["type_pass"] = type + "*"
        member["type_base"] = type
        member["type_kind"] = "value"

    member["type_simple"] = getSimpleName(member["type_base"])

def setName(clazz):
    name = clazz["name"]
    symb_name = name.replace("::", "_")
    clazz["symb_name"] = symb_name

def visitFile(file):
    if file["kind"] == "file":
        file["name"] = ""
        file["symb_name"] = ""
    
    for enum in file["enum"]:
        setName(enum)

    for field in file["field"]:
        setName(field)
        modifyType(field)

    name = file["name"]
    for method in file["method"]:
        setName(method)
        if len(method["type"]) == 0:
            method["type"] = name+"*"
        modifyType(method)
        for param in method["param"]:
            modifyType(param)

def collectTypeDef(file):
    for typedef in file["typedef"]:
        name = typedef["name"]
        type = typedef["type"]
        typeDefs[name] = type

def modifyJson(input):
    for clazz in input:
        collectTypeDef(clazz)

    for clazz in input:
        setName(clazz)
        visitFile(clazz)

file = open(sys.argv[1])
input = json.load(file)
file.close()
modifyJson(input)

js = json.dumps(input, indent=4)
print(js)
