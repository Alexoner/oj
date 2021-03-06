#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
237. Delete Node in a Linked List

Total Accepted: 118624
Total Submissions: 263250
Difficulty: Easy
Contributors: Admin

Write a function to delete a node (except the tail) in a singly linked list, given only
access to that node.

Supposed the linked list is 1 -> 2 -> 3 -> 4 and you are given the third node with value 3, the
linked list should become 1 -> 2 -> 4 after calling your function.

================================================================================
SOLUTION

1. Copy next node to current node's memory

How about deleting the last node in the linked list?

'''
# Definition for singly-linked list.
class ListNode(object):

    def __init__(self, x):
        self.val = x
        self.next = None

class Solution(object):

    def deleteNode(self, node):
        """
        :type node: ListNode
        :rtype: void Do not return anything, modify node in-place instead.
        """
        if node.next:
            node.val = node.next.val
            node.next = node.next.next
        else:
            # TODO: delete the last node?
