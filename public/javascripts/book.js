

var Book = {};


Book.stat = function(book_id){
	Web.ajax('book-stat', {id:book_id}, function(r, success){
		
	});
};

Book.savePoint = function(chapter_id){
	Web.ajax('book-save_point', {chapter_id:chapter_id}, function(r, success){
		
	});
};

