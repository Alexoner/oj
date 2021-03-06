#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
349. Intersection of Two Arrays

Total Accepted: 60656
Total Submissions: 134199
Difficulty: Easy
Contributors: Admin

Given two arrays, write a function to compute their intersection.

Example:
Given nums1 = [1, 2, 2, 1], nums2 = [2, 2], return [2].

Note:
Each element in the result must be unique.
The result can be in any order.

================================================================================
SOLUTION

1. Brute force
For each element in nums1, check existence in nums2 and avoid duplicate.

Complexity: O(mn).

2. Hash table/set

Complexity: O(n) + O(m).

3. Sort and two pointers

Complexity: O(nlogn) + O(mlogm) + O(m + n).

4. Sort and binary search

Complexity: O(nlogn) + O(mlogm) + O(mlogn).

'''

class Solution(object):

    def intersection(self, nums1, nums2):
        """
        :type nums1: List[int]
        :type nums2: List[int]
        :rtype: List[int]
        """
        return self.intersectionSet(nums1, nums2)

    def intersectionSet(self, nums1, nums2):
        """
        :type nums1: List[int]
        :type nums2: List[int]
        :rtype: List[int]
        """
        return list(set(nums1) & set(nums2))

def test():
    solution = Solution()

    assert solution.intersection([1, 2, 1, 1], [2, 2]) == [2]

    print('self test passed')

if __name__ == '__main__':
    test()
