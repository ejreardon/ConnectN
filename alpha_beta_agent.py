import math
import agent

###########################
# Alpha-Beta Search Agent #
###########################

class AlphaBetaAgent(agent.Agent):
    """Agent that uses alpha-beta search"""

    # Class constructor.
    #
    # PARAM [string] name:      the name of this player
    # PARAM [int]    max_depth: the maximum search depth
    def __init__(self, name, max_depth):
        super().__init__(name)
        # Max search depth
        self.max_depth = max_depth

    # Pick a column.
    #
    # PARAM [board.Board] brd: the current board state
    # RETURN [int]: the column where the token must be added
    #
    # NOTE: make sure the column is legal, or you'll lose the game.
    def go(self, brd):
        """Search for the best move (choice of column for the token)"""
        # Use get-successors to find the set of successive board states for the next move
        next_move_list = self.get_successors(brd)
        # Initialize a dictionary to track board states their values to find max values and their assoc states tuples
        values_dict = {}
        # Int to hold the max_value found (init to negative infinity)
        max_found = float("-inf")
        # Iterate through the possible board states (tuple of board and index of new token) in the nextMove_list
        for state in next_move_list:
            # Begin find_min function with the new max and depth of 1 on the successors of the current initial state
            min_found = self.find_min(self.get_successors(state[0]), max_found, 1)
            # Update the dict with the min value found and the state tuple
            values_dict.update({min_found : state})
            # Check for new max and replace if possible
            if min_found > max_found:
                max_found = min_found
        # Once all values are found, find max_found in the dict and get the tuple to return the move needed to be made
        return (values_dict[max_found])[0]

            # - If the list of board states returned is empty or acq state, cut off there
        # - Use a heuristic function to evaluate the successor nodes
        # - Implement max() and min() functions (representing you and your adversary) to determine
        #   which move to make
            # - Keep on working up the tree alternating max and min function until you come to terminating
            #   state or reach the depth
        # - Find out what orignal successive state it branches off of and use that to determine where to place token

    # Find the board state that returns the highest value
    #
    # PARAM [list of board.Board]: The list of successive board states
    # PARAM [int]: The current maximum value found, used for Alpha-Beta Pruning
    # PARAM [int]: The current depth of the nodes
    # RETURN [int]: Maximum value found
    #
    def find_max(self, states, max_val, curr_depth):
        # TODO
        return 1

    # Find the board state that returns the lowest value
    #
    # PARAM [list of board.Board]: The list of successive board states
    # PARAM [int]: The current maximum value found, used for Alpha-Beta Pruning
    # PARAM [int]: The current depth of the nodes
    # RETURN [int]: Minimum value found
    #
    def find_min(self, states, max_val, curr_depth):
        # TODO
        return 1


    # Get the successors of the given board.
    #
    # PARAM [board.Board] brd: the board state
    # RETURN [list of (board.Board, int)]: a list of the successor boards,
    #                                      along with the column where the last
    #                                      token was added in it
    def get_successors(self, brd):
        """Returns the reachable boards from the given board brd. The return value is a tuple (new board state, column number where last token was added)."""
        # Get possible actions
        freecols = brd.free_cols()
        # Are there legal actions left?
        if not freecols:
            return []
        # Make a list of the new boards along with the corresponding actions
        succ = []
        for col in freecols:
            # Clone the original board
            nb = brd.copy()
            # Add a token to the new board
            # (This internally changes nb.player, check the method definition!)
            nb.add_token(col)
            # Add board to list of successors
            succ.append((nb,col))
        return succ
