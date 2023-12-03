FROM python:3.9-slim

WORKDIR /usr/src/app

COPY requirements.txt ./

RUN pip install --no-cache-dir -r requirements.txt

COPY backend ./

EXPOSE 5012

CMD ["python", "./server.py"]
