# ── ui.py — SentimentLens Streamlit frontend ───────────────────────────

import streamlit as st
import requests
import json

# ── page config — must be the first streamlit command ─────────────────
st.set_page_config(
    page_title="SentimentLens",
    page_icon="🎬",
    layout="centered"       # center everything on the page
)

# ── custom CSS — small style tweaks ───────────────────────────────────
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
    .metric-label {
        font-size: 13px;
        color: #666;
    }
</style>
""", unsafe_allow_html=True)

# ── FastAPI URL — points to our backend ───────────────────────────────
# when running locally:  http://localhost:8000
# when deployed on AWS:  http://<your-ec2-ip>:8000
# we use an environment variable so we can change it without editing code
import os
API_URL = os.getenv("API_URL", "http://127.0.0.1:8000")

# ── page header ────────────────────────────────────────────────────────
st.title("🎬 SentimentLens")
st.markdown("**Real-time movie review sentiment analysis** — powered by LSTM + TensorFlow")
st.markdown("---")

# ── sidebar — about section ────────────────────────────────────────────
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

    # threshold slider — lets user adjust sensitivity
    threshold = st.slider(
        "Decision threshold",
        min_value=0.1,
        max_value=0.9,
        value=0.5,
        step=0.05,
        help="Score above this = POSITIVE. Below = NEGATIVE. Default 0.5."
    )
    # this lets the user control how sensitive the model is
    # lower threshold = model more easily calls things positive
    # higher threshold = model needs stronger signal to call positive

# ── main input area ────────────────────────────────────────────────────
st.subheader("Enter a movie review")

review_text = st.text_area(
    label="",                           # no label — title above is enough
    placeholder="e.g. This movie was absolutely brilliant. "
                "The acting was superb and the story kept me hooked "
                "from start to finish. Highly recommended.",
    height=150,                         # text box height in pixels
    key="review_input"
)

# ── analyse button ─────────────────────────────────────────────────────
col1, col2, col3 = st.columns([1, 2, 1])
# columns let us center the button
# col1 and col3 are empty spacers, col2 holds the button

with col2:
    analyse_clicked = st.button(
        "🔍 Analyse Sentiment",
        use_container_width=True    # button stretches to column width
    )

# ── example reviews — quick test buttons ──────────────────────────────
st.markdown("**Or try an example:**")
ex_col1, ex_col2 = st.columns(2)

with ex_col1:
    if st.button("👍 Positive example"):
        # clicking this fills the text area with a positive review
        st.session_state.review_input = (
            "This was one of the most brilliant films I have ever had "
            "the pleasure of watching. The acting was outstanding, the "
            "story was compelling from start to finish, and the direction "
            "was masterful. I left feeling genuinely moved and uplifted."
        )
        st.rerun()      # re-run the app to update the text area

with ex_col2:
    if st.button("👎 Negative example"):
        st.session_state.review_input = (
            "This was one of the worst films I have ever had the "
            "misfortune of watching. The acting was atrocious, the story "
            "made no sense, and every scene was painful to sit through. "
            "A complete waste of time and money."
        )
        st.rerun()

# ── run prediction when button is clicked ─────────────────────────────
if analyse_clicked and review_text.strip():

    # show a spinner while the API call is in progress
    with st.spinner("Analysing..."):
        try:
            # call our FastAPI backend
            response = requests.post(
                f"{API_URL}/predict",
                json={"review": review_text},
                # pass threshold as a query parameter
                params={"threshold": threshold},
                timeout=10      # give up after 10 seconds
            )
            # timeout=10 prevents the UI hanging forever if the API is down

            if response.status_code == 200:
                result = response.json()
                # result = {
                #   "label": "POSITIVE",
                #   "score": 0.93,
                #   "confidence": 93.0,
                #   "word_count": 45,
                #   "warning": null
                # }

                # ── display the result ─────────────────────────────────
                label      = result["label"]
                score      = result["score"]
                confidence = result["confidence"]
                word_count = result["word_count"]
                warning    = result.get("warning")

                # choose styling based on label
                if label == "POSITIVE":
                    st.markdown(f"""
                    <div class="result-positive">
                        <h2 style="color:#28a745; margin:0">👍 POSITIVE</h2>
                        <p style="margin:4px 0 0; color:#155724">
                            The model detected positive sentiment
                        </p>
                    </div>
                    """, unsafe_allow_html=True)
                else:
                    st.markdown(f"""
                    <div class="result-negative">
                        <h2 style="color:#dc3545; margin:0">👎 NEGATIVE</h2>
                        <p style="margin:4px 0 0; color:#721c24">
                            The model detected negative sentiment
                        </p>
                    </div>
                    """, unsafe_allow_html=True)

                # ── metric cards ───────────────────────────────────────
                st.markdown("<br>", unsafe_allow_html=True)
                m1, m2, m3 = st.columns(3)

                with m1:
                    st.metric(
                        label="Confidence",
                        value=f"{confidence}%"
                        # st.metric shows a bold number with a label above
                    )
                with m2:
                    st.metric(
                        label="Raw score",
                        value=f"{score:.3f}",
                        help="0.0 = very negative, 1.0 = very positive"
                    )
                with m3:
                    st.metric(
                        label="Word count",
                        value=word_count
                    )

                # ── confidence progress bar ────────────────────────────
                st.markdown("**Confidence level:**")
                st.progress(confidence / 100)
                # progress bar from 0.0 to 1.0
                # we divide by 100 since confidence is 0–100

                # ── show warning if input was short ────────────────────
                if warning:
                    st.warning(warning)

                # ── score interpretation ───────────────────────────────
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
                # API returned an error
                st.error(f"API error {response.status_code}: {response.text}")

        except requests.exceptions.ConnectionError:
            # FastAPI is not running
            st.error(
                "Cannot connect to the API. "
                "Make sure FastAPI is running: `uvicorn app:app --reload`"
            )
        except requests.exceptions.Timeout:
            st.error("Request timed out. The API took too long to respond.")

elif analyse_clicked and not review_text.strip():
    # button clicked but text box is empty
    st.warning("Please enter a review before clicking Analyse.")

# ── footer ─────────────────────────────────────────────────────────────
st.markdown("---")
st.markdown(
    "<div style='text-align:center; color:#999; font-size:12px'>"
    "SentimentLens — Built with TensorFlow, FastAPI and Streamlit — "
    "Deployed on AWS EC2"
    "</div>",
    unsafe_allow_html=True
)