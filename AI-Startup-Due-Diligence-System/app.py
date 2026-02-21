import streamlit as st
import os
import time
import json
import re

st.set_page_config(
    page_title="AgentForge · Due Diligence",
    page_icon="◈",
    layout="centered",
    initial_sidebar_state="collapsed",
)

# ── Secrets ──────────────────────────────────────────────────────────────────────
for secret_key in ["GEMINI_API_KEY", "GROQ_API_KEY"]:
    try:
        os.environ[secret_key] = st.secrets[secret_key]
    except Exception:
        pass
os.environ.setdefault("OPENAI_API_KEY", "dummy-not-used")

# ── CSS — Editorial Finance Aesthetic ────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,400;0,600;0,700;1,400;1,600&family=IBM+Plex+Mono:wght@400;500&family=IBM+Plex+Sans:wght@300;400;500;600&display=swap');

:root {
    --bg:          #f5f0e8;
    --surface:     #faf7f2;
    --surface2:    #ede8de;
    --surface3:    #e4ddd0;
    --border:      #d8d0c0;
    --border2:     #c4b99e;
    --text:        #1c1810;
    --text2:       #3a3020;
    --muted:       #7a6e5c;
    --muted2:      #a8998a;
    --gold:        #b8860b;
    --gold2:       #d4a017;
    --gold-bg:     rgba(184,134,11,0.08);
    --gold-border: rgba(184,134,11,0.25);
    --green:       #1a5c2e;
    --green-bg:    rgba(26,92,46,0.08);
    --green-border:rgba(26,92,46,0.25);
    --red:         #8b1a1a;
    --red-bg:      rgba(139,26,26,0.08);
    --red-border:  rgba(139,26,26,0.25);
    --blue:        #1a3a5c;
    --blue-bg:     rgba(26,58,92,0.08);
    --blue-border: rgba(26,58,92,0.25);
    --serif:       'Playfair Display', Georgia, serif;
    --mono:        'IBM Plex Mono', monospace;
    --sans:        'IBM Plex Sans', sans-serif;
    --r:           6px;
    --shadow:      0 1px 4px rgba(0,0,0,0.08), 0 1px 2px rgba(0,0,0,0.05);
    --shadow-md:   0 4px 16px rgba(0,0,0,0.10);
}

*, *::before, *::after { box-sizing: border-box; }
html, body, [class*="css"] {
    font-family: var(--sans);
    background: var(--bg);
    color: var(--text);
}
#MainMenu, footer, header { visibility: hidden; }
.block-container { padding: 2.5rem 2rem 5rem; max-width: 920px; }

/* ── Masthead ── */
.masthead {
    border-bottom: 2px solid var(--text);
    padding-bottom: 1.2rem;
    margin-bottom: 0.4rem;
}
.masthead-top {
    display: flex; align-items: flex-start; justify-content: space-between;
    margin-bottom: 0.6rem;
}
.publication {
    font-family: var(--serif); font-size: 2rem; font-weight: 700;
    color: var(--text); letter-spacing: -0.02em; line-height: 1;
}
.edition-info {
    text-align: right;
    font-family: var(--mono); font-size: 0.68rem; color: var(--muted);
    line-height: 1.6;
}
.rule-gold {
    height: 3px;
    background: linear-gradient(90deg, var(--gold), var(--gold2), transparent);
    margin: 0.5rem 0;
}
.masthead-sub {
    display: flex; justify-content: space-between; align-items: center;
    font-family: var(--mono); font-size: 0.7rem; color: var(--muted);
    letter-spacing: 0.04em;
}
.headline-band {
    background: var(--text); color: var(--bg);
    padding: 0.5rem 1rem; margin: 1rem 0;
    font-family: var(--serif); font-size: 1rem; font-style: italic;
    letter-spacing: 0.01em;
}

/* ── Section label ── */
.sec-label {
    font-family: var(--mono); font-size: 0.65rem; color: var(--muted);
    letter-spacing: 0.12em; text-transform: uppercase;
    margin: 0 0 0.4rem; display: block;
    border-left: 2px solid var(--gold); padding-left: 0.5rem;
}

/* ── Inputs ── */
.stTextInput > div > div > input,
.stTextArea > div > div > textarea,
.stSelectbox > div > div,
.stMultiSelect > div > div {
    background: var(--surface) !important;
    border: 1px solid var(--border) !important;
    border-radius: var(--r) !important;
    color: var(--text) !important;
    font-family: var(--sans) !important;
    font-size: 0.9rem !important;
}
.stTextInput > div > div > input:focus,
.stTextArea > div > div > textarea:focus {
    border-color: var(--gold) !important;
    box-shadow: 0 0 0 3px var(--gold-bg) !important;
}
label[data-testid="stWidgetLabel"] {
    font-family: var(--mono) !important;
    font-size: 0.7rem !important;
    color: var(--muted) !important;
    letter-spacing: 0.08em !important;
}

/* ── Button ── */
.stButton > button {
    width: 100%;
    background: var(--text) !important;
    color: var(--bg) !important;
    border: none !important;
    border-radius: var(--r) !important;
    padding: 0.9rem 2rem !important;
    font-family: var(--serif) !important;
    font-weight: 600 !important;
    font-size: 1rem !important;
    font-style: italic !important;
    letter-spacing: 0.01em !important;
    cursor: pointer !important;
    transition: all 0.2s ease !important;
    box-shadow: var(--shadow-md) !important;
}
.stButton > button:hover {
    background: var(--text2) !important;
    transform: translateY(-1px) !important;
    box-shadow: 0 6px 24px rgba(0,0,0,0.18) !important;
}

/* ── Preset chips ── */
.chip-row { display: flex; flex-wrap: wrap; gap: 0.5rem; margin-bottom: 1rem; }

/* ── Divider ── */
.div { height: 1px; background: var(--border); margin: 1.5rem 0; }
.div-gold { height: 1px; background: var(--gold-border); margin: 1.5rem 0; }

/* ── Agent pipeline ── */
.pipeline {
    display: flex; align-items: center; gap: 0;
    background: var(--surface); border: 1px solid var(--border);
    border-radius: var(--r); padding: 1rem 1.2rem;
    margin-bottom: 1.5rem; overflow-x: auto;
}
.pipe-agent {
    display: flex; flex-direction: column; align-items: center;
    min-width: 100px; padding: 0 0.5rem;
}
.pipe-icon {
    width: 38px; height: 38px; border-radius: 50%;
    display: flex; align-items: center; justify-content: center;
    font-size: 1rem; margin-bottom: 0.4rem;
    border: 2px solid var(--border2);
    background: var(--surface2);
}
.pipe-name {
    font-family: var(--mono); font-size: 0.62rem; color: var(--muted);
    text-align: center; line-height: 1.3; letter-spacing: 0.03em;
}
.pipe-arrow {
    flex: 1; min-width: 20px; text-align: center;
    font-family: var(--mono); color: var(--border2); font-size: 1rem;
}
.pipe-active .pipe-icon {
    border-color: var(--gold); background: var(--gold-bg);
}
.pipe-active .pipe-name { color: var(--gold); }

/* ── Log ── */
.log-wrap {
    background: var(--text); border-radius: var(--r);
    overflow: hidden; margin-bottom: 1.5rem;
    font-family: var(--mono);
    box-shadow: var(--shadow-md);
}
.log-head {
    display: flex; align-items: center; gap: 0.5rem;
    padding: 0.65rem 1rem;
    border-bottom: 1px solid rgba(255,255,255,0.1);
    background: rgba(255,255,255,0.05);
}
.log-head-title { font-size: 0.68rem; color: rgba(255,255,255,0.4); margin-left: 0.4rem; letter-spacing: 0.06em; }
.log-body { padding: 0.8rem 1rem; max-height: 220px; overflow-y: auto; }
.log-line { display: flex; align-items: baseline; gap: 0.6rem; margin-bottom: 0.3rem; font-size: 0.74rem; }
.log-t   { color: rgba(255,255,255,0.25); min-width: 42px; }
.log-tag { font-size: 0.62rem; font-weight: 600; padding: 0.1rem 0.45rem; border-radius: 3px;
           letter-spacing: 0.06em; min-width: 54px; text-align: center; }
.log-msg { color: rgba(255,255,255,0.65); }
.t-sys   { background: rgba(255,255,255,0.07); color: rgba(255,255,255,0.4); }
.t-agent { background: rgba(184,134,11,0.25); color: #d4a017; }
.t-task  { background: rgba(26,58,92,0.4);    color: #6ba3d4; }
.t-ok    { background: rgba(26,92,46,0.3);    color: #4caf79; }
.t-err   { background: rgba(139,26,26,0.3);   color: #e07070; }

/* ── Score cards ── */
.score-grid {
    display: grid; grid-template-columns: repeat(4, 1fr);
    gap: 0.75rem; margin-bottom: 1.5rem;
}
.score-card {
    background: var(--surface); border: 1px solid var(--border);
    border-radius: var(--r); padding: 1rem;
    text-align: center; position: relative; overflow: hidden;
}
.score-card::before {
    content: ''; position: absolute; top: 0; left: 0; right: 0;
    height: 3px;
}
.sc-market::before  { background: var(--gold); }
.sc-financial::before { background: var(--blue); }
.sc-risk::before    { background: var(--red); }
.sc-final::before   { background: var(--green); }

.score-num {
    font-family: var(--serif); font-size: 2.2rem; font-weight: 700;
    line-height: 1; margin-bottom: 0.2rem;
}
.sc-market .score-num    { color: var(--gold); }
.sc-financial .score-num { color: var(--blue); }
.sc-risk .score-num      { color: var(--red); }
.sc-final .score-num     { color: var(--green); }

.score-label {
    font-family: var(--mono); font-size: 0.62rem; color: var(--muted);
    letter-spacing: 0.06em; text-transform: uppercase;
}

/* ── Decision badge ── */
.decision-badge {
    display: inline-flex; align-items: center; gap: 0.5rem;
    padding: 0.5rem 1.2rem; border-radius: var(--r);
    font-family: var(--serif); font-size: 1.1rem; font-style: italic;
    font-weight: 600; margin-bottom: 1rem;
}
.decision-invest {
    background: var(--green-bg); border: 1px solid var(--green-border);
    color: var(--green);
}
.decision-pass {
    background: var(--red-bg); border: 1px solid var(--red-border);
    color: var(--red);
}
.decision-conditional {
    background: var(--gold-bg); border: 1px solid var(--gold-border);
    color: var(--gold);
}
.decision-watch {
    background: var(--blue-bg); border: 1px solid var(--blue-border);
    color: var(--blue);
}

/* ── Report sections ── */
.report-section {
    background: var(--surface); border: 1px solid var(--border);
    border-radius: var(--r); overflow: hidden; margin-bottom: 1rem;
}
.report-section-header {
    display: flex; align-items: center; gap: 0.75rem;
    padding: 0.8rem 1.1rem;
    border-bottom: 1px solid var(--border);
    background: var(--surface2);
}
.rs-icon {
    width: 28px; height: 28px; border-radius: 4px;
    display: flex; align-items: center; justify-content: center;
    font-size: 0.8rem;
}
.rs-market    { background: var(--gold-bg);  border: 1px solid var(--gold-border); }
.rs-financial { background: var(--blue-bg);  border: 1px solid var(--blue-border); }
.rs-risk      { background: var(--red-bg);   border: 1px solid var(--red-border); }
.rs-final     { background: var(--green-bg); border: 1px solid var(--green-border); }

.rs-title {
    font-family: var(--serif); font-size: 0.95rem; font-weight: 600;
    color: var(--text);
}
.rs-agent {
    margin-left: auto; font-family: var(--mono); font-size: 0.65rem;
    color: var(--muted2); letter-spacing: 0.04em;
}
.report-body {
    padding: 1.1rem 1.2rem; font-size: 0.88rem; color: var(--text2);
    line-height: 1.75;
}
.report-body strong { color: var(--text); font-weight: 600; }
.report-body h1, .report-body h2, .report-body h3 {
    font-family: var(--serif); color: var(--text); margin: 0.8rem 0 0.4rem;
}

/* ── JSON output ── */
.json-panel {
    background: var(--text); border-radius: var(--r);
    padding: 1.2rem; margin-top: 1rem; overflow-x: auto;
}
.json-panel pre {
    font-family: var(--mono); font-size: 0.78rem;
    color: #d4c89a; margin: 0; white-space: pre-wrap; word-break: break-word;
}
.json-key   { color: #f0c060; }
.json-str   { color: #a8d8a0; }
.json-num   { color: #80c8e8; }

/* ── Startup presets ── */
.startup-card {
    background: var(--surface); border: 1px solid var(--border);
    border-radius: var(--r); padding: 0.9rem 1rem;
    cursor: pointer; transition: all 0.15s ease;
    position: relative;
}
.startup-card:hover {
    border-color: var(--gold); background: var(--gold-bg);
}
.sc-name {
    font-family: var(--serif); font-size: 0.95rem; font-weight: 600;
    color: var(--text); margin-bottom: 0.25rem;
}
.sc-sector {
    font-family: var(--mono); font-size: 0.65rem; color: var(--gold);
    letter-spacing: 0.06em; text-transform: uppercase; margin-bottom: 0.35rem;
}
.sc-desc { font-size: 0.8rem; color: var(--muted); line-height: 1.45; }

/* Expander */
.streamlit-expanderHeader {
    background: var(--surface) !important;
    border: 1px solid var(--border) !important;
    border-radius: var(--r) !important;
    color: var(--text) !important;
    font-family: var(--mono) !important;
    font-size: 0.8rem !important;
    letter-spacing: 0.04em !important;
}

/* Error */
.err-box {
    background: var(--red-bg); border: 1px solid var(--red-border);
    border-radius: var(--r); padding: 0.9rem 1rem;
    font-size: 0.85rem; color: var(--red); margin-top: 1rem;
    font-family: var(--sans);
}

/* Checkbox */
.stCheckbox label { color: var(--muted) !important; font-size: 0.85rem !important; }

/* Radio */
.stRadio > div { gap: 0.5rem !important; }
.stRadio > div > label {
    background: var(--surface) !important;
    border: 1px solid var(--border) !important;
    border-radius: var(--r) !important;
    padding: 0.5rem 0.9rem !important;
    font-size: 0.83rem !important;
    color: var(--muted) !important;
}
.stRadio > div > label:hover {
    border-color: var(--gold) !important;
    color: var(--text) !important;
}

/* Ticker strip */
.ticker {
    background: var(--text); color: var(--bg);
    padding: 0.35rem 1rem; margin: 0.8rem 0 1.5rem;
    font-family: var(--mono); font-size: 0.7rem; letter-spacing: 0.06em;
    display: flex; gap: 2rem; overflow: hidden;
}
.ticker-item { display: flex; gap: 0.4rem; white-space: nowrap; }
.ticker-label { color: rgba(245,240,232,0.45); }
.ticker-val   { color: var(--bg); }
.ticker-up    { color: #6ed88e; }
.ticker-down  { color: #e08080; }

</style>
""", unsafe_allow_html=True)


# ── Masthead ──────────────────────────────────────────────────────────────────────
from datetime import datetime
today = datetime.now().strftime("%A, %B %d, %Y")

st.markdown(f"""
<div class="masthead">
    <div class="masthead-top">
        <div class="publication">AgentForge</div>
        <div class="edition-info">
            DAY 7 OF 15<br>
            {today}<br>
            HIERARCHICAL MULTI-AGENT
        </div>
    </div>
    <div class="rule-gold"></div>
    <div class="masthead-sub">
        <span>AI STARTUP DUE DILIGENCE SYSTEM</span>
        <span>VENTURE CAPITAL INTELLIGENCE · POWERED BY CREWAI</span>
        <span>GEMINI 2.5 FLASH · GROQ FALLBACK</span>
    </div>
</div>
<div class="headline-band">
    Five specialist agents. One investment decision. Zero hallucinated numbers.
</div>
""", unsafe_allow_html=True)

# ── Ticker ────────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="ticker">
    <div class="ticker-item"><span class="ticker-label">AGENTS</span><span class="ticker-val">5 SPECIALISTS</span></div>
    <div class="ticker-item"><span class="ticker-label">PROCESS</span><span class="ticker-val">HIERARCHICAL</span></div>
    <div class="ticker-item"><span class="ticker-label">OUTPUT</span><span class="ticker-val">JSON + REPORT</span></div>
    <div class="ticker-item"><span class="ticker-label">SECTIONS</span><span class="ticker-val">MARKET · FINANCIAL · RISK · INVESTMENT</span></div>
    <div class="ticker-item"><span class="ticker-label">SELLABLE</span><span class="ticker-up">$300–$1000</span></div>
</div>
""", unsafe_allow_html=True)


# ── Agent Pipeline Visual ─────────────────────────────────────────────────────────
st.markdown("""
<span class="sec-label">Agent Architecture</span>
<div class="pipeline">
    <div class="pipe-agent pipe-active">
        <div class="pipe-icon">👑</div>
        <div class="pipe-name">MANAGER<br>DELEGATE</div>
    </div>
    <div class="pipe-arrow">→</div>
    <div class="pipe-agent">
        <div class="pipe-icon">📊</div>
        <div class="pipe-name">MARKET<br>ANALYST</div>
    </div>
    <div class="pipe-arrow">→</div>
    <div class="pipe-agent">
        <div class="pipe-icon">💰</div>
        <div class="pipe-name">FINANCIAL<br>ANALYST</div>
    </div>
    <div class="pipe-arrow">→</div>
    <div class="pipe-agent">
        <div class="pipe-icon">⚠️</div>
        <div class="pipe-name">RISK<br>ANALYST</div>
    </div>
    <div class="pipe-arrow">→</div>
    <div class="pipe-agent">
        <div class="pipe-icon">🎯</div>
        <div class="pipe-name">INVESTMENT<br>ADVISOR</div>
    </div>
    <div class="pipe-arrow">→</div>
    <div class="pipe-agent pipe-active">
        <div class="pipe-icon">📋</div>
        <div class="pipe-name">JSON<br>VERDICT</div>
    </div>
</div>
""", unsafe_allow_html=True)


# ── Startup Presets ───────────────────────────────────────────────────────────────
PRESETS = [
    {
        "name": "AI Medical Appointment Booking",
        "sector": "HealthTech",
        "desc": "AI-powered platform that matches patients with doctors, optimizes scheduling, and reduces no-shows using predictive ML.",
        "idea": "An AI-powered medical appointment booking platform that uses machine learning to match patients with the right specialists, predict no-shows, send smart reminders, and optimize clinic schedules. Target market: private clinics and hospital chains in Southeast Asia."
    },
    {
        "name": "AI Logistics Optimization",
        "sector": "LogisticsTech",
        "desc": "Route optimization and demand forecasting AI for last-mile delivery companies and freight operators.",
        "idea": "An AI logistics optimization platform for last-mile delivery companies that uses real-time traffic data, demand forecasting, and dynamic routing to reduce delivery costs by 25–40%. Target: mid-size e-commerce fulfillment and courier companies."
    },
    {
        "name": "AI Legal Document Analyzer",
        "sector": "LegalTech",
        "desc": "Contract review, risk flagging, and clause extraction AI for law firms and in-house legal teams.",
        "idea": "An AI legal document analyzer that automates contract review, flags high-risk clauses, extracts key obligations, and compares against standard templates. Targets law firms and corporate legal departments looking to reduce manual review time by 70%."
    },
    {
        "name": "AI Farming Automation",
        "sector": "AgriTech",
        "desc": "Precision agriculture platform using satellite imagery, IoT sensors, and AI to optimize crop yield.",
        "idea": "An AI-powered precision farming platform that integrates satellite imagery, soil sensors, and weather data to provide actionable recommendations for irrigation, fertilization, and pest control. Target: commercial farms of 100+ acres in South Asia and Africa."
    },
    {
        "name": "AI Customer Support SaaS",
        "sector": "SaaS / CX",
        "desc": "Autonomous AI agents that resolve 80% of support tickets without human intervention.",
        "idea": "A B2B SaaS product that deploys AI support agents trained on a company's own documentation and past tickets to autonomously resolve customer inquiries. Pricing: per-resolution model. Target: e-commerce and SaaS companies with 500+ monthly tickets."
    },
    {
        "name": "AI Recruitment Screener",
        "sector": "HRTech",
        "desc": "Automated CV screening, skills assessment, and interview scheduling for high-volume hiring.",
        "idea": "An AI recruitment platform that screens thousands of CVs in minutes, conducts async video interviews, scores candidates on skills and culture fit, and schedules final rounds automatically. Target: staffing agencies and enterprise HR teams with 100+ monthly hires."
    },
]

st.markdown('<span class="sec-label">Select a Startup — or Write Your Own Below</span>', unsafe_allow_html=True)

preset_cols = st.columns(3)
for i, p in enumerate(PRESETS):
    with preset_cols[i % 3]:
        if st.button(f"{p['name']}", key=f"preset_{i}"):
            st.session_state["startup_idea"] = p["idea"]
            st.session_state["startup_name"] = p["name"]
            st.rerun()

st.markdown('<div class="div-gold"></div>', unsafe_allow_html=True)

# ── Startup Input ─────────────────────────────────────────────────────────────────
st.markdown('<span class="sec-label">Startup Idea — Full Description</span>', unsafe_allow_html=True)
startup_idea = st.text_area(
    "startup_idea_input",
    value=st.session_state.get("startup_idea", ""),
    placeholder="Describe the startup: what it does, target market, business model, geography, and any traction or differentiators you want the agents to evaluate...",
    height=130,
    label_visibility="collapsed"
)

col_name, col_stage = st.columns(2)
with col_name:
    st.markdown('<span class="sec-label">Startup Name (optional)</span>', unsafe_allow_html=True)
    startup_name = st.text_input(
        "sname",
        value=st.session_state.get("startup_name", ""),
        placeholder="e.g. MedMatch AI",
        label_visibility="collapsed"
    )
with col_stage:
    st.markdown('<span class="sec-label">Stage</span>', unsafe_allow_html=True)
    stage = st.selectbox(
        "stage",
        ["Pre-Seed", "Seed", "Series A", "Series B+", "Concept Only"],
        label_visibility="collapsed"
    )

# ── Model + Settings ──────────────────────────────────────────────────────────────
st.markdown('<div class="div"></div>', unsafe_allow_html=True)

MODELS = {
    "Gemini (Primary)": {
        "gemini/gemini-2.5-flash-preview-04-17": "Gemini 2.5 Flash",
        "gemini/gemini-2.0-flash":               "Gemini 2.0 Flash",
    },
    "Groq (Fallback)": {
        "groq/llama-3.3-70b-versatile": "LLaMA 3.3 70B",
        "groq/mixtral-8x7b-32768":      "Mixtral 8x7B",
    },
}
col_p, col_m = st.columns(2)
with col_p:
    st.markdown('<span class="sec-label">Provider</span>', unsafe_allow_html=True)
    provider_choice = st.selectbox("prov", list(MODELS.keys()), label_visibility="collapsed")
with col_m:
    st.markdown('<span class="sec-label">Model</span>', unsafe_allow_html=True)
    model_opts = MODELS[provider_choice]
    model_id   = st.selectbox("mod", list(model_opts.keys()),
                               format_func=lambda x: model_opts[x],
                               label_visibility="collapsed")

is_gemini = model_id.startswith("gemini/")

with st.expander("⚙  Due Diligence Settings"):
    col_d, col_f = st.columns(2)
    with col_d:
        depth = st.select_slider("Analysis Depth", ["Brief", "Standard", "Detailed"], value="Standard")
    with col_f:
        investor_type = st.selectbox(
            "Investor Perspective",
            ["Venture Capital", "Angel Investor", "Private Equity", "Corporate VC", "Impact Investor"]
        )
    col_g, col_r = st.columns(2)
    with col_g:
        geography = st.selectbox(
            "Target Geography",
            ["Global", "Southeast Asia", "South Asia", "USA & Canada", "Europe", "Middle East & Africa", "Latin America"]
        )
    with col_r:
        currency = st.selectbox("Report Currency", ["USD", "EUR", "GBP", "BDT"])

    include_comparables = st.checkbox("Include comparable companies", value=True)
    include_exit        = st.checkbox("Include exit strategy analysis", value=True)
    include_checklist   = st.checkbox("Include investor DD checklist", value=True)

st.markdown('<div class="div"></div>', unsafe_allow_html=True)
run_btn = st.button("◈  Initiate Due Diligence — Deploy All Agents")


# ══════════════════════════════════════════════════════════════════════════════════
# EXECUTION
# ══════════════════════════════════════════════════════════════════════════════════
if run_btn:
    if not startup_idea.strip():
        st.markdown('<div class="err-box">⚠ Please describe the startup idea before running due diligence.</div>', unsafe_allow_html=True)
        st.stop()

    try:
        from crewai import Agent, Task, Crew, Process, LLM
    except ImportError as e:
        st.markdown(f'<div class="err-box">Import error: {e} — ensure crewai is in requirements.txt</div>', unsafe_allow_html=True)
        st.stop()

    api_key = os.environ.get("GEMINI_API_KEY" if is_gemini else "GROQ_API_KEY", "")
    if not api_key:
        key_name = "GEMINI_API_KEY" if is_gemini else "GROQ_API_KEY"
        st.markdown(f'<div class="err-box">⚠ {key_name} not found in Streamlit Secrets.</div>', unsafe_allow_html=True)
        st.stop()

    t0 = time.time()
    log_ph    = st.empty()
    status_ph = st.empty()

    def ts():
        return f"{round(time.time()-t0,1):>5}s"

    def render_log(lines):
        rows = ""
        for t_str, tag, cls, msg in lines:
            rows += (f'<div class="log-line">'
                     f'<span class="log-t">{t_str}</span>'
                     f'<span class="log-tag {cls}">{tag}</span>'
                     f'<span class="log-msg">{msg}</span></div>')
        log_ph.markdown(f"""
        <div class="log-wrap">
            <div class="log-head">
                <div style="width:8px;height:8px;border-radius:50%;background:#c06060"></div>
                <div style="width:8px;height:8px;border-radius:50%;background:#c09020"></div>
                <div style="width:8px;height:8px;border-radius:50%;background:#608060"></div>
                <span class="log-head-title">DUE DILIGENCE EXECUTION LOG</span>
            </div>
            <div class="log-body">{rows}</div>
        </div>""", unsafe_allow_html=True)

    log = []
    sname = startup_name.strip() if startup_name.strip() else "Unnamed Startup"
    log.append((ts(), "SYS",   "t-sys",   f"Startup: {sname} · Stage: {stage} · {model_id.split('/')[1]}"))
    log.append((ts(), "SYS",   "t-sys",   f"Depth: {depth} · Perspective: {investor_type} · Geography: {geography}"))
    render_log(log)

    # ── Depth / perspective context ───────────────────────────────────────────────
    depth_map = {
        "Brief":    "Provide a concise focused analysis. 2-3 key points per section.",
        "Standard": "Provide a thorough analysis with clear supporting reasoning.",
        "Detailed": "Provide an exhaustive analysis. Cover every sub-dimension. Be specific with estimates.",
    }
    investor_context = {
        "Venture Capital":  "You prioritize 10x+ return potential, scalability, and defensibility of market position.",
        "Angel Investor":   "You prioritize founding team quality, early traction, and capital efficiency.",
        "Private Equity":   "You prioritize unit economics, EBITDA path, and acquisition multiples.",
        "Corporate VC":     "You prioritize strategic fit, IP value, and ecosystem synergies.",
        "Impact Investor":  "You prioritize social impact metrics alongside financial returns.",
    }
    depth_instr     = depth_map[depth]
    inv_context     = investor_context[investor_type]
    geo_context     = f"Focus the analysis on the {geography} market context."
    currency_sym    = {"USD": "$", "EUR": "€", "GBP": "£", "BDT": "৳"}[currency]

    comp_instr    = "Include 2-3 comparable companies with their valuations and differentiators." if include_comparables else ""
    exit_instr    = "Include a brief exit strategy analysis (acquisition targets, IPO path, or strategic buyer landscape)." if include_exit else ""
    checklist_instr = "End with a short investor DD checklist: 5 questions any investor should ask before writing a check." if include_checklist else ""

    # ── LLM ───────────────────────────────────────────────────────────────────────
    try:
        llm = LLM(model=model_id, temperature=0.3)
    except Exception as e:
        st.markdown(f'<div class="err-box">LLM init error: {e}</div>', unsafe_allow_html=True)
        st.stop()

    log.append((ts(), "AGENT", "t-agent", "Instantiating 5 specialist agents..."))
    render_log(log)

    # ── Agents ────────────────────────────────────────────────────────────────────
    manager = Agent(
        role="Startup Evaluation Manager",
        goal=(
            "Orchestrate a comprehensive due diligence process. "
            "Delegate market, financial, risk, and investment analysis to specialists. "
            "Consolidate all findings into a structured final report."
        ),
        backstory=(
            f"You are a senior partner at a top-tier {investor_type} firm with 20 years of experience "
            f"leading due diligence processes for 200+ startups. {inv_context} "
            f"You are rigorous, structured, and never speculate without grounding in evidence."
        ),
        llm=llm,
        allow_delegation=True,
        verbose=True,
        max_iter=3,
    )

    market_analyst = Agent(
        role="Market Analyst",
        goal="Evaluate total addressable market, growth trajectory, demand signals, and competitive landscape.",
        backstory=(
            f"You are a senior market research analyst specializing in technology sectors. "
            f"{geo_context} You are known for precise market sizing, trend identification, "
            f"and identifying whitespace in crowded markets. You always cite estimated market sizes in {currency}."
        ),
        llm=llm,
        verbose=True,
        max_iter=4,
    )

    financial_analyst = Agent(
        role="Financial Analyst",
        goal="Assess revenue model, unit economics, scalability path, and financial viability.",
        backstory=(
            f"You are a startup CFO and financial modeler who has built financial models for 50+ startups. "
            f"You evaluate CAC, LTV, gross margin, burn rate, and path to profitability. "
            f"You express all financial estimates in {currency} ({currency_sym})."
        ),
        llm=llm,
        verbose=True,
        max_iter=4,
    )

    risk_analyst = Agent(
        role="Risk Analyst",
        goal="Identify and assess operational, regulatory, market, technical, and execution risks.",
        backstory=(
            "You are a venture risk specialist who has seen 300+ startup failures. "
            "You identify not just obvious risks but second-order threats that founders overlook. "
            "You rate each risk by severity (High/Medium/Low) and likelihood."
        ),
        llm=llm,
        verbose=True,
        max_iter=4,
    )

    investment_advisor = Agent(
        role="Investment Advisor",
        goal=(
            "Synthesize all specialist analyses into a final investment recommendation with a scored verdict. "
            "Always output a valid JSON block with scores and decision at the end of your analysis."
        ),
        backstory=(
            f"You are a {investor_type} partner who makes the final call on investments. "
            f"You weigh market potential, financial viability, risk-adjusted returns, and execution risk. "
            f"You always end your report with a JSON block containing: "
            f'market_score (0-10), financial_score (0-10), risk_score (0-10, higher = less risky), '
            f'overall_score (0-10), final_decision (one of: INVEST / CONDITIONAL / WATCH / PASS), '
            f'and rationale (one sentence). This JSON must be valid and parseable.'
        ),
        llm=llm,
        verbose=True,
        max_iter=5,
    )

    log.append((ts(), "AGENT", "t-agent", "Manager · Market Analyst · Financial Analyst · Risk Analyst · Investment Advisor"))
    render_log(log)

    # ── Tasks ─────────────────────────────────────────────────────────────────────
    market_task = Task(
        description=(
            f"Conduct a thorough MARKET ANALYSIS of the following startup:\n\n"
            f"Startup: {sname}\nStage: {stage}\n\nIdea: {startup_idea}\n\n"
            f"{depth_instr} {geo_context} {comp_instr}\n\n"
            f"Cover: TAM/SAM/SOM sizing, growth rate, demand drivers, customer segments, "
            f"competitive landscape, and market timing. Score market opportunity 1-10."
        ),
        expected_output=(
            "A structured market analysis with TAM estimate, competitive landscape, "
            "key demand drivers, and a market opportunity score out of 10."
        ),
        agent=market_analyst,
    )

    financial_task = Task(
        description=(
            f"Conduct a thorough FINANCIAL ANALYSIS of the following startup:\n\n"
            f"Startup: {sname}\nStage: {stage}\n\nIdea: {startup_idea}\n\n"
            f"{depth_instr}\n\n"
            f"Cover: revenue model and streams, realistic pricing, estimated CAC and LTV, "
            f"gross margin potential, scalability, capital requirements, and path to profitability. "
            f"Express estimates in {currency} ({currency_sym}). Score financial viability 1-10."
        ),
        expected_output=(
            "A structured financial analysis with revenue model breakdown, unit economics estimates, "
            "capital requirements, and a financial viability score out of 10."
        ),
        agent=financial_analyst,
    )

    risk_task = Task(
        description=(
            f"Conduct a thorough RISK ANALYSIS of the following startup:\n\n"
            f"Startup: {sname}\nStage: {stage}\n\nIdea: {startup_idea}\n\n"
            f"{depth_instr}\n\n"
            f"Identify and assess: market risks, regulatory/compliance risks, technical risks, "
            f"competitive risks, execution risks, and macroeconomic risks. "
            f"Rate each risk High/Medium/Low for severity and likelihood. "
            f"Score overall risk profile 1-10 (10 = lowest risk)."
        ),
        expected_output=(
            "A structured risk matrix with each risk rated by severity and likelihood, "
            "mitigation strategies, and an overall risk score out of 10."
        ),
        agent=risk_analyst,
    )

    investment_task = Task(
        description=(
            f"Based on the market analysis, financial analysis, and risk analysis above, "
            f"produce a FINAL INVESTMENT RECOMMENDATION for:\n\n"
            f"Startup: {sname}\nStage: {stage}\nInvestor Type: {investor_type}\n\n"
            f"{depth_instr} {exit_instr} {checklist_instr}\n\n"
            f"Your analysis must conclude with a JSON block in EXACTLY this format:\n"
            f"```json\n"
            f'{{\n'
            f'  "startup_name": "{sname}",\n'
            f'  "stage": "{stage}",\n'
            f'  "market_score": <0-10>,\n'
            f'  "financial_score": <0-10>,\n'
            f'  "risk_score": <0-10>,\n'
            f'  "overall_score": <0-10>,\n'
            f'  "final_decision": "<INVEST|CONDITIONAL|WATCH|PASS>",\n'
            f'  "rationale": "<one sentence>",\n'
            f'  "recommended_check_size": "<e.g. {currency_sym}500K seed>",\n'
            f'  "key_condition": "<most important condition or milestone>"\n'
            f'}}\n'
            f"```"
        ),
        expected_output=(
            "A final investment memo with recommendation, supporting rationale, "
            "and a valid JSON verdict block."
        ),
        agent=investment_advisor,
        context=[market_task, financial_task, risk_task],
    )

    # ── Crew ──────────────────────────────────────────────────────────────────────
    crew = Crew(
        agents=[manager, market_analyst, financial_analyst, risk_analyst, investment_advisor],
        tasks=[market_task, financial_task, risk_task, investment_task],
        process=Process.sequential,
        verbose=False,
    )

    log.append((ts(), "TASK",  "t-task",  "4 tasks queued: Market → Financial → Risk → Investment"))
    log.append((ts(), "SYS",   "t-sys",   "Process: Sequential · Delegation: enabled on manager"))
    render_log(log)

    status_ph.markdown(
        '<div style="font-size:0.84rem;color:var(--muted);font-family:var(--mono);'
        'margin-bottom:1rem;letter-spacing:0.04em">'
        '⟳ Agents conducting due diligence... this takes 60–120 seconds</div>',
        unsafe_allow_html=True
    )

    # ── Execute ───────────────────────────────────────────────────────────────────
    try:
        result = crew.kickoff()
        elapsed = round(time.time() - t0, 1)

        log.append((ts(), "OK", "t-ok", f"Due diligence complete in {elapsed}s"))
        render_log(log)
        status_ph.empty()

        # ── Extract individual task outputs ────────────────────────────────────────
        def safe_output(task):
            try:
                return str(task.output).strip() if task.output else ""
            except Exception:
                return ""

        market_out    = safe_output(market_task)
        financial_out = safe_output(financial_task)
        risk_out      = safe_output(risk_task)
        investment_out = safe_output(investment_task)
        full_result   = str(result).strip()

        # ── Parse JSON verdict ─────────────────────────────────────────────────────
        verdict = {}
        json_search_text = investment_out + "\n" + full_result
        json_match = re.search(r'```json\s*(\{.*?\})\s*```', json_search_text, re.DOTALL)
        if not json_match:
            json_match = re.search(r'(\{[^{}]*"final_decision"[^{}]*\})', json_search_text, re.DOTALL)
        if json_match:
            try:
                verdict = json.loads(json_match.group(1))
            except Exception:
                pass

        # ── Score cards ────────────────────────────────────────────────────────────
        ms = verdict.get("market_score",    "—")
        fs = verdict.get("financial_score", "—")
        rs = verdict.get("risk_score",      "—")
        os_ = verdict.get("overall_score",  "—")
        decision = verdict.get("final_decision", "—")
        rationale = verdict.get("rationale", "")
        check_size = verdict.get("recommended_check_size", "—")
        condition  = verdict.get("key_condition", "—")

        st.markdown('<div class="div"></div>', unsafe_allow_html=True)
        st.markdown(f'<span class="sec-label">Verdict — {sname}</span>', unsafe_allow_html=True)

        st.markdown(f"""
        <div class="score-grid">
            <div class="score-card sc-market">
                <div class="score-num">{ms}<span style="font-size:1rem">/10</span></div>
                <div class="score-label">Market Score</div>
            </div>
            <div class="score-card sc-financial">
                <div class="score-num">{fs}<span style="font-size:1rem">/10</span></div>
                <div class="score-label">Financial Score</div>
            </div>
            <div class="score-card sc-risk">
                <div class="score-num">{rs}<span style="font-size:1rem">/10</span></div>
                <div class="score-label">Risk Score</div>
            </div>
            <div class="score-card sc-final">
                <div class="score-num">{os_}<span style="font-size:1rem">/10</span></div>
                <div class="score-label">Overall Score</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        # Decision badge
        dec_class_map = {
            "INVEST": "decision-invest",
            "CONDITIONAL": "decision-conditional",
            "WATCH": "decision-watch",
            "PASS": "decision-pass",
        }
        dec_icon_map = {
            "INVEST": "✓", "CONDITIONAL": "◎", "WATCH": "◉", "PASS": "✗", "—": "·"
        }
        dec_cls  = dec_class_map.get(decision, "decision-watch")
        dec_icon = dec_icon_map.get(decision, "·")

        st.markdown(f"""
        <div class="decision-badge {dec_cls}">
            {dec_icon} &nbsp; {decision}
        </div>
        """, unsafe_allow_html=True)

        if rationale:
            st.markdown(f'<div style="font-size:0.88rem;color:var(--muted);margin-bottom:0.5rem;'
                       f'font-style:italic">"{rationale}"</div>', unsafe_allow_html=True)

        col_c, col_k = st.columns(2)
        with col_c:
            st.markdown(f'<div style="font-size:0.78rem;color:var(--muted2);font-family:var(--mono)">'
                       f'CHECK SIZE &nbsp;<strong style="color:var(--text)">{check_size}</strong></div>',
                       unsafe_allow_html=True)
        with col_k:
            st.markdown(f'<div style="font-size:0.78rem;color:var(--muted2);font-family:var(--mono)">'
                       f'KEY CONDITION &nbsp;<strong style="color:var(--text)">{condition}</strong></div>',
                       unsafe_allow_html=True)

        st.markdown('<div class="div-gold"></div>', unsafe_allow_html=True)

        # ── Report sections ────────────────────────────────────────────────────────
        st.markdown('<span class="sec-label">Full Due Diligence Report</span>', unsafe_allow_html=True)

        sections = [
            ("📊", "rs-market",    "Market Analysis",             "Market Analyst",      market_out    or full_result),
            ("💰", "rs-financial", "Financial Analysis",          "Financial Analyst",   financial_out or full_result),
            ("⚠️",  "rs-risk",     "Risk Assessment",             "Risk Analyst",        risk_out      or full_result),
            ("🎯", "rs-final",    "Investment Recommendation",    "Investment Advisor",  investment_out or full_result),
        ]

        for icon, rs_cls, title, agent_name, content in sections:
            if content:
                st.markdown(f"""
                <div class="report-section">
                    <div class="report-section-header">
                        <div class="rs-icon {rs_cls}">{icon}</div>
                        <span class="rs-title">{title}</span>
                        <span class="rs-agent">{agent_name}</span>
                    </div>
                    <div class="report-body">{content.replace(chr(10), '<br>')}</div>
                </div>
                """, unsafe_allow_html=True)

        # ── JSON verdict panel ────────────────────────────────────────────────────
        if verdict:
            st.markdown('<div class="div"></div>', unsafe_allow_html=True)
            st.markdown('<span class="sec-label">Machine-Readable Verdict — JSON Output</span>', unsafe_allow_html=True)
            pretty_json = json.dumps(verdict, indent=2)
            st.markdown(f"""
            <div class="json-panel">
                <pre>{pretty_json}</pre>
            </div>
            """, unsafe_allow_html=True)
        else:
            # Try to surface any JSON-like block from the output
            fallback_json = re.search(r'(\{[^{}]{100,}\})', full_result, re.DOTALL)
            if fallback_json:
                st.markdown('<div class="div"></div>', unsafe_allow_html=True)
                st.markdown('<span class="sec-label">Raw JSON Output</span>', unsafe_allow_html=True)
                st.markdown(f"""
                <div class="json-panel"><pre>{fallback_json.group(1)}</pre></div>
                """, unsafe_allow_html=True)

    except Exception as e:
        log.append((ts(), "ERR", "t-err", str(e)[:100]))
        render_log(log)
        status_ph.empty()
        st.markdown(f'<div class="err-box">Agent execution error: {e}</div>', unsafe_allow_html=True)


# ── Footer ────────────────────────────────────────────────────────────────────────
st.markdown('<div class="div"></div>', unsafe_allow_html=True)
st.markdown("""
<div style="display:flex;justify-content:space-between;align-items:center;
     padding-top:0.5rem;font-size:0.7rem;color:var(--muted2);font-family:var(--mono);
     border-top:1px solid var(--border)">
    <span>agent-forge · day 7 of 15</span>
    <span>crewai hierarchical · gemini 2.5 flash · groq fallback</span>
    <span>startup due diligence system</span>
</div>
""", unsafe_allow_html=True)
