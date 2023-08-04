
from sample_players import DataPlayer
# from isolation.isolation import _WIDTH, _HEIGHT
# from isolation.isolation import DebugState
class CustomPlayer(DataPlayer):
    """ Implement your own agent to play knight's Isolation

    The get_action() method is the only required method for this project.
    You can modify the interface for get_action by adding named parameters
    with default values, but the function MUST remain compatible with the
    default interface.

    **********************************************************************
    NOTES:
    - The test cases will NOT be run on a machine with GPU access, nor be
      suitable for using any other machine learning techniques.

    - You can pass state forward to your agent on the next turn by assigning
      any pickleable object to the self.context attribute.
    **********************************************************************
    """
    def get_action(self, state):
        """ Employ an adversarial search technique to choose an action
        available in the current state calls self.queue.put(ACTION) at least

        This method must call self.queue.put(ACTION) at least once, and may
        call it as many times as you want; the caller will be responsible
        for cutting off the function after the search time limit has expired.

        See RandomPlayer and GreedyPlayer in sample_players for more examples.

        **********************************************************************
        NOTE: 
        - The caller is responsible for cutting off search, so calling
          get_action() from your own code will create an infinite loop!
          Refer to (and use!) the Isolation.play() function to run games.
        **********************************************************************
        """
        # TODO: Replace the example implementation below with your own search
        #       method by combining techniques from lecture
        #
        # EXAMPLE: choose a random move without any search--this function MUST
        #          call self.queue.put(ACTION) at least once before time expires
        #          (the timer is automatically managed for you)
        # self.queue.put(random.choice(state.actions()))
                # Select best action based on greedy search. Action that creates more liberties will be choosen
        def greedy_search(state):        
            return max(state.actions(), key=lambda x: len(state.result(x).liberties(state.locs[self.player_id])))
        
        if state.ply_count <= 2:
#             self.queue.put(random.choice(state.actions()))
            self.queue.put(greedy_search(state))
        else:
#             depth_limit = 5
#             for depth in range(1, depth_limit + 1):
#                 best_move = self.alpha_beta_search(state, depth)
#             self.queue.put(best_move)
            self.queue.put(self.alpha_beta_search(state, depth = 4))
    

  
    def alpha_beta_search(self, gameState, depth):
        """ Return the move along a branch of the game tree that
        has the best possible value.  A move is a pair of coordinates
        in (column, row) order corresponding to a legal move for
        the searching player.

        You can ignore the special case of calling this function
        from a terminal state.
        """

        def min_value(gameState, alpha, beta, depth):
            """ Return the value for a win (+1) if the game is over,
            otherwise return the minimum value over all legal child
            nodes.
            """
            if gameState.terminal_test():
                return gameState.utility(self.player_id)

            if depth <= 0:
                return my_custom_scores(gameState)

            v = float("inf")
            for a in gameState.actions():
                v = min(v, max_value(gameState.result(a), alpha, beta, depth -1))
                if v <= alpha:
                    return v
                beta = min(beta, v)
            return v


        def max_value(gameState, alpha, beta, depth):
            """ Return the value for a loss (-1) if the game is over,
            otherwise return the maximum value over all legal child
            nodes.
            """
            if gameState.terminal_test():
                return gameState.utility(self.player_id)

            if depth <= 0:
                return my_custom_scores(gameState)

            v = float("-inf")
            for a in gameState.actions():
                v = max(v, min_value(gameState.result(a), alpha, beta, depth-1))
                if v >= beta:
                    return v
                alpha = max(alpha, v)
            return v
    
    
        def my_custom_scores(state):
            own_liberties = state.liberties(state.locs[self.player_id])
            opp_liberties = state.liberties(state.locs[1 - self.player_id])
            common_liberties = own_liberties and opp_liberties
            ply_count = state.ply_count

            return len(own_liberties) - len(opp_liberties)
#             return 2*len(own_liberties) - len(opp_liberties)
#             return len(own_liberties) - 2*len(opp_liberties)
#             return len(own_liberties) - 0.5*len(opp_liberties) + len(common_liberties)
#             return  len(own_liberties) -  len(opp_liberties) + 2*len(common_liberties)
#             return ply_count*len(own_liberties) - 2.5*len(opp_liberties) - len(common_liberties)
#             return len(own_liberties) - 2.5*len(opp_liberties) - ply_count*len(common_liberties)
    
    
        alpha = float("-inf")
        beta = float("inf")
        best_score = float("-inf")
        best_move = None
        for a in gameState.actions():
            v = min_value(gameState.result(a), alpha, beta, depth-1)
            alpha = max(alpha, v)
            if v >= best_score:
                best_score = v
                best_move = a
        return best_move
