#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
124. Binary Tree Maximum Path Sum

Total Accepted: 80294
Total Submissions: 324647
Difficulty: Hard
Contributors: Admin

Given a binary tree, find the maximum path sum.

For this problem, a path is defined as any sequence of nodes from some starting node to any
node in the tree along the parent-child connections. The path must contain at least one node
and does not need to go through the root.

For example:
Given the below binary tree,

       1
      / \
     2   3
Return 6.
==============================================================================================
SOLUTION:

In this problem, a path is actually composed of two branches starting with some node v,
each of which is a path from v to its some distant child(neighbor).

The problem STATE is composite, it would be easier to decompose it into a tuple of
simpler ones with respect to a particular root node.
Define simple path as any path starting from a predecessor to a descendant node.

Simple STATE:
    (maximum left simple path sum ending here, maximum right simple path sum ending here)

1. Basic BRUTE-FORCE solution:
    The start node could be any of all nodes.
    Traverse ALL THE NODES, and check their maximum sum left and right paths starting
there. This procedure involves lots of repeated computation.

Check maximum sum of left and right paths takes average O(N). So the overall
time complexity is O(N²).

2. Bottom-up state transition.
A path sum problem shares some similarity with maximum subarray problem, which both have
overlapping subproblems and optimal substructure. Parent vertices depend on its neighbors
(children). So there is a Dynamic Programming solution.

And the maximum path sum ending here depends on the maximum path sum ending with its direct
descendants.

DEFINE STATE to contain enough information for RECURRENCE RELATION.
STATE AS TUPLE of (max_ending_here, max_so_far).

max_ending_here: the maximum sum of path from some distant neighbor(child) up to current node
max_so_far: maximum sum of two paths starting from/ending with current node to some two
distant neighbors.

For each vertex in the tree, there are two scenarios for max_ending_here state transition:
1. Current max path consists only one element at the position
2. Current maximum path consists of one more element than the previous maximum path.

Then we have RECURRENCE RELATION to its neighbors(children). And the STATE contains full
information for different scenarios in the recurrence relation, so repeated calculations
can be spared.

Transit STATE via RETURN VALUE to solve the overlapping optimal substructure in a BOTTOM-UP/
BACKWARD manner.

'''

# Definition for a binary tree node.
class TreeNode(object):

    def __init__(self, x):
        self.val = x
        self.left = None
        self.right = None

class Solution(object):

    def maxPathSum(self, root):
        """
        :type root: TreeNode
        :rtype: int
        """
        return self.maxPathSumRecursion(root)

    def maxPathSumRecursion(self, root):
        """
        :type root: TreeNode
        :rtype: int
        """
        def dfs(node):
            if not node:
                return 0, float('-inf')
            left, right = dfs(node.left), dfs(node.right)
            max_ending_here = max(left[0] + node.val, right[0] + node.val, node.val)
            max_so_far = max(max_ending_here, left[1], right[1], left[0] + right[0] + node.val,)
            # print(node, max_ending_here, max_so_far)
            return max_ending_here, max_so_far

        t = dfs(root) if root else (0, 0)
        print(t, '\n')
        return t[1]

    def maxPathSum2Recursion(self, root):
        """
        :type root: TreeNode
        :rtype: int

        For follow-up problem where a path is defined as a sequence of nodes starting
        from some node down to some children via parent-child connections
        """
        def dfs(node):
            if not node:
                return 0, float('-inf')
            left, right = dfs(node.left), dfs(node.right)
            max_ending_here = max(left[0] + node.val,
                                  right[0] + node.val,
                                  left[0] + right[0] + node.val,
                                  node.val
                                 )
            max_so_far = max(left[1], right[1], max_ending_here)
            print(node, max_ending_here, max_so_far)
            return max_ending_here, max_so_far



def test():

    from serializeAndDeserializeBinaryTree import Codec

    solution = Solution()

    root = Codec.deserialize("[]", int)
    assert solution.maxPathSum(root) == 0

    root = Codec.deserialize("[-3]", int)
    assert solution.maxPathSum(root) == -3

    root = Codec.deserialize("[1,2,3]", int)
    assert solution.maxPathSum(root) == 6

    root = Codec.deserialize('[3,5,1,6,2,0,8,null,null,7,4]', int)
    assert solution.maxPathSum(root) == 26

    root = Codec.deserialize('[3,5,1,6,2,0,8,null,null,-7,4]', int)
    assert solution.maxPathSum(root) == 23

    root = Codec.deserialize('[1, 2, 3,null, null, -4, 5]', int)
    assert solution.maxPathSum(root) == 11

    print('self test passed')

if __name__ == '__main__':
    test()
