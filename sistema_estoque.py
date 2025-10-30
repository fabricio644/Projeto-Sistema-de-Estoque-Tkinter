import csv
import os
from modelo.classe_produto import Produto
from modelo.classe_endereco import Endereco
from modelo.classe_usuario import Usuario

class SistemaEstoque:

    def __init__(self):
        
        self.produtos = [] # Banco de dados dos produtos
        self.enderecos = [] # Banco de dados Endereços
        self.usuarios = [] # Banco de dados Usuarios
        self.carregar_produtos_de_csv()
        self.carregar_enderecos_de_csv()
        self.carregar_usuarios_de_csv()

    def cadastrar_produto(self):

        nome = input("Digite o nome do Produto: ")
        valor = float(input("Digite o valor unitário do Produto: "))
        quantidade = 0
        valortotal = 0
        tipo = input("Digite o tipo do Produto: ")

        produto = Produto(nome, valor, quantidade, valortotal, tipo) # Objeto produto com os atributos

        self.produtos.append(produto) # Colocando no banco de dados

        print(f"{produto.nome} cadastrado com sucesso!")
        self.exportar_produtos_para_csv()

    def cadastrar_endereco(self):

        rua = input("Digite o numero da Rua: ")
        predio = input("Digite o numero da Prédio: ")
        andar = input("Digite o numero da Andar: ")
        posicao = input("Digite o numero da Posição: ")
        status_endereco = "L"

        endereco = Endereco(rua, predio, andar, posicao, status_endereco)

        self.enderecos.append(endereco)

        print("Endereço cadastrado com sucesso!")
        self.exportar_enderecos_para_csv()

    def cadastrar_usuario(self):

        nome_usuario = input("Digite o nome do Usuário: ")
        senha_usuario = input("Digite a senha do Usuário: ")
        cargo = input("Digite o cargo do Usuário: ")

        usuario = Usuario(nome_usuario, senha_usuario, cargo)
        self.usuarios.append(usuario)

        print("Usuário cadastrado com sucesso!")
        self.exportar_usuarios_para_csv()

    def promover_usuario(self):

        # Usuario com permissão pode promover usuario escolhido para outro cargo

        self.listar_usuarios()

        opcao = int(input("Selecione o usuario para Promover: "))

        if opcao > 0 and opcao <= len(self.usuarios):

            usuario_escolhido = self.usuarios[opcao - 1]    
            novo_cargo = input("Digite o novo cargo: ").lower()

            if novo_cargo != usuario_escolhido.cargo:

                if novo_cargo in ["gerente", "assistente", "analista"]:

                    usuario_escolhido.cargo = novo_cargo

                    print("Usuario promovido com sucesso!")

                else:
                    
                    print("Selecione um cargo valído!")

            else:

                print("Não é possivel promover para o mesmo cargo!")    

        else:

            print("Opção inválida!")

    def rebaixar_usuario(self):

        self.listar_usuarios()

        opcao = int(input("Selecione o usuario para Rebaixar: "))

        if opcao > 0 and opcao <= len(self.usuarios):

            usuario_escolhido = self.usuarios[opcao - 1]    
            novo_cargo = input("Digite o novo cargo: ").lower()

            if novo_cargo != usuario_escolhido.cargo:

                if novo_cargo in ["gerente", "assistente", "analista"]:

                    usuario_escolhido.cargo = novo_cargo

                    print("Usuario rebaixado com sucesso!")

                else:
                    
                    print("Selecione um cargo valído!")

            else:

                print("Não é possivel rebaixar para o mesmo cargo!")    

        else:

            print("Opção inválida!")

    def listar_usuarios(self):

        # Lista todos os usuarios

        if not self.usuarios:

            print("Nenhum usuário cadastrado!")
            return False
        
        else:

            for i, usuario in enumerate(self.usuarios, start=1):

                print(f"[{i}] - Nome: {usuario.nome_usuario} | Senha: {usuario.senha_usuario} | Cargo: {usuario.cargo}")

    def listar_enderecos(self):

        if not self.enderecos:

            print("Nenhum endereço cadastrado!")
            return False
        
        for i, endereco in enumerate(self.enderecos, start=1):

            produto_no_endereco = None

            for produto in self.produtos:

                    if produto.endereco == endereco:

                        produto_no_endereco = produto
                        break

            if produto_no_endereco:

                print(f"[{i}] Rua: {endereco.rua} | Prédio: {endereco.predio} | Andar: {endereco.andar} | Posição: {endereco.posicao} | Status: {endereco.status_endereco} | Produto: {produto_no_endereco.nome} | Quantidade: {produto_no_endereco.quantidade}")

            else:

                print(f"[{i}] Rua: {endereco.rua} | Prédio: {endereco.predio} | Andar: {endereco.andar} | Posição: {endereco.posicao} | Status: {endereco.status_endereco} | Produto: Nenhum | Quantidade: 0")

    def listar_produtos(self):

        if not self.produtos: # Verica se não tem nada no banco produtos

            print("Nenhum produto cadastrado!")
            return False

        for i, produto in enumerate(self.produtos, start=1): # i é a numeração, produtos são os objetos que vão ser enumerados em produtos

            print(f"[{i}] - Nome: {produto.nome} | Valor Unitário: R$ {produto.valor:.2f} | Quantidade: {produto.quantidade} | Valor Total: R$ {produto.valortotal:.2f} | Tipo: {produto.tipo}") # Não é necessario return True pois se usar vai listar sempre o primeiro

    def remover_produto(self):

        self.listar_produtos()

        opcao = int(input("Selecione o Produto: "))

        if opcao > 0 and opcao <= len(self.produtos):

            produto_escolhido = self.produtos[opcao - 1]

            del self.produtos[opcao - 1] # Deleta no banco de dados o produto escolhido, precisa do indice que é o opcao e o -1

            print(f"{produto_escolhido.nome} foi excluido.")

        else:

            print("Opção inválida!")

    def remover_usuario(self):

        self.listar_usuarios()

        opcao = int(input("Selecione o Usuário: "))

        if opcao > 0 and opcao <= len(self.usuarios):

            usuario_escolhido = self.usuarios[opcao - 1]

            del self.usuarios[opcao - 1] # Deleta no banco de dados o usuario escolhido, precisa do indice que é o opcao e o -1

            print(f"{usuario_escolhido.nome_usuario} foi excluido.")

        else:

            print("Opção inválida!")

    def remover_endereco(self):

        self.listar_enderecos()

        opcao = int(input("Selecione o Endereço: "))

        if opcao > 0 and opcao <= len(self.enderecos):

            endereco_escolhido = self.enderecos[opcao - 1]

            if endereco_escolhido.status_endereco == "L":

                del self.enderecos[opcao - 1] # Deleta no banco de dados o produto escolhido, precisa do indice que é o opcao e o -1
                print(f"{endereco_escolhido.rua} foi excluido.")

            else:

                print("Não é permitido excluir endereço com saldo!")

        else:

            print("Opção inválida!")

    def movimentacao_entrada(self):

        self.listar_produtos()

        opcao = int(input("Selecione o Produto: "))

        if opcao > 0 and opcao <= len(self.produtos):

            produto_escolhido = self.produtos[opcao - 1]

            self.listar_enderecos()

            opcao_endereco = int(input("Selecione o endereço: "))

            if opcao_endereco > 0 and opcao_endereco <= len(self.enderecos):

                endereco_escolhido = self.enderecos[opcao_endereco - 1]

                if endereco_escolhido.status_endereco == "L" or (
                    endereco_escolhido.status_endereco == "O" and produto_escolhido.endereco == endereco_escolhido
                ): # Verifica tambem se o produto armazenado é igual ao produto que foi escolhido
                    entrada = int(input("Digite a quantidade para Entrada: "))
                    if entrada > 0:
                        produto_escolhido.quantidade += entrada
                        produto_escolhido.valortotal = produto_escolhido.atualizar_valor_total()
                        endereco_escolhido.status_endereco = "O"
                        produto_escolhido.endereco = endereco_escolhido
                        print(
                            f"{produto_escolhido.nome} foi armazenado {entrada} no endereço Rua: {endereco_escolhido.rua} | Prédio: {endereco_escolhido.predio} com sucesso"
                        )
                    else:
                        print("Quantidade inválida!")
                else:
                    print("Endereço já está ocupado por outro produto!")

            else:
                print("Endereço inválido!")

        else:
            print("Produto inválido!")

    def movimentacao_saida(self):

        self.listar_enderecos()

        opcao_endereco = int(input("Selecione o endereço: "))

        if opcao_endereco > 0 and opcao_endereco <= len(self.enderecos):

            endereco_escolhido = self.enderecos[opcao_endereco - 1]

            if endereco_escolhido.status_endereco == "O":
                
                produto_escolhido = None

                for produto in self.produtos:

                    if produto.endereco == endereco_escolhido:
                        produto_escolhido = produto
                        break

                if produto_escolhido is None:

                    print("Nenhum produto encontrado neste endereço!")

                saida = int(input("Digite a quantidade para Saida: "))

                if saida <= produto_escolhido.quantidade:

                    produto_escolhido.quantidade -= saida
                    produto_escolhido.valortotal = produto_escolhido.atualizar_valor_total()
                    # Status do endereco atualizado

                    if produto_escolhido.quantidade == 0:
                        endereco_escolhido.status_endereco = "L"
                        produto_escolhido.endereco = None
                    else:
                        endereco_escolhido.status_endereco = "O"

                    print(f"{produto_escolhido.nome} teve uma movimetação de saida de {saida} no endereco Rua: {endereco_escolhido.rua} | Prédio: {endereco_escolhido.predio} com sucesso")

                else:

                    print("Quantidade inválida!")

            else:

                print("Endereço não possue produto!")

        else:
            print("Endereço inválido!")

    def movimentacao_transferencia(self):
        self.listar_enderecos()

        opcao_origem = int(input("Selecione o ENDEREÇO DE ORIGEM (ocupado): "))

        if opcao_origem > 0 and opcao_origem <= len(self.enderecos):
            endereco_origem = self.enderecos[opcao_origem - 1]

            if endereco_origem.status_endereco == "L":
                print("O endereço selecionado está livre. Escolha um endereço ocupado.")
                return

            # Encontrar o produto que está nesse endereço
            produto_encontrado = None
            for produto in self.produtos:
                if produto.endereco == endereco_origem:
                    produto_encontrado = produto
                    break

            if not produto_encontrado:
                print("Nenhum produto encontrado neste endereço.")
                return

            # Escolher endereço destino
            self.listar_enderecos()
            opcao_destino = int(input("Selecione o ENDEREÇO DE DESTINO (livre): "))

            if opcao_destino > 0 and opcao_destino <= len(self.enderecos):
                endereco_destino = self.enderecos[opcao_destino - 1]

                if endereco_destino.status_endereco == "O":
                    print("O endereço de destino já está ocupado!")
                    return

                # Faz a transferência
                produto_encontrado.endereco = endereco_destino
                endereco_origem.status_endereco = "L"
                endereco_destino.status_endereco = "O"

                print(f"Produto '{produto_encontrado.nome}' transferido com sucesso!")

            else:
                print("Endereço destino inválido!")

        else:
            print("Endereço origem inválido!")

    def exportar_produtos_para_csv(self):

        if not self.produtos:
            print("Nenhum produto cadastrado para exportar!")
            return

        with open("estoque.csv", "w", newline="", encoding="utf-8") as arquivo:
            escritor = csv.writer(arquivo)
            escritor.writerow(["Nome", "Valor Unitário", "Quantidade", "Valor Total", "Tipo"])

            for produto in self.produtos:
                escritor.writerow([produto.nome, produto.valor, produto.quantidade, produto.valortotal, produto.tipo])

        print("Dados exportados com sucesso para 'estoque.csv'!")

    def carregar_produtos_de_csv(self):
        if not os.path.exists("estoque.csv"):  # se o arquivo não existe ainda
            return  # não faz nada (primeira execução)

        with open("estoque.csv", "r", encoding="utf-8") as arquivo:
            leitor = csv.reader(arquivo)
            next(leitor)  # pula a primeira linha (cabeçalho)

            for linha in leitor:
                nome, valor, quantidade, valortotal, tipo = linha
                produto = Produto(nome, float(valor), int(quantidade), float(valortotal), tipo)
                self.produtos.append(produto)

        print(f"{len(self.produtos)} produtos carregados do arquivo estoque.csv.")


    def exportar_enderecos_para_csv(self):
        if not self.enderecos:
            print("Nenhum endereço cadastrado para exportar!")
            return

        with open("enderecos.csv", "w", newline="", encoding="utf-8") as arquivo:
            escritor = csv.writer(arquivo)
            escritor.writerow(["Rua", "Prédio", "Andar", "Posição", "Status"])

            for endereco in self.enderecos:
                escritor.writerow([
                    endereco.rua,
                    endereco.predio,
                    endereco.andar,
                    endereco.posicao,
                    endereco.status_endereco
                ])

        print("Endereços exportados com sucesso para 'enderecos.csv'!")

    def carregar_enderecos_de_csv(self):
        if not os.path.exists("enderecos.csv"):
            return  # Primeira execução, arquivo ainda não existe

        with open("enderecos.csv", "r", encoding="utf-8") as arquivo:
            leitor = csv.reader(arquivo)
            next(leitor)  # pula o cabeçalho

            for linha in leitor:
                rua, predio, andar, posicao, status = linha
                endereco = Endereco(int(rua), int(predio), int(andar), int(posicao), status)
                self.enderecos.append(endereco)

        print(f"{len(self.enderecos)} endereços carregados do arquivo enderecos.csv.")


    def exportar_usuarios_para_csv(self):
        if not self.usuarios:
            print("Nenhum usuário cadastrado para exportar!")
            return

        with open("usuarios.csv", "w", newline="", encoding="utf-8") as arquivo:
            escritor = csv.writer(arquivo)
            escritor.writerow(["Nome", "Senha", "Cargo"])
            for usuario in self.usuarios:
                escritor.writerow([usuario.nome_usuario, usuario.senha_usuario, usuario.cargo])

        print("Usuários exportados com sucesso para 'usuarios.csv'!")

    def carregar_usuarios_de_csv(self):
        if not os.path.exists("usuarios.csv"):
            return

        with open("usuarios.csv", "r", encoding="utf-8") as arquivo:
            leitor = csv.reader(arquivo)
            next(leitor)
            for linha in leitor:
                nome, senha, cargo = linha
                usuario = Usuario(nome, senha, cargo)
                self.usuarios.append(usuario)

        print(f"{len(self.usuarios)} usuários carregados do arquivo usuarios.csv.")




        