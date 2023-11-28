FROM python:3.9-slim

WORKDIR /usr/src/app

COPY flightserver/requirements.txt ./

RUN pip install --no-cache-dir -r requirements.txt

COPY flightserver/main.py ./

EXPOSE 8815

CMD ["python", "./main.py"]
