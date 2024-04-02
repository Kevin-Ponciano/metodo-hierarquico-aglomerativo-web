import csv
import numpy as np

def remover_ponto_virgula_final(linha):
    return linha[:-1] if linha[-1] == '' else linha

def ler_dados_arquivo(caminho):
    dados = []
    mapeamento_classes = {}
    contador_classes = 0

    with open(caminho, 'r', encoding='utf-8') as arquivo:
        leitor_csv = csv.reader(arquivo, delimiter=';')
        for linha in leitor_csv:
            if linha:
                linha_limpa = remover_ponto_virgula_final(linha)
                atributos = list(map(float, linha_limpa[1:-1]))
                classe = linha_limpa[-1]

                if classe not in mapeamento_classes:
                    mapeamento_classes[classe] = contador_classes
                    contador_classes += 1

                classe_numerada = mapeamento_classes[classe]
                dados.append(atributos + [classe_numerada])  

    return dados

def normalizar_dados(dados):
    dados_np = np.array(dados)
    minimo = dados_np.min(axis=0)
    maximo = dados_np.max(axis=0)

    denominador = np.where((maximo - minimo) == 0, 1, maximo - minimo) # Evita divisão por zero
    dados_normalizados = (dados_np - minimo) / denominador
    return dados_normalizados


def calcular_distancia_euclidiana(ponto1, ponto2):
    # Converte os pontos para arrays do NumPy para facilitar operações matemáticas
    ponto1_array = np.array(ponto1)
    ponto2_array = np.array(ponto2)
    
    # Calcula a diferença entre os pontos
    diferenca = ponto1_array - ponto2_array
    
    # Eleva ao quadrado cada elemento da diferença
    quadrado_diferencas = diferenca ** 2
    
    # Soma os valores dos quadrados das diferenças
    soma_quadrados = np.sum(quadrado_diferencas)
    
    # Calcula a raiz quadrada da soma para obter a distância euclidiana
    distancia = np.sqrt(soma_quadrados)
    
    return distancia


def clusterizacao_hierarquica(dados, n_clusters):
    # Inicializa cada dado como um cluster individual
    clusters = [np.array(dado) for dado in dados]
    # Cria um índice para cada cluster
    indice_clusters = [[i] for i in range(len(dados))]
    # Calcula a matriz de distâncias inicial entre todos os clusters
    # Número total de clusters
    num_clusters = len(clusters)

    # Inicializa uma matriz vazia com dimensões apropriadas
    distancias = np.full((num_clusters, num_clusters), float('inf'))

    # Preenche a matriz de distâncias
    for i in range(num_clusters):
        for j in range(i+1, num_clusters):  # Evita calcular a diagonal e duplicatas
            # Calcula a distância Euclidiana entre o cluster i e j
            distancia_ij = calcular_distancia_euclidiana(clusters[i], clusters[j])
            # Atualiza a matriz de distâncias nas posições [i, j] e [j, i]
            distancias[i, j] = distancias[j, i] = distancia_ij


    # Continua até que o número desejado de clusters seja alcançado
    while len(clusters) > n_clusters:
        dist_min = float('inf')  # Inicializa a menor distância com infinito
        para_unir = None  # Inicializa os índices dos clusters a serem unidos
        # Encontra os dois clusters mais próximos
        for i in range(len(distancias)):
            for j in range(i+1, len(distancias)):
                if distancias[i, j] < dist_min:
                    dist_min = distancias[i, j]
                    para_unir = (i, j)
        
        # Calcula o novo cluster como a média dos dois clusters a serem unidos
        novo_cluster = np.mean([clusters[para_unir[0]], clusters[para_unir[1]]], axis=0)
        # Adiciona o novo cluster à lista de clusters
        clusters.append(novo_cluster)
        # Atualiza os índices dos clusters unidos
        indice_clusters.append(indice_clusters[para_unir[0]] + indice_clusters[para_unir[1]])

        # Atualiza a matriz de distâncias para incluir o novo cluster
        distancias = np.append(distancias, [[float('inf')]] * len(distancias), axis=1)
        distancias = np.vstack((distancias, [[float('inf')] * (len(distancias[0]))]))
        
        # Calcula a distância do novo cluster para todos os outros clusters
        for i in range(len(distancias)-1):
            distancias[i, -1] = distancias[-1, i] = calcular_distancia_euclidiana(novo_cluster, clusters[i])
        
        # Remove os clusters antigos da matriz de distâncias
        distancias = np.delete(distancias, para_unir, axis=0)
        distancias = np.delete(distancias, para_unir, axis=1)
        # Remove os clusters antigos da lista de clusters
        clusters.pop(max(para_unir))
        clusters.pop(min(para_unir))
        # Remove os índices dos clusters antigos
        indice_clusters.pop(max(para_unir))
        indice_clusters.pop(min(para_unir))

    # Retorna os índices dos clusters finais
    return indice_clusters

def calcular_sse(clusters, dados):
    sse = []  # Inicializa a lista para armazenar o SSE de cada cluster
    for cluster_indices in clusters:
        # Cria um array com os dados de cada cluster
        cluster = np.array([dados[i] for i in cluster_indices])
        # Calcula o centroide de cada cluster como a média dos seus pontos
        centroide = np.mean(cluster)
        # Calcula o SSE como a soma das distâncias quadradas de cada ponto ao centroide
        soma_sse = np.sum((cluster - centroide) ** 2)
        sse.append(soma_sse)
    # Retorna a lista de SSEs de cada cluster
    return sse


def executar_agrupamento(caminho, n_clusters, is_normalizar_dados):
    
    dados = ler_dados_arquivo(caminho)
    
    if is_normalizar_dados:
        dados_tradados = normalizar_dados(dados)
    else:
        dados_tradados = dados
        
    clusters_indices = clusterizacao_hierarquica(dados_tradados, n_clusters)

    dict = {}
    for i, indices in enumerate(clusters_indices, 1):
        print(f"\nCluster {i} com {len(indices)} objetos:")
        dict[i] = {}
        for indice in indices:
            print(f"Atributos: {dados[indice]}") 
            dict[i][indice] = dados_tradados[indice]
    
    sse_total = calcular_sse(clusters_indices, dados_tradados)
    for i, sse in enumerate(sse_total, 1):
        print(f"SSE do Cluster {i}: {sse}")
        dict[i]["SSE"] = sse

    # print(dict)
if __name__ == "__main__":
    n_clusters = 5
    caminho = "C:\\Users\\Desenvolvedor\\Documents\\Github\\metodo-hierarquico-aglomerativo-web\\python\\dados\\veiculos - teste II.txt"
    is_normalizar_dados = True
    executar_agrupamento( caminho, n_clusters, is_normalizar_dados)
