# ── Dockerfile — SentimentLens ─────────────────────────────────────────

# start from an official Python image
# slim = smaller size, only what we need
FROM python:3.11-slim

# set working directory inside the container
# all subsequent commands run from here
WORKDIR /app

# copy requirements first — Docker caches this layer
# if requirements don't change, Docker skips reinstalling on rebuild
COPY requirements.txt .

# install all Python dependencies
# --no-cache-dir keeps the image size smaller
RUN pip install --no-cache-dir -r requirements.txt

# copy the rest of the project into the container
COPY app.py .
COPY ui.py .
COPY model/ ./model/

# expose the ports our apps run on
# 8000 = FastAPI, 8501 = Streamlit
EXPOSE 8000
EXPOSE 8501

# create a startup script that runs both apps simultaneously
# we need both FastAPI and Streamlit running at the same time
RUN echo '#!/bin/bash\n\
uvicorn app:app --host 0.0.0.0 --port 8000 &\n\
streamlit run ui.py --server.port 8501 --server.address 0.0.0.0\n\
' > /app/start.sh && chmod +x /app/start.sh

# default command when container starts
CMD ["/app/start.sh"]