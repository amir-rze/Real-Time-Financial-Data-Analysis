FROM tiangolo/uvicorn-gunicorn-fastapi:python3.10

COPY ./src /app
COPY requirements.txt /app
WORKDIR /app
RUN pip install --no-cache-dir -r requirements.txt
CMD ["uvicorn", "app:app", "--host", "127.0.0.1", "--port", "7000"]


