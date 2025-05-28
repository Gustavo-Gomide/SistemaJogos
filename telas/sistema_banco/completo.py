import pygame
from utilitarios.Aprincipal_widgets import Tela, Botao, CaixaTexto, TextoFormatado, Cores, Fontes
from databases import simulador_database

class MenuSimuladorTela(Tela):
    def __init__(self, navegador):
        super().__init__(600, 600, "Menu Banco", Cores.azul_escuro(), navegador)
        self._montar()

    def _montar(self):
        self.componentes.clear()
        self.adicionar_componente(TextoFormatado(
            x=300, y=80, texto="MENU BANCÁRIO", tamanho=40,
            cor_texto=Cores.branco(), fonte_nome=Fontes.consolas(), centralizado=True))

        botoes = [
            ("Consultar Saldo", "consultar saldo"),
            ("Realizar Depósito", "deposito"),
            ("Realizar Saque", "saque"),
            ("Realizar PIX", "pix")
        ]

        for i, (texto, destino) in enumerate(botoes):
            self.adicionar_componente(Botao(
                x=150, y=160 + i * 80, largura=300, altura=60,
                texto=texto, cor_fundo=Cores.verde(), cor_hover=Cores.verde_lima(),
                cor_texto=Cores.branco(), fonte=Fontes.consolas(), tamanho_fonte=26,
                funcao=lambda d=destino: self.navegador.ir_para(destino)
            ))

class ConsultarSaldoTela(Tela):
    def __init__(self, navegador, banco):
        super().__init__(600, 600, "Consultar Saldo", Cores.cinza_escuro(), navegador)
        self.banco = banco
        self._montar()

    def _montar(self):
        self.componentes.clear()
        self.caixa_id = CaixaTexto(150, 200, 300, 50, Cores.branco(), Cores.preto(), texto="ID da Conta")
        self.adicionar_componente(self.caixa_id)

        self.texto_resultado = TextoFormatado(300, 300, "", Cores.branco(), Fontes.consolas(), True)
        self.adicionar_componente(self.texto_resultado)

        self.adicionar_componente(Botao(150, 270, 300, 50, Cores.azul_claro(), Cores.azul(),
                                        Cores.preto(), "Consultar", Fontes.consolas(), 26, self._consultar))

        self._adicionar_botao_voltar()

    def _consultar(self):
        try:
            id_conta = int(self.caixa_id.texto)
            saldo = self.banco.consultar_saldo(id_conta)
            self.texto_resultado.texto = f"Saldo: R${saldo:.2f}"
        except:
            self.texto_resultado.texto = "Conta inválida."

    def _adicionar_botao_voltar(self):
        self.adicionar_componente(Botao(10, 540, 120, 40, Cores.vermelho(), Cores.vermelho_escuro(),
                                        Cores.branco(),"Voltar",  Fontes.consolas(), 20,
                                        lambda: self.navegador.ir_para("menu banco")))

class DepositoTela(Tela):
    def __init__(self, navegador, banco):
        super().__init__(600, 600, "Depósito", Cores.cinza(), navegador)
        self.banco = banco
        self._montar()

    def _montar(self):
        self.componentes.clear()
        self.caixa_id = CaixaTexto(150, 180, 300, 50, Cores.branco(), Cores.preto(), texto="ID da Conta")
        self.caixa_valor = CaixaTexto(150, 250, 300, 50, Cores.branco(), Cores.preto(), texto="Valor")
        self.adicionar_componente(self.caixa_id)
        self.adicionar_componente(self.caixa_valor)

        self.adicionar_componente(Botao(150, 320, 300, 50, Cores.verde(), Cores.verde_lima(),
                                        Cores.branco(), "Depositar", Fontes.consolas(), 26, self._depositar))
        self._adicionar_botao_voltar()

    def _depositar(self):
        try:
            id_conta = int(self.caixa_id.texto)
            valor = float(self.caixa_valor.texto)
            self.banco.depositar(id_conta, valor)
        except:
            pass

    def _adicionar_botao_voltar(self):
        self.adicionar_componente(Botao(10, 540, 120, 40, Cores.vermelho(), Cores.vermelho_escuro(),
                                        Cores.branco(), "Voltar", Fontes.consolas(), 20,
                                        lambda: self.navegador.ir_para("menu banco")))

class SaqueTela(Tela):
    def __init__(self, navegador, banco):
        super().__init__(600, 600, "Saque", Cores.cinza_claro(), navegador)
        self.banco = banco
        self._montar()

    def _montar(self):
        self.componentes.clear()
        self.caixa_id = CaixaTexto(150, 180, 300, 50, Cores.branco(), Cores.preto(), texto="ID da Conta")
        self.caixa_valor = CaixaTexto(150, 250, 300, 50, Cores.branco(), Cores.preto(), texto="Valor")
        self.adicionar_componente(self.caixa_id)
        self.adicionar_componente(self.caixa_valor)

        self.adicionar_componente(Botao(150, 320, 300, 50, Cores.verde(), Cores.verde_lima(),
                                        Cores.branco(), "Sacar", Fontes.consolas(), 26, self._sacar))
        self._adicionar_botao_voltar()

    def _sacar(self):
        try:
            id_conta = int(self.caixa_id.texto)
            valor = float(self.caixa_valor.texto)
            self.banco.sacar(id_conta, valor)
        except:
            pass

    def _adicionar_botao_voltar(self):
        self.adicionar_componente(Botao(10, 540, 120, 40,Cores.vermelho(), Cores.vermelho_escuro(),
                                        Cores.branco(), "Voltar",  Fontes.consolas(), 20,
                                        lambda: self.navegador.ir_para("menu banco")))

class PixTela(Tela):
    def __init__(self, navegador, banco):
        super().__init__(600, 600, "PIX", Cores.azul_claro(), navegador)
        self.banco = banco
        self._montar()

    def _montar(self):
        self.componentes.clear()
        self.caixa_origem = CaixaTexto(150, 150, 300, 50, Cores.branco(), Cores.preto(), texto="Conta Origem")
        self.caixa_destino = CaixaTexto(150, 220, 300, 50, Cores.branco(), Cores.preto(), texto="Conta Destino")
        self.caixa_valor = CaixaTexto(150, 290, 300, 50, Cores.branco(), Cores.preto(), texto="Valor")
        self.adicionar_componente(self.caixa_origem)
        self.adicionar_componente(self.caixa_destino)
        self.adicionar_componente(self.caixa_valor)

        self.adicionar_componente(Botao(150, 360, 300, 50, Cores.verde(), Cores.verde_lima(),
                                        Cores.branco(), "Enviar PIX", Fontes.consolas(), 26, self._pix))
        self._adicionar_botao_voltar()

    def _pix(self):
        try:
            origem = int(self.caixa_origem.texto)
            destino = int(self.caixa_destino.texto)
            valor = float(self.caixa_valor.texto)
            self.banco.transferir(origem, destino, valor)
        except:
            pass

    def _adicionar_botao_voltar(self):
        self.adicionar_componente(Botao(10, 540, 120, 40, Cores.vermelho(), Cores.vermelho_escuro(),
                                        Cores.branco(), "Voltar", Fontes.consolas(), 20,
                                        lambda: self.navegador.ir_para("menu banco")))
