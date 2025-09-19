import osmnx as ox
import networkx as nx
import matplotlib.pyplot as plt
import time

from algorithms.grafo import grafo_base, grafo_mapear
from algorithms.dijkstra import Grafo_Dij_Base, dij_Opi
from algorithms.a_star import Grafo_A_Star_Base, a_star_opi

local = "Alagoas, Brazil"
# Aqui pode ser 'lenght' para comparar somente distância e 'travel_time' 
# para comparar tempo
peso = 'travel_time' 
# Latitude e longitude é Y, X. Caso contrário vai dar errado que nem tava dando para mim
# 7615 6660 e 7860 5306
origem = (-9.6660, -35.7615)
destino = (-9.5306, -35.7860)

# Pega o dicionario resultado (pais) e faz o caminho de volta do destino para o inicio
# para pegar o caminho mais curto, basicamente funciona só para checar qual foi exatamente
# o caminho que o algoritmo fez e ver quais os nós que ele percorreu para formar a rota

def reconstruir_caminho(pais, destino, inicio):
    caminho = []
    atual = destino
    while atual is not None and atual != inicio: # continua enquanto ainda tiver nó e n for o de inicio
        caminho.append(atual)
        atual = pais.get(atual)

    if atual == inicio:
        caminho.append(inicio)
        # inverte pq ele começa do fim e vai pro inicio
        return caminho[::-1]
    return None

def main():
    grafo, weight_type = grafo_base(place_name=local, weight_type=peso) #altera no grafo a loc

    origem_node, destino_node = grafo_mapear(grafo, origem, destino) #altera a origem e destino
    
    if origem_node is None or destino_node is None:
        print("Erro: Nós de origem ou destino não encontrados no grafo.")
        return

    print(f"\nOrigem Node: {origem_node}, Destino Node: {destino_node}")
    print(f"Otimizando pelo peso: '{weight_type}'")

    # --- 3. Execução e Medição do Dijkstra ---
    G_dijkstra = Grafo_Dij_Base(grafo, weight_type=weight_type)
    
    print("\nExecutando Dijkstra...")
    tempo_inicio_dijkstra = time.time()
    # A função retorna 3 valores: (distâncias totais, pais, contagem de nós)
    distancias_d, pais_d, nos_d = dij_Opi(G_dijkstra, origem_node)
    tempo_fim_dijkstra = time.time()
    
    path_dijkstra = reconstruir_caminho(pais_d, destino_node, origem_node)
    custo_dijkstra = distancias_d.get(destino_node, float('inf'))
    tempo_total_dijkstra = tempo_fim_dijkstra - tempo_inicio_dijkstra

    
    # --- 4. Execução e Medição do A* ---
    G_astar = Grafo_A_Star_Base(grafo, weight_type=weight_type)

    print("Executando A*...")
    tempo_inicio_astar = time.time()
    # A função retorna 3 valores: (distâncias totais, pais, contagem de nós)
    distancias_a, pais_a, nos_a = a_star_opi(G_astar, origem_node, destino_node)
    tempo_fim_astar = time.time()
    
    path_a_star = reconstruir_caminho(pais_a, destino_node, origem_node)
    custo_astar = distancias_a.get(destino_node, float('inf'))
    tempo_total_astar = tempo_fim_astar - tempo_inicio_astar
    

    # --- 5. Análise e Comparação de Desempenho ---
    
    if path_dijkstra and path_a_star:
        
        # Unidade do custo
        custo_unit = 'segundos' if weight_type == 'travel_time' else 'metros'
        
        print("\n" + "="*40)
        print("   COMPARAÇÃO DE CUSTO E EFICIÊNCIA")
        print("="*40)
        
        # Confirmação de Custo (devem ser iguais)
        print("\n[Custo da Rota Encontrada]")
        print(f"Custo (Dijkstra): {custo_dijkstra:.2f} {custo_unit}")
        print(f"Custo (A*):       {custo_astar:.2f} {custo_unit}")

        # Comparação de Desempenho
        print("\n[Métricas de Eficiência]")
        print("-" * 40)
        print(f"{'Algoritmo':<10} | {'Tempo (s)':>15} | {'Nós Explorados':>15}")
        print("-" * 40)
        print(f"{'Dijkstra':<10} | {tempo_total_dijkstra:15.6f} | {nos_d:15}")
        print(f"{'A*':<10} | {tempo_total_astar:15.6f} | {nos_a:15}")
        print("-" * 40)
        
        # 6. Visualização (Dijkstra vermelho, A* azul)
        print("\nPlotando as rotas (Dijkstra em Vermelho, A* em Azul) para visualização...")
        fig, ax = ox.plot_graph_route(
            grafo, path_dijkstra, route_color='r', route_linewidth=5, 
            route_alpha=0.6, node_size=0, bgcolor='w', show=False, close=False
        )
        fig, ax = ox.plot_graph_route(
            grafo, path_a_star, route_color='b', route_linewidth=3, 
            route_alpha=1.0, ax=ax, node_size=0, show=True, close=True
        )
    else:
        print("Caminho não encontrado pelo Dijkstra e/ou A*. Verifique as coordenadas e a conectividade do grafo.")


if __name__ == '__main__':
    main()