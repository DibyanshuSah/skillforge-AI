FROM python:3.10-slim
WORKDIR /app
# System deps
RUN apt-get update && apt-get install -y \
    git \
    build-essential \
    cmake \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
# Install python dependencies
RUN pip install --no-cache-dir -r requirements.txt
# Copy all the files of the projects
COPY . .

EXPOSE 7860

CMD ["streamlit", "run", "app.py", "--server.port=7860", "--server.address=0.0.0.0"]
