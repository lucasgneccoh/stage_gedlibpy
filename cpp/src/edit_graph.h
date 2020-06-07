#include <iostream>
#include "/home/lucas/Documents/stage_gedlibpy/gedlib/gedlib/src/env/ged_env.hpp"
#include "/home/lucas/Documents/stage_gedlibpy/gedlib/gedlib/median/src/median_graph_estimator.hpp"
#include <random>

#ifndef EDIT_GRAPH_H
#define EDIT_GRAPH_H
 
void describe_graph(ged::ExchangeGraph<ged::GXLNodeID, ged::GXLLabel, ged::GXLLabel> exchange_graph);

std::map<std::string, std::map<std::string, std::vector<std::string>>> 
	get_graphs_structure(ged::GEDEnv<ged::GXLNodeID, ged::GXLLabel, ged::GXLLabel> &env);
 
void edit_add_node(ged::GEDEnv<ged::GXLNodeID, ged::GXLLabel, ged::GXLLabel> &env, 
		std::map<std::string, std::map<std::string, std::vector<std::string>>> structure);

void edit_add_edge(ged::GEDEnv<ged::GXLNodeID, ged::GXLLabel, ged::GXLLabel> &env, ged::GEDGraph::GraphID g_id,
		std::map<std::string, std::map<std::string, std::vector<std::string>>> structure, bool ignore_duplicates);

#endif

