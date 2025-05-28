import pygame
from utilitarios.Aprincipal_widgets import Tela, Botao, CaixaTexto, TextoFormatado, Cores, Fontes
from databases.sistema_banco import SistemaBanco

class TelaPix(Tela):
    def __init__(self, navegador):
        super().__init__(largura=800, altura=600, titulo="PIX - Banco", cor_fundo=Cores.preto(), navegador=navegador)
        self.banco_dados = SistemaBanco()

        self.titulo = TextoFormatado(400, 100, texto="TRANSFERÊNCIA PIX", tamanho=36, centralizado=True, cor_texto=Cores.dourado())
        self.adicionar_componente(self.titulo)

        self.input_chave = CaixaTexto(300, 200, 200, 40, placeholder="Chave PIX", cor_fundo=Cores.cinza_escuro(), cor_texto=Cores.verde_menta())
        self.adicionar_componente(self.input_chave)

        self.input_valor = CaixaTexto(300, 260, 200, 40, placeholder="Valor R$", cor_fundo=Cores.cinza_escuro(), cor_texto=Cores.verde_menta())
        self.adicionar_componente(self.input_valor)

        self.botao_enviar = Botao(300, 320, 200, 50, texto="Enviar PIX", funcao=self.fazer_pix,
                                  cor_fundo=Cores.verde_escuro(), cor_hover=Cores.verde_menta(), cor_texto=Cores.preto(), tamanho_fonte=20)
        self.adicionar_componente(self.botao_enviar)

        self.botao_voltar = Botao(300, 390, 200, 50, texto="Voltar",
                                  funcao=lambda: self.navegador.ir_para("menu_banco"),
                                  cor_fundo=Cores.azul_escuro(), cor_hover=Cores.azul_claro(), cor_texto=Cores.branco(), tamanho_fonte=20)
        self.adicionar_componente(self.botao_voltar)

        self.msg_status = TextoFormatado(400, 460, texto="", cor_texto=Cores.vermelho(), centralizado=True)
        self.adicionar_componente(self.msg_status)

    def fazer_pix(self):
        try:
            chave = self.input_chave.texto
            valor = float(self.input_valor.texto)
            if self.banco_dados.realizar_pix(self.banco_dados.id_conta_atual, chave, valor):
                self.msg_status.atualizar_texto(f"PIX de R$ {valor:.2f} realizado com sucesso!")
            else:
                self.msg_status.atualizar_texto("Erro ao realizar PIX!")
        except ValueError:
            self.msg_status.atualizar_texto("Valor inválido!")