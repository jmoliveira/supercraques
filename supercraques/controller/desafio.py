# coding: utf-8
#!/usr/bin/env python

from torneira.controller import render_to_extension
from supercraques.controller import BaseController, logged, authenticated
from supercraques.core import SuperCraquesError, DesafioJaExisteError
from supercraques.core import meta
from supercraques.model.desafio import Desafio
from supercraques.model.card import Card
from supercraques.core.facebook import GraphAPI
from supercraques.util.helper import PontuacaoHelper, SDEHelper

class DesafioController (BaseController):
    
    @render_to_extension
    def load_atletas(self, *args, **kargs):
        helper = SDEHelper()
        helper.__load__()
        
        return {"msg": "Sucesso"}
        
    
    @logged
    @render_to_extension
    def busca_desafios_todos(self, usuario, *args, **kw):
        result = {"data":[]}
        desafios_recebidos = Desafio().get_desafios_todos(usuario.id)
        for desafio in desafios_recebidos:
            desafio_json = desafio.as_desafio_dict(usuario.id)
            desafio_json["card_desafiou"]["atleta"] =  SDEHelper().get_atleta(desafio_json["card_desafiou"]["atleta_id"])
            if desafio_json.get("card_desafiado_id"):
                desafio_json["card_desafiado"]["atleta"] =  SDEHelper().get_atleta(desafio_json["card_desafiado"]["atleta_id"])
                
            result["data"].append(desafio_json)
        
        return result

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
    @render_to_extension
    def desafios_resultado(self, usuario, *args, **kw):
        handler = kw.get('request_handler')
        
        try:
            
            Desafio().abrir_cards(usuario.id)
        
            # mensagem de sucesso
            return self.render_success(message="Desafios aberto com sucesso", request_handler=handler)
             
        except SuperCraquesError, e:
            return self.render_error(message=e.message, request_handler=handler)

    
    
    
    @logged
    def enviar_desafio(self, usuario, card_id, usuario_desafiado_id, *args, **kw):
        handler = kw.get('request_handler')
        try:
            
            # Criar o desafio
            Desafio().criar_desafio(card_id, usuario_desafiado_id)
            
            # enviar notificacao para o mural
            attachment = {"link":"http://supercraques.com.br:8082/home", 
                          "caption":"Desafio Super Craques!", 
                          "description": "Você foi desafiado por %s para jogar no Super Craques!! Vai jogar ou vair correr?!" % usuario.primeiro_nome, 
                          "picture": "http://lh3.ggpht.com/_OeF_LRL1JqU/TP-tIlvBKVI/AAAAAAAACAU/rDBDXEBCXt8/img_fcbk_post.png"}
            graphAPI = GraphAPI(access_token=usuario.access_token)
            graphAPI.put_wall_post(message="", attachment=attachment, profile_id=usuario_desafiado_id)
            
            # mensagem de sucesso
            return self.render_success(message="Desafio enviado com sucesso", request_handler=handler)
             
        except DesafioJaExisteError, e:
            return self.render_error(message=e.message, request_handler=handler)
        
        except SuperCraquesError, e:
            return self.render_error(message=e.message, request_handler=handler)


    @logged
    def aceitar_desafio(self, usuario, desafio_id, card_id, *args, **kw):
        handler = kw.get('request_handler')
        try:
            
            Desafio().aceitar_desafio(desafio_id, usuario.id, card_id)
        
        except SuperCraquesError, e:
            return self.render_error(message=e.message, request_handler=handler)

        # mensagem de sucesso
        return self.render_success(message="Desafio aceito com sucesso", request_handler=handler)
        
        
