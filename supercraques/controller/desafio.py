# coding: utf-8
#!/usr/bin/env python

import settings
from torneira.controller import render_to_extension
from supercraques.controller import BaseController, logged, authenticated
from supercraques.core import SuperCraquesError, DesafioJaExisteError
from supercraques.core import meta
from supercraques.model.desafio import Desafio

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
