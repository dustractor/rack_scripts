import pathlib,json,copy,random

presets_dir = pathlib.Path.home()/"AppData"/"Local"/"Rack2"/"presets"/"NYSTHI"/"PolySevenSeas2"

# print("presets_dir:",presets_dir)
# print("presets_dir.exists():",presets_dir.exists())

template_file = presets_dir/"blank.vcvm"

with open(template_file,"r",encoding="utf-8") as f:
    jdata = json.loads(f.read())
# print("jdata:",jdata)

tables_dirs = [
    pathlib.Path.home()/"Documents"/"Xfer"/"Serum 2 Presets"/"Tables",
    pathlib.Path.home()/"Documents"/"Xfer"/"Serum Presets"/"Tables",
    pathlib.Path.home()/"Documents"/"Vital"]

wavs = []
for d in tables_dirs:
    wavs.extend(list(d.glob("**/*.wav")))
# print("len(wavs):",len(wavs))
for n in range(32):
    jd = copy.deepcopy(jdata)
    selx = list(map(str,random.choices(wavs,k=64)))
    jd["data"]["m_bank_names"] = selx
    with open(presets_dir/f"randoms_{n}.vcvm","w",encoding="utf-8") as f:
        f.write(json.dumps(jd,indent=True))

