# coding: utf-8
#!/usr/bin/env python


from torneira.controller import render_to_extension
from supercraques.controller import BaseController, logged, authenticated
from supercraques.core import SuperCraquesError, SaldoInsuficienteError, CardJaCompradoError, AtletaNotFoundError
from supercraques.model.card import Card
from supercraques.util.helper import PontuacaoHelper, SDEHelper

class BancaController (BaseController):
    
    @logged
    def banca(self, usuario, *args, **kargs):
        return self.render_to_template("/banca.html",  usuario=usuario, equipes=SDEHelper().get_equipes())

    @logged
    def comprar_card(self, usuario, atleta_id, *args, **kw):
        handler = kw.get('request_handler')
        try:
            
            # recura o atleta
            atleta_json = SDEHelper().get_atleta(atleta_id)
            
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


    @logged
    def descartar_card(self, usuario, atleta_id, *args, **kw):
        handler = kw.get('request_handler')
        try:
            
            # descartar o card
            Card().descartar_card(usuario.id, atleta_id)
            
            return self.render_success(message="Card descartado com sucesso", request_handler=handler)
            
        
        except CardJaCompradoError, e:
            return self.render_error(message=e.message, request_handler=handler)

        except SuperCraquesError, e:
            return self.render_error(message=e.message, request_handler=handler)
            
            

    @authenticated
    @render_to_extension
    def busca_atletas_por_equipe(self, user_cookie, equipe_id, *args, **kargs):
        usuario_id = user_cookie["uid"]
        atletas = SDEHelper().get_atletas_estatisticas(equipe_id=equipe_id) 
        return self.adicionar_status_compra(atletas, usuario_id)

    @authenticated
    @render_to_extension
    def busca_atletas_por_posicao(self, user_cookie, posicao, *args, **kargs):
        usuario_id = user_cookie["uid"]
        atletas = SDEHelper().get_atletas_estatisticas(posicao=posicao) 
        return self.adicionar_status_compra(atletas, usuario_id)


    @authenticated
    @render_to_extension
    def busca_atletas_por_equipe_e_posicao(self, user_cookie, equipe_id, posicao, *args, **kargs):
        usuario_id = user_cookie["uid"]
        atletas = SDEHelper().get_atletas_estatisticas(equipe_id, posicao) 
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
        return {"nacional": SDEHelper().get_equipes()}

    
    def adicionar_status_compra(self, atletas, usuario_id):
        cards = Card().get_cards(usuario_id)
        atleta_ids = [c.atleta_id for c in cards]
        for atleta in atletas:
            atleta.update({"possui": str(atleta["atleta_id"]) in atleta_ids})
        
        return atletas

#    def adicionar_status_compra(self, atletas, usuario_id):
#        cards = Card().get_cards(usuario_id)
#        for atleta in atletas:
#            for card in cards:
##                print str(atleta["atleta_id"]), str(card.atleta_id), str(atleta["atleta_id"]) == str(card.atleta_id)
#                if str(atleta["atleta_id"]) == str(card.atleta_id):
#                    atleta.update({"possui": True, "card_id": card.id})
#                    break
#                else:
#                    atleta.update({"possui": False})
#        
#        return atletas

    def get_atletas_card(self, usuario_id):
        atletas = []
        cards = Card().get_cards(usuario_id)
        for card in cards:
            atleta = SDEHelper().get_atleta(card.atleta_id)
            if atleta:
                atleta.update({"card_id": card.id})
                atletas.append(atleta)
                
        return atletas
