// Plugin para exibir box de mensagem (erro ou sucesso)
(function($){
	$.fn.textFormatter = function(options){
	    var options = jQuery.extend({
			    length: 10,
	        end: "..."
	    }, options);
		
	    return this.each(function(){
            var _str = $(this).html();
            if(_str!='' && _str.length >= options.length) {
                var _newStr = _str.substr(0, options.length) + options.end;
                $(this).html(_newStr);
            }

	        return this;
	    });
	}
})(jQuery);


