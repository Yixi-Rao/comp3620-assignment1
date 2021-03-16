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
        else:
            print(result[2])
        depth = depth + 1
        
def Depth_Limited_Search(problem, limit):
    """
        this function will return the solution if it finds one or it will return cutoff when it reaches the depth limit.
        the return value is ("Cutoff" or "Solution" or "Faliure",
                             actions,
                             lower bound)
        
    """
    explored = set()
    
    return Recursive_DLS(SearchNode(problem.get_initial_state()), problem, limit, explored, 0)

def Recursive_DLS(node, problem, limit, explored, L_cost):
    """
        this function will return the solution if it finds one or it will return cutoff when it reaches the depth limit.
        the return value is ("Cutoff" or "Solution" or "Faliure",
                             actions,
                             lower bound)
        
    """
    cutoff_occurred = False
    initial_state   = problem.get_initial_state()
    # find the goal now we need to create the path
    if problem.goal_test(node.state):
        # find the path backwardly
        parent_node = node.parent
        actions     = []
        actions.insert(0, node.action)
        
        while not parent_node.state.__eq__(initial_state):
            actions.insert(0, parent_node.action)
            parent_node = parent_node.parent
            
        return ("Solution", actions, L_cost)
    # reach the limit
    elif node.depth == limit:
        return ("Cutoff", [], L_cost)
    # we should explore the map because we are not reach the depth limit
    else:
        explored.add(node.state)
        all_cost = 0
        for successor, action, cost in problem.get_successors(node.state):
            if successor not in explored:
                all_cost     = all_cost + 1                 
                child_node   = SearchNode(successor, action, cost, node, node.depth + 1)
                new_explored = set(explored) # we use a temporary explored set because we don't want to add some states that we are still going to explore 
                result       = Recursive_DLS(child_node, problem, limit, new_explored, 0)
                # after the recurisive call, the new_explored list is deleted, and the old one is the same as the before the function call
                all_cost = all_cost + result[2]
                if result[0] == "Solution":
                    return (result[0], result[1], all_cost)
                elif result[0] == "Cutoff":
                    cutoff_occurred = True                
        if cutoff_occurred:
            return ("Cutoff", [], all_cost)
        else:
            return ("Failure", [], all_cost)