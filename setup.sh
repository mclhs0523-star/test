#!/usr/bin/env bash
# HakSeupJi 자동 세팅 (Claude Code용)
#   bash setup.sh            스킬 설치 + 필요한 프로그램 설치 + 점검
#   bash setup.sh --quick    스킬 설치만 (세션 시작 훅에서 사용, 몇 초)
# 하는 일
#   1) HakSeupJi, grammar-checker 스킬을 ~/.claude/skills/ 에 복사한다(예전 이름 학습지세트만들기·korean-grammar-checker는 지운다).
#   2) Python 모듈(fonttools, playwright, pypdf, reportlab, lxml, pillow) 중 없는 것을 설치한다.
#   3) Chromium이 없으면 playwright로 설치한다.
#   4) 샘플 데이터로 makeone·bind·final을 돌려 결과물이 나오는지 점검한다.
set -u
HERE="$(cd "$(dirname "$0")" && pwd)"
DEST="${CLAUDE_SKILLS_DIR:-$HOME/.claude/skills}"
MODE="${1:-full}"

say() { printf '%s\n' "$*"; }

# 1) 스킬 복사
mkdir -p "$DEST"
for old in "학습지세트만들기" "korean-grammar-checker"; do
  [ -e "$DEST/$old" ] && rm -rf "$DEST/$old" && say "예전 스킬 지움: $old"
done
for s in HakSeupJi grammar-checker; do
  if [ ! -f "$HERE/$s/SKILL.md" ]; then say "실패: $HERE/$s/SKILL.md 가 없음"; exit 1; fi
  if [ -L "$DEST/$s" ]; then rm -f "$DEST/$s"; else rm -rf "$DEST/$s"; fi
  cp -R "$HERE/$s" "$DEST/$s"
done
say "스킬 설치: $DEST/HakSeupJi, $DEST/grammar-checker"
[ "$MODE" = "--quick" ] && exit 0

# 2) Python 모듈
PY="$(command -v python3 || command -v python || true)"
if [ -z "$PY" ]; then say "실패: python3가 없습니다. https://www.python.org 에서 설치한 뒤 다시 실행하세요."; exit 1; fi
need=()
for pair in fontTools:fonttools playwright:playwright pypdf:pypdf reportlab:reportlab lxml:lxml PIL:pillow; do
  mod="${pair%%:*}"; pkg="${pair##*:}"
  "$PY" -c "import $mod" 2>/dev/null || need+=("$pkg")
done
if [ ${#need[@]} -gt 0 ]; then
  say "Python 모듈 설치: ${need[*]}"
  "$PY" -m pip install -q "${need[@]}" 2>/dev/null \
  || "$PY" -m pip install -q --user "${need[@]}" 2>/dev/null \
  || "$PY" -m pip install -q --user --break-system-packages "${need[@]}" \
  || { say "실패: pip 설치가 안 됩니다. 직접 실행: $PY -m pip install ${need[*]}"; exit 1; }
fi

# 3) Chromium (PDF 조판용)
if ! "$PY" - <<'E' 2>/dev/null
import os
from playwright.sync_api import sync_playwright
chrome = next((p for p in ("/usr/bin/google-chrome", "/usr/bin/chromium", "/usr/bin/chromium-browser") if os.path.exists(p)), None)
with sync_playwright() as p:
    p.chromium.launch(**({"executable_path": chrome} if chrome else {})).close()
E
then
  say "Chromium 설치 중(처음 한 번, 1~2분)…"
  "$PY" -m playwright install chromium >/dev/null || { say "실패: Chromium 설치. 직접 실행: $PY -m playwright install chromium"; exit 1; }
fi

# 4) 점검
SKD="$DEST/HakSeupJi"; T="$(mktemp -d)"
cp "$SKD/scripts/sheet.py" "$SKD/scripts/fonts.py" "$SKD/scripts/final.py" "$SKD/assets/logo.png" "$T/"
"$PY" -I "$T/fonts.py" "$T" "$SKD" >"$T/log.txt" 2>&1 \
 && "$PY" -I "$T/sheet.py" makeone "$SKD/assets/selftest_content.json" "$T" >>"$T/log.txt" 2>&1 \
 && "$PY" -I "$T/sheet.py" bind "$T" --title 점검 "$T"/out/*_학습지세트.hwpx "$SKD/assets/selftest_content.json" >>"$T/log.txt" 2>&1 \
 && "$PY" -I "$T/final.py" render "$SKD/assets/final_sample.json" "$T" >>"$T/log.txt" 2>&1
n=$(ls "$T/out" 2>/dev/null | grep -c -E '\.(pdf|hwpx)$' || true)
if [ "$n" -ge 8 ]; then
  say "점검 통과: 학습지 세트·본책·답지 PDF/HWPX, 파이널 PDF 생성 확인"
  if command -v pdffonts >/dev/null; then
    t3=$(pdffonts "$T/out/점검_본책.pdf" | grep -c "Type 3" || true); say "Type 3 글꼴: $t3개 (0이어야 정상)"
  else
    say "참고: pdftoppm/pdffonts(poppler)가 없어 결과 그림 확인은 생략됩니다. (Mac: brew install poppler / Ubuntu: sudo apt install poppler-utils)"
  fi
  rm -rf "$T"
else
  say "점검 실패. 로그:"; tail -20 "$T/log.txt"; exit 1
fi
say "완료. 새 세션부터 HakSeupJi·grammar-checker 스킬이 목록에 보입니다."
