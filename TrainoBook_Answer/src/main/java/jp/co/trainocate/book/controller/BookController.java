package jp.co.trainocate.book.controller;

import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestMapping;

import jp.co.trainocate.book.form.BookForm;

/**
 * 【課題2.2, 2.3】書籍管理メニュー画面・検索モック・登録モックを担当するController。
 * 
 * 書籍に関する画面遷移とデータ受信の処理をまとめて管理する。
 * URLはすべて「/book/」配下に統一する。
 */
@Controller
@RequestMapping("/book")
public class BookController {

	/**
	 * 【課題2.2 - ステップ1】
	 * 書籍管理メニュー画面（book_index.html）を表示する。
	 * ログイン成功後や、各画面から戻ってきた際の起点となる画面。
	 */
	@GetMapping("/index")
	public String bookIndex() {
		return "book_index";
	}

	/**
	 * 【課題2.2 - ステップ3】
	 * 全書籍リスト画面（book_list.html）を表示する。
	 * 第2章ではモックとして仮の文言のみを表示する。
	 * （第3章でDB連動の一覧表示を実装予定）
	 */
	@GetMapping("/list")
	public String bookList() {
		return "book_list";
	}

	/**
	 * 【課題2.2 - ステップ5, 6】
	 * 書籍名検索のモック処理。
	 * GETパラメータ「keyword」を受け取り、Modelに格納して検索結果画面へ遷移する。
	 * （第3章で実際のDB検索を実装予定）
	 * 
	 * @param keyword 検索キーワード（name属性: keyword）
	 * @param model   画面へデータを渡すためのModel
	 * @return 検索結果モック画面
	 */
	@GetMapping("/search/title")
	public String searchByTitle(String keyword, Model model) {
		// 受け取ったキーワードをModelに格納し、画面で表示する
		model.addAttribute("keyword", keyword);
		model.addAttribute("searchType", "title");
		return "book_search_result";
	}

	/**
	 * 【課題2.2 - ステップ5, 6】
	 * 価格帯検索のモック処理。
	 * GETパラメータ「minPrice」「maxPrice」を受け取り、Modelに格納して検索結果画面へ遷移する。
	 * （第3章で実際のDB検索（between）を実装予定）
	 * 
	 * @param minPrice 最低価格（name属性: minPrice）
	 * @param maxPrice 最高価格（name属性: maxPrice）
	 * @param model    画面へデータを渡すためのModel
	 * @return 検索結果モック画面
	 */
	@GetMapping("/search/price")
	public String searchByPrice(Integer minPrice, Integer maxPrice, Model model) {
		// 受け取った価格帯をModelに格納し、画面で表示する
		model.addAttribute("minPrice", minPrice);
		model.addAttribute("maxPrice", maxPrice);
		model.addAttribute("searchType", "price");
		return "book_search_result";
	}

	/**
	 * 【課題2.3 - ステップ3】
	 * 書籍登録フォーム画面（book_form.html）を表示する。
	 * book_index.html の「書籍情報の登録」リンクから遷移してくる。
	 */
	@GetMapping("/form")
	public String bookForm() {
		return "book_form";
	}

	/**
	 * 【課題2.3 - ステップ4, 5, 6】
	 * 書籍登録のモック処理。
	 * POSTされたフォームデータをBookFormクラスで一括受け取りし、
	 * そのままModelに格納して確認画面へ遷移する。
	 * （第3章で実際のDB保存処理を実装予定）
	 * 
	 * @param bookForm フォームから送信された書籍データ（title, author, price）
	 * @param model    画面へデータを渡すためのModel
	 * @return 登録完了モック画面
	 */
	@PostMapping("/register")
	public String register(BookForm bookForm, Model model) {
		// 受け取ったFormオブジェクトをそのままModelに格納する
		model.addAttribute("bookForm", bookForm);
		return "book_confirm";
	}
}
