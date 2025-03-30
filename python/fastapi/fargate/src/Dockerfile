FROM python:3.8.1-slim

# the dir name does not make sence for me
WORKDIR /app

COPY requirements.txt requirements.txt

RUN pip install --no-cache-dir -r requirements.txt

ENV PYTHONUNBUFFERED 1
EXPOSE 80

COPY . .

CMD ["uvicorn", "--host", "0.0.0.0", "--port", "80", "app.main:app", "--reload"]
