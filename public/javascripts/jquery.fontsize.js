// (c) 2009 yefe.


(function($) {
	$.fn.fontsize = function(target, options) {
		
	    $.fn.fontsize.defaults = {
	    	path: '/',
	    	sizes: {12:'小', 14:'中', 16:'大'},
	    	expires: 365,
	    	normal: 14
	    };
	    
	    // build main options before element iteration
	    var opts = $.extend($.fn.fontsize.defaults, options);
	    
	    // iterate and construct
	    return this.each(function()
	    {
	    	var container = $(this);
	    	var option_htmls = [];
	    	
	    	$.each(opts.sizes, function(k,v){
	    		option_htmls.push('<a href="#fontsize-'+k+'" class="fontsize'+k+'" v="'+k+'">'+v+'</a>');
	    	});
	    	container.html('文字：' + option_htmls.join('|'));
	    	
	    	function _setFontsize(s){
	    		if (!s) s = opts.normal;
	    		$('a', container).css('font-weight', 'normal');
	    		$('.fontsize'+s, container).css('font-weight', 'bold');
	    		$(target).css('font-size', s+'px');
	    		$.cookie('jquery_fontsize', s, {expires:opts.expires, path:opts.path});
	    	}
	    	
	    	$('a', container).click(function(){
	    		_setFontsize($(this).attr('v'));
	    		return false;
	    	});
	    	
	    	_setFontsize($.cookie('jquery_fontsize'));
	    });
	};
})(jQuery);

