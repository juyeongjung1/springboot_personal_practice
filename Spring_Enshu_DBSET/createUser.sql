-- ユーザの作成

-- ユーザ名：spring_exercise_user
-- パスワード：password

-- GRANT ALL PRIVILEGES ON spring_exercise.* TO spring_exercise_user IDENTIFIED BY 'password';
-- GRANT ALL PRIVILEGES ON spring_exercise.* TO 'spring_exercise_user'@'localhost' IDENTIFIED BY 'password';

CREATE USER 'spring_exercise_user'@'localhost' IDENTIFIED BY 'password';
GRANT all ON spring_exercise.* TO 'spring_exercise_user'@'localhost';
FLUSH PRIVILEGES;



quit
