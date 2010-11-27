# coding: utf-8
#!/usr/bin/env python

import settings
from torneira.controller import render_to_extension
from supercraques.controller import BaseController, logged, authenticated
from supercraques.core import SuperCraquesError, SaldoInsuficienteError, CardJaCompradoError, AtletaNotFoundError
from supercraques.core import meta
from supercraques.model.card import Card
from supercraques.util.helper import PontuacaoHelper

class BancaController (BaseController):
    
    @logged
    def banca(self, usuario, *args, **kargs):
        return self.render_to_template("/banca.html",  usuario=usuario, equipes=self.get_equipes())

    @logged
    def comprar_card(self, usuario, atleta_id, *args, **kw):
        handler = kw.get('request_handler')
        try:
            
            # recura o atleta
            atleta_json = self.get_atleta(atleta_id)
            
            # comprar o card
            Card().comprar_card(usuario.id, atleta_json)
            
            return self.render_success(message="Card comprado com sucesso", request_handler=handler)
            
            
        except AtletaNotFoundError, e:
            return self.render_error(message=e.message, request_handler=handler)

        except SaldoInsuficienteError, e:
            return self.render_error(message=e.message, request_handler=handler)
        
        except CardJaCompradoError, e:
            return self.render_error(message=e.message, request_handler=handler)

        except SuperCraquesError, e:
            return self.render_error(message=e.message, request_handler=handler)
            

    @authenticated
    @render_to_extension
    def busca_atletas_por_equipe(self, user_cookie, equipe_id, *args, **kargs):
        usuario_id = user_cookie["uid"]
        atletas = self.get_atletas_estatisticas(equipe_id=equipe_id) 
        return self.adicionar_status_compra(atletas, usuario_id)

    @authenticated
    @render_to_extension
    def busca_atletas_por_posicao(self, user_cookie, posicao, *args, **kargs):
        usuario_id = user_cookie["uid"]
        atletas = self.get_atletas_estatisticas(posicao=posicao) 
        return self.adicionar_status_compra(atletas, usuario_id)


    @authenticated
    @render_to_extension
    def busca_atletas_por_equipe_e_posicao(self, user_cookie, equipe_id, posicao, *args, **kargs):
        usuario_id = user_cookie["uid"]
        atletas = self.get_atletas_estatisticas(equipe_id, posicao) 
        return self.adicionar_status_compra(atletas, usuario_id)

   
    @authenticated
    @render_to_extension
    def atletas_card(self, user_cookie, *args, **kargs):
        usuario_id = user_cookie["uid"]
        return self.get_atletas_card(usuario_id)

    @logged
    def cards_box(self, usuario, *args, **kargs):
        cards = self.get_atletas_card(usuario.id)
        return self.render_to_template("/cards.html",  usuario=usuario, cards=cards)

    @logged
    @render_to_extension
    def get_supercraque(self, usuario, *args, **kargs):
        result = usuario.as_dict()
        result.update({"qtdCards": len(Card().ids(usuario.id))}) 
        return result
    
    @authenticated
    @render_to_extension
    def busca_equipes(self, user_cookie, *args, **kw):
        return {"nacional": self.get_equipes()}
    
    #############################################
    def adicionar_status_compra(self, atletas, usuario_id):
        cards = Card().get_cards(usuario_id)
        atleta_ids = [c.atleta_id for c in cards]
        for atleta in atletas:
            atleta.update({"possui": str(atleta["atleta_id"]) in atleta_ids})
        
        return atletas

    def get_atletas_card(self, usuario_id):
        atletas = []
        cards = Card().get_cards(usuario_id)
        for card in cards:
            atleta = self.get_atleta(card.atleta_id)
            if atleta:
                atleta.update({"card_id": card.id})
                atletas.append(atleta)
                
        return atletas
        
    def get_equipes(self):
        return self.get_content_service(settings.SEDE['servicos']['equipes_na_edicao'])

    def get_elenco(self, equipe_id):
        return self.get_content_service(settings.SEDE['servicos']['elenco_atual_da_equipe'] % equipe_id)
    
    def get_scout_pessoafuncao(self, pessoafuncao_id):
        return self.get_content_service(settings.SEDE['servicos']['scout_do_atleta_na_edicao'] % pessoafuncao_id)
    
    def get_equipe_map(self, equipe_id=None):
        if not meta.EQUIPE_MAP or (equipe_id and not meta.EQUIPE_MAP.has_key(int(equipe_id))):
            self.__load__(equipe_id)
        return meta.EQUIPE_MAP

    def get_atleta_map(self):
        if not meta.ATLETAS_MAP: self.__load__()
        return meta.ATLETAS_MAP
    
    def get_atleta(self, atleta_id):
        return self.get_atleta_map().get(atleta_id)
    
    def filtrar_atletas(self, atletas, posicao):
        result = []
        for atleta in atletas:
            if atleta["posicao"].upper() == posicao.upper():
                result.append(atleta)
        return result
    
    def get_atletas_estatisticas(self, equipe_id=None, posicao=None):
        if equipe_id and posicao:
            equipe_map = self.get_equipe_map(equipe_id)
            return self.filtrar_atletas(equipe_map.get(int(equipe_id))["atletas"], posicao)
        elif equipe_id:
            equipe_map = self.get_equipe_map(equipe_id)
            return equipe_map.get(int(equipe_id))["atletas"]
        else:
            return self.filtrar_atletas(self.get_atleta_map().values(), posicao)

    def __load__(self, equipe_id=None):
        for equipe in self.get_equipes()[0:5]:
            if equipe_id and int(equipe["equipe_id"]) != int(equipe_id): continue
            elenco = self.get_elenco(equipe["equipe_id"])
            atletas = []
            for atleta in elenco["elenco"]:
                if atleta["funcao_id"] == "A":
                    scout = self.get_scout_pessoafuncao(atleta["pessoafuncao_id"])
                    if scout:
                        qualidade = PontuacaoHelper(scout["funcao"].get("faixa_campo")).calcular_qualidade(scout["eventos"])
                        assiduidade = PontuacaoHelper(scout["funcao"].get("faixa_campo")).calcular_assiduidade(scout.get("estatisticas"))
                        disciplina = PontuacaoHelper(scout["funcao"].get("faixa_campo")).calcular_disciplina(scout["eventos"])
                        atletas.append({ "atleta_id": scout["pessoafuncao_id"],
                                         "img": atleta.get("foto_fpath") if atleta.get("foto_fpath") else "/media/img/foto_padrao.gif",
                                         "posicao": scout["funcao"].get("faixa_campo") if scout["funcao"].get("faixa_campo") else "-",
                                         "nome": scout["nome_popular_atleta"],
                                         "equipe": equipe,
                                         "qualidade": qualidade,
                                         "assiduidade": assiduidade,
                                         "disciplina": disciplina,
                                         "valor":  int(qualidade + assiduidade + assiduidade / 3)})
            
            meta.EQUIPE_MAP[int(equipe["equipe_id"])] = {"equipe": equipe, "atletas":atletas}

 
        for key in meta.EQUIPE_MAP.keys(): 
            for atleta in meta.EQUIPE_MAP[key]["atletas"]:
                meta.ATLETAS_MAP[str(atleta["atleta_id"])] = atleta

    
    
    
        
     
 
#    def invite_friends(self. request):
#        #HTML escape function for invitation content.
#        from cgi import escape
#    
#        facebook_uid = request.facebook.uid
#        # Convert the array of friends into a comma-delimeted string.  
#        exclude_ids = ",".join([str(a) for a in request.facebook.friends.getAppUsers()])
#    
#        # Prepare the invitation text that all invited users will receive.  
#        content = """<fb:name uid="%s" firstnameonly="true" shownetwork="false"/>
#            wants to invite you to play Online board games,
#                 <fb:req-choice url="%s"
#         label="Put Online Gaming and Video Chat on your profile!"/>
#         """ % (facebook_uid, request.facebook.get_add_url())
#    
#        invitation_content = escape(content, True)
#    
#        return render_to_response('facebook/invite_friends.fbml',
#                                   {'content': invitation_content, 'exclude_ids': exclude_ids })
    
#        # ordena os itens de acordo com o criterio escolhido
#        if orderby == 'pontos':
#            atletas.sort(key=lambda x:x['pontuacao'], reverse=True)
#        else:    
#            c = Collator("%s/allkeys.txt" % utils.__path__[0])
#            atletas.sort(key=lambda x:c.sort_key(x['apelido'].lower()))
