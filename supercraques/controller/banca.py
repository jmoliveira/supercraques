# coding: utf-8
#!/usr/bin/env python

import settings
from torneira.controller import render_to_extension
from supercraques.controller import BaseController, logged, authenticated
from supercraques.core import SaldoInsuficienteError, CardJaCompradoError
from supercraques.core import meta
from supercraques.model.card import Card

class BancaController (BaseController):
    
    @logged
    def banca(self, usuario, *args, **kargs):
        return self.render_to_template("/banca.html",  usuario=usuario, equipes=self.get_equipes())

    @logged
    def comprar_card(self, usuario, atleta_id, *args, **kargs):
        sucesso = False
        message = ""
        
        try:
            
            Card().comprar_card(usuario.id, atleta_id, 10.0)
            sucesso = True
            message = "Card comprado com sucesso."
             
        except SaldoInsuficienteError, e:
            message = e.message
        except CardJaCompradoError, e:
            message = e.message
            
        return self.render_to_json({"sucesso":sucesso, "message":message}, kargs.get('request_handler'))

    @logged
    @render_to_extension
    def busca_atletas_por_equipe(self, usuario, equipe_id, *args, **kargs):
        print "Usuario ID:", usuario.id
        atletas = self.get_atletas_estatisticas_por_equipe(equipe_id) 
        return self.adicionar_status_compra(atletas, usuario.id)
   

    #############################################
    def adicionar_status_compra(self, atletas, usuario_id):
        cards_comprado = Card().get_cards(usuario_id)
        atleta_ids = [card.atleta_id for card in cards_comprado]
        for atleta in atletas:
            atleta.update({"possui": str(atleta["atleta_id"]) in atleta_ids})
        
        return atletas
        
    def get_equipes(self):
        return self.get_content_service(settings.SEDE['servicos']['equipes_na_edicao'])

    def get_elenco(self, equipe_id):
        return self.get_content_service(settings.SEDE['servicos']['elenco_atual_da_equipe'] % equipe_id)
    
    def get_scout_pessoafuncao(self, pessoafuncao_id):
        return self.get_content_service(settings.SEDE['servicos']['scout_do_atleta_na_edicao'] % pessoafuncao_id)
    
    def get_equipe_map(self, equipe_id=None):
        if not meta.EQUIPE_MAP or (equipe_id and not meta.EQUIPE_MAP.has_key(int(equipe_id))) : self.__load__(equipe_id)
        return meta.EQUIPE_MAP

    def get_atletas_estatisticas_por_equipe(self, equipe_id):
        equipe_map = self.get_equipe_map(equipe_id)
        return equipe_map.get(int(equipe_id))["atletas"] 

    def __load__(self, equipe_id=None):
        for equipe in self.get_equipes():
            if equipe_id and int(equipe["equipe_id"]) != int(equipe_id): continue
            elenco = self.get_elenco(equipe["equipe_id"])
            atletas = []
            for atleta in elenco["elenco"]:
                if atleta["funcao_id"] == "A":
                    scout = self.get_scout_pessoafuncao(atleta["pessoafuncao_id"])
                    if scout:
                        atletas.append({ "atleta_id": scout["pessoafuncao_id"],
                                         "img": atleta.get("foto_fpath") if atleta.get("foto_fpath") else "/media/img/foto_padrao.gif",
                                         "posicao": scout["funcao"].get("faixa_campo") if scout["funcao"].get("faixa_campo") else "-",
                                         "nome": scout["nome_popular_atleta"],
                                         "qualidade": scout["estatisticas"]["vitorias"] if scout["estatisticas"].get("vitorias") else "-",
                                         "assiduidade": scout["estatisticas"]["empates"] if scout["estatisticas"].get("empates") else "-",
                                         "disciplina": scout["estatisticas"]["derrotas"] if scout["estatisticas"].get("derrotas") else "-"});
            
            meta.EQUIPE_MAP[int(equipe["equipe_id"])] = {"equipe": equipe, "atletas":atletas}
 


     
     
#        # ordena os itens de acordo com o criterio escolhido
#        if orderby == 'pontos':
#            atletas.sort(key=lambda x:x['pontuacao'], reverse=True)
#        else:    
#            c = Collator("%s/allkeys.txt" % utils.__path__[0])
#            atletas.sort(key=lambda x:c.sort_key(x['apelido'].lower()))
