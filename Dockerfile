FROM python:3.11.8-slim-bullseye

WORKDIR /app

COPY . .

RUN pip install --no-cache-dir -r requirements.txt

WORKDIR /app/assignment_2

EXPOSE 5000

CMD ["python", "app_flask.py"]
