package jp.co.trainocate.book.repository;

import org.springframework.data.jpa.repository.JpaRepository;
import jp.co.trainocate.book.entity.User;

/**
 * 【課題4.2】Userエンティティ用のリポジトリ。
 * 
 * 基本的なCRUD操作はJpaRepositoryによって自動提供されます。
 * 主キーが Integer (userId) なので、第2型引数は Integer となります。
 */
public interface UserRepository extends JpaRepository<User, Integer> {
}
