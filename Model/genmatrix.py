import numpy as np
import bz2
import _pickle as cPickle
import networkx as nx
import itertools
import copy

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
        # subtrees = make_all_subtrees(tree)
        # self.subtrees = []
        # if self.n > 2:
        #     for st in subtrees:
        #         self.subtrees.append(Tree(st))
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

def create_treemat(sequence):
    treemat =[]
    for seq in sequence:
        submat = []
        for iseq in seq:
            P = np.array(iseq).flatten()
            new = []
            cond = []
            for i in np.unique(P):
                if np.count_nonzero(P == i)==1:
                    new.append(i)
                else:
                    cond.append(i)
            if len(cond) == 0:
                submat.append(new)
            else:
                submat.append(np.concatenate((new, cond)))
        treemat.append(submat)

    mm = creatematrix(treemat)

    return mm, treemat

def get_sequence(subs, sequences = []):
    for sub in subs:
        print(sub.edges)
        if len(sub.nodes) >= 2:

            xx = get_sequence(sub,sequences)
            print(xx)
            sequences.extend(xx)
        else:
            mm=1
            # print(sub.nodes)
            # sequences.extend(list(sub.edges))

    return sequences

def creatematrix(treemat):
    matrix = np.zeros((len(treemat) + 1, len(treemat) + 1), dtype=int)
    diags = []
    used = {}
    for t in treemat:
        for st in t:
            used[str(st)] = False
    for i_col in range(len(treemat)):
        for i_sub, st in enumerate(treemat):
            if i_sub >= i_col: #Start filling the matrix
                if i_col == i_sub: # we are on the diagonal
                    if len(diags) == 0:
                        matrix[i_col, i_col] = st[0][0]
                        matrix[i_sub + 1, i_col] = st[0][1]
                        diags.append(st[0][0])
                        used[str(st[0])] = True
                    else:

                        for ee in st:
                            if not ee[0] in diags and not ee[1] in diags and not used[str(ee)]:
                                matrix[i_col, i_col] = ee[0]
                                matrix[i_col + 1, i_col] = ee[1]
                                diags.append(ee[0])
                                used[str(ee)] = True
                                break
                if i_sub > i_col:
                    for ee in st:
                        if matrix[i_col, i_col] in ee and not used[str(ee)]:
                            # print(np.delete(ee, np.where(ee == matrix[i_col, i_col]))[0])
                            matrix[i_sub + 1, i_col] = np.delete(ee, np.where(ee == matrix[i_col, i_col]))[0]
                            used[str(ee)] = True

    for i in range(1,len(treemat) + 2):
        if i not in diags:
            matrix[-1, -1] = i

    return matrix

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
    # nx.draw(tree, with_labels=True)
    # plt.show()
    # nx.draw(L_tree, with_labels=True)
    # plt.show()

    new_nodes = list(set(L_tree.nodes)) # newnodes are the nodes of the linegraph and former edges of initree
    # new_labels = create_labels(new_nodes)


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

def get_matrices(tree, Treetypes,n):
    matrices =[]
    subtrees = [subTree(tree, Treetypes)]
    treedata = []
    types = []
    if n == 4:
        for T1 in subtrees:
            for T2 in T1.subtrees:
                for T3 in T2.subtrees:
                    treedata.append([T3.network.edges, T2.network.edges, T1.network.edges])
                    types.append([T1.type])
    elif n == 5:
        for T1 in subtrees:
            for T2 in T1.subtrees:
                for T3 in T2.subtrees:
                    for T4 in T3.subtrees:
                        treedata.append([T4.network.edges, T3.network.edges, T2.network.edges, T1.network.edges])
                        types.append([T1.type, T2.type])
    elif n == 6:
        for T1 in subtrees:
            for T2 in T1.subtrees:
                for T3 in T2.subtrees:
                    for T4 in T3.subtrees:
                        for T5 in T4.subtrees:
                            treedata.append([T5.network.edges, T4.network.edges, T3.network.edges, T2.network.edges,
                                             T1.network.edges])
                            types.append([T1.type, T2.type, T3.type])
    elif n == 7:
        for T1 in subtrees:
            for T2 in T1.subtrees:
                for T3 in T2.subtrees:
                    for T4 in T3.subtrees:
                        for T5 in T4.subtrees:
                            for T6 in T5.subtrees:
                                treedata.append([T6.network.edges, T5.network.edges, T4.network.edges, T3.network.edges,
                                                 T2.network.edges, T1.network.edges])
                                types.append([T1.type, T2.type, T3.type, T4.type])
    elif n == 8:
        for T1 in subtrees:
            for T2 in T1.subtrees:
                for T3 in T2.subtrees:
                    for T4 in T3.subtrees:
                        for T5 in T4.subtrees:
                            for T6 in T5.subtrees:
                                for T7 in T6.subtrees:
                                    treedata.append(
                                        [T7.network.edges, T6.network.edges, T5.network.edges, T4.network.edges,
                                         T3.network.edges, T2.network.edges,
                                         T1.network.edges])
                                    types.append([T1.type, T2.type, T3.type, T4.type, T5.type])


    for i_t, tt in enumerate(treedata):
        matrix, treemat = create_treemat(tt)
        matrix = np.array(matrix,dtype=int)
        matrices.append(matrix)


    return matrices, types

def renumber_matrix(matrix,cdict):
    new_matrix = copy.deepcopy(matrix)
    for key in cdict:
        new_matrix[matrix == key] = cdict[key]
    return new_matrix

def get_all_matrices(input,dir):
    index = int(input[0])
    Trees = decompress_pickle(input[1])
    Tree_dict = decompress_pickle(input[2])
    isos  = Tree_dict[index]
    Treetypes = decompress_pickle(input[3])
    n = int(input[4])
    Tree_tot = Tree(Trees[index],Treetypes)


    matrices, types = get_matrices(Tree_tot.network, Treetypes,n)
    matrices = np.array(matrices)
    fi_name = "submats_" + str(n) + "_" + str(types[0][0]) + ".txt"
    fo = open(dir+fi_name, 'w')

    n_nodes = len(Trees[index].nodes)

    # outputmat = np.zeros([len(isos)*len(matrices),n_nodes,n_nodes],dtype=int)
    i_mat = 0
    for j in isos:

        X = nx.algorithms.isomorphism.GraphMatcher(Trees[index], Trees[j])
        X.is_isomorphic()
        new_matrices = renumber_matrix(matrices, X.mapping)

        for k_mat, mat in enumerate(new_matrices):

            fo.write("Matrix: " + str(i_mat+1) + "\n")
            fo.write("Type:   " + "+".join(types[k_mat]) + "\n")

            for row in mat:
                for col in row:
                    fo.write(str(col) + " ")
                fo.write("\n")
            i_mat += 1
            fo.write("\n")

    fo.close()


    return "Type " + str(types[0][0]) + " has " +  str(i_mat) + " matrices"

def decompress_pickle(file):
    data = bz2.BZ2File(file, 'rb')
    data = cPickle.load(data)
    return data

def create_labels(new_nodes):
    new_labels = []
    if not isinstance(np.array(new_nodes[0])[0], np.int32):
        for new_node in new_nodes:
            part1 = np.array(new_node[0])
            part2 = np.array(new_node[1])
            new = np.concatenate((np.setdiff1d(part1, part2), (np.setdiff1d(part2, part1))))
            all_vals = np.concatenate((part1, part2))
            cond = np.unique(all_vals[~np.isin(all_vals, new)])
            new_labels.append(np.concatenate((new, cond)))
    else:
        new_labels = new_nodes
    return new_labels

if __name__ == "__main__":
    # read data from input directory
    inputdir = "input/"
    # read data nodes specified in array, limited to the generated data in geninput.py
    # create all permutations and write to file
    for i in [5]:
        inputs = decompress_pickle(inputdir+'input'+str(i)+'.pbz2')
        run = 0
        for inp in inputs:
            input = [inp[0], inputdir+inp[1], inp[2], inputdir+inp[3], inp[4]]
            get_all_matrices(input, 'matrices/')

