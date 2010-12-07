# coding: utf-8
#!/usr/bin/env python

import logging
from supercraques.core import meta
from supercraques.core import SuperCraquesError, SaldoInsuficienteError, CardJaCompradoError, AtletaNotFoundError
from supercraques.model.usuario import Usuario
from supercraques.model.base import Model, Repository
from sqlalchemy import Column, ForeignKey, Integer, String, DateTime, Float
from sqlalchemy.exceptions import IntegrityError
from sqlalchemy.orm import relation



class CardRepository(Repository):

    @staticmethod
    def ids(usuario_id):
        session = meta.get_session()
        query = " select card_id from card"
        query = query + " where usuario_id=%s" % usuario_id
        result = session.execute(query)
        return [row['card_id'] for row in result.fetchall()]

    @staticmethod
    def get_cards(usuario_id):
        ids = Card().ids(usuario_id)
        return [Card().get(id) for id in ids]


    @staticmethod
    def delete_card(usuario_id, atleta_id):
        session = meta.get_session()
        query = " delete from card"
        query = query + " where usuario_id=%s and atleta_id" % (usuario_id, atleta_id)
        result = session.execute(query)
        return result
        
#    @staticmethod
#    def get_atleta_ids(usuario_id):
#        session = meta.get_session()
#        query = " select atleta_id from card"
#        query = query + " where usuario_id=%s" % usuario_id
#        result = session.execute(query)
#        return [row['atleta_id'] for row in result.fetchall()]

    @staticmethod
    def descartar_card(usuario_id, atleta_id):
        from supercraques.model.desafio import Desafio
        
        try:
            
            session = meta.get_session()
            session.begin()

            # recupera o usuario        
            usuario = Usuario().get(usuario_id)
            
            card_delete = None
            cards = Card().get_cards(usuario.id)
            for card in cards:
                if atleta_id == card.atleta_id:
                    card_delete = card
                    break
                
            if card_delete:
                if Desafio().existe_desafio(usuario.id, card.id):
                    raise SuperCraquesError("Existe um desafio para esse card")
                else:
                    # deleta o card.
                    session.delete(card)
            else:
                raise SuperCraquesError()

            # atualiza o patrimonio
            usuario.patrimonio = usuario.patrimonio + card.valor
            session.add(usuario)
             
            # faz commit
            session.commit()
    
        except SuperCraquesError, e:
            session.rollback()
            raise e
        
        except Exception, e:
            session.rollback()
            logging.error("Erro ao descartar card! %s " % e)
            raise SuperCraquesError()

    
    @staticmethod
    def comprar_card(usuario_id, atleta_json):
        
        try:
            
            if not atleta_json:
                raise AtletaNotFoundError()
            
            session = meta.get_session()
            session.begin()
        
            usuario = Usuario().get(usuario_id)
            
            # valida o patrimonio
            valor = float(atleta_json["valor"])
            if usuario.patrimonio < valor or usuario.patrimonio - valor < 0:
                logging.debug("usuario.patrimonio < float(valor): %s < %s" % (usuario.patrimonio, valor))
                raise SaldoInsuficienteError()
            
            # seta as informacoes
            card = Card()
            card.usuario_id = usuario.id
            card.atleta_id = atleta_json["atleta_id"]
            card.valor = valor
            
            # cria o card. 
            session.add(card)
            
            # atualiza o patrimonio
            usuario.patrimonio = usuario.patrimonio - card.valor
            session.add(usuario)
             
            # faz commit
            session.commit()
    
            return card
        
        except IntegrityError, e:
            session.rollback()
            logging.error("card já comprado %s " % e)
            raise CardJaCompradoError()
        
        except SaldoInsuficienteError, e:
            session.rollback()
            raise e
        
        except Exception, e:
            session.rollback()
            logging.error("Erro ao comprar card! %s " % e)
            raise SuperCraquesError()



    def as_dict(self):
        dictionary =  {"id": self.id,
                       "usuario_id": self.usuario_id,
                       "atleta_id": self.atleta_id,
                       "valor": self.valor}
        
        return dictionary



class Card(Model, CardRepository):
    __tablename__ = 'card'
    
    id = Column('card_id', String, primary_key=True)
    usuario_id = Column('usuario_id', String)
    atleta_id = Column('atleta_id', String)
    valor = Column('valor', Float)
    
#    usuario = relation(Usuario)
