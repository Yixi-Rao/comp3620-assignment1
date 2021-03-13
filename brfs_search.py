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
    initial_state = problem.get_initial_state()
    initial_node  = SearchNode(initial_state)
    if problem.goal_test(initial_state):
        return []
    frontier = frontiers.Queue()
    frontier.push(initial_node)
    explored = dict([((x, y), False) 
                     for x in range(problem.width) 
                     for y in range(problem.height)])
    while True:
        if frontier.is_empty():
            return []
        node = frontier.pop()
        explored[node.state] = True
        for successor, action, cost in problem.get_successors(node.state):
            child_node = SearchNode(successor, action, cost, node, node.depth + 1)
            if not (explored[successor] or frontier.find(lambda x: x.state.__eq__(successor)) != None):
                if problem.goal_test(successor):
                    parent_node = child_node.parent
                    actions = []
                    actions.insert(0,action)
                    while not parent_node.state.__eq__(initial_state):
                        actions.insert(0,parent_node.action)
                        parent_node = parent_node.parent
                    return actions
                frontier.push(child_node)

