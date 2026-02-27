import pathlib
import json
import copy
import re
import argparse
import tkinter as tk
import tkinterdnd2 as dnd
import uuid

args = argparse.ArgumentParser()
args.add_argument("--blank",default="autobreak_blank.vcvs")
args.add_argument("--outdir",default=str(pathlib.Path.home()/"AppData"/"Local"/"Rack2"/"selections"/"8x_autobreak"))
ns = args.parse_args()


outdir = pathlib.Path(ns.outdir)

with open(ns.blank,"r",encoding="utf-8") as f:
    jdata = json.loads(f.read())

class App(dnd.TkinterDnD.Tk):
    def trace_dirlist(self,*t):
        self.count_label_txt.set(str(len(self.listbox.get(0,tk.END))))
    def __init__(self):
        super().__init__()
        self.dirlist = tk.StringVar()
        self.dirlist.trace("w",self.trace_dirlist)
        self.count_label_txt = tk.StringVar()
        self.count_label = tk.Label(self,textvariable=self.count_label_txt)
        self.count_label.pack()
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
            fpath = pathlib.Path(f)
            if (    fpath.is_file() and
                    fpath.suffix == ".wav" and
                    len(self.listbox.get(0,tk.END)) < 40):
                self.listbox.insert(tk.END,f)
    def clear_pathlist(self):
        self.listbox.delete(0,tk.END)
    def process_pathlist(self):
        pathlist = self.listbox.get(0,tk.END)
        pathx = iter(pathlist)
        jd = copy.deepcopy(jdata)
        outname = outdir / (uuid.uuid4().hex + ".vcvs")
        for module in jd["modules"]:
            if module["plugin"] == "voxglitch" and module["model"] == "autobreak":
                module["data"]["loaded_sample_path_1"] = str(next(pathx))
                module["data"]["loaded_sample_path_2"] = str(next(pathx))
                module["data"]["loaded_sample_path_3"] = str(next(pathx))
                module["data"]["loaded_sample_path_4"] = str(next(pathx))
                module["data"]["loaded_sample_path_5"] = str(next(pathx))
            elif module["plugin"] == "StochasticTelegraph" and module["model"] == "Fermata":
                module["data"]["text"] = "\n".join(pathlist)
        with open(outname,"w",encoding="utf-8") as f:
            f.write(json.dumps(jd,indent=True))
            print("wrote",outname)

app = App()
app.mainloop()

