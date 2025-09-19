import osmnx as ox
import networkx as nx

def grafo_base(
    # Localização e peso que vai ser usado para medir rotas
    place_name="Cruz das Almas, Maceió, Alagoas, Brazil",
    weight_type="travel_time"
    ):
    
    print(f"Fazendo grafo para: {place_name}...")
    
    # Baixa o grafico baseado no que foi dito na função base e define que é
    # para fazer com ruas, por isso o "drive", tem como fazer com bike e etc tmb
    G = ox.graph_from_place(place_name, network_type="drive")

    # Alguns lugares não tem velocidade de ruas e avenidas definidas, por isso
    # precisa definir para manter tudo certinho; ele recebe dicionario nesse formato
    velocidades_medias = {
        'residential': 30, 'secondary': 40, 'tertiary': 50,
        'primary': 60, 'motorway': 80, 'trunk': 80
    }
    # Adiciona as velocidades
    G = ox.add_edge_speeds(G, hwy_speeds=velocidades_medias)
    
    # Calcula o tempo de viagem (adiciona o atributo travel_time às arestas)
    G = ox.add_edge_travel_times(G)
    
    print(f"Grafo carregado e preparado. Peso primário: '{weight_type}'.")
    return G, weight_type

def grafo_mapear(G, coords_origem, coords_destino):
    # Aqui seta a origem e o destino para fazer o grafo com base nisso
    node_origem = ox.nearest_nodes(G, X=coords_origem[1], Y=coords_origem[0])
    node_destino = ox.nearest_nodes(G, X=coords_destino[1], Y=coords_destino[0])
    return node_origem, node_destino

if __name__ == '__main__':
    # Teste para ver se funciona e número de nós e arestas
    G, weight = grafo_base()
    if G:
        print(f"N° de nós: {len(G.nodes())}, N° de arestas: {len(G.edges())}")