package jp.co.trainocate.book.form;

import lombok.Data;

/**
 * 【課題2.3 - ステップ1, 2】
 * 書籍登録フォームのデータを受け取るためのFormクラス。
 * 
 * フォームの各入力項目（name属性）と、このクラスのフィールド名が一致することで、
 * Spring MVCが自動的にデータをバインド（紐付け）してくれる。
 * 
 * Lombokの @Data を付与することで、getter/setter/toString 等を自動生成する。
 */
@Data
public class BookForm {

	/** 書籍タイトル（name属性: title） */
	private String title;

	/** 著者名（name属性: author） */
	private String author;

	/** 価格（name属性: price） */
	private Integer price;
}
