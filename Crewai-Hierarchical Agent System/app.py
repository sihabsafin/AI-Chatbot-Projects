import streamlit as st
import os
import time
from crewai import Agent, Task, Crew, Process, LLM

# ─────────────────────────────────────────────
#  PAGE CONFIG
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="AgentFlow — Day 3 Hierarchical AI",
    page_icon="👑",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ─────────────────────────────────────────────
#  CUSTOM CSS
# ─────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=Space+Mono:wght@400;700&display=swap');

/* ── Root Variables ── */
:root {
    --bg:        #080b10;
    --bg2:       #0d1117;
    --bg3:       #141922;
    --border:    rgba(255,255,255,0.07);
    --accent:    #f0c040;
    --accent2:   #4af0a0;
    --accent3:   #40a0f0;
    --text:      #e8edf5;
    --muted:     #6b7a92;
    --manager:   #f0c040;
    --research:  #4af0a0;
    --strategy:  #40a0f0;
    --output:    #c084fc;
}

/* ── Global Reset ── */
html, body, [class*="css"] {
    font-family: 'Syne', sans-serif;
    background: var(--bg);
    color: var(--text);
}
.stApp { background: var(--bg); }

/* ── Hide Streamlit chrome ── */
#MainMenu, footer, header { visibility: hidden; }
.block-container { padding: 2rem 3rem; max-width: 1400px; margin: 0 auto; }

/* ── Hero Header ── */
.hero {
    text-align: center;
    padding: 3rem 0 2rem;
    position: relative;
}
.hero-badge {
    display: inline-block;
    font-family: 'Space Mono', monospace;
    font-size: 0.7rem;
    letter-spacing: 0.2em;
    color: var(--accent);
    border: 1px solid var(--accent);
    padding: 0.3rem 1rem;
    border-radius: 2px;
    margin-bottom: 1.2rem;
    text-transform: uppercase;
}
.hero h1 {
    font-size: clamp(2.2rem, 5vw, 4rem);
    font-weight: 800;
    line-height: 1.05;
    letter-spacing: -0.03em;
    color: var(--text);
    margin: 0 0 0.8rem;
}
.hero h1 span { color: var(--accent); }
.hero-sub {
    font-family: 'Space Mono', monospace;
    font-size: 0.82rem;
    color: var(--muted);
    letter-spacing: 0.05em;
}

/* ── Architecture Diagram ── */
.arch-wrap {
    background: var(--bg2);
    border: 1px solid var(--border);
    border-radius: 12px;
    padding: 1.8rem 2rem;
    margin: 2rem 0;
    position: relative;
    overflow: hidden;
}
.arch-wrap::before {
    content: 'ARCHITECTURE';
    position: absolute;
    top: 1.2rem; right: 1.5rem;
    font-family: 'Space Mono', monospace;
    font-size: 0.6rem;
    letter-spacing: 0.15em;
    color: var(--muted);
}
.arch-flow {
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 0.5rem;
    flex-wrap: wrap;
}
.arch-node {
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 0.3rem;
}
.arch-icon {
    width: 52px; height: 52px;
    border-radius: 10px;
    display: flex; align-items: center; justify-content: center;
    font-size: 1.3rem;
    font-weight: 700;
}
.arch-icon.user   { background: rgba(255,255,255,0.06); }
.arch-icon.mgr    { background: rgba(240,192,64,0.15); border: 1px solid rgba(240,192,64,0.4); }
.arch-icon.res    { background: rgba(74,240,160,0.12); border: 1px solid rgba(74,240,160,0.35); }
.arch-icon.str    { background: rgba(64,160,240,0.12); border: 1px solid rgba(64,160,240,0.35); }
.arch-icon.out    { background: rgba(192,132,252,0.12); border: 1px solid rgba(192,132,252,0.35); }
.arch-label {
    font-size: 0.65rem;
    font-family: 'Space Mono', monospace;
    color: var(--muted);
    text-align: center;
    letter-spacing: 0.05em;
}
.arch-arrow { color: var(--border); font-size: 1.2rem; margin-top: -1rem; }
.arch-arrow.down { transform: rotate(90deg); }

/* ── Config Panel ── */
.config-card {
    background: var(--bg2);
    border: 1px solid var(--border);
    border-radius: 12px;
    padding: 1.8rem;
    margin-bottom: 1.5rem;
}
.section-label {
    font-family: 'Space Mono', monospace;
    font-size: 0.65rem;
    letter-spacing: 0.18em;
    color: var(--muted);
    text-transform: uppercase;
    margin-bottom: 0.8rem;
}

/* ── Preset Buttons ── */
.stButton > button {
    background: var(--bg3) !important;
    border: 1px solid var(--border) !important;
    color: var(--text) !important;
    border-radius: 8px !important;
    font-family: 'Space Mono', monospace !important;
    font-size: 0.72rem !important;
    transition: all 0.2s !important;
    padding: 0.5rem 0.8rem !important;
    width: 100% !important;
}
.stButton > button:hover {
    border-color: var(--accent) !important;
    color: var(--accent) !important;
    background: rgba(240,192,64,0.06) !important;
}

/* ── Run Button ── */
.run-btn > button {
    background: var(--accent) !important;
    color: #000 !important;
    border: none !important;
    font-weight: 700 !important;
    font-size: 0.9rem !important;
    letter-spacing: 0.05em !important;
    border-radius: 8px !important;
    padding: 0.75rem 2rem !important;
    width: 100% !important;
    transition: opacity 0.2s !important;
}
.run-btn > button:hover { opacity: 0.85 !important; }

/* ── Input overrides ── */
.stTextArea textarea, .stTextInput input, .stSelectbox select {
    background: var(--bg3) !important;
    border: 1px solid var(--border) !important;
    border-radius: 8px !important;
    color: var(--text) !important;
    font-family: 'Space Mono', monospace !important;
    font-size: 0.82rem !important;
}
.stTextArea textarea:focus, .stTextInput input:focus {
    border-color: var(--accent) !important;
    box-shadow: 0 0 0 2px rgba(240,192,64,0.15) !important;
}
label, .stSelectbox label, .stTextArea label { color: var(--muted) !important; font-size: 0.8rem !important; }

/* ── Agent Status Cards ── */
.agent-grid {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 1rem;
    margin: 1.5rem 0;
}
.agent-card {
    background: var(--bg2);
    border: 1px solid var(--border);
    border-radius: 10px;
    padding: 1.2rem;
    position: relative;
    overflow: hidden;
    transition: border-color 0.3s;
}
.agent-card.manager  { border-top: 2px solid var(--manager); }
.agent-card.research { border-top: 2px solid var(--research); }
.agent-card.strategy { border-top: 2px solid var(--strategy); }
.agent-card-icon { font-size: 1.6rem; margin-bottom: 0.5rem; }
.agent-card-role {
    font-family: 'Space Mono', monospace;
    font-size: 0.62rem;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    margin-bottom: 0.2rem;
}
.agent-card.manager  .agent-card-role { color: var(--manager); }
.agent-card.research .agent-card-role { color: var(--research); }
.agent-card.strategy .agent-card-role { color: var(--strategy); }
.agent-card-name { font-size: 0.9rem; font-weight: 700; margin-bottom: 0.4rem; }
.agent-card-desc { font-size: 0.72rem; color: var(--muted); line-height: 1.5; }
.agent-status {
    display: inline-flex;
    align-items: center;
    gap: 0.35rem;
    font-family: 'Space Mono', monospace;
    font-size: 0.62rem;
    margin-top: 0.8rem;
    padding: 0.25rem 0.6rem;
    border-radius: 4px;
    background: rgba(255,255,255,0.04);
    color: var(--muted);
}
.agent-status.active { color: var(--accent2); background: rgba(74,240,160,0.08); }
.status-dot { width: 6px; height: 6px; border-radius: 50%; background: currentColor; }
.status-dot.pulse { animation: pulse 1s infinite; }
@keyframes pulse { 0%,100% { opacity: 1; } 50% { opacity: 0.3; } }

/* ── Progress / Log ── */
.log-wrap {
    background: var(--bg2);
    border: 1px solid var(--border);
    border-radius: 10px;
    padding: 1.2rem 1.4rem;
    margin: 1rem 0;
    font-family: 'Space Mono', monospace;
    font-size: 0.75rem;
    line-height: 1.8;
    max-height: 280px;
    overflow-y: auto;
}
.log-entry { display: flex; gap: 0.8rem; align-items: flex-start; }
.log-ts { color: var(--muted); white-space: nowrap; flex-shrink: 0; }
.log-msg { color: var(--text); }
.log-msg.mgr  { color: var(--manager); }
.log-msg.res  { color: var(--research); }
.log-msg.str  { color: var(--strategy); }
.log-msg.sys  { color: var(--muted); }

/* ── Output Panels ── */
.output-grid {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 1.2rem;
    margin-top: 1.5rem;
}
@media (max-width: 900px) { .output-grid { grid-template-columns: 1fr; } .agent-grid { grid-template-columns: 1fr; } }

.output-panel {
    background: var(--bg2);
    border: 1px solid var(--border);
    border-radius: 12px;
    overflow: hidden;
}
.output-panel.full { grid-column: 1 / -1; }
.panel-header {
    padding: 0.9rem 1.2rem;
    display: flex;
    align-items: center;
    gap: 0.6rem;
    border-bottom: 1px solid var(--border);
}
.panel-header.mgr  { background: rgba(240,192,64,0.07); }
.panel-header.res  { background: rgba(74,240,160,0.07); }
.panel-header.str  { background: rgba(64,160,240,0.07); }
.panel-header.fin  { background: rgba(192,132,252,0.07); }
.panel-icon { font-size: 1.1rem; }
.panel-title {
    font-family: 'Space Mono', monospace;
    font-size: 0.72rem;
    letter-spacing: 0.1em;
    font-weight: 700;
    text-transform: uppercase;
}
.panel-header.mgr .panel-title { color: var(--manager); }
.panel-header.res .panel-title { color: var(--research); }
.panel-header.str .panel-title { color: var(--strategy); }
.panel-header.fin .panel-title { color: var(--output); }
.panel-body { padding: 1.2rem; font-size: 0.85rem; line-height: 1.75; color: var(--text); white-space: pre-wrap; }

/* ── Divider ── */
.divider {
    height: 1px;
    background: var(--border);
    margin: 2rem 0;
}

/* ── Info Pills ── */
.pill-row { display: flex; gap: 0.6rem; flex-wrap: wrap; margin: 0.6rem 0 1.2rem; }
.pill {
    font-family: 'Space Mono', monospace;
    font-size: 0.62rem;
    padding: 0.3rem 0.75rem;
    border-radius: 4px;
    letter-spacing: 0.08em;
    text-transform: uppercase;
}
.pill.yellow { background: rgba(240,192,64,0.12); color: var(--accent); }
.pill.green  { background: rgba(74,240,160,0.12); color: var(--accent2); }
.pill.blue   { background: rgba(64,160,240,0.12); color: var(--accent3); }
.pill.purple { background: rgba(192,132,252,0.12); color: var(--output); }

/* ── Scrollbar ── */
::-webkit-scrollbar { width: 4px; }
::-webkit-scrollbar-track { background: transparent; }
::-webkit-scrollbar-thumb { background: var(--border); border-radius: 4px; }
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
#  HERO
# ─────────────────────────────────────────────
st.markdown("""
<div class="hero">
    <div class="hero-badge">⚡ Day 3 — Hierarchical Process</div>
    <h1>Agent<span>Flow</span> Command</h1>
    <p class="hero-sub">Manager Agent → Delegates → Workers Execute → Final Report</p>
</div>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
#  ARCHITECTURE DIAGRAM
# ─────────────────────────────────────────────
st.markdown("""
<div class="arch-wrap">
    <div class="arch-flow">
        <div class="arch-node">
            <div class="arch-icon user">👤</div>
            <div class="arch-label">User Input</div>
        </div>
        <div class="arch-arrow">→</div>
        <div class="arch-node">
            <div class="arch-icon mgr">👑</div>
            <div class="arch-label">Manager Agent<br/>Orchestrates</div>
        </div>
        <div class="arch-arrow">→</div>
        <div class="arch-node">
            <div class="arch-icon res">🔬</div>
            <div class="arch-label">Market<br/>Researcher</div>
        </div>
        <div class="arch-arrow">→</div>
        <div class="arch-node">
            <div class="arch-icon str">📈</div>
            <div class="arch-label">Strategy<br/>Consultant</div>
        </div>
        <div class="arch-arrow">→</div>
        <div class="arch-node">
            <div class="arch-icon out">📋</div>
            <div class="arch-label">Final<br/>Report</div>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
#  AGENT CARDS
# ─────────────────────────────────────────────
st.markdown("""
<div class="agent-grid">
    <div class="agent-card manager">
        <div class="agent-card-icon">👑</div>
        <div class="agent-card-role">Manager Agent</div>
        <div class="agent-card-name">Project Orchestrator</div>
        <div class="agent-card-desc">Analyzes business goals, breaks into subtasks, delegates to the right specialists, and reviews final output quality.</div>
        <div class="agent-status"><span class="status-dot"></span> allow_delegation=True</div>
    </div>
    <div class="agent-card research">
        <div class="agent-card-icon">🔬</div>
        <div class="agent-card-role">Worker Agent</div>
        <div class="agent-card-name">Market Research Specialist</div>
        <div class="agent-card-desc">Delivers deep market sizing, trend analysis, competitor positioning, and customer profile breakdowns.</div>
        <div class="agent-status"><span class="status-dot"></span> Awaiting Delegation</div>
    </div>
    <div class="agent-card strategy">
        <div class="agent-card-icon">📈</div>
        <div class="agent-card-role">Worker Agent</div>
        <div class="agent-card-name">Business Strategy Consultant</div>
        <div class="agent-card-desc">Converts research insights into monetization models, pricing strategies, go-to-market plans, and risk frameworks.</div>
        <div class="agent-status"><span class="status-dot"></span> Awaiting Delegation</div>
    </div>
</div>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
#  PRESETS
# ─────────────────────────────────────────────
PRESETS = {
    "🏠 AI Real Estate Analyzer": "An AI-powered real estate deal analyzer that helps investors evaluate properties, predict rental yields, estimate renovation ROI, and identify undervalued deals using computer vision and market data.",
    "⚖️ AI Legal Document Assistant": "An AI SaaS platform for solo lawyers and small law firms that automates contract drafting, clause extraction, compliance checking, and legal research using LLMs.",
    "💪 AI Fitness Coaching App": "A personalized AI fitness coaching app that integrates with wearables, creates adaptive workout plans, provides real-time form correction via camera, and adjusts nutrition guidance based on progress.",
    "🛒 AI Dropshipping Research Tool": "An AI tool for ecommerce entrepreneurs that identifies winning products, analyzes competitor stores, predicts trend lifecycles, and automates Shopify product listings with optimized descriptions.",
}

st.markdown('<div class="config-card">', unsafe_allow_html=True)
st.markdown('<div class="section-label">Quick Presets</div>', unsafe_allow_html=True)

cols = st.columns(4)
for i, (label, desc) in enumerate(PRESETS.items()):
    with cols[i]:
        if st.button(label, key=f"preset_{i}"):
            st.session_state["business_idea"] = desc

# Business idea input
if "business_idea" not in st.session_state:
    st.session_state["business_idea"] = ""

st.markdown("---", unsafe_allow_html=True)
business_idea = st.text_area(
    "Business Idea",
    value=st.session_state["business_idea"],
    placeholder="Describe your business idea in detail...",
    height=100,
    key="idea_input",
)

# Model selection
col1, col2 = st.columns(2)
with col1:
    model_choice = st.selectbox(
        "LLM Model",
        ["llama-3.3-70b-versatile", "llama-3.1-8b-instant", "mixtral-8x7b-32768"],
        help="70B = best quality, 8B = fastest",
    )
with col2:
    manager_mode = st.selectbox(
        "Manager Review Mode",
        ["Standard — delegate and consolidate", "Strict — review and refine weak sections"],
        help="Strict mode adds a quality review pass",
    )

st.markdown('</div>', unsafe_allow_html=True)

# API Key
with st.sidebar:
    st.markdown("### ⚙️ Configuration")
    api_key = st.text_input("Groq API Key", type="password", placeholder="gsk_...")
    st.markdown("""
    **How Hierarchical differs from Sequential:**
    - Manager understands the full goal
    - Manager *decides* which agent handles what
    - Workers don't know the plan upfront
    - Manager reviews quality before finalizing
    
    `Process.hierarchical` + `allow_delegation=True`
    """)

# ─────────────────────────────────────────────
#  RUN BUTTON
# ─────────────────────────────────────────────
st.markdown('<div class="run-btn">', unsafe_allow_html=True)
run = st.button("🚀 Launch Hierarchical Agent System", key="run_btn")
st.markdown('</div>', unsafe_allow_html=True)

# ─────────────────────────────────────────────
#  EXECUTION
# ─────────────────────────────────────────────
if run:
    final_key = api_key or os.environ.get("GROQ_API_KEY", "")
    if not final_key:
        st.error("⚠️ Please enter your Groq API key in the sidebar.")
        st.stop()
    if not business_idea.strip():
        st.error("⚠️ Please enter a business idea.")
        st.stop()

    os.environ["GROQ_API_KEY"] = final_key

    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

    # Live log placeholder
    log_ph = st.empty()
    logs = []

    def add_log(msg, kind="sys"):
        ts = time.strftime("%H:%M:%S")
        logs.append((ts, msg, kind))
        html = '<div class="log-wrap">'
        for t, m, k in logs[-20:]:
            html += f'<div class="log-entry"><span class="log-ts">[{t}]</span><span class="log-msg {k}">{m}</span></div>'
        html += '</div>'
        log_ph.markdown(html, unsafe_allow_html=True)

    add_log("Initializing hierarchical agent system...", "sys")

    # ── Build LLM ──
    llm = LLM(model=f"groq/{model_choice}", api_key=final_key)

    # ── Manager description based on mode ──
    review_instruction = (
        "\n\nAfter all specialists complete their work, carefully review the outputs. "
        "Identify any weak, vague, or incomplete sections and request improvements before delivering the final consolidated report."
        if "Strict" in manager_mode else ""
    )

    # ── Agents ──
    add_log("Spawning Manager Agent (allow_delegation=True)...", "mgr")

    manager = Agent(
        role="Project Manager",
        goal="Analyze the business request, delegate tasks to the right specialists, and deliver a comprehensive consolidated business analysis.",
        backstory=(
            "You are a seasoned AI project manager with 20 years of experience running high-stakes business analysis projects. "
            "You excel at breaking complex goals into focused subtasks, assigning them to the right specialists, "
            "and synthesizing their outputs into clear executive-level reports."
        ),
        verbose=True,
        allow_delegation=True,
        llm=llm,
    )

    add_log("Spawning Market Research Specialist...", "res")

    researcher = Agent(
        role="Market Research Specialist",
        goal="Provide exhaustive market analysis including market size, customer segments, competitor landscape, and growth opportunities.",
        backstory=(
            "You are a top-tier market research analyst who has conducted studies for Fortune 500 companies and Y Combinator startups alike. "
            "You're known for uncovering non-obvious market opportunities and delivering data-rich, actionable insights."
        ),
        verbose=True,
        allow_delegation=False,
        llm=llm,
    )

    add_log("Spawning Business Strategy Consultant...", "str")

    strategist = Agent(
        role="Business Strategy Consultant",
        goal="Design a complete business strategy including monetization, pricing, go-to-market, and risk mitigation.",
        backstory=(
            "You are an elite business strategy consultant who has helped scale dozens of B2B and B2C startups from 0 to $10M ARR. "
            "You specialize in translating market research into concrete, executable business strategies."
        ),
        verbose=True,
        allow_delegation=False,
        llm=llm,
    )

    # ── Main Task (owned by Manager) ──
    add_log("Creating hierarchical task — Manager owns and delegates...", "mgr")

    main_task = Task(
        description=f"""
You are the Project Manager. A client has submitted the following business idea:

---
{business_idea.strip()}
---

Your job:
1. DELEGATE market research to the Market Research Specialist — they must cover:
   - Market size and growth trajectory
   - Ideal customer profile (ICP) with 2–3 specific segments
   - Top 3 competitors with their weaknesses
   - 3 underserved market opportunities

2. DELEGATE business strategy to the Business Strategy Consultant — they must cover:
   - Recommended business model (B2B / B2C / marketplace / SaaS)
   - Pricing tiers with specific price points
   - Top 3 revenue streams
   - 90-day go-to-market plan
   - Top 3 risks with mitigation strategies

3. CONSOLIDATE both outputs into a single polished executive report with clear sections.{review_instruction}

Format your final output with these sections clearly labeled:
## EXECUTIVE SUMMARY
## MARKET RESEARCH FINDINGS  
## BUSINESS STRATEGY
## ACTION PLAN
""",
        expected_output=(
            "A comprehensive business analysis report with four clearly labeled sections: "
            "Executive Summary, Market Research Findings, Business Strategy, and Action Plan. "
            "Each section should be detailed, specific, and directly relevant to the submitted business idea."
        ),
        agent=manager,
    )

    # ── Crew ──
    add_log("Assembling Crew with Process.hierarchical...", "sys")

    crew = Crew(
        agents=[manager, researcher, strategist],
        tasks=[main_task],
        process=Process.hierarchical,
        manager_agent=manager,
        verbose=True,
    )

    add_log("🚀 Kickoff! Manager is analyzing and delegating...", "mgr")

    result_placeholder = st.empty()

    try:
        with st.spinner(""):
            result = crew.kickoff()
        add_log("✅ All agents completed. Consolidating report...", "sys")
    except Exception as e:
        add_log(f"❌ Error: {str(e)}", "sys")
        st.error(f"Execution failed: {e}")
        st.stop()

    result_str = str(result)

    # ── Parse sections ──
    def extract_section(text, header, next_headers):
        import re
        pattern = re.compile(
            rf"##\s*{re.escape(header)}\s*\n(.*?)(?={'|'.join([f'##.*?{re.escape(h)}' for h in next_headers])}|$)",
            re.DOTALL | re.IGNORECASE,
        )
        m = pattern.search(text)
        return m.group(1).strip() if m else ""

    exec_summary  = extract_section(result_str, "EXECUTIVE SUMMARY",     ["MARKET RESEARCH", "BUSINESS STRATEGY", "ACTION PLAN"])
    market_data   = extract_section(result_str, "MARKET RESEARCH FINDINGS", ["BUSINESS STRATEGY", "ACTION PLAN"])
    strategy_data = extract_section(result_str, "BUSINESS STRATEGY",     ["ACTION PLAN"])
    action_plan   = extract_section(result_str, "ACTION PLAN",           [])

    # Fallback: show full result if parsing didn't find sections
    if not any([exec_summary, market_data, strategy_data, action_plan]):
        exec_summary = result_str

    add_log("📊 Rendering structured report...", "sys")

    # ── Render Output ──
    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
    st.markdown("""
    <div class="pill-row">
        <span class="pill yellow">👑 Manager Orchestrated</span>
        <span class="pill green">🔬 Research Completed</span>
        <span class="pill blue">📈 Strategy Formulated</span>
        <span class="pill purple">📋 Report Ready</span>
    </div>
    """, unsafe_allow_html=True)

    # Executive Summary — full width
    if exec_summary:
        st.markdown(f"""
        <div class="output-panel full">
            <div class="panel-header mgr">
                <span class="panel-icon">👑</span>
                <span class="panel-title">Executive Summary — Manager Consolidated</span>
            </div>
            <div class="panel-body">{exec_summary}</div>
        </div>
        """, unsafe_allow_html=True)

    # Two-column: Research + Strategy
    col_a, col_b = st.columns(2)
    with col_a:
        st.markdown(f"""
        <div class="output-panel">
            <div class="panel-header res">
                <span class="panel-icon">🔬</span>
                <span class="panel-title">Market Research Findings</span>
            </div>
            <div class="panel-body">{market_data or "See full report below."}</div>
        </div>
        """, unsafe_allow_html=True)

    with col_b:
        st.markdown(f"""
        <div class="output-panel">
            <div class="panel-header str">
                <span class="panel-icon">📈</span>
                <span class="panel-title">Business Strategy</span>
            </div>
            <div class="panel-body">{strategy_data or "See full report below."}</div>
        </div>
        """, unsafe_allow_html=True)

    # Action Plan — full width
    if action_plan:
        st.markdown(f"""
        <div class="output-panel full" style="margin-top:1.2rem">
            <div class="panel-header fin">
                <span class="panel-icon">🎯</span>
                <span class="panel-title">90-Day Action Plan</span>
            </div>
            <div class="panel-body">{action_plan}</div>
        </div>
        """, unsafe_allow_html=True)

    # Full raw output expander
    with st.expander("📄 Full Raw Report"):
        st.text(result_str)

    # Download
    st.download_button(
        label="⬇️ Download Full Report (.txt)",
        data=result_str,
        file_name="agentflow_day3_report.txt",
        mime="text/plain",
    )

    add_log("🎉 Done! Report delivered.", "sys")
