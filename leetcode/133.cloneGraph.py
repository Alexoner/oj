#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
133. Clone Graph

Total Accepted: 85039
Total Submissions: 341037
Difficulty: Medium
Contributors: Admin

Clone an undirected graph. Each node in the graph contains a label and a list of its neighbors.


OJ's undirected graph serialization:
Nodes are labeled uniquely.

We use # as a separator for each node, and , as a separator for node label and each neighbor
of the node.
As an example, consider the serialized graph {0,1,2#1,2#2,2}.

The graph has a total of three nodes, and therefore contains three parts as separated by #.

First node is labeled as 0. Connect node 0 to both nodes 1 and 2.
Second node is labeled as 1. Connect node 1 to node 2.
Third node is labeled as 2. Connect node 2 to node 2 (itself), thus forming a self-cycle.
Visually, the graph looks like the following:

       1
      / \
     /   \
    0 --- 2
         / \
         \_/

===============================================================================================
SOLUTION:
    TRAVERSE the original graph with breadth-first search or depth-first search.
    A graph may consists of not only TREE EDGES, but also FORWARD EDGES, BACKWARD EDGES and
CROSS EDGES. So use a HASH TABLE to maintain association from old node(label) to new node,
thus avoiding duplicate instantiation of vertices.

1. Depth first search the old graph, in the meanwhile construct copied graph vertices and its
neighbors.

Avoid duplicate copies of vertices of same value by using a hash table, mapping from vertex
label to copied vertex.

Avoid infinite search in cycle of the graph by checking whether a copied vertex has already
been visited. This can be done without extra space: check whether its neighbors has been
assigned or not.

##############################################################################################
FOLLOW UP

1. Can we do it without hash table?
2. What if the graph is very big?

==============================================================================================
SOLUTION
1. Without hash table, not without extra space.
If the graph is represented as matrix, or adjacency list, or edges, it would be easily done.

2. Open ended question, talk to the interviewer!
Big, how?


'''

# Definition for a undirected graph node
class UndirectedGraphNode:

    def __init__(self, x):
        self.label = x
        self.neighbors = []

class Graph(object):

    def __init__(self, groups):
        self.label2node = {}

        def getNode(x):
            if x not in self.label2node:
                self.label2node[x] = UndirectedGraphNode(x)
            return self.label2node.get(x)

        for group in groups:
            node = getNode(group[0])
            print('construct', group[0])
            for label in group[1:]:
                print('\tneighbor', label)
                neighbor = getNode(label)
                node.neighbors.append(neighbor)

    def bfs(self, node=None):
        serialization = ''
        node = node or self.label2node[0]
        frontier = [node]
        visited = set()
        while frontier:
            vertex = frontier.pop(0)
            serialization = serialization + '#' + str(vertex.label)
            for neighbor in vertex.neighbors:
                serialization += ',' + str(neighbor.label)
                if neighbor not in visited:
                    frontier.append(neighbor)
                    visited.add(neighbor)

        print('graph:', serialization[1:])

class Solution:
    # @param node, a undirected graph node
    # @return a undirected graph node

    def cloneGraph(self, node):
        return self.cloneGraphBFS(node)
        # return self.cloneGraphDFS(node)

    def cloneGraphBFS(self, node: UndirectedGraphNode):
        """
        The cloning of a graph in a breadth-first search manner.
        """
        if not node:
            return None
        label2node = {}

        def getNode(x):
            if x not in label2node:
                label2node[x] = UndirectedGraphNode(x)
            return label2node.get(x)

        node_new = getNode(node.label)
        # XXX: FIRST-IN FIRST-OUT queue frontier
        frontier = [node]
        while frontier:
            # XXX: explore the frontier
            vertex = frontier.pop(0)
            vertex_new = getNode(vertex.label)
            # avoid infinite loop; vertices may have DUPLICATE neighbors
            if vertex_new.neighbors: continue
            print('clone', vertex_new.label)
            for neighbor in vertex.neighbors:
                neighbor_new = getNode(neighbor.label)
                print('\tneighbor', neighbor_new.label)
                vertex_new.neighbors.append(neighbor_new)
                frontier.append(neighbor)

        return node_new

    def cloneGraphDFS(self, node: UndirectedGraphNode):
        """
        The cloning of a graph in a depth-first search manner.
        """
        if not node:
            return None
        label2node = {}

        def getNode(x):
            if x not in label2node:
                label2node[x] = UndirectedGraphNode(x)
            return label2node.get(x)

        node_new = getNode(node.label)
        # XXX: LAST-IN FIRST-OUT queue frontier
        frontier = [node]
        while frontier:
            # XXX: explore the frontier
            vertex = frontier.pop()
            vertex_new = getNode(vertex.label)
            # avoid infinite loop; vertices may have DUPLICATE neighbors
            if vertex_new.neighbors: continue
            print('clone', vertex_new.label)
            for neighbor in vertex.neighbors:
                neighbor_new = getNode(neighbor.label)
                print('\tneighbor', neighbor_new.label)
                vertex_new.neighbors.append(neighbor_new)
                frontier.append(neighbor)

        return node_new

def test():
    solution = Solution()

    graph = Graph([[0, 1], [1, 2], [2, 2]])
    graph.bfs()
    # print('graph construction de-serialization test passed\n')

    graph.bfs(solution.cloneGraph(graph.label2node[0]))

    graph = Graph([[0, 1, 5], [1, 2, 5], [2, 3], [3, 4, 4], [4, 5, 5], [5]])
    graph.bfs()
    graph.bfs(solution.cloneGraph(graph.label2node[0]))

    print('self test passed')

if __name__ == '__main__':
    test()
