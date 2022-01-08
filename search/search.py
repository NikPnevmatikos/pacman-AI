# search.py
# ---------
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


"""
In search.py, you will implement generic search algorithms which are called by
Pacman agents (in searchAgents.py).
"""

from sys import path
import util

class SearchProblem:
    """
    This class outlines the structure of a search problem, but doesn't implement
    any of the methods (in object-oriented terminology: an abstract class).

    You do not need to change anything in this class, ever.
    """

    def getStartState(self):
        """
        Returns the start state for the search problem.
        """
        util.raiseNotDefined()

    def isGoalState(self, state):
        """
          state: Search state

        Returns True if and only if the state is a valid goal state.
        """
        util.raiseNotDefined()

    def expand(self, state):
        """
          state: Search state

        For a given state, this should return a list of triples, (child,
        action, stepCost), where 'child' is a child to the current
        state, 'action' is the action required to get there, and 'stepCost' is
        the incremental cost of expanding to that child.
        """
        util.raiseNotDefined()

    def getActions(self, state):
        """
          state: Search state

        For a given state, this should return a list of possible actions.
        """
        util.raiseNotDefined()

    def getActionCost(self, state, action, next_state):
        """
          state: Search state
          action: action taken at state.
          next_state: next Search state after taking action.

        For a given state, this should return the cost of the (s, a, s') transition.
        """
        util.raiseNotDefined()

    def getNextState(self, state, action):
        """
          state: Search state
          action: action taken at state

        For a given state, this should return the next state after taking action from state.
        """
        util.raiseNotDefined()

    def getCostOfActionSequence(self, actions):
        """
         actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.
        The sequence must be composed of legal moves.
        """
        util.raiseNotDefined()


def tinyMazeSearch(problem):
    """
    Returns a sequence of moves that solves tinyMaze.  For any other maze, the
    sequence of moves will be incorrect, so only use this for tinyMaze.
    """
    from game import Directions
    s = Directions.SOUTH
    w = Directions.WEST
    return  [s, s, w, s, w, w, s, w]


def depthFirstSearch(problem):
    """
    Search the deepest nodes in the search tree first.

    Your search algorithm needs to return a list of actions that reaches the
    goal. Make sure to implement a graph search algorithm.

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:

    print("Start:", problem.getStartState())
    print("Is the start a goal?", problem.isGoalState(problem.getStartState()))
    """
    "*** YOUR CODE HERE ***"
    frontier = util.Stack()
    frontier.push(problem.getStartState())
    expanded = set()
    pathtostate = dict()                                    #key state will have a list of actions needed to get to that state
    pathtostate = {problem.getStartState() : []}
    while frontier.isEmpty() == False:
        node = frontier.pop()
        if(problem.isGoalState(node) == True):
            return pathtostate[node]
        if((node in expanded) == False):
            expanded.add(node)
            for i in problem.expand(node):
                frontier.push(i[0])
                pathtostate[i[0]] = pathtostate[node] + [i[1]]             #path to child i[0] will be the path of the parent + action to get to child
                
    #return None    
    util.raiseNotDefined()

def breadthFirstSearch(problem):
    """Search the shallowest nodes in the search tree first."""
    "*** YOUR CODE HERE ***"
    frontier = util.Queue()
    frontier.push(problem.getStartState())
    expanded = set()
    pathtostate = dict()
    pathtostate = {problem.getStartState() : []}
    
    while frontier.isEmpty() == False:
        node = frontier.pop()
        if(problem.isGoalState(node) == True):
            return pathtostate[node]
        if((node in expanded) == False):
            expanded.add(node)
            for i in problem.expand(node):
                frontier.push(i[0])
                if(i[0] in pathtostate.keys()):                     #if child in dictionary then check if current path is better than previous one
                    anotherpath = pathtostate[node] + [i[1]]
                    if(problem.getCostOfActionSequence(anotherpath) < problem.getCostOfActionSequence(pathtostate[i[0]])):
                        pathtostate[i[0]] = anotherpath
                else:
                    pathtostate[i[0]] = pathtostate[node] + [i[1]]  
    util.raiseNotDefined()

def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def aStarSearch(problem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    "*** YOUR CODE HERE ***"
    frontier = util.PriorityQueue()
    frontier.push(problem.getStartState(), None)
    expanded = set()
    pathtostate = dict()
    pathtostate = {problem.getStartState() : []}
    
    while frontier.isEmpty() == False:
        node = frontier.pop() 
        if(problem.isGoalState(node) == True):
            return pathtostate[node]
        if((node in expanded) == False):
            expanded.add(node)
            for i in problem.expand(node):
                anotherpath = pathtostate[node] + [i[1]]
                if ((i[0] not in pathtostate.keys()) or (problem.getCostOfActionSequence(anotherpath) < problem.getCostOfActionSequence(pathtostate[i[0]]))):
                    pathtostate[i[0]] = anotherpath
                    priority = problem.getCostOfActionSequence(pathtostate[i[0]]) + heuristic(i[0], problem)
                    frontier.push(i[0], priority)

    util.raiseNotDefined()


# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
