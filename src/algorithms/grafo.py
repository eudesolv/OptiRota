# grafo.py

import osmnx as ox
import networkx as nx

def carregar_e_preparar_grafo(
    place_name="Cruz das Almas, Maceió, Alagoas, Brazil", 
    weight_type="travel_time" # Define o peso primário a ser usado
):
    """
    Carrega o grafo da rede de ruas e o prepara com velocidades e tempos de viagem.

    Args:
        place_name (str): O nome do local para buscar o grafo.
        weight_type (str): O peso que os algoritmos de roteamento devem usar ('length' ou 'travel_time').

    Returns:
        tuple: (O grafo NetworkX pronto, o tipo de peso escolhido)
    """
    print(f"Buscando grafo para: {place_name}...")
    
    # 1. Baixa o mapa
    G = ox.graph_from_place(place_name, network_type="drive")

    # 2. Define velocidades (para calcular o tempo)
    velocidades_medias = {
        'residential': 30, 'secondary': 40, 'tertiary': 50,
        'primary': 60, 'motorway': 80, 'trunk': 80
    }
    G = ox.add_edge_speeds(G, hwy_speeds=velocidades_medias)
    
    # 3. Calcula o tempo de viagem (adiciona o atributo 'travel_time' às arestas)
    G = ox.add_edge_travel_times(G)
    
    print(f"Grafo carregado e preparado. Peso primário: '{weight_type}'.")
    return G, weight_type

def encontrar_nos_origem_destino(G, origem_coords, destino_coords):
    """
    Encontra os nós (nodes) do grafo mais próximos das coordenadas (lat, lon).
    """
    # X é longitude, Y é latitude no OSMnx/NetworkX
    origem_node = ox.nearest_nodes(G, X=origem_coords[1], Y=origem_coords[0])
    destino_node = ox.nearest_nodes(G, X=destino_coords[1], Y=destino_coords[0])
    return origem_node, destino_node

if __name__ == '__main__':
    # Teste de carregamento
    G, weight = carregar_e_preparar_grafo()
    if G:
        print(f"N° de nós: {len(G.nodes())}, N° de arestas: {len(G.edges())}")