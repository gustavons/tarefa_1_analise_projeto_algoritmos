
import networkx as nx
import matplotlib.pyplot as plt

NAO_DIRIGIDO = "ND"
DIGIRIDO = "D"

def retorna_linhas_arquivos(nome_arquivo):
    with open(nome_arquivo, "r") as arquivo:
        linhas = [linha.strip() for linha in arquivo.readlines()]

    return linhas


def ler_grafo(nome_arquivo):
    linhas = retorna_linhas_arquivos(nome_arquivo)
    tipo_grafo = linhas[0]

    if tipo_grafo != DIGIRIDO and tipo_grafo != NAO_DIRIGIDO:
        raise Exception("Tipo do grafo não especificado corretamente")

    return linhas, tipo_grafo

def gerar_grafo_img(G_symmetric, relacoes_elementos):
    for relacao in relacoes_elementos:
        elemento_1, elemento_2 = relacao.split(",")
        G_symmetric.add_edge(elemento_1, elemento_2)

def processa_e_gera_grafo():

    print("/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/")
    print("/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/\n")
    nome_arquivo = input(
        "Adicione o arquivo na pastas onde "
        "está o programa e digite o nome do arquivo.\n"
        "Caso você não insira nenhum nome, será considerado o \"entrada.txt\" como nome do arquivo:"
    )
    print("\n/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/")
    print("/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/\n\n")

    if not nome_arquivo:
        nome_arquivo = "entrada.txt"

    linhas, tipo_grafo = ler_grafo(nome_arquivo)
    relacoes_elementos = linhas[1:]
    if linhas[0] == DIGIRIDO:
        G_symmetric = nx.DiGraph()
    elif linhas[0] == NAO_DIRIGIDO:
        G_symmetric = nx.Graph()
    else:
        raise Exception(
            f"Tipo de grafo inserido incorretamente. Por favor, edite o arquivo insira na "
            f"primeira linha {DIGIRIDO} para grafo dirigido e {NAO_DIRIGIDO} para não dirigido.")

    gerar_grafo_img(G_symmetric, relacoes_elementos)
    pos = nx.spring_layout(G_symmetric,k=0.3,iterations=20)
    nx.draw_networkx(G_symmetric, pos)
    plt.show()


if __name__ == '__main__':
    processa_e_gera_grafo()

