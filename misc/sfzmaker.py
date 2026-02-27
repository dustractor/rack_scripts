import pathlib,argparse,json,subprocess

args = argparse.ArgumentParser()
args.add_argument("--samples-dir")
args.add_argument("--output-dir")
args.add_argument("--mono-strategy",choices=["downmix","left","right"],default="right")
args.add_argument("--ffmpeg-path",default="C:\\Windows\\ffmpeg.exe")
ns = args.parse_args()

print(ns)

samples_list = list(pathlib.Path(ns.samples_dir).glob("*.wav"))
print("samples_list:",samples_list)

output_dir = pathlib.Path(ns.output_dir).resolve()
print("output_dir:",output_dir)
output_dir.mkdir(exist_ok=True)

def monoize(sample_path,output_dir,output_name,mono_strategy):
    if mono_strategy == "downmix":
        cmd = [ns.ffmpeg_path, "-i", str(sample_path),"-ac","1",output_dir/output_name]
    elif mono_strategy == "left":
        cmd = [ns.ffmpeg_path, "-i", str(sample_path),"-af","pan=mono|c0=FL",output_dir/output_name]
    elif mono_strategy == "right":
        cmd = [ns.ffmpeg_path, "-i", str(sample_path),"-af","pan=mono|c0=FR",output_dir/output_name]

    print("cmd:",cmd)
    subprocess.run(cmd)

sfzdata = [
    "<control>",
    "default_path="+str(output_dir),
    "<global>",
    "loop_mode=oneshot"
]
for n,sample in enumerate(samples_list[:128]):
    output_name = f"{output_dir.name}_{n:03d}.wav"
    monoize(sample,output_dir,output_name,ns.mono_strategy)
    sfzdata.append(f"<region>key={n} sample={output_name}")
sfzpath = pathlib.Path(".").resolve() / (output_dir.name + ".sfz")
print("sfzpath:",sfzpath)
with open(sfzpath,"w") as f:
    f.write("\n".join(sfzdata))

