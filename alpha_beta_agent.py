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
        
    # Return the height of the columns, if a column is full, set to -1
    #
    # PARAM [board.Board]: the column of the cell to be checked
    # RETURN [int[]]: the heights of all columns in the board
    def validMoves(brd):
        # Initialize possible moves array with width of board
        moves = [None] * brd.w
        
        # For each column, check if full, if not find valid move spot
        for i in range(brd.w):
            
            # If the column is full, set to no possible move
            if(brd[i][0] != 0):
                moves[i] = -1
            
            # If the column is not full, return the height of the first open space
            else:
                for j in range(brd.h):
                    # If it is at the bottom, only check if the space is empty, not if the space below is full
                    if(brd[i][j] == 0 && j == brd.h - 1):
                        moves[i] = j
                    # Otherwise check if the current space is empty and the space below is full
                    elif(brd[i][j] == 0 && brd[i][j + 1] != 0):
                        moves[i] = j
        # Return the array of possible moves
        return moves
                
        
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
            max_state_value = float("-inf")
            for state in states:
                curr_value = self.heuristic(self, state)
                if curr_value > max_state_value:
                    max_state_value = curr_value
        else:
            # Init max state value to negative infinity
            max_state_value = float("-inf")
            # Iterate through the successive states and find the min for each, increment the depth
            for state in states:
                curr_value = self.find_min(state, max_val, curr_depth + 1)
                if curr_value > max_state_value:
                    max_state_value = curr_value
        return max_state_value

    # Find heuristic value based on vertical arrangement of tokens
    #
    # PARAM [int]: The y value (row) of the token
    # PARAM [int]: The x value (column) of the token
    # PARAM [board.Board] brd: the current board state
    # RETURN [int]: Evaluation of vertical arrangement
    #
    def verticalHeuristic(self, row, col, brd):
        # boolean to tell whether a chain of tokens is broken
        is_broken = False
        # boolean to tell if it the first value to be checked
        first = True
        # variable for the first token to start the chain
        current_token = -1
        # variables for the player and opponent tokens
        plyr = 0
        opp = 0

        # iterate over the next brd.n spaces in the same column to get evaluation,
        # starting from the bottom
        for i in range(brd.n):  # ex: (0, 1, 2, 3)
            # make sure that the token location is valid (less than the board height)
            if (row + (brd.n - 1) - i) <= brd.h:
                # store the value of the next token
                value = brd[row + (brd.n - 1) - i][col]
                # if it is the first, store it as the current_token
                if first:
                    current_token = value
                    first = False
                # if the current_token isn't the same as the value, then it is broken
                if current_token != value:
                    is_broken = True
                # else, the chain is broken, so reset each player and the current_token
                if is_broken:
                    plyr = 0
                    opp = 0
                    is_broken = False
                    current_token = value
                # increment the player and opponent variables based on value
                if value == 1:
                    plyr += 1
                elif value == 2:
                    opp += 1
        # return the greater value to the power of 10 ex: (1, 10, 100, 1000)
        if plyr > opp:
            return (10 ** plyr)/10
        # return the negative if opponent
        else:
            return -(10 ** opp)/10

    # Heuristic function to return an evaluation of the board state
    #
    # PARAM [board.Board] brd: the current board state
    # RETURN [int]: board state value
    #
    def heuristic(self, brd):
        total_score = 0
        for col in range(len(brd.w)):
            for row in range(len(brd.h)):
                # TODO ADD: Set variable to vertical heuristic function
                vertical_score = self.verticalHeuristic(row, col, brd)
                if vertical_score == (10 ** (brd.n-1)) or vertical_score == -(10 ** (brd.n-1)):
                    return vertical_score
                total_score += vertical_score

                # TODO ADD: Set variable to horizontal heuristic function
                horizontal_score = self.horizontalHeuristic(row, col, brd)
                if horizontal_score == (10 ** (brd.n-1)) or horizontal_score == -(10 ** (brd.n-1)):
                    return horizontal_score
                total_score += horizontal_score

                # TODO ADD: Set variable to diagonal up heuristic function
                diagonal_up = self.diagonalUpHeuristic(row, col, brd)
                if diagonal_up == (10 ** (brd.n-1)) or diagonal_up == -(10 ** (brd.n-1)):
                    return diagonal_up
                total_score += diagonal_up

                # TODO ADD: Set variable to diagonal down heuristic function
                diagonal_down = self.diagonalDownHeuristic(row, col, brd)
                if diagonal_down == (10 ** (brd.n-1)) or diagonal_down == -(10 ** (brd.n-1)):
                    return diagonal_down
                total_score += diagonal_down
        return total_score

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
            min_state_value = float("inf")
            for state in states:
                curr_value = self.heuristic(self, state)
                if curr_value < min_state_value:
                    min_state_value = curr_value
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
