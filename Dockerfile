FROM python:3.10-slim AS build

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    LANG=C.UTF-8

WORKDIR /app

RUN apt-get clean && rm -rf /var/lib/apt/lists/* \
    && apt-get update --fix-missing

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libgl1-mesa-glx \
    libsm6 \
    libxext6 \
    libxrender1 \
    libpangocairo-1.0-0 \
    libpango-1.0-0 \
    libcairo2 \
    libglib2.0-0 \
    libmagic1 \
    && dpkg --configure -a \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

COPY requirements.txt ./

RUN pip install --upgrade pip && pip install --no-cache-dir --prefix=/install -r requirements.txt
RUN pip install --no-cache-dir --prefix=/install "python-doctr[torch]" python-multipart uvicorn -vvv

FROM python:3.10-slim AS final

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    LANG=C.UTF-8 \
    APP_HOME=/app \
    PORT=80

WORKDIR $APP_HOME

RUN apt-get update && apt-get install -y --no-install-recommends \
    libgl1 \
    libpango-1.0-0 \
    libcairo2 \
    libglib2.0-0 \
    libmagic1 \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

COPY --from=build /install /usr/local

COPY main.py ./
COPY ocr.py ./
COPY my_csv.py ./
COPY my_json.py ./
COPY my_txt.py ./
COPY my_file.py ./
COPY test.png ./
COPY download_models.py ./
COPY models/* ./models/

RUN python download_models.py

EXPOSE 80

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80"]