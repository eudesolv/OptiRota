import osmnx as ox
import networkx as nx
import matplotlib.pyplot as plt
import time

from algorithms.grafo import grafo_base, grafo_mapear
from algorithms.dijkstra import Grafo_Dij_Base, dij_Opi
from algorithms.a_star import Grafo_A_Star_Base, a_star_opi

local = "Maceió, Alagoas, Brazil"
# Aqui pode ser 'lenght' para comparar somente distância e 'travel_time' 
# para comparar tempo
peso = 'travel_time' 
# Latitude e longitude é Y, X. Caso contrário vai dar errado que nem tava dando para mim
# Anotar aqui quais são algumas cordenadas interesantes de se usar
#SP: -53.28 -29.45 V -49.78 -29.34=
#MCZ: -35.7205, -9.6709 V -35.7508, -9.5386
origem = (-9.6709, -35.7205)
destino = (-9.5386, -35.7508)

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
    print("\n"+"― "*30+"\n")
    grafo, weight_type = grafo_base(place_name=local, weight_type=peso)

    origem_node, destino_node = grafo_mapear(grafo, origem, destino)
    
    if origem_node is None or destino_node is None:
        print("Erro: Nós de origem ou destino não encontrados no grafo.")
        return
    
    # Descomente se der problema nos nodes ou pesoS
    #print(f"\nOrigem Node: {origem_node}, Destino Node: {destino_node}")
    #print(f"Otimizando pelo peso: '{weight_type}'")
    
    # DIJKSTRA --------------------------------------------------------------
    G_dijkstra = Grafo_Dij_Base(grafo, weight_type=weight_type)
    
    print("\nExecutando Dijkstra...")
    tempo_inicio_dijkstra = time.time()
    distancias_d, pais_d, nos_d = dij_Opi(G_dijkstra, origem_node)
    tempo_fim_dijkstra = time.time()
    
    path_dijkstra = reconstruir_caminho(pais_d, destino_node, origem_node)
    tempo_total_dijkstra = tempo_fim_dijkstra - tempo_inicio_dijkstra

    # A* -------------------------------------------------------------------
    G_astar = Grafo_A_Star_Base(grafo, weight_type=weight_type)

    print("Executando A*...")
    tempo_inicio_astar = time.time()
    distancias_a, pais_a, nos_a = a_star_opi(G_astar, origem_node, destino_node)
    tempo_fim_astar = time.time()
    
    path_a_star = reconstruir_caminho(pais_a, destino_node, origem_node)
    tempo_total_astar = tempo_fim_astar - tempo_inicio_astar
    
    
    if path_dijkstra and path_a_star:
        
        print("\n" + "="*35)
        print("   COMPARAÇÃO DE COMPLEXIDADE")
        print("="*35)

        # Comparação de Desempenho
        print("\n[Métricas]")
        print("-" * 60)
        print(f"{'Algoritmo':<10} | {'Tempo (ms)':>15} | {'Nós Explorados':>15}")
        print("-" * 60)
        print(f"{'Dijkstra':<10} | {tempo_total_dijkstra*1000:15.3f} | {nos_d:15}")
        print(f"{'A*':<10} | {tempo_total_astar*1000:15.3f} | {nos_a:15}")
        print("-" * 60)
        
        
        # Desenha a linha usando o A*; Da no msm pq os dois vão chegar no mesmo resultado
        print("\nDesenhando a rota desejada...")
        print("\n"+"― "*30+"\n")
        fig, ax = ox.plot_graph_route(
            grafo, path_a_star,route_color='r', route_linewidth=3, route_alpha=1.0, 
            node_size=0, bgcolor='w', show=True, close=True
        )
    else:
        print("Caminho não encontrado pelo A*. Verifique as coordenadas.")
        print("\n"+"― "*30+"\n")


if __name__ == '__main__':
    main()