#!/usr/bin/env python
# coding: utf-8

# In[15]:


from searchhmc import *
import numpy as np

# Needed to hide warnings in the matplotlib sections
import warnings
warnings.filterwarnings("ignore")


# In[32]:


mc_map = UndirectedGraph(dict(
    One=dict(Two=1, Thirteen=1, Fourteen=1),
    Two=dict(Three=1),
   Three=dict(Four=1),
    Four=dict(Five=1),
    Five=dict(Six=1), 
    Six=dict(Seven=1),
    Seven=dict(Eight=1),
   Eight=dict(Nine=1),
    Nine=dict(Ten=1),
    Ten=dict(Eleven=1,Fifteen=1),
    Eleven=dict(Twelve=1),
    Thirteen=dict(Three=1)))


# In[71]:


def depth_limited_search(problem, limit=50):
    """[Figure 3.17]"""

    def recursive_dls(node, problem, limit):
        if problem.goal_test(node.state):
            return node
        elif limit == 0:
            return 'cutoff'
        else:
            cutoff_occurred = False
            for child in node.expand(problem):
                result = recursive_dls(child, problem, limit - 1)
                if result == 'cutoff':
                    cutoff_occurred = True
                elif result is not None:
                    return result
            return 'cutoff' if cutoff_occurred else None

    # Body of depth_limited_search:
    return recursive_dls(Node(problem.initial), problem, limit)


def iterative_deepening_search(problem):
    """[Figure 3.18]"""
    for depth in range(sys.maxsize):
        result = depth_limited_search(problem, depth)
        if result != 'cutoff':
            return result


# In[72]:


mc_problem = GraphProblem('One', 'Twelve', mc_map)
print("---------------------Iterative Deepening Search--------------------------------------------------------------------")
result=iterative_deepening_search(mc_problem).solution()
result.insert(0,"One")
print("Final path", result)


# In[ ]:


print("\n\n\n\n\n")


# ## A\* SEARCH
# 
# Let's change all the node_colors to starting position and define a different problem statement.

# In[35]:


print("\n\n\n\n\n")


# In[59]:


def best_first_graph_search(problem, f):
    """Search the nodes with the lowest f scores first.
    You specify the function f(node) that you want to minimize; for example,
    if f is a heuristic estimate to the goal, then we have greedy best
    first search; if f is node.depth then we have breadth-first search.
    There is a subtlety: the line "f = memoize(f, 'f')" means that the f
    values will be cached on the nodes as they are computed. So after doing
    a best first search you can examine the f values of the path returned."""
    f = memoize(f, 'f')
    node = Node(problem.initial)
    if problem.goal_test(node.state):
        return node
    frontier = PriorityQueue(min, f)
    frontier.append(node)
    explored = []
    while frontier:
        
        node = frontier.pop()
        print("")
        print("Current Node: ", node.state)
        print("Evaluation function (current node): ",f(node))
        if problem.goal_test(node.state):
            print("")
            print("Total Cost: ",f(node) )
            return node
        explored.append(node.state)
        for child in node.expand(problem):
            
            if child.state not in explored and child not in frontier:
                frontier.append(child)
            elif child in frontier:
                incumbent = frontier[child]
                if f(child) < f(incumbent):
                    del frontier[incumbent]
                    frontier.append(child)
        print("Explored : ",explored)
        print("Frontier : ",frontier.__c__())
        
       
    return None

def astar_search(problem, h=None):
    """A* search is best-first graph search with f(n) = g(n)+h(n).
    You need to specify the h function when you call astar_search, or
    else in your Problem subclass."""
    h = memoize(h or problem.h, 'h')
    return best_first_graph_search(problem, lambda n: n.path_cost + h(n))


# In[60]:


all_node_colors = []
mc_problem = GraphProblem('One', 'Twelve', mc_map)
print("------------------------------------A*---------------------------------------------------------------------------")
result=astar_search(mc_problem).solution()
result.insert(0,"One")
print("Final path", result)


# In[78]:


def recursive_best_first_search(problem, h=None):
    """[Figure 3.26]"""
    h = memoize(h or problem.h, 'h')
    
    def RBFS(problem, node, flimit):
        print("-------------------------------")
        print("Current city: ",node.state)
        print("f_limit :", flimit)
        if problem.goal_test(node.state):
            
            return node, 0   # (The second value is immaterial)
        successors = node.expand(problem)
        if len(successors) == 0:
            return None, float('inf')
        for s in successors:
            s.f = max(s.path_cost + h(s), node.f)
        while True:
            # Order by lowest f value
            successors.sort(key=lambda x: x.f)
            best = successors[0]
            if best.f > flimit:
                return None, best.f
            
            if len(successors) > 1:
                alternative = successors[1].f
            else:
                alternative = float('inf')
            
            print("Best : ",best.f)
            print("Next City :",best.state)
            print("Alternate :", alternative)
            
            result, best.f = RBFS(problem, best, min(flimit, alternative))
            if result is not None:
                return result, best.f
            
    node = Node(problem.initial)
    node.f = h(node)
    result, bestf = RBFS(problem, node, float('inf'))
    return result


# In[79]:


mc_problem = GraphProblem('One', 'Twelve', mc_map)
print("------------------------------------RBFS---------------------------------------------------------------------------")
result = recursive_best_first_search(mc_problem).solution()
result.insert(0,"One")
print("Final path", result)


# In[ ]:




