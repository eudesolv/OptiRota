# a_star.py

import heapq
import osmnx as ox

class GrafoPersonalizadoAStar:
    """Estrutura para abstrair o grafo NetworkX, incluindo coordenadas."""
    def __init__(self, G_ox, weight_type='travel_time'):
        self.vizinhos = {}
        self.coordenadas = {} 
        
        # 1. Armazena as coordenadas (lat, lon)
        for node, data in G_ox.nodes(data=True):
            self.coordenadas[node] = (data['y'], data['x'])

        # 2. Armazena os vizinhos com o peso correto
        for u, n, data in G_ox.edges(data=True):
            peso = data.get(weight_type, data.get('length', 1))
            
            if u not in self.vizinhos:
                self.vizinhos[u] = []
            
            self.vizinhos[u].append((n, peso)) # Aresta direcional


def calcular_heuristica(grafo, no_atual, no_destino):
    """
    Heurística (h): Distância Great Circle (Haversine) entre dois nós em metros.
    Ideal para dados geográficos.
    """
    try:
        lat1, lon1 = grafo.coordenadas[no_atual]
        lat2, lon2 = grafo.coordenadas[no_destino]
        # Usa a função otimizada do OSMnx
        return ox.distance.great_circle_vec(lat1, lon1, lat2, lon2)
    except:
        return 0 # Fallback

def a_star_pathfinder(grafo, inicio, destino):
    """
    Executa o algoritmo A* (A-estrela).

    Retorna: (g_score, pais, nos_explorados_contador)
    """
    
    pais = {n: None for n in grafo.vizinhos.keys()}
    
    # g(n): custo real do início até o nó n
    g_score = {n: float('inf') for n in grafo.vizinhos.keys()}
    g_score[inicio] = 0
    
    # f(n) = g(n) + h(n): custo total estimado
    f_score = {n: float('inf') for n in grafo.vizinhos.keys()}
    f_score[inicio] = calcular_heuristica(grafo, inicio, destino)
    
    # Fila de prioridade: (f_score, nó)
    fila_prioridade = []
    heapq.heappush(fila_prioridade, (f_score[inicio], inicio))
    
    nos_explorados_contador = 0
    
    while fila_prioridade:
        f_atual, no_atual = heapq.heappop(fila_prioridade)
        
        if f_atual > f_score[no_atual]:
            continue

        if no_atual == destino:
            break
            
        nos_explorados_contador += 1 # Conta o nó quando ele é 'explorado'
        
        for vizinho, peso in grafo.vizinhos.get(no_atual, []):
            novo_g_score = g_score[no_atual] + peso
            
            if novo_g_score < g_score[vizinho]:
                pais[vizinho] = no_atual
                g_score[vizinho] = novo_g_score
                
                # Calcula e armazena o novo f(n)
                h_score = calcular_heuristica(grafo, vizinho, destino)
                novo_f_score = novo_g_score + h_score
                f_score[vizinho] = novo_f_score
                
                heapq.heappush(fila_prioridade, (novo_f_score, vizinho))
    
    return g_score, pais, nos_explorados_contador