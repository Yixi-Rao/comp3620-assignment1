# minimax_agent.py
# --------------
# COMP3620/6320 Artificial Intelligence
# The Australian National University
# For full attributions, see attributions.txt on Wattle at the end of the course

"""
    Enter your details below:

    Name: yixi rao
    Student ID: u6826541
    Email: u6826541@anu.edu.au
"""

from typing import Tuple

from agents import Agent
from game_engine.actions import Directions
from search_problems import AdversarialSearchProblem
from functools import reduce
from heuristics import My_DisjointSet,frontiers

Position = Tuple[int, int]
Positions = Tuple[Position]
State = Tuple[int, Position, Position, Positions, float, float]


class MinimaxAgent(Agent):
    """ The agent you will implement to compete with the black bird to try and
        save as many yellow birds as possible. """

    def __init__(self, max_player, depth="2"):
        """ Make a new Adversarial agent with the optional depth argument.
        """
        self.max_player = max_player
        self.depth = int(depth)
    

    def evaluation(self, problem: AdversarialSearchProblem, state: State) -> float:
        """
            This evaluation function will be used when the depth limit is reached. And this evaluation function consider there factors
            below:
                1. Score: the agent will choose the step with the higher utility
                
                2. difference between the average distance of the red bird to all the yellow bird 
                   and the average distance of the black bird to all the yellow bird: since we want the red bird to move to a region with a dense
                   yellow birds, if the the average distance of the red bird to the yellow bird decreases, which mean our bird moves more close
                   to the dense area.
                
                3. The leftover yellow birds: if a state have fewer yellow birds when compared to other state, whcih means that the path to this
                   state comsumes maximum number of birds, so it is tempting to choose this path, the weight of it is -2, since the more leftover,
                   the more small score it got, and '2' can help emphasize the impact of it
                
                4. closest distance to the yellow bird: in some situation where a dense area is on the left side of the bird and there is only one
                   bird that is also the closest one on the right side, we want the bird to eat the cloeset one and go to the right side, which will have
                   more score because we won't want to return to the right side as we finish eating the left side
            
            (MinimaxAgent, AdversarialSearchProblem,
                (int, (int, int), (int, int), ((int, int)), number, number))
                    -> number
        """
        _, red_pos, black_pos, yellow_birds, score, _ = state

        # *** YOUR CODE GOES HERE ***
        
        average_dis_red   = (sum(map(lambda x : problem.maze_distance(red_pos, x), yellow_birds)))/len(yellow_birds) if len(yellow_birds) != 0 else 0   # the average distance of the red bird to all the yellow bird    
        average_dis_black = (sum(map(lambda x : problem.maze_distance(black_pos, x), yellow_birds))/len(yellow_birds)) if len(yellow_birds) != 0 else 0 # the average distance of the black bird to all the yellow bird
        closest_distance   = min(map(lambda x : problem.maze_distance(red_pos, x), yellow_birds)) if len(yellow_birds) != 0 else 0                      # closest distance to the yellow bird
        return score +  (average_dis_black) - (average_dis_red) - len(yellow_birds) * 2  - closest_distance * 1.25
    
    def maximize(self, problem: AdversarialSearchProblem, state: State,
                current_depth: int, alpha = float('-inf'), beta = float('inf')) -> Tuple[float, str]:
        """ This method should return a pair (max_utility, max_action).
            The alpha and beta parameters can be ignored if you are
            implementing minimax without alpha-beta pruning.
        """
        # It is almost the same to the textbook and lecture slides 
        if current_depth == self.depth:
            return (self.evaluation(problem, state), "Stop")
        elif problem.terminal_test(state) or current_depth == self.depth:
            return (state[4], "Stop")
        
        v = float("-inf")
        select_action = ""
        for next_state, action, _ in problem.get_successors(state):
            temp_max_v = self.minimize(problem, next_state, current_depth + 1, alpha, beta)
            if temp_max_v > v:
                v             = temp_max_v
                select_action = action
            if v >= beta:
                return (v, action)
            alpha = max(alpha, v)
                   
        return (v, select_action)
            
    def minimize(self, problem: AdversarialSearchProblem, state: State,
                 current_depth: int, alpha = float('-inf'), beta = float('inf')) -> float:
        """ This function should just return the minimum utility.
            The alpha and beta parameters can be ignored if you are
            implementing minimax without alpha-beta pruning.
        """
        # It is almost the same to the textbook and lecture slides
        if current_depth == self.depth:
            return self.evaluation(problem, state)
        elif problem.terminal_test(state) or current_depth == self.depth:
            return state[4]

        v = float("inf")
        for next_state, _, _ in problem.get_successors(state):
            temp_min_v, _ = self.maximize(problem, next_state, current_depth + 1, alpha, beta)
            if temp_min_v < v:
                v = temp_min_v
                if v <= alpha:
                    return v
                beta = min(beta, v)
        return v

    def get_action(self, game_state):
        """ This method is called by the system to solicit an action from
            MinimaxAgent. It is passed in a State object.

            Like with all of the other search problems, we have abstracted
            away the details of the game state by producing a SearchProblem.
            You will use the states of this AdversarialSearchProblem to
            implement your minimax procedure. The details you need to know
            are explained at the top of this file.
        """
        # We tell the search problem what the current state is and which player
        # is the maximizing player (i.e. who's turn it is now).
        problem = AdversarialSearchProblem(game_state, self.max_player)
        state = problem.get_initial_state()
        utility, max_action = self.maximize(problem, state, 0)
        print("At Root: Utility:", utility, "Action:",
              max_action, "Expanded:", problem._expanded)
        return max_action
