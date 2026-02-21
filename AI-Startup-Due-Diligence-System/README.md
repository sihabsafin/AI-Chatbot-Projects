# AgentForge — AI Startup Due Diligence System

Five specialist agents that analyze any startup idea from four angles — market, financial, risk, investment — and produce a structured report with scored verdict and machine-readable JSON output.

Built as Day 7 of a 15-day CrewAI learning program — the day multi-agent systems became something you could genuinely sell.

---

## What This Does

Enter a startup idea. Five agents run in sequence under manager oversight:

**Market Analyst** — Evaluates TAM/SAM/SOM, competitive landscape, demand drivers, market timing, and comparable companies. Scores market opportunity /10.

**Financial Analyst** — Assesses revenue model, pricing, CAC/LTV estimates, gross margin, capital requirements, and path to profitability. Scores financial viability /10.

**Risk Analyst** — Identifies market, regulatory, technical, competitive, and execution risks. Rates each by severity and likelihood. Scores risk profile /10.

**Investment Advisor** — Synthesizes all three analyses into a final recommendation. Outputs a scored verdict and a valid JSON block with structured decision data.

**Manager** — Oversees the process, enables delegation, and ensures structured output flows between agents.

The final output includes: four scored cards, a decision badge (INVEST / CONDITIONAL / WATCH / PASS), a four-section report, and a machine-readable JSON verdict.

---

## The Six Presets

All three required by the Day 7 assignment are included, plus three bonus presets:

| Preset | Sector | Assignment |
|---|---|---|
| AI Medical Appointment Booking | HealthTech | Day 7 base example |
| **AI Logistics Optimization** | LogisticsTech | ✓ Assignment |
| **AI Legal Document Analyzer** | LegalTech | ✓ Assignment |
| **AI Farming Automation** | AgriTech | ✓ Assignment |
| AI Customer Support SaaS | SaaS / CX | Bonus |
| AI Recruitment Screener | HRTech | Bonus |

---

## JSON Output Format

The Investment Advisor is instructed to end its analysis with a parseable JSON block:

```json
{
  "startup_name": "MedMatch AI",
  "stage": "Seed",
  "market_score": 8,
  "financial_score": 7,
  "risk_score": 6,
  "overall_score": 7,
  "final_decision": "CONDITIONAL",
  "rationale": "Strong market timing but regulatory pathway needs validation before Series A.",
  "recommended_check_size": "$500K seed",
  "key_condition": "Obtain pilot contract with 2 hospital groups before next raise"
}
```

The app parses this JSON, renders the scores as large visual cards, and displays the raw JSON separately — so the output is both human-readable and machine-processable.

---

## Agent Architecture

```
Manager Agent (allow_delegation=True)
        │
        ├── Market Task    → Market Analyst
        ├── Financial Task → Financial Analyst
        ├── Risk Task      → Risk Analyst
        └── Investment Task → Investment Advisor
                              (context: all three above)
```

The Investment Advisor receives all three prior task outputs as context — CrewAI passes them automatically. This is the core of hierarchical multi-agent design: specialists produce, the advisor synthesizes.

---

## Advanced Settings

- **Analysis Depth**: Brief / Standard / Detailed
- **Investor Perspective**: VC / Angel / PE / Corporate VC / Impact — changes agent backstory and scoring emphasis
- **Target Geography**: Adjusts market context for all agents
- **Currency**: USD / EUR / GBP / BDT — all financial estimates expressed in chosen currency
- **Comparable Companies**: Toggle inclusion of benchmark companies
- **Exit Strategy**: Toggle exit path analysis
- **DD Checklist**: Toggle investor checklist at the end

---

## Why This Is Sellable

A due diligence report from a boutique analyst firm costs $2,000–$10,000. This system produces a structured equivalent in 90–120 seconds for the cost of a few API calls. Realistic freelance pricing:

- White-labeled SaaS product: $300–$500/month subscription
- Custom deployment for a VC firm: $800–$1,500 one-time
- Per-analysis pricing: $15–$50/report

The JSON output format means the verdict can feed directly into a CRM, deal pipeline, or investment committee workflow — which is what makes it genuinely enterprise-sellable.

---

## Tech Stack

| Layer | Choice |
|---|---|
| Agent Framework | CrewAI |
| Process | Sequential (manager enabled for delegation) |
| Primary LLM | Gemini 2.5 Flash |
| Fallback LLM | Groq LLaMA 3.3 70B |
| JSON Parsing | Python `re` + `json` — regex fallback if markdown fence absent |
| UI | Streamlit |
| Deployment | Streamlit Cloud |

---

## Local Setup

```bash
git clone https://github.com/sihabsafin/agent-forge
cd crewai-day7-due-diligence

pip install crewai[google-genai] google-generativeai litellm streamlit

export GEMINI_API_KEY=your_key
export GROQ_API_KEY=your_key

streamlit run app.py
```

---

## Streamlit Cloud

```toml
GEMINI_API_KEY = "your_gemini_key"
GROQ_API_KEY   = "your_groq_key"
```

`requirements.txt`:
```
crewai[google-genai]
google-generativeai
litellm
streamlit
```

No new dependencies vs Day 5 — chromadb (Day 6) is not needed here.

---

## Progression: Day 1 → Day 7

| | Day 5 | Day 6 | Day 7 |
|---|---|---|---|
| Agents | 2 specialist | 2 + memory | 5 specialist |
| Process | Sequential | Sequential | Sequential + manager |
| Data source | Live APIs | Vector DB | LLM reasoning |
| Output format | Markdown | Markdown + memory | Markdown + JSON |
| Use case | Intelligence | Knowledge system | Investment product |
| Sellability | Demo | Internal tool | Client-ready product |

---

*Part of `agent-forge` — a 15-day progressive build of multi-agent AI systems using CrewAI.*
