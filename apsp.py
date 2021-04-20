
import networkx as nx
import matplotlib.pyplot as plt
from networkx.algorithms import bipartite
import itertools
import numpy as np
from itertools import combinations
#import fnss
import logging
import random

ne=int(input("Enter Number of Edge nodes"))
edge_nodes=[]
for i in range(1,ne+1):
	edge_nodes.append('Edge device '+str(i))
print(edge_nodes)

nc=int(input("Enter number of IoT cluster nodes"))

iot_nodes=[]
for i in range(1,nc+1):
	iot_nodes.append('IoT device'+str(i))


#r=[5,6,5,3,2,4,3,6,5,5,5,7,6,8,10,5,3,7,8,2,3,5,9,3]
r1=random.choices(range(2,10),k=len(edge_nodes)*len(iot_nodes))


makenodes=[]
makedict={}
k=0
for i in edge_nodes:
	for j in iot_nodes:
		
		makenodes.append((i,j,r1[k]))
		makenodes.append((j,i,r1[k]))
		makedict[(i,j)]=r1[k]
		makedict[(j,i)]=r1[k]
		k=k+1



ed=list(combinations(edge_nodes,2))
print(ed)
p=[]

for i in ed:
	p.append(list(i))
r2=random.choices(range(2,10),k=int((len(edge_nodes)*(len(edge_nodes)-1))/2))
print(r2)
x=0
for i in p:
	
	i.append(r2[x])
	x=x+1
	
edge_edge=[]	
for i in p:
	edge_edge.append(tuple(i))

#clique beween edge devices

ete=nx.Graph()
ete.add_weighted_edges_from(edge_edge)
	
#complete bipartite graph
B=nx.Graph()
B.add_weighted_edges_from(makenodes)
labels1 = nx.get_edge_attributes(B,'weight')
pos1=nx.bipartite_layout(B,iot_nodes)
pos = nx.circular_layout(B)
nx.draw_networkx_nodes(B ,pos1, node_size=2000, nodelist=edge_nodes, node_color='g')
nx.draw_networkx_nodes(B, pos1, node_size=3000, nodelist=iot_nodes, node_color='b')
nx.draw_networkx_edges(B,pos1,  alpha=0.5, width=3)
nx.draw_networkx_edge_labels(B,pos1,font_color='k',edge_labels=labels1)
nx.draw_networkx_labels(B,pos1,font_color='w')
plt.show()



#nearest neibhour 
print(nx.k_nearest_neighbors(B,nodes=iot_nodes, weight='weight'))





#complete bipartite between edge and iot and edge device clique

initial_graph=nx.compose(B,ete)
labels1 = nx.get_edge_attributes(initial_graph,'weight')
pos1=nx.spring_layout(initial_graph)
pos = nx.circular_layout(initial_graph)
nx.draw_networkx_nodes(initial_graph ,pos1, node_size=2000, nodelist=edge_nodes, node_color='g')
nx.draw_networkx_nodes(initial_graph, pos1, node_size=3000, nodelist=iot_nodes, node_color='b')
nx.draw_networkx_edges(initial_graph,pos1,  alpha=0.5, width=3)
nx.draw_networkx_edge_labels(initial_graph,pos1,font_color='k',edge_labels=labels1)
nx.draw_networkx_labels(initial_graph,pos1,font_color='r')
plt.show()

apsp=nx.floyd_warshall(initial_graph)
apsp_e=nx.floyd_warshall(ete)


def find_near(cluster='ICluster1',apsp=apsp):
	min_1=list(apsp[cluster].values())
	min_1.sort()
	i1w=min_1[1]
	for key,value in apsp[cluster].items():
		if i1w==value:
			print(cluster + ' near neibhour is ' +key + ' with edge weight ' +str(value)) 
			return (cluster,key,value)

apbi=[]
for i in iot_nodes:
	
	apbi.append(find_near(i,apsp))
for j in edge_nodes:
	print(sorted(apsp_e[j].items(),key=lambda x:x[1]))
	find_near(j,apsp_e)


ete.add_weighted_edges_from(apbi)
labels1 = nx.get_edge_attributes(ete,'weight')
pos1=nx.spring_layout(ete)
pos = nx.circular_layout(ete)
nx.draw_networkx_nodes(ete,pos1, node_size=2000, nodelist=edge_nodes, node_color='g')
nx.draw_networkx_nodes(ete, pos1, node_size=3000, nodelist=iot_nodes, node_color='b')
nx.draw_networkx_edges(ete,pos1,  alpha=0.5, width=3)
nx.draw_networkx_edge_labels(ete,pos1,font_color='k',edge_labels=labels1)
nx.draw_networkx_labels(ete,pos1,font_color='r')
plt.show()




n=[]
for i in iot_nodes:
	n.append(find_near(i))


e=[]
for j in edge_nodes:
	e.append(find_near(j,apsp_e))
print(e)










min_g1=nx.Graph()
min_g1.add_weighted_edges_from(n)

min_g=nx.compose(min_g1,C)
labels2=nx.get_edge_attributes(min_g,'weight')
pos1=nx.spring_layout(min_g)
pos = nx.spring_layout(min_g)
nx.draw_networkx_nodes(min_g, pos1, node_size=2000, nodelist=edge_nodes, node_color='g')
nx.draw_networkx_nodes(min_g ,pos1, node_size=3000, nodelist=iot_nodes, node_color='b')
nx.draw_networkx_edges(min_g,pos1,  alpha=0.5, width=3)
nx.draw_networkx_edge_labels(min_g,pos1,font_color='k',edge_labels=labels2)
nx.draw_networkx_labels(min_g,pos1,font_color='r')
plt.show()
	

min_g2=nx.compose(B,C)
labels2=nx.get_edge_attributes(min_g2,'weight')
pos1=nx.spring_layout(min_g2)
pos = nx.spring_layout(min_g2)
nx.draw_networkx_nodes(min_g2, pos1, node_size=2000, nodelist=edge_nodes, node_color='g')
nx.draw_networkx_nodes(min_g2,pos1, node_size=3000, nodelist=iot_nodes, node_color='b')
nx.draw_networkx_edges(min_g2,pos1,  alpha=0.5, width=3)
nx.draw_networkx_edge_labels(min_g2,pos1,font_color='k',edge_labels=labels2)
nx.draw_networkx_labels(min_g2,pos1,font_color='r')
plt.show()
	
allpair=nx.floyd_warshall(min_g2)

floyd=[]
for i in iot_nodes:
	floyd.append(find_near(i,allpair))
for k in edge_nodes:
	floyd.append(find_near(k,allpair))
print(floyd)

min_g3=nx.Graph()
min_g3.add_weighted_edges_from(floyd)
labels2=nx.get_edge_attributes(min_g3,'weight')
pos1=nx.circular_layout(min_g3)

nx.draw_networkx_nodes(min_g3, pos1, node_size=2000, nodelist=edge_nodes, node_color='g')
nx.draw_networkx_nodes(min_g3,pos1, node_size=3000, nodelist=iot_nodes, node_color='b')
nx.draw_networkx_edges(min_g3,pos1,  alpha=0.5, width=3)
nx.draw_networkx_edge_labels(min_g3,pos1,font_color='k',edge_labels=labels2)
nx.draw_networkx_labels(min_g3,pos1,font_color='r')
plt.show()

