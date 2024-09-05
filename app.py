from abc import ABC, abstractmethod

# Transacao (Interface)
class Transacao(ABC):
    @abstractmethod
    def registrar(self, conta):
        pass

# Historico
class Historico:
    def __init__(self):
        self.transacoes = []

    def adicionar_transacao(self, transacao):
        self.transacoes.append(transacao)

    def exibir(self):
        if not self.transacoes:
            print("\nNão foram realizadas movimentações.")
        else:
            for transacao in self.transacoes:
                print(transacao)

# Deposito
class Deposito(Transacao):
    def __init__(self, valor):
        self.valor = valor

    def registrar(self, conta):
        if self.valor > 0:
            conta.saldo += self.valor
            conta.historico.adicionar_transacao(f"Depósito:\tR$ {self.valor:.2f}")
            print("\n=== Depósito realizado com sucesso! ===")
        else:
            print("\n@@@ Operação falhou! O valor informado é inválido. @@@")

# Saque
class Saque(Transacao):
    def __init__(self, valor):
        self.valor = valor

    def registrar(self, conta):
        excedeu_saldo = self.valor > conta.saldo
        excedeu_limite = self.valor > conta.limite
        excedeu_saques = conta.numero_saques >= conta.limite_saques

        if excedeu_saldo:
            print("\n@@@ Operação falhou! Você não tem saldo suficiente. @@@")
        elif excedeu_limite:
            print("\n@@@ Operação falhou! O valor do saque excede o limite. @@@")
        elif excedeu_saques:
            print("\n@@@ Operação falhou! Número máximo de saques excedido. @@@")
        elif self.valor > 0:
            conta.saldo -= self.valor
            conta.numero_saques += 1
            conta.historico.adicionar_transacao(f"Saque:\t\tR$ {self.valor:.2f}")
            print("\n=== Saque realizado com sucesso! ===")
        else:
            print("\n@@@ Operação falhou! O valor informado é inválido. @@@")

# Cliente
class Cliente:
    def __init__(self, endereco):
        self.endereco = endereco
        self.contas = []

    def realizar_transacao(self, conta, transacao):
        transacao.registrar(conta)

    def adicionar_conta(self, conta):
        self.contas.append(conta)

# PessoaFisica (herda de Cliente)
class PessoaFisica(Cliente):
    def __init__(self, cpf, nome, data_nascimento, endereco):
        super().__init__(endereco)
        self.cpf = cpf
        self.nome = nome
        self.data_nascimento = data_nascimento

# Conta
class Conta:
    def __init__(self, numero, agencia, cliente):
        self.saldo = 0.0
        self.numero = numero
        self.agencia = agencia
        self.cliente = cliente
        self.historico = Historico()

    @classmethod
    def nova_conta(cls, cliente, numero):
        return cls(numero, "0001", cliente)

# ContaCorrente (herda de Conta)
class ContaCorrente(Conta):
    def __init__(self, numero, agencia, cliente, limite, limite_saques):
        super().__init__(numero, agencia, cliente)
        self.limite = limite
        self.limite_saques = limite_saques
        self.numero_saques = 0

# Função para exibir o menu
def menu():
    menu = """
====================================
                MENU                  
====================================
[d]  Depositar
[s]  Sacar
[e]  Extrato
[nc] Nova conta
[lc] Listar contas
[nu] Novo usuário
[q]  Sair
====================================
"=> "
"""
    return input(menu)

def criar_usuario(usuarios):
    cpf = input("Informe o CPF (somente número): ")
    usuario = filtrar_usuario(cpf, usuarios)

    if usuario:
        print("\n@@@ Já existe usuário com esse CPF! @@@")
        return

    nome = input("Informe o nome completo: ")
    data_nascimento = input("Informe a data de nascimento (dd-mm-aaaa): ")
    endereco = input("Informe o endereço (logradouro, nro - bairro - cidade/sigla estado): ")

    novo_usuario = PessoaFisica(cpf, nome, data_nascimento, endereco)
    usuarios.append(novo_usuario)

    print("=== Usuário criado com sucesso! ===")

def filtrar_usuario(cpf, usuarios):
    usuarios_filtrados = [usuario for usuario in usuarios if usuario.cpf == cpf]
    return usuarios_filtrados[0] if usuarios_filtrados else None

def criar_conta(agencia, numero_conta, usuarios):
    cpf = input("Informe o CPF do usuário: ")
    usuario = filtrar_usuario(cpf, usuarios)

    if usuario:
        nova_conta = ContaCorrente(numero_conta, agencia, usuario, limite=500, limite_saques=3)
        usuario.adicionar_conta(nova_conta)
        print("\n=== Conta criada com sucesso! ===")
        return nova_conta

    print("\n@@@ Usuário não encontrado, fluxo de criação de conta encerrado! @@@")


def listar_contas(contas):
    if len(contas) == 0:
        print("\n@@@ Não há contas cadastradas. @@@")
    else:
        for conta in contas:
            print("=" * 100)
            print(f"Agência:\t{conta.agencia}")
            print(f"C/C:\t\t{conta.numero}")
            print(f"Titular:\t{conta.cliente.nome}")
            print("=" * 100)

# Função principal
def main():
    AGENCIA = "0001"
    usuarios = []
    contas = []

    while True:
        opcao = menu()

        if opcao == "d":
            cpf = input("Informe o CPF do usuário: ")
            usuario = filtrar_usuario(cpf, usuarios)

            if not usuario or not usuario.contas:
                print("\n@@@ Usuário ou conta não encontrados! @@@")
                continue

            conta = usuario.contas[0]  # Assumindo que o usuário tem apenas uma conta
            valor = float(input("Informe o valor do depósito: "))

            usuario.realizar_transacao(conta, Deposito(valor))

        elif opcao == "s":
            cpf = input("Informe o CPF do usuário: ")
            usuario = filtrar_usuario(cpf, usuarios)

            if not usuario or not usuario.contas:
                print("\n@@@ Usuário ou conta não encontrados! @@@")
                continue

            conta = usuario.contas[0]  # Assumindo que o usuário tem apenas uma conta
            valor = float(input("Informe o valor do saque: "))

            usuario.realizar_transacao(conta, Saque(valor))

        elif opcao == "e":
            cpf = input("Informe o CPF do usuário: ")
            usuario = filtrar_usuario(cpf, usuarios)

            if not usuario or not usuario.contas:
                print("\n@@@ Usuário ou conta não encontrados! @@@")
                continue

            conta = usuario.contas[0]  # Assumindo que o usuário tem apenas uma conta
            print("\n================ EXTRATO ================")
            conta.historico.exibir()
            print(f"\nSaldo:\t\tR$ {conta.saldo:.2f}")
            print("==========================================")

        elif opcao == "nu":
            criar_usuario(usuarios)

        elif opcao == "nc":
            numero_conta = len(contas) + 1
            conta = criar_conta(AGENCIA, numero_conta, usuarios)

            if conta:
                contas.append(conta)

        elif opcao == "lc":
            listar_contas(contas)

        elif opcao == "q":
            break

        else:
            print("Operação inválida, por favor selecione novamente a operação desejada.")

main()
