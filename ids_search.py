"""
    Enter your details below:

    Name: yixi rao
    Student ID: u6826541
    Email: u6826541@anu.edu.au
"""

from typing import List

from game_engine.util import raise_not_defined
from search_problems import SearchProblem
from search_strategies import SearchNode
import frontiers

# import sys   
# sys.setrecursionlimit(100000)



def solve(problem: SearchProblem) -> List[str]:
    """See 2_implementation_notes.md for more details.

    Your search algorithms needs to return a list of actions that reaches the
    goal from the start state in the given problem. The elements of this list
    need to be one or more references to the attributes NORTH, SOUTH, EAST and
    WEST of the class Directions.
    """
    depth = 0
    while True:
        result = Depth_Limited_Search(problem, depth)
        if result[0] != "Cutoff":
            return result[1]
        depth = depth + 1
        
def Depth_Limited_Search(problem, limit):
    explored = dict([((x, y), False) 
                     for x in range(problem.width) 
                     for y in range(problem.height)])
    
    return Recursive_DLS(SearchNode(problem.get_initial_state()), problem, limit, explored)

def Recursive_DLS(node, problem, limit, explored):
    cutoff_occurred = False
    initial_state   = problem.get_initial_state()
    
    if problem.goal_test(node.state):
        parent_node = node.parent
        actions     = []
        actions.insert(0, node.action)
        
        while not parent_node.state.__eq__(initial_state):
            actions.insert(0, parent_node.action)
            parent_node = parent_node.parent
            
        return ("Solution", actions)
    
    elif node.depth == limit:
        return ("Cutoff", [])
    
    else:
        explored[node.state] = True
        frontier = []
        for successor, action, cost in problem.get_successors(node.state):
            if not (explored[successor]):                 
                child_node = SearchNode(successor, action, cost, node, node.depth + 1)
                frontier.append(child_node)
  
        for pop_node in frontier:
            new_explored = explored.copy()
            result       = Recursive_DLS(pop_node, problem, limit, new_explored)
            
            if result[0] == "Solution":
                return result
            elif result[0] == "Cutoff":
                cutoff_occurred = True
                    
        if cutoff_occurred:
            return ("Cutoff", [])
        else:
            return ("Failure", [])