# CrewAI Tool Workshop — Tool-Powered Market Intelligence System

A two-agent AI system where agents actively call custom tools during execution — a Market Size Estimator, Competitor Intelligence tool, and ROI Calculator. Built as Day 4 of a 15-day CrewAI learning program.

---

## What This Actually Does

You describe a business idea, enter revenue/cost projections, and select an industry. Two agents run sequentially — the researcher calls the market size and competitor tools, the strategist calls the ROI calculator — and both outputs are grounded in actual tool return values, not LLM estimates.

The key shift from Days 1–3: agents are no longer just writing from memory. They are calling tools and incorporating the results.

---

## Tools Built

**MarketSizeTool** — Returns global market size, CAGR, and key players for 8 industries. The agent decides when to call it based on task context. If the description doesn't indicate it needs market data, it won't call — which is an important behavior to observe.

**ROITool** — Takes revenue and cost as inputs, returns ROI percentage, payback period in months, profit margin, and 3-year net profit projection. The strategist is instructed to always call this before making financial recommendations.

**CompetitorIntelTool** — Returns known competitors with pricing tiers and an identified market gap for each industry. Combined with MarketSizeTool to give the researcher a complete external picture.

All three are mock tools with hardcoded data. In a real system, these would call Serper API for web data, a financial database for market figures, or internal business logic. The architecture is identical — only the `_run()` method changes.

---

## Architecture

```
User Input (idea + revenue + cost + industry)
              │
              ▼
┌─────────────────────────────────────┐
│  Market Research Specialist         │
│  tools: [MarketSizeTool,            │
│           CompetitorIntelTool]      │
│                                     │
│  Calls tools → incorporates data    │
│  → produces market research report  │
└─────────────────────────────────────┘
              │ context passed
              ▼
┌─────────────────────────────────────┐
│  Business Strategy Consultant       │
│  tools: [ROITool]                   │
│                                     │
│  Calls ROI tool → builds strategy   │
│  grounded in actual ROI figures     │
└─────────────────────────────────────┘
              │
              ▼
     Two-panel structured output
```

**Process:** Sequential — researcher runs first, strategist receives research context.

---

## Key Concept: Tool Description Drives Usage

The most important thing Day 4 teaches is that **the tool description is what the LLM reads to decide whether to call the tool**. Not the tool's code. Not the task description alone.

A vague description like `"Gets market data"` will be called inconsistently. A precise description like `"Estimates the global market size and growth rate for a given industry — use this when you need market size data to support business analysis"` gives the LLM enough signal to call it at the right moment.

This is why the tools in this project have verbose, intentional descriptions.

---

## Tech Stack

| Layer | Choice |
|---|---|
| Agent Framework | CrewAI |
| Tools | Custom `BaseTool` subclasses |
| Primary LLM | Gemini 2.5 Flash (free tier) |
| Fallback LLM | Groq LLaMA 3.3 70B |
| UI | Streamlit |
| Deployment | Streamlit Cloud |

---

## Presets

- **AI Fitness SaaS** — B2B corporate wellness, $22B market, ROI modeling from $480K revenue / $180K cost
- **AI Real Estate Platform** — investor deal analyzer, $18B PropTech market, $720K / $210K
- **AI Marketing Automation** — DTC ecommerce content, $107B market, $960K / $290K
- **AI SaaS for Lawyers** — contract intelligence, $12B LegalTech, $540K / $160K

---

## Local Setup

```bash
git clone https://github.com/sihabsafin/agentic-ai-projects
cd crewai-day4-tools

pip install crewai[google-genai] google-generativeai litellm streamlit

export GEMINI_API_KEY=your_key
export GROQ_API_KEY=your_key

streamlit run app.py
```

---

## Progression: Day 1 → Day 4

| | Day 1 | Day 2 | Day 3 | Day 4 |
|---|---|---|---|---|
| Agents | 1 | 2 | 4 | 2 |
| Process | Default | Sequential | Hierarchical | Sequential |
| Tools | None | None | None | 3 custom tools |
| Agent capability | Writing | Writing + context | Delegating | Acting on external data |
| Output grounding | LLM memory | LLM memory | LLM memory | Tool return values |

Day 4 is intentionally simpler in agent count than Day 3. The complexity moved from architecture to capability — fewer agents doing more because they have tools.

---

## Known Limitations

- All three tools use hardcoded mock data — no live API calls
- Tool call behavior depends on the LLM following instructions — weaker models may skip tool calls despite being instructed
- Free tier Gemini limits apply: 5 RPM, leave 30–60s between runs
- The tool execution log in the UI is an animation — it does not stream real CrewAI tool call events in real time

---

*Part of `agentic-ai-projects` — a 15-day progressive build of multi-agent AI systems.*
