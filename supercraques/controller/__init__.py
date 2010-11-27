# coding: utf-8
#!/usr/bin/env python

from torneira.controller import BaseController as TorneiraBaseController 
import logging, pycurl, StringIO, simplejson
from sqlalchemy.exceptions import IntegrityError

from supercraques.core.facebook import GraphAPI, get_user_from_cookie
from supercraques.model.usuario import Usuario

FACEBOOK_APP_ID = "166942923329088"
FACEBOOK_APP_SECRET = "80342273fa7b84e12c095765fe0e095f"


class BaseController (TorneiraBaseController):
    SERVICE_CACHE = {}
    
    def get_content_service(self, url_service):
        
        cache = self.SERVICE_CACHE.get(url_service)
        if cache:
            return cache
        else:
            try:
                # prepara para receber o content
                content_io = StringIO.StringIO()
                        
                # inicia o curl
                curl = pycurl.Curl()
                curl.setopt(pycurl.URL, url_service)
                curl.setopt(pycurl.HTTPHEADER, ["Accept:text/xml","Content-type:text/xml"])
                curl.setopt(pycurl.PUT, 1)
                curl.setopt(pycurl.WRITEFUNCTION, content_io.write)
                curl.setopt(pycurl.INFILESIZE, 0)
                curl.setopt(pycurl.FOLLOWLOCATION, 1)
                curl.setopt(pycurl.MAXREDIRS, 5)
                
                # abre a conexao
                curl.perform()
                
                code = curl.getinfo(pycurl.HTTP_CODE)
                
                if code == 200:
                    # recupera o response como string
                    data = content_io.getvalue()
                    logging.debug("conectado no servico %s com sucesso" % url_service)
                    json = simplejson.loads(data)
                    #cache
                    self.SERVICE_CACHE[url_service] = json
                    return json
                    
                else:
                    logging.debug("Code Erro: %s" % code)
                    return None
                
            except Exception, e:
                logging.error(e)
            finally:
                # fecha a conexao
                curl.close()

    def render_success(self, message="Operação realizada com sucesso!", **kw):
        return self.render_to_json({"tipoAviso": "sucesso", "message": message}, **kw)

    def render_error(self, message="Ops! Ocorreu um erro!", **kw):
        return self.render_to_json({"tipoAviso": "erro", "errors":{"error":{"message": message}}}, **kw)


def authenticated(fn):
    def authenticated_fn(self, *args, **kw):
        request_handler = kw.get('request_handler')
        user_cookie = get_user_from_cookie(request_handler.cookies, FACEBOOK_APP_ID, FACEBOOK_APP_SECRET)
        if not user_cookie:
            request_handler.redirect("/login")
            return
        
        return fn(self, user_cookie=user_cookie, *args, **kw)
    
    return authenticated_fn

def logged(fn):
    def logged_fn(self, *args, **kw):
        usuario = None
        user_cookie = get_user_from_cookie(kw.get('request_handler').cookies, FACEBOOK_APP_ID, FACEBOOK_APP_SECRET)
        if user_cookie:
#            logging.debug("user_cookie: %s" % user_cookie)
            usuario = Usuario().get(user_cookie["uid"])
            logging.debug("usuario: %s" % usuario.as_dict())
            if not usuario:
                return kw.get('request_handler').redirect("/login")
            else:
                usuario.access_token = user_cookie["access_token"]
        else:
            return kw.get('request_handler').redirect("/login")
        
        return fn(self, usuario=usuario, *args, **kw)
    
    return logged_fn
