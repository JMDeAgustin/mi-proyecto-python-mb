FROM python:3.11-slim

RUN apt-get update \
 && apt-get install -y --no-install-recommends ca-certificates curl \
 && apt-get clean \
 && rm -rf /var/lib/apt/lists/*
 

WORKDIR /code

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt \
 && pip install --no-cache-dir --upgrade certifi  # <─ bundle CA actualizado

COPY . .

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
