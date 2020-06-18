NAO_DIRIGIDO = "ND"
DIGIRIDO = "D"


def retorna_linhas_arquivos(nome_arquivo):
    with open(nome_arquivo, "r") as arquivo:
        linhas = [linha.strip() for linha in arquivo.readlines()]
    return linhas


def ler_grafo(nome_arquivo):
    print(f"Processando o arquivo {nome_arquivo}")
    linhas = retorna_linhas_arquivos(nome_arquivo)
    tipo_grafo = linhas[0]
    if tipo_grafo != DIGIRIDO and tipo_grafo != NAO_DIRIGIDO:
        raise Exception("Tipo do grafo não especificado corretamente")
    return linhas, tipo_grafo


def ajustar_matriz(matriz, mapeamento_indices_nos, indices):

    for ind in indices:
        matriz[mapeamento_indices_nos[ind]].append(0)

    return matriz


def prepara_matriz_indices(matriz, mapeamento_nos_indices, mapeamento_indices_nos, elemento):
    if not matriz.get(elemento):
        todos_indices = mapeamento_nos_indices.values()
        indice = len(todos_indices)
        mapeamento_nos_indices[elemento] = indice
        mapeamento_indices_nos[indice] = elemento
        if not indice == 0:
            matriz[elemento] = [0] * (indice + 1)
        else:
            matriz[elemento] = [0]
        matriz = ajustar_matriz(matriz, mapeamento_indices_nos, list(todos_indices)[0:indice])
    return matriz, mapeamento_nos_indices, mapeamento_indices_nos


def inserir_adjacencia(matriz, mapeamento_nos_indices, elemento_1, elemento_2):
    matriz[elemento_1][mapeamento_nos_indices[elemento_2]] = 1
    return matriz


def gerar_matriz(relacoes_elementos):
    mapeamento_nos_indices = {}
    mapeamento_indices_nos = {}
    matriz = {}
    for relacao in relacoes_elementos:
        elemento_1, elemento_2 = relacao.split(",")
        matriz, mapeamento_nos_indices, mapeamento_indices_nos = prepara_matriz_indices(
            matriz, mapeamento_nos_indices, mapeamento_indices_nos, elemento_1
        )
        matriz, mapeamento_nos_indices, mapeamento_indices_nos = prepara_matriz_indices(
            matriz, mapeamento_nos_indices, mapeamento_indices_nos, elemento_2
        )
        matriz = inserir_adjacencia(matriz, mapeamento_nos_indices, elemento_1, elemento_2)

    return matriz, mapeamento_nos_indices, mapeamento_indices_nos


def verifica_se_nos_sao_adjacentes(matriz, mapeamento_nos_indices, vert_1, vert_2):

    if mapeamento_nos_indices.get(vert_1.lower()) is None or mapeamento_nos_indices.get(vert_2.lower()) is None:
        raise Exception("Os vertices infomados na consuta de adjacencia não fazem parte do grafo")

    ind_vert_1 = mapeamento_nos_indices[vert_1.lower()]
    ind_vert_2 = mapeamento_nos_indices[vert_2.lower()]

    valor_1 = matriz[vert_1.lower()][ind_vert_2]
    valor_2 = matriz[vert_2.lower()][ind_vert_1]

    return valor_1 == 1 or valor_2 == 1


def calcula_grau_vertice_grafo_nao_dirigido(matriz, mapeamento_nos_indices, vertice_buscado, tipo_grafo):
    vertice_buscado = vertice_buscado.lower()
    if mapeamento_nos_indices.get(vertice_buscado.lower()) is None:
        raise Exception("O vertice buscado infomado na consuta de grau não faz parte do grafo")

    lista_de_todos_vertices = list(mapeamento_nos_indices.keys())
    lista_de_todos_vertices.remove(vertice_buscado)

    lista_vertices_adjacentes = []
    for vert_da_vez in lista_de_todos_vertices:
        retorno = verifica_se_nos_sao_adjacentes(matriz, mapeamento_nos_indices, vertice_buscado, vert_da_vez)
        if retorno:
            lista_vertices_adjacentes.append(vert_da_vez)

    if tipo_grafo == NAO_DIRIGIDO:
        valor = matriz[vertice_buscado][mapeamento_nos_indices[vertice_buscado]]
        if valor == 1:
            lista_vertices_adjacentes.append(vertice_buscado)
            lista_vertices_adjacentes.append(vertice_buscado)

        return lista_vertices_adjacentes


def calcula_grau_vertice_grafo_dirigido(
    matriz, mapeamento_nos_indices, mapeamento_indices_nos, vertice_buscado, tipo_grafo
):
    vertice_buscado = vertice_buscado.lower()
    if mapeamento_nos_indices.get(vertice_buscado.lower()) is None:
        raise Exception("O vertice buscado infomado na consuta de grau não faz parte do grafo")

    arestas_saindo_do_vertice_buscado = matriz[vertice_buscado]
    list_indices_emissao = []
    for indice in range(0, len(arestas_saindo_do_vertice_buscado)):
        aresta = arestas_saindo_do_vertice_buscado[indice]
        if aresta == 1:
            list_indices_emissao.append(mapeamento_indices_nos[indice])

    lista_de_todos_vertices = list(mapeamento_nos_indices.keys())
    lista_de_todos_vertices.remove(vertice_buscado)
    list_indices_recepcao = []

    for vert_da_vez in lista_de_todos_vertices:
        valor = matriz[vert_da_vez][mapeamento_nos_indices[vertice_buscado]]
        if valor == 1:
            list_indices_recepcao.append(vert_da_vez)

    if tipo_grafo == DIGIRIDO:
        valor = matriz[vertice_buscado][mapeamento_nos_indices[vertice_buscado]]
        if valor == 1:
            list_indices_recepcao.append(vertice_buscado)
            list_indices_emissao.append(vertice_buscado)

    return list_indices_recepcao, list_indices_emissao


def busca_todos_os_vizinhos(matriz, mapeamento_nos_indices, vertice_buscado):
    vertice_buscado = vertice_buscado.lower()
    if mapeamento_nos_indices.get(vertice_buscado.lower()) is None:
        raise Exception("O vertice buscado infomado na consuta de grau não faz parte do grafo")

    lista_de_todos_vertices = list(mapeamento_nos_indices.keys())
    lista_de_todos_vertices.remove(vertice_buscado)

    lista_vertices_adjacentes = []
    for vert_da_vez in lista_de_todos_vertices:
        retorno = verifica_se_nos_sao_adjacentes(matriz, mapeamento_nos_indices, vertice_buscado, vert_da_vez)
        if retorno:
            lista_vertices_adjacentes.append(vert_da_vez)

    return lista_vertices_adjacentes


def visitar_arestas_grafo(matriz, mapeamento_nos_indices, mapeamento_indices_nos):
    todos_os_vertices = list(mapeamento_nos_indices.keys())

    for vertice in todos_os_vertices:
        lista_de_arestas = matriz[vertice]

        for i in range(0, len(lista_de_arestas)):
            if lista_de_arestas[i] == 1:
                print(f"Passou pela aresta {vertice} - {mapeamento_indices_nos[i]}")


import os


def limpa_console():
    os.system("cls" if os.name == "nt" else "clear")


def _recebe_dois_vertices_e_verifica_se_sao_adjacentes(matriz, mapeamento_nos_indices):
    print("\n\nVerificação se dois vertices são adjacentes")

    vert_1 = input("Digite a identificação do primeiro vertice:")
    vert_2 = input("Digite a identificação do segundo vertice")
    sao_adjacentes = verifica_se_nos_sao_adjacentes(matriz, mapeamento_nos_indices, vert_1, vert_2)

    conj = "não "
    if sao_adjacentes:
        conj = ""

    print(f'Vertices "{vert_1}" e "{vert_2}" {conj}são adjacentes')


def _recebe_um_vertice_e_calcula_grau(matriz, mapeamento_nos_indices, tipo_grafo, mapeamento_indices_nos):
    print("\n\nVerificação do grau de um vertice")

    vertice = input("Digite a identificação do vertice:")
    if tipo_grafo == NAO_DIRIGIDO:
        retorno_grau = calcula_grau_vertice_grafo_nao_dirigido(matriz, mapeamento_nos_indices, vertice, tipo_grafo)
        print(f'Grau do vertice "{vertice}" é de {len(retorno_grau)}')
    elif tipo_grafo == DIGIRIDO:
        retorno_grau_recepcao, retorno_grau_emissao = calcula_grau_vertice_grafo_dirigido(
            matriz, mapeamento_nos_indices, mapeamento_indices_nos, vertice, tipo_grafo
        )
        print(f'Grau de recepcao do vertice "{vertice}" é de {len(retorno_grau_recepcao)}')
        print(f'Grau de emissao do vertice "{vertice}" é de {len(retorno_grau_emissao)}')


def _recebe_um_vertice_e_busca_todos_os_vizinhos(matriz, mapeamento_nos_indices):
    print("\n\nBusca por todos os vizinhos de um vertice")

    vertice = input("Digite a identificação do vertice:")
    vizinhos = busca_todos_os_vizinhos(matriz, mapeamento_nos_indices, vertice)
    print(f'Vizinhos do vertice "{vertice}" são os: {vizinhos}')


def _vai_visitar_todas_as_arestas_grafo(matriz, mapeamento_nos_indices, mapeamento_indices_nos):
    print("\n\nBusca por todos os vizinhos de um vertice")
    visitar_arestas_grafo(matriz, mapeamento_nos_indices, mapeamento_indices_nos)


def roda_representacao_grafo():
    print("/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/")
    print("/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/\n")
    nome_arquivo = input(
        "Adicione o arquivo na pastas onde "
        "está o programa e digite o nome do arquivo.\n"
        'Caso você não insira nenhum nome, será considerado o "entrada.txt" como nome do arquivo:'
    )
    print("\n/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/")
    print("/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/\n\n")

    if not nome_arquivo:
        nome_arquivo = "entrada.txt"

    linhas, tipo_grafo = ler_grafo(nome_arquivo)

    relacoes_elementos = linhas[1:]
    matriz, mapeamento_nos_indices, mapeamento_indices_nos = gerar_matriz(relacoes_elementos)

    print(f"Grafo do {nome_arquivo} foi processado com sucesso")
    while True:
        print(
            "Digite:"
            "\n\t0 - Para encerrar o programa"
            "\n\t1 - Para verificar se dois vértices (vX e vY) e são adjacentes"
            "\n\t2 - Calcular o grau de um vértice qualquer"
            "\n\t3 - Buscar todos os vizinhos de vértice qualquer"
            "\n\t4 - Visitar todas as arestas do grafo"
        )
        operacao = input("Opção:")
        if str(operacao) == "0":
            print("Encerrado o programa...")
            break
        elif str(operacao) == "1":
            _recebe_dois_vertices_e_verifica_se_sao_adjacentes(matriz, mapeamento_nos_indices)
        elif str(operacao) == "2":
            _recebe_um_vertice_e_calcula_grau(matriz, mapeamento_nos_indices, tipo_grafo, mapeamento_indices_nos)
        elif str(operacao) == "3":
            _recebe_um_vertice_e_busca_todos_os_vizinhos(matriz, mapeamento_nos_indices)
        elif str(operacao) == "4":
            _vai_visitar_todas_as_arestas_grafo(matriz, mapeamento_nos_indices, mapeamento_indices_nos)
        else:
            print("Opção inválida!!!")


if __name__ == "__main__":
    roda_representacao_grafo()
