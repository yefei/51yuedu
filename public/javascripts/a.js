// 2010-6-18 AD Display

var _ads = [/*
	{path:new RegExp("^\/book\/[0-9]+\/$"),
	 expr:'#ads_book_show_option',
	 css:{float:'right'},
	 html:'<iframe id="baiduSpFrame" border="0" vspace="0" hspace="0" marginwidth="0" marginheight="0" framespacing="0" frameborder="0" scrolling="no" width="80" height="20" src="http://spcode.baidu.com/spcode/spstyle/style2865.jsp?tn=xiongsir_sp&ctn=0&styleid=2865"></iframe>'}
	 ,*/
	 {
	 path:new RegExp("^/$"),
	 expr:'#ads_index_rec_2',
	 css:{marginBottom:'10px'},
	 html:'<iframe id="baiduSpFrame" border="0" vspace="0" hspace="0" marginwidth="0" marginheight="0" framespacing="0" frameborder="0" scrolling="no" width="800" height="60" src="http://spcode.baidu.com/spcode/spstyle/style2861.jsp?tn=xiongsir_sp&ctn=0&styleid=2861"></iframe>'
	 }
	 ,
	 {
	 	 path:new RegExp("^\/book\/s|c[0-9]+\/$"),
	 	 expr:'#ads_book_books_left',
	 	 css:{marginTop:'10px', paddingLeft:'40px'},
	 	 html:'<iframe id="baiduSpFrame" border="0" vspace="0" hspace="0" marginwidth="0" marginheight="0" framespacing="0" frameborder="0" scrolling="no" width="120" height="240" src="http://spcode.baidu.com/spcode/spstyle/style2843.jsp?tn=xiongsir_sp&ctn=0&styleid=2843"></iframe>'
	 }
	 ,
	 {
	 	 path:new RegExp("^\/book\/$"),
	 	 expr:'#ads_book_index_left',
	 	 css:{marginTop:'10px', paddingLeft:'40px'},
	 	 html:'<iframe id="baiduSpFrame" border="0" vspace="0" hspace="0" marginwidth="0" marginheight="0" framespacing="0" frameborder="0" scrolling="no" width="120" height="240" src="http://spcode.baidu.com/spcode/spstyle/style2843.jsp?tn=xiongsir_sp&ctn=0&styleid=2843"></iframe>'
	 }
	 ,
	 {
	 	 path:new RegExp("^\/book\/[0-9]+\/$"),
	 	 expr:'#ads_book_show_right_b',
	 	 css:{marginTop:'10px'},
	 	 html:'<iframe id="baiduSpFrame" border="0" vspace="0" hspace="0" marginwidth="0" marginheight="0" framespacing="0" frameborder="0" scrolling="no" width="250" height="250" src="http://spcode.baidu.com/spcode/spstyle/style2851.jsp?tn=xiongsir_sp&ctn=0&styleid=2851"></iframe>'
	 }
	 ,
	 {
	 	 path:new RegExp("^\/book\/[0-9]+\/download/"),
	 	 expr:'#ads_book_download_right',
	 	 css:{},
	 	 html:'<iframe id="baiduSpFrame" border="0" vspace="0" hspace="0" marginwidth="0" marginheight="0" framespacing="0" frameborder="0" scrolling="no" width="300" height="250" src="http://spcode.baidu.com/spcode/spstyle/style2853.jsp?tn=xiongsir_sp&ctn=0&styleid=2853"></iframe>'
	 }
];


$(document).ready(function(){
	var _path = location.pathname;
	for (var i in _ads) {
		if (_ads[i].path.test(_path)) {
			$(_ads[i].expr).html(_ads[i].html).css(_ads[i].css);
		}
	}
});

