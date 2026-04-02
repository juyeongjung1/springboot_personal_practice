package jp.co.trainocate.book.controller;

import org.springframework.stereotype.Controller;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PostMapping;

/**
 * 【課題2.1】ログイン（トップ画面）の作成と画面遷移
 * 
 * ログイン画面の表示と、ログイン処理（モック）を担当するController。
 * ログイン関連の処理は BookController とは分離して管理する。
 */
@Controller
public class LoginController {

	/**
	 * 【課題2.1 - ステップ2】
	 * URL「/」にアクセスした際、ログイン画面（index.html）を返す。
	 */
	@GetMapping("/")
	public String index() {
		return "index";
	}

	/**
	 * 【課題2.1 - ステップ5, 6】
	 * ログインフォームからPOSTされたユーザIDとパスワードを受け取る。
	 * 第2章ではモックとして、認証処理は行わず、そのまま書籍管理メニュー画面へ遷移する。
	 * ※リダイレクトはせず、直接 book_index を返す。
	 * 
	 * @param userId   ユーザID（name属性: userId）
	 * @param password パスワード（name属性: password）
	 * @return 書籍管理メニュー画面
	 */
	@PostMapping("/login")
	public String login(String userId, String password) {
		// 第2章ではモックのため、認証チェックは行わない
		// （第4章以降でDB連動の認証処理を実装予定）
		return "book_index";
	}
}
