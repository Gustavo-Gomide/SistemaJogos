import pygame
from utilitarios.Aprincipal_widgets import Tela, Botao, CaixaTexto, TextoFormatado, Cores
from databases.sistema_banco import SistemaBanco

class TelaBanco(Tela):
    def __init__(self, navegador):
        super().__init__(largura=800, altura=600, titulo="Simulador de Banco", cor_fundo=Cores.cinza_claro(), navegador=navegador)
        self.estado_tela = "LOGIN"
        self.id_cliente_logado = None
        self.nome_cliente_logado = ""
        self.contas_cliente = []
        self.id_conta_selecionada = None
        self.saldo_conta_selecionada = None
        self.banco_dados = SistemaBanco

        # Mensagem de status
        self.mensagem_status = TextoFormatado(400, 500, texto="", cor_texto=Cores.vermelho(), tamanho=24, centralizado=True)
        self.adicionar_componente(self.mensagem_status)

        # Componentes da tela de login
        self.input_cpf_login = CaixaTexto(300, 200, 200, 40, placeholder="CPF")
        self.input_senha_login = CaixaTexto(300, 260, 200, 40, placeholder="Senha")
        self.botao_login = Botao(300, 320, 100, 40, texto="Login", funcao=self.fazer_login)
        self.botao_ir_registrar = Botao(410, 320, 100, 40, texto="Registrar", funcao=self.ir_para_registro)

        self.adicionar_componente(self.input_cpf_login)
        self.adicionar_componente(self.input_senha_login)
        self.adicionar_componente(self.botao_login)
        self.adicionar_componente(self.botao_ir_registrar)

        # Componentes da tela de registro
        self.input_nome_reg = CaixaTexto(300, 120, 200, 40, placeholder="Nome Completo")
        self.input_cpf_reg = CaixaTexto(300, 180, 200, 40, placeholder="CPF")
        self.input_senha_reg = CaixaTexto(300, 240, 200, 40, placeholder="Senha")
        self.input_confirma_senha_reg = CaixaTexto(300, 300, 200, 40, placeholder="Confirmar Senha")
        self.botao_confirmar_registro = Botao(300, 360, 200, 40, texto="Registrar", funcao=self.fazer_registro)
        self.botao_voltar_login = Botao(300, 420, 200, 40, texto="Voltar", funcao=self.voltar_para_login)

        self.adicionar_componente(self.input_nome_reg)
        self.adicionar_componente(self.input_cpf_reg)
        self.adicionar_componente(self.input_senha_reg)
        self.adicionar_componente(self.input_confirma_senha_reg)
        self.adicionar_componente(self.botao_confirmar_registro)
        self.adicionar_componente(self.botao_voltar_login)

    def fazer_login(self):
        cpf = self.input_cpf_login.texto
        senha = self.input_senha_login.texto
        id_cliente = self.banco_dados.login_cliente(cpf, senha)
        if id_cliente:
            self.id_cliente_logado = id_cliente
            self.nome_cliente_logado = "Cliente Simulado"  # Substitua por lógica real
            self.estado_tela = "MENU"
            self.mensagem_status.atualizar_texto(f"Bem-vindo, {self.nome_cliente_logado}!")
        else:
            self.mensagem_status.atualizar_texto("CPF ou senha inválidos.")

    def ir_para_registro(self):
        self.estado_tela = "REGISTRO"

    def fazer_registro(self):
        nome = self.input_nome_reg.texto
        cpf = self.input_cpf_reg.texto
        senha = self.input_senha_reg.texto
        confirma_senha = self.input_confirma_senha_reg.texto
        if senha != confirma_senha:
            self.mensagem_status.atualizar_texto("Senhas não coincidem.")
            return
        id_cliente = self.banco_dados.registrar_cliente(nome, cpf, senha)
        if id_cliente:
            self.mensagem_status.atualizar_texto(f"Cliente {nome} registrado com sucesso!")
            self.estado_tela = "LOGIN"
        else:
            self.mensagem_status.atualizar_texto("Erro ao registrar cliente.")

    def voltar_para_login(self):
        self.estado_tela = "LOGIN"

    def desenhar(self, tela):
        super().desenhar(tela)
        for componente in self.componentes:
            componente.desenhar(tela)
from utilitarios.Aprincipal_widgets import Tela, Botao, CaixaTexto, TextoFormatado, Cores
from databases.sistema_banco import SistemaBanco

class TelaLogin(Tela):
    def __init__(self, navegador):
        super().__init__(largura=800, altura=600, titulo="Login - Banco", cor_fundo=Cores.cinza_claro(), navegador=navegador)
        self.banco_dados = SistemaBanco()

        # Mensagem de status
        self.mensagem_status = TextoFormatado(400, 500, texto="", cor_texto=Cores.vermelho(), tamanho=24, centralizado=True)
        self.adicionar_componente(self.mensagem_status)

        # Componentes da tela de login
        self.input_cpf_login = CaixaTexto(300, 200, 200, 40, placeholder="CPF")
        self.input_senha_login = CaixaTexto(300, 260, 200, 40, Cores.branco(), placeholder="Senha")
        self.botao_login = Botao(300, 320, 100, 40, texto="Login", funcao=self.fazer_login)
        self.botao_ir_registrar = Botao(410, 320, 100, 40, texto="Registrar", funcao=lambda: self.navegador.ir_para("registro"))

        self.adicionar_componente(self.input_cpf_login)
        self.adicionar_componente(self.input_senha_login)
        self.adicionar_componente(self.botao_login)
        self.adicionar_componente(self.botao_ir_registrar)

    def fazer_login(self):
        cpf = self.input_cpf_login.texto
        senha = self.input_senha_login.texto
        id_cliente = self.banco_dados.login_cliente(cpf, senha)
        if id_cliente:
            self.navegador.ir_para("menu_banco")
        else:
            self.mensagem_status.atualizar_texto("CPF ou senha inválidos.")
     
from utilitarios.Aprincipal_widgets import Tela, Botao, CaixaTexto, TextoFormatado, Cores
from databases.sistema_banco import SistemaBanco

class TelaRegistro(Tela):
    def __init__(self, navegador):
        super().__init__(largura=800, altura=600, titulo="Registro - Banco", cor_fundo=Cores.cinza_claro(), navegador=navegador)
        self.banco_dados = SistemaBanco()

        # Mensagem de status
        self.mensagem_status = TextoFormatado(400, 500, texto="", cor_texto=Cores.vermelho(), tamanho=24, centralizado=True)
        self.adicionar_componente(self.mensagem_status)

        # Componentes da tela de registro
        self.input_nome_reg = CaixaTexto(300, 120, 200, 40, placeholder="Nome Completo")
        self.input_cpf_reg = CaixaTexto(300, 180, 200, 40, placeholder="CPF")
        self.input_senha_reg = CaixaTexto(300, 240, 200, 40, placeholder="Senha")
        self.input_confirma_senha_reg = CaixaTexto(300, 300, 200, 40, placeholder="Confirmar Senha")
        self.botao_confirmar_registro = Botao(300, 360, 200, 40, texto="Registrar", funcao=self.fazer_registro)
        self.botao_voltar_login = Botao(300, 420, 200, 40, texto="Voltar", funcao=lambda: self.navegador.ir_para("login"))

        self.adicionar_componente(self.input_nome_reg)
        self.adicionar_componente(self.input_cpf_reg)
        self.adicionar_componente(self.input_senha_reg)
        self.adicionar_componente(self.input_confirma_senha_reg)
        self.adicionar_componente(self.botao_confirmar_registro)
        self.adicionar_componente(self.botao_voltar_login)

    def fazer_registro(self):
        nome = self.input_nome_reg.texto
        cpf = self.input_cpf_reg.texto
        senha = self.input_senha_reg.texto
        confirma_senha = self.input_confirma_senha_reg.texto
        if senha != confirma_senha:
            self.mensagem_status.atualizar_texto("Senhas não coincidem.")
            return
        id_cliente = self.banco_dados.registrar_cliente(nome, cpf, senha)
        if id_cliente:
            self.navegador.ir_para("login")
        else:
            self.mensagem_status.atualizar_texto("Erro ao registrar cliente.")

    def rodar(self):
        """Executa a lógica da tela."""
        while True:
            self.desenhar(pygame.display.get_surface())
from utilitarios.Aprincipal_widgets import Tela, Botao, TextoFormatado, Cores

class TelaMenuBanco(Tela):
    def __init__(self, navegador):
        super().__init__(largura=800, altura=600, titulo="Menu - Banco", cor_fundo=Cores.cinza_claro(), navegador=navegador)

        # Componentes
        self.botao_saldo = Botao(300, 200, 200, 40, texto="Consultar Saldo", funcao=lambda: self.navegador.ir_para("saldo"))
        self.botao_deposito = Botao(300, 260, 200, 40, texto="Realizar Depósito", funcao=lambda: self.navegador.ir_para("deposito"))
        self.botao_saque = Botao(300, 320, 200, 40, texto="Realizar Saque", funcao=lambda: self.navegador.ir_para("saque"))
        self.botao_pix = Botao(300, 380, 200, 40, texto="Realizar PIX", funcao=lambda: self.navegador.ir_para("pix"))
        self.botao_extrato = Botao(300, 440, 200, 40, texto="Consultar Extrato", funcao=lambda: self.navegador.ir_para("extrato"))
        self.botao_voltar = Botao(300, 500, 200, 40, texto="Sair", funcao=lambda: self.navegador.ir_para("login"))

        self.adicionar_componente(self.botao_saldo)
        self.adicionar_componente(self.botao_deposito)
        self.adicionar_componente(self.botao_saque)
        self.adicionar_componente(self.botao_pix)
        self.adicionar_componente(self.botao_extrato)
        self.adicionar_componente(self.botao_voltar)

    def rodar(self):
        """Executa a lógica da tela."""
        while True:
            self.desenhar(pygame.display.get_surface())

