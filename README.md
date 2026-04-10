# financial-model

**VC-grade financial model builder — bottom-up assumptions to 3-year projections to scenario analysis with dynamic spreadsheet output.**

## Goal

VCs read financial models before they read anything else. Financial-Model automates the build from business assumptions through 3-year projections and scenario analysis (base/bull/bear cases). Outputs include a dynamic Excel file and methodology documentation.

## When & How to Use

Use this skill when building financial projections for investors, strategic planning, or internal decision-making. Input your business assumptions: CAC, pricing tiers, headcount plan, burn rate. Output is a professional Excel workbook with formulas plus methodology documentation.

## Use Cases

| Scenario | Prompt | What Happens |
|---|---|---|
| Seed round pitch | `"financial-model: $50k MRR SaaS, $500 CAC, 10% monthly growth"` | Bottom-up model → 3-year projections → base/bull/bear scenarios → Excel + methodology |
| Series A fundraising | `"Build financial model: expand to 3 new markets, raise $5M"` | Assumptions per market → revenue ramp → team scaling → break-even timeline |
| Board deck prep | `"Model: what happens if churn increases 5% or CAC increases 20%"` | Base case + sensitivity scenarios → board-ready spreadsheet |

## Key Features

- Bottom-up model building from core business assumptions
- 3-year monthly projections across revenue, expenses, and cash flow
- Three-scenario modeling: base, bull, bear cases
- Sensitivity analysis on key drivers: CAC, LTV, churn, pricing
- Dynamic Excel with formula links — change assumptions, projections update
- Key metric calculations: CAC payback, magic number, runway, break-even

## Works With

- **[bp-guide](https://github.com/jasonnamii/bp-guide)** — bp-guide sections integrate financial-model outputs
- **[biz-skill](https://github.com/jasonnamii/biz-skill)** — biz-skill diagnoses strategy; financial-model validates with numbers
- **[ceo-pipeline](https://github.com/jasonnamii/ceo-pipeline)** — financial planning feeds into action lists

## Installation

```bash
git clone https://github.com/jasonnamii/financial-model.git ~/.claude/skills/financial-model
```

## Update

```bash
cd ~/.claude/skills/financial-model && git pull
```

Skills placed in `~/.claude/skills/` are automatically available in Claude Code and Cowork sessions.

## Part of Cowork Skills

This is one of 25+ custom skills. See the full catalog: [github.com/jasonnamii/cowork-skills](https://github.com/jasonnamii/cowork-skills)

## License

MIT License — feel free to use, modify, and share.
