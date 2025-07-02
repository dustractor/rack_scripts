import pathlib
import json
import zstandard
import random
import math
import shutil

outdir = pathlib.Path.home()/"Desktop"/"wbsel"

dataerror = json.dumps(dict(modules=[dict(plugin="ERROR",model="ERROR")]))

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

def getwavbanks(modules):
    for m in modules:
        if m["plugin"] == "voxglitch" and m["model"] == "wavbank":
            yield m
def getsample(module):
    val = None
    path = None
    params = module["params"]
    for param in params:
        if param["id"] == 0:
            val = param["value"]
    path = module["data"]["path"]
    if val and path:
        p = pathlib.Path(path)
        if not p.exists():
            return
        wavs = list(pathlib.Path(path).glob("*.wav"))
        path_len = len(wavs)
        i = math.floor(val*path_len)
        if val == 1.0:
            i = i-1
        return wavs[i]


for patch in patches:
    print("patch:",patch)
    jdata = getpatchjson(patch)
    modules = jdata["modules"]
    for wb in getwavbanks(modules):
        sample = getsample(wb)
        if sample and sample.exists():
            src = sample
            dest = outdir / sample.name
            print("src:",src)
            print("dest:",dest)
            shutil.copy(src,dest)


