FROM python:alpine

WORKDIR /app

COPY requirements.txt .
RUN pip3 install -r requirements.txt

ENV PYTHONUNBUFFERED=1
COPY template/config.yaml /tmp

COPY . .

ENTRYPOINT ["python3"]
CMD ["main.py"]
