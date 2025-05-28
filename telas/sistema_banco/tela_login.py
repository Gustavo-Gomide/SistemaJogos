import pygame
from utilitarios.Aprincipal_widgets import Tela, Botao, CaixaTexto, TextoFormatado, Cores, Fontes
from databases.sistema_banco import SistemaBancario

class TelaLogin(Tela):
    def __init__(self, navegador):
        super().__init__(largura=800, altura=600, titulo="Login - Banco", cor_fundo=Cores.preto(), navegador=navegador)
        self.banco_dados = SistemaBancario()  # <--- ESSA LINHA É FUNDAMENTAL

        # Título com estilo retro
        self.titulo = TextoFormatado(400, 100, 
            texto="BANCO DIGITAL", 
            tamanho=48, 
            centralizado=True,
            cor_texto=Cores.dourado()
        )
        self.adicionar_componente(self.titulo)

        # Subtítulo
        self.subtitulo = TextoFormatado(400, 160,
            texto="Login do Sistema",
            tamanho=24,
            centralizado=True,
            cor_texto=Cores.verde_agua()
        )
        self.adicionar_componente(self.subtitulo)

        # Campos de entrada com estilo retro
        self.input_cpf = CaixaTexto(250, 250, 300, 40, 
            placeholder="CPF",
            cor_fundo=Cores.cinza_escuro(),
            cor_texto=Cores.verde_menta()
        )
        
        self.input_senha = CaixaTexto(250, 310, 300, 40,
            placeholder="Senha",
            cor_fundo=Cores.cinza_escuro(),
            cor_texto=Cores.verde_menta()
        )
        self.input_senha.mascara_texto = True
        
        self.adicionar_componente(self.input_cpf)
        self.adicionar_componente(self.input_senha)

        # Botões com estilo arcade
        self.botao_login = Botao(250, 380, 140, 50,
            texto="LOGIN",
            funcao=self.fazer_login,
            cor_fundo=Cores.verde_escuro(),
            cor_hover=Cores.verde_menta(),
            cor_texto=Cores.preto(),
            tamanho_fonte=20
        )
        
        self.botao_registro = Botao(410, 380, 140, 50,
            texto="NOVO",
            funcao=lambda: self.navegador.ir_para("registro_banco"),
            cor_fundo=Cores.azul_escuro(),
            cor_hover=Cores.azul_claro(),
            cor_texto=Cores.branco(),
            tamanho_fonte=20
        )
        
        self.adicionar_componente(self.botao_login)
        self.adicionar_componente(self.botao_registro)

        # Mensagem de status com estilo retro
        self.msg_status = TextoFormatado(400, 480,
            texto="",
            tamanho=20,
            centralizado=True,
            cor_texto=Cores.vermelho()
        )
        self.adicionar_componente(self.msg_status)

    def fazer_login(self):
        cpf = self.input_cpf.texto
        senha = self.input_senha.texto
        if self.banco_dados.login_cliente(cpf, senha):
            self.navegador.ir_para("menu_banco")
        else:
            self.msg_status.atualizar_texto("Login inválido!")