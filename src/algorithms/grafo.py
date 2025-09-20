import osmnx as ox
import networkx as nx
import os

def grafo_base(
    # Localização e peso que vai ser usado para medir rotas
    place_name="",
    weight_type=""
    ):
    print(f"Procurando grafo para: {place_name}...")
    print("\n")
    data_dir = "src/data" 
    filename_base = place_name.replace(", ", "_").replace(" ", "_") + ".graphml"
    filepath = os.path.join(data_dir, filename_base)
    
    if os.path.exists(filepath):
        try:
            print(f"Grafo encontrado no disco em ({filepath})...\n")
            G = ox.load_graphml(filepath)
            G = ox.add_edge_speeds(G)
            G = ox.add_edge_travel_times(G)
            print("Grafo carregado e preparado a partir do arquivo.")
            return G, weight_type
        except Exception as e:
            print(f"Erro ao carregar o arquivo: {e}. Baixando novamente.")
            # Se falhar ao carregar, continua para baixar
            pass 
    
    # 2. SE NÃO EXISTIR OU FALHAR, BAIXA E SALVA
    print(f"Grafo não encontrado. Baixando e processando para: {place_name}...\n")
    
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
    
    # CRIA O DIRETÓRIO SE NÃO EXISTIR
    if not os.path.exists(data_dir):
        # A flag 'exist_ok=True' evita erro caso a pasta já exista
        os.makedirs(data_dir, exist_ok=True)
    
    # SALVA O GRAFO no novo caminho (filepath)
    print(f"Grafo baixado e processado. Salvando em {filepath}...")
    ox.save_graphml(G, filepath=filepath)
    
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