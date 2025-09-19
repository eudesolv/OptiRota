# dijkstra.py

import heapq
# Importe apenas o que é essencial para o algoritmo
# (networkx e osmnx não são necessários aqui se usarmos a classe Grafo)

class GrafoPersonalizado:
    """Estrutura simples para abstrair o grafo NetworkX para o algoritmo."""
    def __init__(self, G_ox, weight_type='length'): # Adicionando weight_type
        self.vizinhos = {}
        for u, n, data in G_ox.edges(data=True):
            # O peso agora é dinâmico, baseado no que foi carregado no osmnx
            peso = data.get(weight_type, data.get('length', 1)) 
            
            # Garante que todos os nós sejam inicializados no dicionário
            if u not in self.vizinhos:
                self.vizinhos[u] = []
            if n not in self.vizinhos:
                self.vizinhos[n] = []
                
            # Adiciona a aresta. (Atenção: Seu código trata o grafo como bidirecional)
            self.vizinhos[u].append((n, peso))
            # O OSMnx é MultiDiGraph (direcional), se quiser bidirecional:
            # self.vizinhos[n].append((u, peso))

def encontrar_caminho_dijkstra(grafo_personalizado, inicio, destino):
    """
    Executa o algoritmo de Dijkstra em um GrafoPersonalizado.
    
    Retorna (distancia_final, dicionario_de_pais)
    """
    
    # ... [O restante do seu código dijkstraOpi] ...
    # Renomeei a função para ser mais explícita:
    
    inicial = {n: None for n in grafo_personalizado.vizinhos.keys()}
    # Remova 'visitados' se você usar a verificação 'distancia_removida > distancia[removido]'
    # pois a fila de prioridade garante que você só processa o menor caminho
    distancia = {n: float('inf') for n in grafo_personalizado.vizinhos.keys()}
    distancia[inicio] = 0

    filaPrioridade = []
    heapq.heappush(filaPrioridade, (0, inicio))

    while filaPrioridade:
        distancia_removida, removido = heapq.heappop(filaPrioridade)

        # Se esta distância já for maior que a melhor encontrada (distancia[removido]), 
        # significa que já encontramos um caminho mais curto para 'removido' anteriormente.
        if distancia_removida > distancia[removido]: 
            continue

        for vizinho, peso in grafo_personalizado.vizinhos.get(removido, []): 
            novaDistancia = distancia_removida + peso
            if novaDistancia < distancia[vizinho]:
                distancia[vizinho] = novaDistancia
                inicial[vizinho] = removido 
                heapq.heappush(filaPrioridade, (novaDistancia, vizinho))

    # A função original retornava (distancia, pais)
    return distancia, inicial