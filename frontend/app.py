"""FinSight AI - Streamlit Frontend"""

import os
import requests
import streamlit as st

API_URL = os.getenv("API_URL", "http://localhost:8000")

st.set_page_config(page_title="FinSight AI", page_icon="F", layout="wide")

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }
    header[data-testid="stHeader"] {
        display: none;
    }
    .block-container {
        padding-top: 2.5rem;
        padding-left: 2rem;
        max-width: 1100px;
    }
    .logo-container {
        display: flex;
        align-items: center;
        gap: 12px;
        margin-bottom: 4px;
    }
    .logo-icon {
        width: 40px;
        height: 40px;
        background: linear-gradient(135deg, #111827 0%, #374151 100%);
        border-radius: 10px;
        display: flex;
        align-items: center;
        justify-content: center;
        color: white;
        font-weight: 700;
        font-size: 1.1rem;
        letter-spacing: -0.5px;
        flex-shrink: 0;
    }
    .logo-text {
        font-size: 1.6rem;
        font-weight: 700;
        color: #111827;
        letter-spacing: -0.5px;
        line-height: 1;
    }
    .logo-text span {
        color: #2563EB;
    }
    .sub-header {
        font-size: 0.9rem;
        color: #6B7280;
        margin-top: 2px;
        margin-bottom: 1.5rem;
        padding-left: 52px;
    }
    .stTabs [data-baseweb="tab-list"] {
        gap: 0px;
        border-bottom: 1px solid #E5E7EB;
    }
    .stTabs [data-baseweb="tab"] {
        padding: 10px 20px;
        font-size: 0.85rem;
        font-weight: 500;
    }
    .sidebar-section {
        font-size: 0.8rem;
        color: #4B5563;
        line-height: 1.6;
    }
    .pipeline-step {
        padding: 6px 0;
        font-size: 0.8rem;
        color: #374151;
    }
    .pipeline-num {
        display: inline-block;
        width: 20px;
        height: 20px;
        background: #E5E7EB;
        border-radius: 50%;
        text-align: center;
        font-size: 0.7rem;
        line-height: 20px;
        font-weight: 600;
        color: #374151;
        margin-right: 8px;
    }
    div[data-testid="stMetric"] {
        background: #F9FAFB;
        border: 1px solid #E5E7EB;
        border-radius: 8px;
        padding: 12px 16px;
    }
    div[data-testid="stMetric"] label {
        font-size: 0.75rem !important;
        color: #6B7280 !important;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    div[data-testid="stMetric"] [data-testid="stMetricValue"] {
        font-size: 1.4rem !important;
        font-weight: 700 !important;
    }
    .stButton > button[kind="primary"] {
        background: #111827;
        color: white;
        border: none;
        border-radius: 6px;
        font-weight: 500;
        font-size: 0.85rem;
    }
    .stButton > button[kind="primary"]:hover {
        background: #1F2937;
    }
</style>
""", unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.markdown("#### Settings")
    st.caption("LLM provider is configured in .env")
    st.markdown("---")
    st.markdown("#### Agent Pipeline")
    steps = [
        ("1", "Planner", "Identifies ticker and competitors"),
        ("2", "Market Data", "Fetches stock prices and fundamentals"),
        ("3", "News Sentiment", "Searches and analyzes recent news"),
        ("4", "Competitor", "Compares with industry peers"),
        ("5", "Chart Generator", "Creates price and volume charts"),
        ("6", "Report Writer", "Writes the research report"),
        ("7", "Evaluator", "Scores report quality"),
    ]
    for num, name, desc in steps:
        st.markdown(f'<div class="pipeline-step"><span class="pipeline-num">{num}</span><strong>{name}</strong> &mdash; {desc}</div>', unsafe_allow_html=True)

    st.markdown("---")
    try:
        health = requests.get(f"{API_URL}/health", timeout=3).json()
        count = health.get("analyses_in_memory", 0)
        st.caption(f"Analyses in memory: {count}")
    except Exception:
        st.caption("Backend: not connected")

# Main header
st.markdown('''
<div class="logo-container">
    <div class="logo-icon">FA</div>
    <div class="logo-text">Fin<span>Sight</span> AI</div>
</div>
<p class="sub-header">Multi-agent financial analysis platform</p>
''', unsafe_allow_html=True)

# Search bar
col1, col2 = st.columns([4, 1])
with col1:
    company = st.text_input(
        "Company",
        placeholder="Enter a company name, e.g. Tesla, Apple, Reliance Industries",
        label_visibility="collapsed"
    )
with col2:
    analyze_btn = st.button("Analyze", type="primary", use_container_width=True)

st.markdown("---")

if analyze_btn and company:
    progress_bar = st.progress(0)
    status_text = st.empty()

    status_text.info(f"Running analysis for **{company}**...")
    progress_bar.progress(10)

    try:
        response = requests.post(
            f"{API_URL}/analyze",
            json={"company": company},
            timeout=300
        )

        if response.status_code != 200:
            st.error(f"Error: {response.json().get('detail', 'Unknown error')}")
            st.stop()

        data = response.json()
        progress_bar.progress(100)
        status_text.success("Analysis complete")

        # Company header
        ticker = data.get("ticker", "N/A")
        st.markdown(f"## {data.get('company', company)} ({ticker})")

        # Metrics row
        col1, col2, col3 = st.columns(3)
        with col1:
            score = data.get("evaluation", {}).get("overall", "N/A")
            st.metric("Quality Score", score)
        with col2:
            st.metric("Charts Generated", len(data.get("chart_paths", [])))
        with col3:
            error_count = len(data.get("errors", []))
            st.metric("Errors", error_count)

        # Tabs
        tab1, tab2, tab3, tab4 = st.tabs(["Report", "Charts", "Evaluation", "Agent Logs"])

        with tab1:
            report = data.get("report", "No report was generated.")
            st.markdown(report)

        with tab2:
            chart_paths = data.get("chart_paths", [])
            if chart_paths:
                for path in chart_paths:
                    if os.path.exists(path):
                        st.image(path, use_container_width=True)
                    else:
                        filename = os.path.basename(path)
                        st.image(f"{API_URL}/charts/{filename}", use_container_width=True)
            else:
                st.info("No charts were generated for this analysis.")

        with tab3:
            eval_data = data.get("evaluation", {})
            if eval_data.get("overall") and eval_data["overall"] != "N/A":
                st.markdown("### Report Quality Assessment")
                st.markdown("")
                ecol1, ecol2 = st.columns(2)
                with ecol1:
                    st.markdown(f"**Accuracy:** {eval_data.get('accuracy', 'N/A')}")
                    st.markdown(f"**Completeness:** {eval_data.get('completeness', 'N/A')}")
                with ecol2:
                    st.markdown(f"**Clarity:** {eval_data.get('clarity', 'N/A')}")
                    st.markdown(f"**Usefulness:** {eval_data.get('usefulness', 'N/A')}")
                st.markdown("---")
                st.markdown(f"**Overall Score:** {eval_data.get('overall', 'N/A')}")
                feedback = eval_data.get('feedback', '')
                if feedback:
                    st.markdown(f"**Feedback:** {feedback}")
            else:
                st.info("No evaluation data available.")

        with tab4:
            logs = data.get("agent_logs", [])
            for i, log in enumerate(logs):
                st.text(f"[{i+1}] {log}")

            errors = data.get("errors", [])
            if errors:
                st.markdown("### Errors")
                for err in errors:
                    st.error(err)

    except requests.exceptions.ConnectionError:
        status_text.error("Cannot connect to backend. Make sure the server is running.")
        st.code("uvicorn app.main:app --reload", language="bash")
    except requests.exceptions.Timeout:
        status_text.error("Request timed out. The analysis may be taking longer than expected.")
    except Exception as e:
        status_text.error(f"Something went wrong: {str(e)}")

elif analyze_btn:
    st.warning("Please enter a company name.")