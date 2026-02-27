import pathlib,json,copy

inpath = pathlib.Path("C:\\Users\\user\\AppData\\Local\\Rack2\\presets\\SickoCV\\TrigSeqPlus")

print(inpath,inpath.exists())
outpath = inpath / "_12step"
outpath.mkdir(exist_ok=True)
print(outpath,outpath.exists())

infiles = list(inpath.glob("*.vcvm"))
print(infiles)
for infile in infiles:
    outfile = outpath / infile.name
    print(outfile)
    with open(infile,"r",encoding="utf-8") as f:
        data = f.read()
    jdata = json.loads(data)
    jd = copy.deepcopy(jdata)
    for n in range(32):
        jd["data"][f"progSteps{n}"] = [12]
    for param in jd["params"]:
        if param["id"] == 16:
            param["value"] = 12.0
    with open(outfile,"w",encoding="utf-8") as f:
        f.write(json.dumps(jd,indent=True))
