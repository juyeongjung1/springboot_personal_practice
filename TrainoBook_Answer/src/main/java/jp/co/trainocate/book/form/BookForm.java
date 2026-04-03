package jp.co.trainocate.book.form;

import lombok.Data;

/**
 * 書籍登録用・更新用のデータを受け取るためのFormクラス。
 * 
 * フォームの各入力項目（name属性）と一致させることでSpring MVCがデータをバインドします。
 */
@Data
public class BookForm {

	// ==========================================
	// 【課題3.7追加分】 書籍ID（更新用）
	// ==========================================
	private Integer id;

	// ==========================================
	// 【課題2.3実装分】 新規登録用フィールド
	// ==========================================
	/** 書籍タイトル（name属性: title） */
	private String title;

	/** 著者名（name属性: author） */
	private String author;

	/** 価格（name属性: price） */
	private Integer price;

	// ==========================================
	// 【課題3.6追加分】 ジャンルID追加
	// ==========================================
	private Integer genreId;
}
