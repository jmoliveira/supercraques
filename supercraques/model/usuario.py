# coding: utf-8
#!/usr/bin/env python

import logging
from supercraques.core import meta
from supercraques.core import SuperCraquesError
from supercraques.model.base import Model, Repository
from sqlalchemy import Column, ForeignKey, Integer, String, DateTime, Float
from sqlalchemy.exceptions import IntegrityError
from sqlalchemy.orm import relation



class UsuarioRepository(Repository):
    
    @staticmethod
    def criar_usuario(user_facebook):
        try:
            
            session = meta.get_session()
            session.begin()
        
            #seta as informacoes do usuario do facebook
            usuario = Usuario()
            usuario.id = user_facebook.get("id")
            usuario.nome = user_facebook.get("name")
            usuario.primeiro_nome = user_facebook.get("first_name")
            usuario.ultimo_nome = user_facebook.get("last_name")
            usuario.link = user_facebook.get("link")
            usuario.localizacao = user_facebook.get("location").get("name") if user_facebook.get("location") else None
            usuario.sexo = user_facebook.get("gender")
            usuario.email = user_facebook.get("email")
            usuario.patrimonio = 100
            
            # Cria o usuario. 
            session.add(usuario)
            session.commit()
    
            return usuario
        
        except IntegrityError, e:
            session.rollback()
            logging.error("cadastrando usuario, integrity error %s " % e)
            raise SuperCraquesError("Ops! Já existe um usuario com este id!")
        except Exception, e:
            session.rollback()
            logging.error("Erro ao cadastrar o usuario! %s " % e)
            raise SuperCraquesError("Ops! Ocorreu um erro na transação!")


class Usuario(Model, UsuarioRepository):
    __tablename__ = 'usuario'
    
    id = Column('usuario_id', String, primary_key=True)
    nome = Column('nome', String)
    primeiro_nome = Column('primeiro_nome', String)
    ultimo_nome = Column('primeiro_nome', String)
    link = Column('link', String)
    localizacao = Column('localizacao', String)
    sexo = Column('sexo', String)
    email = Column('email', String)
    patrimonio = Column('patrimonio', Float)
