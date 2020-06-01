import os.path
import xml.etree.ElementTree as ET
import sys
import networkx as nx
import numpy as np
  
# Load the gedlibpy libraries 
libpath = "/home/lucas/Documents/stage_gedlibpy/gedlibpy"


# Equivalent to import librariesImport?
from ctypes import *
lib1 = cdll.LoadLibrary(libpath + "/" + 'lib/fann/libdoublefann.so')
lib2 = cdll.LoadLibrary(libpath + "/" + 'lib/libsvm.3.22/libsvm.so')
lib3 = cdll.LoadLibrary(libpath + "/" + 'lib/nomad/libnomad.so')
lib4 = cdll.LoadLibrary(libpath + "/" + 'lib/nomad/libsgtelib.so')

sys.path.append(libpath)
import gedlibpy
#import librariesImport

# My adapted modules
import misc
import edit_graph as eg


# Taken from example median.py
"""
    Replace a graph in script

    If old_id is -1, add a new graph to the environnemt

"""
def replace_graph_in_env(script, graph, old_id, label='median'):
    if(old_id > -1):
        script.clear_graph(old_id)
    new_id = script.add_graph(label)
    for i in graph.nodes():
        script.add_node(new_id,str(i),graph.nodes[i]) # !! strings are required bt gedlib
    for e in graph.edges:
        script.add_edge(new_id, str(e[0]),str(e[1]), {})
    script.init()
    script.set_method("IPFP", "")
    script.init_method()

    return new_id
    
"""    
    Compute new mappings
"""
def update_mappings(script,median_id,listID):
    med_distances = {}
    med_mappings = {}
    sod = 0
    for i in range(0,len(listID)):
        script.run_method(median_id,listID[i])
        med_distances[i] = script.get_upper_bound(median_id,listID[i])
        med_mappings[i] = script.get_forward_map(median_id,listID[i])
        sod += med_distances[i]
    return med_distances, med_mappings, sod

def calcul_Sij(all_mappings, all_graphs,i,j):
    s_ij = 0
    for k in range(0,len(all_mappings)):
        cur_graph =  all_graphs[k]
        cur_mapping = all_mappings[k]
        size_graph = cur_graph.order()
        if ((cur_mapping[i] < size_graph) and 
            (cur_mapping[j] < size_graph) and 
            (cur_graph.has_edge(cur_mapping[i], cur_mapping[j]) == True)):
                s_ij += 1
        
    return s_ij

# def update_median_nodes_L1(median,listIdSet,median_id,dataset, mappings):
#     from scipy.stats.mstats import gmean

#     for i in median.nodes():
#         for k in listIdSet:
#             vectors = [] #np.zeros((len(listIdSet),2))
#             if(k != median_id):
#                 phi_i = mappings[k][i]
#                 if(phi_i < dataset[k].order()):
#                     vectors.append([float(dataset[k].node[phi_i]['x']),float(dataset[k].node[phi_i]['y'])])

#         new_labels = gmean(vectors)
#         median.node[i]['x'] = str(new_labels[0])
#         median.node[i]['y'] = str(new_labels[1])
#     return median

def update_median_nodes(median,dataset,mappings):
    #update node attributes
    for i in median.nodes():
        nb_sub=0
        mean_label = {'x' : 0, 'y' : 0}
        for k in range(0,len(mappings)):
            phi_i = mappings[k][i]
            if ( phi_i < dataset[k].order() ):
                nb_sub += 1
                mean_label['x'] += 0.75*float(dataset[k].nodes[phi_i]['x'])
                mean_label['y'] += 0.75*float(dataset[k].nodes[phi_i]['y'])
        median.nodes[i]['x'] = str((1/0.75)*(mean_label['x']/nb_sub))
        median.nodes[i]['y'] = str((1/0.75)*(mean_label['y']/nb_sub))
    return median

def update_median_edges(dataset, mappings, median, cei=0.425,cer=0.425):
#for letter high, ceir = 1.7, alpha = 0.75
    size_dataset = len(dataset)
    ratio_cei_cer = cer/(cei + cer)
    threshold = size_dataset*ratio_cei_cer
    order_graph_median = median.order()
    for i in range(0,order_graph_median):
        for j in range(i+1,order_graph_median):
            s_ij = calcul_Sij(mappings,dataset,i,j)
            if(s_ij > threshold):
                median.add_edge(i,j)
            else:
                if(median.has_edge(i,j)):
                    median.remove_edge(i,j)
    return median



def compute_median_set(script,listID):
    'Returns the id in listID corresponding to median set'
    #Calcul median set
    N=len(listID)
    map_id_to_index = {}
    map_index_to_id = {}
    for i in range(0,len(listID)):
        map_id_to_index[listID[i]] = i
        map_index_to_id[i] = listID[i]
        
    distances = np.zeros((N,N))
    for i in listID:
        for j in listID:
            script.run_method(i,j)
            distances[map_id_to_index[i],map_id_to_index[j]] = script.get_upper_bound(i,j)

    median_set_index = np.argmin(np.sum(distances,0))
    sod = np.min(np.sum(distances,0))
    return median_set_index, sod

def compute_median(script, listID, dataset,verbose=False):
    """Compute a graph median of a dataset according to an environment

    Parameters

    script : An gedlib initialized environnement 
    listID (list): a list of ID in script: encodes the dataset 
    dataset (list): corresponding graphs in networkX format. We assume that graph
    listID[i] corresponds to dataset[i]

    Returns:
    A networkX graph, which is the median, with corresponding sod
    """
    if(verbose): print(len(listID))
    median_set_index, median_set_sod = compute_median_set(script, listID)
    sods = []
    #Ajout median dans environnement
    set_median = dataset[median_set_index].copy()
    median = dataset[median_set_index].copy()
    cur_med_id = replace_graph_in_env(script,median,-1)
    med_distances, med_mappings, cur_sod = update_mappings(script,cur_med_id,listID)
    sods.append(cur_sod)
    if(verbose): print("Current SOD: ", cur_sod)
    ite_max = 50
    old_sod = cur_sod * 2
    ite = 0
    epsilon = 0.001

    #best_median 
    while((ite < ite_max) and (np.abs(old_sod - cur_sod) > epsilon )):
        median = update_median_nodes(median,dataset, med_mappings)
        median = update_median_edges(dataset,med_mappings,median)

        cur_med_id = replace_graph_in_env(script,median,cur_med_id)
        med_distances, med_mappings, cur_sod = update_mappings(script,cur_med_id,listID)        
        
        sods.append(cur_sod)
        if(verbose): print("Current SOD: ", cur_sod)
        ite += 1
    return median, cur_sod, sods, set_median



### End median.py






##### FOR TESTING #####
if __name__ == "__main__":

    print_options = False
    test_two_graphs = False
    test_median = True

    # List of options
    if print_options:
        print("list_of_edit_cost_options")
        print(gedlibpy.list_of_edit_cost_options)
        print("list_of_method_options")
        print(gedlibpy.list_of_method_options)
        print("list_of_init_options")
        print(gedlibpy.list_of_init_options)
    
    if test_two_graphs:
        # Read a graph, edit it and measure distance
        g1, struct = misc.loadGXL("/home/lucas/Documents/stage_gedlibpy/stage/data/AP1_0000.gxl")
        params = eg.params_Letter()
        g2 = g1.copy()
        
        edits = [eg.edit_add_node,
                 eg.edit_add_node,
                 eg.edit_add_node,
                 eg.edit_add_edge,
                 eg.edit_add_edge,
                 eg.edit_add_edge,
                 eg.edit_transform_node,
                 eg.edit_transform_node,
                 eg.edit_transform_node,
                 eg.edit_transform_node,
                 eg.edit_transform_node,
                 eg.edit_delete_node
                ]
        eg.apply_edits(g2, edits, params)    
        
        dataset = [g1, g2]
        # Add the two graphs to the environment
        for graph in dataset :
            gedlibpy.add_nx_graph(graph, "A")

        listID = gedlibpy.get_all_graph_ids()
        gedlibpy.set_edit_cost("CONSTANT")
        gedlibpy.init()
        gedlibpy.set_method("IPFP", "")
        gedlibpy.init_method()
        
        g = listID[0]
        h = listID[1]
        gedlibpy.run_method(g,h)
        print("Node Map :\n", gedlibpy.get_node_map(g,h))
        print ("Upper Bound = " + str(gedlibpy.get_upper_bound(g,h)) + ", Lower Bound = " +str(gedlibpy.get_lower_bound(g,h)))
        
    if test_median:
        # Create a blob around a graph and calculate median
        path_orig = "/home/lucas/Documents/stage_gedlibpy/stage/data/test_blobs/orig/one_graph.xml"
        dataset_path = "/home/lucas/Documents/stage_gedlibpy/gedlibpy/include/gedlib-master/data/datasets/Letter/LOW"
        
        
        print("Loading...")
        centers,cl, struct = misc.loadFromXML(path_orig,dataset_path)
        
        # LETTER dataset
        params = eg.params_Letter()
        params["size"] = 3
        params["girth"] = lambda:5
        
        print("Making blobs...")
        graphs, classes = eg.make_blobs(centers,cl, params)
        # Fix labeling
        eg.relabel_nodes_to_int(graphs)

        # Now we have the graphs. Add to env 
        listID = []
        for g, c in zip(graphs, classes):
            listID.append(gedlibpy.add_nx_graph(g,c))        
        gedlibpy.set_edit_cost("LETTER")
        gedlibpy.init()
        gedlibpy.set_method("IPFP", "")
        gedlibpy.init_method()
        
        # Compute
        median, sod , sods_path, set_median = compute_median(gedlibpy,listID,graphs,verbose=True)
    
        print("SOD: ",sod)
        print("SOD path: ",sods_path)        
        
        """
        import matplotlib.pyplot as plt
        fig, ax = plt.subplots(1,2)
        misc.draw_Letter(centers[0], ax[0])
        ax[0].set_title("Center graph")
        misc.draw_Letter(median, ax[1])
        ax[1].set_title("Median graph")
        plt.show()
        """
        
        # Calculate distance between every graph
        all_graphs = graphs #+ centers
        all_graphs.append(median)
        
        all_classes = classes + cl #+ cl
        eg.relabel_nodes_to_int(all_graphs)
        
        gedlibpy.restart_env()
        
        listID = []
        for g, c in zip(all_graphs,all_classes):
            listID.append(gedlibpy.add_nx_graph(g,c))  
                  
        gedlibpy.set_edit_cost("LETTER")
        gedlibpy.init()
        gedlibpy.set_method("IPFP", "")
        gedlibpy.init_method()
        
        dist = np.zeros((len(listID),len(listID)))
        mappings = []
        for ii,i in enumerate(listID):
            aux = []
            for jj,j in enumerate(listID):
                gedlibpy.run_method(i,j)
                dist[ii,jj] = gedlibpy.get_upper_bound(i,j)
                aux.append(gedlibpy.get_forward_map(i,j)) 
            mappings.append(aux)
        print(dist)
        print(np.sum(dist, 0))
        print(mappings)
