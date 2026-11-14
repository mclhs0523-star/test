# 학습지세트 조판 도구 (성공의 신화 양식)
# 사용법
#   python3 -I sheet.py makeone 작업폴더/content.json 작업폴더
#       → 작업폴더/out/{title}_학습지세트.pdf, .hwpx  (HWPX 안에 content.json을 함께 넣어 둔다)
#   python3 -I sheet.py bind 작업폴더 --title "책 제목" 파일1 파일2 …   (파일: .hwpx 또는 content.json, 적은 순서대로 엮음)
#       → 작업폴더/out/{책 제목}_본책.pdf, .hwpx / {책 제목}_답지.pdf, .hwpx
#   python3 -I sheet.py extract 파일.hwpx 출력.txt        (HWPX 본문 글자를 꺼냄. content.json이 없는 HWPX를 되살릴 때)
#   python3 -I sheet.py textdump 작업폴더/content.json    (맞춤법 검사용: 지문을 뺀 모든 글을 위치 표시와 함께 출력)
#   python3 -I sheet.py check 작업폴더/content.json       (검증만)
# 작업폴더에 fonts/NanumMyeongjo.ttf, fonts/NanumMyeongjoBold.ttf, fonts/Dotum.ttf, logo.png 가 있어야 한다(fonts.py가 준비).
import sys, os, re, io, json, html, zipfile
from collections import Counter
from xml.sax.saxutils import escape

CIRC = "①②③④⑤"
CIRC20 = "①②③④⑤⑥⑦⑧⑨⑩⑪⑫⑬⑭⑮⑯⑰⑱⑲⑳"
STEPS = [(1, "직접 정리하기"), (2, "OX 정리와 빈칸 넣기"), (3, "초고난도 변형문제")]
JSON_IN_HWPX = "학습지세트/content.json"
WD = FD = LOGO = None
LW = LH = 0
LF = {}

def setup(wd):
    global WD, FD, LOGO, LW, LH, LF
    from PIL import Image
    WD = os.path.abspath(wd); FD = os.path.join(WD, "fonts") + "/"; LOGO = os.path.join(WD, "logo.png")
    for f in ("NanumMyeongjo.ttf", "NanumMyeongjoBold.ttf", "Dotum.ttf"):
        if not os.path.exists(FD + f): sys.exit(f"글꼴 없음: {FD + f} (fonts.py를 먼저 실행)")
    if not os.path.exists(LOGO): sys.exit(f"로고 없음: {LOGO}")
    LW, LH = Image.open(LOGO).size
    LF = {"R": FD + "Dotum.ttf", "B": FD + "Dotum.ttf"}
    os.makedirs(os.path.join(WD, "out"), exist_ok=True)

def safe(s): return re.sub(r"[\\/:*?\"<>|\s]+", "", s) or "학습지"

# ───────── 검증 ─────────
def validate(C):
    P_ = C["passages"]; Q_ = C["questions"]; err = []
    if not P_: err.append("지문이 없음")
    if len(Q_) != 20: err.append(f"문항 수 {len(Q_)} (20이어야 함)")
    if abs(sum(q["pts"] for q in Q_) - 100) > 1e-6: err.append(f"배점 합 {sum(q['pts'] for q in Q_)} (100이어야 함)")
    cnt = Counter(q["ans"] for q in Q_)
    if any(cnt[i] != 4 for i in range(1, 6)): err.append(f"정답 분포 {dict(cnt)} (①~⑤ 각 4개)")
    for i, q in enumerate(Q_, 1):
        if len(q["opts"]) != 5: err.append(f"{i}번 선지 {len(q['opts'])}개")
    if len(C["blank_answers"]) > 20: err.append("빈칸은 20개 이하")
    nb = sum(len(re.findall(r"\( [①-⑳] \)", b["text"])) for b in C["blanks"])
    if nb != len(C["blank_answers"]): err.append(f"빈칸 표시 {nb}개 ≠ 정답 {len(C['blank_answers'])}개")
    return err

def setline(C):
    P_ = C["passages"]
    if len(P_) > 1:
        labs = [f"({p['label']})" for p in P_]
        rng = f"{labs[0]}와 {labs[1]}" if len(labs) == 2 else f"{labs[0]}~{labs[-1]}"
        return f"[1~20] 다음 {rng}를 읽고 물음에 답하시오."
    return "[1~20] 다음 글을 읽고 물음에 답하시오."

# ═════════════════════════ PDF ═════════════════════════
def inl(s):
    s = html.escape(s, quote=False)
    return s.replace("[u]", "<u>").replace("[/u]", "</u>").replace("[b]", "<b>").replace("[/b]", "</b>")

def blanks(s):
    return re.sub(r"\( ([①-⑳]) \)", r'<span class="blank">\1</span>', inl(s))

def h_step_head(num, title):
    return f'<div class="stephead"><div class="stepnum"><span>Step</span>{num}</div><div class="steptitle"><h2>{title}</h2></div></div>'

def boxhtml(b):
    if b["kind"] == "text":
        inner = "".join(f"<p>{inl(p)}</p>" for p in b["paras"])
    elif b["kind"] == "list":
        inner = "".join(f'<p class="li"><span class="lk">{k}.</span>{inl(t)}</p>' for k, t in b["items"])
    else:
        inner = (f'<p>{inl(b["intro"])}</p>' if b.get("intro") else "") + '<table class="dt"><tr>' + "".join(f"<th>{h}</th>" for h in b["head"]) + "</tr>"
        for r in b["rows"]:
            inner += "<tr>" + "".join(f"<td>{inl(c)}</td>" for c in r) + "</tr>"
        inner += "</table>"
        if b.get("note"): inner += f'<p class="note">{inl(b["note"])}</p>'
    return f'<div class="bogi"><div class="bl"><span>&lt;보기&gt;</span></div>{inner}</div>'

def head_html(head):
    return f'<div class="sethead"><span class="sn">{head["no"]}</span><span class="st">{html.escape(head["title"])}</span></div>'

def set_html(C, head=None):
    """학습지 한 세트의 (본문 HTML, 정답과 해설 HTML)."""
    P_, Q_ = C["passages"], C["questions"]; multi = len(P_) > 1
    SH = head_html(head) if head else ""
    parts = [f'<section class="step1{" withhead" if head else ""}">{SH}{h_step_head(*STEPS[0])}</section>']
    rows, cur = [], None
    for i, o in enumerate(C["ox"], 1):
        if o["group"] != cur:
            if cur is not None: rows.append('</table><table class="oxt">')
            rows.append(f'<tr class="grp"><td colspan="3">{o["group"]}</td></tr>'); cur = o["group"]
        rows.append(f'<tr><td class="n">{i}</td><td>{inl(o["text"])}</td><td class="ox">O<i></i>X</td></tr>')
    bl = "".join(f'<div class="bpara"><div class="bk">{b["group"]}</div><p>{blanks(b["text"])}</p></div>' for b in C["blanks"])
    parts.append(f'''<section class="sec">{h_step_head(*STEPS[1])}
<table class="oxt">{"".join(rows)}</table>
<div class="sub2">빈칸 넣기</div><p class="inst">빈칸에 들어갈 말을 지문에서 찾아 쓰세요.</p>{bl}</section>''')
    q = [f'<section class="sec">{h_step_head(*STEPS[2])}<div class="two">', f'<p class="qset">{setline(C)}</p>']
    for p in P_:
        if multi: q.append(f'<p class="plabel">({p["label"]})</p>')
        for para in p["paras"]: q.append(f'<p class="pp">{inl(para)}</p>')
    q.append('<div class="qgap"></div>')
    for n, x in enumerate(Q_, 1):
        q.append(f'<div class="q"><p class="stem"><span class="qn">{n}.</span>{inl(x["stem"])} [{x["pts"]:.1f}점]</p>')
        if x.get("box"): q.append(boxhtml(x["box"]))
        short = all(len(o) <= 12 for o in x["opts"])
        q.append('<div class="opts%s">' % (" short" if short else ""))
        for j, o in enumerate(x["opts"]): q.append(f'<p class="op"><span class="c">{CIRC[j]}</span>{inl(o)}</p>')
        q.append("</div></div>")
    q.append("</div></section>")
    parts.append("\n".join(q))
    OX = C["ox"]; BA = C["blank_answers"]
    oxg = "".join(f'<td><b>{i}</b> {o["ans"]}</td>' + ("</tr><tr>" if i % 7 == 0 and i < len(OX) else "") for i, o in enumerate(OX, 1))
    bg = "".join(f'<td><b>{CIRC20[i]}</b> {a}</td>' + ("</tr><tr>" if (i + 1) % 4 == 0 and i + 1 < len(BA) else "") for i, a in enumerate(BA))
    qg = ""
    for h in (range(0, 10), range(10, 20)):
        qg += "<tr>" + "".join(f"<th>{i+1}</th>" for i in h) + "</tr><tr>" + "".join(f"<td>{CIRC[Q_[i]['ans']-1]}</td>" for i in h) + "</tr>"
    oxexp = "".join(f'<p class="oxe"><b>{i}</b> {o["ans"]} <span>{inl(o["why"])}</span></p>' for i, o in enumerate(OX, 1) if o["ans"] == "X")
    ex = "".join(f'<div class="ex"><p class="exh"><span class="qn">{n}.</span>정답 {CIRC[x["ans"]-1]}</p><p>{inl(x["exp"])}</p></div>' for n, x in enumerate(Q_, 1))
    ans = f'''<section class="sec">{SH}<div class="anshead"><h2>정답과 해설</h2></div><div class="two">
<p class="ah">Step 2 OX</p><table class="ag"><tr>{oxg}</tr></table><p class="ah2">X 진술 바로잡기</p>{oxexp}
<p class="ah">Step 2 빈칸</p><table class="ag bg"><tr>{bg}</tr></table>
<p class="ah">Step 3 빠른 정답</p><table class="qg">{qg}</table>
<p class="ah">Step 3 해설</p>{ex}</div></section>'''
    return "\n".join(parts), ans

def toc_html(title, entries, kind):
    """차례 쪽. entries: [{no, title, page, steps:[(이름, 쪽)…]}]"""
    rows = []
    for e in entries:
        rows.append(f'<div class="trow"><span class="tn">{e["no"]}</span><span class="tt">{html.escape(e["title"])}</span>'
                    f'<span class="tdots"></span><span class="tp">{e["page"]}</span></div>')
        if e.get("steps"):
            rows.append('<div class="tsub">' + '<span class="tsep">·</span>'.join(f'{n} <b>{p}쪽</b>' for n, p in e["steps"]) + '</div>')
    sub = "본책" if kind == "body" else "정답과 해설"
    return (f'<section class="toc"><div class="tochead"><h1>차례</h1><p>{html.escape(title)} <span>{sub}</span></p></div>'
            f'<div class="tlist">{"".join(rows)}</div></section>')

def css(body_text):
    from fontTools.ttLib import TTFont as _TT
    _dc = _TT(LF["R"]).getBestCmap()
    _miss = sorted({ord(ch) for ch in html.unescape(re.sub(r"<[^>]+>", " ", body_text)) if ord(ch) not in _dc and not ch.isspace()})
    UR = ",".join(f"U+{x:04X}" for x in _miss) or "U+FFFF"
    return f'''
@font-face{{font-family:"Body";font-weight:400;src:url("file://{FD}NanumMyeongjo.ttf");}}
@font-face{{font-family:"Body";font-weight:700;src:url("file://{FD}NanumMyeongjoBold.ttf");}}
@font-face{{font-family:"Lab";font-weight:400;src:url("file://{LF['R']}");}}
@font-face{{font-family:"Lab";font-weight:700;src:url("file://{LF['B']}");}}
@font-face{{font-family:"Lab";font-weight:400;src:url("file://{FD}NanumMyeongjo.ttf");unicode-range:{UR};}}
@font-face{{font-family:"Lab";font-weight:700;src:url("file://{FD}NanumMyeongjo.ttf");unicode-range:{UR};}}
@page{{size:A4;margin:24mm 15mm 18mm 15mm;}}
*{{box-sizing:border-box;font-synthesis:none;}}
html{{-webkit-print-color-adjust:exact;}}
body{{margin:0;font-family:"Body",serif;font-size:9.3pt;line-height:1.7;color:#000;word-break:normal;line-break:strict;}}
p{{margin:0;}}
u{{text-underline-offset:2.5px;text-decoration-thickness:.6pt;}}
.sec{{break-before:page;}}
.qgap{{height:4mm;}}
.two{{column-count:2;column-gap:9mm;column-rule:.5pt solid #000;column-fill:auto;}}
.qset{{font-family:"Lab";font-weight:700;font-size:10pt;margin-bottom:2mm;}}
.plabel{{font-family:"Lab";font-weight:700;margin:3.5mm 0 .5mm;}}
.pp{{text-indent:1em;text-align:justify;}}
.stephead{{display:flex;align-items:stretch;border-bottom:2.5pt solid #000;margin-bottom:6mm;}}
.stepnum{{background:#000;color:#fff;font-family:"Lab";font-weight:700;font-size:34pt;line-height:1;width:24mm;display:flex;flex-direction:column;justify-content:flex-end;padding:2.5mm 3mm;}}
.stepnum span{{font-size:9pt;font-weight:400;margin-bottom:1.5mm;}}
.steptitle{{padding:0 0 3mm 5mm;display:flex;flex-direction:column;justify-content:flex-end;}}
.steptitle h2{{font-family:"Lab";font-size:18pt;margin:0;line-height:1.2;}}
.step1{{height:255mm;}}
.oxt{{break-inside:avoid;width:100%;border-collapse:collapse;font-size:9.4pt;line-height:1.5;}}
.oxt td{{border-bottom:.4pt solid #000;padding:1.35mm 1.5mm;vertical-align:middle;}}
.oxt td.n{{font-family:"Lab";width:8mm;text-align:center;}}
.oxt td.ox{{width:22mm;font-family:"Lab";text-align:center;white-space:nowrap;}}
.oxt td.ox i{{display:inline-block;width:5mm;}}
.oxt tr.grp td{{font-family:"Lab";font-weight:700;border-bottom:1.2pt solid #000;padding-top:3.5mm;}}
.oxt tr{{break-inside:avoid;}}
.sub2{{font-family:"Lab";font-weight:700;font-size:12pt;margin-top:8mm;padding-bottom:1.5mm;border-bottom:1.2pt solid #000;break-after:avoid;}}
.inst{{font-family:"Lab";font-size:9pt;margin:2mm 0 1mm;}}
.bpara{{display:flex;gap:4mm;padding:3mm 0;border-bottom:.4pt solid #000;break-inside:avoid;}}
.bk{{font-family:"Lab";font-weight:700;width:17mm;flex:none;}}
.bpara p{{line-height:2.25;text-align:justify;}}
.blank{{display:inline-block;min-width:25mm;border-bottom:.6pt solid #000;line-height:1.3;padding-left:.5mm;}}
.q{{break-inside:avoid;margin-bottom:5mm;}}
.stem{{font-weight:700;padding-left:1.7em;text-indent:-1.7em;margin-bottom:2mm;}}
.qn{{font-family:"Lab";font-weight:700;display:inline-block;min-width:1.7em;text-indent:0;}}
.bogi{{border:.6pt solid #000;padding:3.2mm 3mm 2.4mm;margin:3.5mm 0 3mm;position:relative;font-size:9.2pt;line-height:1.62;}}
.bogi .bl{{position:absolute;top:-2.3mm;left:0;right:0;text-align:center;line-height:1;}}
.bogi .bl span{{background:#fff;padding:0 2mm;}}
.bogi p{{text-align:justify;margin-bottom:.8mm;}}
.bogi .li{{padding-left:1.6em;text-indent:-1.6em;}}
.bogi .lk{{display:inline-block;width:1.6em;text-indent:0;}}
.bogi .note{{font-size:8.4pt;margin-top:1mm;}}
.dt{{width:100%;border-collapse:collapse;margin-top:2mm;font-size:8.4pt;line-height:1.35;text-align:center;}}
.dt th,.dt td{{border:.5pt solid #000;padding:1.2mm .8mm;}}
.dt th{{font-family:"Lab";font-weight:400;}}
.op{{line-height:1.64;padding-left:1.45em;text-indent:-1.45em;margin-bottom:.9mm;text-align:justify;}}
.op .c{{display:inline-block;width:1.45em;text-indent:0;}}
.opts.short{{display:grid;grid-template-columns:1fr 1fr 1fr;}}
.anshead{{border-bottom:2.5pt solid #000;margin-bottom:5mm;}}
.anshead h2{{font-family:"Lab";font-size:18pt;margin:0 0 2.5mm;}}
.ah{{font-family:"Lab";font-weight:700;margin:4mm 0 1.5mm;padding-bottom:1mm;border-bottom:1.2pt solid #000;break-after:avoid;}}
.ah:first-child{{margin-top:0;}}
.ah2{{font-family:"Lab";font-size:9pt;margin:2.5mm 0 1mm;}}
.ag{{width:100%;border-collapse:collapse;font-size:9pt;}}
.ag td{{padding:.8mm .5mm;border-bottom:.4pt solid #bbb;white-space:nowrap;}}
.ag td b{{font-family:"Lab";display:inline-block;min-width:5mm;}}
.ag.bg td{{white-space:normal;font-size:8.6pt;}}
.oxe{{font-size:8.8pt;line-height:1.55;padding-left:2.6em;text-indent:-2.6em;}}
.oxe b{{font-family:"Lab";display:inline-block;width:1.6em;text-indent:0;}}
.qg{{width:100%;border-collapse:collapse;text-align:center;font-size:9.5pt;}}
.qg th,.qg td{{border:.5pt solid #000;padding:.8mm 0;}}
.qg th{{font-family:"Lab";font-weight:400;background:#ececec;}}
.ex{{break-inside:avoid;margin-bottom:3mm;font-size:9pt;line-height:1.62;text-align:justify;}}
.exh{{font-family:"Lab";font-weight:700;}}
.sethead{{display:flex;align-items:baseline;gap:3mm;border-bottom:.6pt solid #000;padding-bottom:1.6mm;margin-bottom:5mm;}}
.sethead .sn{{font-family:"Lab";font-size:15pt;line-height:1;}}
.sethead .st{{font-family:"Lab";font-size:12pt;line-height:1.2;}}
.step1.withhead{{height:241mm;}}
.toc{{}}
.tochead{{border-bottom:2.5pt solid #000;margin-bottom:7mm;display:flex;align-items:flex-end;justify-content:space-between;}}
.tochead h1{{font-family:"Lab";font-weight:400;font-size:24pt;margin:0 0 2.5mm;line-height:1;}}
.tochead p{{font-family:"Lab";font-size:10pt;margin:0 0 3mm;}}
.tochead p span{{border:.6pt solid #000;padding:.3mm 1.6mm;margin-left:1.5mm;}}
.trow{{display:flex;align-items:baseline;gap:3mm;margin-top:4.2mm;break-inside:avoid;break-after:avoid;}}
.tn{{font-family:"Lab";font-size:12pt;width:10mm;flex:none;}}
.tt{{font-family:"Lab";font-size:11pt;flex:none;max-width:135mm;}}
.tdots{{flex:1;border-bottom:.8pt dotted #000;transform:translateY(-1mm);}}
.tp{{font-family:"Lab";font-size:11pt;flex:none;min-width:8mm;text-align:right;}}
.tsub{{font-family:"Lab";font-size:8.6pt;margin:1.2mm 0 0 13mm;padding-bottom:3mm;border-bottom:.4pt solid #000;break-inside:avoid;}}
.tsub b{{font-weight:400;}}
.tsep{{display:inline-block;margin:0 2.2mm;}}
'''

class Renderer:
    """Chromium 하나로 여러 HTML을 PDF로 만든다."""
    def __enter__(self):
        from playwright.sync_api import sync_playwright
        chrome = next((p for p in ("/usr/bin/google-chrome", "/usr/bin/chromium", "/usr/bin/chromium-browser") if os.path.exists(p)), None)
        self.pw = sync_playwright().start()
        self.b = self.pw.chromium.launch(**({"executable_path": chrome} if chrome else {}), args=["--allow-file-access-from-files"])
        self.n = 0; return self
    def pdf(self, body, cssall):
        self.n += 1
        hf = os.path.join(WD, f"_r{self.n:03d}.html"); pf = os.path.join(WD, f"_r{self.n:03d}.pdf")
        open(hf, "w", encoding="utf-8").write(f'<!doctype html><html lang="ko"><head><meta charset="utf-8"><style>{cssall}</style></head><body>{body}</body></html>')
        pg = self.b.new_page(); pg.goto("file://" + hf); pg.wait_for_timeout(600)
        pg.pdf(path=pf, prefer_css_page_size=True, print_background=True); pg.close()
        return pf
    def __exit__(self, *a):
        self.b.close(); self.pw.stop()

def npages(pdf):
    from pypdf import PdfReader
    return len(PdfReader(pdf).pages)

def find_pages(pdf, needles):
    """각 문구가 처음 나오는 쪽(0부터). 못 찾으면 None."""
    from pypdf import PdfReader
    txt = [re.sub(r"\s+", "", p.extract_text() or "") for p in PdfReader(pdf).pages]
    return [next((i for i, t in enumerate(txt) if re.sub(r"\s+", "", n) in t), None) for n in needles]

def stamp(pdfs, out, title):
    """여러 PDF를 이어 붙이고 머리글(로고·밑줄)과 바닥 쪽 번호 '- n -'을 1부터 이어서 단다."""
    from pypdf import PdfReader, PdfWriter
    from reportlab.pdfgen import canvas
    from reportlab.lib.units import mm as RMM
    from reportlab.pdfbase import pdfmetrics
    from reportlab.pdfbase.ttfonts import TTFont as RLTT
    pdfmetrics.registerFont(RLTT("Lab", LF["R"]))
    wr = PdfWriter(); PW, PH = 210 * RMM, 297 * RMM; k = 0
    for src in pdfs:
        for page in PdfReader(src).pages:
            k += 1
            buf = io.BytesIO(); c = canvas.Canvas(buf, pagesize=(PW, PH))
            lh = 5.6 * RMM
            c.drawImage(LOGO, 15 * RMM, PH - 11 * RMM - lh, width=lh * LW / LH, height=lh, mask="auto")
            c.setLineWidth(0.5); c.line(15 * RMM, PH - 18.5 * RMM, PW - 15 * RMM, PH - 18.5 * RMM)
            c.setFont("Lab", 9); c.drawCentredString(PW / 2, 9 * RMM, f"- {k} -")
            c.save(); buf.seek(0); page.merge_page(PdfReader(buf).pages[0]); wr.add_page(page)
    wr.add_metadata({"/Title": title, "/Author": "성공의 신화"})
    wr.write(out); return k

# ═════════════════════════ HWPX ═════════════════════════
MMU = 283.465
def mm(v): return int(round(v * MMU))
NS = ('xmlns:ha="http://www.hancom.co.kr/hwpml/2011/app" xmlns:hp="http://www.hancom.co.kr/hwpml/2011/paragraph" '
      'xmlns:hp10="http://www.hancom.co.kr/hwpml/2016/paragraph" xmlns:hs="http://www.hancom.co.kr/hwpml/2011/section" '
      'xmlns:hc="http://www.hancom.co.kr/hwpml/2011/core" xmlns:hh="http://www.hancom.co.kr/hwpml/2011/head" '
      'xmlns:hhs="http://www.hancom.co.kr/hwpml/2011/history" xmlns:hm="http://www.hancom.co.kr/hwpml/2011/master-page" '
      'xmlns:hpf="http://www.hancom.co.kr/schema/2011/hpf" xmlns:dc="http://purl.org/dc/elements/1.1/" '
      'xmlns:opf="http://www.idpf.org/2007/opf/" xmlns:ooxmlchart="http://www.hancom.co.kr/hwpml/2016/ooxmlchart" '
      'xmlns:hwpunitchar="http://www.hancom.co.kr/hwpml/2016/HwpUnitChar" xmlns:epub="http://www.idpf.org/2007/ops" '
      'xmlns:config="urn:oasis:names:tc:opendocument:xmlns:config:1.0"')
FONTS = ["나눔명조", "돋움"]; M, D = 0, 1
CHARS, PARAS, BFS = [], [], []

def cp(font=M, size=9.6, bold=False, ul=False, color="#000000"):
    k = (font, size, bold, ul, color)
    if k not in CHARS: CHARS.append(k)
    return CHARS.index(k)
def pp(align="JUSTIFY", indent=0, left=0, ls=170, prev=0, nxt=0, kwn=0):
    k = (align, indent, left, ls, prev, nxt, kwn)
    if k not in PARAS: PARAS.append(k)
    return PARAS.index(k)
def bf(l="NONE", r="NONE", t="NONE", b="NONE", w="0.12 mm", fill=None, bw=None):
    k = (l, r, t, b, w, fill, bw)
    if k not in BFS: BFS.append(k)
    return BFS.index(k) + 1
bf(); bf(w="0.1 mm"); cp(); pp(ls=100)

def char_xml(i, k):
    font, size, bold, ul, color = k
    f = " ".join(f'{a}="{font}"' for a in ("hangul", "latin", "hanja", "japanese", "other", "symbol", "user"))
    r = lambda t, v: f'<hh:{t} ' + " ".join(f'{a}="{v}"' for a in ("hangul", "latin", "hanja", "japanese", "other", "symbol", "user")) + "/>"
    return (f'<hh:charPr id="{i}" height="{int(size*100)}" textColor="{color}" shadeColor="none" useFontSpace="0" useKerning="0" symMark="NONE" borderFillIDRef="2">'
            f'<hh:fontRef {f}/>' + r("ratio", 100) + r("spacing", 0) + r("relSz", 100) + r("offset", 0) + ('<hh:bold/>' if bold else '')
            + f'<hh:underline type="{"BOTTOM" if ul else "NONE"}" shape="SOLID" color="#000000"/><hh:strikeout shape="NONE" color="#000000"/>'
            '<hh:outline type="NONE"/><hh:shadow type="NONE" color="#B2B2B2" offsetX="10" offsetY="10"/></hh:charPr>')
def para_xml(i, k):
    align, indent, left, ls, prev, nxt, kwn = k
    mg = lambda f: (f'<hh:margin><hc:intent value="{indent*f}" unit="HWPUNIT"/><hc:left value="{left*f}" unit="HWPUNIT"/><hc:right value="0" unit="HWPUNIT"/>'
                    f'<hc:prev value="{prev*f}" unit="HWPUNIT"/><hc:next value="{nxt*f}" unit="HWPUNIT"/></hh:margin><hh:lineSpacing type="PERCENT" value="{ls}" unit="HWPUNIT"/>')
    return (f'<hh:paraPr id="{i}" tabPrIDRef="0" condense="0" fontLineHeight="0" snapToGrid="0" suppressLineNumbers="0" checked="0">'
            f'<hh:align horizontal="{align}" vertical="BASELINE"/><hh:heading type="NONE" idRef="0" level="0"/>'
            f'<hh:breakSetting breakLatinWord="KEEP_WORD" breakNonLatinWord="BREAK_WORD" widowOrphan="1" keepWithNext="{kwn}" keepLines="1" pageBreakBefore="0" lineWrap="BREAK"/>'
            '<hh:autoSpacing eAsianEng="0" eAsianNum="0"/>'
            f'<hp:switch><hp:case hp:required-namespace="http://www.hancom.co.kr/hwpml/2016/HwpUnitChar">{mg(1)}</hp:case><hp:default>{mg(2)}</hp:default></hp:switch>'
            '<hh:border borderFillIDRef="2" offsetLeft="0" offsetRight="0" offsetTop="0" offsetBottom="0" connect="0" ignoreMargin="0"/></hh:paraPr>')
def bf_xml(i, k):
    l, r, t, b, w, fill, bw = k
    s = (f'<hh:borderFill id="{i}" threeD="0" shadow="0" centerLine="NONE" breakCellSeparateLine="0">'
         '<hh:slash type="NONE" Crooked="0" isCounter="0"/><hh:backSlash type="NONE" Crooked="0" isCounter="0"/>'
         f'<hh:leftBorder type="{l}" width="{w}" color="#000000"/><hh:rightBorder type="{r}" width="{w}" color="#000000"/>'
         f'<hh:topBorder type="{t}" width="{w}" color="#000000"/><hh:bottomBorder type="{b}" width="{bw or w}" color="#000000"/>'
         '<hh:diagonal type="SOLID" width="0.1 mm" color="#000000"/>')
    if fill: s += f'<hc:fillBrush><hc:winBrush faceColor="{fill}" hatchColor="#000000" alpha="0"/></hc:fillBrush>'
    return s + '</hh:borderFill>'

PID = [0]; TID = [1000]
def nid(): PID[0] += 1; return PID[0]
def mkruns(text, font=M, size=9.6, bold=False, color="#000000"):
    res, ul, bd = [], False, False
    for tok in re.split(r"(\[/?[ub]\])", text):
        if tok == "[u]": ul = True
        elif tok == "[/u]": ul = False
        elif tok == "[b]": bd = True
        elif tok == "[/b]": bd = False
        elif tok: res.append(f'<hp:run charPrIDRef="{cp(font, size, bold or bd, ul, color)}"><hp:t>{escape(tok)}</hp:t></hp:run>')
    return "".join(res) or f'<hp:run charPrIDRef="{cp(font, size)}"><hp:t/></hp:run>'
def P(text="", font=M, size=9.6, bold=False, color="#000000", **k):
    return f'<hp:p id="{nid()}" paraPrIDRef="{pp(**k)}" styleIDRef="0" pageBreak="0" columnBreak="0" merged="0">' + mkruns(text, font, size, bold, color) + '</hp:p>'
def P_obj(obj, **k):
    return f'<hp:p id="{nid()}" paraPrIDRef="{pp(**k)}" styleIDRef="0" pageBreak="0" columnBreak="0" merged="0"><hp:run charPrIDRef="0">{obj}<hp:t/></hp:run></hp:p>'
def table(rows, widths, cell_bf, heights=None, spans=None, margin=(1.6, 1.6, 1.0, 1.0), valign="CENTER"):
    TID[0] += 1
    heights = heights or [8] * len(rows); spans = spans or {}
    ml, mr, mt, mb = (mm(x) for x in margin)
    s = (f'<hp:tbl id="{TID[0]}" zOrder="0" numberingType="TABLE" textWrap="TOP_AND_BOTTOM" textFlow="BOTH_SIDES" lock="0" dropcapstyle="None" '
         f'pageBreak="CELL" repeatHeader="0" rowCnt="{len(rows)}" colCnt="{len(widths)}" cellSpacing="0" borderFillIDRef="1" noAdjust="0">'
         f'<hp:sz width="{sum(mm(w) for w in widths)}" widthRelTo="ABSOLUTE" height="{sum(mm(h) for h in heights)}" heightRelTo="ABSOLUTE" protect="0"/>'
         '<hp:pos treatAsChar="1" affectLSpacing="0" flowWithText="1" allowOverlap="0" holdAnchorAndSO="0" vertRelTo="PARA" horzRelTo="COLUMN" vertAlign="TOP" horzAlign="LEFT" vertOffset="0" horzOffset="0"/>'
         f'<hp:outMargin left="0" right="0" top="0" bottom="0"/><hp:inMargin left="{ml}" right="{mr}" top="{mt}" bottom="{mb}"/>')
    for r, row in enumerate(rows):
        s += "<hp:tr>"
        for c, content in enumerate(row):
            if content is None: continue
            cs, rs = spans.get((r, c), (1, 1))
            s += (f'<hp:tc name="" header="0" hasMargin="0" protect="0" editable="0" dirty="0" borderFillIDRef="{cell_bf(r, c)}">'
                  f'<hp:subList id="" textDirection="HORIZONTAL" lineWrap="BREAK" vertAlign="{valign}" linkListIDRef="0" linkListNextIDRef="0" textWidth="0" textHeight="0" hasTextRef="0" hasNumRef="0">'
                  f'{content}</hp:subList><hp:cellAddr colAddr="{c}" rowAddr="{r}"/><hp:cellSpan colSpan="{cs}" rowSpan="{rs}"/>'
                  f'<hp:cellSz width="{sum(mm(w) for w in widths[c:c+cs])}" height="{sum(mm(h) for h in heights[r:r+rs])}"/>'
                  f'<hp:cellMargin left="{ml}" right="{mr}" top="{mt}" bottom="{mb}"/></hp:tc>')
        s += "</hp:tr>"
    return s + "</hp:tbl>"
def pic(height_mm):
    TID[0] += 1
    ow, oh = LW * 75, LH * 75; h = mm(height_mm); w = int(h * LW / LH)
    return (f'<hp:pic id="{TID[0]}" zOrder="1" numberingType="PICTURE" textWrap="TOP_AND_BOTTOM" textFlow="BOTH_SIDES" lock="0" dropcapstyle="None" href="" groupLevel="0" instid="{TID[0]}" reverse="0">'
            f'<hp:offset x="0" y="0"/><hp:orgSz width="{ow}" height="{oh}"/><hp:curSz width="{w}" height="{h}"/><hp:flip horizontal="0" vertical="0"/>'
            f'<hp:rotationInfo angle="0" centerX="{w//2}" centerY="{h//2}" rotateimage="1"/>'
            '<hp:renderingInfo><hc:transMatrix e1="1" e2="0" e3="0" e4="0" e5="1" e6="0"/>'
            f'<hc:scaMatrix e1="{w/ow:.6f}" e2="0" e3="0" e4="0" e5="{h/oh:.6f}" e6="0"/><hc:rotMatrix e1="1" e2="0" e3="0" e4="0" e5="1" e6="0"/></hp:renderingInfo>'
            f'<hp:imgRect><hc:pt0 x="0" y="0"/><hc:pt1 x="{ow}" y="0"/><hc:pt2 x="{ow}" y="{oh}"/><hc:pt3 x="0" y="{oh}"/></hp:imgRect>'
            f'<hp:imgClip left="0" right="{ow}" top="0" bottom="{oh}"/><hp:inMargin left="0" right="0" top="0" bottom="0"/>'
            f'<hp:imgDim dimwidth="{ow}" dimheight="{oh}"/><hc:img binaryItemIDRef="image1" bright="0" contrast="0" effect="REAL_PIC" alpha="0"/><hp:effects/>'
            f'<hp:sz width="{w}" widthRelTo="ABSOLUTE" height="{h}" heightRelTo="ABSOLUTE" protect="0"/>'
            '<hp:pos treatAsChar="1" affectLSpacing="0" flowWithText="1" allowOverlap="0" holdAnchorAndSO="0" vertRelTo="PARA" horzRelTo="COLUMN" vertAlign="TOP" horzAlign="LEFT" vertOffset="0" horzOffset="0"/>'
            '<hp:outMargin left="0" right="0" top="0" bottom="0"/><hp:shapeComment>로고</hp:shapeComment></hp:pic>')

TEXTW = 180.0; COLW = (TEXTW - 9) / 2
def colpr(n):
    line = '<hp:colLine type="SOLID" width="0.12 mm" color="#000000"/>' if n == 2 else ""
    return f'<hp:ctrl><hp:colPr id="" type="NEWSPAPER" layout="LEFT" colCount="{n}" sameSz="1" sameGap="{mm(9)}">{line}</hp:colPr></hp:ctrl>'
def sec_first(cols, restart=False):
    bline = bf(b="SOLID")
    tb = table([[P_obj(pic(5.6), align="LEFT", ls=100)]], [TEXTW], lambda r, c: bline, heights=[8], margin=(0, 0, 0, 1.2), valign="BOTTOM")
    hdr = (f'<hp:ctrl><hp:header id="{nid()}" applyPageType="BOTH"><hp:subList id="" textDirection="HORIZONTAL" lineWrap="BREAK" vertAlign="TOP" linkListIDRef="0" linkListNextIDRef="0" textWidth="{mm(TEXTW)}" textHeight="{mm(14)}" hasTextRef="0" hasNumRef="0">'
           f'{P_obj(tb, align="LEFT", ls=100)}</hp:subList></hp:header></hp:ctrl>')
    pbf = '<hp:pageBorderFill type="{t}" borderFillIDRef="1" textBorder="PAPER" headerInside="0" footerInside="0" fillArea="PAPER"><hp:offset left="1417" right="1417" top="1417" bottom="1417"/></hp:pageBorderFill>'
    secpr = (f'<hp:secPr id="" textDirection="HORIZONTAL" spaceColumns="{mm(9)}" tabStop="8000" tabStopVal="4000" tabStopUnit="HWPUNIT" outlineShapeIDRef="0" memoShapeIDRef="0" textVerticalWidthHead="0" masterPageCnt="0">'
             '<hp:grid lineGrid="0" charGrid="0" wonggojiFormat="0"/>'
             f'<hp:startNum pageStartsOn="BOTH" page="{1 if restart else 0}" pic="0" tbl="0" equation="0"/>'
             '<hp:visibility hideFirstHeader="0" hideFirstFooter="0" hideFirstMasterPage="0" border="SHOW_ALL" fill="SHOW_ALL" hideFirstPageNum="0" hideFirstEmptyLine="0" showLineNumber="0"/>'
             '<hp:lineNumberShape restartType="0" countBy="0" distance="0" startNumber="0"/>'
             f'<hp:pagePr landscape="WIDELY" width="59528" height="84188" gutterType="LEFT_ONLY"><hp:margin header="{mm(10)}" footer="{mm(8)}" gutter="0" left="{mm(15)}" right="{mm(15)}" top="{mm(14)}" bottom="{mm(10)}"/></hp:pagePr>'
             '<hp:footNotePr><hp:autoNumFormat type="DIGIT" userChar="" prefixChar="" suffixChar=")" supscript="0"/><hp:noteLine length="-1" type="SOLID" width="0.12 mm" color="#000000"/><hp:noteSpacing betweenNotes="283" belowLine="567" aboveLine="850"/><hp:numbering type="CONTINUOUS" newNum="1"/><hp:placement place="EACH_COLUMN" beneathText="0"/></hp:footNotePr>'
             '<hp:endNotePr><hp:autoNumFormat type="DIGIT" userChar="" prefixChar="" suffixChar=")" supscript="0"/><hp:noteLine length="14692344" type="SOLID" width="0.12 mm" color="#000000"/><hp:noteSpacing betweenNotes="0" belowLine="567" aboveLine="850"/><hp:numbering type="CONTINUOUS" newNum="1"/><hp:placement place="END_OF_DOCUMENT" beneathText="0"/></hp:endNotePr>'
             + pbf.format(t="BOTH") + pbf.format(t="EVEN") + pbf.format(t="ODD") + '</hp:secPr>')
    return (f'<hp:p id="{nid()}" paraPrIDRef="{pp(ls=100)}" styleIDRef="0" pageBreak="0" columnBreak="0" merged="0">'
            f'<hp:run charPrIDRef="0">{secpr}{colpr(cols)}{hdr}<hp:ctrl><hp:pageNum pos="BOTTOM_CENTER" formatType="DIGIT" sideChar="-"/></hp:ctrl></hp:run><hp:run charPrIDRef="0"><hp:t/></hp:run></hp:p>')
def section(x): return f'<?xml version="1.0" encoding="UTF-8" standalone="yes" ?><hs:sec {NS}>{x}</hs:sec>'
def step_head(num, title):
    black = bf(fill="#000000", b="SOLID", bw="0.7 mm"); line = bf(b="SOLID", bw="0.7 mm")
    left = P("Step", D, 9, color="#FFFFFF", align="LEFT", ls=100) + P(str(num), D, 30, True, "#FFFFFF", align="LEFT", ls=100)
    return P_obj(table([[left, P(title, D, 18, True, align="LEFT", ls=110)]], [24, TEXTW - 24], lambda r, c: black if c == 0 else line,
                       heights=[20], margin=(3, 4, 2, 2.5), valign="BOTTOM"), align="LEFT", ls=100, nxt=mm(5))

def hwpx_reset():
    CHARS.clear(); PARAS.clear(); BFS.clear(); PID[0] = 0; TID[0] = 1000
    bf(); bf(w="0.1 mm"); cp(); pp(ls=100)

def hx_head(head):
    line = bf(b="SOLID")
    t = P(f'{head["no"]}   {head["title"]}', D, 12, True, align="LEFT", ls=120)
    return P_obj(table([[t]], [TEXTW], lambda r, c: line, heights=[9], margin=(0, 0, 0, 1.5), valign="BOTTOM"), align="LEFT", ls=100, nxt=mm(4))

def hx_colchange(n):
    return f'<hp:p id="{nid()}" paraPrIDRef="{pp(ls=100)}" styleIDRef="0" pageBreak="0" columnBreak="0" merged="0"><hp:run charPrIDRef="0">{colpr(n)}</hp:run><hp:run charPrIDRef="0"><hp:t/></hp:run></hp:p>'

def hwpx_set(C, head=None, restart=False):
    """학습지 한 세트의 HWPX 구역들: ([Step1, Step2, Step3], 정답과 해설)."""
    P_, Q_ = C["passages"], C["questions"]; multi = len(P_) > 1
    OX = C["ox"]; BA = C["blank_answers"]
    s1 = section(sec_first(1, restart=restart) + (hx_head(head) if head else "") + step_head(*STEPS[0]))
    s3 = [sec_first(1), step_head(*STEPS[1])]
    ln = bf(b="SOLID"); groups = {}
    for i, o in enumerate(OX, 1): groups.setdefault(o["group"], []).append((i, o["text"]))
    for g, items in groups.items():
        s3.append(P(g, D, 9.6, True, align="LEFT", ls=130, prev=mm(3), kwn=1))
        rows = [[P(str(i), D, 9, align="CENTER", ls=130), P(t, size=9.4, align="LEFT", ls=140), P("O      X", D, 9.4, align="CENTER", ls=130)] for i, t in items]
        s3.append(P_obj(table(rows, [9, 149, 22], lambda r, c: ln, heights=[7.5] * len(rows), margin=(1.2, 1.2, 1.1, 1.1)), align="LEFT", ls=100))
    s3.append(P("빈칸 넣기", D, 12, True, align="LEFT", ls=130, prev=mm(8), kwn=1))
    s3.append(P("빈칸에 들어갈 말을 지문에서 찾아 쓰세요.", D, 9, align="LEFT", ls=130, nxt=mm(1.5), kwn=1))
    brow = [[P(b["group"], D, 9.6, True, align="LEFT", ls=100), P(re.sub(r"\( ([①-⑳]) \)", r"( \1 ______________ )", b["text"]), ls=230)] for b in C["blanks"]]
    s3.append(P_obj(table(brow, [20, 160], lambda r, c: ln, heights=[20] * len(brow), margin=(0, 1, 2.5, 2.5), valign="TOP"), align="LEFT", ls=100))
    s4 = [sec_first(1), step_head(*STEPS[2])]
    b4 = [P(setline(C), D, 10, True, align="LEFT", ls=160, nxt=mm(1.5))]
    for p in P_:
        if multi: b4.append(P(f"({p['label']})", D, 9.6, True, align="LEFT", ls=170, prev=mm(3), kwn=1))
        for para in p["paras"]: b4.append(P(para, indent=mm(3.4), ls=170))
    b4.append(P("", ls=100, nxt=mm(3)))
    box_bf = bf("SOLID", "SOLID", "SOLID", "SOLID")
    for n, x in enumerate(Q_, 1):
        b4.append(P(f'{n}. ' + x["stem"] + f' [{x["pts"]:.1f}점]', bold=True, indent=-mm(5), ls=165, prev=mm(4), nxt=mm(1.5), kwn=1))
        b = x.get("box")
        if b:
            inner = P("<보기>", align="CENTER", ls=120, nxt=mm(1))
            if b["kind"] == "text": inner += "".join(P(t, size=9.1, ls=155, nxt=mm(.8)) for t in b["paras"])
            elif b["kind"] == "list": inner += "".join(P(f"{k}. {t}", size=9.1, indent=-mm(4.2), ls=155, nxt=mm(.5)) for k, t in b["items"])
            else:
                if b.get("intro"): inner += P(b["intro"], size=9.1, ls=155, nxt=mm(1.5))
                nc = len(b["head"]); ws = [(COLW - 6) / nc] * nc
                tr = [[P(h, D, 8.2, align="CENTER", ls=120) for h in b["head"]]] + [[P(cv, size=8.4, align="CENTER", ls=125) for cv in r] for r in b["rows"]]
                inner += P_obj(table(tr, ws, lambda r, c: box_bf, heights=[9] * len(tr), margin=(.6, .6, .8, .8)), align="CENTER", ls=100)
                if b.get("note"): inner += P(b["note"], size=8.4, ls=140, prev=mm(1))
            b4.append(P_obj(table([[inner]], [COLW], lambda r, c: box_bf, heights=[20], margin=(2.8, 2.8, 2.2, 2.2), valign="TOP"), align="LEFT", ls=100, prev=mm(1.5), nxt=mm(2), kwn=1))
        for j, o in enumerate(x["opts"]):
            b4.append(P(f"{CIRC[j]} {o}", indent=-mm(4.6), ls=162, nxt=mm(1), kwn=0 if j == 4 else 1))
    body = [s1, section("".join(s3)), section("".join(s4) + hx_colchange(2) + "".join(b4))]
    # 정답과 해설
    s5 = [sec_first(1, restart=False)] + ([hx_head(head)] if head else []) + [P("정답과 해설", D, 18, True, align="LEFT", ls=120, nxt=mm(3)), hx_colchange(2)]
    ah = lambda t: P(t, D, 10, True, align="LEFT", ls=130, prev=mm(3.5), nxt=mm(1), kwn=1)
    grid = bf("SOLID", "SOLID", "SOLID", "SOLID"); gray = bf("SOLID", "SOLID", "SOLID", "SOLID", fill="#ECECEC")
    s5.append(ah("Step 2 OX"))
    cells = [P(f"{i} {o['ans']}", D, 9, align="CENTER", ls=100) for i, o in enumerate(OX, 1)]
    cells += [P("", ls=100)] * ((-len(cells)) % 7)
    rows = [cells[i:i + 7] for i in range(0, len(cells), 7)]
    s5.append(P_obj(table(rows, [COLW / 7] * 7, lambda r, c: grid, heights=[6] * len(rows), margin=(.3, .3, .8, .8)), align="LEFT", ls=100))
    s5.append(P("X 진술 바로잡기", D, 9, align="LEFT", ls=130, prev=mm(2)))
    for i, o in enumerate(OX, 1):
        if o["ans"] == "X": s5.append(P(f"{i}  {o['why']}", size=8.8, indent=-mm(5), ls=150))
    s5.append(ah("Step 2 빈칸"))
    for i, a in enumerate(BA): s5.append(P(f"{CIRC20[i]} {a}", size=9, ls=140))
    s5.append(ah("Step 3 빠른 정답"))
    qrows = [[P(str(i + 1), D, 9, align="CENTER", ls=100) for i in range(10)], [P(CIRC[Q_[i]["ans"] - 1], size=9.6, align="CENTER", ls=100) for i in range(10)],
             [P(str(i + 1), D, 9, align="CENTER", ls=100) for i in range(10, 20)], [P(CIRC[Q_[i]["ans"] - 1], size=9.6, align="CENTER", ls=100) for i in range(10, 20)]]
    s5.append(P_obj(table(qrows, [COLW / 10] * 10, lambda r, c: gray if r % 2 == 0 else grid, heights=[6] * 4, margin=(.2, .2, .6, .6)), align="LEFT", ls=100))
    s5.append(ah("Step 3 해설"))
    for n, x in enumerate(Q_, 1):
        s5.append(P(f'{n}. 정답 {CIRC[x["ans"]-1]}', D, 9.4, True, align="LEFT", ls=140, prev=mm(2), kwn=1))
        s5.append(P(x["exp"], size=9, ls=158))
    return body, section("".join(s5))

def hwpx_toc(title, entries, kind):
    sub = "본책" if kind == "body" else "정답과 해설"
    x = [sec_first(1, restart=True)]
    thick = bf(b="SOLID", bw="0.7 mm")
    x.append(P_obj(table([[P("차례", D, 24, align="LEFT", ls=110), P(f"{title}  [{sub}]", D, 10, align="RIGHT", ls=110)]], [100, TEXTW - 100],
                         lambda r, c: thick, heights=[14], margin=(0, 0, 0, 2.5), valign="BOTTOM"), align="LEFT", ls=100, nxt=mm(6)))
    ln = bf(b="SOLID"); rows = []
    for e in entries:
        cell = P(e["title"], D, 11, align="LEFT", ls=140)
        if e.get("steps"):
            cell += P("   ·   ".join(f"{n} {p}쪽" for n, p in e["steps"]), D, 8.6, align="LEFT", ls=130, prev=mm(1))
        rows.append([P(e["no"], D, 12, align="LEFT", ls=120), cell, P(str(e["page"]), D, 11, align="RIGHT", ls=120)])
    x.append(P_obj(table(rows, [14, TEXTW - 34, 20], lambda r, c: ln, heights=[14 if entries and entries[0].get("steps") else 10] * len(rows),
                         margin=(0, 1, 2.5, 2.5), valign="TOP"), align="LEFT", ls=100))
    return section("".join(x))

def hwpx_write(path, S, title, embed=None):
    ff = "".join(f'<hh:fontface lang="{lg}" fontCnt="2">' + "".join(f'<hh:font id="{i}" face="{escape(n)}" type="TTF" isEmbedded="0"/>' for i, n in enumerate(FONTS)) + '</hh:fontface>'
                 for lg in ("HANGUL", "LATIN", "HANJA", "JAPANESE", "OTHER", "SYMBOL", "USER"))
    header = (f'<?xml version="1.0" encoding="UTF-8" standalone="yes" ?><hh:head {NS} version="1.4" secCnt="{len(S)}">'
              '<hh:beginNum page="1" footnote="1" endnote="1" pic="1" tbl="1" equation="1"/><hh:refList>'
              f'<hh:fontfaces itemCnt="7">{ff}</hh:fontfaces>'
              f'<hh:borderFills itemCnt="{len(BFS)}">' + "".join(bf_xml(i + 1, k) for i, k in enumerate(BFS)) + '</hh:borderFills>'
              f'<hh:charProperties itemCnt="{len(CHARS)}">' + "".join(char_xml(i, k) for i, k in enumerate(CHARS)) + '</hh:charProperties>'
              '<hh:tabProperties itemCnt="1"><hh:tabPr id="0" autoTabLeft="0" autoTabRight="0"/></hh:tabProperties>'
              f'<hh:paraProperties itemCnt="{len(PARAS)}">' + "".join(para_xml(i, k) for i, k in enumerate(PARAS)) + '</hh:paraProperties>'
              '<hh:styles itemCnt="1"><hh:style id="0" type="PARA" name="바탕글" engName="Normal" paraPrIDRef="0" charPrIDRef="0" nextStyleIDRef="0" langID="1042" lockForm="0"/></hh:styles>'
              '</hh:refList><hh:compatibleDocument targetProgram="HWP201X"><hh:layoutCompatibility/></hh:compatibleDocument>'
              '<hh:docOption><hh:linkinfo path="" pageInherit="0" footnoteInherit="0"/></hh:docOption><hh:trackchageConfig flags="56"/></hh:head>')
    items = "".join(f'<opf:item id="section{i}" href="Contents/section{i}.xml" media-type="application/xml"/>' for i in range(len(S)))
    spine = "".join(f'<opf:itemref idref="section{i}" linear="yes"/>' for i in range(len(S)))
    hpf = (f'<?xml version="1.0" encoding="UTF-8" standalone="yes" ?><opf:package {NS} version="" unique-identifier="" id="">'
           f'<opf:metadata><opf:title>{escape(title)}</opf:title><opf:language>ko</opf:language></opf:metadata>'
           '<opf:manifest><opf:item id="header" href="Contents/header.xml" media-type="application/xml"/>'
           '<opf:item id="image1" href="BinData/image1.png" media-type="image/png" isEmbeded="1"/>'
           f'{items}<opf:item id="settings" href="settings.xml" media-type="application/xml"/></opf:manifest>'
           f'<opf:spine><opf:itemref idref="header" linear="yes"/>{spine}</opf:spine></opf:package>')
    PK = "http://www.hancom.co.kr/hwpml/2016/meta/pkg#"
    rdf = ('<?xml version="1.0" encoding="UTF-8" standalone="yes" ?><rdf:RDF xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">'
           f'<rdf:Description rdf:about=""><ns0:hasPart xmlns:ns0="{PK}" rdf:resource="Contents/header.xml"/></rdf:Description>'
           f'<rdf:Description rdf:about="Contents/header.xml"><rdf:type rdf:resource="{PK}HeaderFile"/></rdf:Description>'
           + "".join(f'<rdf:Description rdf:about=""><ns0:hasPart xmlns:ns0="{PK}" rdf:resource="Contents/section{i}.xml"/></rdf:Description>'
                     f'<rdf:Description rdf:about="Contents/section{i}.xml"><rdf:type rdf:resource="{PK}SectionFile"/></rdf:Description>' for i in range(len(S)))
           + f'<rdf:Description rdf:about=""><rdf:type rdf:resource="{PK}Document"/></rdf:Description></rdf:RDF>')
    files = [("version.xml", '<?xml version="1.0" encoding="UTF-8" standalone="yes" ?><hv:HCFVersion xmlns:hv="http://www.hancom.co.kr/hwpml/2011/version" tagetApplication="WORDPROCESSOR" major="5" minor="1" micro="0" buildNumber="1" os="1" xmlVersion="1.4" application="Hancom Office Hangul" appVersion="11, 0, 0, 0"/>'),
             ("Contents/header.xml", header)] + [(f"Contents/section{i}.xml", s) for i, s in enumerate(S)] + [
             ("Contents/content.hpf", hpf),
             ("settings.xml", '<?xml version="1.0" encoding="UTF-8" standalone="yes" ?><ha:HWPApplicationSetting xmlns:ha="http://www.hancom.co.kr/hwpml/2011/app" xmlns:config="urn:oasis:names:tc:opendocument:xmlns:config:1.0"><ha:CaretPosition listIDRef="0" paraIDRef="0" pos="0"/></ha:HWPApplicationSetting>'),
             ("Preview/PrvText.txt", title),
             ("META-INF/container.xml", '<?xml version="1.0" encoding="UTF-8" standalone="yes" ?><ocf:container xmlns:ocf="urn:oasis:names:tc:opendocument:xmlns:container" xmlns:hpf="http://www.hancom.co.kr/schema/2011/hpf"><ocf:rootfiles><ocf:rootfile full-path="Contents/content.hpf" media-type="application/hwpml-package+xml"/></ocf:rootfiles></ocf:container>'),
             ("META-INF/container.rdf", rdf),
             ("META-INF/manifest.xml", '<?xml version="1.0" encoding="UTF-8" standalone="yes" ?><odf:manifest xmlns:odf="urn:oasis:names:tc:opendocument:xmlns:manifest:1.0"/>')]
    from lxml import etree
    with zipfile.ZipFile(path, "w") as z:
        z.writestr(zipfile.ZipInfo("mimetype"), "application/hwp+zip", compress_type=zipfile.ZIP_STORED)
        for n, d in files:
            if n.endswith((".xml", ".hpf", ".rdf")): etree.fromstring(d.encode("utf-8"))  # 형식 검사
            z.writestr(n, d.encode("utf-8"), compress_type=zipfile.ZIP_DEFLATED)
        z.write(LOGO, "BinData/image1.png", compress_type=zipfile.ZIP_DEFLATED)
        if embed is not None:
            z.writestr(JSON_IN_HWPX, json.dumps(embed, ensure_ascii=False, indent=1).encode("utf-8"), compress_type=zipfile.ZIP_DEFLATED)

# ═════════════════════════ 명령 ═════════════════════════
def cmd_makeone(cj, wd):
    C = json.load(open(cj, encoding="utf-8"))
    err = validate(C)
    if err: print("검증 실패:", *err, sep="\n - "); sys.exit(1)
    setup(wd); NAME = safe(C["title"]) + "_학습지세트"
    body, ans = set_html(C)
    CS = css(body + ans)
    with Renderer() as R:
        pf = R.pdf(body + "\n" + ans, CS)
    PDF = os.path.join(WD, "out", NAME + ".pdf"); n = stamp([pf], PDF, C["title"])
    print("PDF", PDF, n, "쪽")
    hwpx_reset(); b, a = hwpx_set(C, restart=True)
    HW = os.path.join(WD, "out", NAME + ".hwpx"); hwpx_write(HW, b + [a], C["title"], embed=C)
    print("HWPX", HW)

def load_input(f, wd):
    if f.lower().endswith(".json"):
        return json.load(open(f, encoding="utf-8"))
    if f.lower().endswith(".hwpx"):
        with zipfile.ZipFile(f) as z:
            if JSON_IN_HWPX in z.namelist():
                return json.loads(z.read(JSON_IN_HWPX).decode("utf-8"))
        os.makedirs(os.path.join(wd, "_extract"), exist_ok=True)
        t = os.path.join(wd, "_extract", os.path.splitext(os.path.basename(f))[0] + ".txt")
        cmd_extract(f, t)
        print(f"NEED_JSON\t{f}\t{t}"); return None
    print(f"지원하지 않는 파일: {f} (.hwp는 한글에서 .hwpx로 저장해 다시 첨부)"); return None

def cmd_bind(wd, title, files):
    sets = [load_input(f, wd) for f in files]
    if any(s is None for s in sets):
        print("중단: 위 파일들의 content.json을 만든 뒤 .json 경로로 바꿔 다시 실행"); sys.exit(3)
    bad = [(i + 1, e) for i, s in enumerate(sets) for e in validate(s)]
    if bad:
        print("검증 실패:", *[f"{i}번째 세트: {e}" for i, e in bad], sep="\n - "); sys.exit(1)
    setup(wd); NAME = safe(title)
    heads = [{"no": f"{i:02d}", "title": s["title"]} for i, s in enumerate(sets, 1)]
    htmls = [set_html(s, h) for s, h in zip(sets, heads)]
    CS = css("".join(b + a for b, a in htmls) + title + "차례본책정답과해설0123456789·")
    with Renderer() as R:
        bpdf = [R.pdf(b, CS) for b, _ in htmls]
        apdf = [R.pdf(a, CS) for _, a in htmls]
        def make(kind, pdfs):
            def entries(start):
                out, p = [], start
                for i, (s, h, pf) in enumerate(zip(sets, heads, pdfs)):
                    e = {"no": h["no"], "title": s["title"], "page": p}
                    if kind == "body":
                        off = find_pages(pf, ["직접 정리하기", "OX 정리와 빈칸 넣기", "초고난도 변형문제"])
                        e["steps"] = [(f"Step {k + 1}", p + (o if o is not None else 0)) for k, o in enumerate(off)]
                    out.append(e); p += npages(pf)
                return out
            t = R.pdf(toc_html(title, entries(1), kind), CS); tn = npages(t)
            if tn > 1: t = R.pdf(toc_html(title, entries(1 + tn), kind), CS)
            ent = entries(1 + npages(t))
            t = R.pdf(toc_html(title, ent, kind), CS)
            assert npages(t) == ent[0]["page"] - 1, "차례 쪽수가 바뀜"
            out = os.path.join(WD, "out", f"{NAME}_{'본책' if kind == 'body' else '답지'}.pdf")
            n = stamp([t] + pdfs, out, f"{title} {'본책' if kind == 'body' else '답지'}")
            return out, n, ent
        B = make("body", bpdf); A = make("answers", apdf)
    for kind, (out, n, ent) in (("본책", B), ("답지", A)):
        print(f"PDF {kind}", out, n, "쪽")
        for e in ent: print("   ", e["no"], e["title"], e["page"], "쪽", " ".join(f"{a}:{b}" for a, b in e.get("steps", [])))
    # HWPX: 같은 차례(쪽 번호는 PDF 기준)
    hwpx_reset(); S = [hwpx_toc(title, B[2], "body")]
    for s, h in zip(sets, heads): S += hwpx_set(s, h)[0]
    hb = os.path.join(WD, "out", f"{NAME}_본책.hwpx"); hwpx_write(hb, S, f"{title} 본책", embed={"bind": sets})
    hwpx_reset(); S = [hwpx_toc(title, A[2], "answers")]
    for s, h in zip(sets, heads): S.append(hwpx_set(s, h)[1])
    ha = os.path.join(WD, "out", f"{NAME}_답지.hwpx"); hwpx_write(ha, S, f"{title} 답지")
    print("HWPX 본책", hb); print("HWPX 답지", ha)

def cmd_extract(f, out):
    from lxml import etree
    HP = "{http://www.hancom.co.kr/hwpml/2011/paragraph}"
    lines = []
    with zipfile.ZipFile(f) as z:
        secs = sorted((n for n in z.namelist() if re.match(r"Contents/section\d+\.xml$", n)), key=lambda n: int(re.findall(r"\d+", n)[0]))
        for n in secs:
            lines.append(f"===== {n} =====")
            root = etree.fromstring(z.read(n))
            for p in root.iter(HP + "p"):
                if p.find(".//" + HP + "p") is not None: continue  # 표·글상자 바깥 문단은 건너뛰고 안쪽 문단을 씀
                t = "".join(x.text or "" for x in p.iter(HP + "t"))
                if t.strip(): lines.append(t)
    open(out, "w", encoding="utf-8").write("\n".join(lines) + "\n")
    print("추출", out, len(lines), "줄")

def cmd_textdump(cj):
    C = json.load(open(cj, encoding="utf-8"))
    for i, o in enumerate(C["ox"]):
        print(f"ox[{i}].text\t{o['text']}"); print(f"ox[{i}].why\t{o['why']}")
    for i, b in enumerate(C["blanks"]): print(f"blanks[{i}].text\t{b['text']}")
    for i, a in enumerate(C["blank_answers"]): print(f"blank_answers[{i}]\t{a}")
    for i, q in enumerate(C["questions"]):
        print(f"questions[{i}].stem\t{q['stem']}")
        b = q.get("box") or {}
        for k, t in enumerate(b.get("paras", [])): print(f"questions[{i}].box.paras[{k}]\t{t}")
        for k, (_, t) in enumerate(b.get("items", [])): print(f"questions[{i}].box.items[{k}][1]\t{t}")
        if b.get("intro"): print(f"questions[{i}].box.intro\t{b['intro']}")
        for k, r in enumerate(b.get("rows", [])): print(f"questions[{i}].box.rows[{k}]\t{' | '.join(r)}")
        if b.get("note"): print(f"questions[{i}].box.note\t{b['note']}")
        for k, o in enumerate(q["opts"]): print(f"questions[{i}].opts[{k}]\t{o}")
        print(f"questions[{i}].exp\t{q['exp']}")

if __name__ == "__main__":
    a = sys.argv[1:]
    if not a: print(__doc__ or open(__file__, encoding="utf-8").read(900)); sys.exit(0)
    if a[0] == "makeone": cmd_makeone(a[1], a[2])
    elif a[0] == "bind":
        wd = a[1]; rest = a[2:]; title = "학습지 모음"
        if rest[:1] == ["--title"]: title, rest = rest[1], rest[2:]
        cmd_bind(wd, title, rest)
    elif a[0] == "extract": cmd_extract(a[1], a[2])
    elif a[0] == "textdump": cmd_textdump(a[1])
    elif a[0] == "check":
        e = validate(json.load(open(a[1], encoding="utf-8"))); print("검증 실패:", *e, sep="\n - ") if e else print("검증 통과")
    else: sys.exit("명령: makeone | bind | extract | textdump | check")
