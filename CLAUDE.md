# HakSeupJi 패키지

이 폴더는 '성공의 신화' 국어 학습지 스킬 패키지다.

- 처음 열었거나 사용자가 "세팅해 줘"라고 하면 `00_클로드가_먼저_읽을_것.md`의 **A. Claude Code** 순서를 따른다(핵심: `bash setup.sh`).
- 사용자가 `makeone`, `bind`, `makeall`, `final` 또는 "학습지 만들어줘"라고 하면 HakSeupJi 스킬을 쓴다. 스킬 목록에 없으면 `HakSeupJi/SKILL.md`를 Read로 읽고 따른다('Base directory'는 이 폴더의 `HakSeupJi`).
- 맞춤법 검사 단계는 항상 grammar-checker 스킬로 한다. 목록에 없으면 `grammar-checker/SKILL.md`를 읽고 따른다.
- 선생님께 보여 줄 사용법은 `01_선생님용_사용안내.md`에 있다.
