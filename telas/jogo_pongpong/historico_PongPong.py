from utilitarios.Aprincipal_widgets import Tela, TextoFormatado, Cores, Fontes, Botao, Painel, ScrollArea
from databases.PongPong_database import PongPongDB

class TelaHistoricoPongPong(Tela):
    """
    Tela de histórico de partidas do PongPong, com paginação de 5 por página.
    Mostra partidas do usuário logado, dos mais novos para os mais antigos.
    """
    def __init__(self, navegador=None):
        super().__init__(
            largura=900, altura=650, titulo="Histórico PongPong",
            cor_fundo=Cores.preto(), navegador=navegador
        )
        self.navegador = navegador
        self.pagina = 0  # Página atual

        self.adicionar_componente(Botao(
            x=20, y=20, largura=100, altura=40, texto="Voltar",
            cor_fundo=Cores.cinza(), cor_hover=Cores.cinza_escuro(),
            cor_texto=Cores.branco(),
            funcao=lambda: self.navegador.ir_para("menu pong-pong") if self.navegador else None,
            fonte=Fontes.consolas(), tamanho_fonte=24, raio_borda=12
            )
        )

        # Título
        self.adicionar_componente(TextoFormatado(
            x=450, y=50, texto="HISTÓRICO DE PARTIDAS",
            tamanho=44, cor_texto=Cores.amarelo_ouro(),
            fonte_nome=Fontes.consolas(), centralizado=True
        ))

        # Cabeçalho
        self.adicionar_componente(TextoFormatado(
            x=450, y=120, texto="Data/Hora         Jogador 1      Jogador 2      Vencedor",
            tamanho=28, cor_texto=Cores.branco(),
            fonte_nome=Fontes.consolas(), centralizado=True
        ))

        # Área de rolagem para as partidas
        self.scroll_area = ScrollArea(
            x=120, y=160, largura=660, altura=340,
            altura_conteudo=1000,
            cor_fundo=Cores.cinza_escuro(),
            cor_barra=Cores.amarelo_ouro()
        )
        self.adicionar_componente(self.scroll_area)

        # Botões de navegação
        self.btn_anterior = Botao(
            x=220, y=520, largura=180, altura=44, texto="⏪ Anterior",
            cor_fundo=Cores.azul(), cor_hover=Cores.azul_escuro(), cor_texto=Cores.branco(),
            funcao=self.pagina_anterior, fonte=Fontes.consolas(), tamanho_fonte=24, raio_borda=12
        )
        self.btn_proximo = Botao(
            x=500, y=520, largura=180, altura=44, texto="Próxima ⏩",
            cor_fundo=Cores.azul(), cor_hover=Cores.azul_escuro(), cor_texto=Cores.branco(),
            funcao=self.pagina_proxima, fonte=Fontes.consolas(), tamanho_fonte=24, raio_borda=12
        )
        self.adicionar_componente(self.btn_anterior)
        self.adicionar_componente(self.btn_proximo)

        self.carregar_historico()

    def carregar_historico(self):
        self.scroll_area.componentes = []

        # Busca todas as partidas do banco (ajuste a consulta conforme seu banco)
        partidas = PongPongDB.historico_todas_partidas()  # Você precisa criar esse método!
        total = len(partidas)
        inicio = self.pagina * 5
        fim = inicio + 5
        partidas_pagina = partidas[inicio:fim]

        if not partidas_pagina:
            self.scroll_area.adicionar_componente(TextoFormatado(
                x=250, y=40, texto="Nenhuma partida encontrada.",
                tamanho=28, cor_texto=Cores.cinza(), fonte_nome=Fontes.consolas()
            ))
            return

        espacamento = 8
        altura_linha = 36

        for i, partida in enumerate(partidas_pagina, start=1 + inicio):
            # Ajuste os índices conforme o retorno do seu banco
            data = str(partida[6])[:19]  # data_partida
            jogador1 = partida[1]        # apelido jogador 1
            jogador2 = partida[2]        # apelido jogador 2
            vencedor = partida[3]        # apelido vencedor
            y_linha = (i - 1) * (altura_linha + espacamento)
            self.scroll_area.adicionar_componente(TextoFormatado(
                x=0, y=y_linha, texto=f"{data}", tamanho=24, cor_texto=Cores.amarelo(), fonte_nome=Fontes.consolas()
            ))
            self.scroll_area.adicionar_componente(TextoFormatado(
                x=320, y=y_linha, texto=f"{jogador1}", tamanho=24, cor_texto=Cores.verde(), fonte_nome=Fontes.consolas()
            ))
            self.scroll_area.adicionar_componente(TextoFormatado(
                x=470, y=y_linha, texto=f"{jogador2}", tamanho=24, cor_texto=Cores.azul(), fonte_nome=Fontes.consolas()
            ))
            self.scroll_area.adicionar_componente(TextoFormatado(
                x=620, y=y_linha, texto=f"{vencedor}", tamanho=24, cor_texto=Cores.amarelo_ouro(), fonte_nome=Fontes.consolas()
            ))

    def pagina_anterior(self):
        if self.pagina > 0:
            self.pagina -= 1
            self.carregar_historico()

    def pagina_proxima(self):
        id_usuario = getattr(self.navegador, "id_logado", None)
        partidas = PongPongDB.historico_usuario(id_usuario) if id_usuario else []
        if (self.pagina + 1) * 5 < len(partidas):
            self.pagina += 1
            self.carregar_historico()