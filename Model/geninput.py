import itertools
import networkx as nx
import time
import bz2
import _pickle as cPickle

class node():
    def __init__(self, number, name):
        self.n = number
        self.name = name

class Edge():
    def __init__(self, number, nodes, conditions):
        self.n = number
        self.nodes = nodes
        self.conditions = conditions

class Treetype():
    def __init__(self, tree, name):
        self.n = len(tree.nodes)
        self.network = tree
        self.name = name

class Tree():
    def __init__(self, tree, Treetypes):
        self.n = len(tree.nodes)
        self.network = tree

        self.type = ''
        for tt in Treetypes:
            if tt.n == self.n:
                if nx.is_isomorphic(tree,tt.network):
                    self.type = tt.name
                    break
        self.prufer = nx.to_prufer_sequence(nx.convert_node_labels_to_integers(tree))
        self.matrix = False

class subTree():
    def __init__(self, tree, Treetypes):
        self.n = len(tree.nodes)
        self.network = tree
        subtrees = make_all_subtrees(tree)
        self.subtrees = []
        if self.n > 2:
            for st in subtrees:
                self.subtrees.append(subTree(st, Treetypes))
        self.type = ''
        if self.n >=4:
            for tt in Treetypes:
                if tt.n == self.n:
                    if nx.is_isomorphic(tree, tt.network):
                        self.type = tt.name
                        break
        self.prufer = nx.to_prufer_sequence(nx.convert_node_labels_to_integers(tree))
        self.matrix = False

    def get_edges_list(self):
        if len(self.subtrees) == 2:
            edgelist = self.network.edges
        else:
            for st in self.subtrees:
                edgelist = st.get_edges_list()

        return edgelist

def make_all_trees(nodes):
    # generate all pairwise combinations of nodes
    edges =  [a for a in itertools.product(range(1,nodes+1), range(1,nodes+1))]

    # use sets to lose..
    # ..symmetric edges: (0,1), (1,0) => keep only (0,1)
    edges = list(set([tuple(set(e)) for e in edges]))
    # ..and self-loops: (0,0)
    edges = [e for e in edges if len(e)>1]

    trees = []
    # generate all graphs that have nodes-1 edges
    for o in itertools.combinations(edges, nodes-1):
        #make sure that all nodes are in the edgelist:
        flattened = [item for sublist in o for item in sublist]

        if len(set(flattened)) == nodes:
            G = nx.Graph()
            G.add_edges_from(o)
            # make sure all nodes are connected
            if len(list(nx.connected_components(G)))==1:
                trees.append(G)
    return trees

def make_all_subtrees(tree):
    L_tree = nx.line_graph(tree) # create linegraph

    new_nodes = list(set(L_tree.nodes)) # newnodes are the nodes of the linegraph and former edges of initree



    edges =  [a for a in itertools.product(new_nodes, new_nodes)]
    # use sets to lose..
    # ..symmetric edges: (0,1), (1,0) => keep only (0,1)
    edges = list(set([tuple(set(e)) for e in edges]))
    # ..and self-loops: (0,0)
    edges = [e for e in edges if len(e)>1]

    trees = []
    # # generate all graphs that have nodes-1 edges
    for o in itertools.combinations(edges, len(new_nodes)-1):
    #     #make sure that all nodes are in the edgelist:
        flattened = [item for sublist in o for item in sublist]
    #
        if len(set(flattened)) == len(new_nodes):
            G = nx.Graph()
            G.add_edges_from(o)
    #         # make sure all nodes are in the tree and connected
            if len(nx.difference(G,L_tree).edges) == 0 and len(list(nx.connected_components(G)))==1:

                #check if G in trees:
                to_add = True
                for tt in trees:
                    if tt.edges==G.edges:
                        to_add=False
                if to_add: trees.append(G)
    return trees

def compressed_pickle(title, data):
    with bz2.BZ2File(title + '.pbz2', 'w') as f:
        cPickle.dump(data, f)



if __name__ == "__main__":
    outputdir = "input/"
    # definition of first tree of an equivalent regluar vine
    isotree = [[(2, 4), (2, 1), (4, 3)],
        [(2, 4), (2, 1), (2, 3)],
        [(2, 4), (2, 1), (4, 3), (1, 5)],
        [(2, 4), (2, 1), (4, 3), (4, 5)],
        [(2, 4), (2, 1), (2, 3), (2, 5)],
        [(3, 4), (4, 6), (4, 5), (6, 1), (2, 5)],
        [(3, 4), (4, 6), (6, 1), (1, 2), (2, 5)],
        [(3, 4), (4, 6), (4, 5), (4, 2), (6, 1)],
        [(3, 4), (4, 6), (4, 5), (6, 1), (1, 2)],
        [(3, 4), (4, 6), (4, 5), (6, 1), (6, 2)],
        [(3, 4), (4, 6), (4, 5), (4, 2), (4, 1)],
        [(3, 4), (3, 7), (4, 6), (7, 5), (6, 1), (5, 2)],
        [(3, 4), (3, 7), (4, 6), (4, 2), (7, 5), (6, 1)],
        [(3, 4), (3, 7), (4, 6), (7, 5), (7, 2), (6, 1)],
        [(3, 4), (3, 7), (3, 1), (4, 6), (4, 2), (7, 5)],
        [(3, 4), (3, 7), (3, 1), (4, 6), (7, 5), (1, 2)],
        [(3, 4), (3, 7), (3, 1), (3, 2), (4, 6), (7, 5)],
        [(3, 4), (3, 7), (4, 6), (4, 2), (4, 1), (7, 5)],
        [(3, 4), (3, 7), (4, 6), (4, 2), (7, 5), (7, 1)],
        [(3, 4), (3, 7), (3, 1), (4, 6), (4, 5), (4, 2)],
        [(3, 4), (3, 7), (3, 1), (3, 5), (3, 2), (4, 6)],
        [(3, 4), (3, 7), (3, 1), (3, 6), (3, 5), (3, 2)],
        [(3, 4), (3, 7), (3, 8), (4, 6), (7, 5), (6, 1), (5, 2)],
        [(3, 4), (3, 7), (3, 8), (4, 6), (7, 5), (6, 1), (8, 2)],
        [(3, 4), (3, 7), (3, 8), (4, 6), (4, 2), (7, 5), (6, 1)],
        [(3, 4), (3, 7), (3, 8), (4, 6), (7, 5), (6, 1), (1, 2)],
        [(3, 4), (3, 7), (3, 8), (4, 6), (7, 5), (7, 2), (6, 1)],
        [(3, 4), (3, 7), (3, 8), (3, 2), (4, 6), (7, 5), (6, 1)],
        [(3, 4), (3, 7), (3, 8), (4, 6), (7, 5), (6, 1), (6, 2)],
        [(3, 4), (3, 7), (3, 8), (3, 1), (4, 6), (7, 5), (8, 2)],
        [(3, 4), (3, 7), (3, 8), (3, 1), (4, 6), (4, 2), (7, 5)],
        [(3, 4), (3, 7), (3, 8), (3, 1), (3, 2), (4, 6), (7, 5)],
        [(3, 4), (3, 7), (3, 8), (4, 6), (7, 5), (8, 2), (8, 1)],
        [(3, 4), (3, 7), (3, 8), (4, 6), (4, 2), (4, 1), (7, 5)],
        [(3, 4), (3, 7), (3, 8), (4, 6), (4, 2), (7, 5), (7, 1)],
        [(3, 4), (3, 7), (4, 6), (7, 5), (6, 8), (6, 1), (5, 2)],
        [(3, 4), (3, 7), (4, 6), (7, 5), (7, 2), (6, 8), (6, 1)],
        [(3, 4), (3, 7), (4, 6), (7, 5), (6, 8), (6, 1), (6, 2)],
        [(3, 4), (3, 7), (4, 6), (7, 5), (6, 8), (5, 2), (2, 1)],
        [(3, 4), (3, 7), (4, 6), (4, 2), (4, 8), (4, 1), (7, 5)],
        [(3, 4), (3, 7), (4, 6), (4, 2), (4, 8), (7, 5), (7, 1)],
        [(3, 4), (3, 7), (3, 8), (3, 1), (4, 6), (4, 5), (4, 2)],
        [(3, 4), (3, 7), (3, 8), (3, 1), (3, 2), (4, 6), (4, 5)],
        [(3, 4), (3, 7), (3, 8), (3, 1), (3, 5), (3, 2), (4, 6)],
        [(3, 4), (3, 7), (3, 8), (3, 1), (3, 6), (3, 5), (3, 2)]]
    titles = ['T4', 'T5', 'T6','T7','T8','T11','T9','T13','T10','T12','T14','T15','T17','T16','T20','T18','T22','T21','T19','T23','T24','T25',
              'T29','T30','T34','T28','T35', 'T40','T33','T37','T38','T44','T31','T42','T36','T27','T32','T39','T26','T45','T41','T43','T46','T47','T48']

    # generate treetypes files
    print("Generating treetypes")
    Treetypes = []
    for i_t, t in enumerate(isotree):
        G = nx.Graph()
        G.add_edges_from(list(set([tuple(set(x)) for x in t])))
        Treetypes.append(Treetype(G,titles[i_t]))

    compressed_pickle(outputdir+'treetypes',Treetypes)

    # generate all input to generate matrices for the nodes specified in the array, limited to 4 to 8 nodes
    for n in [5]:
        # f = open("matrices_"+str(n)+".txt", "w")
        Trees = [] #treescontainer
        st_time = time.time()
        outputdir = "input/"
        f = open(outputdir + "data_for"+str(n)+".txt", 'w')
        f.write("Get all trees with " + str(n) + " nodes"+"\n")
        # all_trees=[]
        # for i_n in range(4,n+1):
        #     all_trees.extend(make_all_trees(i_n))
        print('create all trees')
        all_trees = make_all_trees(n)
        compressed_pickle(outputdir+'alltrees'+str(n),all_trees)

        f.write("number of trees: "+ str(len(all_trees))+"\n")
        Treelib = []
        for tr in all_trees:
            Treelib.append(Tree(tr,Treetypes))
        to_remove = []
        n_trees = len(all_trees)
        xx = 0

        print('split into isomorphic sets')
        tree_dict={}
        for i_t in range(n_trees):
            found = False
            for k in tree_dict:
                if nx.is_isomorphic(all_trees[i_t],all_trees[k]):
                    tree_dict[k].append(i_t)
                    found = True
            if not found:
                tree_dict[i_t]=[i_t]
        # write the tree dictionary
        compressed_pickle(outputdir+'tree_dict'+str(n),tree_dict)

        # generation of trees on the unique trees
        print('start generating trees on '+ str(len(tree_dict)) + ' unique trees')
        added = 0
        n_trees = len(all_trees)
        xtree = 0
        fi_names =[]
        input = []
        for index in tree_dict:
            str_treedict = ''
            for i_t, t in enumerate(tree_dict[index]):
                str_treedict += str(t)
                if i_t < len(tree_dict[index])-1:
                    str_treedict += ';'

            input.append([index,'alltrees'+str(n)+'.pbz2',outputdir+'tree_dict'+str(n)+'.pbz2','treetypes.pbz2',n])

        compressed_pickle(outputdir+'input'+str(n),input)

