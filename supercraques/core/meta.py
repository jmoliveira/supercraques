# coding: utf-8
#!/usr/bin/env python

from sqlalchemy import create_engine
from sqlalchemy.interfaces import ConnectionProxy
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.orm.interfaces import SessionExtension
import settings
import logging
import time

__session__ = None
__engine_readable__ = None
__engine_writable__ = None
_MODELS = {}
EQUIPE_MAP = {}
ATLETAS_MAP = {}
USUARIO_OFFLINE = None
AMIGOS_FACEBOOK = {}

class TimerProxy(ConnectionProxy):
    def cursor_execute(self, execute, cursor, statement, parameters, context, executemany):
        if not settings.DEBUG:
            return execute(cursor, statement, parameters, context)
            
        now = time.time()
        try:
            return execute(cursor, statement, parameters, context)
        finally:
            total = time.time() - now
            logging.debug("Query: %s" % statement)
            logging.debug("Total Time: %f" % total)

class UndefinedModel(Exception):
    pass

class SessionExtension(SessionExtension):
    def before_flush(self, session, flush_context, instances):
        session.bind = get_engine(max_overflow=10)
        
def get_model(name):
    try:
        return _MODELS[name]
    except KeyError:
        raise UndefinedModel, "The model %s does not exist, perharps it hasn't been imported" % name

def get_engine(**kw):
    global __engine_readable__
    if not __engine_readable__:
        __engine_readable__ = create_engine(settings.DATABASE_ENGINE, pool_size=settings.DATABASE_POOL_SIZE, pool_recycle=300, proxy=TimerProxy(), **kw)
    return __engine_readable__
    
def get_session(writable=False):
    global __session__
    if not __session__:
        __session__ = scoped_session(sessionmaker(autocommit=True, autoflush=False, expire_on_commit=False, extension=SessionExtension()))
    engine = get_engine(max_overflow=10)
    __session__.bind = engine
    return __session__()

def expire_session():
    '''
        Método usado apenas para o processo de atualização de rodada.
    '''
    global __session__  
    global __engine_readable__
    
    __engine_readable__ = None
    
    __engine_readable__ = get_engine(max_overflow=10)
    __session__.bind = __engine_readable__
