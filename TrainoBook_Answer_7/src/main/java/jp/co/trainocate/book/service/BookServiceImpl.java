package jp.co.trainocate.book.service;

import java.util.List;
import org.springframework.stereotype.Service;
import jp.co.trainocate.book.entity.Book;
import jp.co.trainocate.book.entity.Genre;
import jp.co.trainocate.book.form.BookForm;
import jp.co.trainocate.book.repository.BookRepository;
import jp.co.trainocate.book.repository.GenreRepository;
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

    /**
     * 【B-3対応】saveBook() で book.genre を手動セットするために使用。
     * Spring Data JPA の save() は book.genre を null のままにしてしまうため、
     * 別途 GenreRepository から Genre エンティティを取得して設定する。
     */
    private final GenreRepository genreRepository;

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
     * 【課題6.3追加】ジャンル名の一部一致と、指定価格以下による複合検索。
     */
    @Override
    public List<Book> findBooksByComplexCondition(String genreName, Integer maxPrice) {
        return bookRepository.findByGenreNameContainingAndMaxPrice(genreName, maxPrice);
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
        Book saved = bookRepository.save(book);

        // 【B-3対応】save() の戻り値は book.genre が null のまま返るため、
        // GenreRepository から Genre エンティティを取得して手動でセットする。
        // これにより book_confirm.html の ${book.genre.name} が正しく表示される。
        // （JPA L1 キャッシュにより findById では再ロードされず、refresh は
        //  TX が必要なためこの方式を採用）
        if (saved.getGenreId() != null) {
            Genre genre = genreRepository.findById(saved.getGenreId()).orElse(null);
            saved.setGenre(genre);
        }
        return saved;
    }

    @Override
    public void deleteBook(Integer id) {
        bookRepository.deleteById(id);
    }
}
