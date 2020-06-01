# FROM misc.py
if __name__ == "__main__":
    """
    # Test loadGXL and saveGXL
        file = "/home/lucas/Documents/Stage/Lucas/data/molecule_1.gxl"
        dest = "/home/lucas/Documents/Stage/Lucas/data/molecule_1_after.gxl"
        dest2 = "/home/lucas/Documents/Stage/Lucas/data/molecule_1_after_2.gxl"
        g, struct = loadGXL(file)
        print("ORIGINAL")
        visual(g)
        print("Saving...")
        saveGXL(g, dest, struct)
        print("Done saving")
        print("Reading new file")
        g, struct = loadGXL(dest)
        print("NEW")
        visual(g)
        print("Saving...")
        saveGXL(g, dest2, struct)
        print("Done saving")
    """
# Test loadFromXML and saveToXML and make_blobs
    path_orig = "/home/lucas/Documents/Stage/Lucas/data/test_blobs/orig/A_and_L.xml"
    dataset_path = "/home/lucas/Documents/Stage/gedlibpy/include/gedlib-master/data/datasets/Letter/HIGH"
    
    import edit_graph as eg
    print("Loading...")
    centers,cl, struct = loadFromXML(path_orig,dataset_path)
    # LETTER dataset
    params = eg.params_Letter()
    params["size"] = 2
    params["girth"] = lambda:1
    print("Making blobs...")
    graphs, classes = eg.make_blobs(centers,cl, params)
    print("Saving graphs...")
    dest = "/home/lucas/Documents/Stage/Lucas/data/test_blobs/blobs/A_and_L_blobs.xml"
    saveToXML(graphs, classes, filename=dest, graph_dir=None, struct = struct)
    print("Done")
    print("Plotting results")
    import matplotlib.pyplot as plt
    centers,cl, struct = loadFromXML(path_orig,dataset_path)
    fig, ax = plt.subplots(2,3, figsize=(14,6))
    draw_Letter(centers[0], ax[0,0])
    draw_Letter(centers[1], ax[1,0])
    
    blobs,cl, struct = loadFromXML(dest)
    draw_Letter(blobs[0], ax[0,1])
    draw_Letter(blobs[1], ax[0,2])
    draw_Letter(blobs[2], ax[1,1])
    draw_Letter(blobs[3], ax[1,2])
    plt.show()
    
    
#############################################################################
# From edit_graph.py   
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
        filename = "/home/lucas/Documents/stage_gedlibpy/gedlibpy/include/gedlib-master/data/datasets/Letter/HIGH/A_and_L.cxl"
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
    
