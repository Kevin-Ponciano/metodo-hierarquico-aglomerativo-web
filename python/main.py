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

                rotulo_numerico = mapeamento_classes[classe]
                dados.append(atributos + [rotulo_numerico])  

    return dados

def mapear_rotulos_para_numeros(rotulos):
    mapeamento = {rotulo: indice for indice, rotulo in enumerate(set(rotulos))}
    rotulos_numericos = [mapeamento[rotulo] for rotulo in rotulos]
    return rotulos_numericos, mapeamento

def normalizar_dados(dados):
    dados_np = np.array(dados)
    minimo = dados_np.min(axis=0)
    maximo = dados_np.max(axis=0)

    denominador = np.where((maximo - minimo) == 0, 1, maximo - minimo)
    dados_normalizados = (dados_np - minimo) / denominador
    return dados_normalizados


def calcular_distancia_euclidiana(ponto1, ponto2):
    return np.sqrt(np.sum((np.array(ponto1) - np.array(ponto2)) ** 2))

def clusterizacao_hierarquica(dados, n_clusters):
    clusters = [np.array(dado) for dado in dados]
    indice_clusters = [[i] for i in range(len(dados))]  
    distancias = np.array([[float('inf') if i == j else calcular_distancia_euclidiana(clusters[i], clusters[j]) for j in range(len(clusters))] for i in range(len(clusters))])

    while len(clusters) > n_clusters:
        dist_min = float('inf')
        para_unir = None
        for i in range(len(distancias)):
            for j in range(i+1, len(distancias)):
                if distancias[i, j] < dist_min:
                    dist_min = distancias[i, j]
                    para_unir = (i, j)
        
        novo_cluster = np.mean([clusters[para_unir[0]], clusters[para_unir[1]]], axis=0)
        clusters.append(novo_cluster)
        indice_clusters.append(indice_clusters[para_unir[0]] + indice_clusters[para_unir[1]])

        distancias = np.append(distancias, [[float('inf')]] * len(distancias), axis=1)
        distancias = np.vstack((distancias, [[float('inf')] * (len(distancias[0]))]))
        
        for i in range(len(distancias)-1):
            distancias[i, -1] = distancias[-1, i] = calcular_distancia_euclidiana(novo_cluster, clusters[i])
        
        distancias = np.delete(distancias, para_unir, axis=0)
        distancias = np.delete(distancias, para_unir, axis=1)
        clusters.pop(max(para_unir))
        clusters.pop(min(para_unir))
        indice_clusters.pop(max(para_unir))
        indice_clusters.pop(min(para_unir))

    return indice_clusters

def calcular_sse(clusters, dados):
    sse = []
    for cluster_indices in clusters:
        cluster = np.array([dados[i] for i in cluster_indices])
        centroide = np.mean(cluster, axis=0)
        sse.append(np.sum((cluster - centroide) ** 2))
    return sse

def executar_agrupamento():
    caminho = "C:\\Users\\Desenvolvedor\\Documents\\Github\\metodo-hierarquico-aglomerativo-web\\python\\flores.txt"
    dados = ler_dados_arquivo(caminho)
    dados_normalizados = normalizar_dados(dados)
    
    n_clusters = int(input("Digite a quantidade de clusters que deseja: "))
    clusters_indices = clusterizacao_hierarquica(dados_normalizados, n_clusters)

    dict = {}
    for i, indices in enumerate(clusters_indices, 1):
        print(f"\nCluster {i} com {len(indices)} objetos:")
        dict[i] = {}
        for indice in indices:
            print(f"Atributos: {dados[indice]}") 
            dict[i][indice] = dados[indice]
    
    sse_total = calcular_sse(clusters_indices, dados_normalizados)
    for i, sse in enumerate(sse_total, 1):
        print(f"SSE do Cluster {i}: {sse}")
        dict[i]["SSE"] = sse

    # print(dict)
if __name__ == "__main__":
    executar_agrupamento()
