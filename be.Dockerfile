FROM python:3.9-slim

WORKDIR /usr/src/app

COPY requirements.txt ./

RUN pip install --no-cache-dir -r requirements.txt

RUN pip install gunicorn

COPY backend ./

EXPOSE 5012

CMD ["gunicorn", "-w 4", "-b :5012", "server:app"]

