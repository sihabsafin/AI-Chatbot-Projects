# CrewAI Multi-Agent Business Planner

A two-agent AI system that separates market research and business strategy into specialized roles. Built with CrewAI, Groq (LLaMA 3.3 70B), and deployed via Streamlit.

---

## What It Does

You describe a business idea. Two specialized agents work sequentially — the first researches the market, the second receives that research as context and builds a business strategy. Each agent has a distinct role, goal, and backstory that shapes how it reasons.

This demonstrates why role separation produces better outputs than a single agent doing everything.

---

## How It Works

```
User Input (business idea)
        │
        ▼
┌─────────────────────────────┐
│  Agent 1: Market Research   │
│  Analyst                    │
│  → Market size & trends     │
│  → Ideal customer profile   │
│  → Competitor weaknesses    │
│  → 3 market opportunities   │
└─────────────────────────────┘
        │  output passed as context
        ▼
┌─────────────────────────────┐
│  Agent 2: Business Strategy │
│  Consultant                 │
│  → Target audience          │
│  → Pricing model            │
│  → Revenue streams          │
│  → Marketing strategy       │
│  → Risks & mitigations      │
└─────────────────────────────┘
        │
        ▼
  Two-panel structured output
```

**Process type:** Sequential — Agent 2 cannot start until Agent 1 finishes. Agent 1's full output is passed into Agent 2's context automatically via `context=[research_task]`.

---

## Tech Stack

| Layer | Tool |
|---|---|
| Agent Framework | CrewAI |
| LLM Provider | Groq (free tier) |
| Model | LLaMA 3.3 70B / LLaMA 3.1 8B / Mixtral 8x7B |
| UI | Streamlit |
| Deployment | Streamlit Cloud |

---

## Key Concepts Demonstrated

**Role separation** — two agents with different roles, goals, and backstories produce more focused outputs than one generalist agent handling everything.

**Sequential process** — `Process.sequential` ensures execution order. CrewAI will not run Agent 2 until Agent 1 completes.

**Context passing** — `context=[research_task]` explicitly feeds Agent 1's output into Agent 2's task. This is how agents collaborate without manually copying outputs.

**Prompt structure controls output** — the `expected_output` field on each task defines the exact format the agent must follow. Changing this field changes the structure of results without touching any other code.

---

## Presets Included

Four ready-to-run business ideas:

- **AI Fitness Coaching App** — health tech, wearables integration, B2C SaaS
- **AI SaaS for Lawyers** — legal tech, solo practitioners, document automation
- **AI Real Estate Analyzer** — PropTech, investment tools, rental yield prediction
- **AI Dropshipping Research Tool** — ecommerce, product research, Shopify ecosystem

Custom input is supported — describe any business idea and both agents adapt.

---

## Local Setup

```bash
git clone https://github.com/sihabsafin/agentic-ai-projects
cd crewai-day2-multiagent

pip install crewai litellm streamlit

export GROQ_API_KEY=your_key_here  # free at console.groq.com/keys

streamlit run app.py
```

---

## Streamlit Cloud Deployment

1. Push `app.py` and `requirements.txt` to GitHub
2. Connect repo at [share.streamlit.io](https://share.streamlit.io)
3. Add secret: `GROQ_API_KEY = "your_key"`
4. Deploy

---

## Project Structure

```
crewai-day2-multiagent/
├── app.py               # Streamlit UI + 2-agent CrewAI logic
├── requirements.txt     # crewai, litellm, streamlit
└── README.md
```

---


---

---

*Part of the `agentic-ai-projects` repository — a progressive series of multi-agent AI systems built across a 15-day CrewAI learning program.*
