import os.path
import xml.etree.ElementTree as ET
import sys
import networkx as nx
import numpy as np
   
##### All graphs are treated as networkx objects
##### EDIT FUNCTIONS #####
def edit_add_node(graph, params):
    attrs = params['node_attr']
    label = graph.number_of_nodes()
    while label in list(graph.nodes): label += 1
    graph.add_node(label)
    for a in attrs:
        func = attrs[a]
        graph.nodes[label][a] = func(graph, None)
        
def edit_add_edge(graph, params):
    non_e = list(nx.classes.function.non_edges(graph))
    if len(non_e)==0: return
    attrs = params['edge_attr']
    pos = np.random.randint(len(non_e))
    e = non_e[pos]
    graph.add_edge(e[0], e[1])
    for a in attrs:
        func = attrs[a]
        graph.edges[e[0], e[1]][a] = func(graph, e)
    
def edit_delete_node(graph, params):
    if graph.number_of_nodes()==0: return
    pos = np.random.randint(graph.number_of_nodes())
    n = list(graph.nodes)[pos]
    graph.remove_node(n)
        
def edit_delete_edge(graph, params):
    if graph.number_of_edges()==0: return
    pos = np.random.randint(graph.number_of_edges())
    e = list(graph.edges)[pos]
    graph.remove_edge(e[0],e[1])

def edit_transform_node(graph, params):
    # Take an existing node and modify its attributes
    if graph.number_of_nodes()==0: return
    pos = np.random.randint(graph.number_of_nodes())
    attrs = params["node_attr"]
    n = list(graph.nodes)[pos]
    # See if params contains the functions to calculate the values
    for a in attrs:
        func = attrs[a]
        graph.nodes[n][a] = func(graph, graph.nodes[n][a])
        
    
def edit_transform_edge(graph,params):
    if graph.number_of_edges()==0: return
    # Take an existing node and modify its attributes
    pos = np.random.randint(graph.number_of_edges())
    attrs = params["edge_attr"]
    e = list(graph.edges)[pos]
    # See if params contains the functions to calculate the values
    for a in attrs:
        func = attrs[a]
        graph.edges[e][a] = func(graph, graph.edges[e][a])

##### PARAMS for datasets #####
def params_Letter():
    # LETTER dataset
    params = dict()
    def func_unif_coord(graph, value, coord):
        if value is None:
        # Uniform over existing range for new nodes
            values = list(map(float,nx.get_node_attributes(graph,coord).values()))
            if values: 
                m, M = min(values), max(values)
            else:
                m, M = 0, 3
            return str(round(np.random.uniform(low=m, high=M),4))
        else:
        # Normal centered at existing coordinate. std=1
            return str(round(np.random.normal(loc=float(value)),4))
            
    params['node_attr'] = {'x': lambda g, v: func_unif_coord(g, v, 'x'), 'y': lambda g, v: func_unif_coord(g, v, 'y')}
    params['edge_attr'] = {}

    params["size"] = 20
    params["girth"] = lambda : np.random.randint(1,100)
    params["operations"] = [edit_add_node, edit_add_edge, edit_delete_node, edit_delete_edge, edit_transform_node, edit_transform_edge]
    # Uniform probability
    params["probability"] = None
    return params
 
##### UTILS FUNCTIONS #####

def apply_edits(g, operations, params):
    for op in operations: op(g, params)
    
def relabel_nodes_to_int(graphs):
    for g in graphs:
        pass
        # TODO: add relabeling to integers
        
    
"""
    Given the files in gxl format, read them as the centers of the blobs, then create blobs around each center by making random edit operations. The structure of the result is controlled via the parameter 'params'
    
    centers: networkx graphs to use as centers of blobs
    
    cl: vector of classes
    
    params: dictionary to introduce all the options
        size: the size of each blob
        girth: An integer function with no parameters giving the number of edit operations to perform for each generated graph of the blob
            - For constant girth use function lambda:const
        operations: a list of functions that perform transformations in a graph. This operations must take change the graph received inplace. Also, each operation must receive as input the graph and params, even if they are not used (for compatibility)
        probability: a list of float or integer giving the probability of applying each operation. If None then uniform probability is used
        node_attr: the attributes of a node to add/transform. Must be a dictionary having as keys the name of the attribute and as value a function to generate or change the attribute in the add/transform edit operations. This functions must receive as input the graph and the current value for the attribute, even if it doesnt use it) 
        edge_attr: the attributes of an edge to add/transform. Must be a dictionary having as keys the name of the attribute and as value a function to generate or change the attribute in the add/transform edit operations. This functions must receive as input the graph and the current value for the attribute, even if it doesnt use it) 
"""  
def make_blobs(centers, cl, params):
    size = params["size"]
    girth = params["girth"]
    operations = params["operations"]
    probability = params["probability"]
    if probability is None:
        probability = [1 for _ in operations]

    if sum(probability) != 1:
        s = sum(probability)
        probability = [p/s for p in probability]
    res_graphs = []
    res_classes = []
    
    #Create blob for around each center
    for g, cl in zip(centers, cl):
        for i in range(size):
            base = g.copy()
            for j in range(girth()):
                op = np.random.choice(operations,size=1,replace=True, p=probability)[0]
                op(base, params)
                
            res_graphs.append(base)
            res_classes.append(cl)
            
    return res_graphs, res_classes
 



##### FOR TESTING #####
if __name__ == "__main__":
    
    # Testing parts
    test_edit_functions = False
    test_make_blobs = True
    
    
    
    import misc
    """
    TEST: edit functions
    """
    if test_edit_functions:
        filename = "/home/lucas/Documents/Stage/gedlibpy/include/gedlib-master/data/datasets/Letter/HIGH/A_and_L.cxl"
        graphs,classes, _ = misc.loadFromXML(filename)
        graph = graphs[0]
        
        # DEF params for edit operations 
        # LETTER dataset
        params = params_Letter()
        params["size"] = 10
        # TEST EDIT FUNCTIONS
        misc.visual(graph)
        
        print("...... Transform .......")
        #edit_add_node(graph, params)
        #edit_add_edge(graph, params)
        #edit_delete_node(graph, params)
        #edit_delete_edge(graph, params)
        edit_transform_node(graph, params)
        #edit_transform_edge(graph, params)
        
        misc.visual(graph)
        
    
    """
    TEST: make_blobs
    """
    if test_make_blobs:
        path_orig = "/home/lucas/Documents/stage_gedlibpy/stage/data/test_blobs/orig/test_blobs.xml"
        dataset_path = "/home/lucas/Documents/stage_gedlibpy/gedlibpy/include/gedlib-master/data/datasets/Letter/LOW"
        
        
        print("Loading...")
        centers,cl, struct = misc.loadFromXML(path_orig,dataset_path)
        
        # LETTER dataset
        params = params_Letter()
        params["size"] = 2
        params["girth"] = lambda:1
        
        print("Making blobs...")
        graphs, classes = make_blobs(centers,cl, params)
        
        print("Saving graphs...")
        dest = "/home/lucas/Documents/stage_gedlibpy/stage/data/test_blobs/blobs/result_blobs.xml"
        misc.saveToXML(graphs, classes, filename=dest, graph_dir=None, struct = struct)
        print("Done")
        
        print("Plotting results")
        import matplotlib.pyplot as plt
        
        centers,cl, struct = misc.loadFromXML(path_orig,dataset_path)
        fig, ax = plt.subplots(2,3, figsize=(14,6))
        misc.draw_Letter(centers[0], ax[0,0])
        ax[0,0].set_title("Original graphs")
        ax[0,0].set_ylabel(cl[0])
        ax[1,0].set_ylabel(cl[1])
        misc.draw_Letter(centers[1], ax[1,0])
        
        blobs,cl, struct = misc.loadFromXML(dest)
        misc.draw_Letter(blobs[0], ax[0,1])
        misc.draw_Letter(blobs[1], ax[0,2])
        misc.draw_Letter(blobs[2], ax[1,1])
        misc.draw_Letter(blobs[3], ax[1,2])
        ax[0,1].set_title("First simulated")
        ax[0,2].set_title("Second simulated")
        plt.show()

