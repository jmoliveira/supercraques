# coding: utf-8
#!/usr/bin/env python


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
        sum = 0
        for evento in eventos:
            sigla = evento["sigla"]
            if sigla in self.scouts_disciplina:
                sum += self.VALORES_SCOUTS[sigla] * evento["total"]
                  
        return int(sum)
