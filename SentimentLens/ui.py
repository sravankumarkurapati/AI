# ── ui.py — SentimentLens Streamlit frontend ───────────────────────────

import streamlit as st
import requests
import os

st.set_page_config(
    page_title="SentimentLens",
    page_icon="🎬",
    layout="centered"
)

st.markdown("""
<style>
    .main { padding-top: 2rem; }
    .result-positive {
        background-color: #d4edda;
        border-left: 5px solid #28a745;
        padding: 16px 20px;
        border-radius: 8px;
        margin-top: 16px;
    }
    .result-negative {
        background-color: #f8d7da;
        border-left: 5px solid #dc3545;
        padding: 16px 20px;
        border-radius: 8px;
        margin-top: 16px;
    }
</style>
""", unsafe_allow_html=True)

API_URL = os.getenv("API_URL", "http://127.0.0.1:8000")

# ── FIX: initialise the text value in session state BEFORE the widget ──
# we use a separate key "review_text_value" to hold the text content
# the widget key "review_input" is only used by Streamlit internally
# when an example button is clicked we update "review_text_value"
# on the next rerun the widget reads from "review_text_value" as its value
if "review_text_value" not in st.session_state:
    st.session_state.review_text_value = ""

st.title("🎬 SentimentLens")
st.markdown("**Real-time movie review sentiment analysis** — powered by LSTM + TensorFlow")
st.markdown("---")

with st.sidebar:
    st.header("About")
    st.markdown("""
    **SentimentLens** classifies movie reviews as positive or negative using a deep learning model.

    **Model details:**
    - Architecture: LSTM
    - Training data: IMDB (25,000 reviews)
    - Test accuracy: 83.54%
    - Vocabulary: 10,000 words

    **Built with:**
    - TensorFlow / Keras
    - FastAPI
    - Streamlit
    - Deployed on AWS EC2
    """)
    st.markdown("---")
    threshold = st.slider(
        "Decision threshold",
        min_value=0.1,
        max_value=0.9,
        value=0.5,
        step=0.05,
        help="Score above this = POSITIVE. Below = NEGATIVE. Default 0.5."
    )

# ── example buttons BEFORE the text area ──────────────────────────────
# buttons must come before the widget so session state is set
# before st.text_area reads it
st.subheader("Enter a movie review")

st.markdown("**Or try an example:**")
ex_col1, ex_col2 = st.columns(2)

with ex_col1:
    if st.button("👍 Positive example"):
        # update the value key — NOT the widget key
        st.session_state.review_text_value = (
            "This was one of the most brilliant films I have ever had "
            "the pleasure of watching. The acting was outstanding, the "
            "story was compelling from start to finish, and the direction "
            "was masterful. I left feeling genuinely moved and uplifted."
        )

with ex_col2:
    if st.button("👎 Negative example"):
        st.session_state.review_text_value = (
            "This was one of the worst films I have ever had the "
            "misfortune of watching. The acting was atrocious, the story "
            "made no sense, and every scene was painful to sit through. "
            "A complete waste of time and money."
        )

# ── text area reads from review_text_value ─────────────────────────────
# value= parameter pre-fills the box with whatever is in session state
# when an example button sets review_text_value, this box shows it
review_text = st.text_area(
    label="",
    placeholder="e.g. This movie was absolutely brilliant...",
    height=150,
    value=st.session_state.review_text_value,
    key="review_input"
)

# sync typed text back to review_text_value
# so the box does not reset when the analyse button is clicked
st.session_state.review_text_value = review_text

# ── analyse button ─────────────────────────────────────────────────────
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    analyse_clicked = st.button(
        "🔍 Analyse Sentiment",
        use_container_width=True
    )

# ── prediction ─────────────────────────────────────────────────────────
if analyse_clicked and review_text.strip():
    with st.spinner("Analysing..."):
        try:
            response = requests.post(
                f"{API_URL}/predict",
                json={"review": review_text},
                params={"threshold": threshold},
                timeout=10
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
                    <div class="result-positive">
                        <h2 style="color:#28a745; margin:0">👍 POSITIVE</h2>
                        <p style="margin:4px 0 0; color:#155724">
                            The model detected positive sentiment
                        </p>
                    </div>
                    """, unsafe_allow_html=True)
                else:
                    st.markdown("""
                    <div class="result-negative">
                        <h2 style="color:#dc3545; margin:0">👎 NEGATIVE</h2>
                        <p style="margin:4px 0 0; color:#721c24">
                            The model detected negative sentiment
                        </p>
                    </div>
                    """, unsafe_allow_html=True)

                st.markdown("<br>", unsafe_allow_html=True)
                m1, m2, m3 = st.columns(3)
                with m1:
                    st.metric(label="Confidence", value=f"{confidence}%")
                with m2:
                    st.metric(label="Raw score", value=f"{score:.3f}",
                              help="0.0 = very negative, 1.0 = very positive")
                with m3:
                    st.metric(label="Word count", value=word_count)

                st.markdown("**Confidence level:**")
                st.progress(confidence / 100)

                if warning:
                    st.warning(warning)

                st.markdown("---")
                st.markdown("**How to read the score:**")
                st.markdown(f"""
                - Score `{score:.3f}` means the model assigns a
                  **{score*100:.1f}% probability** that this review is positive
                - Threshold is set to `{threshold}` —
                  scores above this are called POSITIVE
                - {'✅ Clear prediction — model is confident' if confidence > 75
                   else '⚠️ Uncertain prediction — consider a longer review'}
                """)

            else:
                st.error(f"API error {response.status_code}: {response.text}")

        except requests.exceptions.ConnectionError:
            st.error(
                "Cannot connect to the API. "
                "Make sure FastAPI is running: `uvicorn app:app --reload`"
            )
        except requests.exceptions.Timeout:
            st.error("Request timed out. The API took too long to respond.")

elif analyse_clicked and not review_text.strip():
    st.warning("Please enter a review before clicking Analyse.")

st.markdown("---")
st.markdown(
    "<div style='text-align:center; color:#999; font-size:12px'>"
    "SentimentLens — Built with TensorFlow, FastAPI and Streamlit — "
    "Deployed on AWS EC2"
    "</div>",
    unsafe_allow_html=True
)