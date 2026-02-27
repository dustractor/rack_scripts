import pathlib
import json
import copy
import re
import argparse
import tkinter as tk
import tkinterdnd2 as dnd

args = argparse.ArgumentParser()
args.add_argument("--blank",default="blank.vcvs")
args.add_argument("--outdir",default=str(pathlib.Path.home()/"AppData"/"Local"/"Rack2"/"selections"/"8xwavbank-lfodriven"))
ns = args.parse_args()


# outdir = pathlib.Path.home()/"AppData"/"Local"/"Rack2"/"selections"/"8xwavbank-lfodriven"
outdir = pathlib.Path(ns.outdir)
print("outdir,outdir.is_dir():",outdir,outdir.is_dir())

with open("blank.vcvs","r",encoding="utf-8") as f:
    jdata = json.loads(f.read())

class App(dnd.TkinterDnD.Tk):
    def __init__(self):
        super().__init__()
        self.dirlist = tk.StringVar()
        self.listbox = tk.Listbox(self,listvariable=self.dirlist)
        self.listbox.pack(fill="both",expand=True)
        self.listbox.drop_target_register(dnd.DND_FILES)
        self.listbox.dnd_bind("<<Drop>>",self.drop_proc)
        self.process_pathlist_btn = tk.Button(self,text="process all",command=self.process_pathlist)
        self.process_pathlist_btn.pack()
        self.clear_pathlist_btn = tk.Button(self,text="clear",command=self.clear_pathlist)
        self.clear_pathlist_btn.pack()
    def drop_proc(self,event):
        for f in self.tk.splitlist(event.data):
            if pathlib.Path(f).is_dir():
                self.listbox.insert(tk.END,f)
    def clear_pathlist(self):
        self.listbox.delete(0,tk.END)
    def process_pathlist(self):
        paths = self.listbox.get(0,tk.END)
        for p in paths:
            jd = copy.deepcopy(jdata)
            path = pathlib.Path(p)
            outname = outdir / (path.parent.name + "__" + path.name + ".vcvs")
            for module in jd["modules"]:
                if module["plugin"] == "voxglitch" and module["model"] == "wavbank":
                    module["data"]["path"] = str(path)
                elif module["plugin"] == "Core" and module["model"] == "Notes":
                    module["data"]["text"] = path.parent.name + "\n" + path.name
                elif module["plugin"] == "NYSTHI" and module["model"] == "Label":
                    module["data"]["m_ltf0"] = path.parent.name + "\n" + path.name
            with open(outname,"w",encoding="utf-8") as f:
                f.write(json.dumps(jd,indent=True))
                print("wrote",outname)

app = App()
app.mainloop()

