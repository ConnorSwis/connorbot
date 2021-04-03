FROM python:3.9.2-slim



WORKDIR /app

COPY . .

RUN pip install -r requirements.txt

CMD ["python3", "connor_bot.py"]