# coding: utf-8
#!/usr/bin/env python

from supercraques.core import meta
from sqlalchemy import MetaData
from sqlalchemy.ext.declarative import DeclarativeMeta, declarative_base

metadata = MetaData()
        
class MetaBaseModel(DeclarativeMeta):
    def __init__(self, classname, bases, dict_):
        meta._MODELS[classname] = self
        return DeclarativeMeta.__init__(self, classname, bases, dict_)

Model = declarative_base(metadata=metadata, metaclass=MetaBaseModel)

class Repository(object):
    
    def as_dict(self):
        items = {}
        for attrname in dir(self):
            if attrname.startswith("_"):
                continue

            attr = getattr(self, attrname)
            if isinstance(attr, (basestring, int, float)):
                items[attrname] = attr
            if hasattr(attr, 'serializable'):
                items[attr.serializable] = apply(attr)

            if isinstance(attr, list):
                items[attrname] = [x.as_dict() for x in attr]

        return items
    
    @classmethod
    def get(cls, id):
        session = meta.get_session()
        return session.query(cls).get(id)

    @classmethod
    def fetch_by(cls, **kw):
        session = meta.get_session()
        return session.query(cls).filter_by(**kw)

    @classmethod
    def all(cls, limit=None):
        session = meta.get_session()
        if limit:
            return session.query(cls).all()[limit[0]:limit[1]]
        return session.query(cls).all()
    
    @classmethod
    def create(cls, **kwargs):
        instance = cls()
        for k,v in kwargs.items():
            setattr(instance, k, v)

        instance.save()
        return instance

    def delete(self):
        session = meta.get_session()
        session.delete(self)
        session.flush()

    def save(self):
        session = meta.get_session()
        if not self.id: 
            session.add(self)
        session.flush()
