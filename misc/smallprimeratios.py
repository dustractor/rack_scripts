import decimal,textwrap,pathlib,itertools,json,copy


# {{{1 json template
jtemplate = {
    "plugin": "voxglitch",
    "model": "onezero",
    "version": "2.32.0",
    "params": [
        { "value": 0.0, "id": 0 },
        { "value": 0.0, "id": 1 },
        { "value": 0.0, "id": 2 },
        { "value": 1.0, "id": 3 }
    ],
    "data": { "path": "placeholder text"
    } }
# }}}1

# primes under 100
smallprimes = [
    2, 3, 5, 7, 11, 13, 17, 19,
    23, 29, 31, 37, 41, 43, 47,
    53, 59, 61, 67, 71, 73, 79,
    83, 89, 97]

_PREC = 2**12
_W = 16

decimal.getcontext().prec = _PREC
D = decimal.Decimal

home = pathlib.Path.home()
docs = home / "Documents"
seqdir = docs / "Github" / "numbersequences"
targetdir_ab = seqdir / "a_div_b"
targetdir_ba = seqdir / "b_div_a"
targetdir_ab.mkdir(exist_ok=True)
targetdir_ba.mkdir(exist_ok=True)
rackdir = home / "AppData" / "Local" / "Rack2"
onezerodir = rackdir / "presets" / "voxglitch" / "onezero"
presetdir_ab = onezerodir / "a_div_b"
presetdir_ba = onezerodir / "b_div_a"
presetdir_ab.mkdir(exist_ok=True)
presetdir_ba.mkdir(exist_ok=True)

pairs = list(itertools.combinations(smallprimes,r=2))

def process(a,b,targetdir,presetdir):
    v = D(a) / D(b)
    s = str(v)
    ss = s.partition(".")[2]
    lx = []
    for c in ss:
        lx.append("01"[int(c) % 2 != 0])
    d = "".join(lx)
    dd = textwrap.wrap(d,width=_W)
    dd = [ln for ln in dd if len(ln)==_W]
    uniq = list(dict.fromkeys(dd))
    if len(uniq) > 1:
        dd = uniq
    else:
        return
    outputname = f"a{a}_div_b{b}x{_W}.txt"
    outputpath = targetdir / outputname
    with open(outputpath,"w") as f:
        for line in dd:
            if len(line) == _W:
                f.write(line + "\n")
    jdata = copy.deepcopy(jtemplate)
    jdata["data"]["path"] = str(outputpath)
    presetname = f"a{a}_div_b{b}x{_W}.vcvm"
    presetpath = presetdir / presetname
    with open(presetpath,"w",encoding="utf-8") as f:
        f.write(json.dumps(jdata,indent=True))


for a,b in pairs:
    process(a,b,targetdir_ab,presetdir_ab)
    process(b,a,targetdir_ba,presetdir_ba)


