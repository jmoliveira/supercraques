# coding: utf-8
#!/usr/bin/env python

from torneira.controller import render_to_extension
from supercraques.controller import BaseController, logged, authenticated
from supercraques.core import SuperCraquesError, DesafioJaExisteError
from supercraques.core import meta
from supercraques.model.desafio import Desafio
from supercraques.model.card import Card

class DesafioController (BaseController):
    
    @logged
    def enviar_desafio(self, usuario, card_id, usuario_desafiado_id, *args, **kargs):
        sucesso = False
        message = ""
        try:
            
            Desafio().criar_desafio(card_id, usuario_desafiado_id)
            sucesso = True
            message = "Card comprado com sucesso."
             
        except DesafioJaExisteError, e:
            message = e.message
        except SuperCraquesError, e:
            message = e.message
                
        return self.render_to_json({"sucesso":sucesso, "message":message}, kargs.get('request_handler'))

#http://supercraques.com.br:8082/home?desafio_id=6&atleta_card_id_selecionado=32&radio=assiduidade

    @logged
    def aceitar_desafio(self, usuario, *args, **kw):
        import pdb;pdb.set_trace()
        desafio_id = kw.get("desafio_id")
        card_desafiado_id = kw.get("card_id_selecionado")
        radio = kw.get("radio")
        Desafio().aceitar_desafio(desafio_id, usuario.id, card_desafiado_id)
