
import heapq
import matplotlib
import osmnx as ox
import math


class Grafo:
    def __init__(self, grafo_teste):
        self.vizinhos = {}
        self.coordenadas = {} 
        
        for node, data in grafo_teste.nodes(data=True):
            self.coordenadas[node] = (data['y'], data['x']) 

        for u, n, dados in grafo_teste.edges(data=True):
            peso = dados.get("length", 1)
            if u not in self.vizinhos:
                self.vizinhos[u] = []
            if n not in self.vizinhos:
                self.vizinhos[n] = []
            self.vizinhos[u].append((n, peso))
            self.vizinhos[n].append((u, peso))


def calcular_heuristica(grafo, no_atual, no_destino):

    lat1, lon1 = grafo.coordenadas[no_atual]
    lat2, lon2 = grafo.coordenadas[no_destino]

    lat_diff = (lat2 - lat1) * 111000
    lon_diff = (lon2 - lon1) * 111000 * math.cos(math.radians(lat1))
    
    return math.sqrt(lat_diff**2 + lon_diff**2)


def a_star(grafo, inicio, destino):

    pais = {n: None for n in grafo.vizinhos.keys()}
    visitados = {n: False for n in grafo.vizinhos.keys()}
    
    # g(n): custo real do início até o nó n
    g_score = {n: float('inf') for n in grafo.vizinhos.keys()}
    g_score[inicio] = 0
    
    # f(n) = g(n) + h(n): custo total estimado
    f_score = {n: float('inf') for n in grafo.vizinhos.keys()}
    f_score[inicio] = calcular_heuristica(grafo, inicio, destino)
    
    # Fila de prioridade: (f_score, g_score, nó)
    fila_prioridade = []
    heapq.heappush(fila_prioridade, (f_score[inicio], g_score[inicio], inicio))
    
    while fila_prioridade:
        f_atual, g_atual, no_atual = heapq.heappop(fila_prioridade)
      
        if g_atual > g_score[no_atual]:
            continue
   
        if visitados[no_atual]:
            continue

        visitados[no_atual] = True

        if no_atual == destino:
            break
      
        for vizinho, peso in grafo.vizinhos[no_atual]:
            if visitados[vizinho]:
                continue
            
            novo_g_score = g_score[no_atual] + peso
            
            if novo_g_score < g_score[vizinho]:
                pais[vizinho] = no_atual
                g_score[vizinho] = novo_g_score
                
                # Calcula f(n) = g(n) + h(n)
                h_score = calcular_heuristica(grafo, vizinho, destino)
                f_score[vizinho] = novo_g_score + h_score
                
                heapq.heappush(fila_prioridade, (f_score[vizinho], novo_g_score, vizinho))
    
    return g_score, pais


bairro_de_teste = "Cruz das Almas, Maceió, Alagoas, Brazil"

velocidades_medias = {
    'residential': 30,
    'secondary': 40,
    'tertiary': 50,
    'primary': 60,
    'motorway': 80,
    'trunk': 80
}

grafo_teste = ox.graph_from_place(bairro_de_teste, network_type="drive")
teste_1 = Grafo(grafo_teste)
grafo_teste = ox.add_edge_speeds(grafo_teste, hwy_speeds=velocidades_medias)
grafo_teste = ox.add_edge_travel_times(grafo_teste)

origem = (-9.6373, -35.7078)
destino = (-9.6300, -35.7001)

origem = ox.distance.nearest_nodes(grafo_teste, X=origem[1], Y=origem[0])
destino = ox.distance.nearest_nodes(grafo_teste, X=destino[1], Y=destino[0])

distancia, pais = a_star(teste_1, origem, destino)

print(f"A melhor rota calculada usando A* saindo de {origem} para {destino} tem o total de {distancia[destino]/1000:.2f} km")

route = ox.shortest_path(grafo_teste, origem, destino, weight="length")
fig, ax = ox.plot_graph_route(grafo_teste, route, node_size=0, show=True)