-- 
-- Database structure for database 'spring_sample'
-- 

CREATE DATABASE spring_sample;
USE spring_sample;

CREATE TABLE product (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(30) NOT NULL,
    price INT NOT NULL
) ENGINE=InnoDB;


CREATE TABLE user (
    emp_id INT(6) PRIMARY KEY,
    password VARCHAR(15) NOT NULL,
    emp_name VARCHAR(30) NOT NULL
) ENGINE=InnoDB;

--
-- Input Data
--
-- 商品テーブル
-- PC関連
INSERT INTO Product (name, price) VALUES ('スマートテレビ', 30000);
INSERT INTO Product (name, price) VALUES ('ゲーミングモニター', 20000);
INSERT INTO Product (name, price) VALUES ('ノートパソコン', 50000);

-- 冷蔵庫
INSERT INTO Product (name, price) VALUES ('2ドア冷蔵庫', 50000);
INSERT INTO Product (name, price) VALUES ('コンパクト冷蔵庫', 15000);
INSERT INTO Product (name, price) VALUES ('ワインクーラー', 30000);

-- 洗濯機
INSERT INTO Product (name, price) VALUES ('全自動洗濯機', 25000);
INSERT INTO Product (name, price) VALUES ('乾燥機能付き洗濯機', 40000);
INSERT INTO Product (name, price) VALUES ('洗濯乾燥機', 60000);


-- 社員テーブル
INSERT INTO user (emp_id, password, emp_name) VALUES (123456, 'pass1234', '山田太郎');
INSERT INTO user (emp_id, password, emp_name) VALUES (234567, 'pass2345', '佐藤花子');
INSERT INTO user (emp_id, password, emp_name) VALUES (345678, 'pass3456', '鈴木一郎');


quit


