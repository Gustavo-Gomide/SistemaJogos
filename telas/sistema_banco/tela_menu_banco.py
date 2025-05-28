import pygame
from utilitarios.Aprincipal_widgets import Tela, Botao, TextoFormatado, Cores
from databases.sistema_banco import SistemaBancario

class TelaMenuBanco(Tela):
    def __init__(self, navegador):
        super().__init__(largura=800, altura=600, titulo="Menu - Banco", cor_fundo=Cores.cinza_claro(), navegador=navegador)
        # Título
        self.titulo = TextoFormatado(400, 100, texto="Menu do Banco", tamanho=36, centralizado=True)
        self.adicionar_componente(self.titulo)

        # Botões
        opcoes = [
            ("Consultar Saldo", "saldo_banco"),
            ("Realizar Depósito", "deposito_banco"),
            ("Realizar Saque", "saque_banco"),
            ("Realizar PIX", "pix_banco"),
            ("Voltar ao Menu", "menu")
        ]

        largura_botao = 300
        x_centralizado = (800 - largura_botao) // 2  # Centraliza os botões na tela
        y_inicial = 200
        for i, (texto, tela) in enumerate(opcoes):
            self.adicionar_componente(
                Botao(x_centralizado, y_inicial + i*70, largura_botao, 60,  # Ajuste de tamanho para letras padronizadas
                     texto=texto,
                     funcao=lambda t=tela: self.navegador.ir_para(t))
            )
        
    def consultar_saldo(self, conta_selecionada_obj):
        saldo = SistemaBancario.consultar_saldo(conta_selecionada_obj.id_conta)
        return saldo if saldo is not None else "Erro ao consultar saldo"