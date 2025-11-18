FROM python:3.11-slim

# Установка ffmpeg
RUN apt update && apt install -y ffmpeg && apt clean

# Создаём директорию для бота
WORKDIR /app

# Копируем зависимости
COPY requirements.txt .

# Устанавливаем зависимости
RUN pip install --no-cache-dir -r requirements.txt

# Копируем код бота
COPY bot.py .

# Запуск бота
CMD ["python", "bot.py"]
