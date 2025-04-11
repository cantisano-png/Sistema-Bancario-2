import textwrap

def menu():
    menu = """\n
    ================== MENU ==================

    [d]\tDepositar
    [s]\tSacar
    [e]\tExtrato
    [nc]\tNova Conta
    [lc]\tListar Contas
    [nu]\tNovo Usuário
    [q]\tSair

    => """
    return input(textwrap.dedent(menu))

def depositar(saldo, valor, extrato, /):
    if valor > 0:
        saldo += valor
        extrato += f"Depósito:\tR$ {valor:.2f}\n"
        print("\n||||| Depósito realizado com sucesso! |||||")
    else:
        print("\n§§§ Operação falhou! O valor informado é inválido. §§§")
    
    return saldo, extrato 

def sacar(*, saldo, valor, extrato, limite, número_saques, limite_saques):
    excedeu_saldo = valor > saldo
    excedeu_limite = valor > limite
    excedeu_saques = número_saques >= limite_saques

    if excedeu_saldo:
        print("\n§§§ Operação falhou! Você não tem saldo suficiente. §§§")

    elif excedeu_limite:
        print("\n§§§ Operação falhou! O valor do saque excede o limite. §§§")

    elif excedeu_saques:
        print("\n§§§ Operação falhou! O número de saques diário foi excedido. §§§")

    elif valor > 0:
        saldo -= valor
        extrato += f"Saque:\t\tR$ {valor:.2f}\n"
        número_saques += 1
        print ("\n ||||| Saque realizado com sucesso! |||||")

    else:
        print("\n§§§ Operação falhou! O valor informado é inválido. §§§")

    return saldo, extrato, número_saques

def exibir_extrato(saldo, /, *, extrato):
    print("\n================== EXTRATO ==================")
    print("\nNão foram realizadas movimentações." if not extrato else extrato)
    print(f"\nSaldo:\t\tR$ {saldo:.2f}")
    print("===============================================")

def criar_usuário(usuários):
    cpf = input("\nInforme o CPF (somente número): ")
    usuário = filtrar_usuário(cpf, usuários)

    if usuário:
        print("\n§§§ Já existe usuário com esse CPF! §§§")
        return
    
    nome = input("\nInforme o nome completo: ")
    data_nascimento = input("\nInforme a data de nascimento (dd-mm-aaaa): ")
    endereço = input("\nInforme o endereço (logradouro, número - bairro - cidade/sigla estado): ")

    usuários.append({"nome": nome, "data_nascimento": data_nascimento, "cpf": cpf, "endereço": endereço})

    print("\n||||| Usuário criado com sucesso! |||||")

def filtrar_usuário(cpf, usuários):
    usuários_filtrados = [usuário for usuário in usuários if usuário["cpf"] == cpf]
    return usuários_filtrados[0] if usuários_filtrados else None

def criar_conta(agência, número_conta, usuários):
    cpf = input("Informe o CPF do usuário: ")
    usuário = filtrar_usuário(cpf, usuários)

    if usuário:
        print("\n ||||| Conta criada com sucesso! |||||")
        return {"agência": agência, "número_conta": número_conta, "usuário": usuário}
    
    print("\n §§§ Usuário não encontrado, fluxo de criação de conta encerrado! §§§")

def listar_contas(contas):
    for conta in contas:
        linha = f"""\
            Agência:\t{conta['agência']}
            C/C:\t\t{conta['número_conta']}
            Titular:\t{conta['usuário']['nome']}
        """
        print("=" * 100)
        print(textwrap.dedent(linha))


def main():
    LIMITE_SAQUES = 3
    AGÊNCIA = "0001"

    saldo = 0
    limite = 500
    extrato = ""
    número_saques = 0
    usuários = []
    contas = []

    while True:
        opção = menu()

        if opção == "d":
            valor = float(input("\nInforme o valor do depósito: "))

            saldo, extrato = depositar(saldo, valor, extrato)

        elif opção == "s":
            valor = float(input("\nInforme o valor do saque: "))

            saldo, extrato, número_saques = sacar(
                saldo=saldo,
                valor=valor,
                extrato=extrato,
                limite=limite,
                número_saques=número_saques,
                limite_saques=LIMITE_SAQUES
            )
        
        elif opção == "e":
            exibir_extrato(saldo, extrato=extrato)

        elif opção == "nu":
            criar_usuário(usuários)

        elif opção == "nc":
            número_conta = len(contas) + 1
            conta = criar_conta(AGÊNCIA, número_conta, usuários)

            if conta: 
                contas.append(conta)

        elif opção == "lc":
            listar_contas(contas)

        elif opção == "q":
            print("\nObrigado pela preferência, tenha um ótimo dia!")
            break

        else:
            print("\nOperação inválida, por favor selecione novamente a operação desejada.")

main ()