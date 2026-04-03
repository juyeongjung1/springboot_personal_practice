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
 * 【課題2.2, 2.3】【課題3.4 〜 3.7】
 * 書籍管理の各種画面遷移とCRUD操作を担当するController。
 */
@Controller
@RequestMapping("/book")
@RequiredArgsConstructor
public class BookController {

    /**
     * 【課題3.4】BookServiceの依存性の注入（DI）
     */
    private final BookService bookService;

    /**
     * 【課題2.2】メニュー画面の表示
     */
    @GetMapping("/index")
    public String bookIndex() {
        return "book_index";
    }

    /**
     * 【課題3.4】全件一覧の表示
     * DBから取得した全書籍の情報をModelに渡します。
     */
    @GetMapping("/list")
    public String bookList(Model model) {
        List<Book> bookList = bookService.findAllBooks();
        model.addAttribute("books", bookList); 
        return "book_list";
    }

    /**
     * 【課題3.4】タイトル検索
     * DBから検索条件に合致する書籍リストを取得してModelに渡します。
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
     * 【課題3.4】価格検索
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
     * 【課題3.5】詳細画面の表示（動的URL）
     * パス変数からIDを受け取って対象の書籍を1件検索します。
     */
    @GetMapping("/detail/{id}")
    public String bookDetail(@PathVariable Integer id, Model model) {
        Book book = bookService.findBookById(id);
        model.addAttribute("book", book);
        return "book_detail";
    }

    /**
     * 【課題2.3】新規登録フォームの表示
     */
    @GetMapping("/form")
    public String bookForm() {
        return "book_form";
    }

    /**
     * 【課題3.6】新規登録の実行
     * Formクラスでデータを受け取り、DBへの登録処理を指示します。
     */
    @PostMapping("/register")
    public String register(BookForm bookForm, Model model) {
        Book book = bookService.saveBook(bookForm);
        model.addAttribute("book", book);
        return "book_confirm";
    }

    /**
     * 【課題3.7】更新フォームの表示
     * 更新対象のデータをDBから取得し、あらかじめ画面にセットさせます。
     */
    @GetMapping("/update/{id}")
    public String updateForm(@PathVariable Integer id, Model model) {
        Book book = bookService.findBookById(id);
        model.addAttribute("book", book);
        return "book_update";
    }

    /**
     * 【課題3.7】更新の実行（動的URLの利用）
     * パス変数から対象のIDを受け取り、Formデータの値で上書き保存します。
     */
    @PostMapping("/update/{id}")
    public String update(@PathVariable Integer id, BookForm bookForm, Model model) {
        bookForm.setId(id);
        Book book = bookService.saveBook(bookForm);
        model.addAttribute("book", book);
        return "book_confirm"; 
    }

    /**
     * 【課題3.7】削除の実行
     * 削除処理の完了後は一覧画面等へリダイレクトして更新内容を反映させます。
     */
    @RequestMapping("/delete/{id}")
    public String delete(@PathVariable Integer id) {
        bookService.deleteBook(id);
        return "redirect:/book/list";
    }
}
