# a_star.py

import heapq
import math
import osmnx as ox # Necessário para a heurística Haversine

class GrafoPersonalizadoAStar:
    """Estrutura para abstrair o grafo NetworkX, incluindo coordenadas."""
    def __init__(self, G_ox, weight_type='length'):
        self.vizinhos = {}
        self.coordenadas = {} 
        
        # 1. Armazena as coordenadas dos nós
        for node, data in G_ox.nodes(data=True):
            self.coordenadas[node] = (data['y'], data['x']) # (lat, lon)

        # 2. Armazena os vizinhos com o peso correto
        for u, n, data in G_ox.edges(data=True):
            peso = data.get(weight_type, data.get('length', 1))
            
            if u not in self.vizinhos:
                self.vizinhos[u] = []
            
            self.vizinhos[u].append((n, peso)) # Mantendo a direcionalidade do OSMnx


def calcular_heuristica(grafo, no_atual, no_destino):
    """Calcula a distância em linha reta (Haversine/Great Circle) em metros."""
    
    # Sua heurística: (Euclidiana com aproximação de graus para metros)
    # lat1, lon1 = grafo.coordenadas[no_atual]
    # ...
    # return math.sqrt(lat_diff**2 + lon_diff**2)
    
    # Alternativa mais precisa (usa a função otimizada do OSMnx):
    try:
        lat1, lon1 = grafo.coordenadas[no_atual]
        lat2, lon2 = grafo.coordenadas[no_destino]
        # Calcula a distância Great Circle (Haversine)
        return ox.distance.great_circle_vec(lat1, lon1, lat2, lon2)
    except:
        # Fallback para o caso de o nó não ter coordenadas (improvável com OSMnx)
        return 0

def a_star_pathfinder(grafo, inicio, destino):
    """
    Executa o algoritmo A* em um GrafoPersonalizadoAStar.
    
    Retorna (g_score_final, dicionario_de_pais)
    """
    
    # ... [O restante do seu código a_star] ...
    
    pais = {n: None for n in grafo.vizinhos.keys()}
    
    g_score = {n: float('inf') for n in grafo.vizinhos.keys()}
    g_score[inicio] = 0
    
    f_score = {n: float('inf') for n in grafo.vizinhos.keys()}
    f_score[inicio] = calcular_heuristica(grafo, inicio, destino)
    
    # Fila de prioridade: (f_score, nó) - o g_score não é estritamente necessário no heap, 
    # mas ajuda a desempatar, se precisar. O nó é o que importa.
    fila_prioridade = []
    heapq.heappush(fila_prioridade, (f_score[inicio], inicio))
    
    while fila_prioridade:
        f_atual, no_atual = heapq.heappop(fila_prioridade) # Apenas f_score e o nó
        
        # Se o f_score tirado é maior que o f_score atual no mapa, é uma rota antiga.
        if f_atual > f_score[no_atual]:
            continue

        if no_atual == destino:
            break
        
        for vizinho, peso in grafo.vizinhos.get(no_atual, []):
            novo_g_score = g_score[no_atual] + peso
            
            if novo_g_score < g_score[vizinho]:
                pais[vizinho] = no_atual
                g_score[vizinho] = novo_g_score
                
                # Calcula f(n) = g(n) + h(n)
                h_score = calcular_heuristica(grafo, vizinho, destino)
                novo_f_score = novo_g_score + h_score
                f_score[vizinho] = novo_f_score
                
                # Enfileira o novo f_score e o nó
                heapq.heappush(fila_prioridade, (novo_f_score, vizinho))
    
    return g_score, pais