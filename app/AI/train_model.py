import os
import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler
from keras.api.models import Sequential
from keras.api.layers import LSTM, Dense, Dropout

def load_all_stock_closes(folder_path):
    close_data = []
    csv_files = [f for f in os.listdir(folder_path) if f.endswith('.csv')]
    
    for file in csv_files:
        path = os.path.join(folder_path, file)
        df = pd.read_csv(path)
        if 'Price' in df.columns:
            df.rename(columns={'Price': 'Date'}, inplace=True)
        df['Date'] = pd.to_datetime(df['Date'], format="%Y-%m-%d")
        df.set_index('Date', inplace=True)
        close_data.append(df[['Close']].rename(columns={'Close': file.split('_')[0]}))
    
    merged = pd.concat(close_data, axis=1)
    merged.dropna(inplace=True)
    return merged

def train_joint_model(data):
    scaler = MinMaxScaler(feature_range=(0, 0.9))
    scaled_data = scaler.fit_transform(data)

    training_data_len = int(len(scaled_data) * 0.95)
    train_data = scaled_data[:training_data_len]

    x_train, y_train = [], []

    for i in range(60, len(train_data)):
        x_train.append(train_data[i-60:i])
        y_train.append(train_data[i])

    x_train, y_train = np.array(x_train), np.array(y_train)

    model = Sequential()
    model.add(LSTM(128, return_sequences=True, input_shape=(x_train.shape[1], x_train.shape[2])))
    model.add(Dropout(0.2))
    model.add(LSTM(64, return_sequences=False))
    model.add(Dropout(0.2))
    model.add(Dense(y_train.shape[1]))

    model.compile(optimizer='adam', loss='mean_squared_error')
    model.fit(x_train, y_train, batch_size=32, epochs=20, verbose=1)

    # Dự đoán để đánh giá RMSE
    test_data = scaled_data[training_data_len - 60:]
    x_test = [test_data[i-60:i] for i in range(60, len(test_data))]
    x_test = np.array(x_test)

    predictions = model.predict(x_test)
    predictions = scaler.inverse_transform(predictions)
    actual = data[training_data_len:].values

    rmse = np.sqrt(np.mean((predictions - actual) ** 2))
    print(f"✅ RMSE toàn tập: {rmse:.2f}")

    # === Lưu mô hình về thư mục AI ===
    model_path = "app/AI/joint_stock_model.keras"
    model_dir = os.path.dirname(model_path)

    if not os.path.exists(model_dir):
        os.makedirs(model_dir)

    if os.path.exists(model_path):
        os.remove(model_path)
        print("🧹 Đã xóa model cũ.")

    model.save(model_path)
    print("✅ Mô hình mới đã được lưu thành công!")

    return model, scaler, predictions, actual, data[training_data_len:]

# === Main logic ===
if __name__ == "__main__":
    print("🚀 Đang load dữ liệu...")
    data = load_all_stock_closes("app/db")
    print("✅ Dữ liệu đã sẵn sàng. Đang huấn luyện mô hình...")
    train_joint_model(data)
