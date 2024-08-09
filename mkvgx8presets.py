import pathlib,json,argparse,itertools

home = pathlib.Path.home()
_DEFAULT_OUTPUT_DIR = home / "AppData" / "Local" / "Rack2" / "presets" / "Voxglitch" / "samplerx8"

print("_DEFAULT_OUTPUT_DIR, _DEFAULT_OUTPUT_DIR.is_dir():",_DEFAULT_OUTPUT_DIR, _DEFAULT_OUTPUT_DIR.is_dir())


# {{{1 json_template
json_template = {
  "plugin": "voxglitch",
  "model": "samplerx8",
  "version": "2.28.0",
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
    "loaded_sample_path_1": "__placeholder_text__",
    "loaded_sample_path_2": "__placeholder_text__",
    "loaded_sample_path_3": "__placeholder_text__",
    "loaded_sample_path_4": "__placeholder_text__",
    "loaded_sample_path_5": "__placeholder_text__",
    "loaded_sample_path_6": "__placeholder_text__",
    "loaded_sample_path_7": "__placeholder_text__",
    "loaded_sample_path_8": "__placeholder_text__",
    "interpolation": 1,
    "samples_root_dir": ""
  }
}

# }}}1

# print(json.dumps(json_template,indent=True))

def batch8(iterable):
    iterator = iter(iterable)
    while batch := tuple(itertools.islice(iterator,8)):
        yield batch


def main(p,out):
    path = pathlib.Path(p)
    output = pathlib.Path(out)
    output_subdir = output / path.name
    output_subdir.mkdir(exist_ok=True)
    for n,each8 in enumerate(batch8(list(path.glob("*.wav")))):
        if len(each8) < 8:
            continue
        output_filename = output_subdir / f"{path.name}_{n}.vcvm"
        js = json_template.copy()
        js["data"]["loaded_sample_path_1"] = str(each8[0])
        js["data"]["loaded_sample_path_2"] = str(each8[1])
        js["data"]["loaded_sample_path_3"] = str(each8[2])
        js["data"]["loaded_sample_path_4"] = str(each8[3])
        js["data"]["loaded_sample_path_5"] = str(each8[4])
        js["data"]["loaded_sample_path_6"] = str(each8[5])
        js["data"]["loaded_sample_path_7"] = str(each8[6])
        js["data"]["loaded_sample_path_8"] = str(each8[7])
        with open(output_filename,"w") as f:
            f.write(json.dumps(js,indent=True))


if __name__ == "__main__":
    args = argparse.ArgumentParser()
    args.add_argument("--path")
    args.add_argument("--output",default=str(_DEFAULT_OUTPUT_DIR))
    ns = args.parse_args()
    if ns.path:
        main(ns.path,ns.output)
    else:
        print("supply a path with --path argument")
