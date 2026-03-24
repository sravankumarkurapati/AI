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

    section[data-testid="stSidebar"] {
        background-color: #1e3a5f !important;
        min-width: 260px !important;
        max-width: 260px !important;
    }
    section[data-testid="stSidebar"] p,
    section[data-testid="stSidebar"] span,
    section[data-testid="stSidebar"] div,
    section[data-testid="stSidebar"] a,
    section[data-testid="stSidebar"] label {
        color: #ffffff !important;
    }
    section[data-testid="stSidebar"] hr {
        border-color: rgba(255,255,255,0.15) !important;
        margin: 8px 0 !important;
    }

    .stApp { background: #ffffff; }
    .main .block-container {
        padding: 0.6rem 1.8rem !important;
        max-width: 800px !important;
    }

    .stTextArea textarea {
        background: #f8fafc !important;
        border: 1.5px solid #cbd5e1 !important;
        border-radius: 10px !important;
        color: #0f172a !important;
        font-size: 0.93rem !important;
        line-height: 1.6 !important;
        padding: 10px 13px !important;
    }
    .stTextArea textarea:focus {
        border-color: #1d4ed8 !important;
        box-shadow: 0 0 0 3px rgba(29,78,216,0.08) !important;
        background: #ffffff !important;
    }
    .stTextArea textarea::placeholder { color: #94a3b8 !important; }

    div[data-testid="stButton"] button {
        background: linear-gradient(135deg,#1d4ed8,#1e40af) !important;
        color: #ffffff !important;
        border: none !important;
        border-radius: 10px !important;
        font-size: 0.93rem !important;
        font-weight: 600 !important;
        padding: 0.55rem 1.5rem !important;
        box-shadow: 0 3px 12px rgba(29,78,216,0.25) !important;
        width: 100% !important;
        margin-top: 6px !important;
    }
    div[data-testid="stButton"] button:hover {
        box-shadow: 0 5px 18px rgba(29,78,216,0.4) !important;
        transform: translateY(-1px) !important;
    }

    .res-pos {
        background: #f0fdf4;
        border: 1.5px solid #86efac;
        border-left: 6px solid #16a34a;
        border-radius: 12px;
        padding: 14px 20px;
        margin-top: 12px;
    }
    .res-neg {
        background: #fff1f2;
        border: 1.5px solid #fecdd3;
        border-left: 6px solid #dc2626;
        border-radius: 12px;
        padding: 14px 20px;
        margin-top: 12px;
    }
    .res-title-pos {
        font-size: 1.4rem;
        font-weight: 800;
        color: #15803d;
        margin: 0 0 3px;
    }
    .res-title-neg {
        font-size: 1.4rem;
        font-weight: 800;
        color: #b91c1c;
        margin: 0 0 3px;
    }
    .res-row {
        display: flex;
        gap: 22px;
        margin-top: 8px;
        flex-wrap: wrap;
    }
    .res-stat { display: flex; flex-direction: column; }
    .res-stat-label {
        font-size: 0.65rem;
        font-weight: 700;
        color: #64748b;
        letter-spacing: 0.07em;
        text-transform: uppercase;
        margin-bottom: 1px;
    }
    .res-stat-value {
        font-size: 1.15rem;
        font-weight: 700;
        color: #0f172a;
    }
    .res-bar-wrap { margin-top: 10px; }
    .res-bar-label {
        font-size: 0.72rem;
        color: #475569;
        font-weight: 600;
        margin-bottom: 4px;
    }
    .res-bar-track {
        background: #e2e8f0;
        border-radius: 6px;
        height: 7px;
        overflow: hidden;
    }
    .res-bar-fill-pos {
        height: 100%;
        border-radius: 6px;
        background: linear-gradient(90deg,#16a34a,#22c55e);
    }
    .res-bar-fill-neg {
        height: 100%;
        border-radius: 6px;
        background: linear-gradient(90deg,#dc2626,#ef4444);
    }

    .ex-pos {
        background: #f0fdf4;
        border-left: 4px solid #16a34a;
        border-radius: 0 8px 8px 0;
        padding: 8px 12px;
        font-size: 0.81rem;
        color: #1e293b;
        font-style: italic;
        line-height: 1.6;
        margin: 4px 0;
    }
    .ex-neg {
        background: #fff1f2;
        border-left: 4px solid #dc2626;
        border-radius: 0 8px 8px 0;
        padding: 8px 12px;
        font-size: 0.81rem;
        color: #1e293b;
        font-style: italic;
        line-height: 1.6;
        margin: 4px 0;
    }

    details {
        background: #f8fafc !important;
        border: 1px solid #e2e8f0 !important;
        border-radius: 10px !important;
        margin-top: 8px !important;
    }
    details summary {
        font-size: 0.81rem !important;
        font-weight: 600 !important;
        color: #1d4ed8 !important;
        padding: 8px 13px !important;
        cursor: pointer !important;
    }

    hr { border-color: #f1f5f9 !important; margin: 8px 0 !important; }

    .footer {
        text-align: center;
        color: #94a3b8;
        font-size: 0.72rem;
        margin-top: 14px;
        padding-top: 10px;
        border-top: 1px solid #f1f5f9;
        line-height: 1.7;
    }
    .footer a { color: #94a3b8; text-decoration: none; }

    div[data-testid="stAlert"] {
        border-radius: 10px !important;
        font-size: 0.83rem !important;
    }
</style>
""", unsafe_allow_html=True)

API_URL = os.getenv("API_URL", "http://127.0.0.1:8000")

# ══════════════════════════════════════════════════
# SIDEBAR
# ══════════════════════════════════════════════════
with st.sidebar:

    st.markdown(
        "<div style='padding:4px 0 12px'>"
        "<div style='font-size:1.2rem;font-weight:800;color:#ffffff;"
        "letter-spacing:-0.01em;'>🎬 Sentiment"
        "<span style='color:#60a5fa'>Lens</span></div>"
        "<div style='font-size:0.73rem;color:#93c5fd;"
        "line-height:1.5;margin-top:4px;'>"
        "AI-powered movie review<br>sentiment analysis</div></div>",
        unsafe_allow_html=True
    )

    st.markdown("---")

    st.markdown(
        "<div style='font-size:0.6rem;font-weight:700;color:#60a5fa;"
        "letter-spacing:0.1em;text-transform:uppercase;"
        "margin-bottom:8px;'>Model Details</div>",
        unsafe_allow_html=True
    )
    for icon, k, v, is_acc in [
        ("🏗", "Architecture", "LSTM",         False),
        ("📊", "Dataset",      "IMDB 25k",     False),
        ("🎯", "Accuracy",     "83.54%",       True),
        ("📖", "Vocabulary",   "10,000 words", False),
        ("⚖️", "Parameters",   "1.3M weights", False),
    ]:
        val_style = (
            "color:#93c5fd;background:rgba(96,165,250,0.15);"
            "border:1px solid rgba(96,165,250,0.3);"
            "padding:1px 7px;border-radius:5px;"
            if is_acc else "color:#ffffff;"
        )
        st.markdown(
            f"<div style='display:flex;justify-content:space-between;"
            f"align-items:center;padding:4px 0;"
            f"border-bottom:1px solid rgba(255,255,255,0.06);'>"
            f"<span style='font-size:0.74rem;color:#94a3b8;'>"
            f"{icon} {k}</span>"
            f"<span style='font-size:0.74rem;font-weight:600;{val_style}'>"
            f"{v}</span></div>",
            unsafe_allow_html=True
        )

    st.markdown("---")

    st.markdown(
        "<div style='font-size:0.6rem;font-weight:700;color:#60a5fa;"
        "letter-spacing:0.1em;text-transform:uppercase;"
        "margin-bottom:8px;'>Tech Stack</div>",
        unsafe_allow_html=True
    )
    # chips wrap naturally — 2-3 per row depending on sidebar width
    chips_html = "".join([
        f"<span style='display:inline-block;font-size:0.64rem;"
        f"font-weight:600;padding:3px 8px;border-radius:10px;"
        f"background:rgba(96,165,250,0.12);"
        f"border:1px solid rgba(96,165,250,0.28);"
        f"color:#93c5fd;margin:2px 2px;'>{c}</span>"
        for c in ["TensorFlow","Keras LSTM","FastAPI",
                  "Streamlit","Docker","AWS EC2","Python"]
    ])
    st.markdown(
        f"<div style='line-height:2;'>{chips_html}</div>",
        unsafe_allow_html=True
    )

    st.markdown("---")

    st.markdown(
        "<div style='font-size:0.6rem;font-weight:700;color:#60a5fa;"
        "letter-spacing:0.1em;text-transform:uppercase;"
        "margin-bottom:8px;'>Built By</div>"
        "<div style='font-size:0.86rem;font-weight:700;"
        "color:#ffffff;margin-bottom:2px;'>"
        "Sravan Kumar Kurapati</div>"
        "<div style='font-size:0.72rem;color:#94a3b8;line-height:1.6;'>"
        "MS Information Systems<br>"
        "Northeastern University<br>"
        "Boston, MA</div>",
        unsafe_allow_html=True
    )

    st.markdown("---")

    st.markdown(
        "<div style='font-size:0.6rem;font-weight:700;color:#60a5fa;"
        "letter-spacing:0.1em;text-transform:uppercase;"
        "margin-bottom:8px;'>Contact</div>"
        "<div style='display:flex;align-items:flex-start;"
        "gap:7px;margin-bottom:7px;'>"
        "<span style='font-size:12px;margin-top:2px;flex-shrink:0;'>✉️</span>"
        "<a href='mailto:kurapati.sr@northeastern.edu' "
        "style='font-size:0.71rem;color:#60a5fa;text-decoration:none;"
        "word-break:break-all;line-height:1.5;'>"
        "kurapati.sr@northeastern.edu</a></div>"
        "<div style='display:flex;align-items:center;gap:7px;'>"
        "<span style='font-size:12px;flex-shrink:0;'>📞</span>"
        "<span style='font-size:0.71rem;color:#94a3b8;'>"
        "+1-857-427-7767</span></div>",
        unsafe_allow_html=True
    )

# ══════════════════════════════════════════════════
# MAIN
# ══════════════════════════════════════════════════

st.markdown(
    "<h1 style='font-size:1.4rem;font-weight:800;color:#0f172a;"
    "letter-spacing:-0.02em;margin:0 0 2px;'>"
    "🎬 SentimentLens</h1>"
    "<p style='font-size:0.83rem;color:#64748b;margin:0 0 8px;'>"
    "Real-time movie review sentiment analysis — "
    "powered by LSTM deep learning</p>",
    unsafe_allow_html=True
)

st.markdown(
    " ".join([
        f"<span style='display:inline-block;background:#eff6ff;"
        f"border:1px solid #bfdbfe;color:#1d4ed8;"
        f"padding:2px 9px;border-radius:20px;"
        f"font-size:0.66rem;font-weight:700;"
        f"letter-spacing:0.06em;'>{b}</span>"
        for b in ["LSTM","NLP","TENSORFLOW","FASTAPI","AWS EC2"]
    ]),
    unsafe_allow_html=True
)

st.markdown(
    "<hr style='border-color:#f1f5f9;margin:8px 0;'>",
    unsafe_allow_html=True
)

st.markdown(
    "<p style='font-size:0.68rem;font-weight:700;color:#1d4ed8;"
    "letter-spacing:0.08em;text-transform:uppercase;"
    "margin:0 0 5px;'>Enter a movie review</p>",
    unsafe_allow_html=True
)

review_text = st.text_area(
    label="",
    placeholder="Type or paste any movie review here...\n"
                "Tip: longer reviews give more accurate results.",
    height=100,
    key="review_input"
)

analyse_clicked = st.button("🔍  Analyse Sentiment")

with st.expander("📖  See example reviews"):
    st.markdown(
        "<p style='font-size:0.66rem;font-weight:700;color:#15803d;"
        "letter-spacing:0.07em;text-transform:uppercase;"
        "margin:0 0 4px;'>Positive</p>",
        unsafe_allow_html=True
    )
    st.markdown(
        "<div class='ex-pos'>"
        "\"This was one of the most brilliant films I have ever watched. "
        "The acting was outstanding, the story compelling from start to "
        "finish, and the direction masterful.\"</div>",
        unsafe_allow_html=True
    )
    st.markdown(
        "<p style='font-size:0.66rem;font-weight:700;color:#b91c1c;"
        "letter-spacing:0.07em;text-transform:uppercase;"
        "margin:7px 0 4px;'>Negative</p>",
        unsafe_allow_html=True
    )
    st.markdown(
        "<div class='ex-neg'>"
        "\"This was one of the worst films I have ever watched. "
        "The acting was atrocious, the story made no sense, "
        "and every scene was painful to sit through.\"</div>",
        unsafe_allow_html=True
    )

# ── prediction ──────────────────────────────────────────────────────────
if analyse_clicked and review_text.strip():
    with st.spinner("Analysing..."):
        try:
            response = requests.post(
                f"{API_URL}/predict",
                json={"review": review_text},
                timeout=15
            )

            if response.status_code == 200:
                result     = response.json()
                label      = result["label"]
                score      = result["score"]
                confidence = result["confidence"]
                word_count = result["word_count"]
                bar_w      = f"{confidence}%"
                verdict    = (
                    "✅ Strong prediction"
                    if confidence > 75
                    else "⚠️ Low confidence — try a longer review"
                )

                if label == "POSITIVE":
                    st.markdown(f"""
                    <div class='res-pos'>
                        <div class='res-title-pos'>👍 POSITIVE</div>
                        <div style='font-size:0.83rem;color:#374151;
                                    margin-bottom:8px;'>
                            The model detected positive sentiment.
                        </div>
                        <div class='res-row'>
                            <div class='res-stat'>
                                <div class='res-stat-label'>Confidence</div>
                                <div class='res-stat-value'
                                style='color:#15803d;'>{confidence}%</div>
                            </div>
                            <div class='res-stat'>
                                <div class='res-stat-label'>Score</div>
                                <div class='res-stat-value'>{score:.3f}</div>
                            </div>
                            <div class='res-stat'>
                                <div class='res-stat-label'>Words</div>
                                <div class='res-stat-value'>{word_count}</div>
                            </div>
                        </div>
                        <div class='res-bar-wrap'>
                            <div class='res-bar-label'>Confidence level</div>
                            <div class='res-bar-track'>
                                <div class='res-bar-fill-pos'
                                style='width:{bar_w}'></div>
                            </div>
                        </div>
                    </div>
                    <p style='font-size:0.78rem;color:#64748b;
                              margin-top:8px;'>{verdict}
                    &nbsp;·&nbsp; Score {score:.3f} / 1.0
                    &nbsp;·&nbsp; ≥ 0.5 = POSITIVE</p>
                    """, unsafe_allow_html=True)

                else:
                    st.markdown(f"""
                    <div class='res-neg'>
                        <div class='res-title-neg'>👎 NEGATIVE</div>
                        <div style='font-size:0.83rem;color:#374151;
                                    margin-bottom:8px;'>
                            The model detected negative sentiment.
                        </div>
                        <div class='res-row'>
                            <div class='res-stat'>
                                <div class='res-stat-label'>Confidence</div>
                                <div class='res-stat-value'
                                style='color:#b91c1c;'>{confidence}%</div>
                            </div>
                            <div class='res-stat'>
                                <div class='res-stat-label'>Score</div>
                                <div class='res-stat-value'>{score:.3f}</div>
                            </div>
                            <div class='res-stat'>
                                <div class='res-stat-label'>Words</div>
                                <div class='res-stat-value'>{word_count}</div>
                            </div>
                        </div>
                        <div class='res-bar-wrap'>
                            <div class='res-bar-label'>Confidence level</div>
                            <div class='res-bar-track'>
                                <div class='res-bar-fill-neg'
                                style='width:{bar_w}'></div>
                            </div>
                        </div>
                    </div>
                    <p style='font-size:0.78rem;color:#64748b;
                              margin-top:8px;'>{verdict}
                    &nbsp;·&nbsp; Score {score:.3f} / 1.0
                    &nbsp;·&nbsp; &lt; 0.5 = NEGATIVE</p>
                    """, unsafe_allow_html=True)

            else:
                st.error(f"API error {response.status_code}: {response.text}")

        except requests.exceptions.ConnectionError:
            st.error("🔌 Cannot connect to the API on port 8000.")
        except requests.exceptions.Timeout:
            st.error("⏱ Request timed out.")
        except Exception as e:
            st.error(f"Error: {str(e)}")

elif analyse_clicked and not review_text.strip():
    st.warning("Please enter a review first.")

st.markdown(
    "<div class='footer'>"
    "SentimentLens &nbsp;·&nbsp; LSTM + TensorFlow &nbsp;·&nbsp; "
    "FastAPI + Streamlit &nbsp;·&nbsp; Docker + AWS EC2<br>"
    "Sravan Kumar Kurapati &nbsp;·&nbsp; "
    "<a href='mailto:kurapati.sr@northeastern.edu'>"
    "kurapati.sr@northeastern.edu</a>"
    " &nbsp;·&nbsp; +1-857-427-7767"
    "</div>",
    unsafe_allow_html=True
)