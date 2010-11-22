# coding: utf-8
#!/usr/bin/env python


class SuperCraquesError(Exception):
    def __init__(self, message):
        Exception.__init__(self, message)


class SaldoInsuficienteError(Exception):
    def __init__(self, message="Usuário não tem dinheiro suficiente para comprar o card!"):
        Exception.__init__(self, message)


class CardJaCompradoError(Exception):
    def __init__(self, message="Card já comprado!"):
        Exception.__init__(self, message)

class DesafioJaExisteError(Exception):
    def __init__(self, message="Desafio já existe!"):
        Exception.__init__(self, message)
