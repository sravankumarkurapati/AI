# ── ui.py — SentimentLens Streamlit frontend ───────────────────────────

import streamlit as st
import requests
import os

# ── page config ────────────────────────────────────────────────────────
st.set_page_config(
    page_title="SentimentLens — AI Sentiment Analyzer",
    page_icon="🎬",
    layout="centered"
)

# ── custom CSS — professional dark-accent design ───────────────────────
st.markdown("""
<style>
    /* page background */
    .stApp {
        background: linear-gradient(135deg, #0f0f1a 0%, #1a1a2e 50%, #16213e 100%);
    }

    /* main content area */
    .main .block-container {
        padding-top: 2rem;
        padding-bottom: 3rem;
        max-width: 780px;
    }

    /* header gradient text */
    .hero-title {
        font-size: 3rem;
        font-weight: 800;
        background: linear-gradient(90deg, #667eea 0%, #764ba2 50%, #f093fb 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        margin-bottom: 0.2rem;
        line-height: 1.1;
    }

    .hero-subtitle {
        font-size: 1rem;
        color: #8892b0;
        margin-bottom: 0.5rem;
        letter-spacing: 0.05em;
    }

    .hero-badge {
        display: inline-block;
        background: rgba(102, 126, 234, 0.15);
        border: 1px solid rgba(102, 126, 234, 0.4);
        color: #667eea;
        padding: 3px 12px;
        border-radius: 20px;
        font-size: 0.75rem;
        font-weight: 600;
        letter-spacing: 0.08em;
        margin-right: 6px;
        margin-bottom: 4px;
    }

    /* text area */
    .stTextArea textarea {
        background: rgba(255, 255, 255, 0.05) !important;
        border: 1px solid rgba(102, 126, 234, 0.3) !important;
        border-radius: 12px !important;
        color: #ccd6f6 !important;
        font-size: 0.95rem !important;
        line-height: 1.7 !important;
        padding: 14px !important;
        transition: border-color 0.3s ease !important;
    }
    .stTextArea textarea:focus {
        border-color: rgba(102, 126, 234, 0.8) !important;
        box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1) !important;
    }
    .stTextArea textarea::placeholder {
        color: #4a5568 !important;
    }

    /* analyse button */
    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
        color: white !important;
        border: none !important;
        border-radius: 10px !important;
        font-size: 1rem !important;
        font-weight: 600 !important;
        padding: 0.65rem 2rem !important;
        letter-spacing: 0.04em !important;
        transition: all 0.3s ease !important;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.3) !important;
    }
    .stButton > button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 6px 20px rgba(102, 126, 234, 0.5) !important;
    }
    .stButton > button:active {
        transform: translateY(0px) !important;
    }

    /* example buttons — smaller */
    div[data-testid="column"] .stButton > button {
        background: rgba(255,255,255,0.05) !important;
        border: 1px solid rgba(255,255,255,0.12) !important;
        color: #8892b0 !important;
        font-size: 0.85rem !important;
        font-weight: 500 !important;
        padding: 0.4rem 1rem !important;
        box-shadow: none !important;
        border-radius: 8px !important;
    }
    div[data-testid="column"] .stButton > button:hover {
        border-color: rgba(102, 126, 234, 0.5) !important;
        color: #667eea !important;
        transform: none !important;
        box-shadow: none !important;
    }

    /* result cards */
    .result-positive {
        background: linear-gradient(135deg,
            rgba(16, 185, 129, 0.15) 0%,
            rgba(5, 150, 105, 0.08) 100%);
        border: 1px solid rgba(16, 185, 129, 0.4);
        border-left: 4px solid #10b981;
        padding: 20px 24px;
        border-radius: 12px;
        margin-top: 20px;
    }

    .result-negative {
        background: linear-gradient(135deg,
            rgba(239, 68, 68, 0.15) 0%,
            rgba(220, 38, 38, 0.08) 100%);
        border: 1px solid rgba(239, 68, 68, 0.4);
        border-left: 4px solid #ef4444;
        padding: 20px 24px;
        border-radius: 12px;
        margin-top: 20px;
    }

    .result-label-pos {
        font-size: 2rem;
        font-weight: 800;
        color: #10b981;
        margin: 0;
        letter-spacing: 0.05em;
    }

    .result-label-neg {
        font-size: 2rem;
        font-weight: 800;
        color: #ef4444;
        margin: 0;
        letter-spacing: 0.05em;
    }

    .result-desc {
        font-size: 0.9rem;
        margin: 6px 0 0;
        opacity: 0.8;
    }

    /* metric cards */
    div[data-testid="metric-container"] {
        background: rgba(255, 255, 255, 0.04) !important;
        border: 1px solid rgba(255, 255, 255, 0.08) !important;
        border-radius: 10px !important;
        padding: 14px !important;
    }
    div[data-testid="metric-container"] label {
        color: #8892b0 !important;
        font-size: 0.78rem !important;
        letter-spacing: 0.06em !important;
        text-transform: uppercase !important;
    }
    div[data-testid="metric-container"] div[data-testid="stMetricValue"] {
        color: #ccd6f6 !important;
        font-size: 1.5rem !important;
        font-weight: 700 !important;
    }

    /* progress bar */
    div[data-testid="stProgress"] > div {
        background: rgba(255,255,255,0.08) !important;
        border-radius: 10px !important;
        height: 8px !important;
    }
    div[data-testid="stProgress"] > div > div {
        background: linear-gradient(90deg, #667eea, #764ba2) !important;
        border-radius: 10px !important;
    }

    /* sidebar */
    section[data-testid="stSidebar"] {
        background: rgba(15, 15, 26, 0.95) !important;
        border-right: 1px solid rgba(102, 126, 234, 0.15) !important;
    }
    section[data-testid="stSidebar"] .stMarkdown {
        color: #8892b0 !important;
    }

    /* slider */
    div[data-testid="stSlider"] div[role="slider"] {
        background: #667eea !important;
    }

    /* divider */
    hr {
        border-color: rgba(255,255,255,0.08) !important;
    }

    /* labels and text */
    .stMarkdown p { color: #8892b0; }
    h1, h2, h3 { color: #ccd6f6 !important; }

    /* score breakdown box */
    .score-breakdown {
        background: rgba(255,255,255,0.03);
        border: 1px solid rgba(255,255,255,0.08);
        border-radius: 10px;
        padding: 14px 18px;
        margin-top: 12px;
        font-size: 0.88rem;
        color: #8892b0;
        line-height: 1.8;
    }

    /* footer */
    .footer {
        text-align: center;
        color: #4a5568;
        font-size: 0.78rem;
        margin-top: 2rem;
        letter-spacing: 0.04em;
    }

    /* stack chips */
    .stack-chip {
        display: inline-block;
        background: rgba(102, 126, 234, 0.1);
        border: 1px solid rgba(102, 126, 234, 0.25);
        color: #667eea;
        padding: 2px 10px;
        border-radius: 12px;
        font-size: 0.75rem;
        margin: 2px;
    }
</style>
""", unsafe_allow_html=True)

# ── API URL ────────────────────────────────────────────────────────────
API_URL = os.getenv("API_URL", "http://127.0.0.1:8000")

# ── session state — initialise BEFORE any widget renders ──────────────
# stores the current text area content across reruns
# example buttons update this → text area reads it on next rerun
if "review_text_value" not in st.session_state:
    st.session_state.review_text_value = ""

# ── sidebar ────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("### 🧠 SentimentLens")
    st.markdown("---")

    st.markdown("""
    <div style='color:#8892b0; font-size:0.88rem; line-height:1.8'>
    Classifies movie reviews as <span style='color:#10b981'>positive</span>
    or <span style='color:#ef4444'>negative</span> using a deep learning model
    trained on 25,000 IMDB reviews.
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("**Model**")
    st.markdown("""
    <div style='font-size:0.83rem;color:#8892b0;line-height:1.9'>
    🏗 Architecture: LSTM<br>
    📊 Training data: IMDB 25k reviews<br>
    🎯 Test accuracy: 83.54%<br>
    📖 Vocabulary: 10,000 words<br>
    ⚖️ Parameters: 1.3M weights
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("**Stack**")
    st.markdown("""
    <span class='stack-chip'>TensorFlow</span>
    <span class='stack-chip'>Keras LSTM</span>
    <span class='stack-chip'>FastAPI</span>
    <span class='stack-chip'>Streamlit</span>
    <span class='stack-chip'>Docker</span>
    <span class='stack-chip'>AWS EC2</span>
    """, unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("**Settings**")
    threshold = st.slider(
        "Decision threshold",
        min_value=0.1,
        max_value=0.9,
        value=0.5,
        step=0.05,
        help="Scores above this → POSITIVE. Below → NEGATIVE."
    )
    st.markdown(f"""
    <div style='font-size:0.8rem;color:#4a5568;margin-top:4px'>
    Currently: score ≥ {threshold:.2f} = POSITIVE
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("""
    <div style='font-size:0.78rem;color:#4a5568;line-height:1.7'>
    Built by Sravan Kumar Kurapati<br>
    MS Information Systems — Northeastern University
    </div>
    """, unsafe_allow_html=True)

# ── hero header ────────────────────────────────────────────────────────
st.markdown("""
<div style='text-align:center; padding: 1.5rem 0 1rem'>
    <div class='hero-title'>🎬 SentimentLens</div>
    <div class='hero-subtitle'>
        Real-time NLP sentiment analysis powered by LSTM + TensorFlow
    </div>
    <div style='margin-top:10px'>
        <span class='hero-badge'>LSTM</span>
        <span class='hero-badge'>NLP</span>
        <span class='hero-badge'>LIVE API</span>
        <span class='hero-badge'>AWS EC2</span>
    </div>
</div>
""", unsafe_allow_html=True)

st.markdown("---")

# ── text area — renders FIRST, reads from session state ───────────────
st.markdown("#### 📝 Enter a movie review")

review_text = st.text_area(
    label="",
    placeholder="Paste or type any movie review here...\n\n"
                "e.g. This film was an absolute masterpiece. "
                "The performances were breathtaking and the story "
                "kept me completely gripped from start to finish.",
    height=160,
    value=st.session_state.review_text_value,  # reads from session state
    key="review_input"
)

# sync whatever the user typed back into session state
# so it persists when the analyse button triggers a rerun
st.session_state.review_text_value = review_text

# ── example buttons — AFTER text area ─────────────────────────────────
# placed after text area so st.rerun() re-renders the text area
# with the new value already set in session state
st.markdown(
    "<div style='font-size:0.85rem;color:#4a5568;"
    "margin:8px 0 6px'>Try an example:</div>",
    unsafe_allow_html=True
)

ex_col1, ex_col2 = st.columns(2)

with ex_col1:
    if st.button("👍 Positive example", use_container_width=True):
        st.session_state.review_text_value = (
            "This was one of the most brilliant films I have ever had "
            "the pleasure of watching. The acting was outstanding and "
            "utterly convincing, the story was compelling from the very "
            "first scene to the last, and the direction was masterful. "
            "I left the cinema feeling genuinely moved and uplifted. "
            "An absolute must-watch for any lover of great cinema."
        )
        st.rerun()   # rerun so text area updates immediately

with ex_col2:
    if st.button("👎 Negative example", use_container_width=True):
        st.session_state.review_text_value = (
            "This was one of the worst films I have ever had the "
            "misfortune of watching. The acting was completely atrocious, "
            "the story made absolutely no sense whatsoever, and every "
            "single scene was painful to sit through. The dialogue was "
            "cringeworthy and the pacing was unbearably slow. "
            "A complete and utter waste of two hours."
        )
        st.rerun()   # rerun so text area updates immediately

# ── analyse button ─────────────────────────────────────────────────────
st.markdown("<div style='height:12px'></div>", unsafe_allow_html=True)
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    analyse_clicked = st.button(
        "🔍 Analyse Sentiment",
        use_container_width=True
    )

# ── prediction logic ───────────────────────────────────────────────────
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

                # ── result card ────────────────────────────────────────
                if label == "POSITIVE":
                    st.markdown(f"""
                    <div class="result-positive">
                        <div class="result-label-pos">👍 POSITIVE</div>
                        <div class="result-desc" style="color:#6ee7b7">
                            The model detected positive sentiment in this review.
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                else:
                    st.markdown(f"""
                    <div class="result-negative">
                        <div class="result-label-neg">👎 NEGATIVE</div>
                        <div class="result-desc" style="color:#fca5a5">
                            The model detected negative sentiment in this review.
                        </div>
                    </div>
                    """, unsafe_allow_html=True)

                # ── metrics ────────────────────────────────────────────
                st.markdown(
                    "<div style='height:16px'></div>",
                    unsafe_allow_html=True
                )
                m1, m2, m3 = st.columns(3)
                with m1:
                    st.metric(label="CONFIDENCE", value=f"{confidence}%")
                with m2:
                    st.metric(
                        label="RAW SCORE",
                        value=f"{score:.3f}",
                        help="0.0 = strongly negative  →  1.0 = strongly positive"
                    )
                with m3:
                    st.metric(label="WORD COUNT", value=word_count)

                # ── confidence bar ─────────────────────────────────────
                st.markdown(
                    "<div style='margin-top:16px;font-size:0.83rem;"
                    "color:#8892b0;margin-bottom:6px'>Confidence level</div>",
                    unsafe_allow_html=True
                )
                st.progress(confidence / 100)

                # ── warning for short inputs ───────────────────────────
                if warning:
                    st.warning(f"⚠️ {warning}")

                # ── score breakdown ────────────────────────────────────
                verdict = (
                    "✅ Strong prediction — model is confident"
                    if confidence > 75
                    else "⚠️ Uncertain — try a longer, more detailed review"
                )
                st.markdown(f"""
                <div class="score-breakdown">
                    <strong style="color:#ccd6f6">How to read this result</strong><br><br>
                    📊 Score <code>{score:.3f}</code> means the model assigns a
                    <strong>{score*100:.1f}%</strong> probability that this review is positive<br>
                    🎚 Threshold is set to <code>{threshold:.2f}</code> —
                    scores above this are labelled POSITIVE<br>
                    🔍 {verdict}
                </div>
                """, unsafe_allow_html=True)

            else:
                st.error(f"API error {response.status_code}: {response.text}")

        except requests.exceptions.ConnectionError:
            st.error(
                "🔌 Cannot connect to the API. "
                "Make sure FastAPI is running on port 8000."
            )
        except requests.exceptions.Timeout:
            st.error("⏱ Request timed out. The server took too long to respond.")
        except Exception as e:
            st.error(f"Unexpected error: {str(e)}")

elif analyse_clicked and not review_text.strip():
    st.warning("Please enter a review before clicking Analyse.")

# ── footer ─────────────────────────────────────────────────────────────
st.markdown("---")
st.markdown("""
<div class='footer'>
    SentimentLens &nbsp;·&nbsp;
    LSTM + TensorFlow &nbsp;·&nbsp;
    FastAPI + Streamlit &nbsp;·&nbsp;
    Deployed on AWS EC2 &nbsp;·&nbsp;
    Built by Sravan Kumar Kurapati
</div>
""", unsafe_allow_html=True)