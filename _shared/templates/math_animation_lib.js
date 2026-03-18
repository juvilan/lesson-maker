/**
 * MathStepAnimator - 인공지능 수학 수업용 단계별 계산 애니메이션 라이브러리
 * 의존성: GSAP (gsap.min.js), MathJax 3.x
 *
 * 사용법:
 *   const anim = new MathStepAnimator('my-animation', { speed: 'normal' });
 *   // HTML에서: <button onclick="mathAnimators['my-animation'].next()">다음 ▶</button>
 */

class MathStepAnimator {
  constructor(animationId, options = {}) {
    this.id = animationId;
    this.currentStep = -1;
    this.totalSteps = 0;
    this.steps = [];
    this.options = {
      speed: options.speed || 'normal',   // 'slow' | 'normal' | 'fast'
      autoPlay: options.autoPlay || false,
      highlightColor: options.highlightColor || '#f39c12',
      resultColor: options.resultColor || '#2ecc71',
      ...options
    };
    this.speedMap = { slow: 1.5, normal: 0.8, fast: 0.4 };
    this.duration = this.speedMap[this.options.speed];

    // 레지스트리에 등록
    if (!window.mathAnimators) window.mathAnimators = {};
    window.mathAnimators[animationId] = this;
  }

  /**
   * 단계 정의 추가
   * @param {Object} stepConfig - { id, latex, numericText, effect, tableUpdate, highlightIds }
   */
  addStep(stepConfig) {
    this.steps.push(stepConfig);
    this.totalSteps = this.steps.length;
    return this;
  }

  /** 다음 단계로 진행 */
  next() {
    if (this.currentStep < this.totalSteps - 1) {
      this.currentStep++;
      this._playStep(this.steps[this.currentStep]);
      this._updateButtons();
    }
  }

  /** 이전 단계로 되돌리기 */
  prev() {
    if (this.currentStep > 0) {
      this.currentStep--;
      this._resetToStep(this.currentStep);
      this._updateButtons();
    }
  }

  /** 처음부터 재시작 */
  reset() {
    this.currentStep = -1;
    const container = document.getElementById(`anim-${this.id}`);
    if (container) {
      // 모든 단계 숨기기 (step-box visible 클래스 제거)
      container.querySelectorAll('.step-box, .anim-step').forEach(el => {
        el.classList.remove('visible');
        el.style.opacity = '0';
        el.style.transform = 'translateY(10px)';
      });
      // 모든 테이블 셀 초기화
      container.querySelectorAll('.calc-table td.fillable').forEach(td => {
        td.textContent = '?';
        td.classList.remove('filled', 'highlighted', 'result-cell');
      });
      // 노드 비활성화
      container.querySelectorAll('.nn-node').forEach(n => n.classList.remove('active', 'fired'));
      // 엣지 비활성화
      container.querySelectorAll('.nn-edge').forEach(e => e.classList.remove('active'));
    }
    this._updateButtons();
  }

  // ─────────────────────────────────────────────
  // 내부 메서드
  // ─────────────────────────────────────────────

  _playStep(step) {
    const d = this.duration;

    switch (step.effect) {
      case 'formula_appear':
        this._formulaAppear(step, d);
        break;
      case 'number_substitute':
        this._numberSubstitute(step, d);
        break;
      case 'highlight_term':
        this._highlightTerm(step, d);
        break;
      case 'box_result':
        this._boxResult(step, d);
        break;
      case 'node_activate':
        this._nodeActivate(step, d);
        break;
      case 'arrow_flow':
        this._arrowFlow(step, d);
        break;
      case 'table_row_fill':
        this._tableRowFill(step, d);
        break;
      case 'graph_point_appear':
        this._graphPointAppear(step, d);
        break;
      default:
        this._formulaAppear(step, d);
    }

    // 테이블 업데이트가 있으면 함께 실행
    if (step.tableUpdate) {
      setTimeout(() => this._fillTableCell(step.tableUpdate), d * 600);
    }

    // MathJax 재렌더링 (수식이 새로 등장한 경우)
    if (step.latex && window.safeTypeset) {
      gsap.delayedCall(d * 0.5, () => safeTypeset());
    }
  }

  /** 수식 등장 애니메이션 */
  _formulaAppear(step, d) {
    const el = document.getElementById(`step-${this.id}-${step.id}`);
    if (!el) return;
    el.classList.add('visible');
    gsap.fromTo(el,
      { opacity: 0, y: 15 },
      { opacity: 1, y: 0, duration: d, ease: 'power2.out' }
    );
  }

  /** 변수→숫자 대입 애니메이션 */
  _numberSubstitute(step, d) {
    const formulaEl = document.getElementById(`step-${this.id}-${step.id}-formula`);
    const numEl = document.getElementById(`step-${this.id}-${step.id}-numeric`);

    if (formulaEl) {
      gsap.fromTo(formulaEl,
        { opacity: 0, y: 10 },
        { opacity: 1, y: 0, duration: d * 0.6, ease: 'power2.out' }
      );
    }
    if (numEl) {
      gsap.fromTo(numEl,
        { opacity: 0, x: -10, color: '#aaa' },
        { opacity: 1, x: 0, duration: d, delay: d * 0.5,
          color: this.options.highlightColor, ease: 'power2.out' }
      );
    }
  }

  /** 특정 항 강조 */
  _highlightTerm(step, d) {
    if (step.highlightIds) {
      step.highlightIds.forEach((id, i) => {
        const el = document.getElementById(id);
        if (!el) return;
        gsap.to(el, {
          backgroundColor: this.options.highlightColor,
          color: '#000',
          borderRadius: '4px',
          padding: '2px 6px',
          duration: d * 0.5,
          delay: i * 0.15
        });
      });
    }
    this._formulaAppear(step, d);
  }

  /** 결과 박스 강조 */
  _boxResult(step, d) {
    const el = document.getElementById(`step-${this.id}-${step.id}`);
    if (!el) return;
    gsap.fromTo(el,
      { opacity: 0, scale: 0.9 },
      { opacity: 1, scale: 1, duration: d,
        ease: 'back.out(1.5)',
        onComplete: () => {
          gsap.to(el, {
            boxShadow: `0 0 0 3px ${this.options.resultColor}`,
            borderRadius: '8px',
            duration: d * 0.5
          });
        }
      }
    );
  }

  /** 신경망 노드 활성화 */
  _nodeActivate(step, d) {
    if (step.nodeIds) {
      step.nodeIds.forEach((id, i) => {
        const node = document.getElementById(id);
        if (!node) return;
        gsap.to(node, {
          backgroundColor: this.options.highlightColor,
          boxShadow: `0 0 12px ${this.options.highlightColor}`,
          duration: d * 0.4,
          delay: i * 0.2,
          onComplete: () => node.classList.add('active')
        });
      });
    }
    this._formulaAppear(step, d);
  }

  /** 엣지(화살표) 흐름 애니메이션 */
  _arrowFlow(step, d) {
    if (step.edgeIds) {
      step.edgeIds.forEach((id, i) => {
        const edge = document.getElementById(id);
        if (!edge) return;
        gsap.fromTo(edge,
          { strokeDashoffset: 100 },
          { strokeDashoffset: 0, duration: d, delay: i * 0.15, ease: 'none',
            onStart: () => edge.classList.add('active') }
        );
      });
    }
  }

  /** 계산 표 셀 채우기 */
  _tableRowFill(step, d) {
    if (step.tableUpdate) {
      const { tableId, values, rowIndex } = step.tableUpdate;
      const table = document.getElementById(tableId);
      if (!table) return;
      const rows = table.querySelectorAll('tbody tr');
      if (rows[rowIndex]) {
        const cells = rows[rowIndex].querySelectorAll('td.fillable');
        values.forEach((val, i) => {
          if (cells[i]) {
            setTimeout(() => {
              gsap.to(cells[i], {
                backgroundColor: this.options.highlightColor + '44',
                duration: d * 0.3,
                onComplete: () => {
                  cells[i].textContent = val;
                  cells[i].classList.add('filled');
                  gsap.to(cells[i], { backgroundColor: 'transparent', duration: d * 0.5 });
                }
              });
            }, i * 200);
          }
        });
      }
    }
  }

  /** 그래프 포인트 등장 */
  _graphPointAppear(step, d) {
    const el = document.getElementById(`point-${this.id}-${step.id}`);
    if (!el) return;
    gsap.fromTo(el,
      { scale: 0, opacity: 0 },
      { scale: 1, opacity: 1, duration: d, ease: 'elastic.out(1, 0.5)' }
    );
  }

  /** 특정 단계까지 되돌리기 (prev 사용 시) */
  _resetToStep(targetStep) {
    const container = document.getElementById(`anim-${this.id}`);
    if (!container) return;

    // 모든 단계 초기화 후 0~targetStep 재생
    this.reset();
    this.currentStep = -1;
    for (let i = 0; i <= targetStep; i++) {
      this.currentStep = i;
      this._playStep(this.steps[i]);
    }
  }

  /** 이전/다음 버튼 상태 업데이트 */
  _updateButtons() {
    const prevBtn = document.getElementById(`btn-prev-${this.id}`);
    const nextBtn = document.getElementById(`btn-next-${this.id}`);
    const counter = document.getElementById(`step-counter-${this.id}`);

    if (prevBtn) prevBtn.disabled = this.currentStep <= 0;
    if (nextBtn) nextBtn.disabled = this.currentStep >= this.totalSteps - 1;
    if (counter) counter.textContent = `${this.currentStep + 1} / ${this.totalSteps}`;
  }

  /** 테이블 단일 셀 채우기 */
  _fillTableCell({ tableId, row, col, value }) {
    const table = document.getElementById(tableId);
    if (!table) return;
    const rows = table.querySelectorAll('tbody tr');
    if (rows[row]) {
      const cells = rows[row].querySelectorAll('td');
      if (cells[col]) {
        gsap.to(cells[col], {
          backgroundColor: this.options.highlightColor + '55',
          duration: 0.3,
          onComplete: () => {
            cells[col].textContent = value;
            cells[col].classList.add('filled');
            gsap.to(cells[col], { backgroundColor: 'transparent', duration: 0.5 });
          }
        });
      }
    }
  }
}

// ─────────────────────────────────────────────────────
// 신경망 다이어그램 헬퍼 클래스
// ─────────────────────────────────────────────────────

class NeuralNetDiagram {
  /**
   * @param {string} containerId - SVG를 삽입할 컨테이너 ID
   * @param {number[]} layers    - 각 레이어 노드 수 [2, 3, 1]
   * @param {Object}   options
   */
  constructor(containerId, layers, options = {}) {
    this.containerId = containerId;
    this.layers = layers;
    const container = document.getElementById(containerId);
    const cw = container ? container.clientWidth : 600;
    const ch = container ? container.clientHeight : 350;
    this.options = {
      width: options.width || Math.min(cw, 600),
      height: options.height || Math.min(ch, 350),
      nodeRadius: options.nodeRadius || Math.min(28, Math.min(ch, 350) / 12),
      nodeColor: options.nodeColor || '#2c3e50',
      edgeColor: options.edgeColor || '#7f8c8d',
      activeNodeColor: options.activeNodeColor || '#f39c12',
      activeEdgeColor: options.activeEdgeColor || '#e74c3c',
      labelFontSize: options.labelFontSize || 13,
      showWeights: options.showWeights !== false,
      showValues: options.showValues !== false,
      ...options
    };
    this.nodes = [];
    this.edges = [];
    this._render();
  }

  _render() {
    const { width, height, nodeRadius } = this.options;
    const container = document.getElementById(this.containerId);
    if (!container) return;

    const svg = document.createElementNS('http://www.w3.org/2000/svg', 'svg');
    svg.setAttribute('width', width);
    svg.setAttribute('height', height);
    svg.setAttribute('viewBox', `0 0 ${width} ${height}`);
    svg.setAttribute('preserveAspectRatio', 'xMidYMid meet');
    svg.style.overflow = 'hidden';

    const layerCount = this.layers.length;
    const xStep = width / (layerCount + 1);
    const layerLabels = ['입력층', '은닉층', '출력층'];

    // 노드 위치 계산
    this.nodePositions = this.layers.map((nodeCount, li) => {
      const x = xStep * (li + 1);
      const yStep = height / (nodeCount + 1);
      return Array.from({ length: nodeCount }, (_, ni) => ({
        x, y: yStep * (ni + 1), layer: li, index: ni
      }));
    });

    // 엣지 그리기
    for (let li = 0; li < layerCount - 1; li++) {
      this.nodePositions[li].forEach((from) => {
        this.nodePositions[li + 1].forEach((to) => {
          const line = document.createElementNS('http://www.w3.org/2000/svg', 'line');
          line.setAttribute('x1', from.x); line.setAttribute('y1', from.y);
          line.setAttribute('x2', to.x);   line.setAttribute('y2', to.y);
          line.setAttribute('stroke', this.options.edgeColor);
          line.setAttribute('stroke-width', '1.5');
          line.setAttribute('opacity', '0.6');
          line.id = `edge-${this.containerId}-${li}-${from.index}-${to.index}`;
          line.classList.add('nn-edge');
          line.style.strokeDasharray = '100';
          line.style.strokeDashoffset = '0';
          svg.appendChild(line);
          this.edges.push(line);
        });
      });
    }

    // 노드 그리기
    this.nodePositions.forEach((layerNodes, li) => {
      // 레이어 라벨
      const labelText = document.createElementNS('http://www.w3.org/2000/svg', 'text');
      labelText.setAttribute('x', xStep * (li + 1));
      labelText.setAttribute('y', height - 10);
      labelText.setAttribute('text-anchor', 'middle');
      labelText.setAttribute('fill', '#bdc3c7');
      labelText.setAttribute('font-size', this.options.labelFontSize);
      labelText.textContent = layerLabels[li] || `레이어 ${li + 1}`;
      svg.appendChild(labelText);

      layerNodes.forEach((pos) => {
        const g = document.createElementNS('http://www.w3.org/2000/svg', 'g');
        g.id = `node-${this.containerId}-${li}-${pos.index}`;
        g.classList.add('nn-node');

        const circle = document.createElementNS('http://www.w3.org/2000/svg', 'circle');
        circle.setAttribute('cx', pos.x);
        circle.setAttribute('cy', pos.y);
        circle.setAttribute('r', nodeRadius);
        circle.setAttribute('fill', this.options.nodeColor);
        circle.setAttribute('stroke', '#ecf0f1');
        circle.setAttribute('stroke-width', '2');

        const text = document.createElementNS('http://www.w3.org/2000/svg', 'text');
        text.setAttribute('x', pos.x);
        text.setAttribute('y', pos.y + 1);
        text.setAttribute('text-anchor', 'middle');
        text.setAttribute('dominant-baseline', 'middle');
        text.setAttribute('fill', '#ecf0f1');
        text.setAttribute('font-size', this.options.labelFontSize);
        text.id = `node-val-${this.containerId}-${li}-${pos.index}`;

        // 노드 라벨 (x₁, x₂, h₁ 등)
        const subscripts = ['₁', '₂', '₃', '₄'];
        const prefixes = ['x', 'h', 'y'];
        text.textContent = (prefixes[li] || 'z') + (subscripts[pos.index] || pos.index + 1);

        g.appendChild(circle);
        g.appendChild(text);
        svg.appendChild(g);
        this.nodes.push(g);
      });
    });

    container.appendChild(svg);
  }

  /** 특정 노드 활성화 (색상 변경 + 값 표시) */
  activateNode(layerIndex, nodeIndex, value = null) {
    const nodeG = document.getElementById(`node-${this.containerId}-${layerIndex}-${nodeIndex}`);
    if (!nodeG) return;
    const circle = nodeG.querySelector('circle');
    const text = nodeG.getElementById ? nodeG.querySelector('text') :
                 document.getElementById(`node-val-${this.containerId}-${layerIndex}-${nodeIndex}`);

    gsap.to(circle, {
      attr: { fill: this.options.activeNodeColor },
      filter: `drop-shadow(0 0 8px ${this.options.activeNodeColor})`,
      duration: 0.5
    });

    if (value !== null && text) {
      const valText = document.getElementById(`node-val-${this.containerId}-${layerIndex}-${nodeIndex}`);
      if (valText) {
        gsap.to(valText, { opacity: 0, duration: 0.2, onComplete: () => {
          valText.textContent = typeof value === 'number' ? value.toFixed(2) : value;
          gsap.to(valText, { opacity: 1, duration: 0.3 });
        }});
      }
    }
  }

  /** 엣지 활성화 (신호 흐름) */
  activateEdge(fromLayer, fromIndex, toIndex) {
    const edge = document.getElementById(
      `edge-${this.containerId}-${fromLayer}-${fromIndex}-${toIndex}`
    );
    if (!edge) return;
    gsap.to(edge, {
      attr: { stroke: this.options.activeEdgeColor, 'stroke-width': 3, opacity: 1 },
      duration: 0.4
    });
  }

  /** 전체 레이어 순전파 시각화 (순서대로) */
  forwardPass(inputValues, hiddenValues, outputValues, delayBetween = 0.8) {
    let delay = 0;

    // 입력층 활성화
    inputValues.forEach((v, i) => {
      setTimeout(() => this.activateNode(0, i, v), delay * 1000);
    });
    delay += delayBetween;

    // 입력→은닉 엣지
    inputValues.forEach((_, fi) => {
      (hiddenValues || []).forEach((_, ti) => {
        setTimeout(() => this.activateEdge(0, fi, ti), delay * 1000);
      });
    });
    delay += delayBetween;

    // 은닉층 활성화
    (hiddenValues || []).forEach((v, i) => {
      setTimeout(() => this.activateNode(1, i, v), delay * 1000);
    });
    delay += delayBetween;

    // 은닉→출력 엣지
    if (this.layers.length > 2) {
      (hiddenValues || []).forEach((_, fi) => {
        outputValues.forEach((_, ti) => {
          setTimeout(() => this.activateEdge(1, fi, ti), delay * 1000);
        });
      });
      delay += delayBetween;
    }

    // 출력층
    outputValues.forEach((v, i) => {
      setTimeout(() => this.activateNode(this.layers.length - 1, i, v), delay * 1000);
    });
  }
}

// ─────────────────────────────────────────────────────
// 퍼셉트론 진리표 헬퍼
// ─────────────────────────────────────────────────────

class PerceptronTruthTable {
  /**
   * @param {string} tableId   - 표 DOM ID
   * @param {Function} gateFunc - 논리 게이트 함수 (x1, x2, w1, w2, b) => y
   */
  constructor(tableId, gateFunc) {
    this.tableId = tableId;
    this.gateFunc = gateFunc;
    this.inputs = [[0,0],[0,1],[1,0],[1,1]];
  }

  /** 진리표를 단계별로 채우기 */
  fillRow(rowIndex, w1, w2, bias, animDuration = 0.5) {
    const [x1, x2] = this.inputs[rowIndex];
    const z = w1 * x1 + w2 * x2 + bias;
    const y = z >= 0 ? 1 : 0;

    const table = document.getElementById(this.tableId);
    if (!table) return;
    const row = table.querySelectorAll('tbody tr')[rowIndex];
    if (!row) return;

    const cells = row.querySelectorAll('td');
    const values = [x1, x2, `${w1}×${x1}+${w2}×${x2}+${bias}`, z.toFixed(2), y];

    values.forEach((val, i) => {
      if (cells[i]) {
        setTimeout(() => {
          gsap.to(cells[i], {
            backgroundColor: '#f39c1244',
            duration: animDuration * 0.3,
            onComplete: () => {
              cells[i].textContent = val;
              if (i === values.length - 1) {
                cells[i].style.fontWeight = 'bold';
                cells[i].style.color = y === 1 ? '#2ecc71' : '#e74c3c';
              }
              gsap.to(cells[i], { backgroundColor: 'transparent', duration: animDuration * 0.5 });
            }
          });
        }, i * 150);
      }
    });
  }

  /** 전체 진리표 채우기 */
  fillAll(w1, w2, bias, intervalMs = 800) {
    this.inputs.forEach((_, i) => {
      setTimeout(() => this.fillRow(i, w1, w2, bias), i * intervalMs);
    });
  }
}

// 전역 등록
window.MathStepAnimator = MathStepAnimator;
window.NeuralNetDiagram = NeuralNetDiagram;
window.PerceptronTruthTable = PerceptronTruthTable;
window.mathAnimators = window.mathAnimators || {};
