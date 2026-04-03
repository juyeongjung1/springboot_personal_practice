package jp.co.trainocate.book.repository;

import org.springframework.data.jpa.repository.JpaRepository;
import jp.co.trainocate.book.entity.Genre;

public interface GenreRepository extends JpaRepository<Genre, Integer> {
}
