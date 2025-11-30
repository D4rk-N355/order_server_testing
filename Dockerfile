# 使用官方 Python 基底映像
FROM python:3.11-slim

# 設定工作目錄
WORKDIR /app

# 複製需求檔並安裝
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 複製程式碼
COPY . .

# 設定環境變數 (讓 Flask 在容器裡跑)
ENV FLASK_APP=run.py
ENV FLASK_RUN_HOST=0.0.0.0
ENV FLASK_RUN_PORT=2323

# 開機啟動命令
CMD ["python", "run.py"]