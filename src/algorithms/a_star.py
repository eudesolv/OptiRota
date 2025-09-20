import heapq
import osmnx as ox
import math
# renomeei os dados e datas todos para data para simplificar
class Grafo_A_Star_Base:
    #Adicionei o peso como atributo tmb para deixar fácil de mudar dps
    def __init__(self, grafo_usado, weight_type='travel_time'):
        self.vizinhos = {}
        self.coordenadas = {} 
        
        for node, data in grafo_usado.nodes(data=True):
            self.coordenadas[node] = (data['y'], data['x'])

        for u, n, data in grafo_usado.edges(data=True):
            # Pega agora o atributo do tipo dp peso também
            peso = data.get(weight_type, data.get('length', 1))
            
            if u not in self.vizinhos:
                self.vizinhos[u] = []
            # A aresta ela é direcional, o que significa que só precisa fazer isso em uma
            # direção, ao invés de fazer do 'u' para o 'n' e 'n' para o 'u'
            self.vizinhos[u].append((n, peso))


def calcular_heuristica(grafo, no_atual, no_destino):

    try:
        lat1, lon1 = grafo.coordenadas[no_atual]
        lat2, lon2 = grafo.coordenadas[no_destino]

        lat_diff = (lat2 - lat1) * 111000
        lon_diff = (lon2 - lon1) * 111000 * math.cos(math.radians(lat1))
        
        return math.sqrt(lat_diff**2 + lon_diff**2)
    except:
        return 0 # Fallback

def a_star_opi(grafo, inicio, destino):
    # CORREÇÃO: Usamos todos os nós a partir das coordenadas, que contém todos
    todos_os_nos = grafo.coordenadas.keys()
    
    # removi visitados aqui e no dijkstra pq n tem necessidade de passar por esse
    # processo de ficar duplicando desnecessariamente e tirando a duplicata, basta
    # checar se o peso for maior e adicionar se não for
    
    # Inicializa com TODOS OS NÓS
    pais = {n: None for n in todos_os_nos}
    
    # g(n): custo real do início até o nó n
    g_score = {n: float('inf') for n in todos_os_nos}
    g_score[inicio] = 0
    
    # f(n) = g(n) + h(n): custo total estimado
    f_score = {n: float('inf') for n in todos_os_nos}
    f_score[inicio] = calcular_heuristica(grafo, inicio, destino)
    
    # Fila de prioridade: (f_score, nó)
    fila_prioridade = []
    heapq.heappush(fila_prioridade, (f_score[inicio], inicio))
    
    # Como eu provavelmente já avisei, coloquei um contandor para comparar o
    # Dijktra com o A* com tempo e nós percorridos
    contador_nos_a = 0
    
    while fila_prioridade:
        # O python pode desempatar o G e F sozinho, n precisa necessariamente fazer isso
        # manualmente
        
        f_atual, no_atual = heapq.heappop(fila_prioridade)
        
        # O .get() é importante aqui, pois o destino pode não ter f_score se não for acessível
        if f_atual > f_score.get(no_atual, float('inf')):
            continue

        if no_atual == destino:
            break
            
        contador_nos_a += 1
        
        # Usamos .get(no_atual, []) para tratar nós sem arestas de saída
        for vizinho, peso in grafo.vizinhos.get(no_atual, []):
            
            # Proteção contra KeyError, garantindo que o vizinho está nos scores
            if vizinho not in g_score:
                 continue
                 
            novo_g_score = g_score[no_atual] + peso
            
            # LINHA QUE CAUSOU O ERRO, AGORA PROTEGIDA PELA INICIALIZAÇÃO CORRETA:
            if novo_g_score < g_score[vizinho]:
                pais[vizinho] = no_atual
                g_score[vizinho] = novo_g_score
                
                # Calcula e armazena o novo f(n)
                h_score = calcular_heuristica(grafo, vizinho, destino)
                novo_f_score = novo_g_score + h_score
                f_score[vizinho] = novo_f_score
                
                heapq.heappush(fila_prioridade, (novo_f_score, vizinho))
    
    return g_score, pais, contador_nos_a