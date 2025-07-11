# Албан ёсны python суурь
FROM python:3.10-slim

# Ажлын директор
WORKDIR /app

# Requirements суулгах
COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt

# Кодыг хуулна
COPY . .

# Flask порт тохируулна
ENV PORT=10000
ENV FLASK_APP=app.py

# Сервер ажиллуулах
CMD ["python", "app.py"]
