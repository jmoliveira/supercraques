# coding: utf-8
#!/usr/bin/env python

from torneira.controller import BaseController as TorneiraBaseController 
import logging, pycurl, StringIO, simplejson


class BaseController (TorneiraBaseController):
    
    def get_content_service(self, url_service):
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
            
            # recupera o response como string
            data = content_io.getvalue()
                       
            logging.debug("conectado no servico %s com sucesso" % url_service)

            return simplejson.loads(data)
            
        except Exception, e:
            logging.error(e)
        finally:
            # fecha a conexao
            curl.close()
