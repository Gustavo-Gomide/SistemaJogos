from utilitarios.Aprincipal_widgets import Tela, Botao, Cores, TextoFormatado, Fontes, ScrollArea
from databases.cadastro_database import DadosUsuario

class TelaRankGlobal(Tela):
    def __init__(self, navegador=None):
        super().__init__(
            largura=700, altura=500, titulo="Ranking Global",
            cor_fundo=Cores.preto(), navegador=navegador
        )
        self.navegador = navegador
        
        # Título
        self.adicionar_componente(TextoFormatado(
            x=350, y=40, texto="RANKING GLOBAL", tamanho=38, 
            cor_texto=Cores.amarelo_ouro(),
            fonte_nome=Fontes.consolas(), centralizado=True
        ))
        
        # Botão Voltar
        self.adicionar_componente(Botao(
            x=20, y=20, largura=120, altura=38, texto="Voltar",
            cor_fundo=Cores.cinza(), cor_hover=Cores.cinza_escuro(),
            cor_texto=Cores.branco(),
            funcao=lambda: self.navegador.ir_para("menu"),
            fonte=Fontes.consolas(), tamanho_fonte=20, raio_borda=10
        ))
        
        # Headers (fora do ScrollArea)
        self.adicionar_componente(TextoFormatado(
            x=70, y=100, texto="Posição", tamanho=22, 
            cor_texto=Cores.amarelo_ouro(), fonte_nome=Fontes.consolas()
        ))
        self.adicionar_componente(TextoFormatado(
            x=170, y=100, texto="Nome", tamanho=22, 
            cor_texto=Cores.verde(), fonte_nome=Fontes.consolas()
        ))
        self.adicionar_componente(TextoFormatado(
            x=400, y=100, texto="Tempo de Jogo", tamanho=22, 
            cor_texto=Cores.azul(), fonte_nome=Fontes.consolas()
        ))
        self.adicionar_componente(TextoFormatado(
            x=580, y=100, texto="Pontos", tamanho=22, 
            cor_texto=Cores.laranja(), fonte_nome=Fontes.consolas()
        ))
        
        # Área de rolagem (agora começa abaixo dos headers)
        self.scroll_area = ScrollArea(
            x=60, y=140, largura=580, altura=320,
            altura_conteudo=1000,
            cor_fundo=Cores.cinza_escuro(),
            cor_barra=Cores.amarelo_ouro()
        )
        self.adicionar_componente(self.scroll_area)
        
        self.carregar_ranking()

    def carregar_ranking(self):
        self.scroll_area.componentes = []
        ranking = DadosUsuario.ranking_global() or []
        
        # Linhas do ranking (dentro do ScrollArea)
        for i, usuario in enumerate(ranking, start=1):
            nome = usuario[0]
            tempo = usuario[1]
            pontos = usuario[2]
            
            # Formatação do tempo em HH:MM:SS
            tempo_str = f"{tempo//3600:02d}:{(tempo%3600)//60:02d}:{tempo%60:02d}" if tempo is not None else "00:00:00"
            
            # Posição (#)
            self.scroll_area.adicionar_componente(TextoFormatado(
                x=10, y=(i-1)*36, texto=f"#{i:02d}", tamanho=20, 
                cor_texto=Cores.amarelo_ouro(), fonte_nome=Fontes.consolas()
            ))
            # Nome do jogador
            self.scroll_area.adicionar_componente(TextoFormatado(
                x=110, y=(i-1)*36, texto=nome, tamanho=20, 
                cor_texto=Cores.verde(), fonte_nome=Fontes.consolas()
            ))
            # Tempo de jogo
            self.scroll_area.adicionar_componente(TextoFormatado(
                x=340, y=(i-1)*36, texto=tempo_str, tamanho=20, 
                cor_texto=Cores.azul(), fonte_nome=Fontes.consolas()
            ))
            # Pontuação
            self.scroll_area.adicionar_componente(TextoFormatado(
                x=520, y=(i-1)*36, texto=f"{int(pontos):,}", tamanho=20, 
                cor_texto=Cores.laranja(), fonte_nome=Fontes.consolas()
            ))