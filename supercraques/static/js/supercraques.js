(function($) {
    $.extend($, {
        barra: {
          
            $container: null,
            statusBar: "open",
            url : "/supercraque.json",
            options : {
                url: "/supercraque.json",
                cartoleta_inicial: 100,
                qtdCards: []
            },
            
            init:function($this, options, autoload, callback){
                $.extend(this.options, options);
                
                this.$patrimonio = $("#fin-patrimonio",$this);
                this.$qtdCards = $("#qtdCards", $this);
                this.cards = this.options.cards;
                this.callback = callback || false;
                var self = this;
                
                if (autoload){
                    this.load();
                }

                $container = $this;
                this.createEvents();

                return this;
            },
            createEvents:function(){
                var self = this;
                // minimizando barra
                $(".max .barra", this.$container).click(function(){
                    $("div.max", self.$container).hide(); $("div.min", self.$container).show();
                    self.statusBar = "close";
                    return false;
                });
                // maxmizando barra
                $(".min .barra", this.$container).click(function(){
                    $("div.min", self.$container).hide(); $("div.max", self.$container).show();
                    self.statusBar = "open";
                    return false;
                });
            },
            
            load: function(){
                var self = this;
                
                $.ajax({
                    method: 'get',
                    url: self.options.url,
                    data: {},
                    cache:false,
                    success: function(response){
                        data =  response
                        if (data.errors){
                            $('#glb-doc').showMessage({response:data, timeout:2000});
                        }
                        else{
                            self.fill(data);
                        }
                    },
                    error: function(XMLHttpRequest, textStatus, errorThrown) {
                       $('#glb-doc').showMessage({response:JSON.parse(response), timeout:4000 });
                    }
                });
                
            },
            
            round:function(val){
                return Math.round((val * 100))/100;
            },

            descartarCard:function($elem){
              var self = this;
              atleta_id = $elem.attr("data");
              $.ajax({
                  method: 'post',
                  url: "/atleta/"+ atleta_id + "/descartar",
                  success: function(data) {
                    $("#glb-doc").showMessage({response:data});
                    if (data.tipoAviso == "sucesso") {
                      $elem.removeClass("btn-descartar-card"); $elem.addClass("btn-comprar-card");
                      self.load();
                    }
                  },
                  error:function(x,e) {
                    $("#glb-doc").showMessage();
                  }
                });

            },

            comprarCard:function($elem){
              var self = this;
              atleta_id = $elem.attr("data");
              $.ajax({
                  method: 'post',
                  url: "/atleta/"+ atleta_id + "/comprar",
                  success: function(data) {
                    $("#glb-doc").showMessage({response:data});
                    if (data.tipoAviso == "sucesso") {
                      $elem.removeClass("btn-comprar-card"); $elem.addClass("btn-descartar-card");
                      self.load();
                    }
                  },
                  error:function(x,e) {
                    $("#glb-doc").showMessage();
                  }
                });
            },
            
            fill: function(supercraque){
                var self = this;
                this.patrimonio = parseFloat(supercraque.patrimonio);
                this.qtdCards = supercraque.qtdCards;
                this.$patrimonio.html("<span class='patrimonio'></span>$ "+this.round(this.patrimonio));
                this.$qtdCards.html(this.qtdCards);
            }       
            
        }
    });
    
    /**
    * Inicializa plugin barra
    */
    $.fn.barra = function(options, autoload, callback){
        return $.barra.init($(this), options, autoload, callback);
    };
    
})(jQuery);
