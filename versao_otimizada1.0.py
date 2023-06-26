def menu():
    menu = """\n
    [d] \tDepositar
    [s] \tSacar
    [e] \tExtrato
    [nc] \tNova Conta
    [nu] \tNovo Usuário
    [q]\33[4;49;31m \tSair\33[m
    
    => """
    return input(menu).upper()

def depositar(saldo, valor, extrato, /):
    if valor > 0:
        saldo += valor
        extrato+= f'Depósito: R${valor:.2f}!\n'
        print('\nDeposito Realizado!')
    else:
        print('\nOperação falhou! O valor informado é inválido.')

    return saldo, extrato

def sacar(*, saldo, valor, extrato, limite, numero_saques, limite_saques):
    excedeu_saldo = valor > saldo
    excedeu_limite = valor > limite
    excedeu_saques = numero_saques >= limite_saques

    if excedeu_saldo:
        print('Operação falhou! Você não tem saldo suficiente.')

    elif excedeu_limite:
        print('Operação falhou! O valor do saque excedeu o limite.')
        
    elif excedeu_saques:
        print('Operação falhou! Número máximo de saques excedido.')
    
    elif valor > 0:
        saldo -= valor
        extrato += f'Saque: R$ {valor:.2f}\n'
        numero_saques += 1
        print(f'R$ {valor:.2f} foi retirado da conta.')

    else:
        print('Operação falhou! O valor informado é inválido.')

    return saldo, extrato, numero_saques

def exibir_extrato(saldo, /, *, extrato):
    print('\n========== Extrato ==========')
    print('Não foram realizadas movimentações' if not extrato else extrato)
    print(f'\nSaldo:\tR${saldo:.2f}')
    print('===============================')

def criar_usuario(usuarios):
    cpf = input('Informe o CPF: ')
    usuario = filtrar_usuario(cpf, usuarios)

    if usuario:
        print('CPF já cadastrado!')
        return
    
    nome = input('Informe o nome completo: ')
    data_nascimento = input('Informe a data de nascimento: ')
    endereco = input('Informe o endereço (Estado, Cidade, N°): ')

    usuarios.apped({'nome': nome, 'data_nascimento': data_nascimento, 'cpf': cpf, 'endereço': endereco})

    print('Usuario criado!')

def criar_conta(agencia, numero_conta, usuarios):
    cpf = input('Informe o CPF do Usuario: ')
    usuario = filtrar_usuario(cpf, usuarios)

    if usuario:
        print('\nConta criada')
        return {'agencia': agencia, 'numero_conta': numero_conta, 'usuario': usuario}
    
    print('\nUsuário não encontrado, fluxo de criação de conta encerrado!')

def filtrar_usuario(cpf, usuarios):
    usuarios_filtrados = [usuario for usuario in usuarios if usuario['cpf'] == cpf]
    return usuarios_filtrados[0] if usuarios_filtrados else None
    for conta in contas:
        linha = f"""\
        Agência:\t{conta['agencia']}
        C/C\t\t{conta['numero_conta']}
        Titular:\t{conta['usuario']['nome']}
        """
        print('+='*50)
        print(linha)

def listar_contas(contas):
    for conta in contas:
        linha = f"""
            Agência:\t{conta['agencia']}
            C/C:\t\t{conta['numero_conta']}
            Titular:\t{conta['usuario']['nome']}
        """
        print("+="*50)
        print(linha)

def main():
    LIMITE_SAQUES = 3
    AGENCIA = '0001'

    saldo = 0
    limite = 500
    extrato = ""
    numero_saques = 0
    usuarios = []
    contas = []

    while True:
        opcao = menu()

        if opcao == 'D':
            valor = float(input('Valor do depósito: '))

            saldo, extrato = depositar(saldo, valor, extrato)

        elif opcao == 'S':
            valor = float(input('Valor de saque: '))

            saldo, extrato, numero_saques = sacar(
                saldo=saldo, valor=valor,
                extrato=extrato, limite=limite,
                numero_saques=numero_saques,
                limite_saques=LIMITE_SAQUES
            )

        elif opcao == 'E':
            exibir_extrato(saldo, extrato=extrato)

        elif opcao == 'NU':
            criar_usuario(usuarios)
        
        elif opcao == 'NC':
            numero_conta = len(contas) + 1
            conta = criar_conta(AGENCIA, numero_conta, usuarios)

            if conta:
                contas.append(conta)
        
        elif opcao == 'LC':
            listar_contas(contas)

        elif opcao == 'Q':
            break

        else:
            print('Operação inválida, selecione uma opção novamente.')


main()