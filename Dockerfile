# Баз дүрс
FROM python:3.10-slim

# libGL болон шаардлагатай сангууд суулгана
RUN apt-get update && apt-get install -y \
    libgl1-mesa-glx \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

# Ажлын хавтас үүсгэнэ
WORKDIR /app

# Төслийн бүх файлыг хуулах
COPY . .

# Шаардлагатай Python сангууд суулгах
RUN pip install --no-cache-dir -r requirements.txt

# Порт тохируулах
EXPOSE 10000

# Сервер эхлүүлэх
CMD ["python", "app.py"]
