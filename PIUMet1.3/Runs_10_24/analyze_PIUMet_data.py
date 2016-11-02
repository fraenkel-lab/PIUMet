import sys
import matplotlib.pyplot as plt

w=5

nodes5 = [325, 343, 309, 339]
edges5 = [435, 448, 380, 432] 
singletons5 = [259, 269, 269, 269]

w=10

nodes10 = [361, 355, 353, 403]
edges10 = [479, 462, 452, 532] 
singletons10 = [110, 193, 259, 269]

w=15

nodes15 = [409, 400, 396, 441]
edges15 = [554, 545, 529, 570] 
singletons15 = [69, 110, 159, 224]

w=20

nodes20 = [437, 420, 467, 555]
edges20 = [594, 559, 600, 738] 
singletons20 = [39, 76, 109, 144]

w=25

nodes25 = [432, 477, 520, 494]
edges25 = [594, 645, 687, 641] 
singletons25 = [30, 55, 80, 109]

betas = [4, 6, 8, 10]
omegas = [5, 10, 15, 20, 25]

#------------------------------------------------
data = {5: (nodes5, edges5, singletons5), 10: (nodes10, edges10, singletons10), 15: (nodes15, edges15, singletons15), 
	20: (nodes20, edges20, singletons20), 25: (nodes25, edges25, singletons25)}
all_nodes = (nodes5, nodes10, nodes15, nodes20, nodes25)
all_edges = (edges5, edges10, edges15, edges20, edges25)
all_singletons = (singletons5, singletons10, singletons15, singletons20, singletons25)


# Get data for parameters vs omega
def parameters_for_beta(b):
	""" Returns values of various graph parameters for a given beta """
	nodes = []
	edges = []
	singletons = []
		
	i = None
	if b == 4: i = 0
	elif b == 6: i = 1
        elif b == 8: i = 2
        elif b == 10: i = 3

	for n in all_nodes:
		nodes.append(n[i])
	for e in all_edges:
		edges.append(e[i])
	for s in all_singletons:
		singletons.append(s[i])

	return nodes, edges, singletons


# Write functions to create plots from this data
def make_plots_against_betas(betas, nodes, edges, singletons, w): #, outdirectory)
	""" Makes a plot of various graph characteristics against varying betas """
	plt.plot(betas, edges, label = "Number of Edges")
	plt.plot(betas, nodes, label = "Number of Nodes")
	plt.plot(betas, singletons, label = "Number of singleton peaks")
	plt.xlabel("Betas")
	plt.ylim([0, 800])
	plt.legend(loc = 'best')
	plt.title("Graph parameters for w = %s vs Betas" % w)

	plt.show()
	#plt.savefig(outdirectory)

def make_plots_against_omegas(omegas, nodes, edges, singletons, b):
        """ Makes a plot of various graph characteristics against varying omegas """
        plt.plot(omegas, nodes, label = "Number of Nodes")
        plt.plot(omegas, edges, label = "Number of Edges")
        plt.plot(omegas, singletons, label = "Number of singleton peaks")
        plt.xlabel("Omegas")
        plt.ylim([0, 800])
        plt.legend(loc = 'best')
        plt.title("Graph parameters for b = %s vs Omegas" % b)

        plt.show()
	#plt.savefig(outdirectory)

if __name__ == "__main__":

	method = int(sys.argv[1])
	if method == 0:
		w = sys.argv[2]
		#outdirectory = sys.argv[2]
		(nodes, edges, singletons) = data[int(w)]
		#make_plots_against_betas(betas, nodes, edges, singletons, w) #, outdirectory)

	if method == 1:
		b = sys.argv[2]
		nodes, edges, singletons = parameters_for_beta(int(b))
		make_plots_against_omegas(omegas, nodes, edges, singletons, b) 
