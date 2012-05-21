$(function() {
		initEditor('codemirror');
 		flickrSearch('#images', 'animated+gif'); 		
});

function flickrSearch(domId, tags)
{
	var url = "http://api.flickr.com/services/rest/?method=flickr.photos.search&licence=7&sort=interestingness-desc&api_key=bbb6179d48df4fdda503d5188913ac8d&tags="+tags+"&privacy_filter=1&safe_search=1&extras=url_sq,url_t,url_s,url_q,url_m,url_n,url_z,url_c,url_l,url_o&per_page=50";
	$.getJSON(url + "&format=json&jsoncallback=?", function(data){
	    $.each(data.photos.photo, function(i,item){	    
		if ((item.url_o)&&(item.url_o.indexOf(".gif")===item.url_o.length-4))		
	    	{
	    		$("<img/>",{src:item.url_t}).appendTo("#images").wrap($('<li></li>',{class:'span2'})).wrap($('<a></a>',{href:location.href.substring(0, location.href.indexOf('/', 14))+'/'+item.url_o,class:'thumbnail'}));
	    	}
	    });
	});
}


function initEditor(domId)
{
	var editor = CodeMirror.fromTextArea(document.getElementById(domId), 
 			{
 				lineNumbers: true,
 				onChange:function(editor){applyStyle(editor.getValue())}
 			}
 			);
	applyStyle(editor.getValue());
}


function applyStyle(css)
{
	
	$('#spriteStyle').remove();
	$("<style>",{
		type:"text/css",
		id:"spriteStyle",
		html:css
	}).appendTo("head");
}


