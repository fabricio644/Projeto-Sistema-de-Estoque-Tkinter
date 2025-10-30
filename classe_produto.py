class Produto:

    def __init__(self, nome, valor, quantidade, valortotal, tipo, endereco=None):

        self.nome = nome
        self.valor = valor
        self.quantidade = quantidade
        self.valortotal = valortotal
        self.tipo = tipo
        self.endereco = endereco

    def atualizar_valor_total(self):

        return self.valor * self.quantidade 