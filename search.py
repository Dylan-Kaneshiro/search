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

    print("Start:", problem.getStartState())
    print("Is the start a goal?", problem.isGoalState(problem.getStartState()))
    print("Start's successors:", problem.getSuccessors(problem.getStartState()))
    """
    "*** YOUR CODE HERE ***"

    def get_unvisited_successors(problem, cur_state, visited):
        return filter(lambda x: not x[0] in visited, problem.getSuccessors(cur_state))
    
    def trim_path(path_to_cur, parent_state):
        while not path_to_cur[-1][0] == parent_state:
            path_to_cur.pop()
        return path_to_cur
    
    stack = util.Stack()
    visited = set()

    cur_state = problem.getStartState()
    cur = (cur_state, None, None)
    for successor in problem.getSuccessors(cur_state):
        stack.push((successor, cur_state))
    path_to_cur = [cur]
    
    while(not problem.isGoalState(cur_state) and not stack.isEmpty()):
        
        # Update cur and cur_state
        cur, parent = stack.pop()
        cur_state = cur[0]

        # Update visited
        visited.add(cur_state)

        # Add children to stack
        for successor in get_unvisited_successors(problem, cur_state, visited):
            stack.push((successor, cur_state))
        
        # Update path_to_cur
        path_to_cur = trim_path(path_to_cur, parent)
        path_to_cur.append(cur)
    
    if problem.isGoalState(cur_state):
        # Compile path from start to goal
        return [t[1] for t in path_to_cur[1::]]
    else:
        print("Goal not found")
        return None

def breadthFirstSearch(problem):
    """Search the shallowest nodes in the search tree first."""
    "*** YOUR CODE HERE ***"
    def get_unvisited_successors(problem, cur_state, visited):
        return filter(lambda x: not x[0] in visited, problem.getSuccessors(cur_state))
    
    queue = util.Queue()
    visited = set() # items in this look like: (5,5)

    cur_state = problem.getStartState() # e.g. (5,5)
    cur = (cur_state, None, None) # e.g. ((5,4), 'South', 1)
    for successor in problem.getSuccessors(cur_state):
        queue.push((successor, cur_state))
        # items in queue data structure look like:
        # (((5,4), 'South', 1), (5,5))
    paths = {}
    
    while(not problem.isGoalState(cur_state) and not queue.isEmpty()):
        
        # Update cur and cur_state
        cur, parent = queue.pop()
        cur_state = cur[0]

        # Update visited
        visited.add(cur_state)

        # Add children to stack
        for successor in get_unvisited_successors(problem, cur_state, visited):
            queue.push((successor, cur_state))
        
        # Update paths
        paths[cur_state] = (parent, cur[1]) # e.g. paths[(5,4)] = ((5,5), 'South')

    
    if problem.isGoalState(cur_state):
        # Compile path from goal to start
        path = []
        while not cur_state == problem.getStartState():
            cur_state, action = paths[cur_state]
            path.append(action)
        path.reverse()
        return path
    else:
        print("Goal not found")
        return None

def uniformCostSearch(problem):
    """Search the node of least total cost first."""
    "*** YOUR CODE HERE ***"
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
    def get_unvisited_successors(problem, cur_state, visited):
        return filter(lambda x: not x[0] in visited, problem.getSuccessors(cur_state))
    
    queue = util.PriorityQueue()
    visited = set() # items in this look like: (5,5)

    cur_state = problem.getStartState() # e.g. (5,5)
    cur = (cur_state, None, None) # e.g. ((5,4), 'South', 1)
    for successor in problem.getSuccessors(cur_state):
        cur_cost = successor[2]
        priority = cur_cost + heuristic(successor[0], problem)
        queue.push((successor, cur_state, cur_cost), priority)
        # items in queue data structure look like:
        # (((5,4), 'South', 1), (5,5), 1)
    paths = {}
    
    while(not problem.isGoalState(cur_state) and not queue.isEmpty()):
        
        # Update cur and cur_state
        cur, parent, cur_cost = queue.pop()
        cur_state = cur[0]

        # Update visited
        visited.add(cur_state)

        # Add children to stack
        for successor in get_unvisited_successors(problem, cur_state, visited):
            cur_cost += successor[2]
            priority = cur_cost + heuristic(successor[0], problem)
            queue.push((successor, cur_state, cur_cost), priority)
        
        # Update paths
        paths[cur_state] = (parent, cur[1]) # e.g. paths[(5,4)] = ((5,5), 'South')


    if problem.isGoalState(cur_state):
        # Compile path from goal to start
        path = []
        while not cur_state == problem.getStartState():
            cur_state, action = paths[cur_state]
            path.append(action)
        path.reverse()
        return path
    else:
        print("Goal not found")
        return None



# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
