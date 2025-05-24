import pygame
from utilitarios.Aprincipal_widgets import Tela, Botao, Cores, TextoFormatado, CaixaTexto, Fontes
from databases.cadastro_database import DadosUsuario
from utilitarios.musicas import Musicas

def largura_botao(texto, tamanho_fonte, fonte_nome=Fontes.consolas(), margem=40):
    fonte = pygame.font.SysFont(fonte_nome, tamanho_fonte, bold=True)
    return fonte.size(texto)[0] + margem

class TelaSelecaoJogadoresVelha(Tela):
    """
    Tela para seleção/autenticação dos dois jogadores antes do Jogo da Velha.
    """
    def __init__(self, navegador):
        super().__init__(
            largura=800, altura=600, titulo="Jogadores Jogo da Velha",
            cor_fundo=Cores.preto(), navegador=navegador
        )
        self.navegador = navegador

        # Estado de cada jogador
        self.j1_login = True  # True: login, False: visitante
        self.j2_login = True
        self.j1_ok = False
        self.j2_ok = False

        # Campos Jogador 1
        self.apelido1 = CaixaTexto(
            x=60, y=180, largura=220, altura=40,
            placeholder="Apelido", cor_fundo=Cores.cinza_claro(), cor_texto=Cores.preto(),
            fonte=Fontes.consolas(), tamanho_fonte=22
        )
        self.senha1 = CaixaTexto(
            x=60, y=230, largura=220, altura=40,
            placeholder="Senha", cor_fundo=Cores.cinza_claro(), cor_texto=Cores.preto(),
            fonte=Fontes.consolas(), tamanho_fonte=22
        )
        self.msg1 = TextoFormatado(x=170, y=280, texto="", tamanho=18, cor_texto=Cores.vermelho(), fonte_nome=Fontes.consolas(), centralizado=True)

        # Campos Jogador 2
        self.apelido2 = CaixaTexto(
            x=320, y=180, largura=220, altura=40,
            placeholder="Apelido", cor_fundo=Cores.cinza_claro(), cor_texto=Cores.preto(),
            fonte=Fontes.consolas(), tamanho_fonte=22
        )
        self.senha2 = CaixaTexto(
            x=320, y=230, largura=220, altura=40,
            placeholder="Senha", cor_fundo=Cores.cinza_claro(), cor_texto=Cores.preto(),
            fonte=Fontes.consolas(), tamanho_fonte=22
        )
        self.msg2 = TextoFormatado(x=430, y=280, texto="", tamanho=18, cor_texto=Cores.vermelho(), fonte_nome=Fontes.consolas(), centralizado=True)

        self.atualizar_componentes()

    def atualizar_componentes(self):
        self.componentes = []

        # Título centralizado
        self.adicionar_componente(TextoFormatado(
            x=self.largura//2, y=40, texto="Seleção de Jogadores",
            tamanho=36, cor_texto=Cores.amarelo(),
            fonte_nome=Fontes.consolas(), centralizado=True
        ))

        # Botão Voltar centralizado embaixo
        texto_voltar = "Voltar ao Menu"
        tam_fonte_voltar = 24
        larg_voltar = largura_botao(texto_voltar, tam_fonte_voltar)
        self.adicionar_componente(Botao(
            x=(self.largura - larg_voltar)//2, y=self.altura-70, largura=larg_voltar, altura=50, texto=texto_voltar,
            cor_fundo=Cores.vermelho_vinho(), cor_hover=Cores.vermelho_escuro(), cor_texto=Cores.branco(),
            funcao=lambda: (Musicas.tocar_efeito('clique'), self.navegador.ir_para("menu jogo-da-velha")),
            fonte=Fontes.consolas(), tamanho_fonte=tam_fonte_voltar, raio_borda=12
        ))

        # --- JOGADOR 1 (esquerda) ---
        area1_x = 0
        area1_w = self.largura // 2

        # Abas Jogador 1 (sempre exibidas)
        abas_j1 = [("Login", self.j1_login, self.j1_aba_login), ("Visitante", not self.j1_login, self.j1_aba_visit)]
        total_larg_abas = sum(largura_botao(texto, 20) for texto, _, _ in abas_j1) + 20  # 20px de espaço entre
        x_inicio_abas = area1_x + area1_w//2 - total_larg_abas//2
        x_atual = x_inicio_abas
        for texto, ativo, func in abas_j1:
            larg = largura_botao(texto, 20)
            self.adicionar_componente(Botao(
                x=x_atual, y=130, largura=larg, altura=36, texto=texto,
                cor_fundo=Cores.verde() if ativo else Cores.cinza(),
                cor_hover=Cores.verde_escuro(), cor_texto=Cores.preto(),
                funcao=lambda f=func: (Musicas.tocar_efeito('clique'), f()),
                fonte=Fontes.consolas(), tamanho_fonte=20, raio_borda=10
            ))
            x_atual += larg + 20

        if self.navegador.id_logado and not self.j1_ok and not getattr(self, "j1_trocando", False):
            self.adicionar_componente(TextoFormatado(
                x=area1_x + area1_w//2, y=180, texto=f"Jogador 1: {self.navegador.apelido_logado}",
                tamanho=24, cor_texto=Cores.verde(), fonte_nome=Fontes.consolas(), centralizado=True
            ))
            for i, (texto, cor, func) in enumerate([
                ("Sim", Cores.verde(), lambda: self.set_j1_ok()),
                ("Não", Cores.cinza(), lambda: self.trocar_j1())
            ]):
                tam_fonte = 20
                larg = largura_botao(texto, tam_fonte)
                self.adicionar_componente(Botao(
                    x=area1_x + area1_w//2 - larg - 10 if i == 0 else area1_x + area1_w//2 + 10,
                    y=230, largura=larg, altura=40, texto=texto,
                    cor_fundo=cor, cor_hover=Cores.verde_escuro() if texto=="Sim" else Cores.cinza_escuro(),
                    cor_texto=Cores.preto(),
                    funcao=lambda f=func: (Musicas.tocar_efeito('clique'), f()),
                    fonte=Fontes.consolas(), tamanho_fonte=tam_fonte, raio_borda=10
                ))
        elif not self.j1_ok:
            if getattr(self, "j1_login", True):
                self.apelido1.rect.x = area1_x + area1_w//2 - self.apelido1.rect.width//2
                self.senha1.rect.x = area1_x + area1_w//2 - self.senha1.rect.width//2
                self.adicionar_componente(self.apelido1)
                self.adicionar_componente(self.senha1)
                texto_entrar = "Entrar"
                tam_fonte = 20
                larg = largura_botao(texto_entrar, tam_fonte)
                self.adicionar_componente(Botao(
                    x=area1_x + area1_w//2 - larg//2, y=320, largura=larg, altura=40, texto=texto_entrar,
                    cor_fundo=Cores.verde(), cor_hover=Cores.verde_escuro(), cor_texto=Cores.preto(),
                    funcao=lambda: (Musicas.tocar_efeito('clique'), self.login_jogador1()),
                    fonte=Fontes.consolas(), tamanho_fonte=tam_fonte, raio_borda=10
                ))
            else:
                texto_visit = "Continuar como Visitante"
                tam_fonte = 20
                larg = largura_botao(texto_visit, tam_fonte)
                self.adicionar_componente(Botao(
                    x=area1_x + area1_w//2 - larg//2, y=220, largura=larg, altura=40, texto=texto_visit,
                    cor_fundo=Cores.cinza(), cor_hover=Cores.cinza_escuro(), cor_texto=Cores.preto(),
                    funcao=lambda: (Musicas.tocar_efeito('clique'), self.visitante1()),
                    fonte=Fontes.consolas(), tamanho_fonte=tam_fonte, raio_borda=10
                ))
            self.msg1.x = area1_x + area1_w//2
            self.adicionar_componente(self.msg1)
        else:
            self.adicionar_componente(TextoFormatado(
                x=area1_x + area1_w//2, y=200, texto=f"{self.navegador.apelido_logado or 'Visitante 1'}",
                tamanho=26, cor_texto=Cores.verde(), fonte_nome=Fontes.consolas(), centralizado=True
            ))

        # --- JOGADOR 2 (direita) ---
        area2_x = self.largura // 2
        area2_w = self.largura // 2

        # Abas Jogador 2 (sempre exibidas)
        abas_j2 = [("Login", self.j2_login, self.j2_aba_login), ("Visitante", not self.j2_login, self.j2_aba_visit)]
        total_larg_abas2 = sum(largura_botao(texto, 20) for texto, _, _ in abas_j2) + 20
        x_inicio_abas2 = area2_x + area2_w//2 - total_larg_abas2//2
        x_atual2 = x_inicio_abas2
        for texto, ativo, func in abas_j2:
            larg = largura_botao(texto, 20)
            self.adicionar_componente(Botao(
                x=x_atual2, y=130, largura=larg, altura=36, texto=texto,
                cor_fundo=Cores.azul() if ativo else Cores.cinza(),
                cor_hover=Cores.azul_escuro(), cor_texto=Cores.branco() if ativo else Cores.preto(),
                funcao=lambda f=func: (Musicas.tocar_efeito('clique'), f()),
                fonte=Fontes.consolas(), tamanho_fonte=20, raio_borda=10
            ))
            x_atual2 += larg + 20

        if self.navegador.jgd_2_id and not self.j2_ok and not getattr(self, "j2_trocando", False):
            self.adicionar_componente(TextoFormatado(
                x=area2_x + area2_w//2, y=180, texto=f"Jogador 2: {self.navegador.jgd_2}",
                tamanho=24, cor_texto=Cores.azul(), fonte_nome=Fontes.consolas(), centralizado=True
            ))
            for i, (texto, cor, func) in enumerate([
                ("Sim", Cores.azul(), lambda: self.set_j2_ok()),
                ("Não", Cores.cinza(), lambda: self.trocar_j2())
            ]):
                tam_fonte = 20
                larg = largura_botao(texto, tam_fonte)
                self.adicionar_componente(Botao(
                    x=area2_x + area2_w//2 - larg - 10 if i == 0 else area2_x + area2_w//2 + 10,
                    y=230, largura=larg, altura=40, texto=texto,
                    cor_fundo=cor, cor_hover=Cores.azul_escuro() if texto=="Sim" else Cores.cinza_escuro(),
                    cor_texto=Cores.branco() if texto=="Sim" else Cores.preto(),
                    funcao=lambda f=func: (Musicas.tocar_efeito('clique'), f()),
                    fonte=Fontes.consolas(), tamanho_fonte=tam_fonte, raio_borda=10
                ))
        elif not self.j2_ok:
            if getattr(self, "j2_login", True):
                self.apelido2.rect.x = area2_x + area2_w//2 - self.apelido2.rect.width//2
                self.senha2.rect.x = area2_x + area2_w//2 - self.senha2.rect.width//2
                self.adicionar_componente(self.apelido2)
                self.adicionar_componente(self.senha2)
                texto_entrar = "Entrar"
                tam_fonte = 20
                larg = largura_botao(texto_entrar, tam_fonte)
                self.adicionar_componente(Botao(
                    x=area2_x + area2_w//2 - larg//2, y=320, largura=larg, altura=40, texto=texto_entrar,
                    cor_fundo=Cores.azul(), cor_hover=Cores.azul_escuro(), cor_texto=Cores.branco(),
                    funcao=lambda: (Musicas.tocar_efeito('clique'), self.login_jogador2()),
                    fonte=Fontes.consolas(), tamanho_fonte=tam_fonte, raio_borda=10
                ))
            else:
                texto_visit = "Continuar como Visitante"
                tam_fonte = 20
                larg = largura_botao(texto_visit, tam_fonte)
                self.adicionar_componente(Botao(
                    x=area2_x + area2_w//2 - larg//2, y=220, largura=larg, altura=40, texto=texto_visit,
                    cor_fundo=Cores.cinza(), cor_hover=Cores.cinza_escuro(), cor_texto=Cores.preto(),
                    funcao=lambda: (Musicas.tocar_efeito('clique'), self.visitante2()),
                    fonte=Fontes.consolas(), tamanho_fonte=tam_fonte, raio_borda=10
                ))
            self.msg2.x = area2_x + area2_w//2
            self.adicionar_componente(self.msg2)
        else:
            self.adicionar_componente(TextoFormatado(
                x=area2_x + area2_w//2, y=200, texto=f"{self.navegador.jgd_2 or 'Visitante 2'}",
                tamanho=26, cor_texto=Cores.azul(), fonte_nome=Fontes.consolas(), centralizado=True
            ))

        # Botão iniciar só se ambos ok (centralizado)
        texto_iniciar = "Iniciar Jogo"
        tam_fonte_iniciar = 24
        larg_iniciar = largura_botao(texto_iniciar, tam_fonte_iniciar)
        self.adicionar_componente(Botao(
            x=(self.largura - larg_iniciar)//2, y=self.altura-130, largura=larg_iniciar, altura=50, texto=texto_iniciar,
            cor_fundo=Cores.amarelo_ouro() if self.j1_ok and self.j2_ok else Cores.cinza(),
            cor_hover=Cores.ocre(), cor_texto=Cores.preto(),
            funcao=lambda: (Musicas.tocar_efeito('clique'), self.iniciar_jogo()),
            fonte=Fontes.consolas(), tamanho_fonte=tam_fonte_iniciar, raio_borda=12
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
            self.navegador.ir_para("jogo da velha")

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