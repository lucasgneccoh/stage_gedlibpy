#include "edit_graph.h"

void describe_graph(ged::ExchangeGraph<ged::GXLNodeID, ged::GXLLabel, ged::GXLLabel> exchange_graph){
	
	std::cout<<"NODES:\n";
	for (std::size_t i{0}; i < exchange_graph.num_nodes; i++) {
		// TODO: for sobre los labels
		std::cout << "Node " << i <<":\n";
		for(auto const &l : exchange_graph.node_labels.at(i)){
			std::cout<<"\t"<<l.first<<": " <<l.second << "\n";
		}
		
	}
	std::cout<<"EDGES:\n";
	for (std::size_t i{0}; i < exchange_graph.num_nodes; i++) {
		for (std::size_t j{i + 1}; j < exchange_graph.num_nodes; j++) {
			if (exchange_graph.adj_matrix[i][j] == 1) {
				std::cout << "Edge:  " << i << " -- " << j << "\n";
				for(auto const &e : exchange_graph.edge_labels.at(std::make_pair(i, j))){
					std::cout<<"\t"<<e.first<<": " <<e.second << "\n";
				} 
			}
		}
	}
}

std::map<std::string, std::map<std::string, std::vector<std::string>>> 
	get_graphs_structure(ged::GEDEnv<ged::GXLNodeID, ged::GXLLabel, ged::GXLLabel> &env){

	std::map<std::string, std::vector<std::string>> node_attr;
	std::map<std::string, std::vector<std::string>> edge_attr;

	ged::ExchangeGraph<ged::GXLNodeID, ged::GXLLabel, ged::GXLLabel> g;
	std::pair<ged::GEDGraph::GraphID, ged::GEDGraph::GraphID> graph_ids = env.graph_ids();
	for (ged::GEDGraph::GraphID g_id{graph_ids.first}; g_id<graph_ids.second; g_id++){
		g = env.get_graph(g_id);
		for (std::size_t i{0}; i < g.num_nodes; i++) {
			for(auto l : g.node_labels.at(i)){
				if(node_attr.count(l.first)==0){
					node_attr.emplace(std::make_pair(l.first, std::vector<std::string>()));
				}		
				node_attr.at(l.first).emplace_back(l.second);
			}
		}
		for (std::size_t i{0}; i < g.num_nodes; i++) {
			for (std::size_t j{i + 1}; j < g.num_nodes; j++) {
				if (g.adj_matrix[i][j] == 1) {				
					for(auto e : g.edge_labels.at(std::make_pair(i, j))){
						if(edge_attr.count(e.first)==0){
							edge_attr.emplace(std::make_pair(e.first, std::vector<std::string>()));
						}
						edge_attr.at(e.first).emplace_back(e.second);
					} 
				}
			}
		}
	}
	std::map<std::string, std::map<std::string, std::vector<std::string>>> result;
	result.emplace(std::make_pair("node_attr", node_attr));
	result.emplace(std::make_pair("edge_attr", edge_attr));	
	return result;
}

void edit_add_node(ged::GEDEnv<ged::GXLNodeID, ged::GXLLabel, ged::GXLLabel> &env, ged::GEDGraph::GraphID g_id,
		ged::GXLNodeID node_id, std::map<std::string, std::map<std::string, std::vector<std::string>>> structure){
	// We create the UserNodeLabel (GXLLabel in our case) and use the existing env.add_node method
	
	ged::GXLLabel label;

	std::random_device rd;
	std::mt19937 gen(rd());
	std::uniform_int_distribution<int> distr(0, 1);

	for(auto const attr : structure.at("node_attr")){
		distr = std::uniform_int_distribution<int>(0, attr.second.size()-1);		
		label.emplace(std::make_pair(attr.first, attr.second.at(distr(gen))));
	}
	env.add_node(g_id, node_id, label);
}


void edit_add_edge(ged::GEDEnv<ged::GXLNodeID, ged::GXLLabel, ged::GXLLabel> &env, ged::GEDGraph::GraphID g_id,
		std::map<std::string, std::map<std::string, std::vector<std::string>>> structure, bool ignore_duplicates){
	// We create the UserNodeLabel (GXLLabel in our case) and use the existing env.add_node method
	
	ged::GXLLabel label;
	std::random_device rd;
	std::mt19937 gen(rd());
	std::uniform_int_distribution<std::size_t> distr(0, 1);

	for(auto const attr : structure.at("edge_attr")){
		distr = std::uniform_int_distribution<std::size_t>(0, attr.second.size()-1);
		label.emplace(std::make_pair(attr.first, attr.second.at(distr(gen))));
	}

	ged::ExchangeGraph<ged::GXLNodeID, ged::GXLLabel, ged::GXLLabel> exchange_graph{env.get_graph(g_id, true, false, false)};
	std::vector<std::pair<std::size_t, std::size_t>> non_edges;

	for (std::size_t i{0}; i < exchange_graph.num_nodes; i++) {
		for (std::size_t j{i + 1}; j < exchange_graph.num_nodes; j++) {
			if (exchange_graph.adj_matrix[i][j] == 0) {			
				non_edges.emplace_back(std::make_pair(i,j));
			}
		}
	}
	distr = std::uniform_int_distribution<std::size_t>(0, non_edges.size()-1);
	std::pair<std::size_t, std::size_t> e_add = non_edges.at(distr(gen));

	ged::GXLNodeID from_id = exchange_graph.original_node_ids.at(e_add.first);
	ged::GXLNodeID to_id = exchange_graph.original_node_ids.at(e_add.second);

	env.add_edge(g_id, from_id, to_id, label,ignore_duplicates);
}

void edit_transform_node(ged::GEDEnv<ged::GXLNodeID, ged::GXLLabel, ged::GXLLabel> &env, ged::GEDGraph::GraphID g_id,
		ged::GXLNodeID node_id, std::map<std::string, std::map<std::string, std::vector<std::string>>> structure){

	ged::ExchangeGraph<ged::GXLNodeID, ged::GXLLabel, ged::GXLLabel> exchange_graph{env.get_graph(g_id, true, false, false)};

	std::random_device rd;
	std::mt19937 gen(rd());
	std::uniform_int_distribution<std::size_t> distr(0, exchange_graph.num_nodes-1);
	std::size_t sel_node = distr(gen);

	for(auto const attr : structure.at("node_attr")){
		distr = std::uniform_int_distribution<int>(0, attr.second.size()-1);		
		exchange_graph.node_labels.at(sel_node).emplace(attr.first, attr.second.at(distr(gen)));
	}

	env.load_exchange_graph(exchange_graph, g_id, Options::ExchangeGraphType::ADJ_MATRIX ,env.get_graph_name(g_id) , env.get_graph_class(g_id));
}


void edit_transform_edge(ged::GEDEnv<ged::GXLNodeID, ged::GXLLabel, ged::GXLLabel> &env, ged::GEDGraph::GraphID g_id,
		std::map<std::string, std::map<std::string, std::vector<std::string>>> structure, bool ignore_duplicates){
	
	ged::ExchangeGraph<ged::GXLNodeID, ged::GXLLabel, ged::GXLLabel> exchange_graph{env.get_graph(g_id, true, false, true)};

	std::random_device rd;
	std::mt19937 gen(rd());
	std::uniform_int_distribution<int> distr(0, exchange_graph.num_edges-1);
	sel_edge = distr(gen);
	std::size_t cont{0};
	std::pair<std::pair<std::size_t, std::size_t>, UserEdgeLabel> edge;
	for(std::list<std::pair<std::pair<std::size_t, std::size_t>::iterator it = exchange_graph.edge_list.begin();
		it != exchange_graph.edge_list.end(), it++){
		if(cont==sel_edge){
			edge = *it;
			break;
		}
		cont++;
	}

	// From here ----------------------------------------------------
	// falta transformar el eje (los label) y recargar el grafo
	for(auto const attr : structure.at("edge_attr")){
		distr = std::uniform_int_distribution<std::size_t>(0, attr.second.size()-1);
		exchange_graph.edge_list.at(sel_edj).emplace(attr.first, attr.second.at(distr(gen)));
	}

	ged::ExchangeGraph<ged::GXLNodeID, ged::GXLLabel, ged::GXLLabel> exchange_graph{env.get_graph(g_id, true, false, false)};
	std::vector<std::pair<std::size_t, std::size_t>> non_edges;

	for (std::size_t i{0}; i < exchange_graph.num_nodes; i++) {
		for (std::size_t j{i + 1}; j < exchange_graph.num_nodes; j++) {
			if (exchange_graph.adj_matrix[i][j] == 0) {			
				non_edges.emplace_back(std::make_pair(i,j));
			}
		}
	}
	distr = std::uniform_int_distribution<std::size_t>(0, non_edges.size()-1);
	std::pair<std::size_t, std::size_t> e_add = non_edges.at(distr(gen));

	ged::GXLNodeID from_id = exchange_graph.original_node_ids.at(e_add.first);
	ged::GXLNodeID to_id = exchange_graph.original_node_ids.at(e_add.second);

	env.load_exchange_graph(exchange_graph, g_id, Options::ExchangeGraphType::ADJ_MATRIX ,env.get_graph_name(g_id) , env.get_graph_class(g_id));
}




// TAKEN FROM EXAMPLES TO MAKE THE CODE WORK
std::unordered_set<std::string> irrelevant_node_attributes(const std::string & dataset) {
	std::unordered_set<std::string> irrelevant_attributes;
	if (dataset == "AIDS") {
		irrelevant_attributes.insert({"x", "y", "symbol", "charge"});
	}
	return irrelevant_attributes;
}

bool constant_node_costs(const std::string & dataset) {
	if (dataset == "Letter") {
		return false;
	}
	else {
		return true;
	}
}

int main(int argc, char* argv[]){

	std::cout<<"MAIN\n";

	/* Test # 1. Make GEDLIB work, manipulate a graph and calculate a median for a known dataset
	 * 
	 * Works

	std::cout<<"--------------START-----------------\n";
	
	std::string gedlib_root("/home/lucas/Documents/stage_gedlibpy/gedlib/gedlib");
	std::string project_root("/home/lucas/Documents/stage_gedlibpy/stage/cpp");

	std::cout<<"--------------LOAD GRAPHS-----------------\n";
	
	
	ged::GEDEnv<ged::GXLNodeID, ged::GXLLabel, ged::GXLLabel> env;

	std::string dataset{"Letter"};
	std::string class_test{"A"};
	std::string extra_dir{"/LOW"};

	std::string collection_file(project_root + "/data/collections/" + dataset + "_" + class_test +".xml");
	std::string graph_dir(gedlib_root + "/data/datasets/" + dataset + extra_dir);

	std::cout<<"Dataset: "<<dataset<<"\n";
	std::cout<<"Collection file: "<<collection_file<<"\n";
	std::cout<<"Graph directory: "<<graph_dir<<"\n";

	
	env.set_edit_costs(ged::Options::EditCosts::CONSTANT, {});
	
	
	std::vector<ged::GEDGraph::GraphID> graph_ids(env.load_gxl_graphs(graph_dir, collection_file,
			ged::Options::GXLNodeEdgeType::LABELED, ged::Options::GXLNodeEdgeType::LABELED, irrelevant_node_attributes(dataset)));
	ged::GEDGraph::GraphID median_id{env.add_graph("median")};
	env.init(ged::Options::InitType::EAGER_WITHOUT_SHUFFLED_COPIES);
	
	std::string ipfp_options("--threads 6 --initial-solutions 5 --initialization-method RANDOM");
	env.set_method(ged::Options::GEDMethod::IPFP, ipfp_options);



	std::cout<<"--------------DESCRIBE GRAPH-----------------\n";
	describe_graph(env.get_graph(graph_ids.at(0), true, false, false));

	
	std::cout<<"--------------FIND MEDIAN FOR LOADED GRAPHS-----------------\n";
	
	// Set up the estimator.
	ged::MedianGraphEstimator<ged::GXLNodeID, ged::GXLLabel, ged::GXLLabel> mge(&env, constant_node_costs(dataset));
	mge.set_refine_method(ged::Options::GEDMethod::IPFP, "--threads 6 --initial-solutions 10 --ratio-runs-from-initial-solutions .5");
	

	// Varied estimator parameters.
	std::vector<std::string> init_types{"RANDOM", "MAX", "MIN", "MEAN", "MEDOID"};
	std::vector<std::string> nums_inits{"16", "1", "2", "4", "8", "32"};

	// Varied algorithm parameters.
	std::vector<ged::Options::GEDMethod> algos{ged::Options::GEDMethod::IPFP, ged::Options::GEDMethod::BRANCH_FAST, ged::Options::GEDMethod::REFINE};
	std::vector<std::string> algo_options_suffixes{" --initial-solutions 10 --ratio-runs-from-initial-solutions .5", "", " --initial-solutions 10 --ratio-runs-from-initial-solutions .5"};

	// Select the GED algorithm.
	std::size_t algo_id{0};

	std::string init_type = "RANDOM";

	std::string num_inits = "16";


	ged::Options::GEDMethod algo{algos.at(algo_id)};
	std::string algo_options("--threads 6" + algo_options_suffixes.at(algo_id));
	
	std::string mge_options("--time-limit 600 --stdout 0 --init-type " + init_type);
	if (init_type != "RANDOM" and num_inits != "1") {
	}
	else {
		std::random_device rng;
		mge_options += " --random-inits " + num_inits + " --randomness PSEUDO --seed " + std::to_string(rng());
	}


	mge.set_options(mge_options);
	mge.set_init_method(algo, algo_options);
	mge.set_descent_method(algo, algo_options);

	// Run the estimator.
	mge.run(graph_ids, median_id);

	// Write the results.
	std::cout << "\n Algo details" << init_type << ", " << num_inits << ", " << algo;
	std::cout << "\n Runtime" << mge.get_runtime() << ", " << mge.get_runtime(ged::Options::AlgorithmState::INITIALIZED) << ", " << mge.get_runtime(ged::Options::AlgorithmState::CONVERGED) <<"\n";
	std::cout << "\n SOD" << mge.get_sum_of_distances() << ", " << mge.get_sum_of_distances(ged::Options::AlgorithmState::INITIALIZED) << ", " << mge.get_sum_of_distances(ged::Options::AlgorithmState::CONVERGED)<<"\n";

	std::cout<<"--------------END-----------------\n";
	*/


	/* Test # 2 work with library edit_graph
	 *	Get graph structure and domain - works
	 *	Edit graph operations
	 *	Make_blobs
	 * 	Calculate median for blob
	 *	Calculate ged between blob and center, blob and median, median and center
	 *
	*/

	std::cout<<"--------------START-----------------\n";
	
	std::string gedlib_root("/home/lucas/Documents/stage_gedlibpy/gedlib/gedlib");
	std::string project_root("/home/lucas/Documents/stage_gedlibpy/stage/cpp");

	std::cout<<"--------------LOAD GRAPHS-----------------\n";
	
	
	ged::GEDEnv<ged::GXLNodeID, ged::GXLLabel, ged::GXLLabel> env;

	std::string dataset{"Letter"};
	std::string class_test{"A"};
	std::string extra_dir{"/LOW"};

	std::string collection_file(project_root + "/data/collections/" + dataset + "_" + class_test +".xml");
	std::string graph_dir(gedlib_root + "/data/datasets/" + dataset + extra_dir);

	std::cout<<"Dataset: "<<dataset<<"\n";
	std::cout<<"Collection file: "<<collection_file<<"\n";
	std::cout<<"Graph directory: "<<graph_dir<<"\n";

	
	env.set_edit_costs(ged::Options::EditCosts::CONSTANT, {});
	
	
	std::vector<ged::GEDGraph::GraphID> graph_ids(env.load_gxl_graphs(graph_dir, collection_file,
			ged::Options::GXLNodeEdgeType::LABELED, ged::Options::GXLNodeEdgeType::LABELED, irrelevant_node_attributes(dataset)));
	ged::GEDGraph::GraphID median_id{env.add_graph("median")};
	env.init(ged::Options::InitType::EAGER_WITHOUT_SHUFFLED_COPIES);

	
	std::map<std::string, std::map<std::string, std::vector<std::string>>> 
	structure = get_graphs_structure(env);

	std::cout<<"--------------GRAPH STRUCTURE-----------------\n";
	for(auto t: structure){
		std::cout<<t.first<<"\n";
		for(auto att: structure.at(t.first)){
			std::cout<<"\t"<<att.first<<":\n\t\t";
			for(std::size_t i{0}; i<5; i++){
				std::cout<<att.second.at(i)<<" ";
			}
			std::cout<<"\n";
		}
	}

	/*
	std::cout<<"--------------EDIT_ Add Node-----------------\n";
	std::cout<<"Before edit\n";
	describe_graph(env.get_graph(0, true, true, true));
	edit_add_node(env, 0, "new_node_1", structure);
	std::cout<<"After edit\n";
	describe_graph(env.get_graph(0, true, true, true));
	*/
	
	std::cout<<"--------------EDIT_ Add Edge-----------------\n";
	std::cout<<"Before edit\n";
	describe_graph(env.get_graph(0, true, true, true));
	edit_add_edge(env, 0, structure, false);
	std::cout<<"After edit\n";
	describe_graph(env.get_graph(0, true, true, true));
}



