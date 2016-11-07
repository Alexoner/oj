#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
297. Serialize and Deserialize Binary Tree

Total Accepted: 36380
Total Submissions: 118822
Difficulty: Hard
Contributors: Admin

Serialization is the process of converting a data structure or object into a sequence of
bits so that it can be stored in a file or memory buffer, or transmitted across a network
connection link to be reconstructed later in the same or another computer environment.

Design an algorithm to serialize and deserialize a binary tree. There is no restriction on
how your serialization/deserialization algorithm should work. You just need to ensure that
a binary tree can be serialized to a string and this string can be deserialized to the
original tree structure.

For example, you may serialize the following tree

    1
   / \
  2   3
     / \
    4   5
as "[1,2,3,null,null,4,5]", just the same as how LeetCode OJ serializes a binary tree. You
do not necessarily need to follow this format, so please be creative and come up with
different approaches yourself.

Note: Do not use class member/global/static variables to store states. Your serialize and
deserialize algorithms should be stateless.
'''

# Definition for a binary tree node.
class TreeNode(object):

    def __init__(self, x):
        self.val = x
        self.left = None
        self.right = None

    def __repr__(self):
        return 'val = {}'.format(self.val)

class Codec:

    def serialize(self, root):
        """Encodes a tree to a single string.

        :type root: TreeNode
        :rtype: str
        """
        return self.serializeBFS(root)

    def deserialize(self, data):
        """Decodes your encoded data to tree.

        :type data: str
        :rtype: TreeNode
        """
        return self.deserializeBFS(data)

    def serializeBFS(self, root):
        """Encodes a tree to a single string.

        :type root: TreeNode
        :rtype: str
        """
        data = []
        frontier = [root]
        while frontier:
            vertex = frontier.pop(0)
            data.append(str(vertex.val) if vertex else 'null')
            if vertex:
                frontier.append(vertex.left)
                frontier.append(vertex.right)
            pass

        while data and data[-1] == 'null':
            data.pop()
        print('BFS result:', data)
        return '[{}]'.format(','.join(data))

    def deserializeBFS(self, data):
        """Decodes your encoded data to tree.

        :type data: str
        :rtype: TreeNode
        """
        if len(data) <= 2:
            return None
        data = data[1:-1]
        vertices = data.split(',')

        val = vertices.pop(0)
        root = TreeNode(val) if val != 'null' else None
        frontier = [root] if root else []
        while frontier and vertices:
            vertex = frontier.pop(0)
            left, right = vertices.pop(0), vertices.pop(0) if vertices else 'null'
            if left != 'null':
                vertex.left = TreeNode(left)
                frontier.append(vertex.left)
            else:
                vertex.left = None

            if right != 'null':
                vertex.right = TreeNode(right)
                frontier.append(vertex.right)
            else:
                vertex.right = None

        return root



# Your Codec object will be instantiated and called as such:
def test():
    codec = Codec()

    root = codec.deserialize("[]")
    assert codec.serialize(root) == "[]"

    assert codec.serialize(codec.deserialize("[1,2]")) == "[1,2]"

    root = codec.deserialize("[1,2,3,null,null,4,5]")
    assert codec.serialize(root) == "[1,2,3,null,null,4,5]"

    root = codec.deserialize("[null,2,3,null,null,4,5]")
    assert codec.serialize(root) == "[]"



test()