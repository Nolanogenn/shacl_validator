from graph import Graph


ttl = open("./data/movieontology.ttl").read().splitlines()
g = Graph(ttl)

g.parse()
#print(g.resources)
