import heapq
import matplotlib
import osmnx as ox

class Grafo:
    def __init__(self, grafo_teste):
        self.vizinhos = {}
        for u, n, dados in grafo_teste.edges(data=True):
            peso = dados.get("length", 1)
            if u not in self.vizinhos:
                self.vizinhos[u] = []
            if n not in self.vizinhos:
                self.vizinhos[n] = []
            self.vizinhos[u].append((n, peso))
            self.vizinhos[n].append((u, peso))


def dijkstraOpi(grafos, inicio):
    inicial = {n: None for n in grafos.vizinhos.keys()}
    visitados = {n: False for n in grafos.vizinhos.keys()}
    distancia = {n: float('inf') for n in grafos.vizinhos.keys()}
    distancia[inicio] = 0

    filaPrioridade = []
    heapq.heappush(filaPrioridade, (0, inicio))

    while filaPrioridade:
        distancia_removida, removido = heapq.heappop(filaPrioridade)

        if distancia_removida > distancia[removido]: 
            continue
        if visitados[removido]:
            continue

        visitados[removido] = True

        for vizinho, peso in grafos.vizinhos[removido]: 
            if visitados[vizinho]:
                continue

            novaDistancia = distancia_removida + peso
            if novaDistancia < distancia[vizinho]:
                distancia[vizinho] = novaDistancia
                inicial[vizinho] = removido 
                heapq.heappush(filaPrioridade, (novaDistancia, vizinho))

    return distancia, inicial
bairro_de_teste = "Cruz das Almas, Maceió, Alagoas, Brazil"

#isso adiciona velocidades diferentes aos tipos diferentes de ruas em um dicionario para usar dps
velocidades_medias = {
    'residential': 30,
    'secondary': 40,
    'tertiary': 50,
    'primary': 60,
    'motorway': 80,
    'trunk': 80}

grafo_teste = ox.graph_from_place(bairro_de_teste, network_type="drive")
teste_1 = Grafo(grafo_teste)
grafo_teste = ox.add_edge_speeds(grafo_teste, hwy_speeds=velocidades_medias)
grafo_teste = ox.add_edge_travel_times(grafo_teste)
origem = (-9.6373, -35.7078)
destino = (-9.6300, -35.7001) 

origem = ox.distance.nearest_nodes(grafo_teste, X=origem[1], Y=origem[0])
destino = ox.distance.nearest_nodes(grafo_teste, X=destino[1], Y=destino[0])
route = ox.shortest_path(grafo_teste, origem, destino, weight="travel_time")

distancia, pais = dijkstraOpi(teste_1, origem)
print(f"A melhor rota calculada saindo de {origem} para {destino} tem o total de {distancia[destino]/1000:.2f} km")

fig, ax = ox.plot_graph_route(grafo_teste, route, node_size=0, show=True)

