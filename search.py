#!/usr/bin/env python
# coding: utf-8

# In[1]:


from searchh import *
import numpy as np

# Needed to hide warnings in the matplotlib sections
import warnings
warnings.filterwarnings("ignore")


# In[2]:


usa_map = UndirectedGraph(dict(
    LosAngeles=dict(SanFrancisco=383, Austin=1377, Bakersville=153),
    SanFrancisco=dict(Bakersville=283, Seattle=807),
    Seattle=dict(SantaFe=1463, Chicago=2064),
    Bakersville=dict(SantaFe=864),
    Austin=dict(Dallas=195,Charlotte=1200 ), 
    SantaFe=dict(Dallas=640),
    Dallas=dict(NewYork=1548),
    Charlotte=dict(NewYork=634),
    NewYork=dict(Boston=225),
    Boston=dict(Chicago=983,Austin=1963, SanFrancisco=3095),
    Chicago=dict(SantaFe=1272)))


# In[10]:


def recursive_best_first_search(problem, h=None):
    """[Figure 3.26]"""
    h = memoize(h or problem.h, 'h')
    
    def RBFS(problem, node, flimit):
        print("-------------------------------")
        
        if problem.goal_test(node.state):
            
            return node, 0   # (The second value is immaterial)
        successors = node.expand(problem)
        if len(successors) == 0:
            return None, float('inf')
        for s in successors:
            s.f = max(s.path_cost + h(s), node.f)
        while True:
            # Order by lowest f value
            flag=0
            successors.sort(key=lambda x: x.f)
            best = successors[0]
            if best.f > flimit:
                flag=1
                
                print("Current city: ",node.state)
                print("f_limit :", flimit)
                print("Best : ",best.f)
               
                print("")
                print("-----Error")
                print("-------------------------------")
                
               
                return None, best.f
            if len(successors) > 1:
                alternative = successors[1].f
            else:
                alternative = float('inf')
            print("Current city: ",node.state)
            print("f_limit :", flimit)
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


# In[11]:


usa_problem = GraphProblem('Seattle', 'Dallas', usa_map)
print("------------------------------------RBFS---------------------------------------------------------------------------")
result=recursive_best_first_search(usa_problem).solution()
result.insert(0,"Seattle")
print("Final path", result)


# ## A\* SEARCH
# 
# Let's change all the node_colors to starting position and define a different problem statement.

# In[5]:


print("\n\n\n\n\n")


# In[6]:


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
    explored = set()
    while frontier:
        
        node = frontier.pop()
        print("")
        print("Current Node: ", node.state)
        print("Evaluation function (current node): ",f(node))
        if problem.goal_test(node.state):
            print("")
            print("Final Cost :",f(node))
            return node
        explored.add(node.state)
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


# In[7]:


all_node_colors = []
usa_problem = GraphProblem('Seattle', 'Dallas', usa_map)
print("------------------------------------A*---------------------------------------------------------------------------")
result=astar_search(usa_problem).solution()
result.insert(0,"Seattle")
print("Final path", result)


# In[ ]:




