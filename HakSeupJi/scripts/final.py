# 파이널 정리 조판 도구 (성공의 신화 양식)
# 사용법 (sheet.py, fonts/, logo.png 가 같은 작업폴더에 있어야 한다)
#   python3 -I final.py render 작업폴더/final.json 작업폴더
#       → 작업폴더/out/{title}_파이널.pdf (문제지), {title}_파이널_정답.pdf (같은 지면에 정답을 빨간 글씨로 채움)
#   python3 -I final.py check 작업폴더/final.json      (검증만)
#   python3 -I final.py textdump 작업폴더/final.json   (맞춤법 검사용: 모든 글을 위치 표시와 함께 출력)
# final.json
#   {"title": "주택 임대차 보호", "source": "출처(선택)",
#    "diagram": [노드…],                       ← 1. 구조도 (빈칸은 {{정답}})
#    "ox": [{"text": "진술", "ans": "O|X", "why": "근거·바로잡기", "tag": "함정 유형(선택)"} × 20]}
# 노드
#   {"type":"section","title":"1문단 · …","items":[노드…]}         제목 띠가 있는 묶음(세로로 쌓음)
#   {"type":"box","title":"(선택)","body":["줄", "- 점 목록"],"shape":"rect|round|pill|dashed|bold|gray|plain","w":1}
#   {"type":"row","items":[노드…],"link":"arrow|back|both|line|vs|plus|eq|none","labels":["간격 위 글"…],"w":1}
#   {"type":"col","items":[노드…],"link":"arrow|line|none","labels":[…],"w":1}
#   {"type":"tree","root":노드,"children":[노드…],"w":1}             위에서 아래로 갈라지는 분류도
#   {"type":"table","head":[…],"rows":[[…]],"w":1}                    비교표 (첫 열은 라벨)
#   {"type":"note","text":"…"}                                        덧붙임 설명
# 글 안 표시: [u]밑줄[/u], [b]굵게[/b], {{빈칸 정답}}
import sys, os, re, json, html, importlib.util

HERE = os.path.dirname(os.path.abspath(__file__))
RED = "#d40000"

def load_sheet(wd):
    for d in (wd, HERE):
        p = os.path.join(d, "sheet.py")
        if os.path.exists(p):
            spec = importlib.util.spec_from_file_location("sheet", p); m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
            return m
    sys.exit("sheet.py를 찾지 못함 (작업폴더에 복사할 것)")

BL = re.compile(r"\{\{(.+?)\}\}")
SHAPES = {"rect", "round", "pill", "dashed", "bold", "gray", "plain"}
LINKS_R = {"arrow", "back", "both", "line", "vs", "plus", "eq", "none"}
LINKS_C = {"arrow", "line", "none"}

# ───────── 순회 (렌더 순서 = 빈칸 번호 순서) ─────────
def walk_texts(n, path="diagram"):
    """(위치, 글) 을 화면에 나오는 순서대로 낸다."""
    t = n.get("type")
    if t == "section":
        yield f"{path}.title", n["title"]
        for i, c in enumerate(n["items"]): yield from walk_texts(c, f"{path}.items[{i}]")
    elif t == "box":
        if n.get("title"): yield f"{path}.title", n["title"]
        for i, s in enumerate(n.get("body", [])): yield f"{path}.body[{i}]", s
    elif t in ("row", "col"):
        labs = n.get("labels", [])
        for i, c in enumerate(n["items"]):
            if i > 0 and i - 1 < len(labs) and labs[i - 1]: yield f"{path}.labels[{i-1}]", labs[i - 1]
            yield from walk_texts(c, f"{path}.items[{i}]")
    elif t == "tree":
        yield from walk_texts(n["root"], f"{path}.root")
        for i, c in enumerate(n["children"]): yield from walk_texts(c, f"{path}.children[{i}]")
    elif t == "table":
        for i, h in enumerate(n["head"]): yield f"{path}.head[{i}]", h
        for r, row in enumerate(n["rows"]):
            for c, cell in enumerate(row): yield f"{path}.rows[{r}][{c}]", cell
    elif t == "note":
        yield f"{path}.text", n["text"]

def all_diagram_texts(F):
    for i, n in enumerate(F["diagram"]): yield from walk_texts(n, f"diagram[{i}]")

# ───────── 검증 ─────────
def validate(F):
    err = []
    def chk(n, p):
        t = n.get("type")
        if t not in ("section", "box", "row", "col", "tree", "table", "note"): err.append(f"{p}: type '{t}' 모름"); return
        if t == "box" and n.get("shape", "rect") not in SHAPES: err.append(f"{p}: shape '{n.get('shape')}' 모름")
        if t == "row" and n.get("link", "arrow") not in LINKS_R: err.append(f"{p}: link '{n.get('link')}' 모름")
        if t == "col" and n.get("link", "arrow") not in LINKS_C: err.append(f"{p}: link '{n.get('link')}' 모름")
        if t in ("section", "row", "col"):
            if not n.get("items"): err.append(f"{p}: items 비어 있음")
            for i, c in enumerate(n.get("items", [])): chk(c, f"{p}.items[{i}]")
        if t == "tree":
            chk(n["root"], f"{p}.root")
            if len(n.get("children", [])) < 2: err.append(f"{p}: tree 가지는 2개 이상")
            for i, c in enumerate(n.get("children", [])): chk(c, f"{p}.children[{i}]")
        if t == "table":
            for r, row in enumerate(n["rows"]):
                if len(row) != len(n["head"]): err.append(f"{p}.rows[{r}]: 칸 수가 head와 다름")
    for i, n in enumerate(F.get("diagram", [])): chk(n, f"diagram[{i}]")
    nb = 0
    for p, s in all_diagram_texts(F):
        for a in BL.findall(s):
            nb += 1
            if not a.strip() or "[" in a: err.append(f"{p}: 빈칸 정답 '{a}' (비었거나 태그 포함)")
        if s.count("{{") != s.count("}}"): err.append(f"{p}: 빈칸 괄호 짝이 안 맞음")
    if nb < 30: err.append(f"구조도 빈칸 {nb}개 (30개 이상)")
    ox = F.get("ox", [])
    if len(ox) != 20: err.append(f"OX {len(ox)}개 (20개여야 함)")
    for i, o in enumerate(ox, 1):
        if o.get("ans") not in ("O", "X"): err.append(f"OX {i}번 ans는 O 또는 X")
        if not o.get("why"): err.append(f"OX {i}번 why 없음")
    nx = sum(o.get("ans") == "X" for o in ox)
    if ox and not 8 <= nx <= 12: err.append(f"OX의 X가 {nx}개 (8~12개)")
    return err, nb

# ───────── HTML ─────────
class Ctx:
    def __init__(self, answer): self.answer = answer; self.n = 0

def inl(s, cx):
    out = []
    for k, part in enumerate(BL.split(s)):
        if k % 2 == 0:
            t = html.escape(part, quote=False)
            out.append(t.replace("[u]", "<u>").replace("[/u]", "</u>").replace("[b]", "<b>").replace("[/b]", "</b>"))
        else:
            cx.n += 1
            w = sum(1.0 if ord(ch) > 0x2E80 else 0.55 for ch in part) + 1.5
            inner = f"<b>{html.escape(part)}</b>" if cx.answer else ""
            out.append(f'<span class="bk" style="min-width:{w:.2f}em"><i>{cx.n}</i>{inner}</span>')
    return "".join(out)

def wstyle(n):
    return f' style="flex:{n.get("w", 1)} 1 0"' if "w" in n else ""

def node(n, cx):
    t = n["type"]
    if t == "section":
        return (f'<div class="fs"><div class="fsh">{inl(n["title"], cx)}</div><div class="fsb">'
                + "".join(node(c, cx) for c in n["items"]) + "</div></div>")
    if t == "box":
        sh = n.get("shape", "rect")
        s = f'<div class="fb {sh}"{wstyle(n)}>'
        if n.get("title"): s += f'<div class="fbt">{inl(n["title"], cx)}</div>'
        for line in n.get("body", []):
            if line.startswith("- "): s += f'<p class="li"><span>·</span>{inl(line[2:], cx)}</p>'
            else: s += f"<p>{inl(line, cx)}</p>"
        return s + "</div>"
    if t == "row":
        link = n.get("link", "arrow"); labs = n.get("labels", []); s = f'<div class="fr"{wstyle(n)}>'
        for i, c in enumerate(n["items"]):
            if i > 0:
                lab = labs[i - 1] if i - 1 < len(labs) else ""
                s += f'<div class="fc {link}{" lab" if lab else ""}"><span class="cl">{inl(lab, cx) if lab else ""}</span>'
                if link in ("vs", "plus", "eq"): s += f'<span class="sym">{ {"vs": "vs", "plus": "+", "eq": "="}[link] }</span>'
                elif link != "none": s += '<span class="ln"></span>'
                s += "</div>"
            s += node(c, cx)
        return s + "</div>"
    if t == "col":
        link = n.get("link", "arrow"); labs = n.get("labels", []); s = f'<div class="fv"{wstyle(n)}>'
        for i, c in enumerate(n["items"]):
            if i > 0:
                lab = labs[i - 1] if i - 1 < len(labs) else ""
                s += f'<div class="fvc {link}"><span class="vl"></span>' + (f'<span class="vlab">{inl(lab, cx)}</span>' if lab else "") + "</div>"
            s += node(c, cx)
        return s + "</div>"
    if t == "tree":
        s = f'<div class="ft"{wstyle(n)}><div class="ftr">{node(n["root"], cx)}</div><div class="ftk">'
        s += "".join(f'<div class="ftc">{node(c, cx)}</div>' for c in n["children"])
        return s + "</div></div>"
    if t == "table":
        s = f'<table class="ftb"{wstyle(n)}><tr>' + "".join(f"<th>{inl(h, cx)}</th>" for h in n["head"]) + "</tr>"
        for r in n["rows"]: s += "<tr>" + "".join(f"<td>{inl(c, cx)}</td>" for c in r) + "</tr>"
        return s + "</table>"
    if t == "note":
        return f'<p class="fn">{inl(n["text"], cx)}</p>'
    return ""

def head(num, title, sub, answer):
    tag = '<span class="ansbadge">정답</span>' if answer else ""
    return (f'<div class="stephead"><div class="stepnum"><span>Final</span>{num}</div>'
            f'<div class="steptitle"><h2>{html.escape(title)}{tag}</h2></div>'
            f'<div class="fsub">{html.escape(sub)}</div></div>')

def page_html(F, answer):
    cx = Ctx(answer)
    sub = F["title"] + (f' · {F["source"]}' if F.get("source") else "")
    dg = "".join(node(n, cx) for n in F["diagram"])
    a = f'<section>{head(1, "한눈에 보는 구조도", sub, answer)}<p class="finst">빈칸 {cx.n}개 · 지문을 보지 않고 채워 보세요.</p><div class="dg">{dg}</div></section>'
    rows = []
    for i, o in enumerate(F["ox"], 1):
        if answer:
            mk = lambda L: f'<span class="mk">{L}</span>' if o["ans"] == L else L
            oxc = f'{mk("O")}<i></i>{mk("X")}'
            tag = f'<span class="tag">{html.escape(o["tag"])}</span>' if o.get("tag") else ""
        else:
            oxc = "O<i></i>X"; tag = ""
        cx2 = Ctx(answer)
        rows.append(f'<tr><td class="n">{i}</td><td><p class="st">{inl(o["text"], cx2)}</p>'
                    f'<p class="why{"" if answer else " hid"}">{tag}{inl(o["why"], cx2)}</p></td><td class="ox">{oxc}</td></tr>')
    b = (f'<section class="pb">{head(2, "고난도 OX 20", sub, answer)}'
         '<p class="finst">개념의 범주·조건·시점·주체가 조금이라도 어긋나면 X. 아래 빈칸에 판단 근거를 쓰세요.</p>'
         f'<table class="fox">{"".join(rows)}</table></section>')
    return a + b

FCSS = f'''
.pb{{break-before:page;}}
.stephead{{position:relative;}}
.fsub{{position:absolute;right:0;bottom:2.2mm;font-family:"Lab";font-size:8.5pt;}}
.ansbadge{{font-family:"Lab";font-size:10pt;color:{RED};border:1pt solid {RED};padding:.2mm 1.6mm;margin-left:3mm;vertical-align:middle;}}
.finst{{font-family:"Lab";font-size:8.6pt;margin:-2.5mm 0 3.5mm;}}
.dg{{display:flex;flex-direction:column;gap:3.2mm;font-size:8.7pt;line-height:1.72;}}
.fs{{border:.8pt solid #000;break-inside:avoid;}}
.fsh{{background:#000;color:#fff;font-family:"Lab";font-size:9.3pt;padding:.9mm 2.6mm;line-height:1.4;}}
.fsh .bk{{border-bottom-color:#fff;}} .fsh .bk i{{color:#fff;}}
.fsb{{padding:3mm 3mm 3.2mm;display:flex;flex-direction:column;gap:2.6mm;}}
.fb{{border:.7pt solid #000;padding:1.6mm 2.4mm 1.8mm;flex:1 1 0;min-width:0;background:#fff;}}
.fb.round{{border-radius:3mm;}}
.fb.pill{{border-radius:20mm;text-align:center;padding:1.6mm 4mm;}}
.fb.dashed{{border-style:dashed;}}
.fb.bold{{border-width:1.7pt;}}
.fb.gray{{background:#ebebeb;}}
.fb.plain{{border:none;padding:0;}}
.fbt{{font-family:"Lab";font-size:9pt;text-align:center;border-bottom:.4pt solid #000;padding-bottom:.6mm;margin-bottom:1mm;line-height:1.45;}}
.fb.plain .fbt{{text-align:left;}}
.fb p{{margin:0;text-align:left;word-break:keep-all;}}
.fb.pill p{{text-align:center;}}
.fb .li{{padding-left:1em;text-indent:-1em;}}
.fb .li span{{display:inline-block;width:1em;text-indent:0;}}
.fr{{display:flex;align-items:stretch;min-width:0;}}
.fr > .fb,.fr > .fr,.fr > .fv,.fr > .ft,.fr > .ftb{{flex:1 1 0;}}
.fc{{flex:none;width:9mm;display:flex;flex-direction:column;align-items:center;justify-content:center;position:relative;}}
.fc.lab{{width:21mm;}}
.fc.none{{width:3mm;}}
.fc .cl{{font-family:"Lab";font-size:7.2pt;line-height:1.25;text-align:center;margin-bottom:.8mm;word-break:keep-all;}}
.fc .ln{{display:block;width:88%;height:0;border-top:.8pt solid #000;position:relative;}}
.fc.arrow .ln::after,.fc.both .ln::after{{content:"";position:absolute;right:-1px;top:-3.6px;border-left:6px solid #000;border-top:3.2px solid transparent;border-bottom:3.2px solid transparent;}}
.fc.back .ln::before,.fc.both .ln::before{{content:"";position:absolute;left:-1px;top:-3.6px;border-right:6px solid #000;border-top:3.2px solid transparent;border-bottom:3.2px solid transparent;}}
.fc .sym{{font-family:"Lab";font-size:8pt;width:6.4mm;height:6.4mm;border:.8pt solid #000;border-radius:50%;display:flex;align-items:center;justify-content:center;line-height:1;background:#fff;}}
.fv{{display:flex;flex-direction:column;align-items:stretch;min-width:0;}}
.fvc{{height:6.5mm;position:relative;display:flex;justify-content:center;}}
.fvc.none{{height:2mm;}}
.fvc .vl{{display:block;height:100%;border-left:.8pt solid #000;position:relative;}}
.fvc.none .vl{{border:none;}}
.fvc.arrow .vl::after{{content:"";position:absolute;bottom:-1px;left:-3.9px;border-top:6px solid #000;border-left:3.2px solid transparent;border-right:3.2px solid transparent;}}
.fvc .vlab{{position:absolute;left:calc(50% + 2.5mm);top:50%;transform:translateY(-50%);font-family:"Lab";font-size:7.2pt;white-space:nowrap;}}
.ft{{display:flex;flex-direction:column;align-items:center;min-width:0;}}
.ftr{{display:flex;justify-content:center;position:relative;padding-bottom:4mm;max-width:100%;}}
.ftr::after{{content:"";position:absolute;bottom:0;left:50%;height:4mm;border-left:.8pt solid #000;}}
.ftk{{display:flex;align-items:stretch;width:100%;}}
.ftc{{flex:1 1 0;min-width:0;position:relative;padding:4mm 1.2mm 0;display:flex;}}
.ftc > *{{flex:1 1 0;}}
.ftc::before{{content:"";position:absolute;top:0;left:50%;height:4mm;border-left:.8pt solid #000;}}
.ftc::after{{content:"";position:absolute;top:0;left:0;right:0;border-top:.8pt solid #000;}}
.ftc:first-child::after{{left:50%;}}
.ftc:last-child::after{{right:50%;}}
.ftb{{width:100%;border-collapse:collapse;font-size:8.4pt;line-height:1.55;}}
.ftb th{{font-family:"Lab";font-weight:400;background:#ebebeb;border:.6pt solid #000;padding:1mm 1.2mm;}}
.ftb td{{border:.6pt solid #000;padding:1.1mm 1.6mm;vertical-align:middle;word-break:keep-all;}}
.ftb td:first-child{{font-family:"Lab";text-align:center;white-space:nowrap;}}
.fn{{font-size:8.2pt;line-height:1.6;border-left:2pt solid #000;padding-left:2mm;margin:0;}}
.bk{{display:inline-block;position:relative;border-bottom:.7pt solid #000;text-align:center;line-height:1.3;padding:0 .2em 0 .9em;text-indent:0;white-space:nowrap;vertical-align:baseline;min-height:1.3em;}}
.bk i{{position:absolute;left:.05em;top:-.2em;font-style:normal;font-family:"Lab";font-size:5.6pt;line-height:1;}}
.bk b{{color:{RED};font-weight:700;}}
.fox{{width:100%;border-collapse:collapse;font-size:9.1pt;line-height:1.55;}}
.fox tr{{break-inside:avoid;}}
.fox td{{border-bottom:.5pt solid #000;padding:1.5mm 1.6mm;vertical-align:top;}}
.fox tr:first-child td{{border-top:1.2pt solid #000;}}
.fox td.n{{font-family:"Lab";width:8mm;text-align:center;}}
.fox td.ox{{width:20mm;font-family:"Lab";text-align:center;white-space:nowrap;}}
.fox td.ox i{{display:inline-block;width:4mm;}}
.fox .st{{text-align:justify;}}
.fox .why{{font-size:8.3pt;line-height:1.5;color:{RED};margin-top:.8mm;min-height:2.6em;}}
.fox .why.hid{{color:transparent;border-bottom:.4pt dotted #999;}}
.fox .why.hid *{{color:transparent !important;border-color:transparent !important;}}
.mk{{color:{RED};border:1.1pt solid {RED};border-radius:50%;padding:0 1.1mm;}}
.tag{{font-family:"Lab";font-size:7.2pt;border:.6pt solid {RED};padding:0 1mm;margin-right:1.5mm;}}
'''

def cmd_render(fj, wd):
    F = json.load(open(fj, encoding="utf-8"))
    err, nb = validate(F)
    if err: print("검증 실패:", *err, sep="\n - "); sys.exit(1)
    S = load_sheet(wd); S.setup(wd)
    name = S.safe(F["title"])
    q, a = page_html(F, False), page_html(F, True)
    CS = S.css(q + a + "Final한눈에보는구조도고난도OX20정답0123456789") + FCSS
    outs = []
    with S.Renderer() as R:
        for body, suf, t in ((q, "_파이널", "파이널"), (a, "_파이널_정답", "파이널 정답")):
            pf = R.pdf(body, CS); out = os.path.join(S.WD, "out", name + suf + ".pdf")
            n = S.stamp([pf], out, f'{F["title"]} {t}'); outs.append((out, n))
    for out, n in outs: print("PDF", out, n, "쪽")
    print("빈칸", nb, "개 / OX", len(F["ox"]), "문항 (X", sum(o["ans"] == "X" for o in F["ox"]), "개)")

def cmd_textdump(fj):
    F = json.load(open(fj, encoding="utf-8"))
    for p, s in all_diagram_texts(F): print(f"{p}\t{s}")
    for i, o in enumerate(F["ox"]):
        print(f"ox[{i}].text\t{o['text']}"); print(f"ox[{i}].why\t{o['why']}")

if __name__ == "__main__":
    a = sys.argv[1:]
    if not a: print(open(__file__, encoding="utf-8").read(1400)); sys.exit(0)
    if a[0] == "render": cmd_render(a[1], a[2])
    elif a[0] == "textdump": cmd_textdump(a[1])
    elif a[0] == "check":
        e, nb = validate(json.load(open(a[1], encoding="utf-8")))
        print("검증 실패:", *e, sep="\n - ") if e else print(f"검증 통과 (빈칸 {nb}개)")
    else: sys.exit("명령: render | check | textdump")
