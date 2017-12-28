#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
84. Largest Rectangle in Histogram

Total Accepted: 76666
Total Submissions: 300455
Difficulty: Hard
Contributors: Admin

Given n non-negative integers representing the histogram's bar height where the width
of each bar is 1, find the area of largest rectangle in the histogram.

[img](./largest_rectangle_in_histogram_i.png)

Above is a histogram where width of each bar is 1, given height = [2,1,5,6,2,3].

[img](./largest_rectangle_in_histogram_ii.png)

The largest rectangle is shown in the shaded area(5, 6), which has area = 10 unit.

For example,
Given heights = [2,1,5,6,2,3],
return 10.

==============================================================================================
SOLUTION:

1. Brute-force.
Find all pairs in O(N²), and compute area in O(1),

f(i, j) = min(height[i, ..., j]) * (j - i + 1),  1 <= i, j <=  n
And we want to get max(f(i, j)).

i, j pairs are of O(N²) complexity, since it involves two loops.
(j - i + 1) is O(1) time complexity, and get query the range minimum is of O(0) because
we can keep track of that while iterating with j index in the inner loop.

Complexity: O(N²).

2. Divide and conquer

The above solution involves duplicate computations.

When computing area of a rectangle formed by a group of bars, the height is decided by the
bar with minimal height. This can form a greedy strategy to eliminate some duplicate cases.

There exists a minimum height in the histogram.

And there is a greedy strategy:
If incorporating the minimum bar into the rectangle, there is no need to compute all possible
rectangles, because among those rectangles including this minimal height bar, the one
starting and ending with two ends of the histogram will have the maximum area.

----------------------------------------------------------------------------------------------
Find the minimum, divide the problem into two parts.


The max area is maximum of three scenarios:
a) Maximum area in left side of minimum height bar (exclusive)
b) Maximum area in right side of minimum height bar (inclusive)
c) Maximum area obtained by number of bars multiplied by minimum height.

But if we use naive divide and conquer, the worst case time complexity could be O(N²).
Complexity
T(n) = 2T(n/2) + O(n), so average time complexity is O(NlogN).
Worst case is O(N²).

3. Divide and conquer optimized

Duplicate calculations of range minimum query, when computing area bounded by a pair of bars.
Linear scanning for range minimum query is O(n) complexity.

Can we optimize the range minimum query process?
Preprocessing the array to build segment tree, sparse table, binary indexed tree?

If we build a range minimum query data structure, of course not look up table with O(N²), with
a tree data structure. Then rmq takes O(logN).

But, unfortunately, the average time complexity isn't reduced.
Because the tree is built only once, every subproblem takes same time complexity to do
range minimum query, O(logN), regardless of the smaller size of subproblem.
The complexity is still O(nlogn) on average.

However, THE WORST CASE COMPLEXITY IS REDUCED to O(nlogn)!

Complexity: O(nlogn) for both average and worst case!

For large data set with length 20000, the speed up can be 1400 times in worst case in theory!
15033.65/

4. Linear algorithm?

Stack or or linear model?
Monotonic analysis?


  2 1 5 6 2 3
2 2
1
5
6
2
3

'''

from _tree import SegmentTree
from _decorators import timeit

class Solution(object):

    @timeit
    def largestRectangleArea(self, heights):
        """
        :type heights: List[int]
        :rtype: int
        """
        # result = self._largestRectangleAreaRMQ(heights)
        # result = self._largestRectangleAreaDivideAndConquer(heights)
        # result = self._largestRectangleAreaDivideAndConquerIterative(heights)
        result = self._largestRectangleAreaDivideAndConquerRMQ(heights)

        # print(heights, ", result: ", result)
        return result

    def _largestRectangleAreaDivideAndConquer(self, heights: list) -> int:
        # FIXME: recursive implementation exceeds maximum recursion depth...
        def dfs(left, right):
            # print(left, right)
            if left > right:
                return 0
            iMin, hMin = 0, float('inf')
            for i in range(left, right+1):
                if heights[i] < hMin:
                    iMin = i # 1
                    hMin = heights[i] # 1
            area = max(hMin * (right - left + 1), dfs(left, iMin - 1), dfs(iMin + 1, right)) # max(6, 2, max(8, 10, 3))
            return area

        area = dfs(0, len(heights) - 1) # 0, 5
        return area

    def _largestRectangleAreaDivideAndConquerIterative(self, heights: list) -> int:
        # FIXME: still O(N²), in worst case.
        area = 0
        stack = [(0, len(heights) - 1)]

        while stack:
            left, right = stack.pop()
            # print(left, right)
            if left > right: continue
            iMin, hMin = 0, float('inf')
            for i in range(left, right+1):
                if heights[i] < hMin:
                    iMin = i # 1
                    hMin = heights[i] # 1
            area = max(area, hMin * (right - left + 1))

            stack.append((left, iMin - 1))
            stack.append((iMin + 1, right))

        # area = dfs(0, len(heights) - 1) # 0, 5
        return area

    def _largestRectangleAreaDivideAndConquerRMQ(self, heights: list) -> int:
        """
        Divide and conquer optimized with efficient range minimum query to reduce worst case complexity
        Comlexity: O(nlogn)

        Runtime: 1516 ms
        """
        # DONE: build range minimum query data structure
        tree = SegmentTree(heights, 'rmq')

        area = 0
        stack = [(0, len(heights) - 1)]
        while stack:
            left, right = stack.pop()
            if left > right: continue
            # DONE: efficient range minimum query
            iMin = tree.query(left, right, index=True)
            hMin = heights[iMin]
            area = max(area, hMin * (right - left + 1))

            stack.append((left, iMin - 1))
            stack.append((iMin + 1, right))

        return area

    # TODO: linear algorithm

def test():
    solution = Solution()

    assert solution.largestRectangleArea([]) == 0
    assert solution.largestRectangleArea([0]) == 0
    assert solution.largestRectangleArea([1]) == 1
    assert solution.largestRectangleArea([0, 1]) == 1
    assert solution.largestRectangleArea([1, 1]) == 2
    assert solution.largestRectangleArea([1, 1]) == 2
    assert solution.largestRectangleArea([2, 1, 5, 6, 2, 3]) == 10
    assert solution.largestRectangleArea([1, 2, 3, 4, 5, 6]) == 12

    # large data test
    import yaml
    data = []
    with open("./largestRectangleInHistogram.json", "r") as f:
        data = yaml.load(f)
    for record in data:
        assert solution.largestRectangleArea(record['input']) == record['output']

    print("large data set passed!")

    print('self test passed')

if __name__ == '__main__':

    test()
