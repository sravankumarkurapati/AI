# ── ui.py — SentimentLens Streamlit frontend ───────────────────────────

import streamlit as st
import requests
import os

# ── page config ────────────────────────────────────────────────────────
st.set_page_config(
    page_title="SentimentLens — AI Sentiment Analyzer",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ── CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
    /* hide all Streamlit chrome */
    #MainMenu { visibility: hidden; }
    header { visibility: hidden; }
    footer { visibility: hidden; }
    [data-testid="stToolbar"] { display: none; }
    [data-testid="collapsedControl"] { display: none; }
    [data-testid="stSidebar"] { display: none; }

    /* reset page */
    .stApp { background: #f1f5f9; }
    .main .block-container {
        padding: 0 !important;
        max-width: 100% !important;
    }

    /* two column layout */
    .layout {
        display: grid;
        grid-template-columns: 300px 1fr;
        min-height: 100vh;
    }

    /* ── LEFT PANE ── */
    .left-pane {
        background: #1e3a5f;
        padding: 32px 24px;
        display: flex;
        flex-direction: column;
        gap: 22px;
        position: sticky;
        top: 0;
        height: 100vh;
        overflow-y: auto;
    }
    .brand-title {
        font-size: 1.5rem;
        font-weight: 800;
        color: #ffffff;
        letter-spacing: -0.01em;
        margin: 0;
    }
    .brand-title span { color: #60a5fa; }
    .brand-tagline {
        font-size: 0.78rem;
        color: #93c5fd;
        line-height: 1.6;
        margin-top: 4px;
    }
    .pane-divider {
        height: 1px;
        background: rgba(255,255,255,0.1);
    }
    .pane-section-head {
        font-size: 0.64rem;
        font-weight: 700;
        color: #60a5fa;
        letter-spacing: 0.1em;
        text-transform: uppercase;
        margin-bottom: 10px;
    }
    .stat-item {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 5px 0;
        border-bottom: 1px solid rgba(255,255,255,0.05);
    }
    .stat-item:last-child { border-bottom: none; }
    .stat-key {
        font-size: 0.78rem;
        color: #94a3b8;
        display: flex;
        align-items: center;
        gap: 7px;
    }
    .stat-value {
        font-size: 0.78rem;
        font-weight: 600;
        color: #ffffff;
    }
    .accuracy-highlight {
        background: rgba(96,165,250,0.15);
        border: 1px solid rgba(96,165,250,0.3);
        border-radius: 6px;
        padding: 1px 8px;
        color: #93c5fd !important;
    }
    .chip-wrap { display: flex; flex-wrap: wrap; gap: 5px; }
    .chip {
        font-size: 0.67rem;
        font-weight: 600;
        padding: 3px 9px;
        border-radius: 10px;
        background: rgba(96,165,250,0.12);
        border: 1px solid rgba(96,165,250,0.25);
        color: #93c5fd;
    }
    .author-name {
        font-size: 0.92rem;
        font-weight: 700;
        color: #ffffff;
        margin-bottom: 2px;
    }
    .author-detail {
        font-size: 0.75rem;
        color: #94a3b8;
        line-height: 1.7;
    }
    .contact-item {
        display: flex;
        align-items: flex-start;
        gap: 9px;
        margin: 6px 0;
    }
    .contact-icon { font-size: 13px; margin-top: 1px; flex-shrink: 0; }
    .contact-text {
        font-size: 0.75rem;
        color: #94a3b8;
        line-height: 1.5;
        word-break: break-all;
    }
    .contact-text a {
        color: #60a5fa;
        text-decoration: none;
    }
    .contact-text a:hover { text-decoration: underline; }

    /* ── RIGHT PANE ── */
    .right-pane {
        background: #ffffff;
        padding: 36px 40px;
    }
    .page-heading {
        font-size: 1.75rem;
        font-weight: 800;
        color: #0f172a;
        margin: 0 0 4px;
        letter-spacing: -0.02em;
    }
    .page-subheading {
        font-size: 0.88rem;
        color: #64748b;
        margin: 0 0 6px;
        line-height: 1.5;
    }
    .badge-row { margin-bottom: 20px; }
    .badge {
        display: inline-block;
        background: #eff6ff;
        border: 1px solid #bfdbfe;
        color: #1d4ed8;
        padding: 2px 10px;
        border-radius: 20px;
        font-size: 0.68rem;
        font-weight: 700;
        letter-spacing: 0.06em;
        margin-right: 5px;
    }
    .field-label {
        font-size: 0.7rem;
        font-weight: 700;
        color: #1d4ed8;
        letter-spacing: 0.08em;
        text-transform: uppercase;
        margin-bottom: 7px;
        margin-top: 20px;
    }

    /* text area */
    .stTextArea textarea {
        background: #f8fafc !important;
        border: 1.5px solid #cbd5e1 !important;
        border-radius: 10px !important;
        color: #0f172a !important;
        font-size: 0.93rem !important;
        line-height: 1.7 !important;
        padding: 13px 15px !important;
        font-family: inherit !important;
    }
    .stTextArea textarea:focus {
        border-color: #1d4ed8 !important;
        box-shadow: 0 0 0 3px rgba(29,78,216,0.1) !important;
        background: #ffffff !important;
    }
    .stTextArea textarea::placeholder {
        color: #94a3b8 !important;
    }

    /* analyse button */
    div[data-testid="stButton"] button {
        background: linear-gradient(135deg, #1d4ed8, #1e40af) !important;
        color: #ffffff !important;
        border: none !important;
        border-radius: 10px !important;
        font-size: 0.93rem !important;
        font-weight: 600 !important;
        padding: 0.65rem 1.5rem !important;
        box-shadow: 0 3px 12px rgba(29,78,216,0.3) !important;
        transition: all 0.2s !important;
        margin-top: 10px !important;
        width: 100% !important;
    }
    div[data-testid="stButton"] button:hover {
        box-shadow: 0 5px 18px rgba(29,78,216,0.4) !important;
        transform: translateY(-1px) !important;
    }

    /* result cards */
    .result-card-pos {
        background: #f0fdf4;
        border: 1px solid #86efac;
        border-left: 5px solid #16a34a;
        border-radius: 12px;
        padding: 18px 22px;
        margin-top: 18px;
    }
    .result-card-neg {
        background: #fff1f2;
        border: 1px solid #fecdd3;
        border-left: 5px solid #dc2626;
        border-radius: 12px;
        padding: 18px 22px;
        margin-top: 18px;
    }
    .result-label-pos {
        font-size: 1.6rem;
        font-weight: 800;
        color: #15803d;
        margin: 0 0 3px;
    }
    .result-label-neg {
        font-size: 1.6rem;
        font-weight: 800;
        color: #b91c1c;
        margin: 0 0 3px;
    }
    .result-desc {
        font-size: 0.86rem;
        color: #374151;
        margin: 0;
    }

    /* metric cards */
    div[data-testid="metric-container"] {
        background: #f8fafc !important;
        border: 1px solid #e2e8f0 !important;
        border-radius: 10px !important;
        padding: 12px 14px !important;
    }
    div[data-testid="metric-container"] label {
        color: #475569 !important;
        font-size: 0.68rem !important;
        font-weight: 700 !important;
        letter-spacing: 0.07em !important;
        text-transform: uppercase !important;
    }
    div[data-testid="metric-container"]
    div[data-testid="stMetricValue"] {
        color: #0f172a !important;
        font-size: 1.4rem !important;
        font-weight: 700 !important;
    }

    /* progress bar */
    div[data-testid="stProgress"] > div {
        background: #e2e8f0 !important;
        border-radius: 8px !important;
        height: 7px !important;
    }
    div[data-testid="stProgress"] > div > div {
        background: linear-gradient(90deg, #1d4ed8, #3b82f6) !important;
        border-radius: 8px !important;
    }

    /* score breakdown */
    .score-box {
        background: #f8fafc;
        border: 1px solid #e2e8f0;
        border-radius: 10px;
        padding: 13px 16px;
        margin-top: 12px;
        font-size: 0.84rem;
        color: #374151;
        line-height: 1.9;
    }
    .score-box strong { color: #0f172a; }
    .score-box code {
        background: #e0e7ff;
        color: #1d4ed8;
        padding: 1px 5px;
        border-radius: 4px;
        font-size: 0.81rem;
    }

    /* example box */
    .ex-pos {
        background: #f0fdf4;
        border-left: 4px solid #16a34a;
        border-radius: 0 8px 8px 0;
        padding: 10px 14px;
        font-size: 0.83rem;
        color: #374151;
        font-style: italic;
        line-height: 1.6;
        margin: 5px 0;
    }
    .ex-neg {
        background: #fff1f2;
        border-left: 4px solid #dc2626;
        border-radius: 0 8px 8px 0;
        padding: 10px 14px;
        font-size: 0.83rem;
        color: #374151;
        font-style: italic;
        line-height: 1.6;
        margin: 5px 0;
    }
    .ex-head-pos {
        font-size: 0.68rem;
        font-weight: 700;
        color: #15803d;
        letter-spacing: 0.07em;
        text-transform: uppercase;
        margin: 10px 0 5px;
    }
    .ex-head-neg {
        font-size: 0.68rem;
        font-weight: 700;
        color: #b91c1c;
        letter-spacing: 0.07em;
        text-transform: uppercase;
        margin: 10px 0 5px;
    }

    /* expander */
    details {
        background: #f8fafc !important;
        border: 1px solid #e2e8f0 !important;
        border-radius: 10px !important;
        margin-top: 12px !important;
    }
    details summary {
        font-size: 0.83rem !important;
        font-weight: 600 !important;
        color: #1d4ed8 !important;
        padding: 10px 14px !important;
        cursor: pointer !important;
    }
    details > div {
        padding: 0 14px 12px !important;
    }

    /* footer */
    .page-footer {
        margin-top: 28px;
        padding-top: 16px;
        border-top: 1px solid #f1f5f9;
        font-size: 0.74rem;
        color: #94a3b8;
        text-align: center;
        line-height: 1.7;
    }

    /* alerts */
    div[data-testid="stAlert"] {
        border-radius: 10px !important;
        font-size: 0.85rem !important;
    }

    /* slider */
    div[data-testid="stSlider"] label {
        color: #94a3b8 !important;
        font-size: 0.75rem !important;
    }

    /* spinner text */
    div[data-testid="stSpinner"] p {
        color: #374151 !important;
    }
</style>
""", unsafe_allow_html=True)

# ── constants ──────────────────────────────────────────────────────────
API_URL = os.getenv("API_URL", "http://127.0.0.1:8000")

# ── two column layout ──────────────────────────────────────────────────
left_col, right_col = st.columns([1, 2.4])

# ══════════════════════════════════════════════════════════════════════
# LEFT PANE
# ══════════════════════════════════════════════════════════════════════
with left_col:
    st.markdown("""
    <div style="background:#1e3a5f; border-radius:14px; padding:28px 22px;
                min-height:95vh; display:flex; flex-direction:column; gap:18px;">

        <!-- brand -->
        <div>
            <div style="font-size:1.4rem;font-weight:800;color:#ffffff;
                        letter-spacing:-0.01em;">
                🎬 Sentiment<span style="color:#60a5fa">Lens</span>
            </div>
            <div style="font-size:0.76rem;color:#93c5fd;
                        line-height:1.6;margin-top:5px;">
                AI-powered movie review sentiment analysis
                using LSTM deep learning
            </div>
        </div>

        <div style="height:1px;background:rgba(255,255,255,0.1)"></div>

        <!-- model details -->
        <div>
            <div style="font-size:0.63rem;font-weight:700;color:#60a5fa;
                        letter-spacing:0.1em;text-transform:uppercase;
                        margin-bottom:10px;">Model Details</div>

            <div style="display:flex;justify-content:space-between;
                        padding:5px 0;border-bottom:1px solid rgba(255,255,255,0.05)">
                <span style="font-size:0.77rem;color:#94a3b8;">🏗 Architecture</span>
                <span style="font-size:0.77rem;font-weight:600;color:#fff;">LSTM</span>
            </div>
            <div style="display:flex;justify-content:space-between;
                        padding:5px 0;border-bottom:1px solid rgba(255,255,255,0.05)">
                <span style="font-size:0.77rem;color:#94a3b8;">📊 Dataset</span>
                <span style="font-size:0.77rem;font-weight:600;color:#fff;">IMDB 25k</span>
            </div>
            <div style="display:flex;justify-content:space-between;
                        padding:5px 0;border-bottom:1px solid rgba(255,255,255,0.05)">
                <span style="font-size:0.77rem;color:#94a3b8;">🎯 Test Accuracy</span>
                <span style="font-size:0.77rem;font-weight:700;
                             color:#93c5fd;background:rgba(96,165,250,0.15);
                             border:1px solid rgba(96,165,250,0.3);
                             padding:1px 8px;border-radius:6px;">83.54%</span>
            </div>
            <div style="display:flex;justify-content:space-between;
                        padding:5px 0;border-bottom:1px solid rgba(255,255,255,0.05)">
                <span style="font-size:0.77rem;color:#94a3b8;">📖 Vocabulary</span>
                <span style="font-size:0.77rem;font-weight:600;color:#fff;">10,000 words</span>
            </div>
            <div style="display:flex;justify-content:space-between;padding:5px 0;">
                <span style="font-size:0.77rem;color:#94a3b8;">⚖️ Parameters</span>
                <span style="font-size:0.77rem;font-weight:600;color:#fff;">1.3M weights</span>
            </div>
        </div>

        <div style="height:1px;background:rgba(255,255,255,0.1)"></div>

        <!-- tech stack -->
        <div>
            <div style="font-size:0.63rem;font-weight:700;color:#60a5fa;
                        letter-spacing:0.1em;text-transform:uppercase;
                        margin-bottom:10px;">Tech Stack</div>
            <div style="display:flex;flex-wrap:wrap;gap:5px;">
                <span style="font-size:0.67rem;font-weight:600;padding:3px 9px;
                             border-radius:10px;background:rgba(96,165,250,0.12);
                             border:1px solid rgba(96,165,250,0.25);
                             color:#93c5fd;">TensorFlow</span>
                <span style="font-size:0.67rem;font-weight:600;padding:3px 9px;
                             border-radius:10px;background:rgba(96,165,250,0.12);
                             border:1px solid rgba(96,165,250,0.25);
                             color:#93c5fd;">Keras LSTM</span>
                <span style="font-size:0.67rem;font-weight:600;padding:3px 9px;
                             border-radius:10px;background:rgba(96,165,250,0.12);
                             border:1px solid rgba(96,165,250,0.25);
                             color:#93c5fd;">FastAPI</span>
                <span style="font-size:0.67rem;font-weight:600;padding:3px 9px;
                             border-radius:10px;background:rgba(96,165,250,0.12);
                             border:1px solid rgba(96,165,250,0.25);
                             color:#93c5fd;">Streamlit</span>
                <span style="font-size:0.67rem;font-weight:600;padding:3px 9px;
                             border-radius:10px;background:rgba(96,165,250,0.12);
                             border:1px solid rgba(96,165,250,0.25);
                             color:#93c5fd;">Docker</span>
                <span style="font-size:0.67rem;font-weight:600;padding:3px 9px;
                             border-radius:10px;background:rgba(96,165,250,0.12);
                             border:1px solid rgba(96,165,250,0.25);
                             color:#93c5fd;">AWS EC2</span>
                <span style="font-size:0.67rem;font-weight:600;padding:3px 9px;
                             border-radius:10px;background:rgba(96,165,250,0.12);
                             border:1px solid rgba(96,165,250,0.25);
                             color:#93c5fd;">Python</span>
            </div>
        </div>

        <div style="height:1px;background:rgba(255,255,255,0.1)"></div>

        <!-- built by -->
        <div>
            <div style="font-size:0.63rem;font-weight:700;color:#60a5fa;
                        letter-spacing:0.1em;text-transform:uppercase;
                        margin-bottom:10px;">Built By</div>
            <div style="font-size:0.92rem;font-weight:700;
                        color:#ffffff;margin-bottom:3px;">
                Sravan Kumar Kurapati
            </div>
            <div style="font-size:0.75rem;color:#94a3b8;line-height:1.7;">
                MS Information Systems<br>
                Northeastern University<br>
                Boston, MA
            </div>
        </div>

        <div style="height:1px;background:rgba(255,255,255,0.1)"></div>

        <!-- contact -->
        <div>
            <div style="font-size:0.63rem;font-weight:700;color:#60a5fa;
                        letter-spacing:0.1em;text-transform:uppercase;
                        margin-bottom:10px;">Contact</div>
            <div style="display:flex;align-items:flex-start;
                        gap:9px;margin:5px 0;">
                <span style="font-size:13px;margin-top:1px;">✉️</span>
                <a href="mailto:kurapati.sr@northeastern.edu"
                   style="font-size:0.74rem;color:#60a5fa;
                          text-decoration:none;line-height:1.5;
                          word-break:break-all;">
                    kurapati.sr@northeastern.edu
                </a>
            </div>
            <div style="display:flex;align-items:center;gap:9px;margin:5px 0;">
                <span style="font-size:13px;">📞</span>
                <span style="font-size:0.74rem;color:#94a3b8;">
                    +1-857-427-7767
                </span>
            </div>
        </div>

    </div>
    """, unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════
# RIGHT PANE
# ══════════════════════════════════════════════════════════════════════
with right_col:

    # header
    st.markdown("""
    <div style="margin-bottom:6px;">
        <div style="font-size:1.7rem;font-weight:800;color:#0f172a;
                    letter-spacing:-0.02em;margin-bottom:3px;">
            🎬 SentimentLens
        </div>
        <div style="font-size:0.87rem;color:#64748b;margin-bottom:10px;">
            Real-time movie review sentiment analysis —
            type any review and get an instant AI prediction
        </div>
        <span style="display:inline-block;background:#eff6ff;
                     border:1px solid #bfdbfe;color:#1d4ed8;
                     padding:2px 10px;border-radius:20px;
                     font-size:0.67rem;font-weight:700;
                     letter-spacing:0.06em;margin-right:4px;">LSTM</span>
        <span style="display:inline-block;background:#eff6ff;
                     border:1px solid #bfdbfe;color:#1d4ed8;
                     padding:2px 10px;border-radius:20px;
                     font-size:0.67rem;font-weight:700;
                     letter-spacing:0.06em;margin-right:4px;">NLP</span>
        <span style="display:inline-block;background:#eff6ff;
                     border:1px solid #bfdbfe;color:#1d4ed8;
                     padding:2px 10px;border-radius:20px;
                     font-size:0.67rem;font-weight:700;
                     letter-spacing:0.06em;margin-right:4px;">TENSORFLOW</span>
        <span style="display:inline-block;background:#eff6ff;
                     border:1px solid #bfdbfe;color:#1d4ed8;
                     padding:2px 10px;border-radius:20px;
                     font-size:0.67rem;font-weight:700;
                     letter-spacing:0.06em;">AWS EC2</span>
    </div>
    <hr style="border-color:#f1f5f9;margin:14px 0 18px;">
    """, unsafe_allow_html=True)

    # threshold slider
    threshold = st.slider(
        "Decision threshold",
        min_value=0.1,
        max_value=0.9,
        value=0.5,
        step=0.05,
        help="Scores ≥ threshold → POSITIVE. Below → NEGATIVE."
    )

    # input label
    st.markdown(
        "<div style='font-size:0.7rem;font-weight:700;color:#1d4ed8;"
        "letter-spacing:0.08em;text-transform:uppercase;"
        "margin-top:16px;margin-bottom:7px;'>Enter a movie review</div>",
        unsafe_allow_html=True
    )

    # text area
    review_text = st.text_area(
        label="",
        placeholder="Type or paste any movie review here...\n"
                    "Tip: longer reviews (20+ words) give more accurate results.",
        height=140,
        key="review_input"
    )

    # analyse button
    analyse_clicked = st.button("🔍  Analyse Sentiment")

    # examples expander
    with st.expander("📖  See example reviews to copy"):
        st.markdown(
            "<div style='font-size:0.68rem;font-weight:700;"
            "color:#15803d;letter-spacing:0.07em;"
            "text-transform:uppercase;margin-bottom:6px;'>"
            "Positive examples</div>",
            unsafe_allow_html=True
        )
        st.markdown("""
        <div class='ex-pos'>
        "This was one of the most brilliant films I have ever watched.
        The acting was outstanding, the story compelling from start to finish,
        and the direction masterful. I left feeling genuinely moved and uplifted."
        </div>
        <div class='ex-pos'>
        "An absolute masterpiece of modern cinema. Every scene was crafted
        with care and the performances were breathtaking.
        Highly recommended to anyone who loves great storytelling."
        </div>
        """, unsafe_allow_html=True)

        st.markdown(
            "<div style='font-size:0.68rem;font-weight:700;"
            "color:#b91c1c;letter-spacing:0.07em;"
            "text-transform:uppercase;margin:10px 0 6px;'>"
            "Negative examples</div>",
            unsafe_allow_html=True
        )
        st.markdown("""
        <div class='ex-neg'>
        "This was one of the worst films I have ever watched. The acting was
        atrocious, the story made no sense, and every scene was painful
        to sit through. A complete waste of time."
        </div>
        <div class='ex-neg'>
        "Terrible script, dreadful pacing, and wooden performances.
        I walked out after the first hour and never looked back."
        </div>
        """, unsafe_allow_html=True)

    # ── prediction ─────────────────────────────────────────────────────
    if analyse_clicked and review_text.strip():
        with st.spinner("Running sentiment analysis..."):
            try:
                response = requests.post(
                    f"{API_URL}/predict",
                    json={"review": review_text},
                    params={"threshold": threshold},
                    timeout=15
                )

                if response.status_code == 200:
                    result     = response.json()
                    label      = result["label"]
                    score      = result["score"]
                    confidence = result["confidence"]
                    word_count = result["word_count"]
                    warning    = result.get("warning")

                    # result card
                    if label == "POSITIVE":
                        st.markdown("""
                        <div class='result-card-pos'>
                            <div class='result-label-pos'>👍 POSITIVE</div>
                            <div class='result-desc'>
                                The model detected positive sentiment
                                in this review.
                            </div>
                        </div>
                        """, unsafe_allow_html=True)
                    else:
                        st.markdown("""
                        <div class='result-card-neg'>
                            <div class='result-label-neg'>👎 NEGATIVE</div>
                            <div class='result-desc'>
                                The model detected negative sentiment
                                in this review.
                            </div>
                        </div>
                        """, unsafe_allow_html=True)

                    # metrics
                    st.markdown(
                        "<div style='height:14px'></div>",
                        unsafe_allow_html=True
                    )
                    m1, m2, m3 = st.columns(3)
                    with m1:
                        st.metric(
                            label="CONFIDENCE",
                            value=f"{confidence}%"
                        )
                    with m2:
                        st.metric(
                            label="RAW SCORE",
                            value=f"{score:.3f}",
                            help="0.0 = strongly negative  →  1.0 = strongly positive"
                        )
                    with m3:
                        st.metric(label="WORD COUNT", value=word_count)

                    # confidence bar
                    st.markdown(
                        "<p style='font-size:0.78rem;font-weight:600;"
                        "color:#374151;margin:14px 0 6px;'>"
                        "Confidence level</p>",
                        unsafe_allow_html=True
                    )
                    st.progress(confidence / 100)

                    if warning:
                        st.warning(f"⚠️  {warning}")

                    # score breakdown
                    verdict = (
                        "✅  Strong prediction — model is confident"
                        if confidence > 75
                        else "⚠️  Uncertain — try a longer, more detailed review"
                    )
                    st.markdown(f"""
                    <div class='score-box'>
                        <strong>How to read this result</strong><br><br>
                        📊 Score <code>{score:.3f}</code> — the model assigns a
                        <strong>{score*100:.1f}%</strong> probability
                        that this review is positive<br>
                        🎚 Threshold <code>{threshold:.2f}</code> —
                        scores above this are labelled
                        <strong>POSITIVE</strong><br>
                        🔍 {verdict}
                    </div>
                    """, unsafe_allow_html=True)

                else:
                    st.error(
                        f"API error {response.status_code}: {response.text}"
                    )

            except requests.exceptions.ConnectionError:
                st.error(
                    "🔌  Cannot connect to the API. "
                    "Make sure FastAPI is running on port 8000."
                )
            except requests.exceptions.Timeout:
                st.error(
                    "⏱  Request timed out. "
                    "The server took too long to respond."
                )
            except Exception as e:
                st.error(f"Unexpected error: {str(e)}")

    elif analyse_clicked and not review_text.strip():
        st.warning("Please enter a review before clicking Analyse.")

    # footer
    st.markdown("""
    <div class='page-footer'>
        SentimentLens &nbsp;·&nbsp;
        LSTM + TensorFlow &nbsp;·&nbsp;
        FastAPI + Streamlit &nbsp;·&nbsp;
        Docker + AWS EC2<br>
        Sravan Kumar Kurapati &nbsp;·&nbsp;
        <a href='mailto:kurapati.sr@northeastern.edu'
           style='color:#94a3b8;text-decoration:none;'>
           kurapati.sr@northeastern.edu
        </a>
        &nbsp;·&nbsp; +1-857-427-7767
    </div>
    """, unsafe_allow_html=True)