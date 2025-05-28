import pygame
from utilitarios.Aprincipal_widgets import Tela, Botao, CaixaTexto, TextoFormatado, Cores, Fontes
from databases.sistema_banco import Conta

class TelaDeposito(Tela):
    def __init__(self, navegador):
        super().__init__(largura=800, altura=600, titulo="Depósito - Banco", cor_fundo=Cores.preto(), navegador=navegador)
        #self.banco_dados = Conta()  # Inicializa com uma conta vazia

        self.titulo = TextoFormatado(400, 100, texto="REALIZAR DEPÓSITO", tamanho=36, centralizado=True, cor_texto=Cores.dourado())
        self.adicionar_componente(self.titulo)

        self.input_valor = CaixaTexto(300, 200, 200, 40, placeholder="Valor R$", cor_fundo=Cores.cinza_escuro(), cor_texto=Cores.verde_menta())
        self.adicionar_componente(self.input_valor)

        self.botao_depositar = Botao(300, 260, 200, 50, texto="Depositar", funcao=self.fazer_deposito,
                                     cor_fundo=Cores.verde_escuro(), cor_hover=Cores.verde_menta(), cor_texto=Cores.preto(), tamanho_fonte=20)
        self.adicionar_componente(self.botao_depositar)

        self.botao_voltar = Botao(300, 330, 200, 50, texto="Voltar",
                                  funcao=lambda: self.navegador.ir_para("menu_banco"),
                                  cor_fundo=Cores.azul_escuro(), cor_hover=Cores.azul_claro(), cor_texto=Cores.branco(), tamanho_fonte=20)
        self.adicionar_componente(self.botao_voltar)

        self.msg_status = TextoFormatado(400, 400, texto="", cor_texto=Cores.vermelho(), centralizado=True)
        self.adicionar_componente(self.msg_status)

    def fazer_deposito(self):
        try:
            valor = float(self.input_valor.texto)
            if self.banco_dados.depositar(self.banco_dados.id_conta_atual, valor):
                self.msg_status.atualizar_texto(f"Depósito de R$ {valor:.2f} realizado com sucesso!")
            else:
                self.msg_status.atualizar_texto("Erro ao realizar depósito!")
        except ValueError:
            self.msg_status.atualizar_texto("Valor inválido!")