# multiAgents.py
# --------------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


from util import manhattanDistance
from game import Directions
import random, util

from game import Agent

class ReflexAgent(Agent):
    """
    A reflex agent chooses an action at each choice point by examining
    its alternatives via a state evaluation function.

    The code below is provided as a guide.  You are welcome to change
    it in any way you see fit, so long as you don't touch our method
    headers.
    """


    def getAction(self, gameState):
        """
        You do not need to change this method, but you're welcome to.

        getAction chooses among the best options according to the evaluation function.

        Just like in the previous project, getAction takes a GameState and returns
        some Directions.X for some X in the set {NORTH, SOUTH, WEST, EAST, STOP}
        """
        # Collect legal moves and child states
        legalMoves = gameState.getLegalActions()

        # Choose one of the best actions
        scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices) # Pick randomly among the best

        "Add more of your code here if you want to"

        return legalMoves[chosenIndex]

    def evaluationFunction(self, currentGameState, action):
        """
        Design a better evaluation function here.

        The evaluation function takes in the current and proposed child
        GameStates (pacman.py) and returns a number, where higher numbers are better.

        The code below extracts some useful information from the state, like the
        remaining food (newFood) and Pacman position after moving (newPos).
        newScaredTimes holds the number of moves that each ghost will remain
        scared because of Pacman having eaten a power pellet.

        Print out these variables to see what you're getting, then combine them
        to create a masterful evaluation function.
        """
        # Useful information you can extract from a GameState (pacman.py)
        childGameState = currentGameState.getPacmanNextState(action)
        newPos = childGameState.getPacmanPosition()
        newFood = childGameState.getFood()
        newGhostStates = childGameState.getGhostStates()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

        "*** YOUR CODE HERE ***"

        score = childGameState.getScore()

        for ghost in newGhostStates:                                        #if any of the ghost is extremely close to the action of pacman
            distance = manhattanDistance(newPos,ghost.getPosition())
            if distance <=1:                                                #add a low number
                score -= 1e6                                                #1e6 = 1000000


        food = newFood.asList()
        for food in food:
            distance = manhattanDistance(newPos, food)
            if(distance != 0):
                score += 1/distance                                             #the closer the food to the action of pacman, 1/distance is biger

        return score

def scoreEvaluationFunction(currentGameState):
    """
    This default evaluation function just returns the score of the state.
    The score is the same one displayed in the Pacman GUI.

    This evaluation function is meant for use with adversarial search agents
    (not reflex agents).
    """
    return currentGameState.getScore()

class MultiAgentSearchAgent(Agent):
    """
    This class provides some common elements to all of your
    multi-agent searchers.  Any methods defined here will be available
    to the MinimaxPacmanAgent, AlphaBetaPacmanAgent & ExpectimaxPacmanAgent.

    You *do not* need to make any changes here, but you can if you want to
    add functionality to all your adversarial search agents.  Please do not
    remove anything, however.

    Note: this is an abstract class: one that should not be instantiated.  It's
    only partially specified, and designed to be extended.  Agent (game.py)
    is another abstract class.
    """

    def __init__(self, evalFn = 'scoreEvaluationFunction', depth = '2'):
        self.index = 0 # Pacman is always agent index 0
        self.evaluationFunction = util.lookup(evalFn, globals())
        self.depth = int(depth)

class MinimaxAgent(MultiAgentSearchAgent):
    """
    Your minimax agent (question 2)
    """

    def getAction(self, gameState):
        """
        Returns the minimax action from the current gameState using self.depth
        and self.evaluationFunction.

        Here are some method calls that might be useful when implementing minimax.

        gameState.getLegalActions(agentIndex):
        Returns a list of legal actions for an agent
        agentIndex=0 means Pacman, ghosts are >= 1

        gameState.getNextState(agentIndex, action):
        Returns the child game state after an agent takes an action

        gameState.getNumAgents():
        Returns the total number of agents in the game

        gameState.isWin():
        Returns whether or not the game state is a winning state

        gameState.isLose():
        Returns whether or not the game state is a losing state
        """
        "*** YOUR CODE HERE ***"

        def terminal_test(gameState, depth):
            if((gameState.isWin() or gameState.isLose()) or depth == self.depth):                 #all terminal cases
                return True
            else:
                return False

        def max_value(currentstate, depth, pacman):

            pacmanactions = currentstate.getLegalActions(pacman)                  
            
            if terminal_test(currentstate, depth) == True:
                return (self.evaluationFunction(currentstate), None)

            v = -1e6                                                            
            action = None                                                       #action to be taken by pacman

            for a in pacmanactions:
                nextstate = currentstate.getNextState(pacman, a)
                ghost1 = 1
                result = min_value(nextstate, depth, ghost1)                    #1 agent is the first ghost
                
                if result[0] > v:                                               #max agent always choses bigest value
                    v = result[0]
                    action = a

            return (v, action)


        def min_value(currentstate, depth, ghost):

            ghostactions = currentstate.getLegalActions(ghost)

            if terminal_test(currentstate, depth) == True:
                return (self.evaluationFunction(currentstate), None)

            v = 1e6
            action = None

            for a in ghostactions:
                nextstate = currentstate.getNextState(ghost, a)
                if (ghost == (currentstate.getNumAgents() - 1)):               #if function is called for the last ghost then call max value
                    result = max_value(nextstate, depth + 1, 0)
                else:
                    result = min_value(nextstate, depth, ghost + 1)          #call minvalue for ghosts layer

                if result[0] < v:                                           #min agent always chooses smallest value
                    v = result[0]
                    action = a

            return (v, action)

        result = max_value(gameState, 0, 0)                                  #0 agent is pacman
        return result[1]

class AlphaBetaAgent(MultiAgentSearchAgent):
    """
    Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):
        """
        Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        #similar to minmax only one condition is added

        def terminal_test(gameState, depth):
            if((gameState.isWin() or gameState.isLose()) or depth == self.depth):                 #all terminal cases
                return True
            else:
                return False

        def max_value(currentstate, depth, pacman, a, b):
            actions = currentstate.getLegalActions(pacman)              
            if terminal_test(currentstate, depth) == True:         
                return (self.evaluationFunction(currentstate), None)

            v = -1e6
            action = None                                             

            for act in actions:
                nextstate = currentstate.getNextState(pacman, act)
                result = min_value(nextstate, depth, 1, a, b)

                if result[0] > v:
                    v = result[0]
                    action = act

                if v > b:                                           #changing the value of a if needed
                    return (v, action)
                
                a = max(a,v)

            return (v, action)


        def min_value(currentstate, depth, ghost, a, b):

            actions = currentstate.getLegalActions(ghost)
            if terminal_test(currentstate, depth) == True:         
                return (self.evaluationFunction(currentstate), None)

            v = 1e6
            action = None

            for act in actions:
                nextstate = currentstate.getNextState(ghost, act)
                
                if (ghost == (currentstate.getNumAgents() - 1)):               #if function is called for the last ghost then call max value
                    result = max_value(nextstate, depth + 1, 0,a,b)
                else:
                    result = min_value(nextstate, depth, ghost + 1, a , b)          #call minvalue for ghosts layer
                
                if result[0] < v:
                    v = result[0]
                    action = act
                
                if v < a:                                                    #change the value of b if needed
                    return (v, action)

                b = min(b, v)

            return (v, action)

        result = max_value(gameState, 0, 0, -1e6, 1e6)                      #0 agent is pacman, a = -1000000 b = 1000000
        return result[1]

class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """

    def getAction(self, gameState):
        """
        Returns the expectimax action using self.depth and self.evaluationFunction

        All ghosts should be modeled as choosing uniformly at random from their
        legal moves.
        """
        "*** YOUR CODE HERE ***"
        #change the min function to chance value

        def terminal_test(gameState, depth):
            if((gameState.isWin() or gameState.isLose()) or depth == self.depth):                 #all terminal cases
                return True
            else:
                return False

        def max_value(currentstate, depth, pacman):
            actions = currentstate.getLegalActions(pacman)                  
            
            if terminal_test(currentstate, depth) == True:         
                return (self.evaluationFunction(currentstate), None)

            v = -1e6
            action = None                                              

            for a in actions:
                nextstate = currentstate.getNextState(pacman, a)
                ghost = 1
                result = chance_value(nextstate, depth, ghost)
                
                if result[0] > v:
                    v = result[0]
                    action = a
            
            return (v, action)


        def chance_value(currentstate, depth, ghost):
            actions = currentstate.getLegalActions(ghost)

            if terminal_test(currentstate, depth) == True:          
                return (self.evaluationFunction(currentstate), None)

            sum = 0

            for a in actions:
                nextstate= currentstate.getNextState(ghost, a)
                
                if (ghost == (currentstate.getNumAgents() - 1)):                   #if function is called for the last ghost then call max value
                    result = max_value(nextstate, depth + 1, 0)
                else:
                    result = chance_value(nextstate, depth, ghost + 1)             #call change_value for ghosts layer
                
                sum += result[0]                                                 

            v = sum/len(actions)                                                   #average of all returned values
            return (v, None)

        result = max_value(gameState, 0, 0)                             
        return result[1]

def betterEvaluationFunction(currentGameState):
    """
    Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
    evaluation function (question 5).

    DESCRIPTION: <write something here so we know what you did>
    """
    "*** YOUR CODE HERE ***"
    pos = currentGameState.getPacmanPosition()
    food = currentGameState.getFood()
    ghostStates = currentGameState.getGhostStates()

    score = currentGameState.getScore()

    for ghost in ghostStates:
        distance = manhattanDistance(pos,ghost.getPosition())
        if distance != 0:
            score += 1/distance  



    food = food.asList()
    for food in food:
        distance = manhattanDistance(pos, food)
        if distance != 0:
            score += 1/distance                        

    return score   

# Abbreviation
better = betterEvaluationFunction
