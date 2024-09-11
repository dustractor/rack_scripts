import tkinter as tk
import tkinter.ttk as ttk
import tkinter.filedialog as filedialog
import pathlib
import os
import json

sentinel_samples_folder_unset = "--choose samples folder--"
rack_presets_dir = pathlib.Path.home() / "AppData" / "Local" / "Rack2" / "presets"
voxglitch_wavbank_presets_dir = rack_presets_dir / "voxglitch" / "wavbank"

voxglitch_wavbank_json = {
    "plugin": "voxglitch",
    "model": "wavbank",
    "version": "2.0",
    "params": [
        {
            "value": 0.0,
            "id": 0
        },
        {
            "value": 1.0,
            "id": 1
        },
        {
            "value": 0.0,
            "id": 2
        }
    ],
    "data": {
        "path": "placeholder text",
        "trig_input_response_mode": 0
    }}

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.samples_folder = tk.StringVar()
        self.presets_folder = tk.StringVar()
        self.option_min_samples_count = tk.IntVar()
        self.samples_folder.set(sentinel_samples_folder_unset)
        self.presets_folder.set(voxglitch_wavbank_presets_dir)
        self.option_min_samples_count.set(15)
        self.frm_samples_folder = ttk.LabelFrame(self,text="Samples location:")
        self.frm_samples_folder.pack(fill="both",expand=True,anchor="ne")
        self.frm_presets_folder = ttk.LabelFrame(self,text="Presets location:")
        self.frm_presets_folder.pack(fill="both",expand=True,anchor="ne")
        self.frm_options = ttk.LabelFrame(self,text="Options:")
        self.frm_options.pack(fill="both",expand=True,anchor="ne")
        self.btn_samples_folder = ttk.Button(self.frm_samples_folder,
                                             command=self.choose_samples_folder,
                                             textvariable=self.samples_folder)
        self.btn_samples_folder.pack()
        self.lbl_presets_folder = ttk.Label(self.frm_presets_folder,
                                            textvariable=self.presets_folder)
        self.lbl_presets_folder.pack()
        self.lbl_opt_min_samples_ct = ttk.Label(self.frm_options,
                                                text="Ignore folders with less than X samples:")
        self.opt_min_samples_ct = tk.Spinbox(self.frm_options,
                                             from_=1,to=9999,
                                             increment=1,
                                             format="%4.0f",
                                             state="readonly",
                                             textvariable=self.option_min_samples_count)
        self.lbl_opt_min_samples_ct.pack()
        self.opt_min_samples_ct.pack()
        self.btn_execute = ttk.Button(self,
                                      command=self.execute,
                                      text="Execute")
        self.btn_execute.pack()

    def choose_samples_folder(self):
        choice = filedialog.askdirectory(mustexist=True)
        path = pathlib.Path(choice)
        if choice != "" and path.is_dir():
            self.samples_folder.set(str(path))

    def execute(self):
        samples_dir = self.samples_folder.get()
        if samples_dir == sentinel_samples_folder_unset:
            print("must choose samples folder")
            return
        presets_dir = self.presets_folder.get()
        min_samples = self.option_min_samples_count.get()
        samples_dir_p = pathlib.Path(samples_dir)
        presets_dir_p = pathlib.Path(presets_dir)
        presets_dir_p.mkdir(parents=True,exist_ok=True)
        subpaths = list()
        presets_rootpath = presets_dir_p / samples_dir_p.name
        presets_rootpath.mkdir(exist_ok=True)
        for r,ds,fs in os.walk(samples_dir_p):
            root = pathlib.Path(r)
            rwavs = 0
            for f in fs:
                rwavs += f.endswith(".wav")
            if rwavs >= min_samples:
                subpaths.append([rwavs,root])
        for wav_ct,path in subpaths:
            rel = path.relative_to(samples_dir_p)
            parts = pathlib.Path(rel).parts
            presets_subpath = presets_rootpath.joinpath(*parts[:-1])
            presets_subpath.mkdir(parents=True,exist_ok=True)
            jdata = voxglitch_wavbank_json.copy()
            jdata["data"]["path"] = str(path)
            jname = f"{path.name} [{wav_ct}].vcvm"
            jpath = presets_subpath / jname
            if not jpath.is_file():
                with open(jpath,"w",encoding="utf-8") as f:
                    f.write(json.dumps(jdata,indent=True))
                    print("written:",jpath)
        print("action completed")


def main():
    if not rack_presets_dir.is_dir():
        print(f"rack presets dir: [ {rack_presets_dir} ] not found.")
        return
    app = App()
    app.mainloop()

if __name__ == "__main__":
    main()
