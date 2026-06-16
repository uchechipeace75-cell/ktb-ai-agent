import streamlit as st
import os
import html
from dotenv import load_dotenv
from tavily import TavilyClient
from groq import Groq

load_dotenv()
TAVILY_API_KEY = os.getenv('TAVILY_API_KEY')
GROQ_API_KEY = os.getenv('GROQ_API_KEY')
client = Groq(api_key=GROQ_API_KEY)

st.set_page_config(
    page_title="Klugekopf TechBridge AI Agent",
    page_icon="🤖",
    layout="centered"
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@300;400;500;600;700&family=Inter:wght@300;400;500;600&display=swap');

/* ── Reset & base ── */
*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

html, body, .stApp, .main, .block-container {
    background-color: #080C14 !important;
    font-family: 'Inter', sans-serif !important;
    color: #E2E8F0 !important;
}

.block-container {
    max-width: 820px !important;
    padding: 0 24px 80px !important;
}

/* ── Hide Streamlit chrome ── */
#MainMenu, footer, header { visibility: hidden; }
[data-testid="stToolbar"] { display: none !important; }

/* ── Animated hero orb ── */
.hero-wrapper {
    position: relative;
    text-align: center;
    padding: 64px 0 48px;
    overflow: hidden;
}

.orb {
    position: absolute;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -60%);
    width: 320px;
    height: 320px;
    border-radius: 50%;
    background: radial-gradient(circle at 35% 35%,
        rgba(56, 182, 255, 0.18) 0%,
        rgba(99, 102, 241, 0.10) 40%,
        transparent 70%);
    filter: blur(40px);
    animation: pulse 6s ease-in-out infinite;
    pointer-events: none;
    z-index: 0;
}

@keyframes pulse {
    0%, 100% { transform: translate(-50%, -60%) scale(1); opacity: 0.7; }
    50%       { transform: translate(-50%, -60%) scale(1.15); opacity: 1; }
}

.hero-badge {
    display: inline-flex;
    align-items: center;
    gap: 8px;
    background: rgba(56, 182, 255, 0.10);
    border: 1px solid rgba(56, 182, 255, 0.25);
    border-radius: 100px;
    padding: 6px 16px;
    font-family: 'Space Grotesk', sans-serif;
    font-size: 12px;
    font-weight: 600;
    letter-spacing: 0.08em;
    text-transform: uppercase;
    color: #38B6FF;
    margin-bottom: 24px;
    position: relative;
    z-index: 1;
}

.hero-badge .dot {
    width: 6px;
    height: 6px;
    border-radius: 50%;
    background: #38B6FF;
    animation: blink 2s ease-in-out infinite;
}

@keyframes blink {
    0%, 100% { opacity: 1; }
    50%       { opacity: 0.3; }
}

.hero-title {
    font-family: 'Space Grotesk', sans-serif !important;
    font-size: 52px !important;
    font-weight: 700 !important;
    line-height: 1.1 !important;
    letter-spacing: -0.03em !important;
    color: #F8FAFC !important;
    position: relative;
    z-index: 1;
    margin-bottom: 16px;
}

.hero-title span {
    background: linear-gradient(135deg, #38B6FF 0%, #818CF8 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
}

.hero-subtitle {
    font-family: 'Inter', sans-serif !important;
    font-size: 16px !important;
    color: #64748B !important;
    font-weight: 400 !important;
    position: relative;
    z-index: 1;
    margin-bottom: 8px;
}

/* ── Agent pills ── */
.agents-row {
    display: flex;
    gap: 10px;
    justify-content: center;
    margin: 28px 0 0;
    flex-wrap: wrap;
    position: relative;
    z-index: 1;
}

.agent-pill {
    display: flex;
    align-items: center;
    gap: 6px;
    background: rgba(255,255,255,0.04);
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 100px;
    padding: 7px 14px;
    font-size: 13px;
    font-weight: 500;
    color: #94A3B8;
    font-family: 'Inter', sans-serif;
}

.agent-pill .icon { font-size: 14px; }

/* ── Divider ── */
.divider {
    height: 1px;
    background: linear-gradient(90deg, transparent, rgba(56,182,255,0.2), transparent);
    margin: 8px 0 40px;
}

/* ── Input area ── */
.input-label {
    font-family: 'Space Grotesk', sans-serif;
    font-size: 13px;
    font-weight: 600;
    letter-spacing: 0.06em;
    text-transform: uppercase;
    color: #38B6FF;
    margin-bottom: 10px;
}

/* Override Streamlit label */
.stTextInput label {
    font-family: 'Space Grotesk', sans-serif !important;
    font-size: 13px !important;
    font-weight: 600 !important;
    letter-spacing: 0.06em !important;
    text-transform: uppercase !important;
    color: #38B6FF !important;
}

.stTextInput input {
    background: rgba(255,255,255,0.04) !important;
    border: 1px solid rgba(255,255,255,0.10) !important;
    border-radius: 14px !important;
    color: #F8FAFC !important;
    font-family: 'Inter', sans-serif !important;
    font-size: 16px !important;
    padding: 14px 18px !important;
    transition: border-color 0.2s ease, box-shadow 0.2s ease !important;
    caret-color: #38B6FF !important;
}

.stTextInput input:focus {
    border-color: rgba(56, 182, 255, 0.5) !important;
    box-shadow: 0 0 0 3px rgba(56, 182, 255, 0.08) !important;
    outline: none !important;
}

.stTextInput input::placeholder {
    color: #334155 !important;
}

/* ── Generate button ── */
.stButton > button {
    width: 100% !important;
    background: linear-gradient(135deg, #38B6FF 0%, #6366F1 100%) !important;
    color: #FFFFFF !important;
    border: none !important;
    border-radius: 14px !important;
    font-family: 'Space Grotesk', sans-serif !important;
    font-size: 15px !important;
    font-weight: 600 !important;
    letter-spacing: 0.02em !important;
    padding: 14px 28px !important;
    transition: opacity 0.2s ease, transform 0.15s ease, box-shadow 0.2s ease !important;
    box-shadow: 0 4px 24px rgba(56, 182, 255, 0.25) !important;
    margin-top: 12px !important;
    cursor: pointer !important;
}

.stButton > button:hover {
    opacity: 0.9 !important;
    transform: translateY(-1px) !important;
    box-shadow: 0 8px 32px rgba(56, 182, 255, 0.35) !important;
}

.stButton > button:active {
    transform: translateY(0) !important;
}

/* ── Spinner ── */
div[data-testid="stSpinner"] {
    background: rgba(255,255,255,0.03) !important;
    border: 1px solid rgba(255,255,255,0.07) !important;
    border-radius: 14px !important;
    padding: 20px 24px !important;
    margin-top: 16px !important;
}

div[data-testid="stSpinner"] p,
div[data-testid="stSpinner"] div,
div[data-testid="stSpinner"] span {
    color: #64748B !important;
    font-family: 'Inter', sans-serif !important;
    font-size: 14px !important;
}

/* ── Success banner ── */
div[data-testid="stAlert"] {
    background: rgba(34, 197, 94, 0.08) !important;
    border: 1px solid rgba(34, 197, 94, 0.25) !important;
    border-radius: 12px !important;
    color: #4ADE80 !important;
}

/* ── Warning ── */
.stWarning {
    background: rgba(251, 191, 36, 0.08) !important;
    border: 1px solid rgba(251, 191, 36, 0.25) !important;
    border-radius: 12px !important;
    color: #FCD34D !important;
}

/* ── Generated content card ── */
.output-header {
    display: flex;
    align-items: center;
    gap: 12px;
    margin: 44px 0 20px;
}

.output-header-line {
    flex: 1;
    height: 1px;
    background: rgba(255,255,255,0.06);
}

.output-header-label {
    font-family: 'Space Grotesk', sans-serif;
    font-size: 11px;
    font-weight: 700;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    color: #475569;
}

.content-card {
    background: rgba(255, 255, 255, 0.03) !important;
    border: 1px solid rgba(255, 255, 255, 0.07) !important;
    border-radius: 20px !important;
    padding: 40px !important;
    position: relative;
    overflow: hidden;
}

.content-card::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    height: 2px;
    background: linear-gradient(90deg, transparent, #38B6FF, #6366F1, transparent);
    opacity: 0.6;
}

/* ── Generated text styles ── */
.content-card h1 {
    font-family: 'Space Grotesk', sans-serif !important;
    font-size: 32px !important;
    font-weight: 700 !important;
    color: #F1F5F9 !important;
    line-height: 1.2 !important;
    margin-bottom: 20px !important;
    letter-spacing: -0.02em !important;
}

.content-card h2 {
    font-family: 'Space Grotesk', sans-serif !important;
    font-size: 24px !important;
    font-weight: 600 !important;
    color: #E2E8F0 !important;
    line-height: 1.3 !important;
    margin: 28px 0 12px !important;
    padding-left: 12px !important;
    border-left: 2px solid #38B6FF !important;
}

.content-card h3 {
    font-family: 'Space Grotesk', sans-serif !important;
    font-size: 18px !important;
    font-weight: 600 !important;
    color: #CBD5E1 !important;
    line-height: 1.4 !important;
    margin: 20px 0 8px !important;
}

.content-card p {
    font-family: 'Inter', sans-serif !important;
    font-size: 16px !important;
    line-height: 1.8 !important;
    color: #94A3B8 !important;
    margin-bottom: 16px !important;
}

.content-card li {
    font-family: 'Inter', sans-serif !important;
    font-size: 16px !important;
    line-height: 1.7 !important;
    color: #94A3B8 !important;
    margin-bottom: 6px !important;
}

/* Scrollbar styling */
::-webkit-scrollbar { width: 6px; }
::-webkit-scrollbar-track { background: transparent; }
::-webkit-scrollbar-thumb { background: rgba(56,182,255,0.2); border-radius: 3px; }
::-webkit-scrollbar-thumb:hover { background: rgba(56,182,255,0.4); }
</style>
""", unsafe_allow_html=True)


# ── Hero section ──
st.markdown("""
<div class="hero-wrapper">
    <div class="orb"></div>
    <div class="hero-badge">
        <span class="dot"></span>
        AI-Powered · Real-Time Research
    </div>
    <h1 class="hero-title">Klugekopf <span>TechBridge</span></h1>
    <p class="hero-subtitle">Research any topic. Get a full SEO-optimized blog post in seconds.</p>
    <div class="agents-row">
        <div class="agent-pill"><span class="icon">🔍</span> Researcher</div>
        <div class="agent-pill"><span class="icon">✍️</span> Content Creator</div>
        <div class="agent-pill"><span class="icon">📈</span> SEO Optimizer</div>
    </div>
</div>
<div class="divider"></div>
""", unsafe_allow_html=True)


# ── Input ──
topic = st.text_input(
    'TOPIC',
    placeholder='e.g. The future of quantum computing in 2025…'
)


# ── Button ──
generate = st.button('✦  Generate Content  ✦')


def render_generated_content(text):
    text = text.replace("*Full Blog Post:*", "# Full Blog Post")
    text = text.replace("*Blog Post:*", "# Blog Post")
    text = text.replace("*Full Blog Post*", "# Full Blog Post")
    text = text.replace("*Blog Post*", "# Blog Post")
    text = text.replace("**", "")

    html_lines = []

    for line in text.splitlines():
        line = line.strip()
        if not line:
            html_lines.append("<br>")
        elif line.startswith("### "):
            html_lines.append(f"<h3>{html.escape(line[4:])}</h3>")
        elif line.startswith("## "):
            html_lines.append(f"<h2>{html.escape(line[3:])}</h2>")
        elif line.startswith("# "):
            html_lines.append(f"<h1>{html.escape(line[2:])}</h1>")
        else:
            html_lines.append(f"<p>{html.escape(line)}</p>")

    return "\n".join(html_lines)


# ── Generate ──
if generate:
    if topic:
        with st.spinner('Three agents are working on your content…'):
            tavily = TavilyClient(api_key=TAVILY_API_KEY)

            research = tavily.search(
                query=topic,
                search_depth='advanced'
            )

            research_text = '\n'.join(
                [r['content'] for r in research['results']]
            )

            prompt = f"""
You are a team of 3 AI agents:

1. Researcher - You have found this information:
{research_text}

2. Content Creator - Write a detailed blog post about:
{topic}

3. SEO Optimizer - Optimize the blog post with keywords, meta description and SEO tips.

Please provide:
- A full blog post
- Meta description
- Recommended keywords
- SEO tips
"""

            response = client.chat.completions.create(
                model='llama-3.3-70b-versatile',
                messages=[{'role': 'user', 'content': prompt}]
            )

            output = response.choices[0].message.content

        st.success('✓ Content generated successfully!')

        st.markdown("""
        <div class="output-header">
            <div class="output-header-line"></div>
            <div class="output-header-label">Generated Content</div>
            <div class="output-header-line"></div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown(
            f'<div class="content-card">{render_generated_content(output)}</div>',
            unsafe_allow_html=True
        )
    else:
        st.warning('⚠️ Please enter a topic first.')
