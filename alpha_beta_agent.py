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
    def valid_moves(self, brd):
        # Initialize possible moves array with width of board
        moves = [None] * brd.w
        
        # For each column, check if full, if not find valid move spot
        for i in range(brd.w):
            
            # If the column is full, set to no possible move
            if brd[i][0] != 0:
                moves[i] = -1
            
            # If the column is not full, return the height of the first open space
            else:
                for j in range(brd.h):
                    # If it is at the bottom, only check if the space is empty, not if the space below is full
                    if brd[i][j] == 0 and j == brd.h - 1:
                        moves[i] = j
                    # Otherwise check if the current space is empty and the space below is full
                    elif brd[i][j] == 0 and brd[i][j + 1] != 0:
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
        print(max_found)
        return (values_dict[max_found])[1]
    
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
                curr_value = self.heuristic(state[0])
                if curr_value > max_state_value:
                    max_state_value = curr_value
        else:
            # Init max state value to negative infinity
            max_state_value = float("-inf")
            # Iterate through the successive states and find the min for each, increment the depth
            for state in states:
                curr_value = self.find_min(self.get_successors(state[0]), max_val, curr_depth + 1)
                if curr_value > max_state_value:
                    max_state_value = curr_value
        return max_state_value

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
                curr_value = self.heuristic(state[0])
                if curr_value < min_state_value:
                    min_state_value = curr_value
        else:
            # Init min state value to positive infinity
            min_state_value = float("inf")
            # Iterate through the successive states and find the max for each, increment the depth
            for state in states:
                curr_value = self.find_max(self.get_successors(state[0]), max_val, curr_depth + 1)
                if curr_value < min_state_value:
                    min_state_value = curr_value
        return min_state_value

    # Find heuristic value based on vertical arrangement of tokens
    #
    # PARAM [int]: The y value (row) of the token
    # PARAM [int]: The x value (column) of the token
    # PARAM [board.Board] brd: the current board state
    # RETURN [int]: Evaluation of vertical arrangement
    #
    def vertical_heuristic(self, row, col, brd):
        # Select the space with the current coordinates
        curr_token = brd.board[row][col]
        # Check if the current space is empty
        if curr_token != 0:
            # Check if the space below is the same token
            if col > 0 and brd.board[row - 1][col] == curr_token:
                # If so, the current space has already been accounted for, return 0
                return 0
            # Keep track of the score to return
            curr_score = 0
            # Variable for space iterating
            new_row = row + 1
            # Iterate upwards until board edge is hit
            while new_row < brd.h:
                # Get whatever is in the new space
                new_token = brd.board[new_row][col]
                # If the newly found token is the same as the one we're on
                if new_token == curr_token:
                    # Add a multiple of 10 to the current score
                    curr_score += 1
                    # Iterate to next space
                    new_row += 1
                # If the space is empty
                elif new_token == 0:
                    # Return the calculated score (1 for 1, 10 for 2, 100 for 3, etc.)
                    # Return positive value for board player
                    if brd.player == curr_token:
                        return (10 ** curr_score) / 10
                    # Return negative value for board opponent
                    else:
                        return (10 ** curr_score) / 10 * -1
                # If the token is the other player's
                else:
                    if brd.player == curr_token:
                        return (10 ** curr_score) / 10 * -1
                    # Return negative value for board opponent
                    else:
                        return (10 ** curr_score) / 10
                    # # Return 0
                    # return 0
            # If board edge is hit, return 0
            return 0
        return 0

    # Find heuristic value based on horizontal arrangement of tokens
    #
    # PARAM [int]: The y value (row) of the token
    # PARAM [int]: The x value (column) of the token
    # PARAM [board.Board] brd: the current board state
    # RETURN [int]: Evaluation of horizontal arrangement
    #
    def horizontal_heuristic(self, row, col, brd):
        # Select the space with the current coordinates
        curr_token = brd.board[row][col]
        # Check if the current space is empty
        if curr_token == 0:
            # Check if the right-adjacent space is a token
            if col < brd.w and brd.board[row][col + 1] != 0:
                # Reset the current token to the new token value
                curr_token = brd.board[row][col + 1]
                # Keep track of the score to return
                curr_score = 0
                # Variable for space iterating
                new_col = col + 1
                # Iterate to the right until board edge is hit
                while new_col < brd.w:
                    # Get whatever is in the new space
                    new_token = brd.board[row][new_col]
                    # If the newly found token is the same as the one we're on
                    if new_token == curr_token:
                        # Add a multiple of 10 to the current score
                        curr_score += 1
                        # Iterate to next space
                        new_col += 1
                    # If the space is empty
                    elif new_token == 0:
                        # Return the calculated score (1 for 1, 10 for 2, 100 for 3, etc.)
                        # Return positive value for board player
                        if brd.player == curr_token:
                            return (10 ** curr_score) / 10
                        # Return negative value for board opponent
                        else:
                            return (10 ** curr_score) / 10 * -1
                    # If the token is the other player's
                    else:
                        if brd.player == curr_token:
                            return (10 ** curr_score) / 10 * -1
                        # Return negative value for board opponent
                        else:
                            return (10 ** curr_score) / 10
                        # # Return 0
                        # return 0
                # Return the calculated score (1 for 1, 10 for 2, 100 for 3, etc.)
                # Return positive value for board player
                if brd.player == curr_token:
                    return (10 ** curr_score) / 10
                # Return negative value for board opponent
                else:
                    return (10 ** curr_score) / 10 * -1
        # Else, if the space contains a token
        else:
            # Check if the space to the left is the same token
            if col > 0 and brd.board[row][col - 1] == curr_token:
                # If so, the current space has already been accounted for, return 0
                return 0
            # Keep track of the score to return
            curr_score = 0
            # Variable for space iterating
            new_col = col + 1
            # Iterate to the right until board edge is hit
            while new_col < brd.w:
                # Get whatever is in the new space
                new_token = brd.board[row][new_col]
                # If the newly found token is the same as the one we're on
                if new_token == curr_token:
                    # Add a multiple of 10 to the current score
                    curr_score += 1
                    # Iterate to next space
                    new_col += 1
                # If the space is empty
                elif new_token == 0:
                    # Check if you are at bottom row or if there is a token below (gravity)
                    if row == 0 or brd.board[row - 1][new_col] != 0:
                        # Return the calculated score (1 for 1, 10 for 2, 100 for 3, etc.)
                        # Return positive value for board player
                        if brd.player == curr_token:
                            return (10 ** curr_score) / 10
                        # Return negative value for board opponent
                        else:
                            return (10 ** curr_score) / 10 * -1
                    # If there is nothing underneath
                    else:
                        # Return 0
                        return 0
                # If the token is the other player's
                else:
                    if brd.player == curr_token:
                        return (10 ** curr_score) / 10 * -1
                    # Return negative value for board opponent
                    else:
                        return (10 ** curr_score) / 10
                    # # Return 0
                    # return 0
            # If board edge is hit, return 0
            return 0
        return 0

    # Find heuristic value based on diagonal up arrangement of tokens
    #
    # PARAM [int]: The y value (row) of the token
    # PARAM [int]: The x value (column) of the token
    # PARAM [board.Board] brd: the current board state
    # RETURN [int]: Evaluation of diagonal up arrangement
    #
    def d_up_heuristic(self, row, col, brd):
        # Select the space with the current coordinates
        curr_token = brd.board[row][col]
        # Check if the current space is empty
        if curr_token == 0:
            # Check if the diagonal up space is a token
            if col < brd.w and row < brd.h and brd.board[row + 1][col + 1] != 0:
                # Reset the current token to the new token value
                curr_token = brd.board[row + 1][col + 1]
                # Keep track of the score to return
                curr_score = 0
                # Variable for col space iterating
                new_col = col + 1
                # Variable for row space iterating
                new_row = row + 1
                # Iterate diagonally up until board edge is hit
                while new_col < brd.w and new_row < brd.h:
                    # Get whatever is in the new space
                    new_token = brd.board[new_row][new_col]
                    # If the newly found token is the same as the one we're on
                    if new_token == curr_token:
                        # Add a multiple of 10 to the current score
                        curr_score += 1
                        # Iterate to next space
                        new_col += 1
                        new_row += 1
                    # If the space is empty
                    elif new_token == 0:
                        # Return the calculated score (1 for 1, 10 for 2, 100 for 3, etc.)
                        # Return positive value for board player
                        if brd.player == curr_token:
                            return (10 ** curr_score) / 10
                        # Return negative value for board opponent
                        else:
                            return (10 ** curr_score) / 10 * -1
                    # If the token is the other player's
                    else:
                        # Return 0
                        return 0
                # Return the calculated score (1 for 1, 10 for 2, 100 for 3, etc.)
                # Return positive value for board player
                if brd.player == curr_token:
                    return (10 ** curr_score) / 10
                # Return negative value for board opponent
                else:
                    return (10 ** curr_score) / 10 * -1
        # Else, if the space contains a token
        else:
            # Check if the space to the left is the same token
            if col > 0 and row > 0 and brd.board[row - 1][col - 1] == curr_token:
                # If so, the current space has already been accounted for, return 0
                return 0
            # Keep track of the score to return
            curr_score = 0
            # Variable for col space iterating
            new_col = col + 1
            # Variable for row space iterating
            new_row = row + 1
            # Iterate to the right until board edge is hit
            while new_col < brd.w and new_row < brd.h:
                # Get whatever is in the new space
                new_token = brd.board[new_row][new_col]
                # If the newly found token is the same as the one we're on
                if new_token == curr_token:
                    # Add a multiple of 10 to the current score
                    curr_score += 1
                    # Iterate to next space
                    new_col += 1
                    new_row += 1
                # If the space is empty
                elif new_token == 0:
                    # Check if you are at bottom row or if there is a token below (gravity)
                    if row == 0 or brd.board[new_row - 1][new_col] != 0:
                        # Return the calculated score (1 for 1, 10 for 2, 100 for 3, etc.)
                        # Return positive value for board player
                        if brd.player == curr_token:
                            return (10 ** curr_score) / 10
                        # Return negative value for board opponent
                        else:
                            return (10 ** curr_score) / 10 * -1
                    # If there is nothing underneath
                    else:
                        # Return 0
                        return 0
                # If the token is the other player's
                else:
                    if brd.player == curr_token:
                        return (10 ** curr_score) / 10 * -1
                    # Return negative value for board opponent
                    else:
                        return (10 ** curr_score) / 10
                    # # Return 0
                    # return 0
            # If board edge is hit, return 0
            return 0
        return 0

    # Find heuristic value based on diagonal down arrangement of tokens
    #
    # PARAM [int]: The y value (row) of the token
    # PARAM [int]: The x value (column) of the token
    # PARAM [board.Board] brd: the current board state
    # RETURN [int]: Evaluation of diagonal down arrangement
    #
    def d_down_heuristic(self, row, col, brd):
        # Select the space with the current coordinates
        curr_token = brd.board[row][col]
        # Check if the current space is empty
        if curr_token == 0:
            # Check if the diagonal down space is a token
            if col < brd.w and row >= 0 and brd.board[row - 1][col + 1] != 0:
                # Reset the current token to the new token value
                curr_token = brd.board[row - 1][col + 1]
                # Keep track of the score to return
                curr_score = 0
                # Variable for col space iterating
                new_col = col + 1
                # Variable for row space iterating
                new_row = row - 1
                # Iterate diagonally up until board edge is hit
                while new_col < brd.w and new_row >= 0:
                    # Get whatever is in the new space
                    new_token = brd.board[new_row][new_col]
                    # If the newly found token is the same as the one we're on
                    if new_token == curr_token:
                        # Add a multiple of 10 to the current score
                        curr_score += 1
                        # Iterate to next space
                        new_col += 1
                        new_row -= 1
                    # If the space is empty
                    elif new_token == 0:
                        # Return the calculated score (1 for 1, 10 for 2, 100 for 3, etc.)
                        # Return positive value for board player
                        if brd.player == curr_token:
                            return (10 ** curr_score) / 10
                        # Return negative value for board opponent
                        else:
                            return (10 ** curr_score) / 10 * -1
                    # If the token is the other player's
                    else:
                        # Return 0
                        return 0
                # Return the calculated score (1 for 1, 10 for 2, 100 for 3, etc.)
                # Return positive value for board player
                if brd.player == curr_token:
                    return (10 ** curr_score) / 10
                # Return negative value for board opponent
                else:
                    return (10 ** curr_score) / 10 * -1
        # Else, if the space contains a token
        else:
            # Check if the space to the left is the same token
            if col > 0 and row < brd.h - 1 and brd.board[row + 1][col - 1] == curr_token:
                # If so, the current space has already been accounted for, return 0
                return 0
            # Keep track of the score to return
            curr_score = 0
            # Variable for col space iterating
            new_col = col + 1
            # Variable for row space iterating
            new_row = row - 1
            # Iterate to the right until board edge is hit
            while new_col < brd.w and new_row >= 0:
                # Get whatever is in the new space
                new_token = brd.board[new_row][new_col]
                # If the newly found token is the same as the one we're on
                if new_token == curr_token:
                    # Add a multiple of 10 to the current score
                    curr_score += 1
                    # Iterate to next space
                    new_col += 1
                    new_row -= 1
                # If the space is empty
                elif new_token == 0:
                    # Check if you are at bottom row or if there is a token below (gravity)
                    if row == 0 or brd.board[new_row - 1][new_col] != 0:
                        # Return the calculated score (1 for 1, 10 for 2, 100 for 3, etc.)
                        # Return positive value for board player
                        if brd.player == curr_token:
                            return (10 ** curr_score) / 10
                        # Return negative value for board opponent
                        else:
                            return (10 ** curr_score) / 10 * -1
                    # If there is nothing underneath
                    else:
                        # Return 0
                        return 0
                # If the token is the other player's
                else:
                    # Return 0
                    return 0
            # If board edge is hit, return 0
            return 0
        return 0

    # Heuristic function to return an evaluation of the board state
    #
    # PARAM [board.Board] brd: the current board state
    # RETURN [int]: board state value
    #
    def heuristic(self, brd):
        # Variable to hold score return value
        total_score = 0
        # Variable to see check if the row contains tokens
        tokens_in_row = False
        # Iterate through the board starting from the bottom left (assuming height decrements) -- WRONG CHECK
        for h_pos in range(0, brd.h - 1):
            for w_pos in range(0, brd.w - 1):
                # Check if space is a token (CAN PROBABLY OPTIMIZE)
                if (brd.board[h_pos][w_pos] == 1) or (brd.board[h_pos][w_pos] == 2):
                    tokens_in_row = True
                # Add result of vertical heuristic check to the total score
                total_score += self.vertical_heuristic(h_pos, w_pos, brd)
                # Add result of horizontal heuristic check to the total score
                total_score += self.horizontal_heuristic(h_pos, w_pos, brd)
                # Add result of diagonal up heuristic check to the total score
                total_score += self.d_up_heuristic(h_pos, w_pos, brd)
                # Add result of diagonal down heuristic check to the total score
                total_score += self.d_down_heuristic(h_pos, w_pos, brd)
            # When width iteration ends, check if there are no tokens in row
            if not tokens_in_row:
                break
            # Set check back to false to check next row
            tokens_in_row = False
        # Return the sum of all the scores found
        return total_score

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
