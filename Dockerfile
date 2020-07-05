FROM python:3.6.1

WORKDIR /app

COPY requirements.txt .

RUN apt update && apt install cmake -y
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

ADD . /app

EXPOSE 8080

CMD ["python", "app.py"]
