FROM python:3.9.7

WORKDIR /usr/src/server

COPY requirements.txt ./

RUN pip install --no-cache-dir -r requirements.txt

COPY ./ ./

CMD ["uvicorn", "server.app:app", "--host", "0.0.0.0", "--port", "8000"]
