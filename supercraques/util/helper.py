# coding: utf-8
#!/usr/bin/env python

import settings
from supercraques.controller import BaseController
from supercraques.core import meta

class SDEHelper(BaseController):

    def get_atleta(self, atleta_id):
        return self.get_atleta_map().get(atleta_id)
    
    def get_equipe_map(self, equipe_id=None):
        if not meta.EQUIPE_MAP or (equipe_id and not meta.EQUIPE_MAP.has_key(int(equipe_id))):
            self.__load__(equipe_id)
        return meta.EQUIPE_MAP

    def get_atleta_map(self):
        if not meta.ATLETAS_MAP: self.__load__()
        return meta.ATLETAS_MAP
    
    def filtrar_atletas(self, atletas, posicao):
        result = []
        for atleta in atletas:
            if atleta["posicao"].upper() == posicao.upper():
                result.append(atleta)
        return result
    
    def get_atletas_estatisticas(self, equipe_id=None, posicao=None):
        if equipe_id and posicao:
            equipe_map = self.get_equipe_map(equipe_id)
            return self.filtrar_atletas(equipe_map.get(int(equipe_id))["atletas"], posicao)
        elif equipe_id:
            equipe_map = self.get_equipe_map(equipe_id)
            return equipe_map.get(int(equipe_id))["atletas"]
        else:
            return self.filtrar_atletas(self.get_atleta_map().values(), posicao)

    def get_equipes(self):
        return self.get_content_service(settings.SEDE['servicos']['equipes_na_edicao'])

    def get_elenco(self, equipe_id):
        return self.get_content_service(settings.SEDE['servicos']['elenco_atual_da_equipe'] % equipe_id)
    
    def get_scout_pessoafuncao(self, pessoafuncao_id):
        return self.get_content_service(settings.SEDE['servicos']['scout_do_atleta_na_edicao'] % pessoafuncao_id)

    def __load__(self, equipe_id=None):
        for equipe in self.get_equipes():
            if equipe_id and int(equipe["equipe_id"]) != int(equipe_id): continue
            elenco = self.get_elenco(equipe["equipe_id"])
            atletas = []
            for atleta in elenco["elenco"]:
                if atleta["funcao_id"] == "A":
                    scout = self.get_scout_pessoafuncao(atleta["pessoafuncao_id"])
                    if scout:
                        qualidade = PontuacaoHelper(scout["funcao"].get("faixa_campo")).calcular_qualidade(scout["eventos"])
                        qualidade = 100 if qualidade > 100 else qualidade
                        assiduidade = PontuacaoHelper(scout["funcao"].get("faixa_campo")).calcular_assiduidade(scout.get("estatisticas"))
                        assiduidade = 100 if assiduidade > 100 else assiduidade
                        disciplina = PontuacaoHelper(scout["funcao"].get("faixa_campo")).calcular_disciplina(scout["eventos"])
                        disciplina = 100 if disciplina > 100 else disciplina
                        valor = int((qualidade + assiduidade + disciplina) / 3)
                        if valor > 90:
                            valor = valor - 29
                        elif valor > 80:
                            valor = valor - 25
                        elif valor > 70:
                            valor = valor - 20
                        elif valor > 60:
                            valor = valor - 14
                        elif valor > 50:
                            valor = valor - 11
                        elif valor > 40:
                            valor = valor - 9
                        elif valor > 30:
                            valor = valor - 7
                        elif valor > 20:
                            valor = valor - 5
                                
                        if qualidade >0 or assiduidade >0:
                            if scout["pessoafuncao_id"] == 50348:
                                valor = valor + 10
                            
                            atletas.append({ "atleta_id": scout["pessoafuncao_id"],
                                             "img": atleta.get("foto_fpath").replace("_FORMATO","_220x220") if atleta.get("foto_fpath") and settings.EXIBIR_FOTO == True else "/media/img/jogador_default.jpg",
                                             "posicao": scout["funcao"].get("faixa_campo") if scout["funcao"].get("faixa_campo") else "-",
                                             "nome": scout["nome_popular_atleta"],
                                             "equipe": equipe,
                                             "qualidade": qualidade,
                                             "assiduidade": assiduidade,
                                             "disciplina": disciplina,
                                             "valor":  valor})
                
            meta.EQUIPE_MAP[int(equipe["equipe_id"])] = {"equipe": equipe, "atletas":atletas}

 
        for key in meta.EQUIPE_MAP.keys(): 
            for atleta in meta.EQUIPE_MAP[key]["atletas"]:
                meta.ATLETAS_MAP[str(atleta["atleta_id"])] = atleta

    


class PontuacaoHelper():
    
    VALORES_ASSIDUIDADE = {"jogos":1, "vitorias":1, "empates":1, "derrotas":1}
    VALORES_SCOUTS = {"RB":2, "FC":-0.5, "GC":-6, "CA":-2, "CV":-5, "DD":2, "DT":7,  "GS":-2, "FR":0.5, "PE":-0.2, "PD":4, "UP":4, "ZT":3.5, "ZD":1, "ZF":0.7, "ZG":7, "IM":-0.5, "TF":-3.5, "TD":-3.5}
    SCOUTS_QUALIDADE = {"GOL": ["DD", "DT"], "ZAGA": ["RB", "FC"], "LATERAL": ["RB", "FC"], "MEIO-CAMPO": ["PE", "PD", "UP"], "ATAQUE": ["ZG", "ZT", "ZD", "ZF", "FR"]}
    ESTATISTICAS_ASSIDUIDADE = ["jogos"]
    SCOUTS_DISCIPLINA = ["CA", "CV", "FC"]
    
    
    def __init__(self, posicao):
        self.posicao = posicao.upper()
        self.scouts_qualidade = self.SCOUTS_QUALIDADE.get(self.posicao, [])
        self.estatisticas_assiduidade = self.ESTATISTICAS_ASSIDUIDADE
        self.scouts_disciplina = self.SCOUTS_DISCIPLINA
    
        
    def calcular_qualidade(self, eventos):
        sum = 0
        for evento in eventos:
            sigla = evento["sigla"]
            if sigla in self.scouts_qualidade:
                sum += self.VALORES_SCOUTS[sigla] * evento["total"]
                  
        return int(sum)
    
    def calcular_assiduidade(self, estatisticas):
        sum = 0
        if estatisticas:
            for estat in self.estatisticas_assiduidade:
                if not estatisticas.get(estat) is None:
                    sum += estatisticas.get(estat) * self.VALORES_ASSIDUIDADE["jogos"]
        
        return int(sum)

    def calcular_disciplina(self, eventos):
        sum = 90
        for evento in eventos:
            sigla = evento["sigla"]
            if sigla in self.scouts_disciplina:
                sum += self.VALORES_SCOUTS[sigla] * evento["total"]
                  
        return int(sum)
