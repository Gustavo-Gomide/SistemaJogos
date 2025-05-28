import pygame
from utilitarios.Aprincipal_widgets import Tela, Botao, CaixaTexto, TextoFormatado, Cores, Fontes
from utilitarios.musicas import Musicas, Fundos


class MenuJogoDaVelhaTela(Tela):
    def __init__(self, navegador):
        super().__init__(
            largura=500,
            altura=600,
            titulo="Menu Jogo da Velha",
            cor_fundo=Cores.preto(),
            navegador=navegador,
        )
        self.componentes = []
        self._montar()

    def _montar(self):
        Musicas.salvar_musica_anterior()
        Musicas.tocar_fundo(Fundos.musica_fundo())  # Música de fundo
        self.componentes.clear()
        self.adicionar_componente(TextoFormatado(
            x=250, y=80, texto="JOGO DA VELHA",
            tamanho=48, cor_texto=Cores.amarelo(),
            fonte_nome=Fontes.consolas(), centralizado=True
        ))
        btn_jogar = Botao(
            x=100, y=200, largura=300, altura=70,
            texto="Jogar", cor_fundo=Cores.amarelo(), cor_hover=Cores.laranja(),
            cor_texto=Cores.preto(), fonte=Fontes.consolas(), tamanho_fonte=36,
            funcao=lambda: (Musicas.tocar_efeito('clique'), self.navegador.ir_para("selecao jogadores velha"))
        )
        self.adicionar_componente(btn_jogar)
        btn_historico = Botao(
            x=100, y=290, largura=300, altura=60,
            texto="Histórico", cor_fundo=Cores.azul_royal(), cor_hover=Cores.azul_marinho(),
            cor_texto=Cores.branco(), fonte=Fontes.consolas(), tamanho_fonte=28,
            funcao=lambda: (Musicas.tocar_efeito('clique'), self.navegador.ir_para("historico velha"))
        )
        self.adicionar_componente(btn_historico)
        btn_voltar = Botao(
            x=100, y=370, largura=300, altura=60,
            texto="Voltar ao Menu", cor_fundo=Cores.vermelho_vinho(), cor_hover=Cores.vermelho_escuro(),
            cor_texto=Cores.branco(), fonte=Fontes.consolas(), tamanho_fonte=28,
            funcao=lambda: (Musicas.tocar_efeito('clique'), self.voltar_para_menu())
        )
        self.adicionar_componente(btn_voltar)

    def renderizar(self):
        self.tela.fill(Cores.preto())
        for c in self.componentes:
            c.desenhar(self.tela)
        pygame.display.flip()


class JogoDaVelhaTela(Tela):
    def __init__(self, navegador, banco=None):
        super().__init__(
            largura=500,
            altura=650,
            titulo="Jogo da Velha",
            cor_fundo=Cores.preto(),
            navegador=navegador
        )
        self.banco = banco
        self.jogador_x = ""
        self.jogador_o = ""
        self.tabuleiro = ['' for _ in range(9)]
        self.jogador_atual = 'X'
        self.resultado = None
        self.componentes = []
        self.estado = "inicio"
        self._montar_tela_inicial()

    def _montar_tela_inicial(self):
        self.componentes.clear()
        self.estado = "inicio"
        # Pega os apelidos do navegador, se existirem
        apelido_x = getattr(self.navegador, "apelido_logado", "") or ""
        apelido_o = getattr(self.navegador, "jgd_2", "") or ""
        self.caixa_x = CaixaTexto(
            x=150, y=180, largura=200, altura=40,
            placeholder="Jogador X", cor_fundo=Cores.cinza_escuro(), cor_texto=Cores.amarelo(),
            fonte=Fontes.consolas(), tamanho_fonte=28,
        )
        self.caixa_x.texto = apelido_x
        self.caixa_o = CaixaTexto(
            x=150, y=240, largura=200, altura=40,
            placeholder="Jogador O", cor_fundo=Cores.cinza_escuro(), cor_texto=Cores.ciano(),
            fonte=Fontes.consolas(), tamanho_fonte=28,
        )
        self.caixa_o.texto = apelido_o
        self.adicionar_componente(TextoFormatado(
            x=250, y=80, texto="JOGO DA VELHA",
            tamanho=44, cor_texto=Cores.amarelo(),
            fonte_nome=Fontes.consolas(), centralizado=True
        ))
        self.adicionar_componente(self.caixa_x)
        self.adicionar_componente(self.caixa_o)
        self.btn_iniciar = Botao(
            x=100, y=320, largura=300, altura=70,
            texto="Iniciar", cor_fundo=Cores.amarelo(), cor_hover=Cores.laranja(),
            cor_texto=Cores.preto(), fonte=Fontes.consolas(), tamanho_fonte=36,
            funcao=lambda: (Musicas.tocar_efeito('clique'), self._iniciar_jogo())
        )
        self.adicionar_componente(self.btn_iniciar)
        self.btn_voltar = Botao(
            x=100, y=400, largura=300, altura=70,
            texto="Voltar ao Menu", cor_fundo=Cores.vermelho_vinho(), cor_hover=Cores.vermelho_escuro(),
            cor_texto=Cores.branco(), fonte=Fontes.consolas(), tamanho_fonte=36,
            funcao=lambda: (Musicas.tocar_efeito('clique'), self.navegador.ir_para("menu jogo-da-velha"))
        )
        self.adicionar_componente(self.btn_voltar)

    def _iniciar_jogo(self):
        self.jogador_x = self.caixa_x.texto.strip() or "Jogador X"
        self.jogador_o = self.caixa_o.texto.strip() or "Jogador O"
        self.tabuleiro = ['' for _ in range(9)]
        self.jogador_atual = 'X'
        self.resultado = None
        self.estado = "jogo"
        self.componentes.clear()

    def _finalizar_jogo(self, vencedor):
        self.resultado = vencedor
        if self.banco:
            self.banco.salvar_resultado(self.jogador_x, self.jogador_o, vencedor)
            self.banco.salvar_partida_no_historico(self.jogador_x, self.jogador_o, vencedor, self.tabuleiro)
        self.estado = "fim"
        self.componentes.clear()
        # Efeito sonoro de vitória ou empate
        if vencedor == "Empate":
            Musicas.tocar_efeito('empate')
        else:
            Musicas.tocar_efeito('vitoria')
        btn_voltar = Botao(
            x=100, y=400, largura=300, altura=60,
            texto="Voltar ao Menu", cor_fundo=Cores.vermelho_vinho(), cor_hover=Cores.vermelho_escuro(),
            cor_texto=Cores.branco(), fonte=Fontes.consolas(), tamanho_fonte=22,
            funcao=lambda: (Musicas.tocar_efeito('clique'),self.navegador.ir_para("menu jogo-da-velha"))
        )
        self.adicionar_componente(btn_voltar)

    def _verificar_vencedor(self):
        linhas = [(0,1,2),(3,4,5),(6,7,8),(0,3,6),(1,4,7),(2,5,8),(0,4,8),(2,4,6)]
        for a,b,c_ in linhas:
            if self.tabuleiro[a] and self.tabuleiro[a] == self.tabuleiro[b] == self.tabuleiro[c_]:
                return self.tabuleiro[a]
        if '' not in self.tabuleiro:
            return "Empate"
        return None

    def processar_eventos(self):
        if self.estado == "inicio" or self.estado == "fim":
            super().processar_eventos()
        elif self.estado == "jogo":
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                elif evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
                    # Botão Voltar ao Menu na tela de fim de jogo
                    if self.estado == "fim":
                        for c in self.componentes:
                            if isinstance(c, Botao) and hasattr(c, "verificar_clique") and c.verificar_clique(evento.pos):
                                Musicas.tocar_efeito('clique')
                                c.funcao()
                                return
                    # Clique no tabuleiro
                    x, y = evento.pos
                    tab_x, tab_y, size = 100, 120, 300
                    if tab_x <= x < tab_x+size and tab_y <= y < tab_y+size:
                        col = (x - tab_x) // 100
                        lin = (y - tab_y) // 100
                        idx = lin * 3 + col
                        if self.tabuleiro[idx] == '' and not self.resultado:
                            Musicas.tocar_efeito('clique')  # <-- Adiciona som de clique na jogada
                            self.tabuleiro[idx] = self.jogador_atual
                            vencedor = self._verificar_vencedor()
                            if vencedor:
                                self._finalizar_jogo(vencedor)
                            else:
                                self.jogador_atual = 'O' if self.jogador_atual == 'X' else 'X'
                elif evento.type == pygame.KEYDOWN and evento.key == pygame.K_ESCAPE:
                    self._montar_tela_inicial()
                    self.estado = "inicio"

    def renderizar(self):
        self.tela.fill(Cores.preto())
        if self.estado == "inicio":
            for c in self.componentes:
                c.desenhar(self.tela)
        elif self.estado == "jogo":
            # Desenha tabuleiro retrô
            tab_x, tab_y, size = 100, 120, 300
            pygame.draw.rect(self.tela, Cores.amarelo(), (tab_x-8, tab_y-8, size+16, size+16), border_radius=12)
            pygame.draw.rect(self.tela, Cores.preto(), (tab_x, tab_y, size, size))
            for i in range(1, 3):
                pygame.draw.line(self.tela, Cores.branco(), (tab_x + i*100, tab_y), (tab_x + i*100, tab_y+size), 8)
                pygame.draw.line(self.tela, Cores.branco(), (tab_x, tab_y + i*100), (tab_x+size, tab_y + i*100), 8)
            # Peças grandes e coloridas
            for i, val in enumerate(self.tabuleiro):
                if val:
                    x = tab_x + (i % 3) * 100 + 50
                    y = tab_y + (i // 3) * 100 + 50
                    cor = Cores.vermelho() if val == 'X' else Cores.ciano()
                    fonte = pygame.font.SysFont(Fontes.consolas(), 72, bold=True)
                    texto = fonte.render(val, True, cor)
                    rect = texto.get_rect(center=(x, y))
                    self.tela.blit(texto, rect)
            # Moldura do tabuleiro
            pygame.draw.rect(self.tela, Cores.amarelo(), (tab_x-8, tab_y-8, size+16, size+16), 8, border_radius=12)
            # Info de vez
            info = f"Vez de: {self.jogador_x if self.jogador_atual == 'X' else self.jogador_o}"
            if self.resultado:
                if self.resultado == "Empate":
                    info = "EMPATE!"
                else:
                    info = f"{self.jogador_x if self.resultado == 'X' else self.jogador_o} VENCEU!"
            fonte = pygame.font.SysFont(Fontes.consolas(), 30, bold=True)
            texto = fonte.render(info, True, Cores.amarelo())
            self.tela.blit(texto, (self.largura//2 - texto.get_width()//2, 450))
        elif self.estado == "fim":
            # Mensagem de resultado retrô
            msg = "EMPATE!" if self.resultado == "Empate" else f"{self.jogador_x if self.resultado == 'X' else self.jogador_o} VENCEU!"
            fonte = pygame.font.SysFont(Fontes.consolas(), 40, bold=True)
            texto = fonte.render(msg, True, Cores.amarelo())
            self.tela.blit(texto, (self.largura//2 - texto.get_width()//2, 250))
            for c in self.componentes:
                c.desenhar(self.tela)
        pygame.display.flip()


class Popup:
    def __init__(self, tela, mensagem, largura=520, altura=90, cor_fundo=None, cor_borda=None, cor_texto=None, fonte=None, tempo=1800):
        self.tela = tela
        self.mensagem = mensagem
        self.largura = largura
        self.altura = altura
        self.cor_fundo = cor_fundo or Cores.preto()
        self.cor_borda = cor_borda or Cores.amarelo()
        self.cor_texto = cor_texto or Cores.amarelo()
        self.fonte = fonte or pygame.font.SysFont(Fontes.consolas(), 24, bold=True)
        self.tempo = tempo  # em milissegundos

    def mostrar(self, renderizar_fundo=None):
        x = (self.tela.get_width() - self.largura) // 2
        y = (self.tela.get_height() - self.altura) // 2
        popup_surface = pygame.Surface((self.largura, self.altura))
        popup_surface.fill(self.cor_fundo)
        pygame.draw.rect(popup_surface, self.cor_borda, (0, 0, self.largura, self.altura), 4)
        texto = self.fonte.render(self.mensagem, True, self.cor_texto)
        popup_surface.blit(
            texto,
            ((self.largura - texto.get_width()) // 2, (self.altura - texto.get_height()) // 2)
        )
        if renderizar_fundo:
            renderizar_fundo()
        self.tela.blit(popup_surface, (x, y))
        pygame.display.flip()
        pygame.time.delay(self.tempo)


class HistoricoVelhaTela(Tela):
    def __init__(self, navegador, banco=None):
        super().__init__(
            largura=800,
            altura=600,
            titulo="Histórico Jogo da Velha",
            cor_fundo=Cores.preto(),
            navegador=navegador
        )
        self.banco = banco
        self.componentes = []
        self._montar()
        self.navegador = navegador

    def _montar(self):
        self.componentes.clear()
        self.adicionar_componente(TextoFormatado(
            x=300, y=30, texto="HISTÓRICO",
            tamanho=36, cor_texto=Cores.amarelo(),
            fonte_nome=Fontes.consolas(), centralizado=True
        ))
        btn_apagar = Botao(
            x=250, y=450, largura=300, altura=60,
            texto="Apagar Histórico", cor_fundo=Cores.vermelho_escuro(), cor_hover=Cores.vermelho_vinho(),
            cor_texto=Cores.branco(), fonte=Fontes.consolas(), tamanho_fonte=28,
            funcao=lambda: (Musicas.tocar_efeito('clique'), self._apagar_historico())
        )
        self.adicionar_componente(btn_apagar)
        btn_voltar = Botao(
            x=250, y=520, largura=300, altura=60,
            texto="Voltar ao Menu", cor_fundo=Cores.vermelho_vinho(), cor_hover=Cores.vermelho_escuro(),
            cor_texto=Cores.branco(), fonte=Fontes.consolas(), tamanho_fonte=28,
            funcao=lambda: (Musicas.tocar_efeito('clique'), self.navegador.ir_para("menu jogo-da-velha"))
        )
        self.adicionar_componente(btn_voltar)

    def _apagar_historico(self):
        if self.banco:
            if not self.navegador.id_logado:
                popup = Popup(
                    self.tela,
                    "Faça login para apagar o histórico!"
                )
                popup.mostrar(renderizar_fundo=self.renderizar)
                return
            self.banco.apagar_historico(id_usuario=self.navegador.id_logado)
        self._montar()

    def renderizar(self):
        self.tela.fill(Cores.preto())
        for c in self.componentes:
            c.desenhar(self.tela)
        # Renderiza histórico retrô
        if self.banco:
            historico = self.banco.buscar_historico()
            fonte = pygame.font.SysFont(Fontes.consolas(), 22)
            y = 90
            for partida in historico[:12]:
                jogador_x, jogador_o, vencedor, data = partida
                texto = f"{data.strftime('%d/%m/%Y %H:%M')} - X:{jogador_x} | O:{jogador_o} | V:{vencedor}"
                txt = fonte.render(texto, True, Cores.amarelo())
                self.tela.blit(txt, (40, y))
                y += 32
        pygame.display.flip()