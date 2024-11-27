FROM python:3.12

RUN mkdir /app
WORKDIR /app

COPY requirements.txt .

RUN pip install -r requirements.txt
RUN apt-get update

COPY . .

CMD ["python", "main.py"]
