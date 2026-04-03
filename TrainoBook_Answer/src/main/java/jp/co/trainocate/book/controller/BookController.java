package jp.co.trainocate.book.controller;

import java.util.List;

import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestMapping;

import jp.co.trainocate.book.entity.Book;
import jp.co.trainocate.book.form.BookForm;
import jp.co.trainocate.book.service.BookService;
import lombok.RequiredArgsConstructor;

/**
 * 書籍管理の各種画面遷移とCRUD操作を担当するController。
 */
@Controller
@RequestMapping("/book")
@RequiredArgsConstructor
public class BookController {

    // 依存性の注入（Service層）
    private final BookService bookService;

    @GetMapping("/index")
    public String bookIndex() {
        return "book_index";
    }

    /**
     * 全件一覧の表示
     */
    @GetMapping("/list")
    public String bookList(Model model) {
        List<Book> bookList = bookService.findAllBooks();
        model.addAttribute("books", bookList); 
        return "book_list";
    }

    /**
     * タイトル検索
     */
    @GetMapping("/search/title")
    public String searchByTitle(String keyword, Model model) {
        List<Book> bookList = bookService.findBooksByTitle(keyword);
        model.addAttribute("books", bookList);
        model.addAttribute("searchType", "title");
        model.addAttribute("keyword", keyword);
        return "book_search_result";
    }

    /**
     * 価格検索
     */
    @GetMapping("/search/price")
    public String searchByPrice(Integer minPrice, Integer maxPrice, Model model) {
        List<Book> bookList = bookService.findBooksByPrice(minPrice, maxPrice);
        model.addAttribute("books", bookList);
        model.addAttribute("searchType", "price");
        model.addAttribute("minPrice", minPrice);
        model.addAttribute("maxPrice", maxPrice);
        return "book_search_result";
    }

    /**
     * 詳細画面の表示（動的URL）
     */
    @GetMapping("/detail/{id}")
    public String bookDetail(@PathVariable Integer id, Model model) {
        Book book = bookService.findBookById(id);
        model.addAttribute("book", book);
        return "book_detail";
    }

    /**
     * 新規登録フォームの表示
     */
    @GetMapping("/form")
    public String bookForm() {
        return "book_form";
    }

    /**
     * 新規登録の実行
     */
    @PostMapping("/register")
    public String register(BookForm bookForm, Model model) {
        Book book = bookService.saveBook(bookForm);
        model.addAttribute("book", book);
        return "book_confirm";
    }

    /**
     * 更新フォームの表示
     */
    @GetMapping("/update/{id}")
    public String updateForm(@PathVariable Integer id, Model model) {
        Book book = bookService.findBookById(id);
        model.addAttribute("book", book);
        return "book_update";
    }

    /**
     * 更新の実行
     */
    @PostMapping("/update/{id}")
    public String update(@PathVariable Integer id, BookForm bookForm, Model model) {
        bookForm.setId(id);
        Book book = bookService.saveBook(bookForm);
        model.addAttribute("book", book);
        return "book_confirm"; 
    }

    /**
     * 削除の実行
     */
    @RequestMapping("/delete/{id}")
    public String delete(@PathVariable Integer id) {
        bookService.deleteBook(id);
        return "redirect:/book/list";
    }
}
