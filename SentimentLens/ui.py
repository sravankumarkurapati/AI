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

# ── CSS — clean professional blue and white ────────────────────────────
st.markdown("""
<style>
    /* white page background */
    .stApp {
        background-color: #f0f4f8;
    }

    .main .block-container {
        padding-top: 2rem;
        padding-bottom: 3rem;
        max-width: 760px;
    }

    /* hero banner */
    .hero {
        background: linear-gradient(135deg, #1a56db 0%, #1e429f 100%);
        border-radius: 16px;
        padding: 32px 36px;
        margin-bottom: 24px;
        color: white;
    }
    .hero-title {
        font-size: 2.2rem;
        font-weight: 800;
        color: white;
        margin: 0 0 6px;
        letter-spacing: -0.02em;
    }
    .hero-subtitle {
        font-size: 0.95rem;
        color: rgba(255,255,255,0.8);
        margin: 0 0 16px;
        line-height: 1.6;
    }
    .hero-badge {
        display: inline-block;
        background: rgba(255,255,255,0.15);
        border: 1px solid rgba(255,255,255,0.3);
        color: white;
        padding: 3px 12px;
        border-radius: 20px;
        font-size: 0.72rem;
        font-weight: 600;
        letter-spacing: 0.06em;
        margin-right: 6px;
    }

    /* white content cards */
    .content-card {
        background: white;
        border-radius: 12px;
        padding: 24px 28px;
        margin-bottom: 16px;
        border: 1px solid #e2e8f0;
        box-shadow: 0 1px 4px rgba(0,0,0,0.06);
    }

    .card-label {
        font-size: 0.78rem;
        font-weight: 700;
        color: #1a56db;
        letter-spacing: 0.08em;
        text-transform: uppercase;
        margin-bottom: 10px;
    }

    /* text area */
    .stTextArea textarea {
        background: #f8fafc !important;
        border: 1.5px solid #cbd5e1 !important;
        border-radius: 10px !important;
        color: #1e293b !important;
        font-size: 0.95rem !important;
        line-height: 1.7 !important;
        padding: 14px !important;
        transition: border-color 0.2s !important;
    }
    .stTextArea textarea:focus {
        border-color: #1a56db !important;
        box-shadow: 0 0 0 3px rgba(26,86,219,0.08) !important;
        background: white !important;
    }
    .stTextArea textarea::placeholder {
        color: #94a3b8 !important;
    }

    /* analyse button */
    .stButton > button {
        background: linear-gradient(135deg, #1a56db 0%, #1e429f 100%) !important;
        color: white !important;
        border: none !important;
        border-radius: 10px !important;
        font-size: 0.95rem !important;
        font-weight: 600 !important;
        padding: 0.65rem 2rem !important;
        letter-spacing: 0.03em !important;
        box-shadow: 0 4px 12px rgba(26,86,219,0.25) !important;
        transition: all 0.2s ease !important;
    }
    .stButton > button:hover {
        box-shadow: 0 6px 18px rgba(26,86,219,0.35) !important;
        transform: translateY(-1px) !important;
    }
    .stButton > button:active {
        transform: translateY(0) !important;
    }

    /* result cards */
    .result-positive {
        background: #f0fdf4;
        border: 1px solid #86efac;
        border-left: 5px solid #16a34a;
        border-radius: 12px;
        padding: 20px 24px;
        margin-top: 16px;
    }
    .result-negative {
        background: #fff1f2;
        border: 1px solid #fda4af;
        border-left: 5px solid #dc2626;
        border-radius: 12px;
        padding: 20px 24px;
        margin-top: 16px;
    }
    .result-label-pos {
        font-size: 1.8rem;
        font-weight: 800;
        color: #16a34a;
        margin: 0 0 4px;
    }
    .result-label-neg {
        font-size: 1.8rem;
        font-weight: 800;
        color: #dc2626;
        margin: 0 0 4px;
    }
    .result-desc {
        font-size: 0.9rem;
        color: #64748b;
        margin: 0;
    }

    /* metric cards */
    div[data-testid="metric-container"] {
        background: white !important;
        border: 1px solid #e2e8f0 !important;
        border-radius: 10px !important;
        padding: 14px 16px !important;
        box-shadow: 0 1px 3px rgba(0,0,0,0.05) !important;
    }
    div[data-testid="metric-container"] label {
        color: #64748b !important;
        font-size: 0.72rem !important;
        font-weight: 700 !important;
        letter-spacing: 0.08em !important;
        text-transform: uppercase !important;
    }
    div[data-testid="metric-container"]
    div[data-testid="stMetricValue"] {
        color: #1e293b !important;
        font-size: 1.5rem !important;
        font-weight: 700 !important;
    }

    /* progress bar */
    div[data-testid="stProgress"] > div {
        background: #e2e8f0 !important;
        border-radius: 10px !important;
        height: 8px !important;
    }
    div[data-testid="stProgress"] > div > div {
        background: linear-gradient(90deg, #1a56db, #3b82f6) !important;
        border-radius: 10px !important;
    }

    /* sidebar */
    section[data-testid="stSidebar"] {
        background: white !important;
        border-right: 1px solid #e2e8f0 !important;
    }

    /* divider */
    hr {
        border-color: #e2e8f0 !important;
    }

    /* score breakdown */
    .score-box {
        background: #f8fafc;
        border: 1px solid #e2e8f0;
        border-radius: 10px;
        padding: 14px 18px;
        margin-top: 14px;
        font-size: 0.88rem;
        color: #475569;
        line-height: 1.9;
    }

    /* example box */
    .example-box {
        background: #f8fafc;
        border: 1px solid #e2e8f0;
        border-left: 4px solid #1a56db;
        border-radius: 0 10px 10px 0;
        padding: 12px 16px;
        font-size: 0.85rem;
        color: #475569;
        line-height: 1.7;
        margin: 6px 0;
        font-style: italic;
    }

    /* footer */
    .footer {
        text-align: center;
        color: #94a3b8;
        font-size: 0.78rem;
        margin-top: 2rem;
        letter-spacing: 0.03em;
    }

    /* stack chip */
    .stack-chip {
        display: inline-block;
        background: #eff6ff;
        border: 1px solid #bfdbfe;
        color: #1a56db;
        padding: 2px 10px;
        border-radius: 12px;
        font-size: 0.72rem;
        font-weight: 600;
        margin: 2px;
    }

    /* general text */
    .stMarkdown p { color: #475569; }
    h1, h2, h3, h4 { color: #1e293b !important; }
</style>
""", unsafe_allow_html=True)

# ── API URL ────────────────────────────────────────────────────────────
API_URL = os.getenv("API_URL", "http://127.0.0.1:8000")

# ── sidebar ────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown(
        "<div style='font-size:1.1rem;font-weight:700;"
        "color:#1e293b;margin-bottom:4px'>🎬 SentimentLens</div>",
        unsafe_allow_html=True
    )
    st.markdown(
        "<div style='font-size:0.8rem;color:#94a3b8;"
        "margin-bottom:16px'>AI Sentiment Analyzer</div>",
        unsafe_allow_html=True
    )
    st.markdown("---")

    st.markdown(
        "<div style='font-size:0.72rem;font-weight:700;"
        "color:#1a56db;letter-spacing:.08em;"
        "text-transform:uppercase;margin-bottom:8px'>About</div>",
        unsafe_allow_html=True
    )
    st.markdown("""
    <div style='font-size:0.85rem;color:#475569;line-height:1.8'>
    Classifies movie reviews as
    <span style='color:#16a34a;font-weight:600'>positive</span> or
    <span style='color:#dc2626;font-weight:600'>negative</span>
    using a deep learning LSTM model trained on 25,000 IMDB reviews.
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<div style='height:16px'></div>", unsafe_allow_html=True)
    st.markdown(
        "<div style='font-size:0.72rem;font-weight:700;"
        "color:#1a56db;letter-spacing:.08em;"
        "text-transform:uppercase;margin-bottom:8px'>Model</div>",
        unsafe_allow_html=True
    )
    st.markdown("""
    <div style='font-size:0.83rem;color:#475569;line-height:2'>
    🏗 Architecture: LSTM<br>
    📊 Dataset: IMDB 25,000 reviews<br>
    🎯 Test accuracy: 83.54%<br>
    📖 Vocabulary: 10,000 words<br>
    ⚖️ Parameters: 1.3M weights
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<div style='height:16px'></div>", unsafe_allow_html=True)
    st.markdown(
        "<div style='font-size:0.72rem;font-weight:700;"
        "color:#1a56db;letter-spacing:.08em;"
        "text-transform:uppercase;margin-bottom:8px'>Stack</div>",
        unsafe_allow_html=True
    )
    st.markdown("""
    <span class='stack-chip'>TensorFlow</span>
    <span class='stack-chip'>Keras LSTM</span>
    <span class='stack-chip'>FastAPI</span>
    <span class='stack-chip'>Streamlit</span>
    <span class='stack-chip'>Docker</span>
    <span class='stack-chip'>AWS EC2</span>
    """, unsafe_allow_html=True)

    st.markdown("---")
    st.markdown(
        "<div style='font-size:0.72rem;font-weight:700;"
        "color:#1a56db;letter-spacing:.08em;"
        "text-transform:uppercase;margin-bottom:8px'>Settings</div>",
        unsafe_allow_html=True
    )
    threshold = st.slider(
        "Decision threshold",
        min_value=0.1,
        max_value=0.9,
        value=0.5,
        step=0.05,
        help="Scores ≥ threshold → POSITIVE. Below → NEGATIVE."
    )
    st.markdown(
        f"<div style='font-size:0.78rem;color:#94a3b8;margin-top:4px'>"
        f"Score ≥ {threshold:.2f} will be classified as POSITIVE</div>",
        unsafe_allow_html=True
    )

    st.markdown("---")
    st.markdown("""
    <div style='font-size:0.78rem;color:#94a3b8;line-height:1.7'>
    Built by <strong style='color:#475569'>Sravan Kumar Kurapati</strong><br>
    MS Information Systems<br>
    Northeastern University
    </div>
    """, unsafe_allow_html=True)

# ── hero banner ────────────────────────────────────────────────────────
st.markdown("""
<div class='hero'>
    <div class='hero-title'>🎬 SentimentLens</div>
    <div class='hero-subtitle'>
        Real-time movie review sentiment analysis powered by
        LSTM deep learning — type any review and get an instant prediction.
    </div>
    <span class='hero-badge'>LSTM</span>
    <span class='hero-badge'>NLP</span>
    <span class='hero-badge'>TENSORFLOW</span>
    <span class='hero-badge'>LIVE API</span>
    <span class='hero-badge'>AWS EC2</span>
</div>
""", unsafe_allow_html=True)

# ── input card ─────────────────────────────────────────────────────────
st.markdown("""
<div class='content-card'>
    <div class='card-label'>Enter your review</div>
</div>
""", unsafe_allow_html=True)

review_text = st.text_area(
    label="",
    placeholder="Type or paste any movie review here...\n\n"
                "Tip: longer reviews (20+ words) give more accurate results.",
    height=160,
    key="review_input"
)

# ── analyse button ─────────────────────────────────────────────────────
st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    analyse_clicked = st.button(
        "🔍  Analyse Sentiment",
        use_container_width=True
    )

# ── example reviews — display only, no autofill ───────────────────────
with st.expander("📖  See example reviews to try"):
    st.markdown(
        "<div style='font-size:0.78rem;font-weight:700;"
        "color:#1a56db;letter-spacing:.06em;"
        "text-transform:uppercase;margin-bottom:8px'>"
        "Positive examples</div>",
        unsafe_allow_html=True
    )
    st.markdown("""
    <div class='example-box'>
    "This was one of the most brilliant films I have ever watched.
    The acting was outstanding, the story compelling from start to finish,
    and the direction masterful. I left feeling genuinely moved and uplifted."
    </div>
    <div class='example-box'>
    "An absolute masterpiece of modern cinema. Every scene was crafted
    with care and the performances were breathtaking. Highly recommended
    to anyone who appreciates great storytelling."
    </div>
    """, unsafe_allow_html=True)

    st.markdown(
        "<div style='font-size:0.78rem;font-weight:700;"
        "color:#dc2626;letter-spacing:.06em;"
        "text-transform:uppercase;margin:12px 0 8px'>"
        "Negative examples</div>",
        unsafe_allow_html=True
    )
    st.markdown("""
    <div class='example-box' style='border-left-color:#dc2626'>
    "This was one of the worst films I have ever had the misfortune
    of watching. The acting was atrocious, the story made no sense,
    and every scene was painful to sit through."
    </div>
    <div class='example-box' style='border-left-color:#dc2626'>
    "A complete waste of time. Terrible script, dreadful pacing,
    and performances so wooden they were painful to watch.
    I walked out after the first hour."
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
                        help="0.0 = strongly negative → 1.0 = strongly positive"
                    )
                with m3:
                    st.metric(label="WORD COUNT", value=word_count)

                # confidence bar
                st.markdown(
                    "<div style='margin-top:16px;font-size:0.8rem;"
                    "font-weight:600;color:#475569;"
                    "margin-bottom:6px'>Confidence level</div>",
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
                    <strong style='color:#1e293b'>
                        How to read this result
                    </strong><br><br>
                    📊  Score <code>{score:.3f}</code> means the model
                    assigns a <strong>{score*100:.1f}%</strong> probability
                    that this review is positive<br>
                    🎚  Threshold is <code>{threshold:.2f}</code> —
                    scores above this are labelled
                    <strong>POSITIVE</strong><br>
                    🔍  {verdict}
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