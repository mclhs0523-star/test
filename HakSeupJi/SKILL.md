---
name: "HakSeupJi"
description: "국어 지문으로 성공의 신화 양식 학습지 세트(Step 1~3, 정답과 해설)를 PDF·HWPX로 만들고(makeone), 여러 세트 한글 파일을 차례·연속 쪽 번호가 있는 본책과 답지로 엮고(bind), 지문 여러 개를 각각 세트로 만들어 바로 한 권으로 엮고(makeall), 지문 구조 도식화(빈칸)와 고난도 OX 20문항으로 된 파이널 정리를 만든다(final). 문제·해설은 마지막에 grammar-checker 스킬로 맞춤법을 자동 검사한다. 학습지, 변형문제, 파이널 정리, makeone, bind, makeall, final 요청에 사용."
---

# HakSeupJi (학습지 세트 만들기)

명령은 네 가지다.

| 명령 | 하는 일 | 사용자가 주는 것 |
|---|---|---|
| **makeone** | 지문 하나(또는 엮어 읽기 묶음)로 학습지 세트 1개를 만든다. | 지문 파일(txt·pdf·hwp 등)이나 붙여 넣은 글 + `makeone` |
| **bind** | makeone으로 만든 한글 파일(.hwpx) 여러 개를 본책 1권과 답지 1권으로 엮는다. | .hwpx 파일 여러 개 + `bind` (뒤에 책 제목을 붙여도 됨: `bind 2학기 독서 학습지`) |
| **makeall** | 지문 여러 개를 **각각** makeone으로 세트로 만든 뒤, 이어서 bind로 본책·답지까지 한 번에 만든다. | 지문 파일 여러 개 + `makeall` (뒤에 책 제목: `makeall 2학기 독서 학습지`) |
| **final** | 지문 하나로 **파이널 정리**를 만든다: ① 지문·정보 구조에 맞춘 도형 도식화(빈칸 30개 이상), ② 고난도 OX 20문항. 문제지 PDF와, 같은 지면에 정답을 빨간 글씨로 채운 정답 PDF가 나온다. | 지문 + `final` (makeone과 함께: `makeone final`) |

명령어 없이 "학습지 만들어줘"라고 하면 makeone, "엮어줘", "합쳐줘", "makebook"이라고 하면 bind로 처리한다. "각각 만들어서 엮어줘", "makeone 하고 bind", "한 권으로 만들어줘"처럼 지문 여러 개를 세트로 만들고 엮으라는 말은 makeall이다. "파이널", "구조도", "도식화", "최종 정리"는 final이다. `makeone final`처럼 함께 쓰면 같은 지문으로 둘 다 만든다(같은 작업 폴더). 지문이 여러 개인 final은 지문마다 하나씩 만든다. 지문 여러 개 + `makeone`만 쓰면 (가)(나)(다) 엮어 읽기 세트 **1개**다. 헷갈리면 한 줄로 어느 쪽인지 묻는다. 디자인과 구성은 이 문서와 `sheet.py`가 고정한다. 사용자가 바꾸라고 하지 않는 한 레이아웃·글꼴·문구를 바꾸지 않는다.

## 고정 양식 (바꾸지 말 것)

- A4, 흑백. 표지 없음. 모든 쪽 머리글은 왼쪽 로고와 가는 밑줄뿐이고, 바닥에 `- n -` 쪽 번호를 단다.
- 순서: Step 1 직접 정리하기 → Step 2 OX 정리와 빈칸 넣기 → Step 3 초고난도 변형문제 → 정답과 해설.
- Step 머리는 검은 사각형 안의 'Step / 숫자'와 제목만 있다. 설명글·부제목은 넣지 않는다.
- Step 1은 머리 아래 한 쪽 전체를 비워 둔다. 칸 나누기와 안내 문구는 넣지 않는다.
- Step 2는 1단이다. 묶음별 OX 표(번호 | 진술 | O X)와 '빈칸 넣기' 요약문으로 구성한다.
- Step 3은 2단(가운데 세로줄)이다. `[1~20] 다음 …를 읽고 물음에 답하시오.` 다음에 지문 전체, 이어서 20문항을 싣는다. 지문을 따로 떼어 앞에 두지 않는다.
- 정답과 해설은 2단이다. OX 정답표, X 진술 바로잡기, 빈칸 정답, 빠른 정답표, 문항별 해설 순서다.
- 글꼴: 본문은 나눔명조, 라벨(Step 머리, 문항 번호, 지시문, 표 머리, 정답표, 차례 등)은 돋움이다. PDF와 HWPX 모두 같다. 시스템 기본 글꼴(본고딕·Noto, 나눔고딕 등)은 라벨에 쓰지 않는다. 돋움은 굵은 꼴이 없으므로 보통 굵기로 쓰고 굵기 합성은 끈다. 돋움에 없는 글자(⑯~⑳ 등)만 `sheet.py`가 나눔명조로 자동으로 채운다. PDF에 Type 3 글꼴이 들어가면 글자가 윤곽선처럼 깨져 보이므로 `sheet.py`의 방식(실제 TrueType 삽입)을 바꾸지 않는다.
- 줄바꿈은 글자 단위, 양쪽 정렬이다(시험지와 같음).
- **bind 본책**: 첫 쪽(들)은 차례, 이어서 세트마다 Step 1~3. 각 세트 첫 쪽(Step 1) 위에 `01  세트 제목` 띠를 단다. 쪽 번호는 차례 쪽을 1로 해서 끝까지 이어진다. 차례에는 세트 번호·제목·시작 쪽과, 그 아래 `Step 1 n쪽 · Step 2 n쪽 · Step 3 n쪽`이 한 줄로 들어간다. 차례의 쪽 번호는 바닥 쪽 번호와 똑같다.
- **bind 답지**: 별도 파일. 차례(세트 번호·제목·쪽) 다음에 세트마다 `01  세트 제목` 띠 + 정답과 해설. 쪽 번호는 답지 안에서 1부터 다시 시작한다.

## 공통 준비 (makeone·bind 모두 처음에 한 번)

작업 목록을 만들고 시작한다. 스킬 경로 `SKD`는 스킬을 불러올 때 표시되는 'Base directory'다.

```bash
SKD="<Base directory>"
# 작업 폴더: claude.ai 채팅이면 /home/claude, Claude Code면 현재 폴더 아래 학습지_작업/
if [ -d /home/claude ] && [ -w /home/claude ]; then BASE=/home/claude; else BASE="$PWD/학습지_작업"; fi
WD="$BASE/학습지_$(date +%m%d_%H%M)"; mkdir -p "$WD"
if [ -f "$SKD/scripts/sheet.py" ]; then
  cp "$SKD/scripts/sheet.py" "$SKD/scripts/fonts.py" "$SKD/scripts/final.py" "$WD/"; cp "$SKD/assets/logo.png" "$WD/"
else  # SKILL.md만 설치된 경우: 아래 '내장 파일'을 꺼낸다
  python3 -I - "$SKD/SKILL.md" "$WD" <<'E'
import sys, re, base64
s = open(sys.argv[1], encoding="utf-8").read()
for name, body in re.findall(r"<!-- file: (\S+) -->\n```\w*\n(.*?)\n```", s, re.S):
    p = sys.argv[2] + "/" + name
    if name.endswith(".b64"): open(p[:-4], "wb").write(base64.b64decode(body))
    else: open(p, "w", encoding="utf-8").write(body + "\n")
    print("꺼냄", name)
E
fi
python3 -I "$WD/fonts.py" "$WD" "$SKD"
```

- `fonts.py` 출력이 `MISSING`이면 글꼴을 찾지 못한 것이다. **HakSeupJi.zip(인수인계 zip)을 채팅에 첨부해 달라**고 하고 기다린다. 그 안에 나눔명조·돋움이 들어 있다. 나눔글꼴 설치 파일(`NanumFontSetup_Win_TTF`)이나 돋움 TTF, 시험지 글꼴 ZIP(`02_돋움/dotum-Regular.ttf`가 든 것)을 받아도 된다. 설치 파일과 ZIP은 `fonts.py`가 실행하지 않고 안에서 TTF만 꺼낸다. 돋움 대신 다른 고딕체로 바꿔 진행하지 않는다.
- 사용자가 새 로고를 주면 흑백으로 바꿔 `$WD/logo.png`를 덮어쓴다.
  ```python
  from PIL import Image
  im = Image.open(src).convert("RGBA"); bg = Image.new("RGBA", im.size, (255,255,255,255)); bg.alpha_composite(im)
  bg.convert("L").point(lambda v: 0 if v < 90 else (255 if v > 235 else int((v-90)/145*255))).save(WD + "/logo.png")
  ```
- 참고 시험지: `$SKD/reference/시험지_스타일_분석.md`가 있으면 문제를 쓰기 전에 읽는다. `$SKD/reference/`에 시험지 PDF가 있거나 사용자가 시험지 PDF를 첨부했으면 그것도 훑어보고 발문·<보기>·선지의 말투를 맞춘다. 레이아웃은 학습지 고정 양식을 따른다.

## makeone 작업 순서

1. **준비**: 위 '공통 준비'.
2. **지문 읽기**: 첨부 파일(txt, pdf, hwp 등)이나 붙여 넣은 글에서 지문을 읽는다. 첫 줄 제목과 `N문단` 같은 표시는 지우고 문단만 남긴다. **본문 글자는 한 글자도 바꾸지 않는다.**
   - 지문이 여러 개면 (가), (나), (다)… 순서를 붙인다. 파일 이름 앞 번호(01, 02, 03)가 있으면 그 순서를 따른다. 지문이 하나면 라벨을 붙이지 않고 `label`을 빈 문자열로 둔다.
   - 원문에 있는 ㉠ 같은 표시는 살린다. 지문마다 ㉠이 따로 있으면 전체에서 겹치지 않게 ㉠, ㉡, ㉢…으로 다시 매긴다. 표시 뒤 낱말에는 밑줄을 친다(`㉠ [u]낱말[/u]`).
   - 어휘 문항용으로 ⓐ~ⓔ 다섯 곳을 골라 `ⓐ[u]낱말[/u]`처럼 표시한다. 여러 지문이면 지문들에 고루 나눈다. 바꿔 쓸 한자어가 분명히 있는 고유어 동사가 좋다(예: 깨질 → 와해될).
   - 표시를 넣을 때는 `str.replace`로 넣고, 원문에서 그 구절이 꼭 한 번만 나오는지 `assert`로 확인한다.
3. **내용 쓰기**: 아래 '문제 작성 기준'에 따라 `$WD/content.json`을 쓴다(스키마는 아래). Python으로 딕셔너리를 만들어 `json.dump(..., ensure_ascii=False)`로 저장한다.
4. **검토**: '검토 체크리스트'를 문항마다 실제로 확인하고 고친다. `python3 -I "$WD/sheet.py" check "$WD/content.json"`로 형식도 확인한다.
5. **맞춤법 검사 (마지막 검사, 항상 자동으로)**: 사용자가 따로 말하지 않아도 매번 한다. 건너뛰지 않는다.
   - `python3 -I "$WD/sheet.py" textdump "$WD/content.json" > "$WD/textdump.txt"`로 지문을 뺀 모든 글(OX 진술·바로잡기, 빈칸 요약문, 발문, <보기>, 선지, 해설)을 위치 표시와 함께 뽑는다.
   - **grammar-checker 스킬로 검사한다.** 순서대로 찾아 처음 되는 것을 쓴다.
     1. 스킬 목록에 `grammar-checker`가 있으면 Skill 도구로 불러 그 지침대로 `textdump.txt`를 검사한다.
     2. 없으면 `$SKD/../grammar-checker/SKILL.md`(같은 zip·같은 스킬 폴더에 함께 설치됨)를 Read로 읽고, 그 안에서 가리키는 `references/rules.md`, `references/common-errors.md`도 읽은 뒤 그 기준으로 검사한다.
     3. 둘 다 없으면 아래 '맞춤법 검사 기준'으로 검사한다.
   - grammar-checker의 '확신도 높음'(규정으로 판정되는 맞춤법·띄어쓰기·문장부호·호응 오류)만 content.json에서 고친다. '중간·낮음'과 권장 사항은 고치지 않는다. 위치 표시(`questions[3].opts[2]` 등)대로 Python으로 고치고 다시 저장한다. 문체·어휘는 바꾸지 않는다. 고친 뒤 정답 근거가 그대로인지 확인하고 `check`를 다시 돌린다.
   - **지문 본문은 고치지 않는다.** 지문에서 오류로 보이는 곳은 최종 답변에서 알리기만 한다.
   - 고친 곳은 `위치: 고치기 전 → 고친 뒤 (이유)` 꼴로 `$WD/맞춤법_검사.txt`에 적어 둔다(전달할 때 고친 곳 수를 알리는 근거).
6. **조판**: `python3 -I "$WD/sheet.py" makeone "$WD/content.json" "$WD"`. 검증 실패 메시지가 나오면 내용을 고쳐 다시 돌린다. HWPX 안에는 content.json이 함께 저장되어 나중에 bind에 쓰인다.
7. **눈으로 확인**: `pdftoppm -r 45 -png`로 모든 쪽을 그림으로 만들어 한 장에 이어 붙여 본다. 이어서 문항 쪽 한두 장을 `-r 75`로 크게 본다. 문항이 단 경계에서 잘리지 않았는지, <보기> 표가 넘치지 않는지, 빈 쪽이 생기지 않았는지 확인한다. `pdffonts` 결과에 `Type 3`이 없어야 한다.
8. **전달**: `$WD/out/` 안의 PDF와 HWPX를 SendUserFile로 한 번에 보낸다. 답변은 짧게: 지문 수와 엮은 방식, 쪽수, 비교 문항 수, 맞춤법 검사에서 고친 곳 수(지문에서 발견한 의심 부분이 있으면 그 목록)를 알리고, HWPX는 한글에서 직접 열어 보지 못했다는 점을 한 줄로 밝힌다. 여러 세트를 만들 계획이면 나중에 HWPX들을 첨부하고 `bind`라고 치거나, 처음부터 지문들을 한꺼번에 주고 `makeall`이라고 치면 된다고 한 줄 안내한다.

## bind 작업 순서

1. **준비**: 위 '공통 준비'.
2. **파일 모으기**: 첨부된 `.hwpx`를 모은다. 같은 채팅에서 makeone으로 만든 세트는 `$WD/out` 이전 폴더의 HWPX나 content.json을 써도 된다.
   - `.hwp`(옛 형식)는 읽지 못한다. 한글에서 '다른 이름으로 저장 → HWPX'로 바꿔 다시 첨부해 달라고 한다.
   - **순서**: 사용자가 순서를 말하면 그대로. 아니면 파일 이름 앞 번호(01_, 1., ①) 순, 번호가 없으면 파일 이름 가나다순. 정한 순서는 최종 답변에 적는다.
   - **책 제목**: `bind` 뒤에 쓴 말이 있으면 그것. 없으면 `학습지 모음`으로 하고, 답변에서 바꿀 수 있다고 알린다.
3. **엮기**: `python3 -I "$WD/sheet.py" bind "$WD" --title "책 제목" 파일1.hwpx 파일2.hwpx …` (적은 순서대로 엮인다)
   - 출력에 `NEED_JSON 파일 → 추출.txt`가 나오면, 그 HWPX에는 content.json이 없다(한글에서 고쳐 다시 저장했거나 예전 버전으로 만든 파일). 추출된 txt를 읽고 같은 내용의 content.json을 되살려 `$WD/세트이름.json`으로 저장한 뒤, 명령에서 그 HWPX 대신 json 경로를 넣어 다시 실행한다.
     - txt 구조: `section0`=Step 1, `section1`=OX 표(번호, 진술, `O X`가 줄마다)와 빈칸 요약문(`( ① ______ )`→`( ① )`로 되돌림), `section2`=지시문·지문(라벨 `(가)` 등)·문항(`n. 발문 [x.x점]`, `<보기>`, ①~⑤), `section3`=정답과 해설(OX 정답, X 바로잡기, 빈칸 정답, 빠른 정답, 해설).
     - 글자는 txt 그대로 옮긴다(선생님이 한글에서 고친 내용이 반영되어야 함). 밑줄 정보는 txt에 없으므로 발문의 '적절하지 않은/가장 적절한/일치하지 않는', ㉠·ⓐ 뒤 낱말에만 `[u]…[/u]`를 다시 넣는다. 세트 제목(`title`)은 파일 이름에서 `_학습지세트`를 뗀 것으로 한다.
   - 검증 실패가 나오면 그 세트의 문제를 알려 주고, 고칠 수 있으면 고쳐 다시 돌린다.
4. **눈으로 확인**: 본책과 답지의 차례 쪽, 각 세트 첫 쪽을 `-r 60`으로 보고, 차례의 쪽 번호가 실제 바닥 쪽 번호와 맞는지 두세 곳 대조한다. 전체를 `-r 30`으로 이어 붙여 빈 쪽이 없는지 본다. `pdffonts`에 `Type 3`이 없어야 한다.
5. **전달**: `$WD/out/`의 `{제목}_본책.pdf`, `{제목}_본책.hwpx`, `{제목}_답지.pdf`, `{제목}_답지.hwpx`를 한 번에 보낸다. 답변은 짧게: 엮은 순서(번호·제목·시작 쪽), 본책·답지 쪽수. 그리고 한 줄로 "차례의 쪽 번호는 PDF 기준이며, 한글에서 HWPX를 열면 줄 간격 차이로 쪽이 밀릴 수 있으니 차례 쪽 번호를 한 번 확인해 달라"고 알린다.

## makeall 작업 순서 (makeone 여러 번 + bind 한 번)

1. **준비**: '공통 준비'를 한 번 한다. 세트마다 `$WD/세트01/`, `$WD/세트02/`… 하위 폴더를 만들고 `sheet.py`, `fonts.py`, `logo.png`, `fonts/`를 복사해 둔다(또는 `fonts.py`를 각 폴더에 다시 돌린다).
2. **지문 나누기**: 첨부 파일 하나가 세트 하나다. 순서는 파일 이름 앞 번호(01_, 1., ①) → 없으면 이름순 → 사용자가 말한 순서가 있으면 그것. 붙여 넣은 글이면 `---`나 `[지문 1]`처럼 사용자가 나눈 대로 나눈다.
   - 사용자가 "1·2번은 엮어 읽기로"처럼 말하면 그 지문들은 한 세트((가)(나))로 묶는다.
   - 시작하기 전에 `세트 01: 파일이름 / 세트 02: …` 계획을 한 줄씩 알리고 바로 진행한다(묻지 않음).
3. **세트마다 makeone 2~7단계**: 지문 읽기 → 내용 쓰기 → 검토 → **맞춤법 검사(grammar-checker, 자동)** → 조판 → 눈으로 확인. 각 세트 폴더에서 돌린다. 세트 하나가 끝날 때마다 `세트 02/05 완료`처럼 짧게 알린다.
4. **bind**: `python3 -I "$WD/sheet.py" bind "$WD" --title "책 제목" "$WD/세트01/out/"*_학습지세트.hwpx "$WD/세트02/out/"*_학습지세트.hwpx …` (세트 순서대로). 책 제목은 `makeall` 뒤에 쓴 말, 없으면 `학습지 모음`. 이어서 bind 4단계(눈으로 확인)를 한다.
5. **전달**: 세트별 PDF·HWPX와 `{제목}_본책`, `{제목}_답지`의 PDF·HWPX를 SendUserFile로 한 번에 보낸다. 세트가 많으면(6개 이상) 본책·답지 4개를 먼저 보내고 세트별 파일은 한 번 더 묶어 보낸다. 답변은 짧게: 세트 순서(번호·제목·시작 쪽), 본책·답지 쪽수, 세트별 맞춤법 고친 곳 수, 지문 의심 부분.

## final 작업 순서 (파이널 정리)

1. **준비**: '공통 준비'. makeone과 함께 하면 같은 `$WD`를 쓴다.
2. **지문 읽기**: makeone 2단계와 같다(본문 글자는 바꾸지 않음). 지문을 문단별로 다시 읽고 아래 '구조 분석'을 먼저 메모한다.
3. **구조 분석 (도식화 설계)**: 바로 그리지 말고 먼저 정한다.
   - 글 전체의 흐름: 문단마다 하는 일(문제 제기, 개념 정의, 대비, 해결책, 절차, 사례, 한계, 결론)과 문단 사이 관계.
   - 정보 구조: 각 문단 안의 핵심 개념 관계가 어떤 모양인지 고른다. 모양에 맞는 도형을 쓴다.

     | 정보 구조 | 쓸 노드 |
     |---|---|
     | 대립·대비 (A와 B) | `row` + `link:"vs"`, 한쪽은 `shape:"gray"` |
     | 절차·인과·시간 순서 | `row`(가로) 또는 `col`(세로) + `link:"arrow"`, 화살표 위 `labels`에 조건·시점 |
     | 요건 결합 (A와 B를 모두 갖추면 C) | `row`(`plus`)로 요건을 묶고, 바깥 `row`(`arrow`)로 결과 상자에 잇는다 |
     | 상위 개념 → 하위 갈래·분류 | `tree` |
     | 여러 대상의 여러 기준 비교 | `table` (첫 열은 대상 이름) |
     | 핵심 정의·결론 | `box` + `shape:"bold"` |
     | 조건·예외·주의 | `box` + `shape:"dashed"` 또는 `note` |
     | 문단 흐름 요약 | 맨 위 `section` 안에 `pill` 상자들을 `arrow`로 |
   - 문단(또는 의미 덩어리)마다 `section` 하나. 제목 띠에 `n문단 · 그 문단이 하는 일`을 쓴다. 맨 위에는 '글 전체' 흐름 section을 둔다.
   - 한 상자에 4줄 넘게 넣지 않는다. 길면 상자를 나누거나 표로 바꾼다. 문장 대신 '개념 → 결과', 'A: 설명'처럼 압축한다.
4. **빈칸 뚫기**: 구조도 글 안에 `{{정답}}`으로 표시한다. 40~70개를 목표로 한다(최소 30).
   - 뚫을 것: 핵심 개념어, 요건·조건, 시점(다음 날, ~한 날), 주체·대상, 범위(정해진 금액까지, 원칙적으로), 관계어(선순위/후순위, 뒤에), 숫자.
   - 정답은 지문의 표현 그대로 쓰고 짧게(1~8글자). 한 줄에 빈칸이 셋을 넘지 않게 하고, 빈칸만 남아 무엇을 묻는지 모르는 줄은 만들지 않는다.
   - 상자 제목은 대부분 남긴다(실마리). 같은 낱말을 여러 번 뚫어도 된다(반복 점검).
5. **고난도 OX 20**: 아래 '파이널 OX 작성 기준'을 따른다. 각 문항에 `ans`, `why`(X는 바로잡기, O는 근거와 함정 포인트), `tag`(함정 유형 한두 낱말)를 쓴다.
6. **final.json 저장**: 스키마는 `final.py` 머리 주석에 있다(아래 예시 참고). 견본은 `$SKD/assets/final_sample.json`.
   ```json
   {"title":"주택 임대차 보호","source":"2023 3월 고2 21~25",
    "diagram":[{"type":"section","title":"1문단 · 임차권은 왜 약한가","items":[
      {"type":"row","link":"vs","items":[
        {"type":"box","title":"채권","body":["- 특정한 {{채무자}}에게만 요구","- 예: ㉠ {{임차권}}"]},
        {"type":"box","title":"물권","shape":"gray","body":["- {{누구에게나}} 주장"]}]}]}],
    "ox":[{"text":"…","ans":"X","tag":"시점","why":"…"}]}
   ```
   `python3 -I "$WD/final.py" check "$WD/final.json"`로 확인한다(빈칸 30개 이상, OX 20개, X 8~12개).
7. **맞춤법 검사 (자동)**: `python3 -I "$WD/final.py" textdump "$WD/final.json" > "$WD/final_textdump.txt"`로 뽑아 makeone 5단계와 같은 방법(grammar-checker)으로 검사한다. 빈칸 정답(`{{…}}` 안)은 지문 표현이므로 고치지 않는다.
8. **조판**: `python3 -I "$WD/final.py" render "$WD/final.json" "$WD"` → `$WD/out/{title}_파이널.pdf`(문제지), `{title}_파이널_정답.pdf`(같은 지면에 빈칸 정답·OX 정답·근거를 빨간 글씨로).
9. **눈으로 확인**: 두 PDF의 모든 쪽을 `pdftoppm -r 70`으로 본다. 상자 글이 넘치거나 겹치지 않는지, 화살표 방향이 맞는지, 빈칸 번호가 이어지는지, 정답 글씨가 빈칸 안에 들어가는지 본다. 문제가 있으면 상자를 나누거나 `w`(가로 비율)를 조정해 다시 조판한다.
10. **전달**: 두 PDF를 SendUserFile로 보낸다. 답변은 짧게: 쪽수, 빈칸 수, OX의 O/X 수와 함정 유형 분포, 맞춤법 고친 곳 수. 파이널은 PDF만 만든다(HWPX 없음)는 점을 한 줄로 밝힌다.

## 파이널 OX 작성 기준 (1등급컷 70점짜리 시험을 낸다는 생각으로)

- **범주를 정확히 가른다.** 개념의 정의·요건·효과·적용 범위를 지문 그대로 쪼갠 뒤, 그중 하나만 살짝 어긋나게 만든다. 조금이라도 어긋나면 X다. 'A의 효력을 준다'와 'A가 된다', '원칙적으로'와 '언제나', '~할 수 있다'와 '~한다'를 구분한다.
- **학생이 실수하는 지점을 노린다.** 문항마다 하나 이상:
  - 개념 혼동: 이름이 비슷하거나 함께 나오는 두 개념의 요건·효과를 맞바꾼다.
  - 요건 바꾸기·빼기·더하기: 필요 없는 요건을 넣거나(동의 필요), 요건 하나를 빼거나, 다른 개념의 요건으로 바꾼다.
  - 시점: 그날/다음 날, 종료 전/후, 먼저/나중. 날짜를 주고 직접 따지게 한다.
  - 순위·범위: 누구보다 앞서는지, 어디까지인지(전액/정해진 금액까지), 모든/일부.
  - 단정: '~할 수 있다', '~하지 못할 수 있다'를 '~한다', '~할 수 없다'로.
  - 주체·대상 뒤집기, 원인과 결과 뒤집기, 지문에 없는 내용 끼워 넣기(지문 밖).
  - 맞는 진술도 함정처럼: 표현을 바꾸어 틀려 보이지만 맞는 O 문항을 8개 안팎 둔다. 지문 문장을 그대로 옮긴 O는 쓰지 않는다.
- **추론형을 섞는다.** 날짜·금액·순서가 든 짧은 가상 사례 진술을 5개 이상 넣는다. 지문의 규칙을 적용해야만 판단되게 한다.
- 진술은 한두 문장, '~이다/~한다'로 끝맺는다. X는 8~12개. 같은 함정 유형이 세 문항 넘게 이어지지 않게 한다.
- `why`: X는 '무엇이 어떻게 틀렸고 지문은 뭐라고 했는지', O는 '근거 문단과 헷갈리는 이유'를 1~2문장으로.
- **스스로 점검**: 문항마다 지문의 어느 문장으로 O/X가 갈리는지 짚는다. 해석에 따라 O도 X도 될 수 있는 문항은 고치거나 버린다.

## 맞춤법 검사 기준 (grammar-checker를 찾지 못했을 때만)

국립국어원 규정(한글 맞춤법, 표준어 규정, 문장 부호, 외래어 표기법)을 기준으로 한다.
- 오류만 고친다. 문체·어조·어휘 선택은 바꾸지 않는다. 규정으로 판정되는 것만 오류로 단정하고, 갈리거나 허용인 것은 고치지 않는다. 확신이 없으면 고치지 않는다.
- 볼 것: 되/돼, 안/않, 로서/로써, 던/든, 데/대, 율/률 같은 혼동; 의존 명사(것, 수, 줄, 뿐, 만큼)·보조 용언·단위 명사 띄어쓰기; 쉼표·마침표·따옴표; 주술 호응, 조사 오용, 이중 피동, 시제·높임 불일치, 중복 표현.
- 인용한 지문 표현, 고유명사, ㉠·ⓐ 표시와 `[u]` 태그는 건드리지 않는다.

## content.json 스키마

```json
{
 "title": "협력과 경쟁",
 "passages": [{"label": "가", "title": "원래 제목", "paras": ["문단1 …ⓐ[u]뜯어내[/u]…", "문단2"]}],
 "ox": [{"group": "(가)", "text": "진술", "ans": "O", "why": "근거나 바로잡은 내용"}],
 "blanks": [{"group": "(가)", "text": "요약문 … ( ① ) … ( ② ) …"}],
 "blank_answers": ["자연 상태", "조건부 협동가"],
 "questions": [
  {"stem": "(가)에 대한 이해로 [u]적절하지 않은[/u] 것은?", "pts": 4.5,
   "box": {"kind": "text", "paras": ["…"]},
   "opts": ["선지1", "선지2", "선지3", "선지4", "선지5"], "ans": 1,
   "exp": "해설"}
 ]
}
```
- `title`: 지문들을 아우르는 짧은 주제(파일 이름이 `{title}_학습지세트`가 된다). 단일 지문이면 그 글의 핵심 화제로 정한다.
- 인라인 표시는 `[u]…[/u]`(밑줄)와 `[b]…[/b]`(굵게)만 쓴다. 문항 발문에서 `적절하지 않은`, `가장 적절한`, `일치하지 [u]않는[/u]`은 반드시 밑줄을 친다.
- `box.kind`는 세 가지다.
  - `text`: `paras` 목록
  - `list`: `items`에 `[["ㄱ","…"],["ㄴ","…"]]` 또는 `[["Ⅰ","서론: …"]]`
  - `table`: `intro`(선택), `head`, `rows`, `note`(선택)
- `blanks`의 빈칸은 정확히 `( ① )` 꼴(괄호, 공백, 원문자, 공백, 괄호)로 쓴다. 전체 번호는 ①부터 이어지고 20개를 넘지 않는다.
- `ans`는 1~5다. 선지는 화면에 나올 순서 그대로 쓴다.

## 문제 작성 기준

참고 시험지는 고등학교 정기시험(독서와 작문) 스타일이다(자세한 분석은 `reference/시험지_스타일_분석.md`). 발문은 짧고 정형적이며 배점을 `[4.5점]`처럼 붙인다. 선지는 한두 문장이고 '~겠군.', '~이다.', '~한다.'로 끝맺는다.

### Step 2
- **OX**: 24~30개, O와 X를 대략 반씩 둔다. X 진술은 숫자·주체·순서·인과·범위 가운데 하나만 살짝 비틀어 만들고, `why`에 바로잡은 내용을 쓴다. O 진술의 `why`는 근거 문단을 적는다(예: "3문단.").
  - 여러 지문: 지문별 묶음 `(가)`, `(나)`… 7~8개씩 두고, 마지막에 `엮어 읽기` 묶음 4~5개를 둔다.
  - 단일 지문: 문단 범위로 묶는다(`1~2문단`, `3~4문단`…). 마지막 묶음은 `글 전체`(구조·관점 진술)로 한다.
- **빈칸**: 묶음마다 핵심을 요약한 2~5문장에 빈칸을 3~6개 넣는다. 전체 15~20개다. 정답은 지문에 나온 핵심어 그대로 쓴다. 여러 지문이면 마지막에 `엮어 읽기` 요약 한 덩어리를 둔다.

### Step 3: 20문항, 100점
- 배점은 4.5/5.0/5.5점으로 합이 100이다. 어려운 <보기>·비교 문항은 5.5, 단순 이해는 4.5로 준다.
- 정답 번호는 ①~⑤가 정확히 4개씩이다. 같은 번호가 세 문항 넘게 연속되지 않게 한다. ⓐ~ⓔ, ㉠~㉢처럼 선지 순서가 정해진 문항은 그 순서를 지킨다.
- '적절하지 않은 것' 문항이 대부분이고, '가장 적절한 것' 문항을 4~6개 섞는다.

**여러 지문(엮어 읽기)일 때의 구성**: 비교 문항을 8~11개 넣는다. 예시 구성은 다음과 같다.
1. (가)~(다)의 서술 방식 비교 (가장 적절한)
2~4. (가) 이해 / (가) <보기> 표·수치 적용 / (가) <보기> 실험·사례 적용
5~8. (나) 일치 / (나) <보기> 분류(ㄱ~ㄹ) / (나) <보기> 변형 사례 / (나) 과정·단계 정리
9~10. (다) 이해 / (다) <보기> 감상·적용
11~15. 두 지문 비교: 개념 대응((가)의 A와 (나)의 B), (가) 글쓴이가 (나)를 읽고 보일 반응, 관점 비교, 문단끼리의 공통 생각, 다른 대상끼리의 유비
16. ㉠~㉢ 통합 이해
17. 세 지문으로 <보기>의 생활 사례 이해
18. 외부 이론 <보기>(예: 액설로드의 맞대응 전략)와 두 지문 연결. 계산이나 따져 보기가 필요한 함정을 둔다.
19. 문맥상 ⓐ~ⓔ와 바꿔 쓰기에 가장 적절한 것
20. (가)~(다)를 활용한 글쓰기 개요의 자료 활용 방안

지문이 두 개면 같은 틀에서 비교 문항 비중을 유지한다. 넷 이상이면 지문별 단독 문항을 2~3개로 줄인다.

**단일 지문일 때의 구성**: 발문은 '윗글'로 쓴다. 비교 대신 <보기>와의 비교·적용으로 깊이를 낸다.
1. 윗글의 내용 전개 방식 (가장 적절한)
2~3. 윗글의 내용과 일치하지 않는 것 / 윗글을 이해한 내용
4~5. 핵심 개념 이해 / 두 개념(입장) 비교
6. ㉠의 이유 또는 ㉠~㉢ 이해
7~12. <보기> 적용 6문항: 표·그래프 수치 해석, 가상 실험, 실제 사례, 변형 사례, 분류(ㄱ~ㄹ), 다른 관점의 글
13~15. 윗글의 관점에서 <보기>를 평가 / <보기>의 관점에서 윗글 비판 / 윗글과 <보기> 비교
16~17. 문단 간 관계·추론 / 글쓴이가 동의하지 않을 진술
18. 생활 사례에 적용 (종합)
19. 문맥상 ⓐ~ⓔ 바꿔 쓰기
20. 윗글을 활용한 글쓰기 개요의 자료 활용 방안

### 초고난도 함정 (문항마다 하나 이상)
- 주체 바꾸기: 처벌하는 쪽과 처벌받는 쪽을 뒤집는다.
- 추측을 단정으로: 원문의 '아마도 ~일 것이다'를 '단정하고 있다'로 바꾼다.
- 시간·순서 비틀기: '이때부터'를 '~한 이후에야'로 바꾼다.
- 같은 현상, 다른 원인: 거절이 드문 이유가 처벌 성향이 약해서가 아니라 제안이 후해서인 경우.
- 목적 혼동: 같은 모방이라도 포식자 회피인지 공격을 위한 접근인지.
- 계산해야 풀리는 선지: <보기>의 점수표·금액으로 이익과 손해를 직접 따져야 알 수 있게 한다.
- 범위 과장('모든', '항상', '전면 부정'), 근거 없는 인과, 지문에 없는 평가 끼워 넣기.
- 오답 선지도 그럴듯한 말과 지문의 표현을 섞어 쓴다. 지문 문장을 그대로 베낀 선지는 쉬운 문항에만 쓴다.

### 해설
- 정답이 왜 정답인지를 근거 문단과 함께 2~4문장으로 쓴다. 헷갈릴 만한 오답이 있으면 한 문장 덧붙인다.
- 해설에는 선지 번호(①~⑤)를 쓰지 않는다. 내용으로 가리킨다. 정답 번호는 `build.py`가 자동으로 붙인다.

### 문장
- 자연스러운 한국어로 쓴다. '~에 의해', '~를 통해' 남발, 이중 피동, '~라고 할 수 있다' 같은 번역투와 상투어를 피한다. 한 문장에 정보를 셋 넘게 담지 않는다.
- <보기> 사례와 외부 이론은 사실에 맞게 쓴다. 가상의 실험·사회는 '가상의', '가정한다'를 밝힌다.

## 검토 체크리스트 (조판 전에 문항마다 확인)
- 정답이 하나뿐인가? '적절하지 않은' 문항이면 나머지 네 선지가 모두 지문(과 <보기>)으로 분명히 뒷받침되는가? '가장 적절한' 문항이면 나머지 넷이 모두 분명히 틀렸는가?
- 정답 근거가 지문의 특정 문장으로 짚이는가? 해설이 그 근거를 대는가?
- 비교 문항의 두 지문 연결이 억지스럽지 않은가?
- 지문 본문이 원문과 같은가? 표시만 더했는가?
- 정답 분포는 각 4개이고 배점 합은 100인가?


## 내장 파일

SKILL.md만 설치되어 `scripts/` 폴더가 없을 때 '공통 준비' 단계가 아래 블록을 파일로 꺼낸다. 내용을 고치지 말 것.

### sheet.py — 조판(makeone·bind, PDF·HWPX)
<!-- file: sheet.py -->
```python
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
```

### final.py — 파이널 정리 조판(구조도·OX, PDF)
<!-- file: final.py -->
```python
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
```

### fonts.py — 나눔명조·돋움 준비
<!-- file: fonts.py -->
```python
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
```

### logo.png.b64 — 성공의 신화 로고(흑백 PNG, base64)
<!-- file: logo.png.b64 -->
```text
iVBORw0KGgoAAAANSUhEUgAAAeAAAABoAgMAAABULssHAAAADFBMVEX////m5uYiIiIAAABvMfoL
AAALsklEQVR42u2aX4hc133HP+dm7l3sDfVAdxVLClEhjps4xltKoBAHfNw6lOKHTMjcsT0SWCFW
Eq0UNKXUBJKidR7Sh5ZmTLSS6+QhhdU6O7PB4zQKNU481xCS9KVZHBOMa9o1bGRLsyYDXWx5ZnZ+
fTj3nHvuzF3HDamShz2wzMy95/x+5/z+/75nYX/sj/2xP/bH/vh9Gyr9qMaArLevM+PwIm1AVVnt
XNdzL8bpl9radT1x8E8N+zv6aPL/w6hegfH92e8SQKkB8xpoM9Q+Y1UFWQdgXjN8x2qY19BL/GXq
hIZfWqKybhi/i/llw7jdLvsEDrXgl+sAhx6tjpY71Ct5DpcbhWJsaeTPAQ4sV+X5DqA0sA6g1ub1
0+YwHFRdabXqrZaMm8d9Cl0RWQJQXZGxRnUlP5qFB54VkWsAnBERDRCI/XZYRDbTiTcHV411xa1N
n7ESf90uzEzwNS+nxhER2bIExoBZOXZ7WbKMow3LKsc4yK27Zij6Y1ys4jP2UDMi8pYjsOukqFPj
evevOqoaQ3v4FD+aICIAzAEjKE+8HBYzLgMda7pDct+UBknMgwNf/ly4FgNx7+65NyqZ7Ya5ddvT
HKSYsQb6dgd91AMVFBC1gPu9ZSf17L2p7Ha+p7wQMuOMZEFENuDshKh3ihl3rfaPiMgmN/rKCVKa
Aag/Tt5vdcy/y6d1zslH7leBF28XB6VUmmb0+YAvozClGUDYUf9Qsqy+q68VWWolk+H/ZZSBhErR
qxKUkvqHrdWoF//rvZkFzdkMwjxQEEv7b5fx3Bw9wZC++RR1Yt0GgnDw0tlJOodiX4bvcEgmqNyq
IamoSwC3/sUukGhQXzt2KclJatv6kAA1P6PpQrWnzpCNPZJOCWB4EDjfONEMOfk3/UnNVhwF8euE
RfctThNCjuYekh/NZaIGtQKD05+6sH1SR/eU8/44t4dFZQKsX2Q1AcJKmr/KPgHZww9KdkLvYG37
X0+C7lOsUplOlSRAdBHqvQa0KjzSmT5xMuP/+lY5c8wb1CsisvG3a9WDIvL3SdMP1bKjUtffzace
l0DOiHkQuNB9xkZxkyP8zHKFhTRHuN11/rTWex4gKeeMpDQZl+cyzUkCURMg0knoplTyghrXfKPW
qaAc3ecO89DPCwwvLAoKI6/YSLWSlCxjpc0Da1bDNlCrMjzqG0AJlPGkEuFH8ixuAVCKPX1GgGp6
yqVycfwwm1lcBjjqWUvgRPJugrmCOOksbOQ9zWK0aloFlOzjG5xHOHEeWgaoN9Pnic+YL1lOE0b9
aHF4TBNsCLQTp/nMCCopqRGgLqZpML9+ZM7+34kGSD5qOYSG8a01iFayE+tsEyMIYXD+P7eM8szj
474NmgNrSzFR1rWdNHTyjbx4+FA6e9jhSHHi2YY5eDWZ8W1QLTmjswmh6vTyJ1lZZbkfZ/UbAKNk
Qnu2MigQdQeOw7eMAdnQHeXkxQiCZs5czfQAkA1jEqsNoKQn5EN00a+1lHahxwRISYzs7JwPpvMq
Ttw3eLtVQNBa8Yxr95yxEptN1Aq2jri/KMu8olSUoLRjnE6xguIhJ6hbJvJWGFeNxDTAH/7i3Gm/
kqlrYJBoP+nP69To59MUPXxKM0wzqp4Q1I3axsAmMOyYxaGVfwlGkGiiu1Tzr/tI8mdm/QrAqG90
YoJg1LJEF9Oc+Mp3/SgmgDqHTe0r7zVSUBp4/PSBK4D+yZRxEQ8PSh9KRqYnAPhmx0/oB6cSZL/k
9K40JHCo4jRkzt5HAYPT9BJQqdNsp4wTAFV/XY/gJk+X0nnNCEZ7DjqZ5Lf9FBKtZFandMUptufX
ne7Emj5sw0P5FA7DZJBtIimoCJKSvwWBkxqg18/MMXHNQL5ICEAggd4SoQbx0/irSAPeptTrmz+V
Cyuw/ppfDZf9mrxk1wUAl+yrPtxknAJAjpuWdlvpPbsVvBQyTFlJZ+iSkCTuJHpK1GX68IM/AlXK
ReRhApeTPcplvKIhhG0vbw+ScQLwnF/VQxkkXdBJRa1Anh3BcxvIJ97lCFwA5Cj01V7Fc6rjUl4b
j0Hj1zYeAUD/doQvMfhpmdHIne5qA+Dy0SQ126laxFVDZeNYI+sL8KITdb6jSiNCYhhvvD5iWO2d
uvCgpv+xm+xx7jOfq7VGvnnLRi/LwJ7DX05gkOR1kzq62en5Wiql0ugugtonj4b/otnV5deM1lat
dnvJDLCdL+cB5ELarFeMtrdNBXgMkGNbhout/5Y4aHcvp1yymnleduNWq/WgyPObtwDMjNOiIY7j
CpHIoBhmOSyygxIZc0Rkk8CCH0RduRaZundBRN5CGXyia4vgEnDP4zclutV67vbjcOmvKv8IjO9r
A+qByrxm2GlHFVvCE8cAvWc61iFDDqWq7BPC8Jix7GNbtvLpA1FLVada7OCi2jkrIle7IuN7lxad
LapF28afyx6lgNPVisMMVp8U2WFBZIOZbKqqr8wYzGDWA4mU1xlwSPNvC7ZdOKJdQuVUBiDYaiR7
NKhYxiIimyyINJm1GnI9x5aPUe2SY7wGXzicvrp2R1YLHvBaD4MZcTTXjVgkTESWOCuyxI0xKo5j
nTHeTDuhFDIJMloETXjfX9qdfxGidN2TU0halMO4tMVZRMYYxqmYdIazbbg5ItIkcHAORITMPpK+
enSHclom5rjIhu3GsrGZPdqCs4af8mC3I2l/tpDBcRnjgBIl3nzQOK1cepm5NMUcnGpnVB5FuRmL
i7LuwmMEDMgH6RdtZDG52YaiG1hsqh0DFr51eClo3d0EX0BOyRNI5q5FV+UK0DWyn/XQrwU7xyht
oA2JHSfq2zR/Z4hu3YF62ohaTXOZQDKNkuvGwFUq4SMeNnvGOteBrvWMWe91oG/THLm7KyLy6NOw
FmjfUboZXHq2CLpVtbUKGeMFj/J8XPVQ1ReYYKyWypqZzTMishttoT4eOV+Qq3Ecx/VueryuiMig
1Wq1nkx9KAf07nrYYwGOvGTB6o0M70oY3HyhCa/OryPPRK7pks92XBGZJtthfR0IF5vsjZ8WN1oT
gFCASgB5+M4EOfaZhntZBi6b2PqEV4GcXwcYXiigPpwqsN4O7ypRIu4lfOfSvVu9H3/vK4Sf+L7r
b9dzeE8IrvizLUacKyiKoYMK3Ga7j5e8fUV0NyB4Sz1bOdOE2V0j6rNZBEqDwowXddLbigPdSQy5
O3VfcMr3jQVnGqW09ho//LXa6z/8Sr7/LsBi8sJ74NeDm8E5XxsVJ3NH7cL/NA7fOqGH9A4qzMSt
nA9OA0t9W+0tZmij3BfuuaWIrgZUd/lZDQSpqLuZXxw1kWvWBQ3zaDwRZDanw47s5qPOtW5Ggohu
HFfhkGzBfFzzGA+qALWuUe6siMiVKhDWui675hkHb894x1U+RtQthnefevXUL6if0HhXOuFqLb2v
cwDTgdWagTNhOIWIF7lYec8pEV1b3dRFRDyrzqfFmambkGAqc06e+JrLiSIi8kpWgJSAXhtVXfxB
JzpB25nRxP4b05dML0+U+J0CAHI0YX/vy/lITVVpn/znzsk7zyf0khsHAJ1cUBwn021bw6+059/R
rcFTd3j7DzSRXL0Yd88P4np7qFOQZnb6gmk6Q2cjLUBmJ0S9mVs09iqfElJJhrX5eyrHXnh8fqlb
hwcfA3gzR/ebAMc3i/oXG2/GRZcPHXpe/zHweqES8tK372/TXn74P776s8V1VOuNxwDGDU/Wg4bp
0/3+5dgEjyfytwK2f/P7nvYM8HLmNHWAcO0DrQoQLeup6taW1X7YXcmzMA3GZJFyZWJzM1kWV0Dw
9Wc6cPjUH5yGuPSEnXXU0V5NgeawVZl8NHlHlTNJeWIiQ87ucPU9/k1Oq1VFtTS1Vis7iaobwxhk
3UGYNjWD5d/sPxRCV+yb4KOqqnq58fnH6pV2TidxWIG269cAVZ3X0B7+9v5bJGzpcnRRc/1H1ORD
15OvK1kGL3Bn8rtgzPdrt/M7GdEa+2N/7I/9sT9+L8f/Ao1osaNFCR8VAAAAAElFTkSuQmCC
```
