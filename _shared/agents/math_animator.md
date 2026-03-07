# 수학 애니메이션 에이전트

## 역할
수학 수업의 핵심 계산 과정을 단계별로 보여주는 GSAP 애니메이션을 생성.
교사가 클릭(또는 N 키)으로 한 단계씩 진행하며 설명할 수 있도록 설계.
**실제 숫자로 계산 과정이 눈에 보이게** 하는 것이 최우선 목표.

**과목 플러그인**에서 해당 과목의 애니메이션 패턴을 로드하여 사용한다.
플러그인이 없으면 아래 범용 애니메이션 패턴을 적용한다.

---

## 입력
- `workspace/{session_id}/merged_context.json`
- `subject_plugin_path`: subjects/{subject}/ 경로
- `output_path`: workspace/{session_id}/math_animations.json

---

## 처리 순서

### Step 1: 플러그인 로드
`{subject_plugin_path}/animations.md` 를 읽어
해당 과목의 애니메이션 카탈로그와 패턴을 파악한다.

### Step 2: 애니메이션 계획 수립
`merged_context.json`의 각 핵심 개념에 대해:
1. 몇 단계 애니메이션이 필요한가?
2. 각 단계에서 어떤 숫자 계산이 보여야 하는가?
3. 계산 추적 표의 컬럼은 무엇인가?
4. 플러그인 패턴이 있으면 사용, 없으면 범용 패턴 사용

> **역할 경계**: 계산 과정을 단계별로 채워나가는 표(`calc-table`)는
> 항상 이 에이전트(math_animator)가 생성합니다.
> visual_creator는 계산 표를 생성하지 않습니다.

### Step 3: 코드 생성
MathStepAnimator 클래스 (`templates/math_animation_lib.js`)를 기반으로 생성.

---

## 범용 애니메이션 패턴

### 패턴 A: 수식 단계별 전개
수식의 변환 과정을 한 단계씩 보여줌.
모든 과목에서 사용 가능.

```html
<!-- HTML 컴포넌트 구조 -->
<div id="anim-{{anim_id}}">
  <!-- 수식 단계들 -->
  <div id="step-{{anim_id}}-1" class="step-box" style="opacity:0; transform:translateY(10px)">
    <div class="step-label">Step 1 — {{step1_title}}</div>
    \[ {{step1_formula}} \]
  </div>
  <div id="step-{{anim_id}}-2" class="step-box" style="opacity:0; transform:translateY(10px)">
    <div class="step-label">Step 2 — {{step2_title}}</div>
    \[ {{step2_formula_general}} \]
    <div id="step-{{anim_id}}-2-num" style="opacity:0; color:#f39c12;">
      \[ {{step2_formula_with_numbers}} \]
    </div>
  </div>
  <!-- ...추가 단계 -->
  <div id="step-{{anim_id}}-result" class="step-box" style="opacity:0; transform:translateY(10px)">
    <div class="step-label">결과</div>
    <span class="big-result">{{final_result}}</span>
  </div>

  <!-- 컨트롤 -->
  <div class="anim-ctrl">
    <button class="abtn" id="btn-prev-{{anim_id}}" onclick="slideAnims['{{anim_id}}'].prev()" disabled>◀ 이전</button>
    <span class="step-cnt" id="step-cnt-{{anim_id}}">0 / {{total_steps}}</span>
    <button class="abtn" id="btn-next-{{anim_id}}" onclick="slideAnims['{{anim_id}}'].next()">다음 ▶</button>
    <button class="abtn gray" onclick="slideAnims['{{anim_id}}'].reset()">↺</button>
  </div>
</div>
```

```javascript
// GSAP 스크립트
(function() {
  const steps = [
    // Step 1: 일반 수식 등장
    () => {
      gsap.to('#step-{{anim_id}}-1', { opacity: 1, y: 0, duration: 0.7, ease: 'power2.out' });
      MathJax.typesetPromise();
    },
    // Step 2: 숫자 대입
    () => {
      gsap.to('#step-{{anim_id}}-2', { opacity: 1, y: 0, duration: 0.7 });
      gsap.to('#step-{{anim_id}}-2-num', { opacity: 1, duration: 0.7, delay: 0.4 });
      MathJax.typesetPromise();
    },
    // ... 추가 단계
    // 결과 등장
    () => {
      gsap.to('#step-{{anim_id}}-result', {
        opacity: 1, y: 0, duration: 0.8, ease: 'back.out(1.5)'
      });
    }
  ];
  window.slideAnims['{{anim_id}}'] = new StepAnimBasic('{{anim_id}}', steps);
})();
```

---

### 패턴 B: 계산 표 점진적 채우기
계산 과정을 표로 보여주면서 단계별로 셀을 채워나감.
수열, 확률, 행렬 계산 등에 사용.

```html
<!-- 계산 추적 표 -->
<table class="calc-table" id="tbl-{{anim_id}}">
  <thead>
    <tr>{{column_headers}}</tr>
  </thead>
  <tbody>
    <!-- 각 행은 하나의 계산 예시 -->
    <tr>
      {{given_values_as_td}}
      <td class="fillable" id="cell-{{anim_id}}-0-{{col}}">?</td>
    </tr>
    <!-- 추가 행 -->
  </tbody>
</table>
```

```javascript
// 셀 채우기 헬퍼
function fillCell(id, val, color = '#fff') {
  const el = document.getElementById(id);
  if (!el) return;
  gsap.to(el, {
    backgroundColor: 'rgba(243,156,18,0.3)', duration: 0.3,
    onComplete: () => {
      el.textContent = val;
      el.style.color = color;
      el.classList.add('filled');
      gsap.to(el, { backgroundColor: 'transparent', duration: 0.5 });
    }
  });
}
```

---

### 패턴 C: 그래프 위 점 단계별 추가
함수 그래프에 점을 하나씩 찍거나, 접선을 그려나가는 패턴.
수학I, 수학II, 미적분에서 사용.

애니메이션 단계:
1. 함수 그래프 표시
2. 특정 x값 강조
3. 해당 점 마킹
4. 접선/법선 추가
5. 기울기 수치 표시

---

### 패턴 D: 좌표계 벡터 애니메이션
벡터를 하나씩 그려나가면서 합성/분해를 보여줌.
기하 과목에서 사용.

```javascript
// p5.js 기반 벡터 그리기
function drawVector(p, ox, oy, vx, vy, color, label, scale) {
  const ex = ox + vx * scale;
  const ey = oy - vy * scale; // y축 반전
  p.stroke(color); p.strokeWeight(2.5);
  p.line(ox, oy, ex, ey);
  // 화살표 머리
  const angle = Math.atan2(oy - ey, ex - ox);
  p.push();
  p.translate(ex, ey);
  p.rotate(-angle);
  p.fill(color); p.noStroke();
  p.triangle(0, 0, -10, 4, -10, -4);
  p.pop();
  // 라벨
  if (label) {
    p.fill(color); p.noStroke();
    p.textSize(13);
    p.text(label, ex + 6, ey - 4);
  }
}
```

---

## StepAnimBasic 헬퍼 클래스

`templates/math_animation_lib.js`의 `MathStepAnimator` 클래스를 사용한다.
이 라이브러리는 `templates/reveal_base.html`에서 이미 로드되므로
슬라이드 HTML에 별도 인라인할 필요 없이 바로 참조 가능하다.

```javascript
// 사용 예시 (슬라이드 스크립트에서)
const anim = new MathStepAnimator('{{anim_id}}', { speed: 'normal' });
anim.addStep({ id: 1, effect: 'formula_appear', latex: '...' });
anim.addStep({ id: 2, effect: 'number_substitute', ... });
// HTML: <button onclick="mathAnimators['{{anim_id}}'].next()">다음 ▶</button>
```

---

## 애니메이션 설계 원칙
- **클릭당 1~2개 요소만** 등장 (한꺼번에 너무 많이 나오지 않게)
- **일반 수식 먼저, 숫자 대입 나중**에 보여주기
- 각 단계 지속시간: 0.6~1.0초
- 계산 표는 모든 애니메이션에 동반 권장
- MathJax 재렌더링: 수식이 새로 등장할 때마다 `MathJax.typesetPromise()` 호출

---

## 출력
`schemas/math_animations.json` 스키마에 맞게
`workspace/{session_id}/math_animations.json`에 저장.

**ID 계약**: `merged_context.json`의 `animation_requirements[].animation_id`를 그대로 사용.
직접 새 ID를 생성하지 마세요.
