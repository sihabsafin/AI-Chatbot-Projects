import streamlit as st
import os
import time

# ── Page config ────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="CrewAI · Multi-Agent Business Planner",
    page_icon="⬡",
    layout="centered",
    initial_sidebar_state="collapsed",
)

# ── CSS ────────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;600&family=IBM+Plex+Sans:wght@300;400;600&display=swap');

html, body, [class*="css"] {
    font-family: 'IBM Plex Sans', sans-serif;
    background-color: #0d0d0d;
    color: #e8e8e8;
}
#MainMenu, footer, header { visibility: hidden; }
.block-container { padding: 2.5rem 2rem 4rem 2rem; max-width: 820px; }

/* ── Header ── */
.app-header {
    border-bottom: 1px solid #1e1e1e;
    padding-bottom: 1.2rem;
    margin-bottom: 2rem;
}
.app-title {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 1.1rem;
    font-weight: 600;
    color: #00ff9d;
    letter-spacing: 0.05em;
    margin: 0 0 0.25rem 0;
}
.app-sub {
    font-size: 0.75rem;
    color: #444;
    font-family: 'IBM Plex Mono', monospace;
}
.day-badge {
    display: inline-block;
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.62rem;
    color: #0d0d0d;
    background: #00ff9d;
    border-radius: 2px;
    padding: 0.15rem 0.5rem;
    margin-right: 0.5rem;
    font-weight: 600;
    letter-spacing: 0.06em;
}

/* ── Agent flow diagram ── */
.flow-wrap {
    display: flex;
    align-items: center;
    gap: 0;
    margin: 1.6rem 0 1.8rem 0;
    justify-content: center;
}
.agent-chip {
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 0.3rem;
}
.agent-chip-box {
    background: #141414;
    border: 1px solid #2a2a2a;
    border-radius: 6px;
    padding: 0.55rem 1rem;
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.7rem;
    color: #aaa;
    text-align: center;
    min-width: 130px;
}
.agent-chip-box.active { border-color: #00ff9d44; color: #00ff9d; }
.agent-chip-label {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.58rem;
    color: #333;
    letter-spacing: 0.08em;
    text-transform: uppercase;
}
.flow-arrow {
    font-size: 0.85rem;
    color: #2a2a2a;
    padding: 0 0.6rem;
    padding-top: 0;
    margin-bottom: 1.1rem;
}
.flow-note {
    text-align: center;
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.62rem;
    color: #333;
    margin-top: -0.8rem;
    margin-bottom: 1.4rem;
    letter-spacing: 0.05em;
}

/* ── Field labels ── */
.field-label {
    font-size: 0.7rem;
    font-family: 'IBM Plex Mono', monospace;
    color: #555;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    margin-bottom: 0.35rem;
    display: block;
}

/* ── Inputs ── */
.stTextInput input, .stTextArea textarea {
    background: #141414 !important;
    border: 1px solid #242424 !important;
    border-radius: 4px !important;
    color: #e8e8e8 !important;
    font-family: 'IBM Plex Sans', sans-serif !important;
    font-size: 0.88rem !important;
}
.stTextInput input:focus, .stTextArea textarea:focus {
    border-color: #00ff9d !important;
    box-shadow: 0 0 0 1px #00ff9d18 !important;
}
.stSelectbox div[data-baseweb="select"] {
    background: #141414 !important;
    border: 1px solid #242424 !important;
    border-radius: 4px !important;
}
.stSelectbox div[data-baseweb="select"] > div {
    background: #141414 !important;
    color: #e8e8e8 !important;
    font-size: 0.88rem !important;
}

/* ── Button ── */
.stButton > button {
    background: #00ff9d !important;
    color: #0d0d0d !important;
    border: none !important;
    border-radius: 4px !important;
    font-family: 'IBM Plex Mono', monospace !important;
    font-size: 0.8rem !important;
    font-weight: 600 !important;
    letter-spacing: 0.08em !important;
    padding: 0.6rem 1.6rem !important;
    width: 100% !important;
    transition: opacity 0.15s !important;
}
.stButton > button:hover { opacity: 0.82 !important; }

/* ── Status ── */
.status-pill {
    display: inline-flex;
    align-items: center;
    gap: 0.5rem;
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.68rem;
    border-radius: 3px;
    padding: 0.25rem 0.7rem;
    margin-bottom: 0.8rem;
}
.status-pill.running {
    color: #f0b429;
    border: 1px solid #f0b42933;
    animation: blink 1.4s ease-in-out infinite;
}
.status-pill.done {
    color: #00ff9d;
    border: 1px solid #00ff9d33;
}
@keyframes blink { 0%,100%{opacity:1} 50%{opacity:0.35} }

/* ── Result panels ── */
.result-panel {
    background: #0f0f0f;
    border: 1px solid #1e1e1e;
    border-radius: 6px;
    padding: 1.2rem 1.5rem;
    margin-bottom: 1rem;
}
.result-panel-header {
    display: flex;
    align-items: center;
    gap: 0.6rem;
    margin-bottom: 0.9rem;
    border-bottom: 1px solid #1a1a1a;
    padding-bottom: 0.7rem;
}
.panel-agent-tag {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.62rem;
    font-weight: 600;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    padding: 0.15rem 0.5rem;
    border-radius: 2px;
}
.tag-researcher { background: #0a2a1e; color: #00ff9d; }
.tag-strategist { background: #1a1a0a; color: #f0b429; }
.panel-title {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.72rem;
    color: #555;
}
.result-content {
    font-size: 0.87rem;
    line-height: 1.8;
    color: #ccc;
    white-space: pre-wrap;
    font-family: 'IBM Plex Sans', sans-serif;
}

/* ── Stats row ── */
.stats-row {
    display: flex;
    gap: 1rem;
    margin-bottom: 1.2rem;
}
.stat-chip {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.62rem;
    color: #444;
    border: 1px solid #1e1e1e;
    border-radius: 3px;
    padding: 0.2rem 0.6rem;
}
.stat-chip span { color: #00ff9d; }

/* ── Error ── */
.error-box {
    background: #130808;
    border: 1px solid #ff444433;
    border-left: 3px solid #ff4444;
    border-radius: 4px;
    padding: 0.9rem 1.2rem;
    font-size: 0.8rem;
    font-family: 'IBM Plex Mono', monospace;
    color: #ff8888;
}

/* ── Divider ── */
.thin-divider { border: none; border-top: 1px solid #161616; margin: 1.6rem 0; }

/* ── Expander ── */
.stExpander { border: 1px solid #1a1a1a !important; border-radius: 4px !important; }
details summary { color: #555 !important; font-size: 0.82rem !important; }
</style>
""", unsafe_allow_html=True)


# ── Secrets ────────────────────────────────────────────────────────────────────
try:
    os.environ["GROQ_API_KEY"] = st.secrets["GROQ_API_KEY"]
except Exception:
    pass
os.environ.setdefault("OPENAI_API_KEY", "dummy-not-used")


# ── Header ─────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="app-header">
    <p class="app-title">
        <span class="day-badge">DAY 2</span>⬡ MULTI-AGENT BUSINESS PLANNER
    </p>
    <p class="app-sub">Research Agent → Strategy Agent · Sequential Crew · Groq + LLaMA 3.3 70B</p>
</div>
""", unsafe_allow_html=True)


# ── Agent flow visualization ────────────────────────────────────────────────────
st.markdown("""
<div class="flow-wrap">
    <div class="agent-chip">
        <div class="agent-chip-box active">Market Research<br>Analyst</div>
        <div class="agent-chip-label">Agent 1</div>
    </div>
    <div class="flow-arrow">──▶</div>
    <div class="agent-chip">
        <div class="agent-chip-box active">Business Strategy<br>Consultant</div>
        <div class="agent-chip-label">Agent 2</div>
    </div>
</div>
<p class="flow-note">Sequential Process · Agent 2 receives Agent 1 output as context</p>
""", unsafe_allow_html=True)


# ── Presets ────────────────────────────────────────────────────────────────────
PRESETS = {
    "AI Fitness Coaching App": "An AI-powered personal fitness coaching app that creates adaptive workout and nutrition plans for busy professionals aged 25–45, using health data from wearables.",
    "AI SaaS for Lawyers": "An AI legal assistant SaaS that helps solo lawyers and small law firms automate contract review, case summarization, and client intake — reducing manual document work by 80%.",
    "AI Real Estate Analyzer": "An AI tool that helps property investors evaluate deals, predict rental yields, flag undervalued markets, and generate investment reports automatically.",
    "AI Dropshipping Research Tool": "An AI-powered product research tool for ecommerce dropshippers that identifies winning products, analyzes competition, and suggests pricing strategies on Shopify.",
    "Custom Idea": "",
}

MODELS = {
    "llama-3.3-70b-versatile (Recommended)": "groq/llama-3.3-70b-versatile",
    "llama-3.1-8b-instant (Fastest)": "groq/llama-3.1-8b-instant",
    "mixtral-8x7b-32768 (Balanced)": "groq/mixtral-8x7b-32768",
}

# ── Form ───────────────────────────────────────────────────────────────────────
col1, col2 = st.columns([3, 2])
with col1:
    st.markdown('<span class="field-label">Business Idea Preset</span>', unsafe_allow_html=True)
    preset_choice = st.selectbox("Preset", list(PRESETS.keys()), label_visibility="collapsed")
with col2:
    st.markdown('<span class="field-label">Groq Model</span>', unsafe_allow_html=True)
    model_choice = st.selectbox("Model", list(MODELS.keys()), label_visibility="collapsed")

st.markdown('<span class="field-label">Business Idea Description</span>', unsafe_allow_html=True)
business_idea = st.text_area(
    "idea",
    value=PRESETS[preset_choice],
    height=90,
    placeholder="Describe the business idea in detail...",
    label_visibility="collapsed",
)

# ── Advanced customization ─────────────────────────────────────────────────────
with st.expander("⚙  Customize Agents & Output (optional)"):
    st.markdown('<span class="field-label">Researcher — Backstory</span>', unsafe_allow_html=True)
    researcher_backstory = st.text_area(
        "rb", height=75, label_visibility="collapsed",
        value="You are a Senior Market Research Analyst with 10+ years of experience across tech, SaaS, and consumer markets. You've advised 100+ startups. You produce concise, data-backed market analyses.",
    )

    st.markdown('<span class="field-label">Strategist — Backstory</span>', unsafe_allow_html=True)
    strategist_backstory = st.text_area(
        "sb", height=75, label_visibility="collapsed",
        value="You are a startup strategy consultant who has helped 80+ companies build scalable business models. You translate market research into actionable monetization and growth plans with clear prioritization.",
    )

    st.markdown('<span class="field-label">Strategy Output Sections (one per line)</span>', unsafe_allow_html=True)
    default_strategy_sections = (
        "1. Target Audience\n"
        "2. Pricing Model\n"
        "3. Revenue Streams\n"
        "4. Marketing Strategy\n"
        "5. Risks & Mitigations"
    )
    strategy_sections = st.text_area(
        "ss", value=default_strategy_sections, height=120, label_visibility="collapsed"
    )

st.markdown('<hr class="thin-divider">', unsafe_allow_html=True)
run_btn = st.button("▶  RUN MULTI-AGENT CREW")


# ── Execution ──────────────────────────────────────────────────────────────────
if run_btn:
    if not business_idea.strip():
        st.markdown('<div class="error-box">⚠ Please enter a business idea description.</div>', unsafe_allow_html=True)
        st.stop()

    try:
        from crewai import Agent, Task, Crew, Process, LLM
    except ImportError:
        st.markdown('<div class="error-box">crewai not installed. Add it to requirements.txt</div>', unsafe_allow_html=True)
        st.stop()

    groq_api_key = os.environ.get("GROQ_API_KEY", "")
    if not groq_api_key:
        st.markdown('<div class="error-box">⚠ GROQ_API_KEY not found. Set it in Streamlit → Settings → Secrets.</div>', unsafe_allow_html=True)
        st.stop()

    model_id = MODELS[model_choice]
    rb = researcher_backstory.strip()
    sb = strategist_backstory.strip()
    ss = strategy_sections.strip() or default_strategy_sections

    status_box = st.empty()
    output_box = st.empty()

    status_box.markdown('<div class="status-pill running">● CREW RUNNING — 2 agents working sequentially…</div>', unsafe_allow_html=True)

    t_start = time.time()

    try:
        llm = LLM(
            model=model_id,
            api_key=groq_api_key,
            temperature=0.7,
        )

        # ── Agent 1: Researcher ────────────────────────────────────────────────
        researcher = Agent(
            role="Market Research Analyst",
            goal=(
                "Research the market size, target audience, top competitors, "
                "and demand signals for the given business idea. "
                "Identify 3 clear market opportunities."
            ),
            backstory=rb,
            llm=llm,
            verbose=False,
        )

        # ── Agent 2: Strategist ────────────────────────────────────────────────
        strategist = Agent(
            role="Business Strategy Consultant",
            goal=(
                "Using the market research findings, create a concrete, "
                "actionable business strategy with monetization plan and growth tactics."
            ),
            backstory=sb,
            llm=llm,
            verbose=False,
        )

        # ── Task 1 ─────────────────────────────────────────────────────────────
        research_task = Task(
            description=(
                f"Conduct thorough market research for this business idea:\n\n"
                f"'{business_idea}'\n\n"
                f"Cover: market size & growth rate, ideal customer profile, "
                f"top 3 competitors with their weaknesses, and 3 market opportunities."
            ),
            expected_output=(
                "A structured market research report with:\n"
                "1. Market Overview (size, growth, trends)\n"
                "2. Ideal Customer Profile\n"
                "3. Competitor Analysis (top 3 with weaknesses)\n"
                "4. Market Opportunities (3 specific gaps)"
            ),
            agent=researcher,
        )

        # ── Task 2 — context flows from Task 1 automatically ──────────────────
        strategy_task = Task(
            description=(
                f"Based on the market research findings above, create a complete "
                f"business strategy for:\n\n'{business_idea}'\n\n"
                f"Format your output strictly using these sections:\n{ss}"
            ),
            expected_output=(
                f"A structured business strategy report with these sections:\n{ss}"
            ),
            agent=strategist,
            context=[research_task],   # explicit context passing
        )

        # ── Crew: Sequential ───────────────────────────────────────────────────
        crew = Crew(
            agents=[researcher, strategist],
            tasks=[research_task, strategy_task],
            process=Process.sequential,
            verbose=False,
        )

        result = crew.kickoff()
        elapsed = round(time.time() - t_start, 1)

        # Extract individual task outputs
        research_out = ""
        strategy_out = ""
        try:
            research_out = str(research_task.output.raw) if research_task.output else ""
            strategy_out = str(strategy_task.output.raw) if strategy_task.output else ""
        except Exception:
            strategy_out = str(result)

        status_box.markdown(
            f'<div class="status-pill done">✓ CREW COMPLETE</div>'
            f'<div class="stats-row">'
            f'  <div class="stat-chip">time <span>{elapsed}s</span></div>'
            f'  <div class="stat-chip">agents <span>2</span></div>'
            f'  <div class="stat-chip">tasks <span>2</span></div>'
            f'  <div class="stat-chip">model <span>{model_id.split("/")[1]}</span></div>'
            f'</div>',
            unsafe_allow_html=True,
        )

        # ── Render: Research panel ─────────────────────────────────────────────
        if research_out:
            st.markdown(f"""
            <div class="result-panel">
                <div class="result-panel-header">
                    <span class="panel-agent-tag tag-researcher">Agent 1 · Researcher</span>
                    <span class="panel-title">Market Research Report</span>
                </div>
                <div class="result-content">{research_out}</div>
            </div>
            """, unsafe_allow_html=True)

        # ── Render: Strategy panel ─────────────────────────────────────────────
        if strategy_out:
            st.markdown(f"""
            <div class="result-panel">
                <div class="result-panel-header">
                    <span class="panel-agent-tag tag-strategist">Agent 2 · Strategist</span>
                    <span class="panel-title">Business Strategy Plan</span>
                </div>
                <div class="result-content">{strategy_out}</div>
            </div>
            """, unsafe_allow_html=True)

        # Fallback if task outputs weren't captured separately
        if not research_out and not strategy_out:
            st.markdown(f"""
            <div class="result-panel">
                <div class="result-panel-header">
                    <span class="panel-agent-tag tag-strategist">Crew Output</span>
                </div>
                <div class="result-content">{str(result)}</div>
            </div>
            """, unsafe_allow_html=True)

    except Exception as e:
        status_box.empty()
        st.markdown(f'<div class="error-box">✗ Error: {str(e)}</div>', unsafe_allow_html=True)
