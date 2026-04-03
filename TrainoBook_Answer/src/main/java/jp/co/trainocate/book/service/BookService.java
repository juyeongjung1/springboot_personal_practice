package jp.co.trainocate.book.service;

import java.util.List;
import jp.co.trainocate.book.entity.Book;
import jp.co.trainocate.book.form.BookForm;

public interface BookService {
    List<Book> findAllBooks();
    Book findBookById(Integer id);
    List<Book> findBooksByTitle(String title);
    List<Book> findBooksByPrice(Integer minPrice, Integer maxPrice);
    Book saveBook(BookForm bookForm);
    void deleteBook(Integer id);
}
