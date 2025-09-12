import matplotlib
import osmnx as ox
#bora la galerinha do youtube !!!!!!!

#usando cruz das almas como o bairro teste
bairro_de_teste = "Cruz das Almas, Maceió, Alagoas, Brazil"

#isso adiciona velocidades diferentes aos tipos diferentes de ruas em um dicionario para usar dps
velocidades_medias = {
    'residential': 30,
    'secondary': 40,
    'tertiary': 50,
    'primary': 60,
    'motorway': 80,
    'trunk': 80
}
#baixa o mapa, especificando com o "drive" para baixar só as ruas que passam carro.
grafo_teste = ox.graph_from_place(bairro_de_teste, network_type="drive")
#adiciona o dicionario para ser usado pelo osmnx
grafo_teste = ox.add_edge_speeds(grafo_teste, hwy_speeds=velocidades_medias)
#isso automaticamente calcula o tempo de viagem usando a velocidade anterior 
# e a distância de quando ele baixou o grafo
grafo_teste = ox.add_edge_travel_times(grafo_teste)
#
#   Agora isso aqui é um exemplo de como seria usando a propria função do osmnx
#       primeiro selecionar a origem e a destinação
origem = (-9.6373, -35.7078)
destino = (-9.6300, -35.7001) 

origem = ox.distance.nearest_nodes(grafo_teste, X=origem[1], Y=origem[0])
destino = ox.distance.nearest_nodes(grafo_teste, X=destino[1], Y=destino[0])

#só abusar do próprio algoritimo deles de encontrar o caminho mais curto, 
# ele usa dijstra mas n sei se usa A*. Importante colocar o peso como o tempo de viagem
route = ox.shortest_path(grafo_teste, origem, destino, weight="travel_time")

#e depois é só fazer o mapa
fig, ax = ox.plot_graph_route(grafo_teste, route, node_size=0, show=True)

#visualizar a quantidade de nós e arestas e dps visualizar o grafo

#print(f"N° de cruzamentos (Nós): {len(grafo_teste.nodes())}")
#print(f"N° de ruas (Arestas): {len(grafo_teste.edges())}")

#fig, ax = ox.plot_graph(grafo_teste)
