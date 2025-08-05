from datetime import date
from abc import ABC, abstractmethod


# Classe Historico
class Historico:
    def __init__(self):
        self.transacoes = []

    def adicionar_transacao(self, transacao):
        self.transacoes.append(transacao)

    def mostrar_extrato(self):
        if not self.transacoes:
            print("Nenhuma transação realizada.")
            return
        for t in self.transacoes:
            tipo = type(t).__name__
            valor = t.valor
            print(f"{tipo}: R$ {valor:.2f}")


# Cliente
class Cliente:
    def __init__(self, endereco):
        self.endereco = endereco
        self.contas = []

    def adicionar_conta(self, conta):
        self.contas.append(conta)

    def realizar_transacao(self, conta, transacao):
        sucesso = transacao.registrar(conta)
        if sucesso:
            conta.historico.adicionar_transacao(transacao)
        return sucesso


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


# Interface (transação)
class Transacao(ABC):
    @abstractmethod
    def registrar(self, conta):
        pass


class Deposito(Transacao):
    def __init__(self, valor):
        self.valor = valor

    def registrar(self, conta):
        return conta.depositar(self.valor)


class Saque(Transacao):
    def __init__(self, valor):
        self.valor = valor

    def registrar(self, conta):
        return conta.sacar(self.valor)


# Conta Corrente (corrigido nome e variável limite_saques)
class ContaCorrente(Conta):
    def __init__(self, cliente, numero, limite_saques=3, limite=500.00):
        super().__init__(cliente, numero)
        self.limite_saques = limite_saques
        self.limite = limite
        self.saques_realizados = 0

    def sacar(self, valor):
        if self.saques_realizados >= self.limite_saques:
            print("Limite de saques atingido")
            return False

        if valor > self.limite:
            print("Valor excede o limite por saque")
            return False

        feito = super().sacar(valor)
        if feito:
            self.saques_realizados += 1
        return feito


def menu():
    clientes = []
    contas = []

    while True:
        opcao = input("""
================ MENU ================
[d]\tDepositar
[s]\tSacar
[e]\tExtrato
[nc]\tNova conta
[lc]\tListar contas
[nu]\tNovo usuário
[q]\tSair
=> """).lower().strip()

        if opcao == "nu":
            cpf = input("Informe o CPF (somente número): ")
            nome = input("Informe o nome completo: ")
            data_nascimento = input("Informe a data de nascimento (dd-mm-aaaa): ")
            endereco = input("Informe o endereço (logradouro, nro - bairro - cidade/sigla estado): ")
            cliente = PessoaFisica(nome=nome, cpf=cpf, data_nascimento=data_nascimento, endereco=endereco)
            clientes.append(cliente)
            print("Usuário criado com sucesso :D")

        elif opcao == "nc":
            cpf = input("Informe o CPF do usuário: ")
            cliente = next((c for c in clientes if c.cpf == cpf), None)

            if not cliente:
                print("Cliente não encontrado")
                continue

            numero = len(contas) + 1
            conta = ContaCorrente(cliente=cliente, numero=numero)
            cliente.contas.append(conta)
            contas.append(conta)
            print(f"Conta criada, boa! Número: {numero}")

        elif opcao == "lc":
            if not contas:
                print("Nenhuma conta cadastrada.")
                continue

            print("\nContas cadastradas:")
            for conta in contas:
                print(f"Agência: {conta.agencia} | Conta: {conta.numero} | Cliente: {conta.cliente.nome}")

        elif opcao == "d":
            cpf = input("Informe o CPF do usuário: ")
            cliente = next((c for c in clientes if c.cpf == cpf), None)

            if not cliente or not cliente.contas:
                print("Cliente ou conta não encontrada.")
                continue

            valor = float(input("Valor do depósito: "))
            conta = cliente.contas[0]
            transacao = Deposito(valor)
            sucesso = cliente.realizar_transacao(conta, transacao)

            if sucesso:
                print("Depósito realizado com sucesso.")
            else:
                print("Falha no depósito.")

        elif opcao == "s":
            cpf = input("Informe o CPF do usuário: ")
            cliente = next((c for c in clientes if c.cpf == cpf), None)

            if not cliente or not cliente.contas:
                print(" Cliente ou conta não encontrada.")
                continue

            valor = float(input("Valor do saque: "))
            conta = cliente.contas[0]
            transacao = Saque(valor)
            sucesso = cliente.realizar_transacao(conta, transacao)

            if sucesso:
                print("Saque realizado com sucesso.")
            else:
                print("Saque não realizado.")

        elif opcao == "e":
            cpf = input("Informe o CPF do usuário: ")
            cliente = next((c for c in clientes if c.cpf == cpf), None)

            if not cliente or not cliente.contas:
                print("Cliente ou conta não encontrada.")
                continue

            conta = cliente.contas[0]
            print(f"\n=== Extrato da Conta {conta.numero} ===")
            conta.historico.mostrar_extrato()
            print(f"Saldo atual: R$ {conta.saldo:.2f}")

        elif opcao == "q":
            print("Saindo... Até mais!")
            break

        else:
            print("Opção inválida.")


if __name__ == "__main__":
    menu()
