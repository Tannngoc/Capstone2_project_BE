from flask import Blueprint, request, jsonify
import pandas as pd
from keras.api.models import load_model
from sklearn.preprocessing import MinMaxScaler
import os

# ✅ Đặt prefix rõ ràng
model_bp = Blueprint("model", __name__, url_prefix="/api/predict")

# ✅ Load mô hình
MODEL_PATH = "app/AI/joint_stock_model.keras"
model = load_model(MODEL_PATH)

# ✅ Danh sách mã cổ phiếu
stock_codes = ["AAPL", "IBM", "MSFT", "NVDA", "TSLA"]

# ✅ Tiền xử lý input với 5 đặc trưng: Open, High, Low, Close, Volume
def preprocess_input(df):
    features = ["Open", "High", "Low", "Close", "Volume"]
    df = df[features].tail(60)  # lấy 60 ngày gần nhất
    scaler = MinMaxScaler()
    data_scaled = scaler.fit_transform(df)  # (60, 5)
    return data_scaled.reshape(1, 60, 5), scaler

# ✅ Route test đơn giản
@model_bp.route("/test", methods=["GET"])
def test_api():
    print("🔥 TEST API CALLED")
    return jsonify({"msg": "Test success"})

# ✅ API dự đoán toàn bộ mã cổ phiếu
@model_bp.route("/all", methods=["GET"])
def predict_all():
    print("===> /api/predict/all called")
    results = []

    for code in stock_codes:
        print(f"Processing {code}")
        csv_path = f"app/db/{code}_stock.csv"  # ✅ Đảm bảo tên file đúng
        if not os.path.exists(csv_path):
            print(f"{csv_path} not found")
            continue

        df = pd.read_csv(csv_path)
        if len(df) < 60:
            print(f"{code}: Not enough data")
            continue

        try:
            input_data, scaler = preprocess_input(df)
            predicted_scaled = model.predict(input_data, verbose=0)

            # ✅ Đảo ngược chỉ riêng giá Close
            dummy = [[0, 0, 0, predicted_scaled[0][0], 0]]
            predicted_price = scaler.inverse_transform(dummy)[0][3]

            current_price = df["Close"].iloc[-1]
            percent = (predicted_price - current_price) / current_price * 100
            direction = "increase" if predicted_price > current_price else "decrease"

            if percent > 1:
                action = "Buy"
            elif percent < -1:
                action = "Sell"
            else:
                action = "Keep"

            result = {
                "stock_code": code,
                "predict": f"{predicted_price:.2f} USD",
                "type": direction,
                "percent": f"{percent:.2f}%",
                "amount": f"{current_price:.2f} USD",
                "action": action
            }

            print(result)
            results.append(result)

        except Exception as e:
            print(f"Error processing {code}: {e}")
            continue

    return jsonify(results)

# ✅ API dự đoán cho 1 doanh nghiệp cụ thể
@model_bp.route("/<stock_code>", methods=["GET"])
def predict_single(stock_code):
    stock_code = stock_code.upper()
    print(f"===> /api/predict/{stock_code} called")

    if stock_code not in stock_codes:
        return jsonify({"error": "Stock code not supported"}), 400

    csv_path = f"app/db/{stock_code}_stock.csv"
    if not os.path.exists(csv_path):
        return jsonify({"error": f"No data found for {stock_code}"}), 404

    df = pd.read_csv(csv_path)
    if len(df) < 60:
        return jsonify({"error": f"Not enough data for {stock_code}"}), 400

    try:
        input_data, scaler = preprocess_input(df)
        predicted_scaled = model.predict(input_data, verbose=0)

        # ✅ Đảo ngược chỉ riêng giá Close
        dummy = [[0, 0, 0, predicted_scaled[0][0], 0]]
        predicted_price = scaler.inverse_transform(dummy)[0][3]

        current_price = df["Close"].iloc[-1]
        percent = (predicted_price - current_price) / current_price * 100
        direction = "increase" if predicted_price > current_price else "decrease"

        if percent > 1:
            action = "Buy"
        elif percent < -1:
            action = "Sell"
        else:
            action = "Keep"

        result = {
            "stock_code": stock_code,
            "predict": f"{predicted_price:.2f} USD",
            "type": direction,
            "percent": f"{percent:.2f}%",
            "amount": f"{current_price:.2f} USD",
            "action": action
        }

        return jsonify(result)

    except Exception as e:
        print(f"Error processing {stock_code}: {e}")
        return jsonify({"error": str(e)}), 500


# http://127.0.0.1:5000/api/predict/all