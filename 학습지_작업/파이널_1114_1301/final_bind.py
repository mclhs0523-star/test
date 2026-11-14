# 파이널 여러 개를 차례가 있는 한 권(문제지)과 정답 한 권으로 엮는다.
#   python3 -I final_bind.py 작업폴더 --title "책 제목" 01.json 02.json …
import sys, os, json, importlib.util

def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path); m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m); return m

def main():
    a = sys.argv[1:]; wd = a[0]; title = a[a.index("--title") + 1]
    files = [f for f in a[1:] if f.endswith(".json")]
    S = load("sheet", os.path.join(wd, "sheet.py")); FN = load("final", os.path.join(wd, "final.py"))
    sets = [json.load(open(f, encoding="utf-8")) for f in files]
    for i, F in enumerate(sets, 1):
        err, _ = FN.validate(F)
        if err: sys.exit(f"{i}번째 파이널 검증 실패: {err}")
    S.setup(wd); NAME = S.safe(title)
    heads = [{"no": f"{i:02d}", "title": F["title"]} for i, F in enumerate(sets, 1)]

    def parts(F, h, answer):
        html = FN.page_html(F, answer)
        k = html.index('<section class="pb">')
        dg, ox = html[:k], html[k:].replace('<section class="pb">', "<section>", 1)
        return dg.replace("<section>", "<section>" + S.head_html(h), 1), ox

    P = {ans: [parts(F, h, ans) for F, h in zip(sets, heads)] for ans in (False, True)}
    alltxt = "".join(d + o for v in P.values() for d, o in v)
    CS = S.css(alltxt + title + "차례본책정답과해설구조도OX20Final한눈에보는고난도0123456789·") + FN.FCSS
    outs = []
    with S.Renderer() as R:
        for ans in (False, True):
            pdfs = [(R.pdf(d, CS), R.pdf(o, CS)) for d, o in P[ans]]
            def entries(start):
                out, p = [], start
                for h, (dp, op) in zip(heads, pdfs):
                    out.append({"no": h["no"], "title": h["title"], "page": p,
                                "steps": [("구조도", p), ("OX 20", p + S.npages(dp))]})
                    p += S.npages(dp) + S.npages(op)
                return out
            kind = "answers" if ans else "body"
            t = R.pdf(S.toc_html(title, entries(1), kind), CS); tn = S.npages(t)
            ent = entries(1 + tn); t = R.pdf(S.toc_html(title, ent, kind), CS)
            assert S.npages(t) == tn, "차례 쪽수가 바뀜"
            suf = "정답" if ans else "문제"
            out = os.path.join(S.WD, "out", f"{NAME}_{suf}.pdf")
            n = S.stamp([t] + [x for pr in pdfs for x in pr], out, f"{title} {suf}")
            outs.append((out, n, ent))
    for out, n, ent in outs:
        print("PDF", out, n, "쪽")
        for e in ent: print("   ", e["no"], e["title"], e["page"], "쪽", " ".join(f"{x}:{y}" for x, y in e["steps"]))

if __name__ == "__main__": main()
