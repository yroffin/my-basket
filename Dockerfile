FROM python:alpine

WORKDIR /app

RUN pip3 install nicegui
RUN pip3 install authlib

ENV PYTHONUNBUFFERED=1
COPY template/config.yaml /tmp

COPY . .

ENTRYPOINT ["python3"]
CMD ["main.py"]
