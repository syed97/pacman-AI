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

    def getSuccessors(self, state):
        """
          state: Search state

        For a given state, this should return a list of triples, (successor,
        action, stepCost), where 'successor' is a successor to the current
        state, 'action' is the action required to get there, and 'stepCost' is
        the incremental cost of expanding to that successor.
        """
        util.raiseNotDefined()

    def getCostOfActions(self, actions):
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
    print "Start:", problem.getStartState()
    print "Is the start a goal?", problem.isGoalState(problem.getStartState())
    print "Start's successors:", problem.getSuccessors(problem.getStartState())
    """

    "*** YOUR CODE HERE ***"
    # DFS stack
    stack = util.Stack()
    visited = set()
    startState = problem.getStartState()
    stack.push((startState, [])) # (state, actions) pair

    while not stack.isEmpty():
        pos, actions = stack.pop()
        # print("popped item")
        # print("pos:",pos)
        # print("actions:", actions)
        # print("==========================================")

        # check if goal state reached - then returns actions to get to goal
        if problem.isGoalState(pos):
            return actions
        
        if pos not in visited:
            visited.add(pos) # mark curr pos as visited

            successors = problem.getSuccessors(pos)

            for successorState, successorAction, successorStepCost in successors:
                # print("pos: ", pos)
                # print("actions: ", actions)
                if successorState not in visited:
                    updatedActions = actions + [successorAction]
                    # print("updatedActions: ", updatedActions)
                    stack.push((successorState, updatedActions))
    return []

def breadthFirstSearch(problem):
    """Search the shallowest nodes in the search tree first."""
    "*** YOUR CODE HERE ***"
    # BFS queu
    queue = util.Queue()
    visited = set()
    startState = problem.getStartState()
    queue.push((startState, [])) # (state, actions) pair

    while not queue.isEmpty():
        pos, actions = queue.pop()
        
        # check if goal state reached - then returns actions to get to goal
        if problem.isGoalState(pos):
            return actions
        
        if pos not in visited:
            visited.add(pos) # mark curr pos as visited

            successors = problem.getSuccessors(pos)

            for successorState, successorAction, successorStepCost in successors:
                updatedActions = actions + [successorAction]
                queue.push((successorState, updatedActions))
    return []

def uniformCostSearch(problem):
    """Search the node of least total cost first."""
    "*** YOUR CODE HERE ***"
    pq = util.PriorityQueue()
    visited = {}
    startState = problem.getStartState()
    pq.push((startState, [], 0), 0) # (state, actions, cumulative cost), priority

    while not pq.isEmpty():
        pos, actions, cumulativeCost = pq.pop()

        # if least path cost for that node already exists - skip traversal
        if pos in visited and visited[pos] <= cumulativeCost:
            continue
        
        if problem.isGoalState(pos):
            return actions
        
        visited[pos] = cumulativeCost # mark visited

        successors = problem.getSuccessors(pos)

        for successorState, successorAction, successorStepCost in successors:
            updatedSuccessorCost = cumulativeCost + successorStepCost
            # update fringe/PQ with new node or update cumulative path cost for already visited node
            if successorState not in visited or updatedSuccessorCost < visited[successorState]:
                updatedActions = actions + [successorAction]
                pq.update((successorState, updatedActions, updatedSuccessorCost), updatedSuccessorCost)
    return []


def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def aStarSearch(problem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    "*** YOUR CODE HERE ***"
    pq = util.PriorityQueue()
    startState = problem.getStartState()
    visited = {}
    pq.push((startState, [], 0), 0) # (state, actions, cost), priority - based on heuristic f = g + h

    while not pq.isEmpty():
            pos, actions, gCost = pq.pop()

            fCost = gCost + heuristic(pos,problem)

            # if least path cost for that node already exists - skip traversal
            if pos in visited and visited[pos] <= fCost:
                continue

            if problem.isGoalState(pos):
                return actions
            
            # mark visited
            visited[pos] = fCost

            successors = problem.getSuccessors(pos)

            for succState, succActions, succgCost in successors:
                newgCost = gCost + succgCost
                newfCost = newgCost + heuristic(succState, problem)
                # note: can also remove the below if statement - works the same
                if succState not in visited or newfCost < visited[succState]:
                    newActions = actions + [succActions]
                    pq.push((succState, newActions, newgCost), newfCost)
    return []


# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
