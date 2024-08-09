import pathlib,json,argparse,itertools

home = pathlib.Path.home()
_DEFAULT_OUTPUT_DIR = home / "AppData" / "Local" / "Rack2" / "presets" / "Voxglitch" / "autobreak"

print("_DEFAULT_OUTPUT_DIR, _DEFAULT_OUTPUT_DIR.is_dir():",_DEFAULT_OUTPUT_DIR, _DEFAULT_OUTPUT_DIR.is_dir())


# {{{1 json_template
json_template = {
  "plugin": "voxglitch",
  "model": "autobreak",
  "version": "2.28.0",
  "params": [
    {
      "value": 0.0,
      "id": 0
    },
    {
      "value": 1.0,
      "id": 1
    }
  ],
  "data": {
    "loaded_sample_path_1": "__placeholder_text__",
    "loaded_sample_path_2": "__placeholder_text__",
    "loaded_sample_path_3": "__placeholder_text__",
    "loaded_sample_path_4": "__placeholder_text__",
    "loaded_sample_path_5": "__placeholder_text__"
  }
}

# }}}1

# print(json.dumps(json_template,indent=True))

def batch5(iterable):
    iterator = iter(iterable)
    while batch := tuple(itertools.islice(iterator,5)):
        yield batch


def main(p,out):
    path = pathlib.Path(p)
    output = pathlib.Path(out)
    output_subdir = output / (path.parent.name + "_" + path.name)
    output_subdir.mkdir(exist_ok=True)
    for n,each5 in enumerate(batch5(list(path.glob("*.wav")))):
        if len(each5) < 5:
            continue
        output_filename = output_subdir / f"{path.name}_{n}.vcvm"
        js = json_template.copy()
        js["data"]["loaded_sample_path_1"] = str(each5[0])
        js["data"]["loaded_sample_path_2"] = str(each5[1])
        js["data"]["loaded_sample_path_3"] = str(each5[2])
        js["data"]["loaded_sample_path_4"] = str(each5[3])
        js["data"]["loaded_sample_path_5"] = str(each5[4])
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
