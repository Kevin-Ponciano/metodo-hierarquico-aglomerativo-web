import csv
import numpy as np
import json

# Função para remover o ponto e vírgula final das linhas do arquivo CSV
def remover_ponto_virgula_final(linha):
    return linha[:-1] if linha[-1] == "" else linha

# Função para ler dados do arquivo e mapear classes para números
def ler_dados_arquivo(caminho):
    dados = []
    mapeamento_classes = {}
    contador_classes = 0

    with open(caminho, "r", encoding="utf-8") as arquivo:
        leitor_csv = csv.reader(arquivo, delimiter=";")
        for linha in leitor_csv:
            if linha:
                linha_limpa = remover_ponto_virgula_final(linha)
                atributos = list(map(float, linha_limpa[0:-1])) # Converte strings para float
                classe = linha_limpa[-1]

                if classe not in mapeamento_classes:
                    mapeamento_classes[classe] = contador_classes
                    contador_classes += 1

                classe_numerada = mapeamento_classes[classe]
                dados.append(atributos + [classe_numerada])  

    return dados

# Função para normalizar os dados
def normalizar_dados(dados):
    dados_np = np.array(dados)
    minimo = dados_np.min(axis=0)
    maximo = dados_np.max(axis=0)

    denominador = np.where((maximo - minimo) == 0, 1, maximo - minimo) # Evita divisão por zero
    dados_normalizados = (dados_np - minimo) / denominador
    return dados_normalizados

# Função para calcular a distância euclidiana entre dois pontos
def calcular_distancia_euclidiana(ponto1, ponto2):
    ponto1_array = np.array(ponto1)
    ponto2_array = np.array(ponto2)
    
    diferenca = ponto1_array - ponto2_array
    quadrado_diferencas = diferenca ** 2
    soma_quadrados = np.sum(quadrado_diferencas)
    distancia = np.sqrt(soma_quadrados)
    
    return distancia

# Função principal para realizar a clusterização hierárquica aglomerativa
def clusterizacao_hierarquica(dados, n_clusters):
    # Etapa 1: Inicializa cada dado como um cluster individual
    clusters = [np.array(dado) for dado in dados]
    indice_clusters = [[i] for i in range(len(dados))]
    num_clusters = len(clusters)

    # Prepara a matriz de distâncias com dimensões apropriadas
    distancias = np.full((num_clusters, num_clusters), float("inf"))

    # Etapa 2: Preenche a matriz de distâncias com distâncias euclidianas
    for i in range(num_clusters):
        for j in range(i+1, num_clusters):
            distancia_ij = calcular_distancia_euclidiana(clusters[i], clusters[j])
            distancias[i, j] = distancias[j, i] = distancia_ij

    # Repete as etapas 2 e 3 até atingir o número desejado de clusters
    while len(clusters) > n_clusters:
        dist_min = float("inf")
        para_unir = None

        # Encontra os dois clusters mais próximos baseado na matriz de distâncias
        for i in range(len(distancias)):
            for j in range(i+1, len(distancias)):
                if distancias[i, j] < dist_min:
                    dist_min = distancias[i, j]
                    para_unir = (i, j)

        # Etapa 3: Une os dois clusters mais próximos
        novo_cluster = np.mean([clusters[para_unir[0]], clusters[para_unir[1]]], axis=0)
        clusters.append(novo_cluster)
        indice_clusters.append(indice_clusters[para_unir[0]] + indice_clusters[para_unir[1]])

        # Etapa 4: Atualiza a matriz de distâncias para refletir a união dos clusters
        # Adiciona uma nova linha e coluna à matriz de distâncias
        num_clusters_atual = len(distancias)
        nova_coluna = np.full((num_clusters_atual, 1), float("inf"))
        nova_linha = np.full((1, num_clusters_atual+1), float("inf"))
        
        distancias = np.append(distancias, nova_coluna, axis=1)
        distancias = np.append(distancias, nova_linha, axis=0)

    
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

# Função para calcular a soma dos quadrados dos erros (SSE) de cada cluster
def calcular_sse(clusters, dados):
    sse = []  
    for cluster_indices in clusters:
        cluster = np.array([dados[i] for i in cluster_indices]) # Cria um array com os dados de cada cluster
        centroide = np.mean(cluster) # Calcula o centroide de cada cluster como a média dos seus pontos
        soma_sse = np.sum((cluster - centroide) ** 2) # Calcula o SSE como a soma das distâncias quadradas de cada ponto ao centroide
        sse.append(soma_sse) # Adiciona o SSE do cluster à lista de SSEs
    return sse


def executar_agrupamento(caminho, n_clusters, is_normalizar_dados):
    resultado_dict = {}
    dados = ler_dados_arquivo(caminho)
    
    if is_normalizar_dados:
        dados_tratados = normalizar_dados(dados)
    else:
        dados_tratados = np.array(dados)
        
    clusters_indices = clusterizacao_hierarquica(dados_tratados, n_clusters)

    for i, indices in enumerate(clusters_indices, 1):
        cluster_info = {}
        atributos_cluster = []
        total_objetos = len(indices)
        cluster_info["total_objetos"] = total_objetos
        for indice in indices:
            atributos_cluster.append(dados_tratados[indice].tolist())  # Converte cada array NumPy para lista
        cluster_info["atributos"] = atributos_cluster
        resultado_dict[f"Cluster - {str(i)}"] = cluster_info  # Assegura que a chave é uma string
    
    sse_total = calcular_sse(clusters_indices, dados_tratados)
    for i, sse in enumerate(sse_total, 1):
        resultado_dict[f"Cluster - {str(i)}"]["SSE"] = sse  # Adiciona o SSE ao respectivo cluster no dicionário
    
    return resultado_dict

if __name__ == "__main__":
    n_clusters = 5
    caminho = "/home/dev/repositorios/metodo-hierarquico-aglomerativo-web/python/dados/flores.txt"
    is_normalizar_dados = False
    ahc = executar_agrupamento(caminho, n_clusters, is_normalizar_dados)
    print(json.dumps(ahc, indent=4))
