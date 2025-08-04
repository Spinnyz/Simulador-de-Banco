
from datetime import date

#Cliente
class cliente:    
    def __init__(self, endereco):
        self.endereco = endereco
        self.contaconta = []
    
    def adicionarconta(self,conta):
        self.conta.append(conta)
    
    def realizar_transação(self,conta,transacao):
        transacao.registrar(conta)
        conta.historico.adicionar_transacao(transacao)
        

#Pessoa física
class Pessoafisica():
    def nome (self,nome,cpf,data_nascimento,endereco):
        super().__init__(endereco)
        self.nome = nome
        self.cpf = cpf
        self.data_nascimento = data_nascimento

#Conta
class Conta():
    def __init__(self,saldo,numero,agencia,cliente,historico):
        self.saldo = 0.0
        self.numero = numero
        self.agencia = agencia
        self.cliente = cliente
        self.historico = historico
        

        
        
    
