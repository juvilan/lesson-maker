# lesson-maker

수학 교사가 Reveal.js 기반 HTML 슬라이드/학습지/시험지를 생성·배포하는 시스템입니다.

## 진입점

- `lesson-maker/orchestrator.md`

## 출력 경로

- `lesson-maker/{subject}/output/slides/`
- `lesson-maker/{subject}/output/worksheet/`
- `lesson-maker/{subject}/output/exam/`
- `lesson-maker/{subject}/output/수행평가/`
- 중간 산출물: `lesson-maker/workspace/`

## 과목 플러그인

각 과목은 `{subject}/config/` 아래에 시각화/애니메이션 템플릿을 둡니다.

- `visuals.md`: 시각화 타입 목록 + 코드 패턴
- `animations.md`: 애니메이션 단계 구성 패턴

## 배포/도구

공통 도구는 `lesson-maker/_shared/tools/`에 있습니다.

- `deploy.py`: Google Drive 자동 배포
- `rename_output.py`: 출력 파일 네이밍 정돈
- `html_to_pdf.py`: Playwright 기반 PDF 변환

## 다른 기기에서 작업하기

슬라이드·학습지 HTML을 만들고 브라우저로 확인하는 것까지는 준비물 없이 됩니다.
**PDF 변환(`html_to_pdf.py`)에만** 아래 설치가 필요합니다.

```bash
git clone https://github.com/juvilan/lesson-maker.git
cd lesson-maker
pip install -r requirements.txt
playwright install chromium
```

### 저장소에 들어 있는 것 / 없는 것

| | 위치 | git |
|---|---|---|
| 교과서 PDF | `{subject}/book/` | ✅ 포함 — clone하면 따라옴 |
| 산출물(슬라이드·학습지·교사노트) | `{subject}/output/` | ✅ 포함 |
| 템플릿·에이전트 정의 | `_shared/` | ✅ 포함 |
| **교사용 지도서** | `{subject}/book/지도서/` | ❌ **제외** (용량 약 52MB) |

지도서는 성취기준 해설·지도상 유의점·문항 풀이가 들어 있어 수업 설계에 필요합니다.
새 기기에서는 Google Drive에서 직접 복사하세요.

```bash
mkdir -p ai-math-2022/book/지도서
cp ~/"내 드라이브(juvilan0429@gmail.com)/001_영일고/1_학교업무/01_수업/교과서/2022_인공지능수학/미래엔_인공지능수학 지도서(2022개정)"/*.pdf \
   ai-math-2022/book/지도서/
```

### 로컬 미리보기

`.claude/launch.json`에 정적 서버가 정의돼 있습니다. Claude Code에서 preview를 띄우거나,
직접 실행할 수도 있습니다.

```bash
python3 -m http.server 8765
```

슬라이드는 인터랙티브 요소가 있어 브라우저로 열어야 동작합니다.

