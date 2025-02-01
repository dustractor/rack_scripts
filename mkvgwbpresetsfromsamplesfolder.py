# mkvgwbpresetsfromsamplesfolder.py
# make voxglitch wavbank presets from samples folder

import argparse
import json
import pathlib
import sys
import copy
home = pathlib.Path.home()

# {{{1 get rack dir
rack_dir = {
    "win32": home / "AppData" / "Local" / "Rack2",
    "darwin": home / "Library" / "Application Support" / "Rack2",
    "linux": home / ".local" / "share" / "Rack2"
}.get(sys.platform,"unknownplatform")

if rack_dir == "unknownplatform":
    print("rack dir unknown for this platform.")
    exit()
# }}}1

# edit the following line or use the --samples-dir argument to choose the folder where you keep your wav samples
_DEFAULT_SAMPLES_DIR = pathlib.Path("d:\\zSamples")

args = argparse.ArgumentParser()
args.add_argument("--samples-dir",type=pathlib.Path,default=_DEFAULT_SAMPLES_DIR)
args.add_argument("--min-wavs",type=int,default=24) # the --min-wavs argument ignores folder with less than a certain number of samples
ns = args.parse_args()

# {{{1 json_template
json_template = {
  "plugin": "voxglitch",
  "model": "wavbank",
  "version": "2.32.1",
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
    "path": "--placeholder-text--",
    "trig_input_response_mode": 0
  }
}
# }}}1

presetsdir = rack_dir / "presets" / "voxglitch" / "wavbank"

target = presetsdir / ns.samples_dir.name

subdirs = []

for rpath,dirlist,filelist in ns.samples_dir.walk():
    wavcount = len([_ for _ in filelist if _.lower().endswith(".wav")])
    if wavcount > ns.min_wavs:
        newname = "{} [{}].vcvm".format(rpath.name,wavcount)
        parts = rpath.relative_to(ns.samples_dir).parts
        newpath = target.joinpath(*parts)/newname
        subdirs.append((rpath,newpath))

for rpath,t in subdirs:
    jd = copy.deepcopy(json_template)
    jd["data"]["path"] = str(rpath)
    t.parent.mkdir(parents=True,exist_ok=True)
    if not t.exists():
        print("creating",t)
    with open(t,"w",encoding="utf-8") as f:
        s = json.dumps(jd,indent=True)
        f.write(s)
    
print("OK")

