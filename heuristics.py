# heuristics.py
# ----------------
# COMP3620/6320 Artificial Intelligence
# The Australian National University
# For full attributions, see attributions.txt on Wattle at the end of the course

""" This class contains heuristics which are used for the search procedures that
    you write in search_strategies.py.

    The first part of the file contains heuristics to be used with the algorithms
    that you will write in search_strategies.py.

    In the second part you will write a heuristic for Q4 to be used with a
    MultiplePositionSearchProblem.
"""

from typing import Tuple

from search_problems import (MultiplePositionSearchProblem,
                             PositionSearchProblem)
import frontiers
Position = Tuple[int, int]
YellowBirds = Tuple[Position]
State = Tuple[Position, YellowBirds]

# -------------------------------------------------------------------------------
# A set of heuristics which are used with a PositionSearchProblem
# You do not need to modify any of these.
# -------------------------------------------------------------------------------


def null_heuristic(pos: Position, problem: PositionSearchProblem) -> int:
    """The null heuristic. It is fast but uninformative. It always returns 0"""

    return 0


def manhattan_heuristic(pos: Position, problem: PositionSearchProblem) -> int:
    """The Manhattan distance heuristic for a PositionSearchProblem."""

    return abs(pos[0] - problem.goal_pos[0]) + abs(pos[1] - problem.goal_pos[1])


def euclidean_heuristic(pos: Position, problem: PositionSearchProblem) -> float:
    """The Euclidean distance heuristic for a PositionSearchProblem"""

    return ((pos[0] - problem.goal_pos[0]) ** 2 + (pos[1] - problem.goal_pos[1]) ** 2) ** 0.5


# Abbreviations
null = null_heuristic
manhattan = manhattan_heuristic
euclidean = euclidean_heuristic

# -------------------------------------------------------------------------------
# You have to implement the following heuristics for Q4 of the assignment.
# It is used with a MultiplePositionSearchProblem
# -------------------------------------------------------------------------------

# You can make helper functions here, if you need them


def bird_counting_heuristic(state: State,
                            problem: MultiplePositionSearchProblem) -> float:
    position, yellow_birds = state
    heuristic_value = 0

    """ *** YOUR CODE HERE *** """

    return len(yellow_birds)


bch = bird_counting_heuristic

        
class My_DisjointSet:
    '''
    this disjoint set will be used when we want to calculate a minimal spinning tree value
    DisjointSet reference: https://blog.csdn.net/weixin_44193909/article/details/88774567
    '''
    def __init__(self, l):
        self.dict = {}
        for e in l:
            self.dict[e] = e
    
    def find(self, ele):
        '''return the group of the 'ele' element belonged'''
        if self.dict[ele] != ele:
            self.dict[ele] = self.find(self.dict[ele])
        return self.dict[ele]
    
    def union_two_set(self, ele1, ele2):
        '''union two groups into one group, ele1 and ele2 are the group number'''
        self.dict[ele2] = self.dict[ele1]
        
    def same_group(self, v1, v2):
        '''check whether the two values is in the same group'''
        return self.find(v1) == self.find(v2)
        

def every_bird_heuristic(state: State,
                         problem: MultiplePositionSearchProblem) -> float:
    """This heuristic will return the minimal spinning tree value, and the tree vertice include the red bird and all the yellow birds
       and it is admissible because the minimal spinning tree value never overestimate the real cost and it is dominate the null and bch. the spnning tree algorithm is Kruskal
       algorithm
    """
    
    position, yellow_birds = state
    heuristic_value = 0

    """ *** YOUR CODE HERE *** """
    node_set         = set(yellow_birds)         # vertice set
    edge_weight_dist = {}                        # a 'edge : weight' dictionary
    edge_queue       = frontiers.PriorityQueue() # PriorityQueue of the minimum value of edges
    edge_used        = set()                     # used to generate the edges
    node_set.add(position)
    # adding and initializing the edge
    for bird_pos in yellow_birds:
        maze_dis                               = problem.maze_distance(position, bird_pos)
        edge_weight_dist[(position, bird_pos)] = maze_dis
        edge_queue.push((position, bird_pos), maze_dis)

    for bird_pos in yellow_birds:
        edge_used.add(bird_pos)
        for another_bird_pos in yellow_birds:
            if another_bird_pos not in edge_used:
                maze_dis                                       = problem.maze_distance(another_bird_pos, bird_pos)
                edge_weight_dist[(bird_pos, another_bird_pos)] = maze_dis
                edge_queue.push((bird_pos, another_bird_pos), maze_dis)
                
    forest = My_DisjointSet(node_set)
    # ----------runing the Kruskal algorithm---------------
    num_edges = len(node_set) - 1 # the number of edge
    while not edge_queue.is_empty():
        v1, v2       = least_edge = edge_queue.pop()
        least_weight = edge_weight_dist[least_edge]
        # if the two vertice of the edge not in the same group (also means not in the same tree), we can add the edge to MST
        if not forest.same_group(v1, v2):
            heuristic_value = heuristic_value + least_weight
            num_edges       = num_edges - 1
            if num_edges == 0:
                return heuristic_value
            else:
                # we make the v1 and v2 in the same disjoint set
                forest.union_two_set(forest.find(v1),  forest.find(v2))        
                
    return heuristic_value

every_bird = every_bird_heuristic
