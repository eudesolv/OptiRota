# dijkstra.py

import heapq
# Não importa osmnx ou matplotlib, pois a classe GrafoPersonalizado já tem os dados

class GrafoPersonalizado:
    """Estrutura simples para converter o grafo NetworkX em uma estrutura de vizinhança
    simples, garantindo que o peso correto seja usado.
    """
    def __init__(self, G_ox, weight_type='travel_time'):
        self.vizinhos = {}
        for u, n, data in G_ox.edges(data=True):
            # Obtém o peso dinamicamente (e usa 'length' ou 1 como fallback)
            peso = data.get(weight_type, data.get('length', 1)) 
            
            # Garante que todos os nós sejam inicializados
            if u not in self.vizinhos:
                self.vizinhos[u] = []
            if n not in self.vizinhos:
                self.vizinhos[n] = []
                
            # O OSMnx é um grafo direcional (MultiDiGraph), então só adicionamos u -> n
            self.vizinhos[u].append((n, peso))

def encontrar_caminho_dijkstra(grafo_personalizado, inicio): 
    """
    Executa o algoritmo de Dijkstra a partir do nó de início.

    Retorna: (distancias, pais, nos_explorados_contador)
    """
    
    # Inicialização
    pais = {n: None for n in grafo_personalizado.vizinhos.keys()}
    distancia = {n: float('inf') for n in grafo_personalizado.vizinhos.keys()}
    distancia[inicio] = 0

    filaPrioridade = []
    heapq.heappush(filaPrioridade, (0, inicio))
    
    nos_explorados_contador = 0

    while filaPrioridade:
        distancia_removida, removido = heapq.heappop(filaPrioridade)

        if distancia_removida > distancia[removido]: 
            continue

        nos_explorados_contador += 1 # Conta o nó quando ele é 'explorado' (removido do heap)
        
        # Itera sobre os vizinhos
        for vizinho, peso in grafo_personalizado.vizinhos.get(removido, []): 
            novaDistancia = distancia_removida + peso
            
            # Relaxamento da aresta
            if novaDistancia < distancia[vizinho]:
                distancia[vizinho] = novaDistancia
                pais[vizinho] = removido 
                heapq.heappush(filaPrioridade, (novaDistancia, vizinho))

    return distancia, pais, nos_explorados_contador