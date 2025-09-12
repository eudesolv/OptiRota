import matplotlib
import osmnx as ox

bairro_de_teste = "Cruz das Almas, Maceió, Alagoas, Brazil"

g = ox.graph_from_place(bairro_de_teste, network_type="all")

fig, ax = ox.plot_graph(g)