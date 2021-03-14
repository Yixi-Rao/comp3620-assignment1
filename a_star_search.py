"""
    Enter your details below:

    Name: yixi rao
    Student ID: u6826541
    Email: u6826541@anu.edu.au
"""

from typing import Callable, List

from game_engine.util import raise_not_defined
from search_problems import SearchProblem
from search_strategies import SearchNode
import frontiers

  


def solve1(problem: SearchProblem, heuristic: Callable) -> List[str]:
    """See 2_implementation_notes.md for more details.

    Your search algorithms needs to return a list of actions that reaches the
    goal from the start state in the given problem. The elements of this list
    need to be one or more references to the attributes NORTH, SOUTH, EAST and
    WEST of the class Directions.
    """
    # --------------------------------------------- initialization------------------------------------
    initial_state    = problem.get_initial_state()
    initial_position = Node_position(initial_state, problem)
    initial_node     = SearchNode(initial_state)
    
    frontier         = frontiers.PriorityQueue()
    explored         = set()
    
    frontier.push(initial_node, 0 + heuristic(initial_state, problem))
    
    if problem.goal_test(initial_state):
        return None
    # --------------------------------------------- find path------------------------------------------
    while not frontier.is_empty():
        
        node = frontier.pop()
        explored.add(node.state)
        
        for successor_state, action, cost in problem.get_successors(node.state):
            successor_pos   = Node_position(successor_state, problem)      
            InFrontier_node = frontier.find(lambda x: Node_position(x.state, problem).__eq__(successor_pos))

            if not (successor_state in explored or InFrontier_node != None):
                successor_node = SearchNode(successor_state, action, node.path_cost + cost, node, node.depth + 1)
                if problem.goal_test(successor_state):
                    
                    parent_node = successor_node.parent
                    actions = []
                    actions.insert(0,action)
                    while not Node_position(parent_node.state, problem).__eq__(initial_position):
                        actions.insert(0,parent_node.action)
                        parent_node = parent_node.parent
                    return actions
                print(successor_pos)
                frontier.push(successor_node, successor_node.path_cost + heuristic(successor_state, problem))
            elif InFrontier_node != None and (node.path_cost + cost) < InFrontier_node.path_cost:
                print("//////////////////////////")
                frontier.change_priority(InFrontier_node, node.path_cost + cost + heuristic(successor_state, problem))
                InFrontier_node.parent = node 
                InFrontier_node.action = action
                InFrontier_node.depth  = node.depth + 1
                
# def Node_position(state, problem):
#     return state if type(problem).__name__ == "PositionSearchProblem" else state[0]    
