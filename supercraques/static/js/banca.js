var TIMES = { mercado_nacional:[], mercado_internacional:[]};
var executouFiltroPorHash = false;


$(document).ready(function() {

  // recupera as equipes
	$.ajax({
		method: 'get',
		url: "/equipes.json",
		success: function(response){
			carregarTimes(response);
		},
		async: false
	});

  // carrega os selects
  loadSelects();
    
  // embeleze de fonte
  if(!$.browser.msie) {
      Cufon.replace('.cufon');
      Cufon.now();
  }
    
});




function resetFiltros() {
  $("#filtroTime").attr("value", "");
  $("#filtroPosicao").attr("value", "");
}


function configurarFiltroComHash() {
  var re = new RegExp("#/(inter)?nacional(/.*)?");

  var match = re.exec(window.location.hash);

  if (match && match.length > 2) {
    var timeUrl = match[2];

    if (timeUrl) {
      var listaTimes = TIMES.mercado_nacional;

      var selecionados = $.grep(listaTimes, function(elem, index) {
        return elem.slug == timeUrl.substring(1);
      });

      if (selecionados && selecionados.length) {
          $("li.dropdown-time[rel="+selecionados[0].nome_popular+"]").trigger("click");
          return;
      }
    }
  }

  filtrar();

}


function carregarTimes(listas) {
	TIMES.mercado_nacional = listas.nacional;
}


function selecionarNomeTime(nomeTime) {
	var timeID = null;
	var timeSlug = null;
	
	var times = TIMES.mercado_nacional;

	for (var i = 0; i < times.length; i++) {
		if (times[i].nome_popular == nomeTime) {
			timeID = times[i].equipe_id;
			timeSlug = times[i].slug;
			break;
		}
	}

	if (timeID) {
		$("#filtroTime").attr("value", timeID);
	}

	filtrar();
}


function selecionarPosicao(posicao) {
	$("#filtroPosicao").attr("value", posicao);
	filtrar();
}

function executarFiltro() {

	if (!executouFiltroPorHash) {
		configurarFiltroComHash();
		executouFiltroPorHash = true;
	} else {
		filtrar();
	}
}

function filtrar() {
	var equipe_id = $("#filtroTime").attr("value");
	var posicao = $("#filtroPosicao").attr("value");
	exibeListaJogadores(equipe_id, posicao);
}

function formatUrl(equipe_id, posicao) {
   var urlService = equipe_id? "/equipe/"+equipe_id: "";
   urlService += posicao? "/posicao/"+posicao: "";
   urlService += "/atletas.json"
   return urlService
}


function exibeListaJogadores(equipe_id, posicao) {
    var $contenTemplate = $("#content-template-banca");
    var $cardTemplate = $("#cardTemplate");
    var $contenLoading = $("#content-loading");

    if (equipe_id || posicao) {
       $contenTemplate.empty();
       $contenLoading.show();
       $.ajax({
          url: formatUrl(equipe_id, posicao),
          success: function(data) {
              $contenLoading.hide();
              $cardTemplate.tmpl( data ).appendTo($contenTemplate);
          },
          error:function(x,e) {
              $contenLoading.hide();
              $("#glb-doc").showMessage();
          }
        });
    } else {
      $contenLoading.hide();
      $contenTemplate.html("");
    }
    
  
}


function exibeListaVazia() {
	$contenTemplate.hide()
	$("tr.listavazia").show();
}


function filtroContemTimeSelecionado() {
	return $("#filtroTime").attr("value") != "";
}

function todosTimes() {
	$("#filtroTime").attr("value", "");
	filtrar();
}

function todasPosicoes() {
	$("#filtroPosicao").attr("value", "");
	filtrar();
}

function loadSelects() {
  
	resetFiltros();
	
	$("#dropdown-times").DropdownMercado({data: TIMES.mercado_nacional,
			       	   				  itemsByLine: 5,
			       	   				  onClickItem: selecionarNomeTime,
			       	   				  onClickReset: todosTimes,
			       	   				  defaultHtmlSelector: 'todos os <strong>times</strong>'
			           				 });
 
  $("#dropdown-posicoes").DropdownMercado({
                                            data: [{sigla: "GOL", nome_completo: "goleiros"},
                                                   {sigla: "ZAGA", nome_completo: "zagueiros"},
                                                   {sigla: "LATERAL", nome_completo: "laterais"},
                                                   {sigla: "MEIO-CAMPO", nome_completo: "meio-campistas"},
                                                   {sigla: "ATAQUE", nome_completo: "atacantes"}
                                                  ],
                                            itemsByLine: 2,
				       	   				  onClickItem: selecionarPosicao,
				       	   				  onClickReset: todasPosicoes,
				       	   				  defaultHtmlSelector: 'todas as <strong>posi&ccedil;&otilde;es</strong>',
				       	   				  updateSelector: atualizarSeletorPosicao
				           				 });

    executarFiltro();
}

function atualizarSeletorPosicao($seletor, value) {
	if (value) {
		$seletor.html($('li[rel=' + value + ']').html());
	} else {
		$seletor.html("todas as <strong>posições</strong>");
	}
}

