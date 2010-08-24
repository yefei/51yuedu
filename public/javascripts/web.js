/* (c) 2010 intne.com */

var Web = {};

Web.location_uri = encodeURIComponent(location.pathname + location.search + location.hash);

//Web.site_search_items = {bookname:'书名', author:'作者', chapter:'章节'};


Web.copyToClipBoard = function(maintext) {
	if (window.clipboardData){
		window.clipboardData.setData("Text", maintext);
	} else if (window.netscape) {
		try {
			netscape.security.PrivilegeManager.enablePrivilege("UniversalXPConnect");
		} catch (e) {
			alert("您的firefox安全限制限制您进行剪贴板操作，请打开'about:config'将signed.applets.codebase_principal_support'设置为true'之后重试");
			return false;
		}
		
		var clip = Components.classes['@mozilla.org/widget/clipboard;1'].createInstance(Components.interfaces.nsIClipboard);
		if (!clip) return;
		var trans = Components.classes['@mozilla.org/widget/transferable;1'].createInstance(Components.interfaces.nsITransferable);
		if (!trans) return;
		trans.addDataFlavor('text/unicode');
		var str = new Object();
		var len = new Object();
		var str = Components.classes["@mozilla.org/supports-string;1"].createInstance(Components.interfaces.nsISupportsString);
		var copytext=maintext;
		str.data=copytext;
		trans.setTransferData("text/unicode",str,copytext.length*2);
		var clipid=Components.interfaces.nsIClipboard;
		if (!clip) return false;
		clip.setData(trans,null,clipid.kGlobalClipboard);
	}
	alert("复制成功！");
	return false;
};

//刷新页面
Web.relocation = function (url) {
	if (url == undefined) {
		var url = location.href;
		url = url.substr(0, url.indexOf('?'));
	}
	location.href = url + "?" + (+new Date);
};

// 载入中信息
Web.loading_html = function(text){
	return '<div style="background:url(/public/images/loading_small.gif) left no-repeat;padding-left:20px;">'+
			(typeof text == 'undefined' ? '载入中...' : text) + '</div>';
};

Web.formatDate = function(dt){
	var a = dt.split(" ");
	var a1 = a[0].split("-");
	var a2 = a[1].split(":");
	return new Date(a1[0], a1[1] - 1, a1[2], a2[0], a2[1]);
};

Web.shortDate = function(dt){
	var d = Web.formatDate(dt);
	var n = new Date();
	
	var
		d_y = d.getFullYear(),
		d_m = d.getMonth()+1,
		d_d = d.getDate(),
		d_h = d.getHours(),
		d_i = d.getMinutes();
	
	var
		n_y = n.getFullYear(),
		n_m = n.getMonth()+1,
		n_d = n.getDate(),
		n_h = n.getHours(),
		n_i = n.getMinutes();
	
	if (n_y > d_y) {
		return d_y + '年' + d_m + '月';
	} else if (n_m > d_m) {
		return d_m + '月' + d_d + '日';
	} else if (n_d > d_d) {
		if (n_d-d_d == 1) return '昨天' + d_h + ':' + d_i;
		if (n_d-d_d == 2) return '前天' + d_h + ':' + d_i;
		return '本月' + d_d + '号' + d_h + '点';
	} else if (n_h > d_h) {
		return '今日' + d_h + ':' + d_i;
	} else {
		var m = n_i - d_i;
		return  m > 0 ? (m+'分钟前') : '刚刚';
	}
};

// 生日选择
Web.birthday = function(id) {
	setTimeout(function(){
		$(id).datepicker({dateFormat:'yy-mm-dd',changeMonth:true,changeYear:true,yearRange:'-100:+100',minDate:'-100y',maxDate:'-5y'});
	}, 100);
};

//延时消失
Web.slideTimeout = function(id, timeout) {
	if (id == undefined) return;
	if (timeout == undefined) timeout = 2000;
	setTimeout(function(){$(id).hide("fast");}, timeout);
};

Web.ajax_defaults = {
	cache: false,
	type: 'POST',
	async: true,
	dataType: 'json',
	showError: false,
	showAjaxError: true
};
Web._ajax_error_dialog_object = null;
Web.ajax = function (api, params, callback, options)
{
	if (typeof params == 'function') {
		callback = params;
		params = {};
	}
	
	var opts = $.extend(Web.ajax_defaults, options);
	
	$.ajax({
		async: opts.async,
		cache: opts.cache,
		type: opts.type,
		url: '/$'+api+'.json',
		dataType: opts.dataType,
		data: params,
		success: function(r)
		{
			if (r.success) {
				callback(r.response, true, null);
			} else {
				if (opts.showAjaxError) Web.showAjaxFormError(r.error);
				callback(r.response, false, r.error);
			}
		},
		error: function(XMLHttpRequest, textStatus, errorThrown)
		{
			if (!opts.showError) return;
			if (Web._ajax_error_dialog_object == null) {
				$('body').append('<div id="web_error_dialog" style="display:none;"></div>');
				Web._ajax_error_dialog_object = $('#web_error_dialog');
				Web._ajax_error_dialog_object.dialog({
					title:"网站发生错误",
					modal: true,
					autoOpen:false,
					width:500,
					resizable:false,
					buttons: {'关闭': function() {$(this).dialog('close');Web.relocation();}}
				});
			}
			Web._ajax_error_dialog_object.html(
				'<textarea style="width:100%;height:300px">'+
				'API: ' + api + 
				'\nReadyState: ' + XMLHttpRequest.readyState + 
				'\nStatus: ' + XMLHttpRequest.status + 
				'\nErrorThrown: ' + errorThrown + 
				'\nResponseText: ' + XMLHttpRequest.responseText.replace(/</g,'&lt;').replace(/>/g,'&gt;') + '</textarea>' +
				'<p>请将错误信息报告给: support@ichuzhou.cn</p>').dialog('open');
		}
	});
};

Web._show_ajax_form_error_dialog_object = null;
Web.showAjaxFormError = function(error){
	if (Web._show_ajax_form_error_dialog_object == null) {
		$('body').append('<div id="web_ajax_form_error_dialog" style="display:none;"></div>');
		Web._show_ajax_form_error_dialog_object = $('#web_ajax_form_error_dialog');
		Web._show_ajax_form_error_dialog_object.dialog({
			title:"错误",
			modal: true,
			autoOpen:false,
			width:500,
			resizable:false,
			buttons: {'确定': function() {$(this).dialog('close');}}
		});
	}
	
	var h = '';
	
	if (typeof error == 'string') {
		if (error == 'login_required') error = '请先登陆';
		h = '<p>' + error + '</p>';
	} else {
		h = '<ul>';
		$.each(error, function(k,v){
			//h += '<dt>' + k + '</dt>';
			$.each(v, function(_k,_v){
				h += '<li>' + _v + '</li>';
			});
		});
		h += '</ul>';
	}
	
	Web._show_ajax_form_error_dialog_object.html(h).dialog('open');
};

Web.tip = function(content){
	var id = 'web_tip_dialog' + (+new Date);
	$('body').append('<div id="'+id+'" style="display:none;">'+content+'</div>');
	var tip = $('#'+id);
	tip.dialog({
		title:"提示",
		modal: true,
		autoOpen:true,
		width:300,
		minHeight:20,
		resizable:false,
		beforeClose:function(){return false;}
	});
	return tip;
};

Web.tipClose = function(tip, timeout){
	if (typeof timeout != 'undefined') {
		return setTimeout(function(){Web.tipClose(tip);}, timeout);
	}
	tip.dialog('option', 'beforeClose', null);
	tip.dialog('close');
	tip.remove();
};

Web.confirm = function(content, ok_callback, close_callback){
	var id = 'web_confirm_dialog' + (+new Date);
	$('body').append('<div id="'+id+'" style="display:none;">'+content+'</div>');
	var tip = $('#'+id);
	tip.dialog({
		title:"提示",
		modal: true,
		autoOpen:true,
		width:350,
		minHeight:120,
		resizable:false,
		closeOnEscape:false,
		beforeClose:function(){tip.remove();try{close_callback();}catch(e){}},
		buttons: {
			'取消': function() {tip.dialog('close');},
			'确定': function() {tip.dialog('close');ok_callback();}
		}
	});
};

Web.action = function(api, confirm_text, data, callback){
	if (typeof data == 'undefined') data = {};
	Web.confirm(confirm_text, function(){
		var tip = Web.tip('正在执行...<br/><img src="/public/images/loading_bar.gif" />');
			tip.dialog('option', 'width', 220);
		Web.ajax(api, data, function(r, success){
			if (success) try{callback(r);}catch(e){}
			Web.tipClose(tip);
		});
	});
};

Web.action2 = function(api, data, callback){
	if (typeof data == 'undefined') data = {};
	var tip = Web.tip('正在执行...<br/><img src="/public/images/loading_bar.gif" />');
	tip.dialog('option', 'width', 220);
	Web.ajax(api, data, function(r, success){
		if (success) try{callback(r);}catch(e){}
		tip.html('完成');
		Web.tipClose(tip, 1000);
	});
};

//轮询查询
Web.ajaxCheck = function(api, query, callback, infocallback, interval){
	if (typeof infocallback == 'undefined') infocallback = function(){};
	if (typeof interval == 'undefined') interval = 1000;
	var t = {};
	t._listen_loop_geting = false; // 正在查询服务器
	t._listen_loop_lastval = ''; // 最后查询时的字符串
	return setInterval(function(){Web._ajaxCheck_listen(api, query, callback, infocallback, t);}, interval);
};
Web._ajaxCheck_listen = function(api, query, callback, infocallback, t){
	if (t._listen_loop_geting) return;
	var v = query();
	if (v == t._listen_loop_lastval) return;
	if (v == '') {
		t._listen_loop_lastval = '';
		infocallback('');
		return;
	}
	infocallback('查询中...');
	t._listen_loop_geting = true;
	t._listen_loop_lastval = v;
	Web.ajax(api, v, function(data){
		if (data) {
			callback(data);
		} else {
			infocallback('');
		}
		t._listen_loop_geting = false;
	});
};


Web.bbcode2html = function(str){
	str = str.replace(/\[user=(\d+?)\](.*?)\[\/user\]/ig, '<a href="/space/$1/" target="_blank">$2</a> ');
	return str;
};

Web._open_window_caches = {};
Web.openWindow = function(url, name, w, h){
	if (Web._open_window_caches[name] && !Web._open_window_caches[name].closed) {
		Web._open_window_caches[name].focus();
		return;
	}
	if (typeof w == 'undefined') w = 600;
	if (typeof h == 'undefined') h = 350;
	var x = (window.screen.width - w) / 2;
	var y = (window.screen.height - h) / 2;
	Web._open_window_caches[name] = window.open(url, name, 'height='+h+',width='+w+',top='+y+',left='+x+',toolbar=0,menubar=0,scrollbars=0,resizable=1,location=0,status=1');
	Web._open_window_caches[name].focus();
};

Web.message =
{
	open: function(user_id){
		Web.openWindow('/my/message/'+user_id+'/?popup=1','account_message'+user_id);
	}
};

Web.init = function (){
	// 登录,退出
	if (location.pathname != '/my/login/') {
		$.each([$('.href_login'), $('.href_logout')], function(k,v){
			v.attr('href', v.attr('href') + '?next=' + Web.location_uri);
		});
	}
	// 搜索
	/*
	var s = $('#site_search_form');
	if (s.is(':visible')) {
		var id = 'id' + (+new Date);
		$('input:text', s).css('border-left','0').before('<input type="button" value="全站" id="'+id+'" class="siteHeaderSearch_item" />');
		var h = '';
		$.each(Web.site_search_items, function(k,v){
			h += '<li><a href="/search/'+k+'/">'+v+'</a></li>';
		})
		s.prepend('<div id="siteHeaderSearch_item"><ul><li><a href="/search/">全站</a></li>'+h+'<ul></div>');
		$('#'+id).click(function(){
			$('#siteHeaderSearch_item').show('blind');
			return false;
		});
		$('#siteHeaderSearch_item a').click(function(){
			s.attr('action', $(this).attr('href'));
			$('#'+id).val($(this).text());
			$('input:text', s).focus();
			return false;
		});
		$(document).mouseup(function(){
			if ($('#siteHeaderSearch_item').is(':visible')) $('#siteHeaderSearch_item').hide();
		});
	}
	*/
};

$(document).ready(Web.init);
