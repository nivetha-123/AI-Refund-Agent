-- ============================================================
-- Mock CRM Database — 15 customers, 20 orders
-- ============================================================

CREATE TABLE IF NOT EXISTS customers (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    email TEXT UNIQUE NOT NULL,
    name TEXT NOT NULL,
    phone TEXT,
    account_tier TEXT DEFAULT 'standard',
    joined_date TEXT NOT NULL,
    total_orders INTEGER DEFAULT 0,
    lifetime_value REAL DEFAULT 0.0
);

CREATE TABLE IF NOT EXISTS orders (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    order_id TEXT UNIQUE NOT NULL,
    customer_email TEXT NOT NULL,
    product_name TEXT NOT NULL,
    product_category TEXT NOT NULL,
    amount REAL NOT NULL,
    order_date TEXT NOT NULL,
    delivery_date TEXT,
    status TEXT DEFAULT 'delivered',
    is_final_sale INTEGER DEFAULT 0,
    is_digital INTEGER DEFAULT 0,
    payment_method TEXT DEFAULT 'credit_card',
    FOREIGN KEY (customer_email) REFERENCES customers(email)
);

CREATE TABLE IF NOT EXISTS refund_requests (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    request_id TEXT UNIQUE NOT NULL,
    order_id TEXT NOT NULL,
    customer_email TEXT NOT NULL,
    reason TEXT NOT NULL,
    requested_at TEXT NOT NULL,
    status TEXT DEFAULT 'pending',
    agent_decision TEXT,
    created_at TEXT DEFAULT CURRENT_TIMESTAMP
);

-- 15 Customers
INSERT INTO customers VALUES
(1,'priya.sharma@email.com','Priya Sharma','+91-9876543210','premium','2021-03-14',12,2340.50),
(2,'james.wilson@email.com','James Wilson','+1-555-234-5678','vip','2020-01-08',34,8920.00),
(3,'sofia.rodriguez@email.com','Sofia Rodriguez','+34-612-345-678','standard','2022-07-22',5,450.75),
(4,'chen.wei@email.com','Chen Wei','+86-138-0013-8000','premium','2021-11-01',18,3100.20),
(5,'amara.okafor@email.com','Amara Okafor','+234-801-234-5678','standard','2023-02-15',3,189.99),
(6,'luca.ferrari@email.com','Luca Ferrari','+39-333-456-7890','vip','2019-09-30',47,12500.00),
(7,'emily.chang@email.com','Emily Chang','+1-415-678-9012','premium','2022-04-10',9,1670.30),
(8,'omar.hassan@email.com','Omar Hassan','+20-100-234-5678','standard','2023-06-01',2,89.50),
(9,'nina.petrov@email.com','Nina Petrov','+7-916-234-5678','standard','2022-12-20',6,520.00),
(10,'raj.patel@email.com','Raj Patel','+91-8765432109','premium','2021-05-18',15,2890.00),
(11,'sarah.johnson@email.com','Sarah Johnson','+1-212-345-6789','vip','2020-08-25',29,7340.00),
(12,'marco.bianchi@email.com','Marco Bianchi','+39-347-890-1234','standard','2023-01-10',4,310.00),
(13,'yuki.tanaka@email.com','Yuki Tanaka','+81-90-1234-5678','premium','2021-09-05',11,1980.00),
(14,'fatima.al-rashid@email.com','Fatima Al-Rashid','+971-50-123-4567','standard','2022-10-30',7,640.00),
(15,'david.kim@email.com','David Kim','+1-310-456-7890','vip','2020-03-12',38,9800.00);

-- 20 Orders — every edge case covered
INSERT INTO orders VALUES
(1,'ORD-10001','priya.sharma@email.com','Wireless Noise-Cancelling Headphones','electronics',189.99,'2025-12-01','2025-12-04','delivered',0,0,'credit_card'),
(2,'ORD-10002','priya.sharma@email.com','Leather Handbag','clothing',249.00,'2025-08-10','2025-08-14','delivered',0,0,'credit_card'),
(3,'ORD-10003','james.wilson@email.com','Apple MacBook Pro 14"','electronics',1999.00,'2025-11-20','2025-11-25','delivered',0,0,'credit_card'),
(4,'ORD-10004','james.wilson@email.com','Black Friday TV Deal 65"','electronics',399.00,'2025-11-29','2025-12-02','delivered',1,0,'credit_card'),
(5,'ORD-10005','sofia.rodriguez@email.com','Yoga Mat Premium','clothing',59.99,'2025-11-28','2025-12-01','delivered',0,0,'paypal'),
(6,'ORD-10006','chen.wei@email.com','Adobe Creative Suite Annual License','digital',599.99,'2025-11-15','2025-11-15','delivered',0,1,'credit_card'),
(7,'ORD-10007','chen.wei@email.com','Mechanical Keyboard RGB','electronics',145.00,'2025-12-05','2025-12-08','delivered',0,0,'credit_card'),
(8,'ORD-10008','amara.okafor@email.com','Running Shoes','clothing',89.99,'2025-11-25','2025-11-28','delivered',0,0,'credit_card'),
(9,'ORD-10009','omar.hassan@email.com','Bluetooth Speaker','electronics',45.00,'2025-10-01','2025-10-05','returned',0,0,'credit_card'),
(10,'ORD-10010','raj.patel@email.com','Sony 4K Camera','electronics',649.00,'2025-11-30','2025-12-04','delivered',0,0,'credit_card'),
(11,'ORD-10011','raj.patel@email.com','Clearance Winter Jacket','clothing',34.99,'2025-11-15','2025-11-19','delivered',1,0,'paypal'),
(12,'ORD-10012','sarah.johnson@email.com','KitchenAid Stand Mixer','electronics',379.00,'2025-11-22','2025-11-27','delivered',0,0,'credit_card'),
(13,'ORD-10013','marco.bianchi@email.com','System Design Interview Book Set','books',79.99,'2025-12-02','2025-12-05','delivered',0,0,'credit_card'),
(14,'ORD-10014','yuki.tanaka@email.com','iPad Pro 12.9" M2','electronics',1099.00,'2025-11-18','2025-11-22','delivered',0,0,'credit_card'),
(15,'ORD-10015','fatima.al-rashid@email.com','Silk Evening Dress','clothing',159.00,'2025-11-20','2025-11-25','delivered',0,0,'credit_card'),
(16,'ORD-10016','david.kim@email.com','Seasonal Clearance Bundle','clothing',129.00,'2025-11-10','2025-11-14','delivered',1,0,'credit_card'),
(17,'ORD-10017','david.kim@email.com','Herman Miller Aeron Chair','electronics',1450.00,'2025-12-01','2025-12-06','delivered',0,0,'credit_card'),
(18,'ORD-10018','nina.petrov@email.com','Skincare Gift Set','clothing',65.00,'2025-11-26','2025-11-29','delivered',0,0,'credit_card'),
(19,'ORD-10019','emily.chang@email.com','Logitech MX Master Mouse','electronics',99.00,'2025-11-30','2025-12-03','delivered',0,0,'paypal'),
(20,'ORD-10020','luca.ferrari@email.com','Designer Watch','clothing',480.00,'2025-06-01','2025-06-05','delivered',0,0,'credit_card');
