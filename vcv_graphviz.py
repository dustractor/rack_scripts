import pathlib
import json
import zstandard
import random
import math
import shutil
import subprocess
import tempfile
import sys
import tkinter as tk
from PIL import Image,ImageTk

outputdot = pathlib.Path.home()/"Desktop"/"outputdot.dot"
outputpng = pathlib.Path.home()/"Desktop"/"outputpng.png"

dataerror = json.dumps(dict(modules=[dict(plugin="ERROR",model="ERROR")]))

dot_location = "c:\\Program Files (x86)\\Graphviz\\bin\\dot.exe"
dot_path = pathlib.Path(dot_location)

names = dict()

def getname(n):
    if n not in names:
        names[n] = 0
    names[n] += 1
    return f"{n}.{names[n]}"

def getvcvpatches():
    vcv_patchdir = pathlib.Path.home()/"AppData"/"Local"/"Rack2"/"patches"
    files = list(vcv_patchdir.glob("*.vcv"))
    return files

def getpatchjson(patchpathobj):
    with open(patchpathobj,"rb") as f:
        zstd = zstandard.ZstdDecompressor()
        reader = zstd.stream_reader(f)
        rdata = reader.read()
        subdata = rdata[
            rdata.index(bytes("{",encoding="latin-1")):
            rdata.rindex(bytes("}\x00",encoding="latin-1"))+1]
        try:
            data = subdata.decode("utf-8")
        except UnicodeDecodeError:
            data = dataerror
        jdata = json.loads(data)
        return jdata

patches = getvcvpatches()

patch = random.choice(patches)

jdata = getpatchjson(patch)

dottemplate = """digraph foograph{{
    bgcolor="#333333";
    color="#880000";
    graph[fontname="arial"];
    edge[fontname="arial"];
    node[fontname="arial",shape="box",style="filled,rounded",fillcolor="#555555",fontcolor="#cccccc"];
    {dotcontent}
}}
"""

def dot_txt(dotdata):
    txt = dottemplate.format(dotcontent=dotdata)
    return txt

def getslug(m):
    plugin = m["plugin"]
    model = m["model"]
    name = f"{plugin}[{model}]"
    name = name.replace(" ","_")
    slug = getname(name)
    return slug

def json_to_gv(jd):
    cxlist = list()
    print(list(jd.keys()))
    id_to_module = {m["id"]:m for m in jd["modules"]}
    id_to_slug = {m["id"]:getslug(m) for m in jd["modules"]}
    for cable in jd["cables"]:
        from_id = cable["outputModuleId"]
        to_id = cable["inputModuleId"]

        module_from = id_to_module[from_id]
        module_to = id_to_module[to_id]

        module_from_label = id_to_slug[from_id]
        module_to_label = id_to_slug[to_id]
        cxlist.append(f"\"{module_from_label}\"->\"{module_to_label}\";")
    gv = "\n".join(cxlist)
    print(gv)
    # sys.exit()
    return gv
# json_to_gv(jdata)

with open(outputdot,"w",encoding="utf-8") as f:
    f.write(dot_txt(json_to_gv(jdata)))

subprocess.run([dot_path,"-Tpng",outputdot,"-o",outputpng])

root = tk.Tk()
root.bind("<Escape>",lambda _:root.quit())
image = Image.open(outputpng)
imgtk = ImageTk.PhotoImage(image)
image_label = tk.Label(root,image=imgtk)
image_label.imgtk = imgtk
image_label.pack()
root.mainloop()
