from game_engine.state import State
import layout
import search_problems
import brfs_search
import ids_search
import a_star_search
import heuristics
import minimax_agent

env_layout = layout.try_to_load("search_layouts/aiMultiSearch.lay")
state      = State(layout = env_layout) 

multi_position_prob = search_problems.MultiplePositionSearchProblem(state) 
# a_star_search.solve(multi_position_prob,heuristics.manhattan_heuristic)

print(heuristics.every_bird_heuristic(multi_position_prob.initial_state, multi_position_prob))