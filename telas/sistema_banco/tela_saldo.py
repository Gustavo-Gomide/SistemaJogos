import pygame
from utilitarios.Aprincipal_widgets import Tela, Botao, TextoFormatado, Cores, Fontes
from databases.sistema_banco import SistemaBancario

class TelaSaldo(Tela):
    def __init__(self, navegador):
        super().__init__(largura=800, altura=600, titulo="Saldo - Banco", cor_fundo=Cores.preto(), navegador=navegador)
        self.banco_dados = SistemaBancario()
        self.id_conta_atual = None  # Variável para armazenar o ID da conta atual
        # Título retro
        # Supondo que você tem self.id_conta_atual definido ao logar/selecionar conta
        self.saldo = self.banco_dados.consultar_saldo(self.id_conta_atual)
        self.titulo = TextoFormatado(400, 100, texto="CONSULTA DE SALDO", tamanho=36, centralizado=True, cor_texto=Cores.dourado())
        self.adicionar_componente(self.titulo)

        # Exibição do Saldo
        self.saldo_texto = TextoFormatado(400, 250, texto="Saldo: R$ 0,00", tamanho=32, centralizado=True, cor_texto=Cores.verde_menta())
        self.adicionar_componente(self.saldo_texto)

        # Botão Atualizar
        self.botao_atualizar = Botao(300, 350, 200, 50, texto="Atualizar Saldo",
                                     funcao=self.atualizar_saldo,
                                     cor_fundo=Cores.verde_escuro(),
                                     cor_hover=Cores.verde_menta(),
                                     cor_texto=Cores.preto(),
                                     tamanho_fonte=20)
        self.adicionar_componente(self.botao_atualizar)

        # Botão Voltar
        self.botao_voltar = Botao(300, 420, 200, 50, texto="Voltar",
                                  funcao=lambda: self.navegador.ir_para("menu_banco"),
                                  cor_fundo=Cores.azul_escuro(),
                                  cor_hover=Cores.azul_claro(),
                                  cor_texto=Cores.branco(),
                                  tamanho_fonte=20)
        self.adicionar_componente(self.botao_voltar)

    def atualizar_saldo(self):
        # Supondo que você tem self.id_conta_atual definido ao logar/selecionar conta
        saldo = self.banco_dados.consultar_saldo(self.id_conta_atual)
        self.saldo_texto.atualizar_texto(f"Saldo: R$ {saldo:.2f}" if saldo is not None else "Saldo: ERRO")