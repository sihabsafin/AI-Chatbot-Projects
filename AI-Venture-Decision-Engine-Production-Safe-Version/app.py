import streamlit as st
import os
import time
import json
import re

st.set_page_config(
    page_title="AgentForge · Resilient Analyzer",
    page_icon="⬡",
    layout="centered",
    initial_sidebar_state="collapsed",
)

# ── Secrets ─────────────────────────────────────────────────────────────────────
for secret_key in ["GEMINI_API_KEY", "GROQ_API_KEY"]:
    try:
        os.environ[secret_key] = st.secrets[secret_key]
    except Exception:
        pass
os.environ.setdefault("OPENAI_API_KEY", "dummy-not-used")

# ── CSS ─────────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=IBM+Plex+Sans:wght@300;400;500;600&family=IBM+Plex+Mono:wght@300;400;500&display=swap');

:root {
    --bg:           #050810;
    --surface:      #090d18;
    --surface2:     #0d1220;
    --surface3:     #111828;
    --border:       #1a2236;
    --border2:      #1e2a40;
    --text:         #dce8f5;
    --muted:        #4a6080;
    --muted2:       #6a80a0;
    --accent:       #2979ff;
    --accent-dim:   #0a1a40;
    --green:        #00e676;
    --green-dim:    #002818;
    --amber:        #ffab40;
    --amber-dim:    #281800;
    --red:          #ff5252;
    --red-dim:      #280808;
    --cyan:         #18ffff;
    --cyan-dim:     #001820;
    --purple:       #e040fb;
    --purple-dim:   #1a0828;
    --sans:         'IBM Plex Sans', sans-serif;
    --mono:         'IBM Plex Mono', monospace;
    --glow-g:       0 0 12px rgba(0,230,118,0.3);
    --glow-r:       0 0 12px rgba(255,82,82,0.3);
    --glow-a:       0 0 12px rgba(255,171,64,0.3);
    --glow-b:       0 0 12px rgba(41,121,255,0.3);
}

* { box-sizing: border-box; }
html, body, [class*="css"] {
    font-family: var(--sans);
    background: var(--bg);
    color: var(--text);
}
#MainMenu, footer, header { visibility: hidden; }
.block-container { padding: 1.8rem 1.6rem 5rem; max-width: 920px; }

/* ── Scanline overlay ── */
body::before {
    content: '';
    position: fixed; top:0; left:0; right:0; bottom:0;
    background: repeating-linear-gradient(
        0deg, transparent, transparent 2px,
        rgba(0,0,0,0.03) 2px, rgba(0,0,0,0.03) 4px
    );
    pointer-events: none;
    z-index: 9999;
}

/* ── Header ── */
.hdr {
    display: flex; align-items: flex-start; justify-content: space-between;
    padding-bottom: 1.2rem;
    border-bottom: 1px solid var(--border);
    margin-bottom: 1.6rem;
}
.hdr-left {}
.hdr-title {
    font-family: var(--mono);
    font-size: 0.72rem; font-weight: 500;
    color: var(--muted2); letter-spacing: 0.14em;
    text-transform: uppercase; margin-bottom: 0.3rem;
}
.hdr-name {
    font-family: var(--sans);
    font-size: 1.5rem; font-weight: 600;
    color: var(--text); letter-spacing: -0.02em;
    line-height: 1.1;
}
.hdr-sub {
    font-family: var(--mono);
    font-size: 0.6rem; color: var(--muted);
    letter-spacing: 0.1em; margin-top: 0.3rem;
}
.hdr-right { display: flex; flex-direction: column; align-items: flex-end; gap: 0.4rem; }
.hdr-pill {
    font-family: var(--mono); font-size: 0.58rem; font-weight: 500;
    padding: 0.2rem 0.65rem; border-radius: 2px;
    letter-spacing: 0.08em; text-transform: uppercase;
}
.pill-day    { background: var(--accent-dim); color: var(--accent); border: 1px solid #1a2a50; }
.pill-prod   { background: var(--green-dim); color: var(--green); border: 1px solid #004020;
               box-shadow: var(--glow-g); }

/* ── System health bar ── */
.health-bar {
    display: grid;
    grid-template-columns: repeat(5, 1fr);
    gap: 0.5rem;
    margin-bottom: 1.4rem;
}
.health-cell {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 4px;
    padding: 0.6rem 0.8rem;
    position: relative;
    overflow: hidden;
}
.health-cell::before {
    content: '';
    position: absolute; bottom: 0; left: 0; right: 0; height: 2px;
}
.hc-ok::before    { background: var(--green); box-shadow: var(--glow-g); }
.hc-warn::before  { background: var(--amber); box-shadow: var(--glow-a); }
.hc-err::before   { background: var(--red); box-shadow: var(--glow-r); }
.hc-info::before  { background: var(--accent); box-shadow: var(--glow-b); }
.hc-label { font-family: var(--mono); font-size: 0.52rem; color: var(--muted); letter-spacing: 0.1em; text-transform: uppercase; margin-bottom: 0.2rem; }
.hc-value { font-family: var(--mono); font-size: 0.75rem; font-weight: 500; }
.hcv-ok   { color: var(--green); }
.hcv-warn { color: var(--amber); }
.hcv-err  { color: var(--red); }
.hcv-info { color: var(--accent); }

/* ── Section label ── */
.slabel {
    font-family: var(--mono); font-size: 0.58rem; color: var(--muted);
    letter-spacing: 0.12em; text-transform: uppercase;
    margin-bottom: 0.35rem; display: block;
}

/* ── Reliability config panel ── */
.config-grid {
    display: grid; grid-template-columns: 1fr 1fr 1fr;
    gap: 0.7rem; margin-bottom: 1.2rem;
}
.config-card {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 6px;
    padding: 0.9rem 1rem;
}
.config-card-label {
    font-family: var(--mono); font-size: 0.55rem; color: var(--muted);
    letter-spacing: 0.1em; text-transform: uppercase; margin-bottom: 0.35rem;
}
.config-card-value {
    font-family: var(--mono); font-size: 0.92rem; font-weight: 500;
    color: var(--cyan);
}
.config-card-sub {
    font-family: var(--mono); font-size: 0.58rem; color: var(--muted);
    margin-top: 0.2rem;
}

/* ── Inputs ── */
.stTextInput input, .stTextArea textarea {
    background: var(--surface) !important;
    border: 1px solid var(--border2) !important;
    border-radius: 5px !important;
    color: var(--text) !important;
    font-family: var(--sans) !important;
    font-size: 0.87rem !important;
    caret-color: var(--accent) !important;
}
.stTextInput input:focus, .stTextArea textarea:focus {
    border-color: var(--accent) !important;
    box-shadow: 0 0 0 2px rgba(41,121,255,0.12) !important;
    background: var(--surface2) !important;
}
.stSelectbox div[data-baseweb="select"] {
    background: var(--surface) !important;
    border: 1px solid var(--border2) !important;
    border-radius: 5px !important;
}
.stSelectbox div[data-baseweb="select"] > div {
    background: var(--surface) !important;
    color: var(--text) !important;
    font-family: var(--sans) !important;
    font-size: 0.87rem !important;
}
.stSlider [data-baseweb="slider"] { padding: 0.2rem 0 !important; }
.stNumberInput input {
    background: var(--surface) !important;
    border: 1px solid var(--border2) !important;
    border-radius: 5px !important;
    color: var(--text) !important;
    font-family: var(--mono) !important;
    font-size: 0.87rem !important;
}
.stCheckbox label { color: var(--muted2) !important; font-size: 0.82rem !important; }
.stToggle label { color: var(--muted2) !important; font-size: 0.82rem !important; }

/* ── Buttons ── */
.stButton > button {
    background: var(--accent) !important;
    color: white !important; border: none !important;
    border-radius: 5px !important;
    font-family: var(--mono) !important;
    font-size: 0.75rem !important; font-weight: 500 !important;
    letter-spacing: 0.08em !important;
    padding: 0.65rem 1.5rem !important;
    width: 100% !important;
    transition: all 0.15s !important;
    box-shadow: var(--glow-b) !important;
}
.stButton > button:hover {
    background: #1a5ce0 !important;
    box-shadow: 0 0 20px rgba(41,121,255,0.5) !important;
    transform: translateY(-1px) !important;
}

/* ── Expander ── */
.stExpander { background: var(--surface) !important; border: 1px solid var(--border) !important; border-radius: 5px !important; }
details summary { color: var(--muted2) !important; font-size: 0.8rem !important; font-family: var(--sans) !important; }

/* ── Divider ── */
.div { border: none; border-top: 1px solid var(--border); margin: 1.2rem 0; }

/* ── Mission log ── */
.mission-log {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 7px;
    overflow: hidden;
    margin-bottom: 1rem;
    font-family: var(--mono);
}
.ml-head {
    display: flex; align-items: center; gap: 0.6rem;
    padding: 0.55rem 1rem;
    background: var(--surface2);
    border-bottom: 1px solid var(--border);
}
.ml-dot { width:6px; height:6px; border-radius:50%; }
.ml-head-title { font-size: 0.58rem; color: var(--muted); letter-spacing: 0.12em; text-transform: uppercase; }
.ml-live { font-size: 0.55rem; color: var(--green); margin-left: auto; animation: blink 2s ease-in-out infinite; }
.ml-body { padding: 0.7rem 1rem; display: flex; flex-direction: column; gap: 0.35rem; max-height: 300px; overflow-y: auto; }
.ml-line { display: flex; align-items: flex-start; gap: 0.65rem; font-size: 0.67rem; line-height: 1.5; }
.ml-t { color: var(--muted); min-width: 48px; flex-shrink: 0; }
.ml-tag {
    font-size: 0.54rem; font-weight: 500;
    padding: 0.1rem 0.4rem; border-radius: 2px;
    white-space: nowrap; margin-top: 0.15rem;
    flex-shrink: 0; letter-spacing: 0.04em;
}
.lt-sys   { background: var(--surface3); color: var(--muted2); }
.lt-ok    { background: var(--green-dim); color: var(--green); }
.lt-retry { background: var(--amber-dim); color: var(--amber); }
.lt-err   { background: var(--red-dim); color: var(--red); }
.lt-json  { background: var(--cyan-dim); color: var(--cyan); }
.lt-val   { background: var(--purple-dim); color: var(--purple); }
.lt-cost  { background: #0a1228; color: #6a9fdf; }
.ml-msg { color: var(--text); }

@keyframes blink { 0%,100%{opacity:1} 50%{opacity:0.3} }

/* ── Status bar ── */
.status-bar {
    display: flex; align-items: center; gap: 0.8rem;
    padding: 0.65rem 1rem;
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 6px;
    margin-bottom: 1rem;
    font-family: var(--mono);
}
.s-dot { width:7px; height:7px; border-radius:50%; flex-shrink:0; }
.s-run  { background: var(--amber); animation: blink 1.2s ease-in-out infinite; box-shadow: var(--glow-a); }
.s-ok   { background: var(--green); box-shadow: var(--glow-g); }
.s-err  { background: var(--red); box-shadow: var(--glow-r); }
.s-warn { background: var(--amber); box-shadow: var(--glow-a); }
.s-text { font-size: 0.72rem; color: var(--text); flex: 1; }
.s-meta { font-size: 0.62rem; color: var(--muted); }

/* ── Retry attempt cards ── */
.retry-track {
    display: flex; gap: 0.5rem; margin-bottom: 1rem; flex-wrap: wrap;
}
.retry-card {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 5px;
    padding: 0.5rem 0.8rem;
    font-family: var(--mono); font-size: 0.65rem;
    display: flex; flex-direction: column; gap: 0.15rem;
    min-width: 80px;
}
.rc-attempt { color: var(--muted2); font-size: 0.55rem; letter-spacing: 0.08em; text-transform: uppercase; }
.rc-status  { font-size: 0.68rem; font-weight: 500; }
.rcs-pass { color: var(--green); }
.rcs-fail { color: var(--red); }
.rcs-skip { color: var(--muted); }
.rc-time { color: var(--muted); font-size: 0.6rem; }

/* ── Decision banner ── */
.decision-banner {
    border-radius: 8px;
    padding: 1.2rem 1.4rem;
    margin-bottom: 1.1rem;
    display: flex; align-items: center; justify-content: space-between;
    flex-wrap: wrap; gap: 1rem;
    font-family: var(--mono);
}
.db-invest  { background: var(--green-dim); border: 1px solid #004a28; box-shadow: var(--glow-g); }
.db-consider{ background: var(--amber-dim); border: 1px solid #4a2800; box-shadow: var(--glow-a); }
.db-reject  { background: var(--red-dim);   border: 1px solid #4a1010; box-shadow: var(--glow-r); }
.db-lbl { font-size: 0.55rem; color: var(--muted2); letter-spacing: 0.12em; text-transform: uppercase; margin-bottom: 0.3rem; }
.db-dec { font-family: var(--sans); font-size: 1.6rem; font-weight: 600; letter-spacing: -0.02em; line-height: 1; }
.db-invest .db-dec  { color: var(--green); }
.db-consider .db-dec{ color: var(--amber); }
.db-reject .db-dec  { color: var(--red); }
.db-right { display: flex; flex-direction: column; align-items: flex-end; gap: 0.4rem; }
.db-conf {
    font-family: var(--mono); font-size: 0.65rem; font-weight: 500;
    padding: 0.25rem 0.7rem; border-radius: 3px;
}
.conf-h { background: var(--green-dim); color: var(--green); border: 1px solid #004020; }
.conf-m { background: var(--amber-dim); color: var(--amber); border: 1px solid #4a2800; }
.conf-l { background: var(--red-dim);   color: var(--red);   border: 1px solid #4a1010; }
.db-idea { font-family: var(--sans); font-size: 0.72rem; color: var(--muted2); max-width: 240px; text-align: right; line-height: 1.4; }

/* ── Score grid ── */
.score-grid { display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 0.7rem; margin-bottom: 1.1rem; }
.score-card {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 7px;
    padding: 0.9rem 1rem;
    position: relative; overflow: hidden;
}
.score-card::after {
    content: ''; position: absolute;
    bottom: 0; left: 0; right: 0; height: 2px;
}
.sc-m::after { background: var(--accent); box-shadow: var(--glow-b); }
.sc-f::after { background: var(--green);  box-shadow: var(--glow-g); }
.sc-r::after { background: var(--red);    box-shadow: var(--glow-r); }
.sc-label { font-family: var(--mono); font-size: 0.55rem; color: var(--muted); letter-spacing: 0.1em; text-transform: uppercase; margin-bottom: 0.4rem; }
.sc-val { font-family: var(--mono); font-size: 2rem; font-weight: 500; line-height: 1; margin-bottom: 0.4rem; }
.scv-m { color: var(--accent); }
.scv-f { color: var(--green); }
.scv-r { color: var(--red); }
.sc-bar-wrap { height: 3px; background: var(--surface3); border-radius: 2px; margin-bottom: 0.45rem; overflow: hidden; }
.sc-bar { height: 100%; border-radius: 2px; }
.scb-m { background: var(--accent); }
.scb-f { background: var(--green); }
.scb-r { background: var(--red); }
.sc-sum { font-family: var(--sans); font-size: 0.72rem; color: var(--muted2); line-height: 1.5; }

/* ── Validation panel ── */
.val-panel {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 7px; overflow: hidden;
    margin-bottom: 1.1rem;
}
.val-head {
    display: flex; align-items: center; justify-content: space-between;
    padding: 0.6rem 1rem;
    background: var(--surface2);
    border-bottom: 1px solid var(--border);
}
.val-title { font-family: var(--mono); font-size: 0.58rem; color: var(--muted); letter-spacing: 0.12em; text-transform: uppercase; }
.vstat-ok   { font-family: var(--mono); font-size: 0.6rem; color: var(--green); background: var(--green-dim); padding: 0.15rem 0.5rem; border-radius: 2px; }
.vstat-fail { font-family: var(--mono); font-size: 0.6rem; color: var(--red);   background: var(--red-dim);   padding: 0.15rem 0.5rem; border-radius: 2px; }
.val-body { padding: 0.7rem 1rem; display: flex; flex-direction: column; gap: 0.35rem; }
.val-row { display: flex; align-items: center; gap: 0.6rem; font-family: var(--mono); font-size: 0.67rem; }
.vi-ok   { color: var(--green); }
.vi-fail { color: var(--red); }
.vi-warn { color: var(--amber); }
.vk { color: var(--muted2); min-width: 140px; }
.vm { color: var(--text); }

/* ── Actions ── */
.actions-panel {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 7px; overflow: hidden;
    margin-bottom: 1.1rem;
}
.actions-head {
    padding: 0.6rem 1rem;
    background: var(--surface2);
    border-bottom: 1px solid var(--border);
    font-family: var(--mono); font-size: 0.58rem; color: var(--muted); letter-spacing: 0.12em; text-transform: uppercase;
}
.actions-body { padding: 0.8rem 1rem; display: flex; flex-direction: column; gap: 0.5rem; }
.action-item { display: flex; align-items: flex-start; gap: 0.6rem; }
.a-num {
    font-family: var(--mono); font-size: 0.6rem; font-weight: 500;
    color: var(--accent); background: var(--accent-dim);
    padding: 0.05rem 0.4rem; border-radius: 2px;
    min-width: 24px; text-align: center; margin-top: 2px; flex-shrink: 0;
}
.a-txt { font-family: var(--sans); font-size: 0.82rem; color: var(--text); line-height: 1.5; }

/* ── Cost panel ── */
.cost-panel {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 7px; overflow: hidden;
    margin-bottom: 1.1rem;
}
.cost-head {
    display: flex; align-items: center; justify-content: space-between;
    padding: 0.6rem 1rem;
    background: var(--surface2);
    border-bottom: 1px solid var(--border);
}
.cost-title { font-family: var(--mono); font-size: 0.58rem; color: var(--muted); letter-spacing: 0.12em; text-transform: uppercase; }
.cost-body { display: grid; grid-template-columns: repeat(4, 1fr); padding: 0.8rem 0; }
.cost-cell {
    padding: 0.5rem 1rem;
    border-right: 1px solid var(--border);
}
.cost-cell:last-child { border-right: none; }
.cost-cell-label { font-family: var(--mono); font-size: 0.55rem; color: var(--muted); letter-spacing: 0.08em; text-transform: uppercase; margin-bottom: 0.25rem; }
.cost-cell-val { font-family: var(--mono); font-size: 0.85rem; font-weight: 500; color: var(--cyan); }
.cost-cell-sub { font-family: var(--mono); font-size: 0.6rem; color: var(--muted2); margin-top: 0.15rem; }
.cost-tip {
    padding: 0.5rem 1rem;
    border-top: 1px solid var(--border);
    font-family: var(--mono); font-size: 0.62rem; color: var(--muted2);
    background: var(--bg);
}

/* ── JSON panel ── */
.json-panel {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 7px; overflow: hidden;
    margin-bottom: 1.1rem;
}
.json-head {
    display: flex; align-items: center; justify-content: space-between;
    padding: 0.6rem 1rem;
    background: var(--surface2);
    border-bottom: 1px solid var(--border);
}
.json-title { font-family: var(--mono); font-size: 0.58rem; color: var(--muted); letter-spacing: 0.12em; text-transform: uppercase; }
.json-body {
    padding: 1rem 1.2rem;
    font-family: var(--mono); font-size: 0.7rem; line-height: 1.9;
    color: #8090a8; white-space: pre-wrap; word-break: break-word;
}
.jk { color: #6a9fd8; }
.jvn { color: var(--amber); }
.jvs { color: var(--green); }
.jva { color: #c080e0; }

/* ── Stats ── */
.stats-row { display: flex; flex-wrap: wrap; gap: 0.5rem; margin: 0.8rem 0 1.2rem; }
.stat { font-family: var(--mono); font-size: 0.59rem; color: var(--muted); background: var(--surface); border: 1px solid var(--border); border-radius: 3px; padding: 0.2rem 0.6rem; }
.stat b { color: var(--accent); }

/* ── Error box ── */
.err-box {
    background: var(--red-dim); border: 1px solid #4a1010; border-left: 3px solid var(--red);
    border-radius: 6px; padding: 0.9rem 1.2rem;
    font-family: var(--mono); font-size: 0.7rem; color: #e09090; line-height: 1.6;
}

/* ── Test panel (intentional failure) ── */
.test-panel {
    background: var(--surface);
    border: 1px solid var(--amber-dim);
    border-left: 3px solid var(--amber);
    border-radius: 6px;
    padding: 0.9rem 1.1rem;
    margin-bottom: 1rem;
}
.test-panel-title { font-family: var(--mono); font-size: 0.6rem; color: var(--amber); letter-spacing: 0.1em; text-transform: uppercase; margin-bottom: 0.5rem; }
.test-panel-body { font-family: var(--sans); font-size: 0.8rem; color: var(--muted2); line-height: 1.6; }
</style>
""", unsafe_allow_html=True)


# ── Core reliability functions ──────────────────────────────────────────────────

def validate_input(text: str, min_len: int = 30) -> tuple[bool, str]:
    """Input validation before agents run. Returns (is_valid, reason)."""
    if not text or not text.strip():
        return False, "Input is empty"
    if len(text.strip()) < min_len:
        return False, f"Too short — minimum {min_len} characters, got {len(text.strip())}"
    if len(text.strip()) > 3000:
        return False, "Too long — maximum 3000 characters"
    if text.strip().lower() in ["test", "hello", "hi", "startup", "idea"]:
        return False, "Input too generic — describe the startup with market, pricing, and context"
    return True, "valid"


def extract_json_safe(text: str) -> dict:
    """Two-pass JSON extraction with fallback error dict."""
    try:
        # Pass 1: strip markdown, find JSON block
        cleaned = re.sub(r'```json\s*', '', text)
        cleaned = re.sub(r'```\s*', '', cleaned)
        match = re.search(r'\{.*\}', cleaned, re.DOTALL)
        if match:
            return json.loads(match.group())
    except (json.JSONDecodeError, Exception):
        pass
    try:
        # Pass 2: fix common LLM JSON issues
        if match:
            fixed = re.sub(r',\s*}', '}', match.group())
            fixed = re.sub(r',\s*]', ']', fixed)
            fixed = re.sub(r'(?<!")(\b\w+\b)(?=\s*:)', r'"\1"', fixed)
            return json.loads(fixed)
    except Exception:
        pass
    return {"error": "JSON extraction failed after two passes", "raw_preview": text[:300]}


def validate_output(data: dict) -> list:
    """Full validation pipeline. Returns list of (icon, key, message, passed)."""
    results = []
    if "error" in data:
        results.append(("✗", "json_extraction", data["error"], False))
        return results

    required = ["market_score", "financial_score", "risk_score",
                "final_decision", "confidence_level", "recommended_actions",
                "market_summary", "financial_summary", "risk_summary"]

    for key in required:
        if key in data:
            results.append(("✓", key, "present", True))
        else:
            results.append(("✗", key, "MISSING — required field not returned", False))

    for sk in ["market_score", "financial_score", "risk_score"]:
        if sk in data:
            v = data[sk]
            if isinstance(v, (int, float)) and 0 <= float(v) <= 10:
                results.append(("✓", f"{sk} range", f"valid: {v}/10", True))
            else:
                results.append(("✗", f"{sk} range", f"OUT OF RANGE: {v} (must be 0–10)", False))

    # Business logic: risk > 8 → cannot be Invest
    if "risk_score" in data and "final_decision" in data:
        rs = float(data.get("risk_score", 0))
        fd = str(data.get("final_decision", "")).strip().lower()
        if rs > 8 and fd == "invest":
            results.append(("✗", "risk/decision logic", f"CONFLICT — risk {rs} > 8 but decision is 'Invest'", False))
        elif rs > 8:
            results.append(("✓", "risk/decision logic", f"consistent — high risk ({rs}) correctly avoided 'Invest'", True))
        else:
            results.append(("✓", "risk/decision logic", "passed — no conflict", True))

    if "recommended_actions" in data:
        ra = data["recommended_actions"]
        if isinstance(ra, list) and len(ra) >= 3:
            results.append(("✓", "recommended_actions", f"{len(ra)} actions returned", True))
        elif isinstance(ra, list):
            results.append(("⚠", "recommended_actions", f"only {len(ra)} actions — expected 5", len(ra) >= 1))
        else:
            results.append(("✗", "recommended_actions", "not a list", False))

    return results


def safe_kickoff(crew, retries: int, delay: float, log_lines: list, log_ph, ts_fn) -> tuple:
    """
    Retry-wrapped crew execution.
    Returns (result, attempts_used, success).
    Each attempt is logged live.
    """
    last_error = None
    for attempt in range(1, retries + 1):
        try:
            log_lines.append((ts_fn(), "RETRY" if attempt > 1 else "SYS",
                               "lt-retry" if attempt > 1 else "lt-sys",
                               f"Attempt {attempt}/{retries} — executing crew…"))
            _render_log(log_lines, log_ph)
            result = crew.kickoff()
            log_lines.append((ts_fn(), "OK", "lt-ok",
                               f"Attempt {attempt} succeeded ✓"))
            _render_log(log_lines, log_ph)
            return result, attempt, True
        except Exception as e:
            last_error = str(e)
            short_err = last_error[:80] + "…" if len(last_error) > 80 else last_error
            log_lines.append((ts_fn(), "ERR", "lt-err",
                               f"Attempt {attempt} failed: {short_err}"))
            _render_log(log_lines, log_ph)
            if attempt < retries:
                log_lines.append((ts_fn(), "RETRY", "lt-retry",
                                   f"Waiting {delay}s before retry {attempt+1}…"))
                _render_log(log_lines, log_ph)
                time.sleep(delay)
    return last_error, retries, False


def _render_log(lines: list, ph):
    rows = ""
    for t, tag, cls, msg in lines:
        rows += (f'<div class="ml-line">'
                 f'<span class="ml-t">{t}</span>'
                 f'<span class="ml-tag {cls}">{tag}</span>'
                 f'<span class="ml-msg">{msg}</span></div>')
    ph.markdown(f"""
    <div class="mission-log">
        <div class="ml-head">
            <div class="ml-dot" style="background:var(--green);box-shadow:var(--glow-g)"></div>
            <span class="ml-head-title">Mission Log</span>
            <span class="ml-live">● LIVE</span>
        </div>
        <div class="ml-body">{rows}</div>
    </div>""", unsafe_allow_html=True)


def decision_cls(d): return "db-invest" if "invest" in d.lower() and "consider" not in d.lower() else ("db-consider" if "consider" in d.lower() else "db-reject")
def conf_cls(c): return "conf-h" if c.lower()=="high" else ("conf-m" if c.lower() in ["medium","med"] else "conf-l")
def render_json_colored(data):
    lines = ["{"]
    items = list(data.items())
    for i, (k, v) in enumerate(items):
        comma = "," if i < len(items)-1 else ""
        if isinstance(v, (int, float)):
            lines.append(f'  <span class="jk">"{k}"</span>: <span class="jvn">{v}</span>{comma}')
        elif isinstance(v, list):
            lines.append(f'  <span class="jk">"{k}"</span>: [')
            for j, item in enumerate(v):
                ic = "," if j < len(v)-1 else ""
                lines.append(f'    <span class="jva">"{item}"</span>{ic}')
            lines.append(f'  ]{comma}')
        else:
            lines.append(f'  <span class="jk">"{k}"</span>: <span class="jvs">"{v}"</span>{comma}')
    lines.append("}")
    return "\n".join(lines)


# ── Header ──────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="hdr">
    <div class="hdr-left">
        <div class="hdr-title">AgentForge · Day 9</div>
        <div class="hdr-name">Resilient Analyzer</div>
        <div class="hdr-sub">RETRY LOGIC · LAYERED VALIDATION · COST OPTIMIZATION · FALLBACK CHAINS</div>
    </div>
    <div class="hdr-right">
        <span class="hdr-pill pill-day">DAY 9</span>
        <span class="hdr-pill pill-prod">PRODUCTION READY</span>
    </div>
</div>
""", unsafe_allow_html=True)

# ── System health bar ──────────────────────────────────────────────────────────
gemini_key_present = bool(os.environ.get("GEMINI_API_KEY", "").strip())
groq_key_present   = bool(os.environ.get("GROQ_API_KEY", "").strip())
key_status    = ("ONLINE", "hcv-ok", "hc-ok") if gemini_key_present else ("NO KEY", "hcv-err", "hc-err")
groq_status   = ("STANDBY", "hcv-ok", "hc-ok") if groq_key_present else ("NO KEY", "hcv-warn", "hc-warn")

st.markdown(f"""
<div class="health-bar">
    <div class="health-cell {key_status[2]}">
        <div class="hc-label">Gemini API</div>
        <div class="hc-value {key_status[1]}">{key_status[0]}</div>
    </div>
    <div class="health-cell {groq_status[2]}">
        <div class="hc-label">Groq Fallback</div>
        <div class="hc-value {groq_status[1]}">{groq_status[0]}</div>
    </div>
    <div class="health-cell hc-info">
        <div class="hc-label">Retry Engine</div>
        <div class="hc-value hcv-info">ARMED</div>
    </div>
    <div class="health-cell hc-ok">
        <div class="hc-label">Validation</div>
        <div class="hc-value hcv-ok">ACTIVE</div>
    </div>
    <div class="health-cell hc-ok">
        <div class="hc-label">Cost Guard</div>
        <div class="hc-value hcv-ok">ACTIVE</div>
    </div>
</div>
""", unsafe_allow_html=True)

# ── Presets ────────────────────────────────────────────────────────────────────
PRESETS = {
    "AI Logistics Optimizer": (
        "An AI-powered logistics optimization SaaS for mid-size e-commerce companies shipping "
        "10,000–500,000 parcels/month. Uses ML to reduce last-mile costs by 15–25% through "
        "carrier optimization and delay prediction. Pricing: $2,000–$8,000/month. "
        "TAM: $75B growing at 14% CAGR. Moat: proprietary model trained on 50M+ shipments."
    ),
    "AI Legal Document Analyzer": (
        "An AI contract intelligence SaaS for solo lawyers and boutique firms billing $200–$500/hr. "
        "Scans contracts in 60 seconds, flags risky clauses, suggests redlines. "
        "Pricing: $149/month flat. TAM: $12B LegalTech at 26% CAGR. "
        "Key risk: liability if AI misses a critical clause in a high-value contract."
    ),
    "AI Crypto Trading Bot": (
        "A retail-facing AI crypto trading bot executing algorithmic trades based on technical signals "
        "and sentiment analysis. Subscription $99/month plus 0.5% performance fee. "
        "TAM: $2.3B crypto trading tools. Risks: regulatory uncertainty, user loss liability, "
        "extreme market volatility, and competition from established quant firms."
    ),
    "AI HR Screening Tool": (
        "An AI candidate screening SaaS for companies hiring 50–500 employees/year. "
        "Auto-screens resumes, scores candidates, schedules interviews. "
        "Pricing: $500/month per active posting. TAM: $28B recruitment tech. "
        "Key risks: AI hiring bias liability and tightening EU/US regulations on automated decisions."
    ),
    "Custom Startup Idea": "",
}

MODELS = {
    "Gemini (Recommended)": {
        "gemini/gemini-2.5-flash": "Gemini 2.5 Flash  ✓ Free tier",
        "gemini/gemini-2.0-flash": "Gemini 2.0 Flash",
    },
    "Groq (Fallback)": {
        "groq/llama-3.3-70b-versatile": "LLaMA 3.3 70B",
        "groq/mixtral-8x7b-32768":      "Mixtral 8x7B",
    },
}

# ── Form ───────────────────────────────────────────────────────────────────────
col1, col2, col3 = st.columns([3, 2, 2])
with col1:
    st.markdown('<span class="slabel">Startup Idea</span>', unsafe_allow_html=True)
    preset = st.selectbox("preset", list(PRESETS.keys()), label_visibility="collapsed")
with col2:
    st.markdown('<span class="slabel">Provider</span>', unsafe_allow_html=True)
    prov = st.selectbox("prov", list(MODELS.keys()), label_visibility="collapsed")
with col3:
    st.markdown('<span class="slabel">Model</span>', unsafe_allow_html=True)
    model_opts = MODELS[prov]
    model_id = st.selectbox("mod", list(model_opts.keys()),
                             format_func=lambda x: model_opts[x], label_visibility="collapsed")

is_gemini = model_id.startswith("gemini/")

st.markdown('<span class="slabel">Startup Description</span>', unsafe_allow_html=True)
startup_idea = st.text_area("idea", value=PRESETS[preset], height=100,
    placeholder="Describe the startup with market size, pricing model, competitive moat, and key risks...",
    label_visibility="collapsed")

# ── Reliability config ─────────────────────────────────────────────────────────
st.markdown('<div class="div"></div>', unsafe_allow_html=True)
st.markdown('<span class="slabel">Reliability Configuration</span>', unsafe_allow_html=True)

col_r1, col_r2, col_r3, col_r4 = st.columns(4)
with col_r1:
    max_retries = st.number_input("Max Retries", min_value=1, max_value=5, value=3,
                                   help="How many times to retry on failure")
with col_r2:
    retry_delay = st.number_input("Retry Delay (s)", min_value=1.0, max_value=10.0, value=2.0, step=0.5,
                                   help="Seconds to wait between retry attempts")
with col_r3:
    min_input_len = st.number_input("Min Input Length", min_value=10, max_value=100, value=30,
                                     help="Minimum characters required in startup description")
with col_r4:
    regen_on_fail = st.checkbox("Auto-Regenerate on Invalid JSON", value=True,
                                 help="If JSON validation fails, automatically retry once")

with st.expander("⚙  Advanced — Analyst + Cost Settings"):
    col_a1, col_a2 = st.columns(2)
    with col_a1:
        analyst_persona = st.selectbox("Analyst Persona",
            ["Venture Capital Partner", "Angel Investor",
             "Private Equity Analyst", "Startup Accelerator"])
        investment_stage = st.selectbox("Investment Stage",
            ["Pre-seed", "Seed", "Series A", "Series B+"])
    with col_a2:
        risk_tolerance = st.selectbox("Risk Tolerance",
            ["Conservative", "Balanced", "Aggressive"])
        temperature = st.slider("LLM Temperature", 0.0, 1.0, 0.2, 0.1,
                                  help="Lower = more consistent JSON output. 0.1–0.3 recommended for structured output.")

    st.markdown("---")
    st.markdown("**Cost Optimization Settings**")
    col_c1, col_c2 = st.columns(2)
    with col_c1:
        concise_mode = st.checkbox("Concise Agent Backstory", value=True,
                                    help="Shorter backstory = fewer tokens = lower cost")
    with col_c2:
        verbose_off  = st.checkbox("Verbose=False (Production Mode)", value=True,
                                    help="Disables CrewAI internal logging — reduces token waste")

# ── Intentional failure test mode ─────────────────────────────────────────────
st.markdown('<div class="div"></div>', unsafe_allow_html=True)
test_mode = st.toggle("🔬  Test Mode — simulate failure scenarios to demonstrate retry system", value=False)

if test_mode:
    test_scenario = st.selectbox("Failure Scenario",
        ["Bad Input (too short)",
         "Force JSON Extraction Recovery",
         "Simulate High-Risk Conflict (risk>8 + Invest)"])
    st.markdown(f"""
    <div class="test-panel">
        <div class="test-panel-title">⚠ Test Mode Active</div>
        <div class="test-panel-body">
        Scenario: <b>{test_scenario}</b><br>
        This will intentionally trigger the selected failure mode so you can observe
        the retry engine, validation layer, and fallback logic working in real time.
        </div>
    </div>""", unsafe_allow_html=True)

st.markdown('<div class="div"></div>', unsafe_allow_html=True)
run_btn = st.button("⬡  EXECUTE WITH RELIABILITY ENGINE")


# ── Execution ──────────────────────────────────────────────────────────────────
if run_btn:
    try:
        from crewai import Agent, Task, Crew, LLM
    except ImportError as e:
        st.markdown(f'<div class="err-box">Import error: {e}</div>', unsafe_allow_html=True)
        st.stop()

    api_key = os.environ.get("GEMINI_API_KEY" if is_gemini else "GROQ_API_KEY", "")
    if not api_key:
        k = "GEMINI_API_KEY" if is_gemini else "GROQ_API_KEY"
        st.markdown(f'<div class="err-box">⚠ {k} not found in Streamlit Secrets.</div>', unsafe_allow_html=True)
        st.stop()

    if is_gemini:
        os.environ["GEMINI_API_KEY"] = api_key

    # ── Handle test scenarios ──────────────────────────────────────────────────
    active_idea = startup_idea
    if test_mode:
        scn = test_scenario
        if "Bad Input" in scn:
            active_idea = "AI"
        elif "Force JSON" in scn:
            active_idea = startup_idea  # will modify schema instruction below
        elif "High-Risk" in scn:
            active_idea = (
                "A highly speculative AI-powered meme coin launchpad targeting retail crypto speculators. "
                "No revenue model, no regulatory compliance, extreme market volatility, "
                "SEC investigation risk, and zero defensible moat. "
                "Pricing: free with 5% token allocation. TAM: unclear."
            )

    # ── Retrieve config vars ───────────────────────────────────────────────────
    persona  = analyst_persona if 'analyst_persona' in dir() else "Venture Capital Partner"
    stage    = investment_stage if 'investment_stage' in dir() else "Seed"
    strict   = risk_tolerance if 'risk_tolerance' in dir() else "Balanced"
    temp     = temperature if 'temperature' in dir() else 0.2
    concise  = concise_mode if 'concise_mode' in dir() else True
    v_off    = verbose_off if 'verbose_off' in dir() else True
    regen    = regen_on_fail

    # ── Runtime tracking ───────────────────────────────────────────────────────
    t0          = time.time()
    log_ph      = st.empty()
    status_ph   = st.empty()
    retry_ph    = st.empty()
    log_lines   = []
    attempt_log = []

    def ts():
        return f"{round(time.time()-t0,1):>5}s"

    def render_retries(attempts):
        cards = ""
        for i, (status, elapsed) in enumerate(attempts, 1):
            cls = "rcs-pass" if status == "PASS" else ("rcs-fail" if status == "FAIL" else "rcs-skip")
            cards += f"""<div class="retry-card">
                <div class="rc-attempt">Attempt {i}</div>
                <div class="rc-status {cls}">{status}</div>
                <div class="rc-time">{elapsed}</div>
            </div>"""
        retry_ph.markdown(f'<div class="retry-track">{cards}</div>', unsafe_allow_html=True)

    provider_label = "gemini" if is_gemini else "groq"
    log_lines.append((ts(), "SYS", "lt-sys",
                       f"Reliability engine started · retries={max_retries} · delay={retry_delay}s · temp={temp}"))
    _render_log(log_lines, log_ph)

    # ── Step 1: Input validation ───────────────────────────────────────────────
    log_lines.append((ts(), "SYS", "lt-sys", "Running input validation…"))
    _render_log(log_lines, log_ph)

    is_valid, reason = validate_input(active_idea, min_input_len)

    if not is_valid:
        log_lines.append((ts(), "ERR", "lt-err", f"Input validation failed: {reason}"))
        _render_log(log_lines, log_ph)
        status_ph.markdown(f"""
        <div class="status-bar">
            <div class="s-dot s-err"></div>
            <span class="s-text">Input validation failed — {reason}</span>
        </div>""", unsafe_allow_html=True)
        st.markdown(f"""
        <div class="err-box">
        ✗ <b>Input Validation Failed</b><br><br>
        Reason: {reason}<br><br>
        {'This is expected — Test Mode triggered bad input intentionally.' if test_mode else
         f'Please provide at least {min_input_len} characters describing the startup with market size, pricing, and context.'}
        </div>""", unsafe_allow_html=True)
        st.stop()

    log_lines.append((ts(), "OK", "lt-ok", f"Input valid ✓ — {len(active_idea.strip())} chars"))
    _render_log(log_lines, log_ph)

    # ── Step 2: Build crew ─────────────────────────────────────────────────────
    strictness_instruction = {
        "Conservative": "Apply strict conservative criteria. Penalize uncertainty heavily in risk scoring.",
        "Balanced":     "Apply balanced criteria — weigh upside and downside equally.",
        "Aggressive":   "Apply growth-focused criteria. Accept higher risk for large market opportunities.",
    }.get(strict, "Apply balanced criteria.")

    backstory_full = (
        f"You are a seasoned {persona} with 15+ years evaluating {stage} deals. "
        f"You are known for rigorous, data-driven analysis and returning clean, strictly formatted JSON. "
        f"You never return prose, markdown, or explanations — only the JSON object."
    )
    backstory_concise = f"Expert {persona} evaluating {stage} opportunities. Returns strict JSON only. No prose."
    backstory = backstory_concise if concise else backstory_full

    JSON_SCHEMA = """{
  "market_score": <integer 0-10>,
  "market_summary": "<2-sentence market assessment>",
  "financial_score": <integer 0-10>,
  "financial_summary": "<2-sentence financial assessment>",
  "risk_score": <integer 0-10, 10=extreme risk>,
  "risk_summary": "<2-sentence risk assessment>",
  "final_decision": "<Invest OR Consider OR Reject>",
  "confidence_level": "<Low OR Medium OR High>",
  "recommended_actions": ["action1", "action2", "action3", "action4", "action5"],
  "total_score": <float: (market_score + financial_score + (10-risk_score))/3>
}"""

    # Force broken JSON for test
    if test_mode and "Force JSON" in test_scenario:
        JSON_SCHEMA += "\n\nNote: feel free to add some extra explanation after the JSON."

    task_description = f"""You are a {persona}. {strictness_instruction}

Startup:
{active_idea}

Return ONLY this exact JSON. Nothing else. No text before or after.

{JSON_SCHEMA}

Critical rules:
- Scores: integers 0–10 only
- If risk_score > 8, final_decision MUST be 'Consider' or 'Reject' — never 'Invest'
- recommended_actions: exactly 5 specific actionable strings in a JSON array
- Return ONLY the JSON object"""

    try:
        llm = LLM(model=model_id, api_key=api_key, temperature=temp)
        analyst = Agent(
            role=persona,
            goal="Evaluate startup investment opportunities and return strictly structured JSON analysis.",
            backstory=backstory,
            llm=llm,
            verbose=not v_off,
        )
        main_task = Task(
            description=task_description,
            expected_output="A single valid JSON object. No other text.",
            agent=analyst,
        )
        crew = Crew(agents=[analyst], tasks=[main_task], verbose=not v_off)

        log_lines.append((ts(), "SYS", "lt-sys",
                           f"Crew built · {persona} · backstory={'concise' if concise else 'full'} · verbose={not v_off}"))
        _render_log(log_lines, log_ph)

    except Exception as e:
        log_lines.append((ts(), "ERR", "lt-err", f"Crew init failed: {str(e)[:80]}"))
        _render_log(log_lines, log_ph)
        st.markdown(f'<div class="err-box">Crew initialization failed: {str(e)}</div>', unsafe_allow_html=True)
        st.stop()

    # ── Step 3: Safe kickoff with retry ────────────────────────────────────────
    status_ph.markdown("""
    <div class="status-bar">
        <div class="s-dot s-run"></div>
        <span class="s-text">Retry engine running — attempt 1…</span>
    </div>""", unsafe_allow_html=True)

    attempt_log.append(("RUNNING", ts()))
    render_retries(attempt_log)

    raw_result, attempts_used, success = safe_kickoff(
        crew, retries=max_retries, delay=retry_delay,
        log_lines=log_lines, log_ph=log_ph, ts_fn=ts
    )

    # Update attempt log
    attempt_log[0] = ("PASS" if success else "FAIL", attempt_log[0][1])
    for i in range(1, attempts_used):
        attempt_log.append(("PASS" if (success and i == attempts_used - 1) else "FAIL", ts()))
    render_retries(attempt_log)

    if not success:
        log_lines.append((ts(), "ERR", "lt-err",
                           f"All {max_retries} attempts exhausted"))
        _render_log(log_lines, log_ph)
        status_ph.markdown(f"""
        <div class="status-bar">
            <div class="s-dot s-err"></div>
            <span class="s-text">All {max_retries} retry attempts failed</span>
        </div>""", unsafe_allow_html=True)
        err_str = str(raw_result)
        if "quota" in err_str.lower() or "429" in err_str or "resource_exhausted" in err_str.lower():
            st.markdown('<div class="err-box"><b>Quota Exhausted (429)</b>\n\nSwitch to Gemini 2.5 Flash and wait 60 seconds.</div>', unsafe_allow_html=True)
        elif "rate_limit" in err_str.lower():
            st.markdown('<div class="err-box"><b>Rate limit hit.</b> Retry delay was active. Try again in ~60s.</div>', unsafe_allow_html=True)
        else:
            st.markdown(f'<div class="err-box"><b>System failed after {max_retries} retries:</b>\n{err_str[:600]}</div>', unsafe_allow_html=True)
        st.stop()

    # ── Step 4: JSON extraction ────────────────────────────────────────────────
    raw_text = str(main_task.output.raw) if main_task.output else str(raw_result)
    log_lines.append((ts(), "JSON", "lt-json", "Running two-pass JSON extraction…"))
    _render_log(log_lines, log_ph)

    parsed = extract_json_safe(raw_text)

    if "error" in parsed:
        log_lines.append((ts(), "ERR", "lt-err", f"Extraction failed: {parsed['error']}"))
        _render_log(log_lines, log_ph)

        if regen:
            log_lines.append((ts(), "RETRY", "lt-retry",
                               "Auto-regenerate triggered — rebuilding crew and retrying…"))
            _render_log(log_lines, log_ph)
            time.sleep(retry_delay)
            raw2, _, success2 = safe_kickoff(
                crew, retries=2, delay=retry_delay,
                log_lines=log_lines, log_ph=log_ph, ts_fn=ts
            )
            if success2:
                raw_text2 = str(main_task.output.raw) if main_task.output else str(raw2)
                parsed = extract_json_safe(raw_text2)
                if "error" not in parsed:
                    log_lines.append((ts(), "OK", "lt-ok",
                                       "Auto-regeneration succeeded — JSON extracted ✓"))
                    _render_log(log_lines, log_ph)
                else:
                    log_lines.append((ts(), "ERR", "lt-err",
                                       "Auto-regeneration also failed — showing raw output"))
                    _render_log(log_lines, log_ph)
            else:
                log_lines.append((ts(), "ERR", "lt-err", "Auto-regeneration exhausted"))
                _render_log(log_lines, log_ph)
    else:
        log_lines.append((ts(), "JSON", "lt-json", "JSON extracted successfully ✓"))
        _render_log(log_lines, log_ph)

    # ── Step 5: Validation ─────────────────────────────────────────────────────
    val_results = validate_output(parsed)
    all_pass    = all(r[3] for r in val_results)
    fail_count  = sum(1 for r in val_results if not r[3])

    log_lines.append((ts(), "VAL", "lt-val",
                       f"Validation: {'ALL PASSED ✓' if all_pass else f'{fail_count} issue(s) found'}"))

    # ── Step 6: Cost estimation ────────────────────────────────────────────────
    est_input_tokens  = len(task_description.split()) * 1.3
    est_output_tokens = 350
    est_total_tokens  = round((est_input_tokens + est_output_tokens) * attempts_used)
    est_cost_usd      = round(est_total_tokens * 0.000001 * 0.075, 6)
    token_savings     = round(((len(backstory_full.split()) - len(backstory.split())) * 1.3))

    log_lines.append((ts(), "COST", "lt-cost",
                       f"Est. tokens: {est_total_tokens} · Est. cost: ${est_cost_usd:.6f} · Saved: ~{token_savings} tokens (concise mode)"))
    log_lines.append((ts(), "SYS", "lt-sys",
                       f"Complete · {round(time.time()-t0,1)}s · attempts: {attempts_used}/{max_retries}"))
    _render_log(log_lines, log_ph)

    elapsed = round(time.time() - t0, 1)
    status_ph.markdown(f"""
    <div class="status-bar">
        <div class="s-dot s-ok"></div>
        <span class="s-text">
            {'All checks passed — ' if all_pass else f'{fail_count} validation issue(s) — '}
            {attempts_used} attempt{'s' if attempts_used>1 else ''} · {elapsed}s
        </span>
        <span class="s-meta">{'✓ VALIDATED' if all_pass else '⚠ REVIEW'}</span>
    </div>""", unsafe_allow_html=True)

    # ── Render results ─────────────────────────────────────────────────────────
    if "error" not in parsed:
        decision   = str(parsed.get("final_decision", "Unknown")).strip()
        confidence = str(parsed.get("confidence_level", "Low")).strip()
        ms  = parsed.get("market_score", 0)
        fs  = parsed.get("financial_score", 0)
        rs  = parsed.get("risk_score", 0)
        tot = parsed.get("total_score", round((ms + fs + (10-rs))/3, 1))

        # Decision banner
        db_cls = decision_cls(decision)
        cf_cls = conf_cls(confidence)
        idea_short = active_idea[:80] + "…" if len(active_idea) > 80 else active_idea
        st.markdown(f"""
        <div class="decision-banner {db_cls}">
            <div>
                <div class="db-lbl">Final Decision</div>
                <div class="db-dec">{decision}</div>
            </div>
            <div class="db-right">
                <span class="db-conf {cf_cls}">Confidence: {confidence}</span>
                <span class="db-idea">{idea_short}</span>
            </div>
        </div>""", unsafe_allow_html=True)

        # Score grid
        st.markdown(f"""
        <div class="score-grid">
            <div class="score-card sc-m">
                <div class="sc-label">Market Score</div>
                <div class="sc-val scv-m">{ms}<span style="font-size:0.85rem;color:var(--muted)">/10</span></div>
                <div class="sc-bar-wrap"><div class="sc-bar scb-m" style="width:{ms*10}%"></div></div>
                <div class="sc-sum">{str(parsed.get("market_summary",""))[:160]}</div>
            </div>
            <div class="score-card sc-f">
                <div class="sc-label">Financial Score</div>
                <div class="sc-val scv-f">{fs}<span style="font-size:0.85rem;color:var(--muted)">/10</span></div>
                <div class="sc-bar-wrap"><div class="sc-bar scb-f" style="width:{fs*10}%"></div></div>
                <div class="sc-sum">{str(parsed.get("financial_summary",""))[:160]}</div>
            </div>
            <div class="score-card sc-r">
                <div class="sc-label">Risk Score</div>
                <div class="sc-val scv-r">{rs}<span style="font-size:0.85rem;color:var(--muted)">/10</span></div>
                <div class="sc-bar-wrap"><div class="sc-bar scb-r" style="width:{rs*10}%"></div></div>
                <div class="sc-sum">{str(parsed.get("risk_summary",""))[:160]}</div>
            </div>
        </div>""", unsafe_allow_html=True)

        # Validation panel
        vstat_html = (f'<span class="vstat-ok">ALL {len(val_results)} CHECKS PASSED</span>'
                      if all_pass else f'<span class="vstat-fail">{fail_count} ISSUE(S) FOUND</span>')
        val_rows = ""
        for icon, key, msg, passed in val_results:
            ic = "vi-ok" if icon=="✓" else ("vi-warn" if icon=="⚠" else "vi-fail")
            val_rows += f'<div class="val-row"><span class="{ic}">{icon}</span><span class="vk">{key}</span><span class="vm">— {msg}</span></div>'
        st.markdown(f"""
        <div class="val-panel">
            <div class="val-head"><span class="val-title">Validation Pipeline</span>{vstat_html}</div>
            <div class="val-body">{val_rows}</div>
        </div>""", unsafe_allow_html=True)

        # Recommended actions
        actions = parsed.get("recommended_actions", [])
        if isinstance(actions, list) and actions:
            items = "".join([f'<div class="action-item"><span class="a-num">{i:02d}</span><span class="a-txt">{a}</span></div>'
                             for i, a in enumerate(actions[:7], 1)])
            st.markdown(f"""
            <div class="actions-panel">
                <div class="actions-head">Recommended Actions</div>
                <div class="actions-body">{items}</div>
            </div>""", unsafe_allow_html=True)

        # Cost panel
        savings_pct = round((token_savings / max(est_total_tokens, 1)) * 100) if token_savings > 0 else 0
        tip = f"Concise backstory saved ~{token_savings} tokens ({savings_pct}%). temperature={temp} reduces retry waste." if token_savings > 0 else f"temperature={temp} set for stable JSON output."
        st.markdown(f"""
        <div class="cost-panel">
            <div class="cost-head">
                <span class="cost-title">Cost Intelligence</span>
                <span style="font-family:var(--mono);font-size:0.58rem;color:var(--muted);">estimated · Gemini 2.5 Flash pricing</span>
            </div>
            <div class="cost-body">
                <div class="cost-cell">
                    <div class="cost-cell-label">Est. Tokens</div>
                    <div class="cost-cell-val">{est_total_tokens:,}</div>
                    <div class="cost-cell-sub">{attempts_used} attempt(s)</div>
                </div>
                <div class="cost-cell">
                    <div class="cost-cell-label">Est. Cost</div>
                    <div class="cost-cell-val">${est_cost_usd:.5f}</div>
                    <div class="cost-cell-sub">USD per run</div>
                </div>
                <div class="cost-cell">
                    <div class="cost-cell-label">Tokens Saved</div>
                    <div class="cost-cell-val">{token_savings:+}</div>
                    <div class="cost-cell-sub">vs full backstory</div>
                </div>
                <div class="cost-cell">
                    <div class="cost-cell-label">Temperature</div>
                    <div class="cost-cell-val">{temp}</div>
                    <div class="cost-cell-sub">JSON consistency</div>
                </div>
            </div>
            <div class="cost-tip">💡 {tip}</div>
        </div>""", unsafe_allow_html=True)

        # Stats
        st.markdown(f"""
        <div class="stats-row">
            <div class="stat">total score <b>{tot}/10</b></div>
            <div class="stat">decision <b>{decision}</b></div>
            <div class="stat">attempts <b>{attempts_used}/{max_retries}</b></div>
            <div class="stat">validation <b>{'✓ passed' if all_pass else f'⚠ {fail_count} issues'}</b></div>
            <div class="stat">elapsed <b>{elapsed}s</b></div>
            <div class="stat">model <b>{model_id.split('/')[1]}</b></div>
        </div>""", unsafe_allow_html=True)

        # Raw JSON
        st.markdown(f"""
        <div class="json-panel">
            <div class="json-head">
                <span class="json-title">Raw JSON — Extracted Output</span>
                <span style="font-family:var(--mono);font-size:0.58rem;color:var(--green);">production-ready · db-insertable</span>
            </div>
            <div class="json-body">{render_json_colored(parsed)}</div>
        </div>""", unsafe_allow_html=True)

    else:
        st.markdown(f"""
        <div class="err-box">
        ✗ <b>JSON Extraction Failed</b><br><br>
        {parsed.get('error','Unknown error')}<br><br>
        Raw output preview:<br>{parsed.get('raw_preview', raw_text[:400])}
        </div>""", unsafe_allow_html=True)
