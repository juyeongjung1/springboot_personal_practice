package jp.co.trainocate.book.controller;

import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestMapping;

import jp.co.trainocate.book.form.BookForm;

/**
 * 書籍管理の各種画面遷移を担当するController。
 */
@Controller
@RequestMapping("/book")
public class BookController {

    @GetMapping("/index")
    public String bookIndex() {
        return "book_index";
    }

    @GetMapping("/list")
    public String bookList() {
        return "book_list";
    }

    @GetMapping("/search/title")
    public String searchByTitle(String keyword, Model model) {
        model.addAttribute("keyword", keyword);
        model.addAttribute("searchType", "title");
        return "book_search_result";
    }

    @GetMapping("/search/price")
    public String searchByPrice(Integer minPrice, Integer maxPrice, Model model) {
        model.addAttribute("minPrice", minPrice);
        model.addAttribute("maxPrice", maxPrice);
        model.addAttribute("searchType", "price");
        return "book_search_result";
    }

    @GetMapping("/form")
    public String bookForm() {
        return "book_form";
    }

    @PostMapping("/register")
    public String register(BookForm bookForm, Model model) {
        model.addAttribute("bookForm", bookForm);
        return "book_confirm";
    }
}
