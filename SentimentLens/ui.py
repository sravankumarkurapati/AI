# ── ui.py — SentimentLens ──────────────────────────────────────────────

import streamlit as st
import requests
import os

st.set_page_config(
    page_title="SentimentLens",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
    #MainMenu { visibility: hidden; }
    header { visibility: hidden; }
    footer { visibility: hidden; }
    [data-testid="stToolbar"] { display: none; }

    /* sidebar — navy */
    section[data-testid="stSidebar"] {
        background-color: #1e3a5f !important;
        min-width: 280px !important;
        max-width: 280px !important;
    }
    section[data-testid="stSidebar"] * {
        color: #ffffff !important;
    }
    section[data-testid="stSidebar"] hr {
        border-color: rgba(255,255,255,0.15) !important;
    }

    /* main area */
    .stApp { background: #f8fafc; }
    .main .block-container {
        padding: 2rem 2.5rem 2rem 2.5rem !important;
        max-width: 860px !important;
    }

    /* text area */
    .stTextArea textarea {
        background: #ffffff !important;
        border: 1.5px solid #cbd5e1 !important;
        border-radius: 10px !important;
        color: #0f172a !important;
        font-size: 0.93rem !important;
        line-height: 1.7 !important;
        padding: 12px 14px !important;
    }
    .stTextArea textarea:focus {
        border-color: #1d4ed8 !important;
        box-shadow: 0 0 0 3px rgba(29,78,216,0.08) !important;
    }
    .stTextArea textarea::placeholder { color: #94a3b8 !important; }

    /* button */
    div[data-testid="stButton"] button {
        background: linear-gradient(135deg,#1d4ed8,#1e40af) !important;
        color: #ffffff !important;
        border: none !important;
        border-radius: 10px !important;
        font-size: 0.95rem !important;
        font-weight: 600 !important;
        padding: 0.65rem 1.5rem !important;
        box-shadow: 0 3px 12px rgba(29,78,216,0.3) !important;
        width: 100% !important;
        margin-top: 8px !important;
    }
    div[data-testid="stButton"] button:hover {
        box-shadow: 0 5px 18px rgba(29,78,216,0.4) !important;
        transform: translateY(-1px) !important;
    }

    /* result cards */
    .res-pos {
        background: #f0fdf4; border: 1px solid #86efac;
        border-left: 5px solid #16a34a; border-radius: 12px;
        padding: 16px 20px; margin-top: 16px;
    }
    .res-neg {
        background: #fff1f2; border: 1px solid #fecdd3;
        border-left: 5px solid #dc2626; border-radius: 12px;
        padding: 16px 20px; margin-top: 16px;
    }
    .res-label-pos { font-size:1.5rem; font-weight:800; color:#15803d; margin:0 0 2px; }
    .res-label-neg { font-size:1.5rem; font-weight:800; color:#b91c1c; margin:0 0 2px; }
    .res-desc { font-size:0.85rem; color:#374151; margin:0; }

    /* metrics */
    div[data-testid="metric-container"] {
        background: #ffffff !important;
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
    div[data-testid="metric-container"] div[data-testid="stMetricValue"] {
        color: #0f172a !important;
        font-size: 1.4rem !important;
        font-weight: 700 !important;
    }

    /* progress */
    div[data-testid="stProgress"] > div {
        background: #e2e8f0 !important; border-radius: 8px !important; height: 7px !important;
    }
    div[data-testid="stProgress"] > div > div {
        background: linear-gradient(90deg,#1d4ed8,#3b82f6) !important;
        border-radius: 8px !important;
    }

    /* score box */
    .score-box {
        background: #f8fafc; border: 1px solid #e2e8f0;
        border-radius: 10px; padding: 12px 16px; margin-top: 12px;
        font-size: 0.84rem; color: #374151; line-height: 1.9;
    }
    .score-box strong { color: #0f172a; }
    .score-box code {
        background: #e0e7ff; color: #1d4ed8;
        padding: 1px 5px; border-radius: 4px; font-size: 0.8rem;
    }

    /* expander */
    details {
        background: #ffffff !important; border: 1px solid #e2e8f0 !important;
        border-radius: 10px !important; margin-top: 10px !important;
    }
    details summary {
        font-size: 0.83rem !important; font-weight: 600 !important;
        color: #1d4ed8 !important; padding: 10px 14px !important;
    }

    /* example boxes */
    .ex-pos {
        background:#f0fdf4; border-left:4px solid #16a34a;
        border-radius:0 8px 8px 0; padding:9px 13px;
        font-size:0.82rem; color:#374151; font-style:italic;
        line-height:1.6; margin:5px 0;
    }
    .ex-neg {
        background:#fff1f2; border-left:4px solid #dc2626;
        border-radius:0 8px 8px 0; padding:9px 13px;
        font-size:0.82rem; color:#374151; font-style:italic;
        line-height:1.6; margin:5px 0;
    }

    /* divider */
    hr { border-color: #e2e8f0 !important; }

    /* slider label */
    div[data-testid="stSlider"] label { color: #374151 !important; font-size:0.82rem !important; }
    div[data-testid="stSlider"] div[data-testid="stTickBarMin"],
    div[data-testid="stSlider"] div[data-testid="stTickBarMax"] { color:#64748b !important; }

    /* footer */
    .footer {
        text-align:center; color:#94a3b8; font-size:0.74rem;
        margin-top:20px; padding-top:14px; border-top:1px solid #f1f5f9;
        line-height:1.7;
    }
    .footer a { color:#94a3b8; text-decoration:none; }

    /* alerts */
    div[data-testid="stAlert"] { border-radius:10px !important; font-size:0.84rem !important; }
</style>
""", unsafe_allow_html=True)

API_URL = os.getenv("API_URL", "http://127.0.0.1:8000")

# ══════════════════════════════════════════════════
# SIDEBAR — left pane
# ══════════════════════════════════════════════════
with st.sidebar:

    st.markdown("""
    <div style="padding:4px 0 16px">
        <div style="font-size:1.3rem;font-weight:800;color:#ffffff;
                    letter-spacing:-0.01em;">
            🎬 Sentiment<span style="color:#60a5fa">Lens</span>
        </div>
        <div style="font-size:0.75rem;color:#93c5fd;
                    line-height:1.5;margin-top:4px;">
            AI-powered movie review<br>sentiment analysis
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")

    # model details
    st.markdown(
        "<p style='font-size:0.62rem;font-weight:700;color:#60a5fa;"
        "letter-spacing:0.1em;text-transform:uppercase;"
        "margin-bottom:10px;'>Model Details</p>",
        unsafe_allow_html=True
    )

    details = [
        ("🏗", "Architecture", "LSTM"),
        ("📊", "Dataset", "IMDB 25k"),
        ("🎯", "Accuracy", "83.54%"),
        ("📖", "Vocabulary", "10,000 words"),
        ("⚖️", "Parameters", "1.3M weights"),
    ]
    for icon, key, val in details:
        st.markdown(
            f"<div style='display:flex;justify-content:space-between;"
            f"align-items:center;padding:5px 0;"
            f"border-bottom:1px solid rgba(255,255,255,0.07)'>"
            f"<span style='font-size:0.76rem;color:#94a3b8;'>{icon} {key}</span>"
            f"<span style='font-size:0.76rem;font-weight:600;"
            f"color:#ffffff;'>{val}</span></div>",
            unsafe_allow_html=True
        )

    st.markdown("---")

    # tech stack
    st.markdown(
        "<p style='font-size:0.62rem;font-weight:700;color:#60a5fa;"
        "letter-spacing:0.1em;text-transform:uppercase;"
        "margin-bottom:10px;'>Tech Stack</p>",
        unsafe_allow_html=True
    )
    chips = ["TensorFlow","Keras LSTM","FastAPI",
             "Streamlit","Docker","AWS EC2","Python"]
    chip_html = "".join([
        f"<span style='font-size:0.66rem;font-weight:600;"
        f"padding:3px 9px;border-radius:10px;"
        f"background:rgba(96,165,250,0.15);"
        f"border:1px solid rgba(96,165,250,0.3);"
        f"color:#93c5fd;margin:2px;display:inline-block;'>{c}</span>"
        for c in chips
    ])
    st.markdown(
        f"<div style='display:flex;flex-wrap:wrap;gap:3px'>{chip_html}</div>",
        unsafe_allow_html=True
    )

    st.markdown("---")

    # built by
    st.markdown(
        "<p style='font-size:0.62rem;font-weight:700;color:#60a5fa;"
        "letter-spacing:0.1em;text-transform:uppercase;"
        "margin-bottom:10px;'>Built By</p>",
        unsafe_allow_html=True
    )
    st.markdown(
        "<p style='font-size:0.88rem;font-weight:700;"
        "color:#ffffff;margin:0 0 3px;'>"
        "Sravan Kumar Kurapati</p>"
        "<p style='font-size:0.74rem;color:#94a3b8;"
        "line-height:1.7;margin:0;'>"
        "MS Information Systems<br>"
        "Northeastern University<br>"
        "Boston, MA</p>",
        unsafe_allow_html=True
    )

    st.markdown("---")

    # contact
    st.markdown(
        "<p style='font-size:0.62rem;font-weight:700;color:#60a5fa;"
        "letter-spacing:0.1em;text-transform:uppercase;"
        "margin-bottom:10px;'>Contact</p>",
        unsafe_allow_html=True
    )
    st.markdown(
        "<div style='display:flex;align-items:flex-start;"
        "gap:8px;margin-bottom:8px;'>"
        "<span style='font-size:13px;margin-top:1px;'>✉️</span>"
        "<a href='mailto:kurapati.sr@northeastern.edu' "
        "style='font-size:0.73rem;color:#60a5fa;"
        "text-decoration:none;line-height:1.5;word-break:break-all;'>"
        "kurapati.sr@northeastern.edu</a></div>"
        "<div style='display:flex;align-items:center;gap:8px;'>"
        "<span style='font-size:13px;'>📞</span>"
        "<span style='font-size:0.73rem;color:#94a3b8;'>"
        "+1-857-427-7767</span></div>",
        unsafe_allow_html=True
    )

# ══════════════════════════════════════════════════
# MAIN — right pane
# ══════════════════════════════════════════════════

# header
st.markdown(
    "<h2 style='font-size:1.6rem;font-weight:800;color:#0f172a;"
    "letter-spacing:-0.02em;margin:0 0 3px;'>🎬 SentimentLens</h2>"
    "<p style='font-size:0.85rem;color:#64748b;margin:0 0 12px;'>"
    "Real-time movie review sentiment analysis — "
    "powered by LSTM deep learning and deployed on AWS</p>",
    unsafe_allow_html=True
)

# badges
badges = ["LSTM", "NLP", "TENSORFLOW", "FASTAPI", "AWS EC2"]
badge_html = "".join([
    f"<span style='display:inline-block;background:#eff6ff;"
    f"border:1px solid #bfdbfe;color:#1d4ed8;"
    f"padding:2px 10px;border-radius:20px;"
    f"font-size:0.67rem;font-weight:700;"
    f"letter-spacing:0.06em;margin-right:4px;'>{b}</span>"
    for b in badges
])
st.markdown(badge_html, unsafe_allow_html=True)
st.markdown("---")

# threshold
threshold = st.slider(
    "Decision threshold",
    min_value=0.1, max_value=0.9,
    value=0.5, step=0.05,
    help="Scores ≥ threshold = POSITIVE. Below = NEGATIVE."
)

# input label
st.markdown(
    "<p style='font-size:0.7rem;font-weight:700;color:#1d4ed8;"
    "letter-spacing:0.08em;text-transform:uppercase;"
    "margin:14px 0 6px;'>Enter a movie review</p>",
    unsafe_allow_html=True
)

# text area
review_text = st.text_area(
    label="",
    placeholder="Type or paste any movie review here...\n"
                "Tip: longer reviews (20+ words) give more accurate results.",
    height=130,
    key="review_input"
)

# button
analyse_clicked = st.button("🔍  Analyse Sentiment")

# examples
with st.expander("📖  See example reviews"):
    st.markdown(
        "<p style='font-size:0.67rem;font-weight:700;color:#15803d;"
        "letter-spacing:0.07em;text-transform:uppercase;"
        "margin-bottom:5px;'>Positive</p>",
        unsafe_allow_html=True
    )
    st.markdown("""
    <div class='ex-pos'>
    "This was one of the most brilliant films I have ever watched.
    The acting was outstanding, the story compelling from start to finish,
    and the direction masterful. I left feeling genuinely moved."
    </div>
    """, unsafe_allow_html=True)

    st.markdown(
        "<p style='font-size:0.67rem;font-weight:700;color:#b91c1c;"
        "letter-spacing:0.07em;text-transform:uppercase;"
        "margin:8px 0 5px;'>Negative</p>",
        unsafe_allow_html=True
    )
    st.markdown("""
    <div class='ex-neg'>
    "This was one of the worst films I have ever watched. The acting was
    atrocious, the story made no sense, and every scene was painful
    to sit through. A complete waste of time."
    </div>
    """, unsafe_allow_html=True)

# ── prediction ──────────────────────────────────────────────────────────
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

                if label == "POSITIVE":
                    st.markdown("""
                    <div class='res-pos'>
                        <div class='res-label-pos'>👍 POSITIVE</div>
                        <div class='res-desc'>
                            The model detected positive sentiment in this review.
                        </div>
                    </div>""", unsafe_allow_html=True)
                else:
                    st.markdown("""
                    <div class='res-neg'>
                        <div class='res-label-neg'>👎 NEGATIVE</div>
                        <div class='res-desc'>
                            The model detected negative sentiment in this review.
                        </div>
                    </div>""", unsafe_allow_html=True)

                st.markdown(
                    "<div style='height:12px'></div>",
                    unsafe_allow_html=True
                )
                m1, m2, m3 = st.columns(3)
                with m1:
                    st.metric("CONFIDENCE", f"{confidence}%")
                with m2:
                    st.metric("RAW SCORE", f"{score:.3f}",
                              help="0.0 = strongly negative → 1.0 = strongly positive")
                with m3:
                    st.metric("WORD COUNT", word_count)

                st.markdown(
                    "<p style='font-size:0.78rem;font-weight:600;"
                    "color:#374151;margin:14px 0 6px;'>"
                    "Confidence level</p>",
                    unsafe_allow_html=True
                )
                st.progress(confidence / 100)

                if warning:
                    st.warning(f"⚠️  {warning}")

                verdict = (
                    "✅ Strong prediction — model is confident"
                    if confidence > 75
                    else "⚠️ Uncertain — try a longer review"
                )
                st.markdown(f"""
                <div class='score-box'>
                    <strong>How to read this result</strong><br><br>
                    📊 Score <code>{score:.3f}</code> — model assigns
                    <strong>{score*100:.1f}%</strong> probability
                    this review is positive<br>
                    🎚 Threshold <code>{threshold:.2f}</code> —
                    scores above this = <strong>POSITIVE</strong><br>
                    🔍 {verdict}
                </div>""", unsafe_allow_html=True)

            else:
                st.error(f"API error {response.status_code}: {response.text}")

        except requests.exceptions.ConnectionError:
            st.error("🔌 Cannot connect to the API. "
                     "Make sure FastAPI is running on port 8000.")
        except requests.exceptions.Timeout:
            st.error("⏱ Request timed out.")
        except Exception as e:
            st.error(f"Unexpected error: {str(e)}")

elif analyse_clicked and not review_text.strip():
    st.warning("Please enter a review before clicking Analyse.")

# footer
st.markdown("""
<div class='footer'>
    SentimentLens &nbsp;·&nbsp; LSTM + TensorFlow &nbsp;·&nbsp;
    FastAPI + Streamlit &nbsp;·&nbsp; Docker + AWS EC2<br>
    Sravan Kumar Kurapati &nbsp;·&nbsp;
    <a href='mailto:kurapati.sr@northeastern.edu'>
    kurapati.sr@northeastern.edu</a>
    &nbsp;·&nbsp; +1-857-427-7767
</div>
""", unsafe_allow_html=True)