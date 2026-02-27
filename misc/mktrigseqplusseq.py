import json,copy,textwrap,decimal,pathlib

p = pathlib.Path.home()/"AppData"/"Local"/"Rack2"/"presets"/"SickoCV"/"TrigSeqPlus"

with open(p/"auto.vcvm","r",encoding="utf-8") as f:
    jdata = json.loads(f.read())



decimal.getcontext().prec = 16*33 #leave some extra
D = decimal.Decimal
vals = dict(
    metal1=(D(1)+D(5).sqrt())/D(2),
    metal2=(D(2)+D(8).sqrt())/D(2),
    metal3=(D(3)+D(13).sqrt())/D(2),
    metal4=(D(4)+D(20).sqrt())/D(2),
    metal5=(D(5)+D(29).sqrt())/D(2),
    metal6=(D(6)+D(40).sqrt())/D(2),
    metal7=(D(7)+D(53).sqrt())/D(2),
    metal8=(D(8)+D(68).sqrt())/D(2),
    metal9=(D(9)+D(85).sqrt())/D(2),
    metal10=(D(10)+D(104).sqrt())/D(2)
)

for k in vals:
    jd = copy.deepcopy(jdata)
    s = str(vals[k]).partition(".")[2]
    s = "".join(["01"[int(c)%2==0] for c in s])
    s = textwrap.wrap(s,width=16)
    jd["data"]["wSeq"] = list(map(int,s[0]))
    for n in range(32):
        jd["data"][f"prog{n}"] = list(map(int,s[n]))
    out = p/f"{k}.vcvm"
    with open(out,"w",encoding="utf-8") as f:
        f.write(json.dumps(jd,indent=True))

