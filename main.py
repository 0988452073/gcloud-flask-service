from flask import Flask, request, jsonify
import cv2
import numpy as np
from ultralytics import YOLO

app = Flask(__name__)

# 載入 YOLOv8 模型
model = YOLO("yolov8n.pt")

@app.route("/")
def home():
    return "Flask YOLOv8 API is running!"

@app.route("/upload", methods=["POST"])
def upload_image():
    if "image" not in request.files:
        return jsonify({"error": "No image uploaded"}), 400

    # 讀取影像
    file = request.files["image"]
    image_bytes = file.read()
    np_arr = np.frombuffer(image_bytes, np.uint8)
    img = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)

    # 使用 YOLO 進行物件偵測
    results = model(img)

    # 提取手機偵測結果
    phones = []
    for r in results:
        for box in r.boxes:
            cls = int(box.cls[0])  # 取得類別索引
            name = model.names[cls]  # 取得類別名稱
            if name == "cell phone":  # 確保名稱對應 "cell phone"
                x1, y1, x2, y2 = map(int, box.xyxy[0])  # 取得邊界框
                confidence = float(box.conf[0])  # 取得信心分數
                phones.append({"label": name, "confidence": confidence, "box": [x1, y1, x2, y2]})

    return jsonify({"phones_detected": phones})

if __name__ == "__main__":
    from os import environ
    port = int(environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)