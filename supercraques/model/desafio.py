# coding: utf-8
#!/usr/bin/env python

import logging
from datetime import datetime
from sqlalchemy import Column, ForeignKey, Integer, String, DateTime, Float
from sqlalchemy.orm import relation
from sqlalchemy.exceptions import IntegrityError
from supercraques.core import SuperCraquesError, DesafioJaExisteError, SuperCraquesNotFoundError
from supercraques.core import meta
from supercraques.model.usuario import Usuario
from supercraques.model.card import Card
from supercraques.model.base import Model, Repository
from supercraques.util import date_to_date_br, datetime_to_format

class DesafioRepository(Repository):
    

    @staticmethod
    def get_desafios_todos(usuario_id):
        session = meta.get_session()
        query = " select desafio_id from desafio"
        query = query + " where usuario_desafiado_id=%s or usuario_desafiou_id=%s order by data_criacao DESC" % (usuario_id, usuario_id)
        result = session.execute(query)
        return [Desafio().get(r[0]) for r in result.fetchall()]

    
    @staticmethod
    def get_desafios_recebidos(usuario_id):
        session = meta.get_session()
        query = " select desafio_id from desafio"
        query = query + " where usuario_desafiado_id=%s and status='%s'" % (usuario_id, Desafio.STATUS_PENDENTE)
        result = session.execute(query)
        return [Desafio().get(r[0]) for r in result.fetchall()]


    @staticmethod
    def get_desafios_enviados(usuario_id):
        session = meta.get_session()
        query = " select desafio_id from desafio"
        query = query + " where usuario_desafiou_id=%s and status='%s'" % (usuario_id, Desafio.STATUS_PENDENTE)
        result = session.execute(query)
        return [Desafio().get(r[0]) for r in result.fetchall()]

    @staticmethod
    def get_desafios_aceitos(usuario_id):
        session = meta.get_session()
        query = " select desafio_id from desafio"
        query = query + "  where usuario_desafiado_id=%s or usuario_desafiou_id=%s and status='%s'" % (usuario_id,usuario_id,  Desafio.STATUS_ACEITE)
        result = session.execute(query)
        return [Desafio().get(r[0]) for r in result.fetchall()]

    
    @staticmethod
    def existe_desafio(usuario_desafiou_id, card_desafiou_id):
        session = meta.get_session()
        
        query = " select desafio_id from desafio"
        query = query + " where usuario_desafiou_id=%s and card_desafiou_id=%s and status in (%s)" % (usuario_desafiou_id, card_desafiou_id, Desafio.IN_STATUS)
        result = session.execute(query)
        if result.fetchone():
            return True
        else:
            return False
        
    @staticmethod
    def criar_desafio(card_id, usuario_desafiado_id):
        
        try:
            
            session = meta.get_session()
            session.begin()
        
            card = Card().get(card_id)
            
            if Desafio.existe_desafio(card.usuario_id, card.id):
                raise DesafioJaExisteError()
            
            
            desafio = Desafio()
            desafio.usuario_desafiou_id = card.usuario_id
            desafio.card_desafiou_id = card.id
            desafio.usuario_desafiado_id = usuario_desafiado_id
            desafio.status = Desafio.STATUS_PENDENTE
            desafio.data_criacao = datetime.now() 
            desafio.data_update = desafio.data_criacao
            
            # cria o desafio 
            session.add(desafio)
            
            # faz commit
            session.commit()
    
            return desafio
        
        except IntegrityError, e:
            session.rollback()
            logging.error("desafio já existe %s " % e)
            raise SuperCraquesError("Ops! Ocorreu um erro na integridade!")
       
        except DesafioJaExisteError, e:
            session.rollback()
            logging.error("desafio já existe %s " % e)
            raise e
        
        except Exception, e:
            session.rollback()
            logging.error("Erro ao tentar criar desafio! %s " % e)
            raise SuperCraquesError("Ops! Ocorreu um erro na transação!")


    @staticmethod
    def abrir_cards(usuario_id):
        
        desafios =  Desafio().get_desafios_aceitos(usuario_id)
        
        try:
            
            session = meta.get_session()
            session.begin()

            for desafio in desafios:
                if desafio.card_desafiou.valor >= desafio.card_desafiado.valor:
                    desafio.usuario_vencedor_id = desafio.usuario_desafiou_id
                    desafio.valor_ganho = desafio.card_desafiado.valor
                else:
                    desafio.usuario_vencedor_id = desafio.usuario_desafiado_id
                    desafio.valor_ganho = desafio.card_desafiou.valor
    
                #atualiza o status e data de update
                desafio.status = Desafio.STATUS_FINALIZADO
                desafio.data_update = datetime.now()
                
                #atualiza o patrimonio
                if desafio.usuario_vencedor_id == desafio.usuario_desafiou.id:
                    desafio.usuario_desafiou.patrimonio = desafio.usuario_desafiou.patrimonio + desafio.valor_ganho
                    desafio.usuario_desafiado.patrimonio = desafio.usuario_desafiado.patrimonio - desafio.valor_ganho
                else:
                    desafio.usuario_desafiado.patrimonio = desafio.usuario_desafiado.patrimonio + desafio.valor_ganho
                    desafio.usuario_desafiou.patrimonio = desafio.usuario_desafiou.patrimonio - desafio.valor_ganho
                    
#                #perde/ganha o card
#                if desafio.usuario_vencedor_id == desafio.usuario_desafiou.id:
#                    desafio.card_desafiou.
#                else:
#                    pass
#                session.add(desafio.usuario_desafiou)
#                session.add(desafio.usuario_desafiado)

                
                
                # atualiza o desafio 
                session.add(desafio)
                
            
            # faz commit
            session.commit()
   
                
        except Exception, e:
            session.rollback()
            logging.error("Erro ao tentar criar desafio! %s " % e)
            raise SuperCraquesError("Ops! Ocorreu um erro na transação!")
                

    @staticmethod
    def aceitar_desafio(desafio_id, usuario_desafiado_id, card_desafiado_id):
        
        try:
            
            session = meta.get_session()
            session.begin()
        
            desafio = Desafio().get_by_id(desafio_id)
            
            if desafio.usuario_desafiado_id != usuario_desafiado_id:
                raise SuperCraquesError("usuario que aceitou é diferente do que esta no desafio")
            
            if desafio.status != Desafio.STATUS_PENDENTE:
                raise SuperCraquesError("Desafio já aceito!")
            
            desafio.card_desafiado_id = card_desafiado_id
            desafio.status = Desafio.STATUS_ACEITE
            desafio.data_update = datetime.now()
            
            # atualiza o desafio 
            session.add(desafio)
            
            # faz commit
            session.commit()
    
            logging.error("Desafio aceito!")
            
            return desafio
        
        except IntegrityError, e:
            session.rollback()
            logging.error("desafio já existe %s " % e)
            raise SuperCraquesError("Ops! Ocorreu um erro na integridade!")
       
        except SuperCraquesNotFoundError, e:
            session.rollback()
            logging.error("desafio não existe %s " % e)
            raise e

        except SuperCraquesError, e:
            session.rollback()
            raise e
        
        except Exception, e:
            session.rollback()
            logging.error("Erro ao aceitar desafio! %s " % e)
            raise SuperCraquesError("Ops! Ocorreu um erro na transação!")


    def get_by_id(self, desafio_id):
        desafio = Desafio().get(desafio_id)
        if desafio:
            return desafio
        
        raise SuperCraquesNotFoundError("Desafio não existe")
        

    def as_dict(self):
        dictionary =  {"id": self.id,
                       "usuario_desafiou_id": self.usuario_desafiou_id,
                       "usuario_desafiou": self.usuario_desafiou.as_dict(),
                       "card_desafiou_id": self.card_desafiou_id,
                       "usuario_desafiado_id": self.usuario_desafiado_id,
                       "usuario_desafiado": self.usuario_desafiado.as_dict() if self.usuario_desafiado_id else None,
                       "card_desafiado_id": self.card_desafiado_id,
                       "usuario_vencedor_id":self.usuario_vencedor_id,
                       "status": self.status,
                       "valor_ganho": self.valor_ganho,
                       "descricao": self.descricao,
                       "data_criacao": date_to_date_br(self.data_criacao),
                       "data_update": date_to_date_br(self.data_update)}
        
        return dictionary


    def as_desafio_dict(self, usuario_id):
        dictionary =  {"id": self.id,
                       "desafio_enviado": True if usuario_id == self.usuario_desafiou_id else False,
                       "usuario_desafiou_id": self.usuario_desafiou_id,
                       "usuario_desafiou": self.usuario_desafiou.as_dict(), 
                       "card_desafiou_id": self.card_desafiou_id,
                       "card_desafiou": self.card_desafiou.as_dict(),
                       "usuario_desafiado_id": self.usuario_desafiado_id,
                       "usuario_desafiado": self.usuario_desafiado.as_dict() if self.usuario_desafiado else None,
                       "card_desafiado_id": self.card_desafiado_id,
                       "card_desafiado": self.card_desafiado.as_dict() if self.card_desafiado_id else None,
                       "usuario_vencedor_id": self.usuario_vencedor_id,
                       "is_finalizado": True if self.status == self.STATUS_FINALIZADO else False, 
                       "ganhou": True if self.usuario_vencedor_id == usuario_id else False,
                       "status": self.status,
                       "valor_ganho": self.valor_ganho,
                       "descricao": self.descricao,
                       "data_criacao": datetime_to_format(self.data_criacao),
                       "data_update": datetime_to_format(self.data_update)}
        
        return dictionary



class Desafio(Model, DesafioRepository):
    __tablename__ = 'desafio'
    
    STATUS_PENDENTE = "P"
    STATUS_ACEITE = "A"
    STATUS_FINALIZADO = "F"
#    STATUS_VISUALIZADO = "V"
#    STATUS_ESCONDIDO = "E"
    IN_STATUS = "'%s','%s'" % (STATUS_PENDENTE, STATUS_ACEITE)
    
    id = Column('desafio_id', Integer, primary_key=True)
    usuario_desafiou_id = Column('usuario_desafiou_id', String, ForeignKey("usuario.usuario_id"))
    card_desafiou_id = Column('card_desafiou_id', String, ForeignKey("card.card_id"))
    usuario_desafiado_id = Column('usuario_desafiado_id', String, ForeignKey("usuario.usuario_id"))
    card_desafiado_id = Column('card_desafiado_id', String, ForeignKey("card.card_id"))
    usuario_vencedor_id = Column('usuario_vencedor_id', String, ForeignKey("usuario.usuario_id"))
    status = Column('status', String)
    valor_ganho = Column('valor_ganho', Float)
    descricao = Column('descricao', String)
    data_criacao = Column('data_criacao', DateTime)
    data_update = Column('data_update', DateTime)


    usuario_desafiou = relation(Usuario, primaryjoin=usuario_desafiou_id==Usuario.id)
    card_desafiou = relation(Card, primaryjoin=card_desafiou_id==Card.id)
    usuario_desafiado = relation(Usuario, primaryjoin=usuario_desafiado_id==Usuario.id)
    card_desafiado = relation(Card, primaryjoin=card_desafiado_id==Card.id)
    
    
    
    
    