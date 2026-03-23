# ── ui.py — SentimentLens Streamlit frontend ───────────────────────────

import streamlit as st
import requests
import os

# ── page config ────────────────────────────────────────────────────────
st.set_page_config(
    page_title="SentimentLens",
    page_icon="🎬",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# ── CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
    /* hide Streamlit top bar, hamburger menu, footer */
    #MainMenu { visibility: hidden; }
    header { visibility: hidden; }
    footer { visibility: hidden; }
    [data-testid="stToolbar"] { display: none; }
    [data-testid="collapsedControl"] { display: none; }

    /* white background */
    .stApp {
        background-color: #ffffff;
    }
    .main .block-container {
        padding-top: 1.5rem;
        padding-bottom: 2rem;
        max-width: 720px;
    }

    /* hero */
    .hero {
        background: linear-gradient(135deg, #1d4ed8 0%, #1e40af 100%);
        border-radius: 14px;
        padding: 24px 28px;
        margin-bottom: 20px;
    }
    .hero-title {
        font-size: 1.9rem;
        font-weight: 800;
        color: #ffffff;
        margin: 0 0 4px;
        letter-spacing: -0.01em;
    }
    .hero-subtitle {
        font-size: 0.88rem;
        color: rgba(255,255,255,0.85);
        margin: 0 0 14px;
        line-height: 1.5;
    }
    .hero-badge {
        display: inline-block;
        background: rgba(255,255,255,0.18);
        border: 1px solid rgba(255,255,255,0.35);
        color: #ffffff;
        padding: 2px 10px;
        border-radius: 20px;
        font-size: 0.7rem;
        font-weight: 700;
        letter-spacing: 0.07em;
        margin-right: 5px;
    }

    /* section label */
    .section-label {
        font-size: 0.72rem;
        font-weight: 700;
        color: #1d4ed8;
        letter-spacing: 0.08em;
        text-transform: uppercase;
        margin-bottom: 8px;
    }

    /* text area */
    .stTextArea textarea {
        background: #f8fafc !important;
        border: 1.5px solid #cbd5e1 !important;
        border-radius: 10px !important;
        color: #0f172a !important;
        font-size: 0.93rem !important;
        line-height: 1.7 !important;
        padding: 12px 14px !important;
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
    .stButton > button {
        background: linear-gradient(135deg, #1d4ed8, #1e40af) !important;
        color: #ffffff !important;
        border: none !important;
        border-radius: 10px !important;
        font-size: 0.95rem !important;
        font-weight: 600 !important;
        padding: 0.6rem 1.5rem !important;
        box-shadow: 0 3px 10px rgba(29,78,216,0.3) !important;
        transition: all 0.2s !important;
        width: 100% !important;
    }
    .stButton > button:hover {
        box-shadow: 0 5px 16px rgba(29,78,216,0.4) !important;
        transform: translateY(-1px) !important;
    }

    /* result cards */
    .result-positive {
        background: #f0fdf4;
        border: 1px solid #86efac;
        border-left: 5px solid #16a34a;
        border-radius: 12px;
        padding: 18px 22px;
        margin-top: 16px;
    }
    .result-negative {
        background: #fff1f2;
        border: 1px solid #fecdd3;
        border-left: 5px solid #dc2626;
        border-radius: 12px;
        padding: 18px 22px;
        margin-top: 16px;
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
        font-size: 0.88rem;
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
        font-size: 0.7rem !important;
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
        border-radius: 10px !important;
        height: 8px !important;
    }
    div[data-testid="stProgress"] > div > div {
        background: linear-gradient(90deg, #1d4ed8, #3b82f6) !important;
        border-radius: 10px !important;
    }

    /* score box */
    .score-box {
        background: #f8fafc;
        border: 1px solid #e2e8f0;
        border-radius: 10px;
        padding: 13px 16px;
        margin-top: 12px;
        font-size: 0.85rem;
        color: #374151;
        line-height: 1.9;
    }
    .score-box strong {
        color: #0f172a;
    }
    .score-box code {
        background: #e2e8f0;
        color: #1d4ed8;
        padding: 1px 5px;
        border-radius: 4px;
        font-size: 0.82rem;
    }

    /* examples box */
    .example-box {
        background: #f8fafc;
        border: 1px solid #e2e8f0;
        border-left: 4px solid #1d4ed8;
        border-radius: 0 8px 8px 0;
        padding: 10px 14px;
        font-size: 0.84rem;
        color: #374151;
        line-height: 1.6;
        margin: 6px 0;
        font-style: italic;
    }
    .example-box-neg {
        background: #fff8f8;
        border: 1px solid #fecdd3;
        border-left: 4px solid #dc2626;
        border-radius: 0 8px 8px 0;
        padding: 10px 14px;
        font-size: 0.84rem;
        color: #374151;
        line-height: 1.6;
        margin: 6px 0;
        font-style: italic;
    }

    /* sidebar */
    section[data-testid="stSidebar"] {
        background: #f8fafc !important;
        border-right: 1px solid #e2e8f0 !important;
    }
    section[data-testid="stSidebar"] p,
    section[data-testid="stSidebar"] div,
    section[data-testid="stSidebar"] span {
        color: #374151 !important;
    }

    /* stack chip */
    .stack-chip {
        display: inline-block;
        background: #eff6ff;
        border: 1px solid #bfdbfe;
        color: #1d4ed8;
        padding: 2px 9px;
        border-radius: 12px;
        font-size: 0.7rem;
        font-weight: 600;
        margin: 2px;
    }

    /* divider */
    hr { border-color: #e2e8f0 !important; }

    /* footer */
    .footer {
        text-align: center;
        color: #94a3b8;
        font-size: 0.76rem;
        margin-top: 1.5rem;
        letter-spacing: 0.03em;
    }

    /* expander */
    details summary {
        color: #1d4ed8 !important;
        font-size: 0.85rem !important;
        font-weight: 600 !important;
    }
    details {
        background: #f8fafc !important;
        border: 1px solid #e2e8f0 !important;
        border-radius: 10px !important;
        padding: 4px 12px !important;
    }

    /* general text visibility */
    p, span, div, label {
        color: #374151;
    }
    h1, h2, h3, h4, h5 {
        color: #0f172a !important;
    }

    /* warning / info boxes */
    div[data-testid="stAlert"] {
        border-radius: 10px !important;
    }
</style>
""", unsafe_allow_html=True)

# ── constants ──────────────────────────────────────────────────────────
API_URL = os.getenv("API_URL", "http://127.0.0.1:8000")

# ── sidebar ────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown(
        "<p style='font-size:1rem;font-weight:700;color:#0f172a;"
        "margin-bottom:2px'>🎬 SentimentLens</p>",
        unsafe_allow_html=True
    )
    st.markdown(
        "<p style='font-size:0.78rem;color:#64748b;"
        "margin-bottom:12px'>AI Sentiment Analyzer</p>",
        unsafe_allow_html=True
    )
    st.markdown("---")

    st.markdown(
        "<p style='font-size:0.7rem;font-weight:700;color:#1d4ed8;"
        "letter-spacing:.08em;text-transform:uppercase;"
        "margin-bottom:6px'>About</p>",
        unsafe_allow_html=True
    )
    st.markdown(
        "<p style='font-size:0.83rem;color:#374151;line-height:1.7'>"
        "Classifies movie reviews as "
        "<span style='color:#15803d;font-weight:600'>positive</span> or "
        "<span style='color:#b91c1c;font-weight:600'>negative</span> "
        "using an LSTM deep learning model trained on 25,000 IMDB reviews."
        "</p>",
        unsafe_allow_html=True
    )

    st.markdown(
        "<p style='font-size:0.7rem;font-weight:700;color:#1d4ed8;"
        "letter-spacing:.08em;text-transform:uppercase;"
        "margin:12px 0 6px'>Model</p>",
        unsafe_allow_html=True
    )
    st.markdown(
        "<p style='font-size:0.82rem;color:#374151;line-height:2'>"
        "🏗 Architecture: LSTM<br>"
        "📊 Dataset: IMDB 25k reviews<br>"
        "🎯 Test accuracy: 83.54%<br>"
        "📖 Vocabulary: 10,000 words<br>"
        "⚖️ Parameters: 1.3M weights"
        "</p>",
        unsafe_allow_html=True
    )

    st.markdown(
        "<p style='font-size:0.7rem;font-weight:700;color:#1d4ed8;"
        "letter-spacing:.08em;text-transform:uppercase;"
        "margin:12px 0 6px'>Stack</p>",
        unsafe_allow_html=True
    )
    st.markdown(
        "<span class='stack-chip'>TensorFlow</span>"
        "<span class='stack-chip'>Keras LSTM</span>"
        "<span class='stack-chip'>FastAPI</span>"
        "<span class='stack-chip'>Streamlit</span>"
        "<span class='stack-chip'>Docker</span>"
        "<span class='stack-chip'>AWS EC2</span>",
        unsafe_allow_html=True
    )

    st.markdown("---")
    threshold = st.slider(
        "Decision threshold",
        min_value=0.1,
        max_value=0.9,
        value=0.5,
        step=0.05,
        help="Scores ≥ threshold = POSITIVE. Below = NEGATIVE."
    )
    st.markdown(
        f"<p style='font-size:0.78rem;color:#64748b;margin-top:4px'>"
        f"Score ≥ {threshold:.2f} → POSITIVE</p>",
        unsafe_allow_html=True
    )

    st.markdown("---")
    st.markdown(
        "<p style='font-size:0.78rem;color:#64748b;line-height:1.7'>"
        "Built by <strong style='color:#374151'>Sravan Kumar Kurapati</strong>"
        "<br>MS Information Systems<br>Northeastern University</p>",
        unsafe_allow_html=True
    )

# ── hero ───────────────────────────────────────────────────────────────
st.markdown("""
<div class='hero'>
    <div class='hero-title'>🎬 SentimentLens</div>
    <div class='hero-subtitle'>
        Real-time movie review sentiment analysis —
        powered by LSTM deep learning and deployed on AWS
    </div>
    <span class='hero-badge'>LSTM</span>
    <span class='hero-badge'>NLP</span>
    <span class='hero-badge'>TENSORFLOW</span>
    <span class='hero-badge'>AWS EC2</span>
    <span class='hero-badge'>83.54% ACCURACY</span>
</div>
""", unsafe_allow_html=True)

# ── input ──────────────────────────────────────────────────────────────
st.markdown(
    "<p class='section-label'>Enter a movie review</p>",
    unsafe_allow_html=True
)

review_text = st.text_area(
    label="",
    placeholder="Type or paste any movie review here...\n"
                "Tip: longer reviews (20+ words) give more accurate results.",
    height=130,
    key="review_input"
)

# ── analyse button ─────────────────────────────────────────────────────
analyse_clicked = st.button("🔍  Analyse Sentiment")

# ── examples expander ──────────────────────────────────────────────────
with st.expander("📖  See example reviews"):
    st.markdown(
        "<p style='font-size:0.72rem;font-weight:700;color:#15803d;"
        "letter-spacing:.07em;text-transform:uppercase;"
        "margin-bottom:6px'>Positive examples</p>",
        unsafe_allow_html=True
    )
    st.markdown("""
    <div class='example-box'>
    "This was one of the most brilliant films I have ever watched.
    The acting was outstanding, the story compelling from start to finish,
    and the direction masterful. I left feeling genuinely moved."
    </div>
    <div class='example-box'>
    "An absolute masterpiece. Every scene was crafted with care and
    the performances were breathtaking. Highly recommended."
    </div>
    """, unsafe_allow_html=True)

    st.markdown(
        "<p style='font-size:0.72rem;font-weight:700;color:#b91c1c;"
        "letter-spacing:.07em;text-transform:uppercase;"
        "margin:10px 0 6px'>Negative examples</p>",
        unsafe_allow_html=True
    )
    st.markdown("""
    <div class='example-box-neg'>
    "This was one of the worst films I have ever watched. The acting was
    atrocious, the story made no sense, and every scene was painful
    to sit through. A complete waste of time."
    </div>
    <div class='example-box-neg'>
    "Terrible script, dreadful pacing, and wooden performances.
    I walked out after the first hour and never looked back."
    </div>
    """, unsafe_allow_html=True)

# ── prediction ─────────────────────────────────────────────────────────
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
                    <div class='result-positive'>
                        <div class='result-label-pos'>👍 POSITIVE</div>
                        <div class='result-desc'>
                            The model detected positive sentiment
                            in this review.
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                else:
                    st.markdown("""
                    <div class='result-negative'>
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
                    st.metric(label="CONFIDENCE", value=f"{confidence}%")
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
                    "<p style='font-size:0.8rem;font-weight:600;"
                    "color:#374151;margin:14px 0 6px'>"
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
                    📊 Score <code>{score:.3f}</code> means the model assigns a
                    <strong>{score*100:.1f}%</strong> probability
                    that this review is positive<br>
                    🎚 Threshold is <code>{threshold:.2f}</code> —
                    scores above this are labelled POSITIVE<br>
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
            st.error("⏱  Request timed out. The server took too long.")
        except Exception as e:
            st.error(f"Unexpected error: {str(e)}")

elif analyse_clicked and not review_text.strip():
    st.warning("Please enter a review before clicking Analyse.")

# ── footer ─────────────────────────────────────────────────────────────
st.markdown("---")
st.markdown(
        "<p style='font-size:0.78rem;color:#64748b;line-height:1.9'>"
        "Built by <strong style='color:#374151'>Sravan Kumar Kurapati</strong><br>"
        "MS Information Systems<br>"
        "Northeastern University<br>"
        "<a href='mailto:kurapati.sr@northeastern.edu' "
        "style='color:#1d4ed8;text-decoration:none'>"
        "kurapati.sr@northeastern.edu</a><br>"
        "<span style='color:#374151'>+1-857-427-7767</span>"
        "</p>",
        unsafe_allow_html=True
    )