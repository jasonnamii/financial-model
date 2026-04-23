---
name: financial-model
description: "VC-grade 재무모델 빌더. 가정→산출→시나리오 구조의 xlsx + 방법론 md 생성. 재무모델·매출추정·시나리오분석 요청시 자동발동. 일반/TURBO(시나리오 3종·탭·감도매트릭스 병렬 Agent) 2모드. P1: 재무모델, financial model, 매출추정, revenue projection, unit economics, 시나리오분석, 터보재무모델, 재무모델 터보, TURBO. P2: 만들어줘, 추정해줘, 터보로 만들어줘, build, create, turbo model. P3: financial modeling, revenue projection, scenario analysis, turbo model, parallel scenario. P5: .xlsx로, .md로, 스프레드시트로. NOT: 회계장부(→xlsx스킬직접)."
"@uses":
  - references/kpi-formulas.py
---


# Financial Model Builder

가정 기반 동적 재무모델. Bottom-Up 5~15개 핵심가정 → 3개년+ 추정 → 시나리오 분석.

---

---

## ⛔ 절대 규칙

| # | 규칙 |
|---|------|
| 1 | 발동 조건 외 임의 실행 금지 |
| 2 | 출력 형식 준수 — 내부 라벨 사용자 노출 금지 |
| 3 | UP 존댓말·호칭 규칙 우선 적용 |

### 피드백
개선 제안은 thumbs down 버튼으로 Anthropic에 전달.

### 입력 검증
발동 전 필수 입력 확인. 불충분 시 1줄 질문으로 보완.

### 자체 점검 (self-check)
SKILL.md ≤10KB · P1 ≥5개 · Gotchas 존재 확인 후 수정 완료.

---

## 실행 흐름

```
입력 파싱 → 프리셋 판별 → Phase 1 가정설계 → Phase 2 모델구조 → Phase 3 xlsx 생성 → Phase 4 md 가이드 → 검증
```

---

## Phase 1: 가정설계 — 모델의 뼈대

### 가정 분류

| 구분 | 설명 | 예시 |
|------|------|------|
| 핵심가정 (5~8개) | 모델 전체를 움직이는 레버 | 사용자 성장률, 전환율, ARPU, 이탈률 |
| 파생가정 (5~10개) | 핵심가정에서 산출 | CAC, LTV, LTV/CAC, 매출총이익률 |
| 운영가정 (3~5개) | 비용 구조 | 인건비/매출비, 인프라/매출비, 채용 속도 |

**원칙:**
- Bottom-Up 우선. TAM→점유율 방식(Top-Down)은 교차검증용으로만.
- 가정은 전부 Input 탭에 집중. 본문 수식에 하드코딩 금지.
- 각 가정에 출처·근거 주석 필수 (벤치마크/내부데이터/가설 중 명시).

---

## Phase 2: 모델구조 — 탭 설계

### 표준 탭 구성

| 탭 | 역할 | 핵심 내용 |
|----|------|----------|
| **Assumptions** | Input. 모든 가정값 집중 | 핵심/파생/운영 가정, 시나리오 스위치 |
| **Revenue** | Calculation. 매출 빌드업 | 사용자 퍼널 → 유료전환 → 매출라인별 산출 |
| **Costs** | Calculation. 비용 빌드업 | COGS + OpEx (인건비/인프라/마케팅/G&A) |
| **P&L** | Output. 손익계산서 | Revenue - Costs → EBITDA → Net Income |
| **Cash Flow** | Output. 현금흐름 | 운영CF + 투자CF + 재무CF → 잔액 |
| **KPIs** | Output. 핵심지표 대시보드 | 유닛이코노믹스, 성장지표, 효율지표 |
| **Scenarios** | Switch. 시나리오 비교 | Base/Bull/Bear 3개 이상, 감도분석 |

### 수식 원칙

- **동적 연결**: 모든 산출값 = 수식. Python 계산→하드코딩 금지.
- **단방향 흐름**: Assumptions → Revenue/Costs → P&L → Cash Flow → KPIs.
- **시나리오 스위치**: Assumptions 탭 1셀 변경 → 전체 모델 재계산.
- **색상규약**: xlsx 스킬 컬러코딩 준수 (파랑=입력, 검정=수식, 초록=시트간링크).

---

## Phase 3: xlsx 생성

### Revenue 빌드업 패턴

```
월별(또는 분기별) 코호트:
신규가입 × 전환율 = 유료사용자
유료사용자 × (1 - 월이탈률)^월수 = 잔존사용자
잔존사용자 × ARPU = 매출
매출라인 합산 = 총매출
```

### KPI 탭 필수지표

| 범주 | 지표 | 산식 |
|------|------|------|
| 유닛이코노믹스 | LTV | ARPU × Gross Margin / 월이탈률 |
| | CAC | 총마케팅비 / 신규유료사용자 |
| | LTV/CAC | LTV / CAC (≥3x 목표) |
| | CAC Payback | CAC / (ARPU × Gross Margin) (개월) |
| 성장 | MoM/YoY Growth | (현재-이전) / 이전 |
| | Net Revenue Retention | (기존매출+확장-이탈-축소) / 기존매출 |
| 효율 | Burn Multiple | Net Burn / Net New ARR |
| | Rule of 40 | 매출성장률 + EBITDA마진 |
| 활주로 | Runway | 현금잔액 / 월평균순소진 (개월) |

### 시나리오 분석

| 시나리오 | 조정 대상 | 조정 폭 |
|----------|----------|---------|
| Base | 핵심가정 그대로 | — |
| Bull | 성장률/전환율/ARPU | +20~30% |
| Bear | 성장률/전환율/ARPU | -20~30% |

감도분석: 핵심가정 2개 축 × 3~5단계 매트릭스 → P&L/Cash 영향.

### 생성 후 필수

**검증 통합:** recalc.py에 단위정합 체크 통합 (구조6축 + 단위). formula_audit.py는 수식 10행 초과 모델에서만 실행. 10행 이하 → recalc.py 1회로 검증 완료.

구체적으로:
- **① 구조 검증 (`recalc.py`)** — openpyxl 기반, 6축 전수 감사 + 단위 정합:
```bash
python scripts/recalc.py output.xlsx          # 콘솔 출력
python scripts/recalc.py output.xlsx --json   # JSON 출력
```
  - 수식 셀 전수 탐지 + 탭간 참조 정합성
  - 하드코딩 감지 (Assumptions 탭 외 숫자 직입력 → 에러)
  - 색상규약 검증 (파랑=입력, 검정=수식, 초록=시트간링크)
  - 단방향 흐름 위반 감지 (input→calc→output 역참조 → 에러)
  - 시나리오 스위치 셀 존재 확인
  - **단위 정합 체크 통합:** 월/연 단위 혼용, 환산 누락 감지

- **② 수식 심볼릭 검증 (`formula_audit.py`)** — sympy + openpyxl 기반 (수식 10행 초과 모델만):
```bash
python scripts/formula_audit.py audit output.xlsx          # 전체 감사
python scripts/formula_audit.py audit output.xlsx --json   # JSON 출력
python scripts/formula_audit.py verify LTV "arpu * gross_margin / monthly_churn"  # KPI 등가성
```
  - 순환참조 감지 (DFS 기반)
  - 수식 종속성 그래프 + 시트별 수식 수 집계
  - KPI 수식 심볼릭 등가성: 10개 정준 수식(LTV, CAC, LTV/CAC, CAC_Payback, Burn_Multiple, Rule_of_40, Runway, NRR, Quick_Ratio, Net_New_MRR) 대비 검증

**의존성:** `pip install openpyxl sympy`

에러 0 확인 후 납품. 에러 발생 시 수정→재검증 반복.

---

## Phase 4: md 가이드

xlsx와 함께 제공. 투자자/경영진이 모델을 읽는 가이드.

```markdown
# [프로젝트명] 재무모델 가이드
v1.0 | [날짜]

## 모델 개요
[1문장: 이 모델이 무엇을 추정하는가]

## 핵심 가정 (근거 포함)
| 가정 | 값 | 근거 | 감도 |
[핵심가정 5~8개]

## 매출 빌드업 로직
[퍼널 다이어그램 or 단계 설명]

## 시나리오 요약
| 지표 | Bear | Base | Bull |
[핵심 3~5개 지표 비교]

## 한계·전제
[모델이 커버하지 않는 것]
```

---

## 프리셋 (base 위에 delta만)

### `saas`

| 구분 | 추가 |
|------|------|
| 가정 | MRR/ARR 워터폴 (New+Expansion-Contraction-Churn), 코호트별 이탈률, 업셀비율 |
| KPI | ARR 워터폴, Quick Ratio (New+Expansion)/(Contraction+Churn), Magic Number |
| Revenue | MRR 코호트 빌드업 → ARR 환산 |

### `marketplace`

| 구분 | 추가 |
|------|------|
| 가정 | 공급자 수, 수요자 수, 매칭률, 거래당 GMV, Take Rate, 다중이용률 |
| KPI | GMV, Take Rate, Match Rate, 공급/수요 집중도, 전환비용, Power User Curve |
| Revenue | GMV × Take Rate + 부가매출 (광고/프리미엄/데이터) |
| 특수 | a16z 마켓플레이스 13대 지표 렌즈: Match Rate, Market Depth, Time to Match, Concentration, Fragmentation, Take Rate, Unit Economics, Multi-Tenanting, Switching Costs, User Retention Cohorts, Core Action Retention, Dollar Retention, Power User Curves |

### `hardware`

| 구분 | 추가 |
|------|------|
| 가정 | BOM 원가, 생산 수량, 리드타임, 재고회전, 보증비용 |
| KPI | 매출총이익률 (하드웨어), ASP 추이, 재고일수 |
| Revenue | 출하량 × ASP + 서비스/구독 매출 |

---

## VC 체크리스트 — 투자자가 보는 것

모델 완성 후 자가점검:

- [ ] 가정이 분리되어 있고, 1셀 변경으로 전체 재계산 가능한가?
- [ ] Bottom-Up 로직이 명확한가? (TAM→점유율 하향식이 아닌)
- [ ] 가정마다 출처/근거가 있는가? (벤치마크·내부데이터·가설 구분)
- [ ] LTV/CAC ≥ 3x, CAC Payback ≤ 18개월 등 유닛이코노믹스 건전성?
- [ ] 시나리오 3개+ 존재하고, Bear 시나리오가 현실적인가?
- [ ] Runway가 명시되어 있는가? (현금 소진 시점)
- [ ] Rule of 40 또는 Burn Multiple 추적 중인가?
- [ ] 탭 구조가 Input→Calc→Output으로 단방향인가?
- [ ] 수식에 하드코딩 0건인가?
- [ ] `recalc.py` 에러 0건인가?
- [ ] `formula_audit.py` 순환참조·단위이슈 0건인가?

---

## 제약

- 가정의 품질 = 모델의 품질. 가정 근거 불충분 시 리포트에 명시.
- 산술 = Python 필수 (#11~13). LLM 눈 검산 금지.
- xlsx 생성 후 `recalc.py` 필수. 에러 0 확인까지 반복.
- 외부 벤치마크 인용 시 출처·시점 명시. 미확인 수치 확신도 50 이하.

---

## TURBO 모드 — 고품질 병렬 가속화

**목적:** 재무모델 구축 시간 단축. 가정 품질·단방향 흐름·색상규약·recalc.py/formula_audit.py 검증 불변, Phase 3 탭·시나리오·감도·Phase 4 가이드 드래프트만 Agent 분산.

**트리거:** "터보로 재무모델" · "TURBO" · "재무모델 터보" 명시. 미명시 = 일반.

**원칙 (4):**
1. **병렬화만, 스킵 금지** — Phase 1 가정설계·Phase 2 탭 설계·검증(recalc·formula_audit) 불변
2. **독립성 확인** — Assumptions 고정 후 탭·시나리오는 독립 계산 가능
3. **통합 시퀀셜** — xlsx 최종 조립·탭간 참조 무결성·순환참조 검증은 메인
4. **Agent 브리프 완결성** — Assumptions 전체·수식 원칙(동적 연결·하드코딩 금지)·색상규약·정준 수식(LTV·CAC 등 10개) 전달

**병렬 타겟:**
- Phase 3 탭별 수식 드래프트 — Revenue/Costs/P&L/Cash Flow 각 Agent (Assumptions 고정 후)
- 시나리오 3개(Base/Bull/Bear) 가정 조정·재계산 드래프트 — 시나리오별 Agent
- 감도분석 2×3~5 매트릭스 — 축별 Agent
- Phase 4 md 가이드 섹션별 드래프트 — 섹션별 Agent

**병렬 제외 (시퀀셜):**
- Phase 1 가정설계 (모델 전체 뼈대, 핵심/파생/운영 가정 일관성)
- Phase 2 탭 설계·단방향 흐름 규약 확정
- xlsx 최종 조립·탭간 참조 연결·시나리오 스위치 구현
- recalc.py 6축 감사·단위 정합 (하드코딩·역참조·색상 위반)
- formula_audit.py 순환참조·심볼릭 등가성 (수식 10행 초과 시)
- VC 체크리스트 자가점검

**품질 저하 방어:**
- 탭간 참조 단절(Assumptions→Revenue/Costs) 감지 → 재연결
- 단위 혼용(월/연·개월/년) 감지 → 해당 수식 시퀀셜 재작성
- Bear 시나리오 낙관성·Burn Multiple/Runway 누락 감지 → 재조정
- recalc.py 에러 0건 아니면 납품 차단 (병렬 결과 무효)

**예상 단축:** 40~55% (탭 수·시나리오 수·감도 축 수에 비례)

---

## 예시

발동 후 스킬 프로토콜에 따라 단계별 실행 → 산출물 생성.

---

## Gotchas

| 함정 | 대응 |
|---|---|
| recalc.py 실행을 빼먹고 납품하는 것이 최다 실패. xlsx 생성 직후 반드시 실행 | 주의 |
| Assumptions 탭에 값을 넣었는데 Revenue/Costs 탭 수식이 참조 안 하는 | 주의 |
| 시나리오 스위치가 1셀 변경으로 전체 재계산이 안 되면 구조 오류. 반드시 테스트. | 주의 |
| LTV 계산에서 월이탈률을 연이탈률로 잘못 넣는 실수. 단위 확인 필수. | 주의 |
| Bear 시나리오를 너무 낙관적으로 만드는 경향. VC는 Bear가 현실적인지 먼저 본다. | 주의 |

