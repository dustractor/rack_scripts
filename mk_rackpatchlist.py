import pathlib,datetime
rackdir = pathlib.Path.home()/"AppData"/"Local"/"Rack2"
outfile = pathlib.Path.home()/"Desktop"/"rackpatches.htm"

patchdir = rackdir/"patches"


patchdata = []
for p in patchdir.glob("*.vcv"):
    patchdata.append([p.stat().st_mtime,p])

with open(outfile,"w",encoding="utf8") as f:
    f.write(
"""<html>
    <head>
        <title>Rack Patches</title>
    </head>
    <body>
        <ol>
""")
    for t,p in sorted(patchdata):
        date = datetime.datetime.fromtimestamp(t).strftime("%Y-%b-%d")
        path = p.resolve().as_uri()
        name = p.name
        f.write(f"<li><a href=\"{path}\">{name}</a> <small>{date}</small></li>")
    f.write(
        """
        </ol>
    </body>
</html>
""")
