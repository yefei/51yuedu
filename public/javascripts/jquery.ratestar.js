// $Id$

(function($) {
	$.fn.ratestar = function(options) {
		
	    $.fn.ratestar.defaults = {
	    	api: null,
	    	id: 0,
	    	confirm_fun: function(s){},
	    	none_image: '/public/images/rate_none.gif',
	    	light_image: '/public/images/rate_light.gif',
	    	dark_image: '/public/images/rate_dark.gif',
	    	sp_image: '/public/images/rate_sp.gif',
	    	min_score: -5,
	    	max_score: 5
	    };
	    
	    // build main options before element iteration
	    var opts = $.extend($.fn.ratestar.defaults, options);
	    
	    // iterate and construct
	    return this.each(function()
	    {
	    	var container = $(this);
	    	var stararea_id = container.attr('id') + '_stararea';
	    	
	    	var h = '<div id="'+stararea_id+'">';
	    	for (var i=opts.min_score; i<0; i++) {
	    		h += '<img class="ratestar_dark" alt="'+i+'" src="'+opts.none_image+'" />';
	    	}
	    	h += '<img src="'+opts.sp_image+'" />';
	    	for (var i=1; i<=opts.max_score; i++) {
		    	h += '<img class="ratestar_light" alt="'+i+'" src="'+opts.none_image+'" />';
		    }
	    	h += '<div>评分: <span>0</span></div></div>';
	    	container.html(h);
	    	
	    	var score_view = $('span', container);
	    	var score = 0;
	    	
	    	var mouse_out = function(){
	    		$('img.ratestar_dark', container).attr('src',opts.none_image);
	    		$('img.ratestar_light', container).attr('src',opts.none_image);
	    		score = 0;
	    		score_view.text(score);
	    	};
	    	
	    	$('img.ratestar_dark', container).hover(function(){
	    		var t = $(this);
	    		score = parseInt(t.attr('alt'));
	    		var _t = t;
	    		for (var i=score;i<0;i++) {
	    			_t.attr('src',opts.dark_image);
	    			_t = _t.next();
	    		}
	    		score_view.text(score);
	    	},mouse_out);
	    	
	    	$('img.ratestar_light', container).hover(function(){
	    		var t = $(this);
	    		score = parseInt(t.attr('alt'));
	    		var _t = t;
	    		for (var i=1;i<=score;i++) {
	    			_t.attr('src',opts.light_image);
	    			_t = _t.prev();
	    		}
	    		score_view.text(score);
	    	},mouse_out);
	    	
	    	$('img', container).click(function(){
	    		var s = score;
	    		if (s == 0) {
	    			alert('请将鼠标移至需要评分的星星上然后点击。');
	    			return false;
	    		}
	    		if (s < opts.min_score || s > opts.max_score) {
	    			alert('您选择的分数不正确。');
	    			return false;
	    		}
	    		$('#'+stararea_id).hide().after(
	    			'<div>' + opts.confirm_fun(s) +
	    			'<div><a class="ok_button" href="#">确定</a> | <a class="cancel_button" href="#">取消</a></div></div>'
	    		);
	    		$('.cancel_button', container).click(function(){
	    			$(this).parent().parent().remove();
	    			$('#'+stararea_id).show();
	    			return false;
	    		});
	    		$('.ok_button', container).click(function(){
	    			$(this).parent().parent().remove();
	    			$('#'+stararea_id).after('<span class="sending">提交中，请稍候...</span>');
	    			Web.ajax(opts.api, {'id':opts.id,'rate':s}, function(r, success){
	    				if (success) {
    						alert('评分成功！');
    						Web.relocation();
    						return;
    					}
    					$('.sending', container).remove();
    					$('#'+stararea_id).show();
	    			});
	    			return false;
	    		});
	    		return false;
	    	});
	    });
	};
})(jQuery);

