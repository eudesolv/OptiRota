import osmnx as ox
import networkx as nx
import os # Necessário para checar se o arquivo existe

def grafo_base(
    # Localização e peso que vai ser usado para medir rotas
    place_name="Cruz das Almas, Maceió, Alagoas, Brazil",
    weight_type="travel_time"
    ):
    
    print(f"Fazendo grafo para: {place_name}...")
    
    # Define o nome do arquivo GraphML baseado no local.
    # Ex: 'Alagoas, Brazil.graphml'
    filename = place_name.replace(", ", "_").replace(" ", "_") + ".graphml"
    
    # 1. TENTA CARREGAR O GRAFO SALVO
    if os.path.exists(filename):
        try:
            print(f"Grafo encontrado em disco ({filename}). Carregando...")
            G = ox.load_graphml(filename)
            # Re-calcula tempos/velocidades (caso o arquivo tenha sido salvo sem eles)
            # ou apenas para garantir que o peso correto está lá
            G = ox.add_edge_speeds(G)
            G = ox.add_edge_travel_times(G)
            print("Grafo carregado e preparado a partir do arquivo.")
            return G, weight_type
        except Exception as e:
            print(f"Erro ao carregar o arquivo: {e}. Baixando novamente.")
            # Se falhar ao carregar, continua para baixar
            pass 
    
    # 2. SE NÃO EXISTIR OU FALHAR, BAIXA E SALVA
    print(f"Grafo não encontrado. Baixando e processando para: {place_name}...")
    
    # Baixa o grafico baseado no que foi dito na função base
    G = ox.graph_from_place(place_name, network_type="drive")

    # Define as velocidades médias (o restante do seu código)
    velocidades_medias = {
        'residential': 30, 'secondary': 40, 'tertiary': 50,
        'primary': 60, 'motorway': 80, 'trunk': 80
    }
    # Adiciona as velocidades
    G = ox.add_edge_speeds(G, hwy_speeds=velocidades_medias)
    
    # Calcula o tempo de viagem
    G = ox.add_edge_travel_times(G)
    
    # SALVA O GRAFO para uso futuro (depois do longo download)
    print(f"Grafo baixado e processado. Salvando em {filename}...")
    ox.save_graphml(G, filepath=filename)
    
    print(f"Grafo carregado e preparado. Peso primário: '{weight_type}'.")
    return G, weight_type

def grafo_mapear(G, coords_origem, coords_destino):
    # Aqui seta a origem e o destino para fazer o grafo com base nisso
    node_origem = ox.nearest_nodes(G, X=coords_origem[1], Y=coords_origem[0])
    node_destino = ox.nearest_nodes(G, X=coords_destino[1], Y=coords_destino[0])
    return node_origem, node_destino

if __name__ == '__main__':
    # Teste para ver se funciona e número de nós e arestas
    G, weight = grafo_base(place_name="Maceió, Alagoas, Brazil") # Exemplo de como testar
    if G:
        print(f"N° de nós: {len(G.nodes())}, N° de arestas: {len(G.edges())}")