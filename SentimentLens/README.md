# 🎬 SentimentLens — AI Sentiment Analyzer

> Real-time movie review sentiment analysis powered by LSTM deep learning, deployed on AWS EC2.

[![Live Demo](https://img.shields.io/badge/Live%20Demo-Available-brightgreen)](https://bit.ly/sentimentlens-demo)
[![Python](https://img.shields.io/badge/Python-3.11-blue)](https://www.python.org/)
[![TensorFlow](https://img.shields.io/badge/TensorFlow-2.21-orange)](https://tensorflow.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.135-teal)](https://fastapi.tiangolo.com/)
[![Docker](https://img.shields.io/badge/Docker-Containerised-blue)](https://www.docker.com/)
[![AWS](https://img.shields.io/badge/AWS-EC2-yellow)](https://aws.amazon.com/)

---

## 🔗 Live Demo

👉 **[https://bit.ly/sentimentlens-demo](https://bit.ly/sentimentlens-demo)**

---

## 📌 What is SentimentLens?

SentimentLens classifies any movie review as **POSITIVE** or **NEGATIVE** in real time using a deep learning LSTM model. Type any review into the web interface and get an instant prediction with a confidence score and probability breakdown.

---

## 🧠 How It Works
```
User types review
       ↓
Tokenize + pad to 200 tokens
       ↓
Embedding layer (10,000 × 128 weights)
       ↓
LSTM layer (64 units — reads sequence)
       ↓
Dense + Sigmoid (outputs 0.0 – 1.0)
       ↓
≥ 0.5 → POSITIVE   |   < 0.5 → NEGATIVE
```

---

## 📊 Model Details

| Property | Value |
|---|---|
| Architecture | Keras LSTM |
| Training dataset | IMDB (25,000 reviews) |
| Test dataset | IMDB (25,000 reviews) |
| Test accuracy | **83.54%** |
| Vocabulary size | 10,000 words |
| Sequence length | 200 tokens |
| Trainable parameters | 1,329,473 |
| Embedding dimensions | 128 |
| LSTM units | 64 |
| Optimizer | Adam |
| Loss function | Binary Crossentropy |

---

## 💻 Tech Stack

| Layer | Technology |
|---|---|
| Deep learning | TensorFlow 2.21 · Keras LSTM |
| Backend API | FastAPI · Uvicorn |
| Frontend UI | Streamlit |
| Containerisation | Docker |
| Cloud deployment | AWS EC2 (t2.micro) |
| Training environment | Google Colab (T4 GPU) |
| Language | Python 3.11 |

---

## 🏗 Architecture
```
┌─────────────────────────────────────────┐
│              AWS EC2 Instance           │
│                                         │
│   ┌─────────────┐    ┌───────────────┐  │
│   │  Streamlit  │───▶│   FastAPI     │  │
│   │  (port 8501)│    │  (port 8000)  │  │
│   └─────────────┘    └───────┬───────┘  │
│                              │          │
│                    ┌─────────▼────────┐ │
│                    │  TensorFlow LSTM │ │
│                    │  sentiment model │ │
│                    └──────────────────┘ │
│                                         │
│   ┌─────────────────────────────────┐   │
│   │         Docker Container        │   │
│   └─────────────────────────────────┘   │
└─────────────────────────────────────────┘
```

---

## 📁 Project Structure
```
SentimentLens/
├── app.py                  # FastAPI backend — /predict endpoint
├── ui.py                   # Streamlit frontend
├── Dockerfile              # Docker container definition
├── requirements.txt        # Python dependencies
├── model/
│   ├── sentiment_model.keras   # trained model weights (gitignored)
│   └── word_index.json         # vocabulary (gitignored)
└── README.md
```

---

## 🚀 Run Locally

**Prerequisites:** Python 3.11, Docker

### Option A — Run with Docker (recommended)
```bash
# clone the repository
git clone https://github.com/YOUR_USERNAME/AI.git
cd AI/SentimentLens

# add model files to model/ folder
# (download from Google Drive or train using the steps below)

# build the Docker image
docker build -t sentimentlens .

# run the container
docker run -p 8000:8000 -p 8501:8501 sentimentlens

# open in browser
http://localhost:8501
```

### Option B — Run without Docker
```bash
# install dependencies
pip install -r requirements.txt

# terminal 1 — start FastAPI
uvicorn app:app --reload --port 8000

# terminal 2 — start Streamlit
streamlit run ui.py --server.port 8501

# open in browser
http://localhost:8501
```

---

## 🔌 API Reference

### POST /predict

Classify a movie review as positive or negative.

**Request:**
```json
{
  "review": "This movie was absolutely brilliant."
}
```

**Response:**
```json
{
  "label": "POSITIVE",
  "score": 0.9302,
  "confidence": 93.0,
  "word_count": 6,
  "warning": "Short input — confidence may be lower"
}
```

### GET /health
```json
{
  "status": "healthy",
  "vocab_size": 88584
}
```

---

## 🏋️ Train the Model

The model was trained in Google Colab using a T4 GPU. To retrain:
```python
# key hyperparameters
VOCAB_SIZE     = 10000
MAX_LEN        = 200
EMBEDDING_DIM  = 128
LSTM_UNITS     = 64
BATCH_SIZE     = 128
EPOCHS         = 5
```

Training data: IMDB dataset built into `tensorflow.keras.datasets`

---

## 📈 Training Results

| Epoch | Train Loss | Train Acc | Val Loss | Val Acc |
|---|---|---|---|---|
| 1 | 0.682 | 0.601 | 0.590 | 0.621 |
| 2 | 0.453 | 0.783 | 0.420 | 0.790 |
| 3 | 0.321 | 0.861 | 0.365 | 0.840 |
| 4 | 0.275 | 0.889 | 0.382 | 0.839 |
| 5 | 0.234 | 0.904 | 0.410 | 0.820 |

Final test accuracy: **83.54%**

---

## 🐳 Docker
```bash
# build
docker build -t sentimentlens .

# run
docker run -d -p 8000:8000 -p 8501:8501 \
  --name sentimentlens-app \
  --restart unless-stopped \
  sentimentlens

# check logs
docker logs -f sentimentlens-app

# stop
docker stop sentimentlens-app
```

---

## ☁️ AWS Deployment

Deployed on AWS EC2 t2.micro (free tier):

- **Instance:** Amazon Linux 2023
- **Region:** us-east-1
- **Ports open:** 22 (SSH) · 8000 (FastAPI) · 8501 (Streamlit)
- **Container:** runs with `--restart unless-stopped`

---

## 🔑 Key Learnings

- How LSTM weights and embeddings encode word meaning through training
- Why sequence truncation at 200 tokens improves gradient flow
- Debugging a Keras token offset bug (+3 index shift) causing all predictions to return 0.5
- Docker containerisation of a multi-service Python application
- AWS EC2 setup and deployment from scratch
- Building a production REST API around a trained ML model

---

## 👤 Author

**Sravan Kumar Kurapati**

📧 kurapati.sr@northeastern.edu
📞 +1-857-427-7767
🔗 [LinkedIn](https://www.linkedin.com/in/sravankumar-kurapati/)
💻 [GitHub](https://github.com/sravankumarkurapati)

---

## 📄 License

MIT License — free to use, modify and distribute.

---

*Part of a structured AI/ML portfolio. More projects coming soon.*
