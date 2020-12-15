#!/usr/bin/env python
#-*- coding: utf-8 -*-

import collections

def access(node):
    print(node)

def bfs(graph, root): 
    visited, queue = set(), collections.deque([root])
    visited.add(root)
    access(root)
    while queue: 
        vertex = queue.popleft()
        for neighbour in graph[vertex]: 
            if neighbour not in visited: 
                visited.add(neighbour) 
                access(neighbour)
                queue.append(neighbour) 

if __name__ == '__main__':
    graph = {0: [1, 2], 1: [2], 2: [3], 3: [1,2]} 
    bfs(graph, 0)
    graph = {'0': set(['1', '2']),
         '1': set(['0', '3', '4']),
         '2': set(['0']),
         '3': set(['1']),
         '4': set(['2', '3'])}
    bfs(graph, '0')