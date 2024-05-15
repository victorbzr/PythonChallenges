import textwrap

def menu():
    menu = """
    ================= MENU =================
    [1]\tDepositar
    [2]\tSacar
    [3]\tExtrato
    [4]\tNovo Usuário
    [5]\tNova Conta
    [6]\tListar Contas
    [7]\tSair
    => """
    return input(textwrap.dedent(menu))

def depositar(saldo, valor, extrato, /):
    if valor > 0:
        saldo += valor
        extrato += f"Depósito: R$ {valor:.2f}\n"
    else:
        print("Operação falhou! O valor informado é inválido.")
    return saldo, extrato

def sacar(*, saldo, valor, extrato, limite, numero_saques, limite_saques):
    excedeu_saldo = valor > saldo
    excedeu_limite = valor > limite
    excedeu_saques = numero_saques >= limite_saques
    if excedeu_saldo:
        print("Operação falhou! Saldo suficiente.")
        
    elif excedeu_limite:
        print("Operação falhou! O valor do saque excede o limite.")
        
    elif excedeu_saques:
        print("Operação falhou! Número máximo de saques diários excedido.")

    elif valor > 0:
        saldo -= valor
        extrato += f"Saque: R$ {valor:.2f}\n"
        numero_saques += 1
        print("Saque realizado com sucesso")

    else:
        print("Operação falhou! O valor informado é inválido.")
    
    return saldo, extrato, numero_saques

def exibir_extrato(saldo, /, *, extrato):
    print("\n================ EXTRATO ================")
    print("Não foram realizadas movimentações." if not extrato else extrato)
    print(f"\nSaldo: R$ {saldo:.2f}")
    print("==========================================")

def criar_usuario(usuarios):
    cpf = input("Informe o CPF(somente números):")
    usuario = filtrar_usuarios(cpf, usuarios)
    
    if usuario:
        print("@@@ Já existe um usuário vinculado ao CPF informado @@@")
        return
    
    nome = input("Informe o nome completo:")
    data_nascimento = input("Informe a data de nascimento (dd-MM-AAAA)")
    endereco = input("Informe o endereço (logradouro, nro - bairro - cidade/sigla estado):")
    
    usuarios.append({"nome": nome, "data_nascimento": data_nascimento, "cpf": cpf, "endereco": endereco})
    print("=== Usuário criado com sucesso ===")
    
def filtrar_usuarios(cpf, usuarios):
    usuarios_filtrados = [usuario for usuario in usuarios if usuario["cpf"] == cpf]
    return usuarios_filtrados[0] if usuarios_filtrados else None

def criar_conta(agencia, numero_conta, usuarios, contas):
    cpf = input("Informe o CPF do usuário (somente números)")
    usuario = filtrar_usuarios(cpf, usuarios)
    
    if usuario:
        print("=== Conta criada com sucesso ===")
        contas.append({"agencia": agencia, "numero_conta": numero_conta, "usuario": usuario})
        return
    
    print("@@@ Usuário não encontrado, criação de conta encerrada! @@@")

def listar_contas(contas):
    for conta in contas:
        linha = f"""
        ==================================================
            Agencia: {conta['agencia']}
            Conta: {conta['numero_conta']}
            Titular: {conta['usuario']['nome']}
        ==================================================
        """
        print(textwrap.dedent(linha))

def main():
    LIMITE_SAQUES = 3
    AGENCIA = "0001"
    
    saldo = 0
    limite = 500
    extrato = ""
    numero_saques = 0
    usuarios = []
    contas = []

    while True:

        opcao = menu()
    
        if opcao == "1":
            valor = float(input("Informe o valor do depósito: "))

            saldo, extrato = depositar(saldo, valor, extrato)
            

        elif opcao == "2":
            valor = float(input("Informe o valor do saque: "))

            saldo, extrato, numero_saques = sacar(
                saldo = saldo,
                valor = valor,
                extrato = extrato,
                limite = limite,
                numero_saques = numero_saques,
                limite_saques = LIMITE_SAQUES,
            )
            

        elif opcao == "3":
            exibir_extrato(saldo, extrato = extrato)
            
        elif opcao == "4":
            criar_usuario(usuarios)
            
        elif opcao == "5":
            numero_conta = len(contas)+1
            conta = criar_conta(AGENCIA, numero_conta, usuarios, contas)
        
        elif opcao == "6":
            listar_contas(contas)
        
        elif opcao == "7":
            break

        else:
            print("Operação inválida, por favor selecione novamente a operação desejada.")
            
main()