# 재무모델 빌더

> 🇺🇸 [English README](./README.md)

**VC 등급 재무모델 빌더 — 하향식 가정에서 3년 예측, 시나리오 분석, 동적 스프레드시트 산출.**

## 사전 요구사항

- **Claude Cowork 또는 Claude Code** 환경
- **Python with `openpyxl`** — `.xlsx` 생성용

## 목적

VC는 다른 어떤 것보다 먼저 재무모델을 읽습니다. Financial-Model은 사업 가정에서 3년 예측 및 시나리오 분석(베이스/상승/하락 케이스)까지의 구축을 자동화합니다. 산출물은 동적 Excel 파일 및 방법론 문서입니다.

## 사용 시점 및 방법

투자자, 전략 기획, 내부 의사결정을 위한 재무 예측 구축 시 이 스킬을 사용하세요. 사업 가정 입력: CAC, 가격 계층, 인원 계획, 번애율. 산출물: 공식 포함 전문가급 Excel 워크북 + 방법론 문서.

## 사용 예시

| 상황 | 프롬프트 | 결과 |
|---|---|---|
| Seed 투자 피치 | `"financial-model: $50k MRR SaaS, $500 CAC, 월 10% 성장"` | 하향식 모델→3년 예측→베이스/상승/하락→Excel + 방법론 |
| Series A 투자 | `"재무모델 구축: 3개 신규 시장 확장, $5M 투자 유치"` | 시장별 가정→매출 경사→팀 확대→손익분기점 시간표 |
| 이사회 덱 준비 | `"모델: 이탈 5% 증가 또는 CAC 20% 증가 시 어떻게?"` | 베이스 케이스 + 민감도 시나리오→이사회급 스프레드시트 |

## 핵심 기능

- 핵심 사업 가정에서 하향식 모델 구축
- 3년 월단위 예측 매출, 비용, 현금 흐름 전반
- 3가지 시나리오 모델링: 베이스, 상승, 하락 케이스
- 주요 드라이버 민감도 분석: CAC, LTV, 이탈, 가격
- 동적 Excel 공식 링크 — 가정 변경 시 예측 자동 업데이트
- 주요 지표 계산: CAC 회수기간, 매직 숫자, 런웨이, 손익분기점

## 연관 스킬

- **[bp-guide](https://github.com/jasonnamii/bp-guide)** — bp-guide 절이 financial-model 산출물 통합
- **[biz-skill](https://github.com/jasonnamii/biz-skill)** — biz-skill이 전략 진단; financial-model이 숫자로 검증
- **[ceo-pipeline](https://github.com/jasonnamii/ceo-pipeline)** — 재무 기획이 액션리스트로 유입

## 설치

```bash
git clone https://github.com/jasonnamii/financial-model.git ~/.claude/skills/financial-model
```

## 업데이트

```bash
cd ~/.claude/skills/financial-model && git pull
```

`~/.claude/skills/`에 배치된 스킬은 Claude Code 및 Cowork 세션에서 자동으로 사용할 수 있습니다.

## Cowork 스킬 생태계

25개 이상의 커스텀 스킬 중 하나입니다. 전체 카탈로그: [github.com/jasonnamii/cowork-skills](https://github.com/jasonnamii/cowork-skills)

## 라이선스

MIT 라이선스 — 자유롭게 사용, 수정, 공유하세요.