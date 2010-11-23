# coding: utf-8
#!/usr/bin/env python

import logging
from supercraques.core import meta
from supercraques.core import SuperCraquesError, SaldoInsuficienteError, CardJaCompradoError
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

#    @staticmethod
#    def get_atleta_ids(usuario_id):
#        session = meta.get_session()
#        query = " select atleta_id from card"
#        query = query + " where usuario_id=%s" % usuario_id
#        result = session.execute(query)
#        return [row['atleta_id'] for row in result.fetchall()]

    
    @staticmethod
    def comprar_card(usuario_id, atleta_id, valor):
        
        try:
            
            session = meta.get_session()
            session.begin()
        
            usuario = Usuario().get(usuario_id)
            # valida o patrimonio
            if usuario.patrimonio < float(valor):
                raise SaldoInsuficienteError()
            
            # seta as informacoes
            card = Card()
            card.usuario_id = usuario.id
            card.atleta_id = atleta_id
            card.valor = float(valor)
            
            # cria o card. 
            session.add(card)
            
            # atualiza o patrimonio
            session.execute("update usuario set patrimonio = patrimonio-%f where usuario_id=%s" % (card.valor, usuario.id))
            
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
            raise SuperCraquesError("Ops! Ocorreu um erro na transação!")


class Card(Model, CardRepository):
    __tablename__ = 'card'
    
    id = Column('card_id', String, primary_key=True)
    usuario_id = Column('usuario_id', String)
    atleta_id = Column('atleta_id', String)
    valor = Column('valor', Float)
    
#    usuario = relation(Usuario)
