import sqlite3
import pathlib
import wave
import os
import argparse
import shutil
_DEFAULT_WAVDIR = "d:\\zSamples"
_DEFAULT_DBFILE = str(pathlib.Path.home() / "Desktop" / "wave_info.db")
_DEFAULT_TARGET = str(pathlib.Path.home() / "Desktop" / "wave_info_target")
args = argparse.ArgumentParser()
args.add_argument("--wavdir",default=_DEFAULT_WAVDIR)
args.add_argument("--dbfile",default=_DEFAULT_DBFILE)
args.add_argument("--scan",action="store_true")
args.add_argument("--dump",action="store_true")
args.add_argument("--copy",action="store_true")
args.add_argument("--target",default=_DEFAULT_TARGET)
args.add_argument("--tempo",type=int,default=120)
args.add_argument("--bars",type=int,default=4)
args.add_argument("--dry-run",action="store_true")
args.add_argument("--t-epsilon",type=float,default=0.1)
ns = args.parse_args()


class WaveLibrarian(sqlite3.Connection):
    def __init__(self,name,**kwargs):
        super().__init__(name,**kwargs)
        self.cu = self.cursor()
        self.cu.row_factory = lambda c,r:r[0]
        self.executescript(
            """
            create table if not exists wavs (
            id integer primary key,
            path text,
            nchannels integer,
            bitdepth integer,
            framerate integer,
            nframes integer,
            seconds real,
            unique (path) on conflict replace);

            create table if not exists errors (
            id integer primary key,
            path text,
            unique (path) on conflict replace);

            """)
        self.commit()
    def insert(self,wavpath):
        print("--> wavpath:",wavpath)
        path = str(wavpath)
        try:
            with wave.open(path,"rb") as wf:
                nchannels = wf.getnchannels()
                bitdepth = wf.getsampwidth() * 8
                framerate = wf.getframerate()
                nframes = wf.getnframes()
                seconds = nframes / framerate
            self.execute("insert into wavs (path,nchannels,bitdepth,framerate,nframes,seconds) values (?,?,?,?,?,?)",
                         (path,nchannels,bitdepth,framerate,nframes,seconds))
        except:
            self.execute("insert into errors (path) values (?)",(path,))

    def scan(self,folder):
        for r,ds,fs in os.walk(folder):
            root = pathlib.Path(r)
            for f in fs:
                wp = root/f
                if wp.suffix.lower() == ".wav":
                    self.insert(wp)
        self.commit()


wavdir = pathlib.Path(ns.wavdir)

dbfile = pathlib.Path(ns.dbfile)

class WaveLibrary:
    _handle = None
    @property
    def cx(self):
        if not self._handle:
            self._handle = sqlite3.connect(
                dbfile,
                factory=WaveLibrarian)
            return self._handle

db = WaveLibrary()

cx = db.cx

if ns.scan:
    print("scanning",ns.wavdir)
    cx.scan(wavdir)

if ns.dump:
    list(map(print,cx.iterdump()))

if ns.copy:
    print("ns.tempo:",ns.tempo)
    print("ns.bars:",ns.bars)
    print("ns.target:",ns.target)
    print("ns.t_epsilon:",ns.t_epsilon)
    target = pathlib.Path(ns.target)
    target.mkdir(exist_ok=True)

    desired_length = 60 / ns.tempo * 4 * ns.bars
    print("desired_length:",desired_length)
    min_ = desired_length - ns.t_epsilon
    max_ = desired_length + ns.t_epsilon
    if ns.dry_run:
        q = cx.cu.execute(f"select count(*) from wavs where seconds between {min_} and {max_}").fetchone()
        print("found:",q)
    else:
        for f in cx.cu.execute(f"select path from wavs where seconds between {min_} and {max_}"):
            shutil.copy(f,target)

