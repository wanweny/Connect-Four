#Connect4 AI Player
class alphaBetaAI(connect4Player): 
    
	def play(self, env, move):
		depth = 2
		if not env.history[env.turnPlayer.position-1]:
			move[:] = [3] #if board is empty play middle column
		else:
			move[:] = [self.alphaBeta(env, depth, True, -math.inf, math.inf)[1]]
		print ("Done")
    
	def successor(self, indices):
		for i in range(1, len(indices)):
		    j = i
		    while j > 0 and abs(3-indices[j]) < abs(3-indices[j-1]):
		        indices[j], indices[j-1] = indices[j-1], indices[j]
		        j -= 1
		return indices
    
	def simulateMove(self, env, move, player):
		env.board[env.topPosition[move]][move] = player
		env.topPosition[move] -= 1
		env.history[player-1].append(move)
    
	def alphaBeta(self, env, depth, maxPlayer, alpha, beta):
		if depth == 0 or (env.history[env.turnPlayer.position-1] and env.gameOver(env.history[env.turnPlayer.position-1][-1], env.turnPlayer)):
		    return self.eval(env, env.turnPlayer) - self.eval(env, env.turnPlayer.opponent), None
		if maxPlayer:
		    #get indices of possible moves
		    possible = env.topPosition >= 0
		    indices = []
		    for i, p in enumerate(possible):
		        if p: indices.append(i)
		    indices = self.successor(indices)
		    #set best value  and move
		    best_value = -math.inf
		    best_move = 0
		    #loop through each child/possible move    
		    for i in range(0,len(indices)):
		        nextEnv = env.getEnv()
		        child_move = indices[i]
		        self.simulateMove(nextEnv, child_move, nextEnv.turnPlayer.position)
		        child = nextEnv.getBoard()
		        child_value = self.alphaBeta(nextEnv, depth-1, False, alpha, beta)[0]
		        if child_value > best_value:
		            best_value = child_value
		            best_move = child_move
		        #pruning
		        if best_value >= beta:
		            return best_value, best_move
		        alpha = max(alpha, best_value)
		    return best_value, best_move
		else: #minPlayer
		    #get indices of possible moves
		    possible = env.topPosition >= 0
		    indices = []
		    for i, p in enumerate(possible):
		        if p: indices.append(i)
		    indices = self.successor(indices)
		    #set best value  and move
		    best_value = math.inf
		    best_move = 0
		    #loop through each child/possible move    
		    for i in range(0,len(indices)):
		        nextEnv = env.getEnv()
		        child_move = indices[i]
		        self.simulateMove(nextEnv, child_move, nextEnv.turnPlayer.opponent.position)
		        child = nextEnv.getBoard()
		        child_value = self.alphaBeta(nextEnv, depth-1, True, alpha, beta)[0]
		        if child_value < best_value:
		            best_value = child_value
		            best_move = child_move
		        #pruning
		        if best_value <= alpha:
		            return best_value, best_move
		        beta = min(beta, best_value)
		    return best_value, best_move
    
	def eval(self, env, player):
		env = env.getEnv()
		eval = 0
		#Horizontal check possible 4 in a row
		for i in range(0, ROW_COUNT):#0,1,2,3,4,5
		    for j in range(0, COLUMN_COUNT-3):#0,1,2,3
		        count = 0
                #check next set if opponent takes any position
                if env.board[i][j] == player.opponent.position or env.board[i][j+1] == player.opponent.position or env.board[i][j+2] == player.opponent.position or env.board[i][j+3] == player.opponent.position:
		            continue
		        if env.board[i][j] == player.position:
		            count += 1
		        if env.board[i][j+1] == player.position:
		            count += 1
		        if env.board[i][j+2] == player.position:
		            count += 1
		        if env.board[i][j+3] == player.position:
		            count += 1
		        #add value to eval base on the number of pieces in the row
		        if count == 4:
		            eval += 1000000000000000
		        elif count == 3:
		            eval += 700
		        elif count == 2:
		            eval += 15
		        else:
		            eval += 1
		        #add additional points where the pieces are together
		        if (env.board[i][j] == player.position and env.board[i][j+1] == player.position) or (env.board[i][j+1] == player.position and env.board[i][j+2] == player.position) or (env.board[i][j+2] == player.position and env.board[i][j+3] == player.position):
		            eval += 15 #two pieces together
		
		#Vertical check possible 4 in a row
		for i in range(0, ROW_COUNT-3):
		    for j in range(0, COLUMN_COUNT):
		        count = 0
                #check next set if opponent takes any position
                if env.board[i][j] == player.opponent.position or env.board[i+1][j] == player.opponent.position or env.board[i+2][j] == player.opponent.position or env.board[i+3][j] == player.opponent.position:
		            continue
		        if env.board[i][j] == player.position:
		            count += 1
		        if env.board[i+1][j] == player.position:
		            count += 1
		        if env.board[i+2][j] == player.position:
		            count += 1
		        if env.board[i+3][j] == player.position:
		            count += 1
		        #add value to eval base on the number of pieces in the column
		        if count == 4:
		            eval += 1000000000000000
		        elif count == 3:
		            eval += 700
		        elif count == 2:
		            eval += 15
		        else:
		            eval += 1
		        #add additional points where there pieces are together
		        if (env.board[i][j] == player.position and env.board[i+1][j] == player.position) or (env.board[i+1][j] == player.position and env.board[i+2][j] == player.position) or (env.board[i+2][j] == player.position and env.board[i+3][j] == player.position):
		            eval += 15 #two pieces together
	       
	       #Diagonal(left to right) check possible 4 in a row
		for i in range(0, ROW_COUNT-3):
		    for j in range(0, COLUMN_COUNT-3):
		        count = 0
                #check next set if opponent takes any position
                if env.board[i][j] == player.opponent.position or env.board[i+1][j+1] == player.opponent.position or env.board[i+2][j+2] == player.opponent.position or env.board[i+3][j+3] == player.opponent.position:
                    continue
		        if env.board[i][j] == player.position:
		            count += 1
		        if env.board[i+1][j+1] == player.position:
		            count += 1
		        if env.board[i+2][j+2] == player.position:
		            count += 1
		        if env.board[i+3][j+3] == player.position:
		            count += 1
		        #add value to eval base on the number of pieces in the diagonal
		        if count == 4:
		            eval += 1000000000000000
		        elif count == 3:
		            eval += 700
		        elif count == 2:
		            eval += 15
		        else:
		            eval += 1
		        #add additional points where there pieces are together
		        if (env.board[i][j] == player.position and env.board[i+1][j+1] == player.position) or (env.board[i+1][j+1] == player.position and env.board[i+2][j+2] == player.position) or (env.board[i+2][j+2] == player.position and env.board[i+3][j+3] == player.position):
		            eval += 15 #two pieces together
		        
		#Diagonal(right to left) check possible 4 in a row
		for i in range(0, ROW_COUNT-3):
		    for j in range(COLUMN_COUNT-1, COLUMN_COUNT-5, -1):
		        count = 0
                #check next set if opponent takes any position
                if env.board[i][j] == player.opponent.position or env.board[i+1][j-1] == player.opponent.position or env.board[i+2][j-2] == player.opponent.position or env.board[i+3][j-3] == player.opponent.position:
                    continue
		        if env.board[i][j] == player.position:
		            count += 1
		        if env.board[i+1][j-1] == player.position:
		            count += 1
		        if env.board[i+2][j-2] == player.position:
		            count += 1
		        if env.board[i+3][j-3] == player.position:
		            count += 1
		        #add value to eval base on the number of pieces in the diagonal
		        if count == 4:
		            eval += 1000000000000000
		        elif count == 3:
		            eval += 700
		        elif count == 2:
		            eval += 15
		        else:
		            eval += 1
		        #add additional points where there pieces are together
		        if (env.board[i][j] == player.position and env.board[i+1][j-1] == player.position) or (env.board[i+1][j-1] == player.position and env.board[i+2][j-2] == player.position) or (env.board[i+2][j-2] == player.position and env.board[i+3][j-3] == player.position):
		            eval += 15 #two pieces together
		return eval