CREATE TABLE gerioea_store (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    description TEXT,
    size VARCHAR(50),
    cost DECIMAL(10, 2) NOT NULL,
    material VARCHAR(100),
    brand VARCHAR(100),
    category VARCHAR(100),
    weight DECIMAL(10, 2),
    active_status VARCHAR(20),
    phone_number VARCHAR(20)
);
