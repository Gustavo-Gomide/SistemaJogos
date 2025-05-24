from utilitarios.Aprincipal_widgets import Botao, Tela, TextoFormatado, Cores, Fontes, ScrollArea, Painel
from databases.PongPong_database import PongPongDB
from databases.cadastro_database import DadosUsuario

class TelaRankPongPong(Tela):
    """
    Tela de ranking dos jogadores do PongPong.
    Mostra posição, nome, vitórias, derrotas e % de vitória.
    """
    def __init__(self, navegador=None):
        super().__init__(
            largura=900, altura=650, titulo="Ranking PongPong",
            cor_fundo=Cores.preto(), navegador=navegador
        )
        self.navegador = navegador

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
            x=450, y=40, texto="RANKING PONGPONG",
            tamanho=48, cor_texto=Cores.amarelo_ouro(),
            fonte_nome=Fontes.consolas(), centralizado=True
        ))

        # Cabeçalho da tabela (ajuste os x conforme as colunas das linhas)
        self.adicionar_componente(TextoFormatado(
            x=180, y=120, texto="POS", tamanho=28, cor_texto=Cores.amarelo_ouro(), fonte_nome=Fontes.consolas()
        ))
        self.adicionar_componente(TextoFormatado(
            x=250, y=120, texto="NOME", tamanho=28, cor_texto=Cores.branco(), fonte_nome=Fontes.consolas()
        ))
        self.adicionar_componente(TextoFormatado(
            x=480, y=120, texto="VIT", tamanho=28, cor_texto=Cores.verde(), fonte_nome=Fontes.consolas()
        ))
        self.adicionar_componente(TextoFormatado(
            x=570, y=120, texto="DER", tamanho=28, cor_texto=Cores.vermelho(), fonte_nome=Fontes.consolas()
        ))
        self.adicionar_componente(TextoFormatado(
            x=670, y=120, texto="% WIN", tamanho=28, cor_texto=Cores.amarelo(), fonte_nome=Fontes.consolas()
        ))

        # Área de rolagem para o ranking (linhas)
        self.scroll_area = ScrollArea(
            x=120, y=150, largura=660, altura=400,
            altura_conteudo=1000,
            cor_fundo=Cores.preto(),
            cor_barra=Cores.amarelo_ouro()
        )
        self.adicionar_componente(self.scroll_area)

        self.carregar_ranking()

    def carregar_ranking(self):
        usuarios = DadosUsuario.listar_usuarios()
        ranking = []

        for usuario in usuarios:
            id_usuario = usuario[0]
            apelido = usuario[3]
            stats = PongPongDB.estatisticas_usuario(id_usuario)
            ranking.append({
                "apelido": apelido,
                "vitorias": stats["vitorias"],
                "derrotas": stats["derrotas"],
                "porcentagem": stats["porcentagem_vitorias"]
            })

        # Só mostra quem já jogou pelo menos uma partida
        ranking = [j for j in ranking if (j["vitorias"] + j["derrotas"]) > 0]

        if not ranking:
            self.scroll_area.componentes = []
            self.scroll_area.adicionar_componente(TextoFormatado(
                x=20, y=40, texto="Nenhuma partida registrada ainda.",
                tamanho=32, cor_texto=Cores.cinza(), fonte_nome=Fontes.consolas()
            ))
            return

        ranking.sort(key=lambda x: (-x["vitorias"], -x["porcentagem"], x["apelido"]))

        self.scroll_area.componentes = []
        espacamento = 8  # Espaço vertical entre as linhas
        altura_linha = 36  # Altura de cada linha

        for i, jogador in enumerate(ranking, start=1):
            y_linha = (i - 1) * (altura_linha + espacamento)
            self.scroll_area.adicionar_componente(TextoFormatado(
                x=70, y=y_linha, texto=f"{i:02d}", tamanho=26, cor_texto=Cores.amarelo_ouro(), fonte_nome=Fontes.consolas()
            ))
            self.scroll_area.adicionar_componente(TextoFormatado(
                x=130, y=y_linha, texto=f"{jogador['apelido'][:18]:<18}", tamanho=26, cor_texto=Cores.branco(), fonte_nome=Fontes.consolas()
            ))
            self.scroll_area.adicionar_componente(TextoFormatado(
                x=340, y=y_linha, texto=f"{jogador['vitorias']:>3}", tamanho=26, cor_texto=Cores.verde(), fonte_nome=Fontes.consolas()
            ))
            self.scroll_area.adicionar_componente(TextoFormatado(
                x=430, y=y_linha, texto=f"{jogador['derrotas']:>3}", tamanho=26, cor_texto=Cores.vermelho(), fonte_nome=Fontes.consolas()
            ))
            self.scroll_area.adicionar_componente(TextoFormatado(
                x=530, y=y_linha, texto=f"{jogador['porcentagem']:>6.1f}%", tamanho=26, cor_texto=Cores.amarelo(), fonte_nome=Fontes.consolas()
            ))

# Para rodar isolado:
if __name__ == "__main__":
    TelaRankPongPong().rodar()