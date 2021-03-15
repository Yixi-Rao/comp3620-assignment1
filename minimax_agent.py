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
            (MinimaxAgent, AdversarialSearchProblem,
                (int, (int, int), (int, int), ((int, int)), number, number))
                    -> number
        """
        player, red_pos, black_pos, yellow_birds, score, yb_score = state

        # *** YOUR CODE GOES HERE ***

        return score
    
    explored = set()
    
    def maximize(self, problem: AdversarialSearchProblem, state: State,
                 current_depth: int, alpha=float('-inf'), beta=float('inf')) -> Tuple[float, str]:
        """ This method should return a pair (max_utility, max_action).
            The alpha and beta parameters can be ignored if you are
            implementing minimax without alpha-beta pruning.
        """
        
        self.explored.add((state[0], state[1] , state[3]))

        if problem.terminal_test(state) or current_depth == self.depth:
            return (self.evaluation(problem, state), "Stop")

        v = float("-inf")
        select_action = ""
        for next_state, action, _ in problem.get_successors(state):
            if (tuple([state[0], next_state[1] , next_state[3]]) not in self.explored):
                self.explored.add(tuple([state[0], next_state[1] , next_state[3]]))
                temp_max_v = self.minimize(problem, next_state, current_depth + 1)

                if temp_max_v > v:
                    v             = temp_max_v
                    select_action = action
                    
        self.explored.clear()        
        return (v, select_action)
            
    def minimize(self, problem: AdversarialSearchProblem, state: State,
                 current_depth: int, alpha=float('-inf'), beta=float('inf')) -> float:
        """ This function should just return the minimum utility.
            The alpha and beta parameters can be ignored if you are
            implementing minimax without alpha-beta pruning.
        """
        self.explored.add((state[0], state[2] , state[3]))

        if problem.terminal_test(state) or current_depth == self.depth:
            return self.evaluation(problem, state)

        v = float("inf")
        
        for next_state, _, _ in problem.get_successors(state):
            if (tuple([state[0], next_state[2] , next_state[3]]) not in self.explored):
                self.explored.add(tuple([state[0], next_state[2] , next_state[3]]))
                temp_min_v, _ = self.maximize(problem, next_state, current_depth + 1)
                if temp_min_v < v:
                    v = temp_min_v
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
