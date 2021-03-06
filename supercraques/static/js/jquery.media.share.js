(function($){

	$.fn.mediaShare = function(options){
		
		var _options = $.extend({
			facebookURL:'http://facebook.com/sharer.php?u={urlShared}&t={textShared}', 
			width:550,
			height:350,
			menubar:0,
			scrollbars:0,
			status:0,
			toolbar:0,
			resizable:0,
			location:0
  		}, options);
		
		var openwindow = function(url, urlShare, text){
			centeredY = (screen.height - _options.height)/2;
			centeredX = (screen.width - _options.width)/2;

			var windowFeatures =    'height=' + _options.height +
									',width=' + _options.width +
									',toolbar=' + _options.toolbar +
									',scrollbars=' + _options.scrollbars +
									',status=' + _options.status + 
									',resizable=' + _options.resizable +
									',location=' + _options.location +
									',menuBar=' + _options.menubar +
									',left=' + centeredX +
									',top=' + centeredY;
									
			window.open(url.replace("{urlShared}", urlShare).replace("{textShared}",text), "", windowFeatures);
		};
		
		return this.each(function(){
			$el = $(this);
			$el.unbind().bind('click', function(){
				text = $(this).attr("data-text");
				
				FB.ui({
					method: 'stream.publish',
					message: text,
					attachment: {
						media: [{
							type: 'image',
							src: '/media/img/logo_supercraques.png',
							href: 'http://supercraques.com.br'
						}]
					}
				});
				
				return false;				
			});
			
		});
	};

})(jQuery);