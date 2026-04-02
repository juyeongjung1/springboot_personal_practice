package jp.co.trainocate.answer.controller;


import java.util.List;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestMapping;

import jp.co.trainocate.answer.entity.Category;
import jp.co.trainocate.answer.entity.Product;
import jp.co.trainocate.answer.form.ProductForm;
import jp.co.trainocate.answer.repository.CategoryRepository;
import jp.co.trainocate.answer.repository.ProductRepository;

@Controller
@RequestMapping("/product")
public class ProductController {
	@Autowired
	private ProductRepository prodRepo;
	
    @Autowired
    private CategoryRepository cateRepo;
    
	@GetMapping("/findAll")
	public String showProductList(Model model) {
		List<Product> list = prodRepo.findAllProducts();
		//System.out.println(list); //外部参照の定義後は、エラーになる
		model.addAttribute("products", list);
		return "product/list";
	}

	@GetMapping("/")
	public String showSearchView() {
		return "product/search";
	}

	@GetMapping("/findById")
	public String showProductById(int id, Model model) {
		Product product = prodRepo.findById(id).orElse(null);
		model.addAttribute("product", product);
		return "product/detail";
	}

	@GetMapping("/findByPrice")
	public String showProductListByPrice(int price, Model model) {
		List<Product> list = prodRepo.findByPrice(price);
		model.addAttribute("products", list);
		return "product/list";
	}

	@GetMapping("/findByNameAndPrice")
	public String showProductListByNameAndPrice(String name, int price, Model model) {
		//List<Product> list = prodRepo.findByNameAndPrice(name, price);
		List<Product> list = prodRepo.findByNameContainingAndPrice(name, price);
		model.addAttribute("products", list);
		return "product/list";
	}

	@GetMapping("/insert")
	public String showProductInsertView(Model model) {
		List<Category> list = cateRepo.findAll();
		model.addAttribute("categories", list);
		return "product/insert";
	}

	@PostMapping("/insert")
	public String insertProduct(ProductForm productForm, Model model) {
		Product product = new Product();
		product.setName(productForm.getName());
		product.setPrice(productForm.getPrice());
		
		// カテゴリIDを設定する処理を追加しようとする
		product.setCategoryId(productForm.getCategoryId());
		
		product = prodRepo.save(product);
		model.addAttribute("product", product);
		return "product/result";
	}

	@GetMapping("update/{id}")
	public String showUpdateInputView(@PathVariable int id, Model model) {
		Product product = prodRepo.findById(id).orElse(null);
		model.addAttribute("product", product);
		return "product/update_input";
	}

	@PostMapping("/update")
	public String updateProduct(ProductForm productForm) {
		Product product = new Product();
		product.setId(productForm.getId());
		product.setName(productForm.getName());
		product.setPrice(productForm.getPrice());
		prodRepo.save(product);
		return "redirect:/product/findAll";
	}
	
	@GetMapping("/delete/{id}")
	public String deleteProduct(@PathVariable int id) {
		prodRepo.deleteById(id);
		return "redirect:/product/findAll";
	}
	
	/*@GetMapping("/findByPriceBetween")
	public String showProductListByPriceBetween(int priceMin,int priceMax, Model model) {
		List<Product> list = prodRepo.findByPriceBetween(priceMin, priceMax);
		System.out.println(list);
		model.addAttribute("products", list);
		return "product/list";
	}*/
	

}
