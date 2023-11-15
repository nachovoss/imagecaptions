FROM python:3.9-slim

WORKDIR /usr/src/app

COPY src/ ./
COPY requirements.txt ./

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 5000

CMD ["hypercorn", "app:app", "--bind", "0.0.0.0:5000"]
