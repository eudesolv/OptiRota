# main.py

import osmnx as ox
import networkx as nx
import matplotlib.pyplot as plt

# --- Importação das Funções ---
from grafo import carregar_e_preparar_grafo, encontrar_nos_origem_destino
from dijkstra import GrafoPersonalizado, encontrar_caminho_dijkstra
from a_star import GrafoPersonalizadoAStar, a_star_pathfinder
# ------------------------------

# --- Configurações Comuns ---
BAIRRO_TESTE = "Cruz das Almas, Maceió, Alagoas, Brazil"
# Use 'travel_time' para rotear por tempo, 'length' para rotear por distância
PESO = 'travel_time' 
COORD_ORIGEM = (-9.6373, -35.7078)
COORD_DESTINO = (-9.6300, -35.7001)

def reconstruir_caminho(pais, destino, inicio):
    """Reconstrói a lista de nós do destino até a origem usando o dicionário 'pais'."""
    caminho = []
    atual = destino
    while atual is not None and atual != inicio:
        caminho.append(atual)
        atual = pais.get(atual)
    if atual == inicio:
        caminho.append(inicio)
        return caminho[::-1] # Inverte o caminho para começar na origem
    return None

def main():
    # 1. Carregar e Preparar o Grafo
    G_ox, weight_type = carregar_e_preparar_grafo(place_name=BAIRRO_TESTE, weight_type=PESO)
    
    # 2. Encontrar Nós
    origem_node, destino_node = encontrar_nos_origem_destino(G_ox, COORD_ORIGEM, COORD_DESTINO)
    
    if origem_node is None or destino_node is None:
        print("Erro: Nós de origem ou destino não encontrados no grafo.")
        return

    print(f"\nOrigem: {origem_node}, Destino: {destino_node}")
    print(f"Otimizando por: {weight_type}")

    # --- 3. Execução do Dijkstra ---
    G_dijkstra = GrafoPersonalizado(G_ox, weight_type=weight_type)
    distancias_d, pais_d = encontrar_caminho_dijkstra(G_dijkstra, origem_node)
    
    # 4. Reconstrução do Caminho Dijkstra
    path_dijkstra = reconstruir_caminho(pais_d, destino_node, origem_node)
    
    # --- 5. Execução do A* ---
    G_astar = GrafoPersonalizadoAStar(G_ox, weight_type=weight_type)
    distancias_a, pais_a = a_star_pathfinder(G_astar, origem_node, destino_node)

    # 6. Reconstrução do Caminho A*
    path_a_star = reconstruir_caminho(pais_a, destino_node, origem_node)


    # --- 7. Análise de Resultados ---
    if path_dijkstra and path_a_star:
        custo_dijkstra = distancias_d.get(destino_node, float('inf'))
        custo_astar = distancias_a.get(destino_node, float('inf'))
        
        print("\n--- Resultados de Custo ---")
        if weight_type == 'travel_time':
            print(f"Custo Dijkstra (Tempo): {custo_dijkstra:.2f} segundos")
            print(f"Custo A* (Tempo): {custo_astar:.2f} segundos")
        else: # length
            print(f"Custo Dijkstra (Distância): {custo_dijkstra:.2f} metros")
            print(f"Custo A* (Distância): {custo_astar:.2f} metros")

        # 8. Visualização
        fig, ax = ox.plot_graph_route(
            G_ox, path_dijkstra, route_color='r', route_linewidth=5, 
            route_alpha=0.6, node_size=0, bgcolor='k', show=False, close=False
        )
        fig, ax = ox.plot_graph_route(
            G_ox, path_a_star, route_color='b', route_linewidth=3, 
            route_alpha=1.0, ax=ax, node_size=0, show=True, close=True
        )
        print("\nRotas plotadas (Dijkstra em vermelho, A* em azul)")
    else:
        print("Caminho não encontrado por um ou ambos os algoritmos.")


if __name__ == '__main__':
    main()