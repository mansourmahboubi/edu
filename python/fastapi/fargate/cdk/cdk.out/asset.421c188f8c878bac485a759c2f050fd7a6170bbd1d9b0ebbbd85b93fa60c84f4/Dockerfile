FROM python:3.8.1-slim

# the dir name does not make sence for me
WORKDIR /app

COPY . .

RUN pip install --no-cache-dir -r requirements.txt

ENV PYTHONUNBUFFERED 1
EXPOSE 8000

CMD ["uvicorn", "--host", "0.0.0.0", "--port", "8000", "app.main:app"]
