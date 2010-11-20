# coding: utf-8
#!/usr/bin/env python

import settings
from torneira.controller import render_to_extension
from supercraques.controller import BaseController, logged, authenticated
from supercraques.core import meta

class BancaController (BaseController):
    
    @logged
    def banca(self, usuario, *args, **kargs):
        return self.render_to_template("/banca.html",  usuario=usuario, equipes=self.get_equipes())

    @render_to_extension
    def busca_atletas_por_equipe(self, equipe_id, *args, **kargs):
        return self.get_atletas_estatisticas_por_equipe(equipe_id)
   

    #############################################    
    def get_equipes(self):
        return self.get_content_service(settings.SEDE['servicos']['equipes_na_edicao'])

    def get_elenco(self, equipe_id):
        return self.get_content_service(settings.SEDE['servicos']['elenco_atual_da_equipe'] % equipe_id)
    
    def get_scout_pessoafuncao(self, pessoafuncao_id):
        return self.get_content_service(settings.SEDE['servicos']['scout_do_atleta_na_edicao'] % pessoafuncao_id)
    
    def get_equipe_map(self):
        if not meta.EQUIPE_MAP: self.__load__()
        return meta.EQUIPE_MAP

    def get_atletas_estatisticas_por_equipe(self, equipe_id):
        equipe_map = self.get_equipe_map()
        return equipe_map.get(int(equipe_id))["atletas"] 


    def __load__(self):
        for equipe in self.get_equipes():
            elenco = self.get_elenco(equipe["equipe_id"])
            atletas = []
            for atleta in elenco["elenco"]:
                if atleta["funcao_id"] == "A":
                    scout = self.get_scout_pessoafuncao(atleta["pessoafuncao_id"])
                    if scout:
                        foto_fpath = atleta.get("foto_fpath")
                        scout.update({"foto_fpath": foto_fpath if foto_fpath else "/media/img/foto_padrao.gif"})
                        atletas.append(scout)
                    
            meta.EQUIPE_MAP[equipe["equipe_id"]] = {"equipe": equipe, "atletas":atletas}
 
        
        
#    @render_to_extension
#    def atletas_json(self, *args, **kargs):
#        return self.get_equipe_map()


#        # ordena os itens de acordo com o criterio escolhido
#        if orderby == 'pontos':
#            atletas.sort(key=lambda x:x['pontuacao'], reverse=True)
#        else:    
#            c = Collator("%s/allkeys.txt" % utils.__path__[0])
#            atletas.sort(key=lambda x:c.sort_key(x['apelido'].lower()))
