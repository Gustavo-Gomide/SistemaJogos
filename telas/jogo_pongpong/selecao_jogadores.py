from utilitarios.Aprincipal_widgets import Tela, Botao, Cores, TextoFormatado, CaixaTexto, Fontes, Painel
from databases.cadastro_database import DadosUsuario

class TelaSelecaoJogadores(Tela):
    """
    Tela para seleção/autenticação dos dois jogadores antes do jogo PongPong.
    Layout dividido meio a meio, cada lado com login ou visitante.
    """
    def __init__(self, navegador):
        super().__init__(
            largura=700, altura=500, titulo="Jogadores PongPong",
            cor_fundo=Cores.preto(), navegador=navegador
        )
        self.navegador = navegador

        # Estado de cada jogador
        self.j1_login = True  # True: login, False: visitante
        self.j2_login = True
        self.j1_ok = False
        self.j2_ok = False

        # Campos Jogador 1
        self.apelido1 = CaixaTexto(x=60, y=180, largura=220, altura=50, tamanho_fonte=30, placeholder="Apelido", cor_fundo=Cores.cinza_claro(), cor_texto=Cores.preto())
        self.senha1 = CaixaTexto(x=60, y=230, largura=220, altura=50, tamanho_fonte=30, placeholder="Senha", cor_fundo=Cores.cinza_claro(), cor_texto=Cores.preto())
        self.msg1 = TextoFormatado(x=170, y=280, texto="", tamanho=18, cor_texto=Cores.vermelho(), fonte_nome=Fontes.segoe_ui_emoji(), centralizado=True)

        # Campos Jogador 2
        self.apelido2 = CaixaTexto(x=420, y=180, largura=220, altura=50, tamanho_fonte=30, placeholder="Apelido", cor_fundo=Cores.cinza_claro(), cor_texto=Cores.preto())
        self.senha2 = CaixaTexto(x=420, y=230, largura=220, altura=50, tamanho_fonte=30, placeholder="Senha", cor_fundo=Cores.cinza_claro(), cor_texto=Cores.preto())
        self.msg2 = TextoFormatado(x=530, y=280, texto="", tamanho=18, cor_texto=Cores.vermelho(), fonte_nome=Fontes.segoe_ui_emoji(), centralizado=True)

        # Botões de aba para cada jogador
        self.btn_j1_login = Botao(
            x=60, y=130, largura=110, altura=36, texto="Login",
            cor_fundo=Cores.verde() if self.j1_login else Cores.cinza(),
            cor_hover=Cores.verde_escuro(), cor_texto=Cores.preto(),
            funcao=self.j1_aba_login, fonte=Fontes.segoe_ui_emoji(), tamanho_fonte=20, raio_borda=10
        )
        self.btn_j1_visit = Botao(
            x=170, y=130, largura=110, altura=36, texto="Visitante",
            cor_fundo=Cores.verde() if not self.j1_login else Cores.cinza(),
            cor_hover=Cores.verde_escuro(), cor_texto=Cores.preto(),
            funcao=self.j1_aba_visit, fonte=Fontes.segoe_ui_emoji(), tamanho_fonte=20, raio_borda=10
        )
        self.btn_j2_login = Botao(
            x=420, y=130, largura=110, altura=36, texto="Login",
            cor_fundo=Cores.azul() if self.j2_login else Cores.cinza(),
            cor_hover=Cores.azul_escuro(), cor_texto=Cores.branco(),
            funcao=self.j2_aba_login, fonte=Fontes.segoe_ui_emoji(), tamanho_fonte=20, raio_borda=10
        )
        self.btn_j2_visit = Botao(
            x=530, y=130, largura=110, altura=36, texto="Visitante",
            cor_fundo=Cores.azul() if not self.j2_login else Cores.cinza(),
            cor_hover=Cores.azul_escuro(), cor_texto=Cores.branco(),
            funcao=self.j2_aba_visit, fonte=Fontes.segoe_ui_emoji(), tamanho_fonte=20, raio_borda=10
        )

        self.atualizar_componentes()

    def atualizar_componentes(self):
        self.componentes = []

        # Botão Voltar no topo centralizado
        self.adicionar_componente(Botao(
            x=260, y=20, largura=180, altura=38, texto="⏪ Voltar ao Menu",
            cor_fundo=Cores.azul(), cor_hover=Cores.azul_escuro(), cor_texto=Cores.branco(),
            funcao=lambda: self.navegador.ir_para("menu pong-pong"),
            fonte=Fontes.segoe_ui_emoji(), tamanho_fonte=20, raio_borda=12
        ))

        # --- JOGADOR 1 ---
        if self.navegador.id_logado and not self.j1_ok and not getattr(self, "j1_trocando", False):
            # Pergunta: continuar como logado?
            self.adicionar_componente(TextoFormatado(
                x=170, y=120, texto=f"Jogador 1: {self.navegador.apelido_logado}",
                tamanho=24, cor_texto=Cores.verde(), fonte_nome=Fontes.segoe_ui_emoji(), centralizado=True
            ))
            self.adicionar_componente(Botao(
                x=60, y=180, largura=100, altura=40, texto="Sim",
                cor_fundo=Cores.verde(), cor_hover=Cores.verde_escuro(), cor_texto=Cores.preto(),
                funcao=lambda: self.set_j1_ok(), fonte=Fontes.segoe_ui_emoji(), tamanho_fonte=20, raio_borda=10
            ))
            self.adicionar_componente(Botao(
                x=180, y=180, largura=100, altura=40, texto="Não",
                cor_fundo=Cores.cinza(), cor_hover=Cores.cinza_escuro(), cor_texto=Cores.preto(),
                funcao=lambda: self.trocar_j1(), fonte=Fontes.segoe_ui_emoji(), tamanho_fonte=20, raio_borda=10
            ))
        elif not self.j1_ok:
            # Paginação login/visitante para J1
            if getattr(self, "j1_login", True):
                self.adicionar_componente(self.apelido1)
                self.adicionar_componente(self.senha1)
                self.adicionar_componente(Botao(
                    x=60, y=320, largura=220, altura=40, texto="Entrar",
                    cor_fundo=Cores.verde(), cor_hover=Cores.verde_escuro(), cor_texto=Cores.preto(),
                    funcao=self.login_jogador1, fonte=Fontes.segoe_ui_emoji(), tamanho_fonte=20, raio_borda=10
                ))
            else:
                self.adicionar_componente(Botao(
                    x=60, y=200, largura=230, altura=40, texto="Continuar como Visitante",
                    cor_fundo=Cores.cinza(), cor_hover=Cores.cinza_escuro(), cor_texto=Cores.preto(),
                    funcao=self.visitante1, fonte=Fontes.segoe_ui_emoji(), tamanho_fonte=20, raio_borda=10
                ))
            # Abas
            self.adicionar_componente(self.btn_j1_login)
            self.adicionar_componente(self.btn_j1_visit)
            self.adicionar_componente(self.msg1)
        else:
            self.adicionar_componente(TextoFormatado(
                x=170, y=200, texto=f"{self.navegador.apelido_logado or 'Visitante 1'}",
                tamanho=26, cor_texto=Cores.verde(), fonte_nome=Fontes.segoe_ui_emoji(), centralizado=True
            ))

        # --- JOGADOR 2 ---
        if self.navegador.jgd_2_id and not self.j2_ok and not getattr(self, "j2_trocando", False):
            self.adicionar_componente(TextoFormatado(
                x=530, y=120, texto=f"Jogador 2: {self.navegador.jgd_2}",
                tamanho=24, cor_texto=Cores.azul(), fonte_nome=Fontes.segoe_ui_emoji(), centralizado=True
            ))
            self.adicionar_componente(Botao(
                x=420, y=180, largura=100, altura=40, texto="Sim",
                cor_fundo=Cores.azul(), cor_hover=Cores.azul_escuro(), cor_texto=Cores.branco(),
                funcao=lambda: self.set_j2_ok(), fonte=Fontes.segoe_ui_emoji(), tamanho_fonte=20, raio_borda=10
            ))
            self.adicionar_componente(Botao(
                x=540, y=180, largura=100, altura=40, texto="Não",
                cor_fundo=Cores.cinza(), cor_hover=Cores.cinza_escuro(), cor_texto=Cores.preto(),
                funcao=lambda: self.trocar_j2(), fonte=Fontes.segoe_ui_emoji(), tamanho_fonte=20, raio_borda=10
            ))
        elif not self.j2_ok:
            # Paginação login/visitante para J2
            if getattr(self, "j2_login", True):
                self.adicionar_componente(self.apelido2)
                self.adicionar_componente(self.senha2)
                self.adicionar_componente(Botao(
                    x=420, y=320, largura=220, altura=40, texto="Entrar",
                    cor_fundo=Cores.azul(), cor_hover=Cores.azul_escuro(), cor_texto=Cores.branco(),
                    funcao=self.login_jogador2, fonte=Fontes.segoe_ui_emoji(), tamanho_fonte=20, raio_borda=10
                ))
            else:
                self.adicionar_componente(Botao(
                    x=420, y=200, largura=230, altura=40, texto="Continuar como Visitante",
                    cor_fundo=Cores.cinza(), cor_hover=Cores.cinza_escuro(), cor_texto=Cores.preto(),
                    funcao=self.visitante2, fonte=Fontes.segoe_ui_emoji(), tamanho_fonte=20, raio_borda=10
                ))
            # Abas
            self.adicionar_componente(self.btn_j2_login)
            self.adicionar_componente(self.btn_j2_visit)
            self.adicionar_componente(self.msg2)
        else:
            self.adicionar_componente(TextoFormatado(
                x=530, y=200, texto=f"{self.navegador.jgd_2 or 'Visitante 2'}",
                tamanho=26, cor_texto=Cores.azul(), fonte_nome=Fontes.segoe_ui_emoji(), centralizado=True
            ))

        # Botão iniciar só se ambos ok
        self.adicionar_componente(Botao(
            x=250, y=420, largura=200, altura=50, texto="Iniciar Jogo",
            cor_fundo=Cores.amarelo_ouro() if self.j1_ok and self.j2_ok else Cores.cinza(),
            cor_hover=Cores.ocre(), cor_texto=Cores.preto(),
            funcao=self.iniciar_jogo, fonte=Fontes.segoe_ui_emoji(), tamanho_fonte=24, raio_borda=12
        ))

    # Abas
    def j1_aba_login(self):
        self.j1_login = True
        self.atualizar_componentes()
    def j1_aba_visit(self):
        self.j1_login = False
        self.atualizar_componentes()
    def j2_aba_login(self):
        self.j2_login = True
        self.atualizar_componentes()
    def j2_aba_visit(self):
        self.j2_login = False
        self.atualizar_componentes()

    # Login/visitante Jogador 1
    def login_jogador1(self):
        apelido = self.apelido1.texto
        senha = self.senha1.texto
        usuario = next((u for u in DadosUsuario.listar_usuarios() if u[3] == apelido), None)
        if usuario and usuario[4] == senha:
            self.navegador.apelido_logado = apelido
            self.navegador.id_logado = usuario[0]
            self.msg1.atualizar_texto("OK!")
            self.j1_ok = True
        else:
            self.msg1.atualizar_texto("Login inválido!")
        self.atualizar_componentes()

    def visitante1(self):
        self.navegador.apelido_logado = "Visitante 1"
        self.navegador.id_logado = None
        self.msg1.atualizar_texto("Visitante")
        self.j1_ok = True
        self.atualizar_componentes()

    # Login/visitante Jogador 2
    def login_jogador2(self):
        apelido = self.apelido2.texto
        senha = self.senha2.texto
        usuario = next((u for u in DadosUsuario.listar_usuarios() if u[3] == apelido), None)
        if usuario and usuario[4] == senha:
            self.navegador.jgd_2 = apelido
            self.navegador.jgd_2_id = usuario[0]
            self.msg2.atualizar_texto("OK!")
            self.j2_ok = True
        else:
            self.msg2.atualizar_texto("Login inválido!")
        self.atualizar_componentes()

    def visitante2(self):
        self.navegador.jgd_2 = "Visitante 2"
        self.navegador.jgd_2_id = None
        self.msg2.atualizar_texto("Visitante")
        self.j2_ok = True
        self.atualizar_componentes()

    def iniciar_jogo(self):
        if self.j1_ok and self.j2_ok:
            self.navegador.ir_para("jogo pong-pong")

    def set_j1_ok(self):
        self.j1_ok = True
        self.atualizar_componentes()

    def set_j2_ok(self):
        self.j2_ok = True
        self.atualizar_componentes()

    # Métodos auxiliares para trocar usuário
    def trocar_j1(self):
        self.j1_trocando = True
        self.navegador.id_logado = None
        self.navegador.apelido_logado = None
        self.j1_ok = False
        self.atualizar_componentes()

    def trocar_j2(self):
        self.j2_trocando = True
        self.navegador.jgd_2_id = None
        self.navegador.jgd_2 = None
        self.j2_ok = False
        self.atualizar_componentes()