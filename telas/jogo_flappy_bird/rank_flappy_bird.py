from utilitarios.Aprincipal_widgets import Tela, Botao, Cores, TextoFormatado, Fontes, ScrollArea
from databases.flappy_database import FlappyDB

class TelaRankFlappy(Tela):
    def __init__(self, navegador=None):
        super().__init__(
            largura=400, altura=600, titulo="Ranking Flappy",
            cor_fundo=Cores.azul_claro(), navegador=navegador
        )
        self.navegador = navegador
        self.adicionar_componente(TextoFormatado(
            x=200, y=80, texto="RANKING FLAPPY", tamanho=38, cor_texto=Cores.amarelo_ouro(),
            fonte_nome=Fontes.consolas(), centralizado=True
        ))
        self.scroll_area = ScrollArea(
            x=40, y=100, largura=320, altura=350,
            altura_conteudo=1000,
            cor_fundo=Cores.cinza_escuro(),
            cor_barra=Cores.amarelo_ouro()
        )
        self.adicionar_componente(self.scroll_area)
        self.adicionar_componente(Botao(
            x=20, y=20, largura=120, altura=38, texto="Voltar",
            cor_fundo=Cores.cinza(), cor_hover=Cores.cinza_escuro(),
            cor_texto=Cores.branco(),
            funcao=lambda: self.navegador.ir_para("menu flappy"),
            fonte=Fontes.consolas(), tamanho_fonte=20, raio_borda=10
        ))
        self.carregar_ranking()

    def carregar_ranking(self):
        self.scroll_area.componentes = []
        ranking = FlappyDB.ranking() or []
        
        # Pega a maior pontuação de cada usuário cadastrado
        melhores = {}
        for partida in ranking:
            id_usuario = partida[1]
            apelido = partida[2]
            pontos = partida[3]
            
            if id_usuario is not None:  # Só considera usuários cadastrados
                if id_usuario not in melhores or pontos > melhores[id_usuario][1]:
                    melhores[id_usuario] = (apelido, pontos)
        
        # Ordena por pontuação decrescente
        ranking_ordenado = sorted(melhores.values(), key=lambda x: x[1], reverse=True)
        
        for i, (apelido, pontos) in enumerate(ranking_ordenado, start=1):
            self.scroll_area.adicionar_componente(TextoFormatado(
                x=10, y=(i-1)*40, texto=f"{i:02d}", tamanho=24, 
                cor_texto=Cores.amarelo_ouro(), fonte_nome=Fontes.consolas()
            ))
            self.scroll_area.adicionar_componente(TextoFormatado(
                x=70, y=(i-1)*40, texto=f"{apelido}", tamanho=24,
                cor_texto=Cores.verde(), fonte_nome=Fontes.consolas()
            ))
            self.scroll_area.adicionar_componente(TextoFormatado(
                x=220, y=(i-1)*40, texto=f"{pontos}", tamanho=24,
                cor_texto=Cores.azul(), fonte_nome=Fontes.consolas()
            ))