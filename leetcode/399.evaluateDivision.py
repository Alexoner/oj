#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
399. Evaluate Division

Total Accepted: 5245
Total Submissions: 13888
Difficulty: Medium
Contributors: Admin

Equations are given in the format A / B = k, where A and B are variables represented
as strings, and k is a real number (floating point number). Given some queries, return
the answers. If the answer does not exist, return -1.0.

Example:
Given a / b = 2.0, b / c = 3.0.
queries are: a / c = ?, b / a = ?, a / e = ?, a / a = ?, x / x = ? .
return [6.0, 0.5, -1.0, 1.0, -1.0 ].

The input is: vector<pair<string, string>> equations, vector<double>& values,
vector<pair<string, string>> queries , where equations.size() == values.size(),
and the values are positive. This represents the equations. Return vector<double>.

According to the example above:

equations = [ ["a", "b"], ["b", "c"] ],
values = [2.0, 3.0],
queries = [ ["a", "c"], ["b", "a"], ["a", "e"], ["a", "a"], ["x", "x"] ].
The input is always valid. You may assume that evaluating the queries will
result in no division by zero and there is no contradiction.

SOLUTION
================================================================================
The problem can be modeled as a GRAPH problem where variables are graph VERTICES
and the quotients are EDGES connecting vertices.

Then it can be solved by search the graph with depth-first search or breadth-first search.
1. Graph search traversal

2. Floyd-warshall
We are to find vertex to vertex path in a directed graph.

'''

class Solution(object):

    def calcEquation(self, equations, values, queries):
        """
        :type equations: List[List[str]]
        :type values: List[float]
        :type queries: List[List[str]]
        :rtype: List[float]
        """
        # result = self.calcEquationBFS(equations, values, queries)
        result = self.calcEquationFloydWarshall(equations, values, queries)

        print(result)

        return result

    def calcEquationBFS(self, equations, values, queries):
        adj = self._buildGraph(equations, values, queries)
        result = []
        for query in queries:
            result.append(self._BFS(query, adj))

        return result

    def _BFS(self, query, adj):
        '''
        Graph search with BFS

        32ms, beats 98.14%, 2016-10-30 18:02
        '''
        i, j = query
        if not (i in adj and j in adj):
            return -1.0
        # search
        frontier, visited = [i], {i}

        while frontier:
            v = frontier.pop(0)
            if v == j:
                return adj[i][j]
            for u in adj[v].keys():
                # push
                if u not in visited:
                    adj[i][u] = adj[i][v] * adj[v][u] # path compression & memoize
                    frontier.append(u)
                    visited.add(u)
                pass
            pass

        return -1.0

    def calcEquationFloydWarshall(self, equations, values, queries):

        # TODO: submit
        adj = self._buildGraph(equations, values, queries)
        adj = self.floydWarshall(adj)

        result = []
        for query in queries:
            if query[0] not in adj or query[1] not in adj:
                result.append(-1)
            else:
                result.append(adj[query[0]][query[1]])

        return result

    def floydWarshall(self, adj):
        '''
        Adapt floyd warshall dynamic programming algorithm for all pairs shortest path in graph.

        Process is like a matrix multiplication.

        '''
        # floyd-warshall algorithm
        # adj = self._buildGraph(equations, values, queries)
        result = []
        for k in adj.keys(): # increase intermediate vertices set when tracking state
            # changed = False
            for i in adj.keys(): # vertex i
                for j in adj.keys(): # possible edge from i to j
                    if j in adj[i]: continue # already computed, and no contradiction, no need to compare
                    if k in adj[i] and j in adj[k]:
                        adj[i][j] = adj[i][k] * adj[k][j]
                        adj[j][i] = 1/adj[i][j]
                        # changed = True
            # if not changed: break
        return adj

    def unionFind(self, query, adj):
        '''
        Graph search with BFS

        '''
        # TODO: union-find algorithm?

    def _buildGraph(self, equations, values, queries):
        '''
        Build the graph represented by sparse matrix(actually it's a dictionary)

        adj[i][j] = v: means (variable i/variable j = v)
        '''
        adj = {}
        for i, equation in enumerate(equations):
            adj.setdefault(equation[0], {})
            adj.setdefault(equation[1], {})
            adj[equation[0]][equation[0]] = 1.0
            adj[equation[1]][equation[1]] = 1.0

            adj[equation[0]][equation[1]] = values[i]
            adj[equation[1]][equation[0]] = 1.0 / values[i]
            pass
        # for _, query in enumerate(queries):
            # adj.setdefault(query[0], {})
            # adj.setdefault(query[1], {})
            # adj[query[0]][query[0]] = 1.0
            # adj[query[1]][query[1]] = 1.0
            # pass

        # print(adj)
        return adj

def test():
    solution = Solution()
    assert solution.calcEquation(
        [["a", "b"], ["b", "c"]],
        [2.0, 3.0],
        [["a", "c"], ["b", "a"], ["a", "e"], ["a", "a"], ["x", "x"]]) == \
        [6.00000, 0.5, -1.00000, 1.00000, -1.00000]
    print('self test passed')

if __name__ == '__main__':
    test()
