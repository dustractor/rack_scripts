import pathlib,json,decimal,textwrap
decimal.getcontext().prec = 32*17
D = decimal.Decimal
outdir = pathlib.Path.home()/"AppData"/"Local"/"Rack2"/"presets"/"SickoCV"/"TrigSeq8x"

jsontemplate = outdir/"Untitled.vcvm"


with open(jsontemplate,"r",encoding="utf-8") as f:
    jdata = json.loads(f.read())

def mm(k):
    return (D(k)+((D(k)*D(k))+D(4)).sqrt())/D(2)

nums = list(map(mm,range(25,33)))
print("nums:",nums)

def numtobits(num):
    s = str(num).partition(".")[2]
    s = "".join(["01"[int(c)%2==0] for c in s])
    return s


bits = numtobits(nums[0])
w = textwrap.wrap(bits,width=16)
bitls = [textwrap.wrap(numtobits(num),width=16) for num in nums]
for t in range(8):
    jdata["data"][f"wSeq_t{t}"] = [int(c) for c in bitls[t][0]]
for p in range(32):
    for t in range(8):
        jdata["data"][f"p{p}t{t}"] = [int(c) for c in bitls[t][p]]

with open(outdir/"metals24-32.vcvm","w",encoding="utf-8") as f:
    f.write(json.dumps(jdata,indent=True))


