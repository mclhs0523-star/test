# 사용법: python3 -I fonts.py 작업폴더 [스킬폴더]
# 나눔명조(본문)와 돋움(라벨)을 작업폴더/fonts/ 에 준비한다.
# 찾는 순서: 스킬폴더/assets/fonts → 첨부 TTF → 첨부 ZIP(인수인계 zip 포함) 안의 TTF → 첨부 나눔 설치 파일(실행하지 않고 풀기) → 시스템 글꼴.
import sys, os, glob, struct, lzma, zlib, subprocess, shutil, zipfile
from fontTools.ttLib import TTFont

out = os.path.join(sys.argv[1], "fonts"); os.makedirs(out, exist_ok=True)
WANT = {"NanumMyeongjo": "NanumMyeongjo.ttf", "NanumMyeongjoBold": "NanumMyeongjoBold.ttf", "Dotum": "Dotum.ttf"}

def psname(path):
    try:
        return TTFont(path, fontNumber=0)["name"].getDebugName(6)
    except Exception:
        return None

def take(path):
    n = psname(path)
    if n in WANT and not os.path.exists(os.path.join(out, WANT[n])):
        shutil.copy(path, os.path.join(out, WANT[n]))

def nsis_extract(exe, dest):
    d = open(exe, "rb").read()
    i = d.find(b"\xef\xbe\xad\xdeNullsoftInst")
    if i < 0: return
    data = d[i - 4 + 28:]; pos = 0; n = 0
    while pos + 4 <= len(data):
        l, = struct.unpack("<I", data[pos:pos + 4]); comp = l & 0x80000000; l &= 0x7fffffff
        if l == 0 or pos + 4 + l > len(data): break
        blk = data[pos + 4:pos + 4 + l]; pos += 4 + l
        o = None
        if not comp: o = blk
        elif blk[0] == 0x5d:
            p = blk[0]; ds = struct.unpack("<I", blk[1:5])[0]
            try:
                o = lzma.LZMADecompressor(format=lzma.FORMAT_RAW, filters=[{"id": lzma.FILTER_LZMA1, "lc": p % 9, "lp": (p // 9) % 5, "pb": p // 45, "dict_size": ds}]).decompress(blk[5:])
            except Exception: o = None
        else:
            try: o = zlib.decompressobj(-15).decompress(blk)
            except Exception: o = None
        if o and o[:4] == b"\x00\x01\x00\x00":
            fp = os.path.join(dest, f"x{n:02d}.ttf"); open(fp, "wb").write(o); n += 1

if len(sys.argv) > 2:
    for f in glob.glob(os.path.join(sys.argv[2], "assets", "fonts", "*.ttf")): take(f)
up = "/mnt/user-data/uploads"
for f in glob.glob(up + "/**/*", recursive=True):
    if os.path.isfile(f) and f.lower().endswith((".ttf", ".otf")): take(f)
tmp = os.path.join(sys.argv[1], "_nanum_extract"); os.makedirs(tmp, exist_ok=True)
for f in glob.glob(up + "/**/*", recursive=True):
    if os.path.isfile(f) and open(f, "rb").read(2) == b"MZ":
        nsis_extract(f, tmp)
for f in glob.glob(up + "/**/*", recursive=True):
    if os.path.isfile(f) and zipfile.is_zipfile(f):
        with zipfile.ZipFile(f) as z:
            for k, m in enumerate(z.namelist()):
                if m.lower().endswith(".ttf"):
                    fp = os.path.join(tmp, f"z{k:03d}.ttf"); open(fp, "wb").write(z.read(m))
for f in glob.glob(tmp + "/*.ttf"): take(f)
try:
    for line in subprocess.run(["fc-list", ":", "file"], capture_output=True, text=True).stdout.splitlines():
        p = line.split(":")[0]
        if "anum" in p and p.endswith(".ttf"): take(p)
except Exception: pass
miss = [v for v in WANT.values() if not os.path.exists(os.path.join(out, v))]
print("MISSING" if miss else "OK", miss)
