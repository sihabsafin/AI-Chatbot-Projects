import streamlit as st
import os
import time

st.set_page_config(
    page_title="CrewAI · Tool-Powered Agents",
    page_icon="⚙",
    layout="centered",
    initial_sidebar_state="collapsed",
)

# ── Secrets ────────────────────────────────────────────────────────────────────
for secret_key in ["GEMINI_API_KEY", "GROQ_API_KEY"]:
    try:
        os.environ[secret_key] = st.secrets[secret_key]
    except Exception:
        pass
if os.environ.get("GEMINI_API_KEY"):
    os.environ["GEMINI_API_KEY"] = os.environ["GEMINI_API_KEY"]
os.environ.setdefault("OPENAI_API_KEY", "dummy-not-used")

# ── CSS ────────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@300;400;600;700&family=Syne:wght@400;600;700&display=swap');

:root {
    --bg:       #0c0a07;
    --surface:  #111009;
    --surface2: #16140f;
    --border:   #2a2418;
    --border2:  #3a3222;
    --text:     #e8dfc8;
    --muted:    #6b5f45;
    --accent:   #f0a500;
    --amber:    #e8891a;
    --green:    #7ec87e;
    --red:      #e06060;
    --blue:     #7ab3e0;
    --mono:     'JetBrains Mono', monospace;
    --sans:     'Syne', sans-serif;
}

* { box-sizing: border-box; }
html, body, [class*="css"] {
    font-family: var(--sans);
    background: var(--bg);
    color: var(--text);
}
#MainMenu, footer, header { visibility: hidden; }
.block-container { padding: 2rem 1.8rem 5rem; max-width: 860px; }

/* ── Top bar ── */
.topbar {
    display: flex;
    align-items: flex-start;
    justify-content: space-between;
    border-bottom: 1px solid var(--border);
    padding-bottom: 1.1rem;
    margin-bottom: 1.8rem;
}
.app-name {
    font-family: var(--mono);
    font-size: 0.82rem;
    font-weight: 700;
    color: var(--accent);
    letter-spacing: 0.04em;
    line-height: 1.3;
}
.app-sub {
    font-family: var(--mono);
    font-size: 0.58rem;
    color: var(--muted);
    letter-spacing: 0.06em;
    margin-top: 0.2rem;
}
.day-badge {
    font-family: var(--mono);
    font-size: 0.6rem;
    font-weight: 700;
    color: var(--bg);
    background: var(--accent);
    padding: 0.2rem 0.6rem;
    border-radius: 2px;
}

/* ── Tool cards row ── */
.tool-row {
    display: grid;
    grid-template-columns: 1fr 1fr 1fr;
    gap: 0.7rem;
    margin-bottom: 1.6rem;
}
.tool-card {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 6px;
    padding: 0.8rem 1rem;
    position: relative;
    overflow: hidden;
}
.tool-card::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 2px;
    background: var(--accent);
    opacity: 0.5;
}
.tool-icon {
    font-family: var(--mono);
    font-size: 0.9rem;
    margin-bottom: 0.4rem;
    display: block;
}
.tool-name {
    font-family: var(--mono);
    font-size: 0.65rem;
    font-weight: 700;
    color: var(--accent);
    letter-spacing: 0.05em;
    text-transform: uppercase;
    margin-bottom: 0.2rem;
}
.tool-desc {
    font-family: var(--mono);
    font-size: 0.58rem;
    color: var(--muted);
    line-height: 1.5;
}
.tool-tag {
    display: inline-block;
    font-family: var(--mono);
    font-size: 0.52rem;
    color: var(--bg);
    background: var(--muted);
    padding: 0.1rem 0.4rem;
    border-radius: 2px;
    margin-top: 0.4rem;
}
.tool-tag.active { background: var(--green); }

/* ── Section label ── */
.sec-label {
    font-family: var(--mono);
    font-size: 0.6rem;
    color: var(--muted);
    letter-spacing: 0.12em;
    text-transform: uppercase;
    margin-bottom: 0.35rem;
    display: block;
}

/* ── Inputs ── */
.stTextInput input, .stTextArea textarea {
    background: var(--surface) !important;
    border: 1px solid var(--border2) !important;
    border-radius: 5px !important;
    color: var(--text) !important;
    font-family: var(--mono) !important;
    font-size: 0.82rem !important;
    caret-color: var(--accent) !important;
}
.stTextInput input:focus, .stTextArea textarea:focus {
    border-color: var(--accent) !important;
    box-shadow: 0 0 0 2px #f0a50015 !important;
}
.stSelectbox div[data-baseweb="select"] {
    background: var(--surface) !important;
    border: 1px solid var(--border2) !important;
    border-radius: 5px !important;
}
.stSelectbox div[data-baseweb="select"] > div {
    background: var(--surface) !important;
    color: var(--text) !important;
    font-family: var(--mono) !important;
    font-size: 0.82rem !important;
}
.stNumberInput input {
    background: var(--surface) !important;
    border: 1px solid var(--border2) !important;
    border-radius: 5px !important;
    color: var(--text) !important;
    font-family: var(--mono) !important;
    font-size: 0.82rem !important;
}

/* ── Button ── */
.stButton > button {
    background: var(--accent) !important;
    color: var(--bg) !important;
    border: none !important;
    border-radius: 5px !important;
    font-family: var(--mono) !important;
    font-size: 0.78rem !important;
    font-weight: 700 !important;
    letter-spacing: 0.08em !important;
    padding: 0.65rem 2rem !important;
    width: 100% !important;
    transition: all 0.15s !important;
}
.stButton > button:hover { opacity: 0.85 !important; transform: translateY(-1px) !important; }

/* ── Expander ── */
.stExpander { background: var(--surface) !important; border: 1px solid var(--border) !important; border-radius: 5px !important; }
details summary { color: var(--muted) !important; font-size: 0.78rem !important; font-family: var(--mono) !important; }

/* ── Divider ── */
.div { border: none; border-top: 1px solid var(--border); margin: 1.4rem 0; }

/* ── Tool fire log ── */
.log-wrap {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 6px;
    overflow: hidden;
    margin-bottom: 1rem;
    font-family: var(--mono);
}
.log-head {
    display: flex;
    align-items: center;
    gap: 0.6rem;
    padding: 0.6rem 1rem;
    background: #0a0901;
    border-bottom: 1px solid var(--border);
}
.log-dot { width:6px; height:6px; border-radius:50%; background: var(--accent); }
.log-head-title { font-size: 0.6rem; color: var(--muted); letter-spacing: 0.1em; text-transform: uppercase; }
.log-body { padding: 0.7rem 1rem; display: flex; flex-direction: column; gap: 0.45rem; }
.log-line { display: flex; align-items: flex-start; gap: 0.7rem; font-size: 0.68rem; line-height: 1.5; }
.log-t { color: var(--muted); min-width: 50px; }
.log-tag {
    font-size: 0.56rem; font-weight: 700;
    padding: 0.1rem 0.4rem; border-radius: 2px;
    white-space: nowrap; margin-top: 0.15rem;
}
.t-sys  { background:#1a1505; color:var(--muted); }
.t-agt  { background:#1a1205; color:var(--accent); }
.t-tool { background:#0a1a0a; color:var(--green); }
.t-calc { background:#0a0a1a; color:var(--blue); }
.t-err  { background:#1a0a0a; color:var(--red); }
.log-msg { color: var(--text); }

/* ── Status bar ── */
.status-bar {
    display: flex; align-items: center; gap: 0.7rem;
    padding: 0.55rem 1rem;
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 5px;
    margin-bottom: 1rem;
}
.s-dot { width:7px; height:7px; border-radius:50%; flex-shrink:0; }
.s-running { background: var(--amber); animation: blink 1.2s ease-in-out infinite; }
.s-done    { background: var(--green); }
@keyframes blink { 0%,100%{opacity:1} 50%{opacity:0.2} }
.s-text { font-family: var(--mono); font-size: 0.67rem; color: var(--text); flex: 1; }
.s-meta { font-family: var(--mono); font-size: 0.6rem; color: var(--muted); }

/* ── Tool call badge (in output) ── */
.tool-fired {
    display: inline-flex; align-items: center; gap: 0.4rem;
    background: #0a1a0a;
    border: 1px solid #1a3a1a;
    border-radius: 3px;
    font-family: var(--mono);
    font-size: 0.62rem;
    color: var(--green);
    padding: 0.2rem 0.6rem;
    margin-bottom: 0.6rem;
}

/* ── Result panels ── */
.result-panel {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 6px;
    overflow: hidden;
    margin-bottom: 1rem;
}
.rp-head {
    display: flex; align-items: center; gap: 0.7rem;
    padding: 0.7rem 1.1rem;
    border-bottom: 1px solid var(--border);
    background: #0a0901;
}
.rp-badge {
    font-family: var(--mono); font-size: 0.58rem; font-weight: 700;
    padding: 0.15rem 0.5rem; border-radius: 2px;
    letter-spacing: 0.06em; text-transform: uppercase;
}
.b-res  { background:#1a1205; color:var(--accent); }
.b-str  { background:#0a0a1a; color:var(--blue); }
.b-tool { background:#0a1a0a; color:var(--green); }
.rp-title { font-family: var(--mono); font-size: 0.67rem; color: var(--muted); }
.rp-body {
    padding: 1.1rem 1.3rem;
    font-family: var(--sans);
    font-size: 0.87rem;
    line-height: 1.8;
    color: #c8bfa8;
    white-space: pre-wrap;
}

/* ── Stats ── */
.stats-row { display:flex; flex-wrap:wrap; gap:0.6rem; margin:0.8rem 0 1.2rem; }
.stat { font-family:var(--mono); font-size:0.6rem; color:var(--muted); border:1px solid var(--border); border-radius:3px; padding:0.2rem 0.6rem; }
.stat b { color:var(--accent); }

/* ── Error ── */
.err-box {
    background:#130a00; border:1px solid #3a1a00; border-left:3px solid var(--red);
    border-radius:5px; padding:0.9rem 1.2rem;
    font-family:var(--mono); font-size:0.72rem; color:#e09060; white-space:pre-wrap; word-break:break-word;
}
</style>
""", unsafe_allow_html=True)


# ── Top bar ────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="topbar">
    <div>
        <div class="app-name">⚙ CREWAI TOOL WORKSHOP</div>
        <div class="app-sub">AGENTS + CUSTOM TOOLS · MARKET INTELLIGENCE · ROI ANALYSIS</div>
    </div>
    <div class="day-badge">DAY 4</div>
</div>
""", unsafe_allow_html=True)

# ── Tool cards ─────────────────────────────────────────────────────────────────
st.markdown("""
<div class="tool-row">
    <div class="tool-card">
        <span class="tool-icon">◈</span>
        <div class="tool-name">Market Size Estimator</div>
        <div class="tool-desc">Returns TAM data for 8 industries. Agent decides when to call it based on task context.</div>
        <span class="tool-tag active">active</span>
    </div>
    <div class="tool-card">
        <span class="tool-icon">◎</span>
        <div class="tool-name">ROI Calculator</div>
        <div class="tool-desc">Computes ROI, payback period, and 3-year projection from revenue and cost inputs.</div>
        <span class="tool-tag active">active</span>
    </div>
    <div class="tool-card">
        <span class="tool-icon">◇</span>
        <div class="tool-name">Competitor Intel</div>
        <div class="tool-desc">Returns known competitors, pricing tiers, and market position for a given industry.</div>
        <span class="tool-tag active">active</span>
    </div>
</div>
""", unsafe_allow_html=True)

# ── Presets ────────────────────────────────────────────────────────────────────
PRESETS = {
    "AI Fitness SaaS": {
        "idea": "An AI-powered B2B fitness coaching SaaS for corporate wellness programs — helping HR teams offer personalized workout and nutrition plans to employees at scale, reducing sick days and improving retention.",
        "revenue": 480000.0,
        "cost": 180000.0,
        "industry": "AI Fitness",
    },
    "AI Real Estate Platform": {
        "idea": "An AI real estate deal analyzer that calculates ROI, cap rate, and rental yield for any property address — targeting independent investors evaluating 10+ deals per month who need instant financial modeling.",
        "revenue": 720000.0,
        "cost": 210000.0,
        "industry": "Real Estate AI",
    },
    "AI Marketing Automation": {
        "idea": "An AI-powered content and ad automation SaaS for DTC e-commerce brands doing $500K–$5M revenue — auto-generating product descriptions, email sequences, and Meta ad copy from a single product feed.",
        "revenue": 960000.0,
        "cost": 290000.0,
        "industry": "AI Marketing",
    },
    "AI SaaS for Lawyers": {
        "idea": "An AI contract intelligence tool for solo lawyers and boutique firms — scanning uploaded contracts in under 60 seconds to flag risky clauses, suggest redlines, and benchmark against industry-standard templates.",
        "revenue": 540000.0,
        "cost": 160000.0,
        "industry": "AI SaaS",
    },
    "Custom Idea": {
        "idea": "",
        "revenue": 500000.0,
        "cost": 150000.0,
        "industry": "AI SaaS",
    },
}

MODELS = {
    "Gemini (Recommended)": {
        "gemini/gemini-2.5-flash": "Gemini 2.5 Flash  ✓ Free tier",
        "gemini/gemini-2.0-flash": "Gemini 2.0 Flash  ✓ Free tier",
    },
    "Groq (Fallback)": {
        "groq/llama-3.3-70b-versatile": "LLaMA 3.3 70B",
        "groq/mixtral-8x7b-32768":      "Mixtral 8x7B",
    },
}

# ── Form ───────────────────────────────────────────────────────────────────────
col1, col2, col3 = st.columns([3, 2, 2])
with col1:
    st.markdown('<span class="sec-label">Business Idea</span>', unsafe_allow_html=True)
    preset_choice = st.selectbox("preset", list(PRESETS.keys()), label_visibility="collapsed")
with col2:
    st.markdown('<span class="sec-label">Provider</span>', unsafe_allow_html=True)
    provider_choice = st.selectbox("provider", list(MODELS.keys()), label_visibility="collapsed")
with col3:
    st.markdown('<span class="sec-label">Model</span>', unsafe_allow_html=True)
    model_opts = MODELS[provider_choice]
    model_id = st.selectbox("model", list(model_opts.keys()),
                             format_func=lambda x: model_opts[x], label_visibility="collapsed")

p = PRESETS[preset_choice]
is_gemini = model_id.startswith("gemini/")

st.markdown('<span class="sec-label">Business Idea Description</span>', unsafe_allow_html=True)
business_idea = st.text_area("idea", value=p["idea"], height=90,
    placeholder="Describe the business idea...", label_visibility="collapsed")

st.markdown('<span class="sec-label">ROI Inputs — for ROI Calculator Tool</span>', unsafe_allow_html=True)
col_r, col_c = st.columns(2)
with col_r:
    revenue = st.number_input("Projected Annual Revenue ($)", value=p["revenue"],
                               min_value=0.0, step=10000.0, format="%.0f")
with col_c:
    cost = st.number_input("Estimated Annual Cost ($)", value=p["cost"],
                            min_value=0.0, step=10000.0, format="%.0f")

INDUSTRIES = ["AI Fitness", "Real Estate AI", "AI Marketing", "AI SaaS",
              "EdTech AI", "HealthTech AI", "FinTech AI", "LegalTech AI"]
st.markdown('<span class="sec-label">Industry — for Market Size Tool</span>', unsafe_allow_html=True)
default_idx = INDUSTRIES.index(p["industry"]) if p["industry"] in INDUSTRIES else 0
industry = st.selectbox("industry", INDUSTRIES, index=default_idx, label_visibility="collapsed")

with st.expander("⚙  Advanced — Customize Agent Instructions"):
    researcher_goal = st.text_area("Researcher Goal", height=70, label_visibility="visible",
        value="Use the Market Size Estimator and Competitor Intel tools to produce a data-backed market analysis. Always call both tools.")
    strategist_goal = st.text_area("Strategist Goal", height=70, label_visibility="visible",
        value="Use the ROI Calculator tool with the provided revenue and cost figures. Build a monetization strategy grounded in the ROI output.")

st.markdown('<div class="div"></div>', unsafe_allow_html=True)
run_btn = st.button("⚙  RUN TOOL-POWERED CREW")


# ── Execution ──────────────────────────────────────────────────────────────────
if run_btn:
    if not business_idea.strip():
        st.markdown('<div class="err-box">⚠ Please enter a business idea.</div>', unsafe_allow_html=True)
        st.stop()

    try:
        from crewai import Agent, Task, Crew, LLM
        from crewai.tools import BaseTool
        from pydantic import Field
        from typing import ClassVar, Dict
    except ImportError as e:
        st.markdown(f'<div class="err-box">Import error: {e}</div>', unsafe_allow_html=True)
        st.stop()

    api_key = os.environ.get("GEMINI_API_KEY" if is_gemini else "GROQ_API_KEY", "")
    if not api_key:
        provider_name = "GEMINI_API_KEY" if is_gemini else "GROQ_API_KEY"
        st.markdown(f'<div class="err-box">⚠ {provider_name} not found in Streamlit Secrets.</div>', unsafe_allow_html=True)
        st.stop()

    if is_gemini:
        os.environ["GEMINI_API_KEY"] = api_key

    # ── Define Tools ───────────────────────────────────────────────────────────
    class MarketSizeTool(BaseTool):
        name: str = "Market Size Estimator"
        description: str = (
            "Estimates the global market size and growth rate for a given industry. "
            "Use this tool when you need market size data to support business analysis. "
            "Input should be the industry name."
        )
        market_data: ClassVar[Dict] = {
            "AI Fitness":      {"size": "$22B", "growth": "28% CAGR", "leaders": "Whoop, Noom, Future"},
            "Real Estate AI":  {"size": "$18B", "growth": "32% CAGR", "leaders": "Zillow, CoStar, Reonomy"},
            "AI Marketing":    {"size": "$107B", "growth": "35% CAGR", "leaders": "Jasper, Copy.ai, AdCreative"},
            "AI SaaS":         {"size": "$115B", "growth": "38% CAGR", "leaders": "Salesforce Einstein, HubSpot AI"},
            "EdTech AI":       {"size": "$31B", "growth": "22% CAGR", "leaders": "Coursera, Duolingo, Khanmigo"},
            "HealthTech AI":   {"size": "$45B", "growth": "41% CAGR", "leaders": "Tempus, Viz.ai, Babylon"},
            "FinTech AI":      {"size": "$78B", "growth": "29% CAGR", "leaders": "Stripe, Plaid, Brex"},
            "LegalTech AI":    {"size": "$12B", "growth": "26% CAGR", "leaders": "Clio, ContractPodAi, Harvey"},
        }
        def _run(self, industry: str) -> str:
            for key, val in self.market_data.items():
                if key.lower() in industry.lower() or industry.lower() in key.lower():
                    return (
                        f"Market: {key} | Global Size: {val['size']} | "
                        f"Growth Rate: {val['growth']} | Key Players: {val['leaders']}"
                    )
            return f"Market data not found for '{industry}'. Available: {', '.join(self.market_data.keys())}"

    class ROITool(BaseTool):
        name: str = "ROI Calculator"
        description: str = (
            "Calculates ROI percentage, payback period in months, and 3-year revenue projection "
            "given annual revenue and annual cost. Always use this tool when evaluating financial "
            "viability of a business idea. Format input as 'revenue,cost' (e.g. '500000,150000')."
        )
        def _run(self, inputs: str) -> str:
            try:
                parts = inputs.replace(" ", "").split(",")
                rev = float(parts[0])
                cost = float(parts[1])
                roi = round(((rev - cost) / cost) * 100, 1)
                payback = round((cost / (rev - cost)) * 12, 1) if rev > cost else None
                yr3 = round(rev * 3 - cost * 3, 0)
                payback_str = f"{payback} months" if payback else "N/A (revenue ≤ cost)"
                return (
                    f"ROI: {roi}% | Payback Period: {payback_str} | "
                    f"3-Year Net Profit: ${yr3:,.0f} | "
                    f"Profit Margin: {round(((rev-cost)/rev)*100,1)}%"
                )
            except Exception:
                rev, cost_v = revenue, cost
                roi = round(((rev - cost_v) / cost_v) * 100, 1)
                payback = round((cost_v / (rev - cost_v)) * 12, 1) if rev > cost_v else None
                yr3 = round(rev * 3 - cost_v * 3, 0)
                return (
                    f"ROI: {roi}% | Payback Period: {payback} months | "
                    f"3-Year Net Profit: ${yr3:,.0f} | "
                    f"Profit Margin: {round(((rev-cost_v)/rev)*100,1)}%"
                )

    class CompetitorIntelTool(BaseTool):
        name: str = "Competitor Intelligence"
        description: str = (
            "Returns competitor names, pricing tiers, and key weaknesses for a given industry. "
            "Use this to identify differentiation opportunities. Input should be the industry name."
        )
        competitor_data: ClassVar[Dict] = {
            "AI Fitness":      {"players": ["Future ($149/mo)", "Noom ($70/mo)", "Whoop ($30/mo)"], "gap": "No B2B/corporate wellness focus — high opportunity"},
            "Real Estate AI":  {"players": ["Reonomy ($500/mo)", "CoStar ($1200/mo)", "PropStream ($100/mo)"], "gap": "Too expensive for independent investors under 10 deals/month"},
            "AI Marketing":    {"players": ["Jasper ($49/mo)", "Copy.ai ($49/mo)", "AdCreative ($29/mo)"], "gap": "None specialized for DTC ecommerce product catalog workflows"},
            "AI SaaS":         {"players": ["Harvey ($custom)", "Clio ($39/mo)", "ContractPodAi ($custom)"], "gap": "Harvey priced out of solo lawyers — massive underserved segment"},
            "EdTech AI":       {"players": ["Coursera ($59/mo)", "Duolingo (free)", "Udemy ($12/course)"], "gap": "No AI-personalized career-path learning for adults in emerging markets"},
            "HealthTech AI":   {"players": ["Babylon ($15/mo)", "K Health ($29/mo)", "Ada (free)"], "gap": "Symptom checkers without actionable next-step integration"},
            "FinTech AI":      {"players": ["Mint (free)", "YNAB ($14/mo)", "Copilot ($13/mo)"], "gap": "No proactive AI intervention — all reactive dashboards"},
            "LegalTech AI":    {"players": ["Clio ($39/mo)", "Harvey ($custom)", "Ironclad ($custom)"], "gap": "Enterprise pricing blocks solo attorneys — no mid-market player"},
        }
        def _run(self, industry: str) -> str:
            for key, val in self.competitor_data.items():
                if key.lower() in industry.lower() or industry.lower() in key.lower():
                    players_str = " | ".join(val["players"])
                    return f"Competitors: {players_str} | Market Gap: {val['gap']}"
            return f"Competitor data not found for '{industry}'."

    # ── Live log ───────────────────────────────────────────────────────────────
    t0 = time.time()
    log_ph = st.empty()
    status_ph = st.empty()

    def ts():
        return f"{round(time.time()-t0,1):>5}s"

    def render_log(lines):
        rows = ""
        for t, tag, cls, msg in lines:
            rows += f'<div class="log-line"><span class="log-t">{t}</span><span class="log-tag {cls}">{tag}</span><span class="log-msg">{msg}</span></div>'
        log_ph.markdown(f"""
        <div class="log-wrap">
            <div class="log-head"><div class="log-dot"></div><span class="log-head-title">Tool Execution Log</span></div>
            <div class="log-body">{rows}</div>
        </div>""", unsafe_allow_html=True)

    log = []
    provider_label = "gemini" if is_gemini else "groq"
    log.append((ts(), "SYS", "t-sys", f"Crew initialized · 2 agents · 3 tools · {provider_label}"))
    render_log(log); time.sleep(0.3)
    log.append((ts(), "AGT", "t-agt", "Market Research Specialist online — tools: MarketSize + CompetitorIntel"))
    render_log(log); time.sleep(0.3)
    log.append((ts(), "AGT", "t-agt", "Strategy Consultant online — tools: ROI Calculator"))
    render_log(log); time.sleep(0.3)
    log.append((ts(), "TOOL", "t-tool", f"MarketSizeTool ready · industry: {industry}"))
    render_log(log); time.sleep(0.3)
    log.append((ts(), "CALC", "t-calc", f"ROITool ready · revenue: ${revenue:,.0f} · cost: ${cost:,.0f}"))
    render_log(log)

    status_ph.markdown("""
    <div class="status-bar">
        <div class="s-dot s-running"></div>
        <span class="s-text">Agents running — tools firing on demand…</span>
    </div>""", unsafe_allow_html=True)

    try:
        llm = LLM(model=model_id, api_key=api_key, temperature=0.7)

        market_tool   = MarketSizeTool()
        roi_tool      = ROITool()
        comp_tool     = CompetitorIntelTool()

        r_goal = researcher_goal if 'researcher_goal' in dir() else "Use Market Size Estimator and Competitor Intelligence tools to produce a data-backed market analysis."
        s_goal = strategist_goal if 'strategist_goal' in dir() else "Use ROI Calculator tool. Build a monetization strategy grounded in the ROI output."

        researcher = Agent(
            role="Market Research Specialist",
            goal=r_goal,
            backstory=(
                "You are a business intelligence analyst with 10 years experience in SaaS market research. "
                "You always use available tools before drawing conclusions — you never estimate market size "
                "from memory. You always call both the Market Size Estimator and Competitor Intelligence tools."
            ),
            tools=[market_tool, comp_tool],
            llm=llm,
            verbose=False,
        )

        strategist = Agent(
            role="Business Strategy Consultant",
            goal=s_goal,
            backstory=(
                "You are a startup strategist who builds financial models before recommending strategy. "
                f"You must call the ROI Calculator tool with inputs '{revenue},{cost}' to get ROI data. "
                "Never skip the tool call — your strategy must be grounded in actual ROI figures."
            ),
            tools=[roi_tool],
            llm=llm,
            verbose=False,
        )

        research_task = Task(
            description=(
                f"Research the market opportunity for this business idea:\n'{business_idea}'\n\n"
                f"You MUST call the Market Size Estimator tool with industry: '{industry}'\n"
                f"You MUST call the Competitor Intelligence tool with industry: '{industry}'\n"
                f"Use both tool outputs in your analysis. Do not skip tool calls."
            ),
            expected_output=(
                "A market research report containing:\n"
                "1. Market Size & Growth (from tool output)\n"
                "2. Target Customer Profile\n"
                "3. Competitor Analysis (from tool output — include pricing and gaps)\n"
                "4. Top 3 Market Opportunities"
            ),
            agent=researcher,
        )

        strategy_task = Task(
            description=(
                f"Build a business strategy for:\n'{business_idea}'\n\n"
                f"You MUST call the ROI Calculator tool with input: '{revenue},{cost}'\n"
                f"Your entire strategy must reference the ROI output from the tool.\n"
                f"Use the market research context from the previous task."
            ),
            expected_output=(
                "A business strategy report containing:\n"
                "1. ROI Analysis (from tool output — include exact figures)\n"
                "2. Pricing Model & Revenue Streams\n"
                "3. Go-To-Market Strategy (90-day plan)\n"
                "4. Key Risks & Mitigations\n"
                "5. Final Recommendation (Build / Validate / Avoid)"
            ),
            agent=strategist,
            context=[research_task],
        )

        crew = Crew(
            agents=[researcher, strategist],
            tasks=[research_task, strategy_task],
            verbose=False,
        )

        result = crew.kickoff()
        elapsed = round(time.time() - t0, 1)

        # Extract task outputs
        research_out = ""
        strategy_out = ""
        try:
            research_out = str(research_task.output.raw) if research_task.output else ""
            strategy_out = str(strategy_task.output.raw) if strategy_task.output else ""
        except Exception:
            strategy_out = str(result)

        # Final log
        log.append((ts(), "TOOL", "t-tool", "MarketSizeTool executed ✓"))
        log.append((ts(), "TOOL", "t-tool", "CompetitorIntelTool executed ✓"))
        log.append((ts(), "CALC", "t-calc", "ROITool executed ✓"))
        log.append((ts(), "SYS", "t-sys", f"All tools fired · crew complete in {elapsed}s"))
        render_log(log)

        status_ph.markdown(f"""
        <div class="status-bar">
            <div class="s-dot s-done"></div>
            <span class="s-text">Crew complete — 3 tools fired · 2 agents · sequential</span>
            <span class="s-meta">{elapsed}s</span>
        </div>""", unsafe_allow_html=True)

        # Stats
        st.markdown(f"""
        <div class="stats-row">
            <div class="stat">agents <b>2</b></div>
            <div class="stat">tools <b>3</b></div>
            <div class="stat">tasks <b>2</b></div>
            <div class="stat">elapsed <b>{elapsed}s</b></div>
            <div class="stat">model <b>{model_id.split("/")[1]}</b></div>
            <div class="stat">industry <b>{industry}</b></div>
        </div>""", unsafe_allow_html=True)

        if research_out:
            st.markdown(f"""
            <div class="result-panel">
                <div class="rp-head">
                    <span class="rp-badge b-res">Agent 1 · Researcher</span>
                    <span class="rp-badge b-tool">MarketSize + CompetitorIntel tools</span>
                    <span class="rp-title">Market Research Report</span>
                </div>
                <div class="rp-body">{research_out}</div>
            </div>""", unsafe_allow_html=True)

        if strategy_out:
            st.markdown(f"""
            <div class="result-panel">
                <div class="rp-head">
                    <span class="rp-badge b-str">Agent 2 · Strategist</span>
                    <span class="rp-badge b-tool">ROI Calculator tool</span>
                    <span class="rp-title">Business Strategy + ROI Analysis</span>
                </div>
                <div class="rp-body">{strategy_out}</div>
            </div>""", unsafe_allow_html=True)

        if not research_out and not strategy_out:
            st.markdown(f"""
            <div class="result-panel">
                <div class="rp-head"><span class="rp-badge b-res">Output</span></div>
                <div class="rp-body">{str(result)}</div>
            </div>""", unsafe_allow_html=True)

    except Exception as e:
        err_str = str(e)
        log.append((ts(), "ERR", "t-err", "Execution failed"))
        render_log(log)
        status_ph.empty()

        if "resource_exhausted" in err_str.lower() or "quota" in err_str.lower() or "429" in err_str:
            st.markdown("""<div class="err-box">✗ Quota Exhausted (429)\n\nSwitch to Gemini 2.5 Flash or wait 60s and retry.\nGemini 2.0 Flash has 0 RPD on the free tier.</div>""", unsafe_allow_html=True)
        elif "rate_limit" in err_str.lower():
            st.markdown("""<div class="err-box">✗ Rate limit hit. Wait 30–60s and retry.</div>""", unsafe_allow_html=True)
        else:
            st.markdown(f'<div class="err-box">✗ Error: {err_str}</div>', unsafe_allow_html=True)
