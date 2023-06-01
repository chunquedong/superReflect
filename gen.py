import jinja2
import sys
import json



file = open(sys.argv[1])
template = sys.argv[2]
input = json.load(file)
file.close()

env = jinja2.Environment(loader=jinja2.FileSystemLoader(""))
temp = env.get_template(template)

temp_out = temp.render(clazz=input["class"], file=input["file"])
print(temp_out)
