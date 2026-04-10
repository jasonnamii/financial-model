---
name: financial-model
description: |
  VC-grade 재무모델 빌더. 가정→산출→시나리오 구조의 xlsx + 방법론 md 생성. 재무모델·매출추정·시나리오분석 요청시 자동발동.
  P1: 재무모델, financial model, 매출추정, revenue projection, unit economics, 시나리오분석.
  P2: 만들어줘, 추정해줘, build, create.
  P3: financial modeling, revenue projection, scenario analysis.
  P5: .xlsx로, .md로, 스프레드시트로.
  NOT: 회계장부(→xlsx스킬직접).
"@uses":
  - references/kpi-formulas.py
---

<!-- Trigger Conditions (moved from description for token compression)
P1: 재무모델, financial model, 매출추정, revenue projection, unit economics, 시나리오분석.
P4: 재무모델·매출추정·시나리오분석 요청시 자동발동(형 호출 불요). 미발동=실패.
P5: .xlsx로, .md로, 스프레드시트로.
NOT: 회계장부(→xlsx스킬직접)
-->

# Financial Model Builder

가정 기반 동적 재무모델. Bottom-Up 5~15개 핵심가정 → 3개년+ 추정 → 시나리오 분석.

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

**① 구조 검증 (`recalc.py`)** — openpyxl 기반, 6축 전수 감사:
```bash
python scripts/recalc.py output.xlsx          # 콘솔 출력
python scripts/recalc.py output.xlsx --json   # JSON 출력
```
- 수식 셀 전수 탐지 + 탭간 참조 정합성
- 하드코딩 감지 (Assumptions 탭 외 숫자 직입력 → 에러)
- 색상규약 검증 (파랑=입력, 검정=수식, 초록=시트간링크)
- 단방향 흐름 위반 감지 (input→calc→output 역참조 → 에러)
- 시나리오 스위치 셀 존재 확인

**② 수식 심볼릭 검증 (`formula_audit.py`)** — sympy + openpyxl 기반:
```bash
python scripts/formula_audit.py audit output.xlsx          # 전체 감사
python scripts/formula_audit.py audit output.xlsx --json   # JSON 출력
python scripts/formula_audit.py verify LTV "arpu * gross_margin / monthly_churn"  # KPI 등가성
```
- 순환참조 감지 (DFS 기반)
- 월/연 단위 혼용 감지 (×12 변환 누락 시 경고)
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

## Gotchas

- recalc.py 실행을 빼먹고 납품하는 것이 최다 실패. xlsx 생성 직후 반드시 실행.
- Assumptions 탭에 값을 넣었는데 Revenue/Costs 탭 수식이 참조 안 하는 경우 빈번. 탭 간 연결을 전수 확인.
- 시나리오 스위치가 1셀 변경으로 전체 재계산이 안 되면 구조 오류. 반드시 테스트.
- LTV 계산에서 월이탈률을 연이탈률로 잘못 넣는 실수. 단위 확인 필수.
- Bear 시나리오를 너무 낙관적으로 만드는 경향. VC는 Bear가 현실적인지 먼저 본다.
- 색상규약(파랑=입력, 검정=수식, 초록=시트간링크) 미적용 시 투자자가 구조를 못 읽음.

실수 발견 시 이 섹션에 직접 추가.
