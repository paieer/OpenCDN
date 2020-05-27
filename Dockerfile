FROM python:3.8
RUN pip install --upgrade --no-cache-dir pip
WORKDIR /app

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY run.py .
COPY resources ./resources
COPY opencdn.conf .

ENV PYTHONPATH=/app

CMD ["python", "run.py"]