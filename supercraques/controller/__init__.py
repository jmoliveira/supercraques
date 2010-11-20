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
    
#    def get_user(self, request):
#        request_handler = kargs.get('request_handler')
#        resul = get_user_from_cookie(request_handler.cookies, FACEBOOK_APP_ID, FACEBOOK_APP_SECRET)
#        pass
#        
    
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
            usuario = Usuario().get(user_cookie["uid"])
            if not usuario:
                kw.get('request_handler').redirect("/login")
                return
        else:
            kw.get('request_handler').redirect("/login")
            return
        
        return fn(self, usuario=usuario, *args, **kw)
    
    return logged_fn




#{'uid': '100001830967449', 'access_token': '166942923329088|91973d991dfad32ea0110f4b-100001830967449|zORtlkhMPbjkQlk7qGw-XFfLf7k', 
#'expires': '0', 'base_domain': 'supercraques.com.br', 'secret': '6315afbaf58f5a49ad87686351c79a06', 'sig': '555880acdf0ef6d9274fdc4a892a370e',
# 'session_key': '91973d991dfad32ea0110f4b-100001830967449'}

#"id" : 100001830967449,
#   "name" : "SuperCraques Cards",
#   "first_name" : "SuperCraques",
#   "last_name" : "Cards",
#   "link" : http://www.facebook.com/profile.php?id=100001830967449,
#   "birthday" : "11/05/1977",
#   "location": {
#    "id" : 110346955653479,
#    "name" : "Rio de Janeiro, Rio de Janeiro"
#    },
#   "gender" : "male",
#   "relationship_status" : "Single",
#   "email" : "cururuzteitei@gmail.com",
#   "timezone" : -2,
#   "locale" : "en_US",
#   "updated_time" : "2010-11-15T21:47:03+0000"




#    @property
#    def current_user(self):
#        """Returns the logged in Facebook user, or None if unconnected."""
#        if not hasattr(self, "_current_user"):
#            self._current_user = None
#            user_id = parse_cookie(self.request.cookies.get("fb_user"))
#            if user_id:
##                self._current_user = User.get_by_key_name(user_id)
#                self._current_user = None
#        return self._current_user
#    


#def parse_cookie(value):
#    """Parses and verifies a cookie value from set_cookie"""
#    if not value: return None
#    parts = value.split("|")
#    if len(parts) != 3: return None
#    if cookie_signature(parts[0], parts[1]) != parts[2]:
#        logging.warning("Invalid cookie signature %r", value)
#        return None
#    timestamp = int(parts[1])
#    if timestamp < time.time() - 30 * 86400:
#        logging.warning("Expired cookie %r", value)
#        return None
#    try:
#        return base64.b64decode(parts[0]).strip()
#    except:
#        return None
#    
#
#def cookie_signature(*parts):
#    """Generates a cookie signature.
#
#    We use the Facebook app secret since it is different for every app (so
#    people using this example don't accidentally all use the same secret).
#    """
#    hash = hmac.new(FACEBOOK_APP_SECRET, digestmod=hashlib.sha1)
#    for part in parts: hash.update(part)
#    return hash.hexdigest()