import pathlib,json,argparse,os

home = pathlib.Path.home()
args = argparse.ArgumentParser()

args.add_argument("--path",action="append")
args.add_argument("--rack-user-presets",default=home/"AppData"/"Local"/"Rack2"/"presets")


ns = args.parse_args()

if not ns.path:
    print("no paths supplied. exiting.")
    exit()
paths = list(set(ns.path))

rack_user_presets = pathlib.Path(ns.rack_user_presets)

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

# }}}1

rack_vg_output = ns.rack_user_presets / "voxglitch" / "wavbank"

subpaths = list()


for path in paths:
    for r,ds,fs in os.walk(path):
        root = pathlib.Path(r)
        rwavs = 0
        for f in fs:
            rwavs += f.endswith(".wav")
        if rwavs > 14:
            subpaths.append([rwavs,r,pathlib.Path(path)])


for L,p,root in subpaths:
    rack_vg_rootpath = rack_vg_output / root.name
    rack_vg_rootpath.mkdir(exist_ok=True)

    path = pathlib.Path(p)
    rel = path.relative_to(root)
    parts = pathlib.Path(rel).parts

    rack_vg_sub = rack_vg_rootpath.joinpath(*parts[:-1])

    rack_vg_sub.mkdir(parents=True,exist_ok=True)

    for w in path.glob("*.wav"):
        firstwav = w
        break

    vg_j = voxglitch_wavbank_json.copy()
    vg_j["data"]["path"] = str(path)

    jname = f"{path.name} [{L}].vcvm"

    rack_vg_jpath = rack_vg_sub / jname

    if not rack_vg_jpath.is_file():
        with open(rack_vg_jpath,"w",encoding="utf-8") as f:
            f.write(json.dumps(vg_j,indent=True))
            print("wrote",rack_vg_jpath)

