# coding: utf-8
#!/usr/bin/env python


class SuperCraquesError(Exception):
    def __init__(self, message="Ops! Ocorreu um erro na transação!"):
        Exception.__init__(self, message)

class SaldoInsuficienteError(Exception):
    def __init__(self, message="Voçê não tem dinheiro suficiente para comprar o card!"):
        Exception.__init__(self, message)

class CardJaCompradoError(Exception):
    def __init__(self, message="Card já comprado!"):
        Exception.__init__(self, message)

class DesafioJaExisteError(Exception):
    def __init__(self, message="Desafio já existe!"):
        Exception.__init__(self, message)

class SuperCraquesNotFoundError:
    def __init__(self, message="Objeto inexistente"):
        Exception.__init__(self, message)

class AtletaNotFoundError:
    def __init__(self, message="Atleta não encontrado!"):
        Exception.__init__(self, message)

