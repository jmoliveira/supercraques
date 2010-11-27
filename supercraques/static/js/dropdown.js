/*
 * @requires jquery.js
 */
(function($) {

	var methods = {
		init : function(options) {

            var $this = $(this);

			var settings = {
				data : [],
				itemsByLine : 1,
				onClickItem : null, // essa funcao deve receber como parametro o valor "rel" que esta no item
				onClickReset : null,
				defaultHtmlSelector : "ver todos",
				updateSelector: null
			};

			if (options) {
				$.extend(settings, options);
			}

			$(this).show();

			if (settings.data) {

                var $listaBase = $this.children("ul");
                var $templateBase = decodeURI($this.children(".dropdown-template").html());
                $.template( "tItem", $templateBase );
                $listaBase.html($.tmpl( "tItem", settings.data ));
                $(".dropdown-template").hide();
                //adicionar classe ao ultimo item da linha
                var indexCanto = settings.itemsByLine;
                if (settings.itemsByLine >=  settings.data.length) {
                	indexCanto = settings.data.length;
                }
                $listaBase.children("li:nth-child("+ indexCanto +"n)").addClass("ultimo-item");
                $(".dropdown-todos").show();
			}

            widthMax = 0;
			// calcula a largura dependente da quantidade de itens
           	if (settings.itemsByLine >= settings.data.length) {
				widthMax = methods.calculateWidth($("li:eq(0)", $listaBase)) * (settings.data.length - 1);
			} else {
				widthMax = methods.calculateWidth($("li:eq(0)", $listaBase)) * (settings.itemsByLine - 1);
			}
            
            widthMax += methods.calculateWidth($(".ultimo-item", $listaBase));
   			
            $(this).css("width", widthMax + "px");
            
            $(this).hide();
            
            //indica a partir de qual item teremos a indicao de ultima linha
            var lastLineIndicator = 0;
    
            if(settings.itemsByLine > 1){
		     
               lastLineIndicator = (Math.floor((settings.data.length-1)/settings.itemsByLine) * settings.itemsByLine);

	        }
		
            //adiciona class para ultima-linha
            $("li", $listaBase).filter(":eq("+ lastLineIndicator + "), :gt(" + lastLineIndicator + ")").addClass("ultima-linha");
            
			methods.bindEvents(this, settings);
		},
		calculateWidth : function(theDiv) {

			var totalWidth = 0;

			if (theDiv.size() > 0) {

				totalWidth += theDiv.width();
				totalWidth += parseInt(theDiv.css("padding-left"), 10) + parseInt(theDiv.css("padding-right"), 10); // Total Padding Width
				totalWidth += parseInt(theDiv.css("margin-left"), 10) + parseInt(theDiv.css("margin-right"), 10); // Total Margin  Width

				totalWidth += parseInt(theDiv.css("borderLeftWidth"), 10) + parseInt(theDiv.css("borderRightWidth"), 10); // Total Border Width
			}
			return totalWidth;
		},
		// configura os eventos do dropdown
		bindEvents : function($context, settings) {

			var $selector = $(".filtros-atual-label", $context.siblings(".filtros-grupo-botao"));
			methods.updateSelector($selector, settings);

			$.each($context.children("ul").children("li"), function(i, item) {

				$(this).bind('click', function() {

					var value = $(this).attr("rel");
					methods.updateSelector($selector, settings, value);

                    $(".dropdown-filtro").hide();

					if (settings.onClickItem) {
						settings.onClickItem.call(this, value);
					}
				});

				// configura o efeito de hover dos itens do dropdown
				$(this).bind('mouseenter mouseleave', function(event) {

					if (event.type == 'mouseleave') {
						$(this).removeClass("mouseover");
					}
					if (event.type == 'mouseenter') {
						$(this).addClass("mouseover");
					}

				});

			});

			// configura o efeito toogle do dropdown de times
			$(".filtros-grupo-botao", $context.parent()).unbind('click').bind('click', function(event) {

                if($(this).next().is(":hidden")){
                    $(".dropdown-filtro").hide();
                    $(".filtros-grupo-botao").removeClass("filtros-grupo-botao-active");
                    $(this).next().show();
                    $(this).addClass("filtros-grupo-botao-active");

                }else{

                    $(this).next().hide();
                    $(this).removeClass("filtros-grupo-botao-active");

                }
			});

			$(".dropdown-todos", $context).unbind('click').bind('click', function(ev){

                if (settings.onClickReset) {
					settings.onClickReset.call();
				}

				methods.updateSelector($selector, settings);
                $(".dropdown-filtro").hide();

			});
		},
		// atualiza os valores o filtro para o atual selecionado
		updateSelector : function($selector, settings, value) {

			if (settings && settings.updateSelector) {
				settings.updateSelector.call(this, $selector, value);
			} else {
				if (value) {
					$selector.html($('li[rel=' + value + ']').html() + ' <div>' + value + '</div>');
				} else {
					$selector.html(settings.defaultHtmlSelector);
				}
			}
		}
	};

	$.fn.DropdownMercado = function(method) {

		if (methods[method]) {

			return methods[method].apply(this, Array.prototype.slice.call(
					arguments, 1));

		} else if (typeof method === 'object' || !method) {

			return methods.init.apply(this, arguments);

		} else {

			$.error('Method ' + method + ' does not exist on Dropdown');

		}

	};

})(jQuery);
