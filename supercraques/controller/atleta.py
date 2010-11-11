# coding: utf-8
#!/usr/bin/env python

from supercraques.controller import BaseController
import settings

class AtletaController (BaseController):


    def atletas(self, **kw):
#        import pdb;pdb.set_trace()
        equipe = self.get_content_service(settings.SEDE['servicos']['elenco_atual_da_equipe'] % "262")
        
#        atletas = [{"nome":"janilton","idade":33}, {"nome":"command", "idade":47}]
        return self.render_to_template("/atletas.html",  equipe=equipe)