from flask import Flask, request, jsonify, Blueprint
import pandas as pd
import numpy as np
import os
from keras.api.models import load_model
from sklearn.preprocessing import MinMaxScaler

model_bp = Blueprint('train_model', __name__, url_prefix="/api/predict")

MODEL_PATH = "app/AI/joint_stock_model.keras"
DATA_DIR = "app/db"

model = load_model(MODEL_PATH)

@model_bp.route("/predict", methods=["GET"])
def predict():
    symbol = request.args.get("symbol")
    if not symbol:
        return jsonify({"error": "Missing stock symbol"}), 400

    file_path = os.path.join(DATA_DIR, f"{symbol}_stock.csv")
    if not os.path.exists(file_path):
        return jsonify({"error": "Stock data not found"}), 404

    df = pd.read_csv(file_path)
    if 'Date' in df.columns:
        df['Date'] = pd.to_datetime(df['Date'])
        df.set_index('Date', inplace=True)

    data = df[['Close']].values
    last_price = data[-1][0]

    # Scale dữ liệu
    scaler = MinMaxScaler(feature_range=(0, 0.9))
    scaled_data = scaler.fit_transform(data)

    last_60 = scaled_data[-60:]
    x_input = np.array([last_60])

    prediction = model.predict(x_input)
    predicted_price = scaler.inverse_transform(prediction)[0][0]

    # Tính phần trăm thay đổi
    diff = predicted_price - last_price
    percent = (diff / last_price) * 100
    trend = "increase" if diff > 0 else "decrease" if diff < 0 else "no change"

    # Gợi ý hành động đơn giản (tùy bạn custom thêm):
    if percent > 1:
        action = "Buy"
    elif percent < -1:
        action = "Sell"
    else:
        action = "Keep"

    return jsonify({
        "predict": f"{predicted_price:.2f} USD",
        "type": trend,
        "percent": f"{percent:.2f}%",
        "amount": f"{last_price:.2f} USD",
        "action": action
    })

