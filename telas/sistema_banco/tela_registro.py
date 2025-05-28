import pygame
from utilitarios.Aprincipal_widgets import Tela, Botao, CaixaTexto, TextoFormatado, Cores, Fontes
from databases.sistema_banco import SistemaBancario

class TelaRegistro(Tela):
    def __init__(self, navegador):
        super().__init__(largura=800, altura=600, titulo="Registro - Banco", cor_fundo=Cores.preto(), navegador=navegador)
        self.banco_dados = SistemaBancario()
        self.conta = None

        # Título com estilo retro
        self.titulo = TextoFormatado(400, 80,
            texto="CRIAR CONTA",
            tamanho=48,
            centralizado=True,
            cor_texto=Cores.dourado()
        )
        self.adicionar_componente(self.titulo)

        # Campos de entrada com estilo retro
        self.input_nome = CaixaTexto(250, 180, 300, 40,
            placeholder="Nome Completo",
            cor_fundo=Cores.cinza_escuro(),
            cor_texto=Cores.verde_agua()
        )
        
        self.input_cpf = CaixaTexto(250, 250, 300, 40,
            placeholder="CPF",
            cor_fundo=Cores.cinza_escuro(),
            cor_texto=Cores.verde_agua()
        )
        
        self.input_senha = CaixaTexto(250, 320, 300, 40,
            placeholder="Senha",
            cor_fundo=Cores.cinza_escuro(),
            cor_texto=Cores.verde_agua()
        )
        self.input_senha.mascara_texto = True
        
        self.input_confirma = CaixaTexto(250, 390, 300, 40,
            placeholder="Confirmar Senha",
            cor_fundo=Cores.cinza_escuro(),
            cor_texto=Cores.verde_agua()
        )
        self.input_confirma.mascara_texto = True

        self.adicionar_componente(self.input_nome)
        self.adicionar_componente(self.input_cpf)
        self.adicionar_componente(self.input_senha)
        self.adicionar_componente(self.input_confirma)

        # Botões com estilo arcade
        self.botao_registrar = Botao(250, 470, 140, 50,
            texto="CRIAR",
            funcao=self.fazer_registro,
            cor_fundo=Cores.verde_escuro(),
            cor_hover=Cores.verde_menta(),  # Changed from verde_neon to verde_menta
            cor_texto=Cores.branco(),
            tamanho_fonte=20
        )
        
        self.botao_voltar = Botao(410, 470, 140, 50,
            texto="VOLTAR",
            funcao=lambda: self.navegador.ir_para("login_banco"),
            cor_fundo=Cores.vermelho_escuro(),
            cor_hover=Cores.vermelho(),
            cor_texto=Cores.branco(),
            tamanho_fonte=20
        )

        self.adicionar_componente(self.botao_registrar)
        self.adicionar_componente(self.botao_voltar)

        # Mensagem de status
        self.msg_status = TextoFormatado(400, 540,
            texto="",
            tamanho=20,
            centralizado=True,
            cor_texto=Cores.vermelho()
        )
        self.adicionar_componente(self.msg_status)

    def fazer_registro(self):
        """Realiza o registro do novo usuário"""
        nome = self.input_nome.texto
        cpf = self.input_cpf.texto
        senha = self.input_senha.texto
        confirma = self.input_confirma.texto

        # Validações básicas
        if not nome or not cpf or not senha or not confirma:
            self.msg_status.atualizar_texto("Preencha todos os campos!")
            return

        if senha != confirma:
            self.msg_status.atualizar_texto("As senhas não coincidem!")
            return

        # Tenta registrar o usuário
        if self.banco_dados.registrar_cliente(nome, cpf, senha):
            self.navegador.ir_para("login_banco")
        else:
            self.msg_status.atualizar_texto("Erro ao registrar. CPF já existe ou é inválido.")        
        