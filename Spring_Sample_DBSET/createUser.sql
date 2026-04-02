-- ユーザの作成

-- ユーザ名：spring_sample_user
-- パスワード：trainocate

-- GRANT ALL PRIVILEGES ON spring_sample.* TO spring_sample_userIDENTIFIED BY 'trainocate';
-- GRANT ALL PRIVILEGES ON spring_sample.* TO 'spring_sample_user'@'localhost' IDENTIFIED BY 'trainocate';

CREATE USER 'spring_sample_user'@'localhost' IDENTIFIED BY 'trainocate';
GRANT all ON spring_sample.* TO 'spring_sample_user'@'localhost';
FLUSH PRIVILEGES;



quit
