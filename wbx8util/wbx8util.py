import argparse,sys,json,pathlib,math,pyperclip

# {{{1 x8template
x8template = """{
  "plugin": "voxglitch",
  "model": "samplerx8",
  "version": "2.39.0",
  "params": [
    {
      "value": 1.0,
      "id": 0
    },
    {
      "value": 1.0,
      "id": 1
    },
    {
      "value": 1.0,
      "id": 2
    },
    {
      "value": 1.0,
      "id": 3
    },
    {
      "value": 1.0,
      "id": 4
    },
    {
      "value": 1.0,
      "id": 5
    },
    {
      "value": 1.0,
      "id": 6
    },
    {
      "value": 1.0,
      "id": 7
    },
    {
      "value": 0.0,
      "id": 8
    },
    {
      "value": 0.0,
      "id": 9
    },
    {
      "value": 0.0,
      "id": 10
    },
    {
      "value": 0.0,
      "id": 11
    },
    {
      "value": 0.0,
      "id": 12
    },
    {
      "value": 0.0,
      "id": 13
    },
    {
      "value": 0.0,
      "id": 14
    },
    {
      "value": 0.0,
      "id": 15
    },
    {
      "value": 1.0,
      "id": 16
    },
    {
      "value": 1.0,
      "id": 17
    },
    {
      "value": 1.0,
      "id": 18
    },
    {
      "value": 1.0,
      "id": 19
    },
    {
      "value": 1.0,
      "id": 20
    },
    {
      "value": 1.0,
      "id": 21
    },
    {
      "value": 1.0,
      "id": 22
    },
    {
      "value": 1.0,
      "id": 23
    }
  ],
  "data": {
    "loaded_sample_path_1": "",
    "loaded_sample_path_2": "",
    "loaded_sample_path_3": "",
    "loaded_sample_path_4": "",
    "loaded_sample_path_5": "",
    "loaded_sample_path_6": "",
    "loaded_sample_path_7": "",
    "loaded_sample_path_8": "",
    "interpolation": 1,
    "samples_root_dir": ""
  }
}"""
# }}}1

x8jdata = json.loads(x8template)

storagepath = pathlib.Path(__file__).parent/"storage.json"

storagedict = None

blank_storagedict = dict(
    p1="", p2="", p3="", p4="",
    p5="", p6="", p7="", p8="")

def write_storage(storage):
    with open(storagepath,"w",encoding="utf-8") as f:
        f.write(json.dumps(storage,indent=True))

def read_storage():
    with open(storagepath,"r",encoding="utf-8") as f:
        return json.loads(f.read())

if not storagepath.exists():
    storagedict = blank_storagedict
    write_storage(storagedict)
else:
    storagedict = read_storage()

print("storagedict:",storagedict)

def getslot():
    args = argparse.ArgumentParser()
    args.add_argument("--slot",type=int,default=1)
    ns = args.parse_args()
    return ns.slot

def getsample():
    clipboard = pyperclip.paste()
    print("clipboard:",clipboard)
    jdata = None
    val = 0.0
    if not (clipboard[0] == "{" and clipboard[-1] == "}"):
        print("doesn't look like json data")
        return -1
    try:
        jdata = json.loads(clipboard)
    except:
        print("error loading json")
        return -1
    if not jdata:
        print("nothing loaded")
        return -1
    pathstr = jdata["data"]["path"]
    if not pathstr:
        print("path string empty")
        return -1
    path = pathlib.Path(pathstr)
    if not path.is_dir():
        print("invalid root dir:",path)
        return -1
    for param in jdata["params"]:
        if param["id"] == 0:
            val = param["value"]
    wavs = list(path.glob("*.wav"))
    index = math.floor(val*len(wavs))
    if val == 1.0:
        index = index-1
    wav = wavs[index]
    return wav

slot = getslot()
sample = getsample()
print("slot,sample:",slot,sample)
if sample == -1:
    print("no sample returned")
    sys.exit()

if not ((slot >= 1) and (slot <= 8)):
    print("bad slot")
    sys.exit()

storagedict[f"p{slot}"] = str(sample)
print("storagedict:",storagedict)
write_storage(storagedict)

for n in range(1,9):
    x8jdata["data"][f"loaded_sample_path_{n}"] = storagedict[f"p{n}"]
x8jdata["data"]["samples_root_dir"] = "d:\\zSamples"

pyperclip.copy(json.dumps(x8jdata,indent=True))

