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
                
                this.isOpenDesafio = false;
                this.isOpenMeusCards = false;
                this.$patrimonio = $("#fin-patrimonio",$this);
                this.$qtdCards = $("#qtdCards", $this);
                this.cards = this.options.cards;
                this.callback = callback || false;
                this.$desafioArea = $("#desafios-area");
                this.$desafioContent = $("#desafio-content");
                this.$meusCardsArea = $("#meus-cards-area");
                this.$meusCardsContent = $("#meus-cards-content");
                this.$escolhaAmigo = $("#escolha-amigo");
                this.$atletaCardTemplate = $("#atletaCardTemplate");
                // this.$opaco = $("#glb-corpo, #glb-doc");
                
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
                
                $("#desafiar-amigos-menu").click(function() {
                    // self.$opaco.addClass("opacity1");
                    if (self.isOpenMeusCards == true){self.$meusCardsArea.hide();self.isOpenMeusCards = false};
                    if (self.isOpenDesafio == false) {
                      $.ajax({
                          url: "/atletas_card.json",
                          success: function(data) {
                            self.$desafioContent.empty(); self.opaco(1);
                            self.$atletaCardTemplate.tmpl(data).appendTo(self.$desafioContent);
                            $(".card", self.$desafioContent).addClass("cardDesafio");
                            self.$desafioArea.show();
                            self.isOpenDesafio = true;
                          },
                          error:function(x,e) {
                            $("#glb-doc").showMessage();
                          }
                        });
                     }else{
                        self.$desafioArea.hide();
                        //self.$escolhaAmigo.hide()
                        // self.$opaco.removeClass("opacity1");
                        self.isOpenDesafio = false; 
                     }
                   
                    return false;
                });
                
                $("#meus-cards-menu").click(function() {
                  // self.$opaco.addClass("opacity1");
                  if (self.isOpenDesafio == true){self.$desafioArea.hide();self.isOpenDesafio = false};
                    if (self.isOpenMeusCards == false) {
                      $.ajax({
                          url: "/atletas_card.json",
                          success: function(data) {
                            self.$meusCardsContent.empty();
                            self.$atletaCardTemplate.tmpl(data).appendTo(self.$meusCardsContent);
                            $(".card", self.$meusCardsContent).addClass("cardMeusCards");
                            self.$meusCardsArea.show();
                            self.isOpenMeusCards = true;
                          },
                          error:function(x,e) {
                            $("#glb-doc").showMessage();
                          }
                        });
                     }else{
                        self.$meusCardsArea.hide();
                        self.isOpenMeusCards = false;
                        // self.$opaco.removeClass("opacity1"); 
                     }
                   
                    return false;
                });
                
                $(".cardDesafio").live("click", function() {
                    $("#card_id_selecionado", self.$escolhaAmigo).val($(this).attr("data"));
                    self.$desafioContent.empty();
                    self.$desafioContent.append($(this));
                    self.opaco(2);
                    $clone  = $('#escolha-amigo');
                    self.$desafioContent.append($clone);
                    $clone.show();
                    
                    return false;
                });
                
                $(".cardMeusCards").live("click", function() {
                    $("#glb-doc").showMessage({message: "Card neoneo", tipoAviso: "sucesso"});
                    
                    return false;
                });
                

                $(".btn-escolher-card").live("click", function() {
                    desafio_id = $(this).attr("data");
                    
                    $.ajax({
                        url: "/atletas_card.json",
                        success: function(data) {
                          self.$meusCardsContent.empty();
                          self.$atletaCardTemplate.tmpl(data).appendTo(self.$meusCardsContent);
                          $(".card", self.$meusCardsContent).addClass("cardEscolherCards").attr("desafio_id", desafio_id);
                          self.$meusCardsArea.show();
                          self.isOpenMeusCards = true;
                        },
                        error:function(x,e) {
                          $("#glb-doc").showMessage();
                        }
                      });
                     
                      return false;
                });
                
            
            
                $(".cardEscolherCards").live("click", function() {
                    card_id = $(this).attr("data");
                    desafio_id = $(this).attr("desafio_id");
                    $.ajax({
                          method: 'post',
                          url: "/desafio/"+ desafio_id + "/card/"+ card_id + "/aceitar",
                          success: function(data) {
                            $("#glb-doc").showMessage({response:data});
                            window.location = "/home";
                          },
                          error:function(x,e) {
                            $("#glb-doc").showMessage();
                          }
                     });
                    
                    return false;
                });

                    
                $( "#project" ).autocomplete({
                    minLength: 2,
                    source: "/fb/friends.json",
                    focus: function( event, ui ) {
                      $( "#project" ).val( ui.item.name );
                      return false;
                    },
                    select: function( event, ui ) {
                      $( "#project" ).val("");
                      $( "#project-id" ).val( ui.item.id );
                      $( "#project-description" ).html( ui.item.name );
                      $( "#project-icon" ).html('<img height="40" width="40" border="0"  src="https://graph.facebook.com/'+ ui.item.id + '/picture" >');
                      return false;
                    }
                  })
                  .data( "autocomplete" )._renderItem = function( ul, item ) {
                      text_item = '<a>';
                      text_item +=  '<img height="40" width="40" border="0"  src="https://graph.facebook.com/'+ item.id + '/picture" >';
                      text_item +=  item.name;
                      text_item += '</a>';
                      return $("<li></li>").data("item.autocomplete", item).append(text_item).appendTo(ul);
                   };
               
                   $('#btn-desafiar-amigo').live("click",function(){
                      usuario_id = $( "#project-id", self.$escolhaAmigo).val();
                      card_selecionado_id = $("#card_id_selecionado", self.$escolhaAmigo).val();
                      if (usuario_id != "") {
                        $.ajax({
                            url: "/desafio/card/" + card_selecionado_id + "/usuario_desafiado/"+ usuario_id + "/desafiar",
                            success: function(data) {
                                $("#glb-doc").showMessage({response:data});
                                window.location = "/home";
                            },
                            error:function(x,e) {
                              $("#glb-doc").showMessage();
                            }
                          });
                      }else {
                          $("#glb-doc").showMessage();
                      }
                    });
                
            },
            
       
            
            opaco: function(etapa){
                if (etapa == 1) {
                  $("#desafio-escolher-card").removeClass("opacity");
                  $("#desafio-escolher-amigo").addClass("opacity");  
                }else{
                  $("#desafio-escolher-card").addClass("opacity");
                  $("#desafio-escolher-amigo").removeClass("opacity");
                }
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
            
            exibirDesafios:function(){
              var self = this;
              // buscar e exibe os desafios
              var $boxDesafios = $("#box-desafios");
              $boxDesafios.addClass("ui-autocomplete-desafio-loading");
              var $boxDesafiosTemplate = $("#box-desafios-template");
              var $desafiosVazioArea = $("#desafios-vazio-area");
              $desafiosVazioArea.hide()
              
              $.ajax({
                  url: "/desafio/todos.json",
                  success: function(result) {
                      if (result.data.length > 0) {
                        // console.log("desafios-vazio-area");
                        $boxDesafiosTemplate.tmpl( result.data ).appendTo($boxDesafios);
                      }else{
                        // console.log("desafios-vazioasasa");
                        $desafiosVazioArea.show();
                      }
                      
                      $boxDesafios.removeClass("ui-autocomplete-desafio-loading");
                  },
                  error:function(x,e) {
                    $("#glb-doc").showMessage();
                    $boxDesafios.removeClass("ui-autocomplete-desafio-loading");
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
