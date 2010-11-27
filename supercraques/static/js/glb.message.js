// Plugin para exibir box de mensagem (erro ou sucesso)
(function($){
	$.fn.showMessage = function(options){
	    var options = jQuery.extend({
			          message: "Ops! Ocorreu um erro, por favor tente novamente.",
	              tipoAviso: "erro",
                timeout: 2000
	    }, options)

		if (options.response){

            _obj = options.response;
            options.tipoAviso = _obj.tipoAviso;
            if (_obj.tipoAviso == "erro") {
              _errors = _obj.errors.error;
              
              if($.typeOf(_errors)=='array') {
        				options.message = _errors[0].message;
        			} else {
        				options.message = _errors.message;
        			}
        		} else {
        		  options.message = _obj.message;
        		}
	    }

	    return this.each(function(){
	        var _imgSrc = (options.tipoAviso == "sucesso")?"/media/img/ico_sucesso.png":"/media/img/ico_erro.png";

	        var _html = '<div class="box-mensagem">'
	            +'<div class="topo-mensagem"><a href="#" class="btn-fechar"><img src="/media/img/ico_fechar.png" /></a></div>'
	            +'<div class="conteudo-mensagem">'

	            +'<img src="' + _imgSrc + '" alt="' + options.tipoAviso + '" /> '
	            +'<strong>'+options.message

	            +'</strong>'

	            +'</div>'
	            +'</div>';
	        $(_html).appendTo($(this));


			var _posIni = $(window).scrollTop();

			$('strong', $('.box-mensagem'))
				.html(options.message)
				.end()
				.fadeIn("slow");


			$('.box-mensagem').fadeIn("slow");

	        $('.btn-fechar').click(function(){
	            $('.box-mensagem').fadeOut("slow", function(){
					$('.box-mensagem').remove();
				});
				return false;
	        });

            //a mensagem some apos o timeout
            setTimeout(function() {
                $('.box-mensagem').fadeOut("slow", function(){
                    $('.box-mensagem').remove();
                });
            }, options.timeout);

	        return this;
	    });
	}
})(jQuery);
