<<<<<<< HEAD
FROM python:3.10-slim

WORKDIR /app

COPY ./src /app
COPY requirements.txt /app


RUN pip install --no-cache-dir -r requirements.txt

CMD ["python","main.py"]
||||||| 12dd70a
=======
FROM python:3.10-alpine
ENV PYTHONUNBUFFERED 1
WORKDIR /app
COPY ./src /app

CMD ["python","main.py"]
>>>>>>> e50b6c23dd043df01a08eb507ffcec1c654402a4
