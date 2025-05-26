from utilitarios.Aprincipal_widgets import Tela, Botao, Cores, TextoFormatado, CaixaTexto, Paginador, Painel, Fontes
from databases.cadastro_database import DadosUsuario
import os

def limpar_tela():
    """Limpa o terminal (útil para debug)."""
    if os.name == 'nt':
        os.system('cls')
    else:
        os.system('clear')

class TelaLoginCadastro(Tela):
    """
    Tela visual e intuitiva de Login e Cadastro de Usuário, usando Paginador para navegação entre abas.

    Parâmetros:
    -----------
    - navegador: objeto Navegador, responsável pela navegação entre telas.

    Como usar:
    ----------
    Basta registrar a classe no navegador:
        navegador.registrar_tela("cadastro", TelaLoginCadastro)

    O Navegador irá instanciar e rodar a tela automaticamente.
    """

    def __init__(self, navegador):
        super().__init__(
            largura=900,
            altura=650,
            titulo="Entrar ou Criar Conta",
            cor_fundo=Cores.preto(),
            navegador=navegador
        )

        self.navegador = navegador
        self.mensagem = {'texto': ''}

        # Título retrô com sombra dupla
        self.adicionar_componente(TextoFormatado(
            x=452, y=62, texto="LOGIN / CADASTRO",
            tamanho=40, cor_texto=Cores.cinza_escuro(),
            fonte_nome=Fontes.consolas(), centralizado=True
        ))
        self.adicionar_componente(TextoFormatado(
            x=450, y=60, texto="LOGIN / CADASTRO",
            tamanho=40, cor_texto=Cores.amarelo_ouro(),
            fonte_nome=Fontes.consolas(), centralizado=True
        ))

        if self.navegador.apelido_logado:
            self.adicionar_componente(
                Botao(
                    x=680, y=60, largura=180, altura=45, texto='Deslogar',
                    cor_fundo=Cores.azul(), cor_hover=Cores.azul_escuro(),
                    cor_texto=Cores.branco(),
                    funcao=self.Deslogar,
                    fonte=Fontes.consolas(), tamanho_fonte=22, raio_borda=12
                )
            )

            self.adicionar_componente(
                Botao(
                    x=680, y=110, largura=180, altura=45, texto='Excluir Conta',
                    cor_fundo=Cores.azul(), cor_hover=Cores.azul_escuro(),
                    cor_texto=Cores.branco(),
                    funcao=lambda: (DadosUsuario.deletar_usuario(self.navegador.apelido_logado), self.Deslogar()),
                    fonte=Fontes.consolas(), tamanho_fonte=22, raio_borda=12
                )
            )

        # Mensagem de feedback centralizada
        self.mensagem_texto = TextoFormatado(
            x=450, y=600, texto='', tamanho=24, cor_texto=Cores.amarelo_ouro(), fonte_nome=Fontes.consolas(), centralizado=True
        )

        # Paginador: cada página é uma "aba" (Login/Cadastro)
        self.paginador = Paginador(
            x=120, y=120, largura=660, altura=370, itens_por_pagina=1, texto_anterior="Login", texto_proxima="Cadastro",
            estilo_btn={"cor_fundo": Cores.laranja(), "cor_hover": Cores.laranja_escuro(), "cor_texto": Cores.branco(), "fonte": Fontes.consolas(), "tamanho_fonte": 22, "raio_borda": 10}
        )

        # -------- Página 1: Login --------
        self.apelido_login = CaixaTexto(
            x=320, y=210, largura=260, altura=48, placeholder='Digite seu apelido',
            cor_fundo=Cores.cinza_claro(), cor_texto=Cores.preto(), tamanho_fonte=24, fonte=Fontes.consolas()
        )
        self.senha_login = CaixaTexto(
            x=320, y=270, largura=260, altura=48, placeholder='Digite sua senha',
            cor_fundo=Cores.cinza_claro(), cor_texto=Cores.preto(), tamanho_fonte=24, fonte=Fontes.consolas()
        )
        botao_login = Botao(
            x=370, y=340, largura=160, altura=48, texto='Entrar',
            cor_fundo=Cores.verde(), cor_hover=Cores.verde_escuro(),
            cor_texto=Cores.branco(), funcao=self.fazer_login, fonte=Fontes.consolas(), tamanho_fonte=24, raio_borda=14
        )
        painel_login = Painel([
            TextoFormatado(x=450, y=150, texto='Acesse sua conta', tamanho=30, cor_texto=Cores.branco(), fonte_nome=Fontes.consolas(), centralizado=True),
            TextoFormatado(x=450, y=185, texto='Faça login para acessar o sistema', tamanho=18, cor_texto=Cores.cinza_claro(), fonte_nome=Fontes.consolas(), centralizado=True),
            self.apelido_login,
            self.senha_login,
            botao_login,
            TextoFormatado(x=450, y=400, texto='Não possui conta? Clique em "Cadastro" abaixo.', tamanho=16, cor_texto=Cores.cinza_claro(), fonte_nome=Fontes.consolas(), centralizado=True)
        ])

        # -------- Página 2: Cadastro --------
        self.nome_cad = CaixaTexto(
            x=320, y=150, largura=260, altura=45, placeholder='Nome completo',
            cor_fundo=Cores.cinza_claro(), cor_texto=Cores.preto(), tamanho_fonte=20, fonte=Fontes.consolas()
        )
        self.data_nasc_cad = CaixaTexto(
            x=320, y=200, largura=260, altura=45, placeholder='Data Nasc (YYYY-MM-DD)',
            cor_fundo=Cores.cinza_claro(), cor_texto=Cores.preto(), tamanho_fonte=20, fonte=Fontes.consolas()
        )
        self.apelido_cad = CaixaTexto(
            x=320, y=250, largura=260, altura=45, placeholder='Escolha um apelido',
            cor_fundo=Cores.cinza_claro(), cor_texto=Cores.preto(), tamanho_fonte=20, fonte=Fontes.consolas()
        )
        self.senha_cad = CaixaTexto(
            x=320, y=300, largura=260, altura=45, placeholder='Crie uma senha',
            cor_fundo=Cores.cinza_claro(), cor_texto=Cores.preto(), tamanho_fonte=20, fonte=Fontes.consolas()
        )
        botao_cad = Botao(
            x=370, y=360, largura=160, altura=48, texto='Cadastrar',
            cor_fundo=Cores.azul_royal(), cor_hover=Cores.azul_marinho(),
            cor_texto=Cores.branco(), funcao=self.fazer_cadastro, fonte=Fontes.consolas(), tamanho_fonte=24, raio_borda=14
        )
        painel_cadastro = Painel([
            TextoFormatado(x=450, y=110, texto='Crie sua conta', tamanho=30, cor_texto=Cores.branco(), fonte_nome=Fontes.consolas(), centralizado=True),
            TextoFormatado(x=450, y=140, texto='Preencha os dados abaixo para se cadastrar', tamanho=16, cor_texto=Cores.cinza_claro(), fonte_nome=Fontes.consolas(), centralizado=True),
            self.nome_cad,
            self.data_nasc_cad,
            self.apelido_cad,
            self.senha_cad,
            botao_cad,
            TextoFormatado(x=450, y=420, texto='Já possui conta? Clique em "Login" abaixo.', tamanho=16, cor_texto=Cores.cinza_claro(), fonte_nome=Fontes.consolas(), centralizado=True)
        ])

        # Adiciona as páginas ao paginador
        self.paginador.adicionar_componente(painel_login)
        self.paginador.adicionar_componente(painel_cadastro)
        self.adicionar_componente(self.paginador)

        # Mensagem de feedback centralizada
        self.adicionar_componente(self.mensagem_texto)

        # Botão para voltar ao menu (estilo retrô)
        self.adicionar_componente(
            Botao(
                x=40, y=590, largura=180, altura=45, texto='Voltar ao Menu',
                cor_fundo=Cores.azul(), cor_hover=Cores.azul_escuro(),
                cor_texto=Cores.branco(),
                funcao=lambda: self.navegador.ir_para("menu"),
                fonte=Fontes.consolas(), tamanho_fonte=22, raio_borda=12
            )
        )

        # Botão para sair do sistema (estilo retrô)
        self.adicionar_componente(
            Botao(
                x=680, y=590, largura=180, altura=45, texto='Sair',
                cor_fundo=Cores.vermelho(), cor_hover=Cores.vermelho_escuro(),
                cor_texto=Cores.branco(), funcao=self.sair, fonte=Fontes.consolas(), tamanho_fonte=22, raio_borda=12
            )
        )

        # Apelido logado no canto superior direito (se houver)
        if hasattr(self.navegador, "apelido_logado") and self.navegador.apelido_logado:
            self.adicionar_componente(
                TextoFormatado(
                    x=870, y=35, texto=self.navegador.apelido_logado,
                    tamanho=22, cor_texto=Cores.menta(), fonte_nome=Fontes.consolas(), centralizado=True
                )
            )

        # Troca o texto dos botões do paginador para "Login" e "Cadastro"
        self.paginador.botao_anterior.texto = "Login"
        self.paginador.botao_proxima.texto = "Cadastro"

    def fazer_login(self):
        """Valida o login do usuário e navega para o menu se correto."""
        apelido = self.apelido_login.texto
        senha = self.senha_login.texto
        if apelido and senha:
            usuarios = DadosUsuario.listar_usuarios()
            if usuarios:
                usuario = next((u for u in usuarios if u[3] == apelido), None)
                if usuario:
                    senha_correta = usuario[4]
                    if senha == senha_correta:
                        self.navegador.apelido_logado = apelido
                        self.navegador.id_logado = usuario[0]  # id global único
                        self.mensagem['texto'] = f"Bem-vindo, {apelido}!"
                        self.navegador.ir_para("menu")
                    else:
                        self.mensagem['texto'] = "Senha incorreta!"
                else:
                    self.mensagem['texto'] = "Usuário não encontrado!"
            else:
                self.mensagem['texto'] = "Usuário não encontrado!"
        else:
            self.mensagem['texto'] = "Preencha apelido e senha!"
        self.mensagem_texto.atualizar_texto(self.mensagem['texto'])

    def fazer_cadastro(self):
        """Realiza o cadastro do usuário no banco de dados."""
        nome = self.nome_cad.texto
        data_nasc = self.data_nasc_cad.texto
        apelido = self.apelido_cad.texto
        senha = self.senha_cad.texto
        if not (nome and data_nasc and apelido and senha):
            self.mensagem['texto'] = "Preencha todos os campos!"
            self.mensagem_texto.atualizar_texto(self.mensagem['texto'])
            return
        try:
            DadosUsuario.cadastrar_usuario(nome, data_nasc, apelido, senha)
            self.mensagem['texto'] = "Usuário cadastrado com sucesso!"
        except Exception as e:
            self.mensagem['texto'] = f"Erro: {e}"
        self.mensagem_texto.atualizar_texto(self.mensagem['texto'])
    
    def Deslogar(self):
        """Desloga o usuário atual, limpando os dados de login."""
        self.navegador.apelido_logado = None
        self.navegador.id_logado = None
        self.mensagem['texto'] = "Usuário deslogado com sucesso!"
        self.mensagem_texto.atualizar_texto(self.mensagem['texto'])
        self.navegador.ir_para("menu")

    # Não há necessidade de sobrescrever o método rodar(), pois já está implementado na classe Tela.
    # O Navegador irá instanciar e rodar esta tela automaticamente quando necessário.
