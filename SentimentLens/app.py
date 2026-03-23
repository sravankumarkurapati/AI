# app.py — SentimentLens FastAPI backend

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from tensorflow.keras.preprocessing.sequence import pad_sequences
import tensorflow as tf
import numpy as np
import json
import os

# ── constants — must match Colab exactly ──────────────────────────────
VOCAB_SIZE = 10000
MAX_LEN    = 200

# ── file paths ─────────────────────────────────────────────────────────
BASE_DIR   = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(BASE_DIR, "model", "sentiment_model.keras")
VOCAB_PATH = os.path.join(BASE_DIR, "model", "word_index.json")

# ── load model and vocabulary at startup ──────────────────────────────
print("Loading model...")
model = tf.keras.models.load_model(MODEL_PATH)
print("Model loaded")

print("Loading vocabulary...")
with open(VOCAB_PATH, "r") as f:
    word_index = json.load(f)
print(f"Vocabulary loaded: {len(word_index)} words")

# ── create FastAPI app — this is what uvicorn looks for ───────────────
app = FastAPI(
    title="SentimentLens",
    description="Movie review sentiment classifier",
    version="1.0.0"
)

# ── request and response shapes ────────────────────────────────────────
class ReviewRequest(BaseModel):
    review: str

class PredictionResponse(BaseModel):
    label:      str
    score:      float
    confidence: float
    word_count: int
    warning:    str | None = None

# ── endpoints ──────────────────────────────────────────────────────────
@app.get("/")
def root():
    return {"status": "running", "app": "SentimentLens v1.0"}

@app.get("/health")
def health():
    return {
        "status"    : "healthy",
        "vocab_size" : len(word_index)
    }

@app.post("/predict", response_model=PredictionResponse)
def predict(request: ReviewRequest, threshold: float = 0.5):

    if not request.review.strip():
        raise HTTPException(status_code=400, detail="Review cannot be empty")

    # tokenize with +3 offset
    words     = request.review.lower().split()
    token_ids = []
    for word in words:
        idx = word_index.get(word)
        if idx is None or idx + 3 >= VOCAB_SIZE:
            token_ids.append(2)
        else:
            token_ids.append(idx + 3)

    # pad to MAX_LEN
    padded = pad_sequences(
        [token_ids],
        maxlen=MAX_LEN,
        padding="pre",
        truncating="post"
    )

    # predict
    score      = float(model.predict(padded, verbose=0)[0][0])
    label      = "POSITIVE" if score >= threshold else "NEGATIVE"
    confidence = round((score if score >= threshold else 1 - score) * 100, 1)

    return {
        "label"     : label,
        "score"     : round(score, 4),
        "confidence": confidence,
        "word_count": len(words),
        "warning"   : "Short input — confidence may be lower" if len(words) < 20 else None
    }