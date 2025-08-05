from datetime import date
from abc import ABC, abstractmethod


# Classe Historico
class Historico:
    def __init__(self):
        self.transacoes = []

    def adicionar_transacao(self, transacao):
        self.transacoes.append(transacao)

# Cliente
class Cliente:
    def __init__(self, endereco):
        self.endereco = endereco
        self.contas = []

    def adicionar_conta(self, conta):
        self.contas.append(conta)

    def realizar_transacao(self, conta, transacao):
        transacao.registrar(conta)
        conta.historico.adicionar_transacao(transacao)

# Pessoa Física
class PessoaFisica(Cliente):
    def __init__(self, nome, cpf, data_nascimento, endereco):
        super().__init__(endereco)
        self.nome = nome
        self.cpf = cpf
        self.data_nascimento = data_nascimento

# Conta
class Conta:
    def __init__(self, cliente, numero, agencia='0001'):
        self.saldo = 0.0
        self.numero = numero
        self.agencia = agencia
        self.cliente = cliente
        self.historico = Historico()

    def saldo_atual(self):
        return self.saldo

    def sacar(self, valor):
        if valor > self.saldo:
            return False
        self.saldo -= valor
        return True

    def depositar(self, valor):
        if valor > 0:
            self.saldo += valor
            return True
        return False

    @classmethod
    def nova_conta(cls, cliente, numero):
        return cls(cliente, numero)


#interfase (transação)
class Transacao(ABC):
    @abstractmethod
    def registrar(self, conta):
        pass


class Deposito (transacao):
    def __init__ (self,valor):
        self.valor = valor
    
    def registrar(self, conta):
        return conta.depositar(self.valor)
    
class Saque (transacao):
    def __init__(self,valor):
        self.valor = valor
    
    def registrar(self, conta):
        return conta.sacar(self.valor)

#Conta Corrente

class Contacorrente(conta):
    def __init_ (self, limite_saque, limite):
        self.limite_saque = 3
        self.limite = 500.00
        self.saques_realizados = 0
