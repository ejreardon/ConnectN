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

    # Find the board state that returns the highest value
    #
    # PARAM [list of board.Board]: The list of successive board states
    # PARAM [int]: The current maximum value found, used for Alpha-Beta Pruning
    # PARAM [int]: The current depth of the nodes
    # RETURN [int]: Maximum value found
    #
    def find_max(self, states, max_val, curr_depth):
        # Check to see if no states are returned
        # TODO: Figure out what to do
        # Check to see if the current depth is the maximum depth
        if curr_depth == self.max_depth:
            # TODO ADD: Perform heuristics on the states and return the max
            print("Reached max depth")
            max_state_value = 100000
        else:
            # Init max state value to negative infinity
            max_state_value = float("-inf")
            # Iterate through the successive states and find the min for each, increment the depth
            for state in states:
                curr_value = self.find_min(state, max_val, curr_depth + 1)
                if curr_value > max_state_value:
                    max_state_value = curr_value
        return max_state_value

    # Heuristic function to return an evaluation of the board state
    #
    # PARAM [board.Board] brd: the current board state
    # RETURN [int]: board state value
    #
    def heuristic(self, brd):
        total_score = 0
        for row in range(len(brd.w)):
            for col in range(len(brd.h)):
                # TODO ADD: Set variable to vertical heuristic function
                vertical_score = VerticalHeuristic(row, col, brd)
                if vertical_score == 1000 or vertical_score == -1000:
                    return vertical_score
                total_score += vertical_score

                # TODO ADD: Set variable to horizontal heuristic function
                horizontal_score = HorizontalHeuristic(row, col, brd)
                if horizontal_score == 1000 or horizontal_score == -1000:
                    return horizontal_score
                total_score += horizontal_score

                # TODO ADD: Set variable to diagonal up heuristic function
                diagonal_up = DiagonalUpHeuristic(row, col, brd)
                if diagonal_up == 1000 or diagonal_up == -1000:
                    return diagonal_up
                total_score += diagonal_up

                # TODO ADD: Set variable to diagonal down heuristic function
                diagonal_down = DiagonalDownHeuristic(row, col, brd)
                if diagonal_down == 1000 or diagonal_down == -1000:
                    return diagonal_down
                total_score += diagonal_down;
        return total_score;

    # Find the board state that returns the lowest value
    #
    # PARAM [list of board.Board]: The list of successive board states
    # PARAM [int]: The current maximum value found, used for Alpha-Beta Pruning
    # PARAM [int]: The current depth of the nodes
    # RETURN [int]: Minimum value found
    #
    def find_min(self, states, max_val, curr_depth):
        # Check to see if no states are returned
        # TODO: Figure out what to do
        # Check to see if the current depth is the maximum depth
        if curr_depth == self.max_depth:
            # TODO ADD: Perform heuristics on the states and return the max
            print("Reached max depth")
            min_state_value = 100000
        else:
            # Init min state value to positive infinity
            min_state_value = float("inf")
            # Iterate through the successive states and find the max for each, increment the depth
            for state in states:
                curr_value = self.find_max(state, max_val, curr_depth + 1)
                if curr_value < min_state_value:
                    min_state_value = curr_value
        return min_state_value


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
