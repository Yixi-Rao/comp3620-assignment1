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

def solve1(problem, heuristic):
    """
    Return a list of directions. See handout for more details.
    :param problem: the starting set up.
    :param heuristic: a heuristic function.
    :return: a list of directions.
    """

    # *** YOUR CODE HERE ***

    # ______________________SET UP
    from frontiers import PriorityQueue
    
    frontier        = PriorityQueue()
    explored        = set()
    action_list     = list()
    g               = dict()  # cost from s0 to current
    f               = dict()  # g + heuristic to goal
    previous_action = dict()

    # ____________________________INITIALIZE
    initial_state    = problem.get_initial_state()
    g[initial_state] = 0
    fv               = g[initial_state] + heuristic(initial_state, problem)
    f[initial_state] = fv
    back_start       = None # this variable is used for back tracking from the goal to the root. It will be defined as the goal once we hit the goal.
    
    frontier.push(initial_state, fv)
      
    # ITERATIONS________________________
    while not frontier.is_empty():
        node = frontier.peek()

        if problem.goal_test(node):
            back_start = node
            break

        node = frontier.pop()
        explored.add(node)

        for successor, action, cost in problem.get_successors(node):
            if successor not in explored:
                g[successor] = g[node] + cost
                fv           = g[successor] + heuristic(successor, problem)

                if successor not in f.keys():
                    previous_action[successor] = (node, action)
                    frontier.push(successor, fv)
                    f[successor] = fv

                elif f[successor] > fv:
                    frontier.change_priority(successor, fv)
                    f[successor] = fv
                    previous_action[successor] = (node, action)

    while back_start is not initial_state:
        action_list.append(previous_action[back_start][1])  
        back_start = previous_action[back_start][0]  
    return list(reversed(action_list))


def solve(problem: SearchProblem, heuristic: Callable) -> List[str]:
    """See 2_implementation_notes.md for more details.

    Your search algorithms needs to return a list of actions that reaches the
    goal from the start state in the given problem. The elements of this list
    need to be one or more references to the attributes NORTH, SOUTH, EAST and
    WEST of the class Directions.
    """
    # --------------------------------------------- initialization------------------------------------
    initial_state = problem.get_initial_state()
    initial_node  = SearchNode(initial_state)
    
    frontier      = frontiers.PriorityQueue()
    frontier_ele  = {initial_state : initial_node}
    explored      = set()
    
    frontier.push(initial_node, 0 + heuristic(initial_state, problem))
    if problem.goal_test(initial_state):
        return []
    # --------------------------------------------- find path------------------------------------------
    while not frontier.is_empty():
        node = frontier.pop()
        frontier_ele.pop(node.state)
        explored.add(node.state)
        
        for successor_state, action, cost in problem.get_successors(node.state): 
            InFrontier_node = frontier_ele[successor_state] if successor_state in frontier_ele else None # InFrontier_node = frontier.find(lambda x: x.state.__eq__(successor_state))
            
            if not (successor_state in explored or InFrontier_node != None):
                successor_node = SearchNode(successor_state, action, node.path_cost + cost, node, node.depth + 1)
                if problem.goal_test(successor_state):
                    parent_node = successor_node.parent
                    actions     = []
                    actions.insert(0, action)
                    while not parent_node.state.__eq__(initial_state):
                        actions.insert(0, parent_node.action)
                        parent_node = parent_node.parent
                    return actions
                
                frontier.push(successor_node, successor_node.path_cost + heuristic(successor_state, problem))
                frontier_ele[successor_state] = successor_node
                
            elif InFrontier_node != None and (node.path_cost + cost) < InFrontier_node.path_cost:
                frontier.change_priority(InFrontier_node, node.path_cost + cost + heuristic(successor_state, problem))
                InFrontier_node.parent = node 
                InFrontier_node.action = action
                InFrontier_node.depth  = node.depth + 1
                
