from utilitarios.Aprincipal_widgets import Tela, Botao, Cores, TextoFormatado, Fontes, ScrollArea
from databases.forca_database import ForcaDB
from databases.cadastro_database import DadosUsuario

class TelaRankForca(Tela):
    def __init__(self, navegador=None):
        super().__init__(
            largura=600, altura=400, titulo="Ranking Forca",
            cor_fundo=Cores.preto(), navegador=navegador
        )
        self.navegador = navegador
        self.adicionar_componente(TextoFormatado(
            x=300, y=40, texto="RANKING FORCA", tamanho=38, cor_texto=Cores.verde(),
            fonte_nome=Fontes.consolas(), centralizado=True
        ))
        self.scroll_area = ScrollArea(
            x=80, y=100, largura=440, altura=220,
            altura_conteudo=1000,
            cor_fundo=Cores.cinza_escuro(),
            cor_barra=Cores.verde()
        )
        self.adicionar_componente(self.scroll_area)
        self.adicionar_componente(Botao(
            x=20, y=20, largura=120, altura=38, texto="Voltar",
            cor_fundo=Cores.cinza(), cor_hover=Cores.cinza_escuro(),
            cor_texto=Cores.branco(),
            funcao=lambda: self.navegador.ir_para("menu forca"),
            fonte=Fontes.consolas(), tamanho_fonte=20, raio_borda=10
        ))
        self.carregar_ranking()

    def carregar_ranking(self):
        self.scroll_area.componentes = []
        ranking = ForcaDB.ranking() or []
        print(f"Partidas encontradas: {len(ranking)}")  # DEBUG

        melhores = {}
        for partida in ranking:
            id_usuario = partida[1]
            apelido = partida[2]
            pontos = partida[3]
            print(f"Partida: id_usuario={id_usuario}, apelido={apelido}, pontos={pontos}")  # DEBUG

            if id_usuario is not None:  # Só usuários logados
                if apelido not in melhores or pontos > melhores[apelido][1]:
                    melhores[apelido] = (id_usuario, pontos)

        ranking_ordenado = sorted(
            [(apelido, pontos) for apelido, (id_usuario, pontos) in melhores.items()],
            key=lambda x: x[1], reverse=True
        )
        print(f"Ranking filtrado: {ranking_ordenado}")  # DEBUG

        for i, (apelido, pontos) in enumerate(ranking_ordenado, start=1):
            self.scroll_area.adicionar_componente(TextoFormatado(
                x=10, y=(i-1)*40, texto=f"{i:02d}", tamanho=24, cor_texto=Cores.verde(), fonte_nome=Fontes.consolas()
            ))
            self.scroll_area.adicionar_componente(TextoFormatado(
                x=70, y=(i-1)*40, texto=f"{apelido}", tamanho=24, cor_texto=Cores.amarelo_ouro(), fonte_nome=Fontes.consolas()
            ))
            self.scroll_area.adicionar_componente(TextoFormatado(
                x=320, y=(i-1)*40, texto=f"{pontos}", tamanho=24, cor_texto=Cores.azul(), fonte_nome=Fontes.consolas()
            ))