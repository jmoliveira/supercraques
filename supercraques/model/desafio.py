# coding: utf-8
#!/usr/bin/env python

from supercraques.model.usuario import Usuario
from supercraques.core import meta
from supercraques.model.base import Model, Repository
from sqlalchemy import Column, ForeignKey, Integer, String, DateTime, Float
from sqlalchemy.orm import relation


class DesafioRepository(Repository):
    
    @staticmethod
    def get_desafios_recebidos(usuario_id):
        #, usuario_desafiou_id, usuario_desafiado_id, descricao, data_criacao, data_update, status
        session = meta.get_session()
        query = " select desafio_id from desafio"
        query = query + " where usuario_desafiado_id=%s and status='%s'" % (usuario_id, Desafio.STATUS_PENDENTE)
        result = session.execute(query)
        if result:
            return [Desafio().get(r[0]) for r in result]
        
        return None


    @staticmethod
    def get_desafios_enviados(usuario_id):
        session = meta.get_session()
        query = " select desafio_id from desafio"
        query = query + " where usuario_desafiou_id=%s and status='%s'" % (usuario_id, Desafio.STATUS_PENDENTE)
        result = session.execute(query)
        if result:
            return [Desafio().get(r[0]) for r in result]
        
        return None


class Desafio(Model, DesafioRepository):
    __tablename__ = 'desafio'
    
    STATUS_PENDENTE = "P"
    STATUS_ACEITE = "A"
    STATUS_FINALIZADO = "F"
    STATUS_VISTO = "V"
    STATUS_ESCONDIDO = "E"
    
    id = Column('desafio_id', Integer, primary_key=True)
    usuario_desafiou_id = Column('usuario_desafiou_id', String, ForeignKey("usuario.usuario_id"))
    atleta_desafiou_id = Column('atleta_desafiou_id', String)
    usuario_desafiado_id = Column('usuario_desafiado_id', String, ForeignKey("usuario.usuario_id"))
    atleta_desafiado_id = Column('atleta_desafiado_id', String)
    usuario_vencedor_id = Column('usuario_vencedor_id', String, ForeignKey("usuario.usuario_id"))
    status = Column('status', String)
    valor_ganho = Column('valor_ganho', Float)
    descricao = Column('descricao', String)
    data_criacao = Column('data_criacao', DateTime)
    data_update = Column('data_update', DateTime)

    usuario_desafiou = relation(Usuario, primaryjoin=usuario_desafiou_id==Usuario.id)
    usuario_desafiado = relation(Usuario, primaryjoin=usuario_desafiado_id==Usuario.id)