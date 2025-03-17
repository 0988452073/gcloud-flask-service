# 設定 GOOGLE_ENTRYPOINT 環境變數
ENV GOOGLE_ENTRYPOINT gunicorn -b 0.0.0.0:8080 app:app

# 使用官方 Python 3.9 映像
FROM python:3.9

# 設定工作目錄
WORKDIR /app

# 複製檔案
COPY requirements.txt requirements.txt
COPY . .

# 安裝相依套件
RUN pip install -r requirements.txt

# 指定執行 Flask 應用
CMD ["gunicorn", "-b", "0.0.0.0:8080", "app:app"]