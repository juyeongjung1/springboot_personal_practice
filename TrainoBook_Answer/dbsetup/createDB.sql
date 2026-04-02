-- 
-- Database structure for database 'traino_book'
-- 書籍管理システム（TrainoBook）用データベース
-- 

CREATE DATABASE IF NOT EXISTS traino_book;
USE traino_book;

-- ジャンルテーブル（第6章で使用）
DROP TABLE IF EXISTS book;
DROP TABLE IF EXISTS genre;

CREATE TABLE genre (
    id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(50) NOT NULL
);

INSERT INTO genre (name) VALUES
('プログラミング'),
('ビジネス'),
('小説'),
('科学'),
('自己啓発');

-- 書籍テーブル
CREATE TABLE book (
    id INT PRIMARY KEY AUTO_INCREMENT,
    title VARCHAR(255) NOT NULL,
    author VARCHAR(100) NOT NULL,
    price INT NOT NULL,
    genre_id INT,
    FOREIGN KEY (genre_id) REFERENCES genre(id)
);

INSERT INTO book (title, author, price, genre_id) VALUES
('Java入門', '山田太郎', 2800, 1),
('Spring Boot実践', '鈴木一郎', 3200, 1),
('Python基礎', '田中花子', 2500, 1),
('ビジネス戦略入門', '佐藤次郎', 1800, 2),
('リーダーシップ論', '高橋美咲', 2000, 2),
('星の物語', '小林翔', 1500, 3),
('夏の記憶', '渡辺菜々', 1400, 3),
('宇宙の謎', '伊藤博', 2200, 4),
('AI時代の生き方', '中村真一', 1900, 5);

-- ユーザテーブル（第4章で使用）
CREATE TABLE user (
    emp_id INT(6) PRIMARY KEY,
    password VARCHAR(255) NOT NULL,
    emp_name VARCHAR(50) NOT NULL
);

INSERT INTO user (emp_id, password, emp_name) VALUES
(100001, 'pass1234', '山田太郎'),
(100002, 'pass2345', '鈴木花子'),
(100003, 'pass3456', '田中一郎');

quit
