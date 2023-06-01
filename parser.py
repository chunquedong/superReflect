from xml.dom import minidom
import json
import os
import sys

classIndex = {}

def parse_type(member: minidom.Element):
    mem_type = "void"
    type_content = member.getElementsByTagName("type")[0].firstChild
    if type_content is not None:
        mem_type = type_content.nodeValue
        if mem_type == None:
            refid = type_content.getAttribute("refid")
            mem_type = classIndex[refid]
    return mem_type

def parse_operation(member: minidom.Element):

    mem_name = member.getElementsByTagName("name")[0].firstChild.nodeValue
    mem_privacy = member.getAttribute("prot")
    mem_static = member.getAttribute("static")
    mem_type = parse_type(member)

    mem_args = []
    argsstring = member.getElementsByTagName("param")
    for p in argsstring:
        p_type = parse_type(p)
        p_name = p.getElementsByTagName("declname")[0].firstChild.nodeValue
        #mem_args.append({"name":p_name, "type":p_type})
        mem_args.append(p_type)


    brief_desc = ""
    desc = member.getElementsByTagName("briefdescription")
    if len(desc) > 0:
        desc = desc[0].getElementsByTagName("para")
        if len(desc) > 0:
            desc = desc[0].firstChild.nodeValue
            brief_desc = desc

    command = []
    desc = member.getElementsByTagName("detaileddescription")
    if len(desc) > 0:
        for para in desc[0].childNodes:
            for itemlist in para.childNodes:
                if itemlist.nodeName == "simplesect":
                    name = itemlist.getAttribute("kind")
                    spara = para.getElementsByTagName("para")
                    value = ""
                    if len(spara) > 0:
                        value = spara[0].firstChild.nodeValue
                    #print("@",name, value)
                    command.append({name:value})

                if itemlist.nodeName == "parameterlist":
                    for item in itemlist.childNodes:
                        if item.nodeName == "parameteritem":
                            pi = item
                            pnl = pi.getElementsByTagName("parameternamelist")
                            name = ""
                            for pn in pnl:
                                name = pn.getElementsByTagName("parametername")[0].firstChild.nodeValue
                                break
                            pd = pi.getElementsByTagName("parameterdescription")
                            pdpara = pd[0].getElementsByTagName("para")
                            value = pdpara[0].firstChild.nodeValue
                            #print("@param",name, value)
                            command.append({"param":name, "value":value})

    res = {
        "name": mem_name,
        "access": mem_privacy,
        "static": mem_static,
        "type": mem_type,
        "param": mem_args,
        "desc": brief_desc,
        "command": command,
    }
    return res

def parse_enum(member: minidom.Element):
    mem_name = member.getElementsByTagName("name")[0].firstChild.nodeValue
    mem_privacy = member.getAttribute("prot")

    values = []
    for enumvalue in member.getElementsByTagName("enumvalue"):
        name = enumvalue.getElementsByTagName("name")[0].firstChild.nodeValue
        value = enumvalue.getElementsByTagName("initializer")
        if len(value) > 0:
            value = value[0].firstChild.nodeValue
            value = value.replace("=", "").strip()
        else:
            value = ""
        values.append({"name":name, "value":value})
    
    return {"name": mem_name, "access":mem_privacy, "values": values}
    
def _parse_class_file(file: str):
    xml_doc = minidom.parse(file)

    compounddef = xml_doc.getElementsByTagName('compounddef')[0]
    refid = compounddef.attributes["id"].value

    class_name = compounddef.getElementsByTagName("compoundname")[0].firstChild.nodeValue

    kind = compounddef.attributes["kind"].value
    class_flag = ""
    base_class = []
    inner_class = []
    if kind == "file":
        if compounddef.hasAttribute("abstract"):
            if compounddef.attributes["abstract"].value == "yes":
                class_flag = "abstract"

        basecompounds = compounddef.getElementsByTagName("basecompoundref")
        for cop in basecompounds:
            if cop.hasAttribute("refid"):
                gen_refid = cop.attributes["refid"].value
                gens.append(classIndex[gen_refid])
            else:
                base_class.append(cop.childNodes[0].data)
    
    field = []
    method = []
    enum = []
    typedef = []
    sections = compounddef.getElementsByTagName("sectiondef")
    # print("nb section", len(sections))
    for section in sections:
        for member in section.getElementsByTagName("memberdef"):
            mem_kind = member.attributes["kind"].value
            if mem_kind in ["property","variable"]:
                af = parse_operation(member)
                del af["param"]
                field.append(af)
            elif mem_kind in ["event","function","signal","prototype","friend","slot"]:
                # print("  do_operation", member.getElementsByTagName("name")[0].firstChild.nodeValue)
                method.append(parse_operation(member))

            elif mem_kind in ["enum"]:
                enum.append(parse_enum(member))

            elif mem_kind == "typedef":
                name = member.getElementsByTagName("name")[0].firstChild.nodeValue
                ptype = parse_type(member)
                typedef.append({"name": name, "type":ptype})


    for innerclass in compounddef.getElementsByTagName("innerclass"):
        #print("#####", innerclass)
        cname = innerclass.firstChild.nodeValue
        inner_class.append(cname)
    
    res = {
        "name": class_name,
        "kind": kind,
        "field": field,
        "method": method,
        "enum": enum,
        "inner_class": inner_class,
        "typedef": typedef,
    }
    if kind != "file":
        res["flag"] = class_flag
        res["base"] = base_class
    return res
    


def parse_file(indexFile, files):
    clist = []
    file = []
    doxy_root = os.path.dirname(indexFile)

    for clss in files:
        obj = _parse_class_file(os.path.join(doxy_root, clss[1] + ".xml"))
        if obj["kind"] == "file":
            file.append(obj)
        else:
            clist.append(obj)

    return {"class":clist, "file":file}

def parse_index(indexFile):
    xml_doc = minidom.parse(indexFile)
    compounds = xml_doc.getElementsByTagName('compound')

    files = []
    for s in compounds:
        kind = s.attributes["kind"].value
        if kind in ["class","struct","interface","protocol","exception","file"]:
            refid = s.attributes["refid"].value
            name = s.getElementsByTagName('name')[0].firstChild.nodeValue
            classIndex[refid] = name
            files.append((name, refid))
    return files



indexFile = sys.argv[1]
files = parse_index(indexFile)
res = parse_file(indexFile, files)
js = json.dumps(res, indent=4)
print(js)
