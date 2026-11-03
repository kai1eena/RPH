class MyPlayer:
    '''Mine interpretation of aPavlov strategy. Every 6 rounds checks opp moves'''
    #player initialization
    def __init__(self, payoff_matrix, number_of_iterations = None):
        self.payoff_matrix = payoff_matrix
        self.number_of_iterations = number_of_iterations

        #declaretion of values for other functions
        self.my_last_move = None
        self.opponents_last_move = None
        self.my_moves = []
        self.opponents_moves = []
        self.rounds = 0
        self.const_move = None
        self.Cooperate = False
        self.Defect = True
        self.strategy_type = None

        #call matrix analyzis before the game start
        self.analyze_matrix()

    #matrix analyzis
    def analyze_matrix(self):
        #defining 4 payoff values
        payoff00 = self.payoff_matrix[0][0][0]
        payoff01 = self.payoff_matrix[0][1][0]
        payoff10 = self.payoff_matrix[1][0][0]
        payoff11 = self.payoff_matrix[1][1][0]


        #Check if the matrix is standard
        if payoff00 >= payoff11:
            #R, S, T, P are by definition is Reward, Sucker payoff, Temptation and Punishment
            self.Cooperate = False
            self.Defect = True
            #assigning payoffs to values
            R = payoff00
            S = payoff01
            T = payoff10
            P = payoff11

        #Check if the matrix is reversed
        else:
            self.Cooperate = True
            self.Defect = False
            R = payoff11
            S = payoff10
            T = payoff01
            P = payoff00

        #check if always cooperate is supperior
        if R >= T and S >= P:
            self.const_move = self.Cooperate
        
        #check if always defect is supperior
        elif (P >= R and T >= S and (P > R or 2 * R <= T + S)) or (P == R and T >= R and P >= S):
            self.const_move = self.Defect

    #Move selection
    def select_move(self):
        #checks if one move is supperior
        if self.const_move != None:
            return self.const_move
        
        self.rounds = len(self.my_moves)

        #last round defect(if there was atleast one defect, for self vs self tournament)
        if (self.number_of_iterations != None and 
            len(self.my_moves) >= self.number_of_iterations - 1 and
            self.Defect in self.opponents_moves):
            return self.Defect
        
        #aPavlov strategy implementation. To clarify, in mine implementation
        #I dont use Pavlov strategy in aPavlov, its too risky, so instead I use more forgiving cycle to maximize points
        if self.rounds == 0:
            return self.Cooperate

        if self.strategy_type == 'Always D':
            return self.Defect

        #every 6 round check of last 6 opponents moves, then program chooses strat
        #basicaly if less than 2 defects next 6 rounds is titfortat
        #if more than one and less than 4 defects its titfortwotats
        #if more than 3 defects, its permanent defect
        if self.rounds % 6 == 0:
            #defect count
            defects = self.opponents_moves[self.rounds - 6:].count(self.Defect)
            if defects <= 1:
                self.strategy_type = 'TitForTat'
            
            elif (defects >=2 and defects < 4 and
                  self.strategy_type != 'TitForTwoTats'):
                self.strategy_type = 'TitForTwoTats'

            else:
                self.strategy_type = 'Always D'
        #first 6 rounds tft than choosing based on strategy_type
        if self.strategy_type == None or self.strategy_type == 'TitForTat':
            return self.tftat()

        if self.strategy_type == 'TitForTwoTats':
            return self.tftwo_tats()

        if self.strategy_type == 'Always D':
            return self.Defect
        
    #Writing down last moves
    def record_last_moves(self, my_last_move, opponents_last_move):
        self.opponents_last_move = opponents_last_move
        self.my_last_move = my_last_move
        self.my_moves.append(my_last_move)
        self.opponents_moves.append(opponents_last_move)

    #titfortat strategy for aPavlov
    def tftat(self):
        if self.opponents_last_move == self.Defect:
            return self.Defect
        
        else:
            return self.Cooperate

    #titfortwotats for aPavlov
    def tftwo_tats(self):
        if self.opponents_moves[-1] == self.Defect and self.opponents_moves[-2] == self.Defect:
            return self.Defect
    
        else:
            return self.Cooperate