package jp.co.trainocate.book.repository;

import java.util.List;
import org.springframework.data.jpa.repository.JpaRepository;
import jp.co.trainocate.book.entity.Book;

public interface BookRepository extends JpaRepository<Book, Integer> {
    
    // タイトルに特定の文字列を含む検索
    List<Book> findByTitleContaining(String title);
    
    // 価格が指定範囲内の検索
    List<Book> findByPriceBetween(Integer minPrice, Integer maxPrice);
}
