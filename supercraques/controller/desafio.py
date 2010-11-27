# coding: utf-8
#!/usr/bin/env python

from torneira.controller import render_to_extension
from supercraques.controller import BaseController, logged, authenticated
from supercraques.core import SuperCraquesError, DesafioJaExisteError
from supercraques.core import meta
from supercraques.model.desafio import Desafio
from supercraques.model.card import Card
from supercraques.core.facebook import GraphAPI

class DesafioController (BaseController):
    
    @logged
    @render_to_extension
    def busca_desafios_recebidos(self, usuario, *args, **kargs):
        result = {"data":[]}
        desafios_recebidos = Desafio().get_desafios_recebidos(usuario.id)
        for desafio in desafios_recebidos:
            result["data"].append(desafio.as_dict())
        
        return result


    @logged
    @render_to_extension
    def busca_desafios_enviados(self, usuario, *args, **kargs):
        result = {"data":[]}
        desafios_enviados = Desafio().get_desafios_enviados(usuario.id)
        for desafio in desafios_enviados:
            result["data"].append(desafio.as_dict())
        
        return result

    
    @logged
    def enviar_desafio(self, usuario, card_id, usuario_desafiado_id, *args, **kw):
        handler = kw.get('request_handler')
        try:
            
            # Criar o desafio
            Desafio().criar_desafio(card_id, usuario_desafiado_id)
            
            # enviar notificacao para o mural
            attachment = {"link":"http://www.supercraques.com.br", 
                          "caption":"Desafio Super Craques!", 
                          "description": "Você foi desafiado por %s para jogar no Super Craques!! Vai jogar ou vair correr?!" % usuario.primeiro_nome, 
                          "picture": "http://sabadao-santamonica.zip.net/images/craque.jpg"}
            graphAPI = GraphAPI(access_token=usuario.access_token)
            graphAPI.put_wall_post(message="", attachment=attachment, profile_id=usuario_desafiado_id)
            
            # mensagem de sucesso
            return self.render_success(message="Desafio enviado com sucesso", request_handler=handler)
             
        except DesafioJaExisteError, e:
            return self.render_error(message=e.message, request_handler=handler)
        
        except SuperCraquesError, e:
            return self.render_error(message=e.message, request_handler=handler)


    @logged
    def aceitar_desafio(self, usuario, *args, **kw):
        desafio_id = kw.get("desafio_id")
        card_desafiado_id = kw.get("card_id_selecionado")
        radio = kw.get("radio")
        Desafio().aceitar_desafio(desafio_id, usuario.id, card_desafiado_id)
        kw.get('request_handler').redirect("/home")
        
        
