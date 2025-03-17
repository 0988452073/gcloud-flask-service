# 使用官方 Python 3.9
FROM python:3.9

# 設定工作目錄
WORKDIR /app

# 複製專案
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 複製 Flask 程式
COPY . .

# 設定 Flask 環境
ENV FLASK_APP=app.py
ENV FLASK_RUN_HOST=0.0.0.0
ENV FLASK_RUN_PORT=8080
ENV PYTHONUNBUFFERED=1

# 對外開放 8080 Port
EXPOSE 8080

# 使用 gunicorn 運行 Flask 應用
CMD ["gunicorn", "-b", "0.0.0.0:8080", "app:app"]