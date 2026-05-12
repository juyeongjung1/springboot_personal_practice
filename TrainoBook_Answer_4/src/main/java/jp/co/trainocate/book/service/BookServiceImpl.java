package jp.co.trainocate.book.service;

import java.util.List;
import org.springframework.stereotype.Service;
import jp.co.trainocate.book.entity.Book;
import jp.co.trainocate.book.form.BookForm;
import jp.co.trainocate.book.repository.BookRepository;
import lombok.RequiredArgsConstructor;

/**
 * 【課題3.3】BookServiceの実装クラス。
 * 
 * @Serviceアノテーションを付けることで、SpringのDIコンテナに登録されます。
 */
@Service
@RequiredArgsConstructor
public class BookServiceImpl implements BookService {

    /**
     * 【課題3.3】依存性の注入（DI）
     * データベース操作を行うため、BookRepositoryをフィールドとして宣言します。
     * @RequiredArgsConstructor（Lombok）とfinalにより自動的にDIされます。
     */
    private final BookRepository bookRepository;

    @Override
    public List<Book> findAllBooks() {
        return bookRepository.findAll();
    }

    @Override
    public Book findBookById(Integer id) {
        return bookRepository.findById(id).orElse(null);
    }

    @Override
    public List<Book> findBooksByTitle(String title) {
        return bookRepository.findByTitleContaining(title);
    }

    @Override
    public List<Book> findBooksByPrice(Integer minPrice, Integer maxPrice) {
        // 【B-4対応】最低価格・最高価格が未入力の場合のフォールバック処理
        // 両方未指定なら全件、片方のみ指定なら 0 円〜 / 〜 上限なし として検索
        if (minPrice == null && maxPrice == null) {
            return bookRepository.findAll();
        }
        Integer min = (minPrice != null) ? minPrice : 0;
        Integer max = (maxPrice != null) ? maxPrice : Integer.MAX_VALUE;
        return bookRepository.findByPriceBetween(min, max);
    }

    /**
     * 【課題3.6, 3.7】登録および更新処理
     */
    @Override
    public Book saveBook(BookForm bookForm) {
        Book book = new Book();
        
        // idがあればセット（更新用）
        if (bookForm.getId() != null) {
            book.setId(bookForm.getId());
        }
        
        // フォームからエンティティへの値の詰め替え
        book.setTitle(bookForm.getTitle());
        book.setAuthor(bookForm.getAuthor());
        book.setPrice(bookForm.getPrice());
        book.setGenreId(bookForm.getGenreId());
        
        // 登録・更新の実行。IDが存在すればUPDATE、無ければINSERTになる
        return bookRepository.save(book);
    }

    @Override
    public void deleteBook(Integer id) {
        bookRepository.deleteById(id);
    }
}
