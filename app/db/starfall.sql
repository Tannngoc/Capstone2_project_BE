DROP DATABASE IF EXISTS starfall;
CREATE DATABASE IF NOT EXISTS starfall;
USE starfall;

-- 1. Bảng người dùng
CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    password_hash TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
) ENGINE=InnoDB;

CREATE INDEX idx_users_username ON users (username);
CREATE INDEX idx_users_email ON users (email);
CREATE INDEX idx_users_created_at ON users (created_at);
CREATE INDEX idx_users_updated_at ON users (updated_at);


-- 2. Bảng vai trò người dùng
CREATE TABLE roles (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(50) UNIQUE NOT NULL
) ENGINE=InnoDB;

CREATE TABLE user_roles (
    user_id INT,
    role_id INT,
    PRIMARY KEY (user_id, role_id),
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (role_id) REFERENCES roles(id) ON DELETE CASCADE
) ENGINE=InnoDB;

CREATE INDEX idx_user_roles_role_id ON user_roles (role_id);


-- 3. Bảng danh sách cổ phiếu
CREATE TABLE stocks (
    id INT AUTO_INCREMENT PRIMARY KEY,
    symbol VARCHAR(10) UNIQUE NOT NULL,
    name VARCHAR(100) NOT NULL
) ENGINE=InnoDB;


-- 4. Bảng giá cổ phiếu (Partition by Year)
CREATE TABLE stock_prices (
    id INT AUTO_INCREMENT PRIMARY KEY,
    stock_id INT,
    date DATETIME NOT NULL,
    year INT AS (YEAR(date)) STORED, -- Đảm bảo là STORED
    open_price DECIMAL(10,2) NOT NULL,
    high_price DECIMAL(10,2) NOT NULL,
    low_price DECIMAL(10,2) NOT NULL,
    close_price DECIMAL(10,2) NOT NULL,
    volume BIGINT NOT NULL,
    FOREIGN KEY (stock_id) REFERENCES stocks(id) ON DELETE CASCADE,
    INDEX idx_stock_date (stock_id, date),
    INDEX idx_stock_prices_stock_id_date (stock_id, year, date DESC) -- Tạo INDEX sau khi khai báo STORED
) ENGINE=InnoDB;

CREATE INDEX idx_stock_prices_year ON stock_prices (year);
CREATE UNIQUE INDEX idx_stock_prices_unique ON stock_prices (stock_id, date);

-- 5. Bảng dự đoán AI
CREATE TABLE IF NOT EXISTS predictions (
    id INT AUTO_INCREMENT PRIMARY KEY,
    stock_id INT,
    predicted_price DECIMAL(10,2) NOT NULL,
    prediction_date DATETIME NOT NULL,
    model_used VARCHAR(50) NOT NULL,
    FOREIGN KEY (stock_id) REFERENCES stocks(id) ON DELETE CASCADE
) ENGINE=InnoDB;

CREATE INDEX idx_predictions_date ON predictions (prediction_date);


-- 6. Bảng lệnh giao dịch
CREATE TABLE IF NOT EXISTS orders (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT,
    stock_id INT,
    order_type ENUM('BUY', 'SELL') NOT NULL,
    quantity INT NOT NULL,
    price DECIMAL(10,2) NOT NULL,
    status ENUM('PENDING', 'COMPLETED', 'CANCELLED') NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    executed_at TIMESTAMP NULL,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (stock_id) REFERENCES stocks(id) ON DELETE CASCADE
) ENGINE=InnoDB;

CREATE INDEX idx_orders_user_id ON orders (user_id);
CREATE INDEX idx_orders_stock_id ON orders (stock_id);
CREATE INDEX idx_orders_status ON orders (status);
CREATE INDEX idx_orders_created_at ON orders (created_at);
CREATE INDEX idx_orders_executed_at ON orders (executed_at);


-- 7. Bảng lịch sử giao dịch
CREATE TABLE IF NOT EXISTS transactions (
    id INT AUTO_INCREMENT PRIMARY KEY,
    order_id INT,
    user_id INT,
    executed_price DECIMAL(10,2) NOT NULL,
    executed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (order_id) REFERENCES orders(id) ON DELETE CASCADE
) ENGINE=InnoDB;

CREATE INDEX idx_transactions_order_id ON transactions (order_id);


-- 8. Bảng thông báo
CREATE TABLE IF NOT EXISTS notifications (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT,
    message TEXT NOT NULL,
    is_read BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
) ENGINE=InnoDB;

CREATE INDEX idx_notifications_read ON notifications (user_id, is_read, created_at);


-- 9. Trigger thông báo khi giá cổ phiếu biến động
-- Thay đổi DELIMITER
DELIMITER //

-- Xóa Trigger nếu đã tồn tại
DROP TRIGGER IF EXISTS price_change_trigger //

-- Tạo Trigger mới
CREATE TRIGGER price_change_trigger 
AFTER UPDATE ON stock_prices
FOR EACH ROW
BEGIN
    -- Kiểm tra điều kiện và tạo thông báo
    IF NEW.close_price IS NOT NULL AND OLD.close_price IS NOT NULL AND NEW.close_price != OLD.close_price THEN
        
        -- Nếu giá tăng hơn 5%
        IF OLD.close_price > 0 AND NEW.close_price > OLD.close_price * 1.05 THEN
            INSERT IGNORE INTO notifications (user_id, message, created_at)
            SELECT DISTINCT o.user_id, 
                CONCAT('Cổ phiếu ', s.symbol, ' tăng hơn 5%!'),
                NOW()
            FROM orders o
            JOIN stocks s ON s.id = o.stock_id
            WHERE o.stock_id = NEW.stock_id
            LIMIT 100;
        
        -- Nếu giá giảm hơn 5%
        ELSEIF OLD.close_price > 0 AND NEW.close_price < OLD.close_price * 0.95 THEN
            INSERT IGNORE INTO notifications (user_id, message, created_at)
            SELECT DISTINCT o.user_id, 
                CONCAT('Cổ phiếu ', s.symbol, ' giảm hơn 5%!'),
                NOW()
            FROM orders o
            JOIN stocks s ON s.id = o.stock_id
            WHERE o.stock_id = NEW.stock_id
            LIMIT 100;
        END IF;
        
    END IF;
END //

DELIMITER ;

INSERT INTO stocks (symbol, name) 
	VALUES 
    		('AAPL', 'Apple Inc.'),
    		('IBM', 'IBM Corp.'),
    		('NVDA', 'NVIDIA.'),
    		('MSFT', 'Microsoft Corp.'),
    		('TSLA', 'Tesla Inc.');
