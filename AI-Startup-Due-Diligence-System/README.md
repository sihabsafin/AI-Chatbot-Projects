# VentureIQ — AI Startup Due Diligence System
- Live demo: [aibusinessintelligence.streamlit.app](https://ai-startup-due-diligence-system.streamlit.app/)
> Five specialist agents. One investment decision. 90 seconds.

A multi-agent due diligence system built on CrewAI that analyzes any startup idea through four analytical lenses — market, financial, risk, and investment strategy — and delivers a structured report with a scored verdict and machine-readable JSON output.

This is Day 7 of [`agent-forge`](https://github.com/sihabsafin/agentic-ai-projects), a 15-day progressive build of production-grade AI agent systems.

---

![Python](https://img.shields.io/badge/Python-3.10%2B-3B82F6?style=flat-square&logo=python&logoColor=white)
![CrewAI](https://img.shields.io/badge/CrewAI-Latest-10B981?style=flat-square)
![Streamlit](https://img.shields.io/badge/Streamlit-1.x-F43F5E?style=flat-square&logo=streamlit&logoColor=white)
![Gemini](https://img.shields.io/badge/Gemini_2.5_Flash-Primary-F59E0B?style=flat-square)
![License](https://img.shields.io/badge/License-MIT-8B5CF6?style=flat-square)

---

## What This Actually Does

You paste a startup idea. Five agents run sequentially — each one receives the prior agent's output as context — and together they produce something that would take a junior analyst two days to write manually.

The Market Analyst sizes the opportunity and maps the competitive landscape. The Financial Analyst builds out unit economics and stress-tests the revenue model. The Risk Analyst produces a severity-rated risk matrix. The Investment Advisor synthesizes all three into a final recommendation — scored, reasoned, and formatted as JSON so it can plug directly into a CRM, deal pipeline, or investor dashboard.

What comes out at the end looks like this:

```json
{
  "startup_name": "MedMatch AI",
  "stage": "Seed",
  "market_score": 8,
  "financial_score": 7,
  "risk_score": 6,
  "overall_score": 7,
  "final_decision": "CONDITIONAL",
  "rationale": "Strong market timing in underpenetrated SEA health market, but regulatory pathway needs validation before committing full ticket.",
  "recommended_check_size": "$300K–$500K seed",
  "key_condition": "Signed pilot with 2 hospital groups before next raise"
}
```

---

## Screenshots

> UI is built on a token-based design system inspired by Carta, Linear, and Vercel Dashboard — deep navy base, electric blue primary, semantic color-coding per agent.

| Input & Pipeline | Verdict & Scores | Full Report |
|---|---|---|
| Agent architecture visualization, preset startup cards, startup brief form | Four scored cards with progress bars, decision chip (INVEST/CONDITIONAL/WATCH/PASS), check size + key condition | Color-coded report sections per agent, JSON verdict panel |

---

## Agent Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                     CREWAI SEQUENTIAL PROCESS                   │
│                                                                 │
│  👑 Manager                                                     │
│  ├─ Oversees delegation                                         │
│  ├─ allow_delegation=True                                       │
│  └─ Consolidates output structure                               │
│                                                                 │
│  📊 Market Analyst ──────────────────────────► Task 1          │
│  ├─ TAM / SAM / SOM sizing                                      │
│  ├─ Competitive landscape mapping                               │
│  ├─ Demand drivers + market timing                              │
│  └─ Market opportunity score /10                                │
│          │ output passed as context ↓                           │
│  💰 Financial Analyst ────────────────────────► Task 2         │
│  ├─ Revenue model + pricing analysis                            │
│  ├─ CAC / LTV / gross margin estimates                          │
│  ├─ Capital requirements + burn modeling                        │
│  └─ Financial viability score /10                               │
│          │ output passed as context ↓                           │
│  ⚠️  Risk Analyst ─────────────────────────────► Task 3        │
│  ├─ Market / regulatory / technical / execution risks           │
│  ├─ Each risk: severity (H/M/L) × likelihood (H/M/L)           │
│  ├─ Second-order threats                                        │
│  └─ Risk score /10 (10 = safest)                                │
│          │ all three outputs passed as context ↓                │
│  🎯 Investment Advisor ────────────────────────► Task 4        │
│  ├─ Synthesizes all three analyses                              │
│  ├─ Exit strategy + DD checklist (optional)                     │
│  ├─ Final recommendation: INVEST / CONDITIONAL / WATCH / PASS  │
│  └─ Structured JSON verdict                                     │
└─────────────────────────────────────────────────────────────────┘
```

The key architectural decision here is **context chaining** — CrewAI automatically passes each completed task's output as context to the Investment Advisor's task. The advisor never works from scratch. It synthesizes what three specialists already established.

---

## Six Built-In Startup Presets

All three from the Day 7 assignment criteria, plus three bonus presets covering different sectors and risk profiles:

| Startup | Sector | Why It's Useful for Testing |
|---|---|---|
| AI Medical Appointment Booking | HealthTech | Tests regulatory risk handling, high-TAM analysis |
| **AI Logistics Optimization** | LogisticsTech | Assignment — tests operational risk, unit economics |
| **AI Legal Document Analyzer** | LegalTech | Assignment — tests IP/regulatory risks, B2B SaaS model |
| **AI Farming Automation** | AgriTech | Assignment — tests emerging market analysis, hardware risk |
| AI Customer Support SaaS | SaaS / CX | Per-resolution pricing model, tests margin analysis |
| AI Recruitment Screener | HRTech | Tests competitive landscape depth, ATS market sizing |

Each preset loads a detailed idea description into the input field — specific enough that agents produce substantive output, not generic observations.

---

## Configuration Options

The system is configurable beyond just swapping the startup idea. Every setting changes the actual agent instructions, not just the label on the output:

**Investor Lens** — Changes each agent's backstory and scoring emphasis. A Venture Capital lens weights scalability and 10x return potential. A Private Equity lens shifts focus to EBITDA path and acquisition multiples. An Impact Investor lens adds social impact metrics alongside financial returns.

**Analysis Depth** — Brief gives you 2-3 key points per section, useful for quick screening. Detailed instructs agents to cover every sub-dimension with specific estimates — useful before a partner meeting.

**Target Geography** — Adjusts market context across all agents. Selecting South Asia, for example, tells the Market Analyst to focus on Bangladesh, India, and Pakistan market dynamics rather than defaulting to US/EU assumptions.

**Report Currency** — All financial estimates (TAM, CAC, check size) are expressed in your chosen currency: USD, EUR, GBP, or BDT.

**Optional Sections** — Comparable companies with valuations, exit strategy analysis (M&A targets, IPO path), and a 5-question investor DD checklist — each toggle injects additional instructions into the relevant agent's task.

---

## JSON Verdict Design

The Investment Advisor is explicitly instructed to produce a JSON block in a specific schema. The app uses a two-pass regex parser to extract it:

```python
# Pass 1: look for fenced ```json block
m = re.search(r'```json\s*(\{.*?\})\s*```', search_text, re.DOTALL)

# Pass 2: fallback — look for any object containing "final_decision"
if not m:
    m = re.search(r'(\{[^{}]*"final_decision"[^{}]*\})', search_text, re.DOTALL)
```

This matters in production. LLMs occasionally drop the markdown fence, especially under heavy token load. The fallback ensures the verdict panel renders even if the agent formatted its output slightly off-spec.

The parsed JSON drives the scored cards, decision chip, check size, and key condition fields — so the visual dashboard is entirely data-driven, not hardcoded.

---

## Tech Stack

| Layer | Technology | Why |
|---|---|---|
| Agent Framework | [CrewAI](https://crewai.com) | Sequential process with context chaining; clean agent/task/crew API |
| Primary LLM | Gemini 2.5 Flash | Best reasoning-per-second for structured output tasks at this scale |
| Fallback LLM | Groq LLaMA 3.3 70B | Near-zero latency; useful when Gemini rate limits hit |
| LLM Router | LiteLLM | Single interface for switching between providers without code changes |
| UI | Streamlit | Fastest path from agent output to rendered dashboard |
| Deployment | Streamlit Cloud | Zero-config; secrets management built-in |

---

## Local Setup

**1. Clone**
```bash
git clone https://github.com/sihabsafin/agent-forge
cd agent-forge/crewai-day7-due-diligence
```

**2. Install dependencies**
```bash
pip install crewai[google-genai] google-generativeai litellm streamlit
```

**3. Set API keys**
```bash
export GEMINI_API_KEY="your_key_here"   # aistudio.google.com/apikey — free tier works
export GROQ_API_KEY="your_key_here"     # console.groq.com/keys — optional fallback
```

**4. Run**
```bash
streamlit run app.py
```

Open `http://localhost:8501`. Select a preset or write your own startup idea and hit **Run Due Diligence**.

---

## Streamlit Cloud Deployment

**Step 1 — Push to GitHub**

Your repo structure should look like this:
```
agent-forge/
└── crewai-day7-due-diligence/
    ├── app.py
    ├── requirements.txt
    └── README.md
```

**Step 2 — Create app on Streamlit Cloud**

Go to [share.streamlit.io](https://share.streamlit.io) → New app → Select your repo → Set main file path to `crewai-day7-due-diligence/app.py`.

**Step 3 — Add secrets**

Settings → Secrets → paste:
```toml
GEMINI_API_KEY = "your_gemini_key"
GROQ_API_KEY   = "your_groq_key"
```

**Step 4 — requirements.txt** (place in repo root or same folder as app.py)
```
crewai[google-genai]
google-generativeai
litellm
streamlit
```

> ⚠️ Common deployment issue: if your `requirements.txt` is inside a subfolder, Streamlit Cloud may fail to detect it. Either place it in the repo root or explicitly set the requirements path in app settings. See the [Day 5 deployment fix](../crewai-day5-real-apis/README.md) for details.

---

## The Commercial Angle

A boutique analyst firm charges $2,000–$10,000 for a due diligence report. This system produces a structured equivalent in 90–120 seconds.

**How to sell it:**

*White-label SaaS product* — Wrap this behind a custom domain, add a login screen and Stripe, charge $49–$99/report or $299/month for unlimited. Your total build time beyond this codebase: a weekend.

*VC firm deployment* — A small fund running 20+ deal screens per month saves 40+ analyst hours. Charge $800–$1,500 setup + $200/month hosting. The ROI conversation writes itself.

*Freelance automation* — Pitch to angel investor networks, startup accelerators, and pitch competition organizers who need to screen hundreds of applications. They pay per batch.

The JSON output is the most important commercial feature. It means the verdict plugs directly into Notion databases, Airtable deal pipelines, Salesforce, or any CRM — no copy-paste, no reformatting. That integration story is what turns a demo into a paid contract.

---

## Project Progression — agent-forge

This is Day 7 of a 15-day series. Each day introduces one architectural concept:

| Day | Project | New Concept |
|---|---|---|
| 1 | Single-agent content writer | Basic agent + task |
| 2 | Sequential research pipeline | Multi-agent sequential |
| 3 | Hierarchical content system | Hierarchical process |
| 4 | Market intelligence tool | Mock tool integration |
| 5 | Live Weather + Crypto dashboard | Real external APIs |
| 6 | Business memory system | ChromaDB vector memory |
| **7** | **AI Due Diligence System** | **Complex delegation + JSON output** |
| 8–15 | Coming soon | — |

Each project in the series is production-deployable, not a Colab notebook. They're designed to be shown to clients, not just run locally.

---

## Known Limitations

**LLM output variability** — The JSON parser has a two-pass fallback, but on rare occasions an agent may produce output that resists clean extraction. In that case the score cards show `—` and the full report text is still rendered correctly. Running again usually resolves it.

**Execution time** — Sequential agent execution with four tasks typically takes 60–120 seconds on Gemini 2.5 Flash. Groq is faster (~30–60s) but with slightly less reasoning depth. This is a CrewAI architecture constraint, not a bug.

**Analysis quality ceiling** — The agents reason from training knowledge, not live market data. The Market Analyst estimates TAM based on what the LLM knows about the sector, not a live Bloomberg pull. For real investment decisions, treat the output as a starting framework, not a final verdict.

**No persistence** — Analysis results are not saved between sessions. Add a database layer (Supabase, Postgres) and an export-to-PDF button if you need audit trails for client work.

---

## License

MIT — use it, sell it, modify it. Attribution appreciated but not required.

---

## Author

**Sihab Safin** — building [`agent-forge`](https://github.com/sihabsafin/agent-forge), a 15-day series of production-grade CrewAI systems.

- GitHub: [@sihabsafin](https://github.com/sihabsafin)


---

*If this saved you time or gave you ideas, a ⭐ on the repo helps others find it.*
