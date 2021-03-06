#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
456. 132 Pattern

Given a sequence of n integers a1, a2, ..., an, a 132 pattern is a subsequence ai, aj, ak such
that i < j < k and ai < ak < aj. Design an algorithm that takes a list of n numbers as input
and checks whether there is a 132 pattern in the list.

Note: n will be less than 15,000.

Example 1:
Input: [1, 2, 3, 4]

Output: False

Explanation: There is no 132 pattern in the sequence.
Example 2:
Input: [3, 1, 4, 2]

Output: True

Explanation: There is a 132 pattern in the sequence: [1, 4, 2].
Example 3:
Input: [-1, 3, 2, 0]

Output: True

Explanation: There are three 132 patterns in the sequence: [-1, 3, 2], [-1, 3, 0] and [-1, 2, 0].

==============================================================================================
SOLUTION

1. Brute force

Track the state of 3-tuples.
Exhaust all possible 3-tuples, and verify.

Complexity: O(N³)

2. Improved brute force with some greedy strategy

Idea: Fix '1' as minimum so far, exhaust all possible '3' and '2' pairs.

For '1', it's optimal to always choose the minimum number so far.
For '3', it can be any number after '1'.
For '2', it can be any number after '3'.

Scan the list, keep track of the minimum as '1'. For every number in the list, try to treat it
as '3',  and search for '2' after it.

Fixing minimum value so far as '1', reduce O(n) to O(1) for finding '1'.

Complexity: O(N²)

3. Divide and conquer
Still, keep track  of 3-tuple state.

Brute force method involves duplicate computations, with some greedy strategy or insights,
it shall be reduced.

This is an order model. After MONOTONICITY analysis or EXTREMA POINTS analysis, we can
find the maximum as '3', then divide and conquer.

We have some greedy strategy of choosing '1' and '3': local minimums and local maximums.

Find the maximum, and there are three scenarios:
    1) Target pattern is on the left of this maximum number
    2) Target pattern is on the right
    3) Target pattern contains this maximum number, as a '3'.

Complexity
O(NlogN), O(1)

But the worst case complexity is O(N²). To reduce that, we can build a range maximum query
data structure, such as a segment tree. Then complexity is reduced to O(NlogN)

Space complexity O(N).

4. Stack of non-overlapping intervals

Idea: maintain a list of ['1', '3'] pairs/intervals, try to find possible '2' within range.

An array can be partitioned into a set of sequence monotonic increasing or decreasing subarray.

For each monotonic subarray, we can locate corresponding local extrema: local minima and local maxima.
Then a first greedy strategy is:
    when choose '1', we can always choose LOCAL MINIMUM within a monotonic subarray.

The second greedy strategy:
    when choose '3', we can always choose LOCAL MAXIMUM within a monotonic subarray.
Then choosing '2' would be easy: verify the largest element after '3'.

Problem: How about this case: [1, 4, -1, 2, 5, 7]

No clue yet: doesn't work...

--------------------------------------------------------------------------------
Think it as INTERVAL overlapping problem?

132 pattern is actually finding such number 2 that is within range (1, 3).

--------------------------------------------------------------------------------
The key state of the problem is the local minimum points and local maximum points.

A greedy strategy will be choosing local minimums as '1', and local maximums as '3'.
Then try to find 2 that is within the range.

Represent increasing subarrays by intervals like [local mininum, local maximum].
If intervals overlap, then we have found '132' pattern.

Every time we encounter a local minimum point, we have a range start value 'lmin'.
And for any number in the increasing subsequence beginning with 'lmin', we have
a range end value 'lmax', and we have a temporary interval.

Maintain a stack of decreasing non-overlapping intervals.
Why decreasing? Because if a new interval is larger, then we will merge it into a new one,
because of the greedy property.

Then the state transition regarding to intervals are: merge, push and pop intervals.

--------------------------------------------------------------------------------
Then, scan the array, and for each new element:
1) If it's within the stack top interval: found solution!
2) If it's local minimum: we have a new interval start 'lmin'
3) If it's larger than previous number, we have a temporary interval end 'lmax'
And try to merge the intervals:
1) If it OVERLAPS with an interval within the stack, then pattern is found
2) If NON-OVERLAPPING, then push the new interval into the stack. And still keep
the interval start 'lmin'. In this case, the new interval must be below stack top one.
3) If new interval INCLUDES the stack top interval, then merge them.

Repeat above procedures.

5. STACK - Backward induction - finding 3, min array, decreasing stack of '2'

Idea: Use minimum so far as '1', maintain a list of possible '2', and linear search for '3'.

Still keep track of state of individual numbers '1', '3' and '2'.

In improved brute force method, fixing minimum so far as '1',
reduces O(n) to O(1) for finding '1'.
The idea is to fix global minimum so far as '1', and keep a list of potential
'2', and scan the list to find proper '3', and updating '2' meanwhile.

Note that, the minimum value function is monotonically decreasing!

If scanning the array backward, then the minimum '1' is increasing.
So shall be the '2'.

Denote the min[j] as the minimum value of subarray [0, ..., j].

Scan the list backward, at each position i, we have  min[i] <= nums[i].
Now if we have a potential '2', denoted as n2. Then there are several case:
    1) min[i] < n2  < nums[i]: found!
    2) n2 <= min[i]: discard n2, and find a larger oner, since min[i] is
increasing, n2 have no change of being '2'
    3) n2 = nums[i]:  just keep one of them, as potential '2'.
    4) n2 > nums[i]:  there is a change for both nums[i] and n2 being '2'.

This indicates maintaining a monotonically decreasing stack of '2'.

6. Finding '1', keep decreasing stack of '3'

Idea: Maintain a list of possible '3', and linear search for '1', '2' can be
determined by maximum number less than '3'.

Both '3' and '2' have greedy strategy to choose!

'2' can be found by greedily choosing the maximum number that has a larger
element, '3' before it.

Scan the array backward. For each number n, treat it as '1'. If there is a
match, then we found it. If n is larger than current '3', then greedily
choose n as the new '3', and choose the maximum number less than n, as the '2'.

This is be done with a MONOTONICALLY DECREASING STACK of '3'.

--------------------------------------------------------------------------------
Reference: https://leetcode.com/articles/132-pattern/

'''

from _decorators import timeit

class Solution(object):

    @timeit
    def find132pattern(self, nums):
        """
        :type nums: List[int]
        :rtype: bool
        """
        # result = self._find132patternExtreama(nums)
        # result = self._find132patternDivideAndConquer(nums)
        # result = self._find132patternIntervalStack(nums)
        # result = self._find132patternNumberStackFind3(nums)
        result = self._find132patternNumberStackFind1(nums)

        print(nums[:100], result)

        return result

    def _find132patternExtreama(self, nums):
        """
        DON'T LOOK AT IT.

        Wrong answer
        """
        minIndices = [] # local minima
        maxIndices = [] # local maxima

        for i in range(0, len(nums) - 2):
            if nums[i] < nums[i + 1] and (i == 0 or nums[i]  <= nums[i - 1]):
                minIndices.append(i)
        for i in range(1, len(nums) - 1):
            if nums[i] > nums[i + 1] and ( nums[i]  >= nums[i - 1]):
                maxIndices.append(i)
        for i in minIndices:
            for j in maxIndices:
                if j < i or nums[j] <= nums[i] or nums[j + 1] <= nums[i]:
                    continue
                return True

        return False

    def _find132patternDivideAndConquer(self, nums):
        # FIXME: time limit exceeded for worst case O(N²)
        # Maybe a range query data structure like segment tree will do...
        def argmax(low, high, upper_bound=float('inf')):
            iMax, vMax = -1, float('-inf')
            for i in range(low, high + 1):
                if upper_bound >= nums[i] > vMax:
                    iMax, vMax = i, nums[i]
            return iMax, vMax

        def dfs(low, high):
            if high - low <= 1:
                return False
            # find 3
            i3, v3 = argmax(low + 1, high - 1)
            pivot = i3
            if i3 == -1: return False
            # find 2
            i2, v2 = argmax(i3 + 1, high, v3 - 1)
            if i2 == -1:
                return dfs(low, i3 - 1) or dfs(i3 + 1, high)
            # find 1
            i1, v1 = argmax(low, i3 - 1, v2 - 1)
            if i1 == -1:
                return dfs(low, i3 - 1) or dfs(i3 + 1, high)

            return True
        return dfs(0, len(nums) - 1)

    def _find132patternIntervalStack(self, nums):
        intervals = []
        lmin, lmax = -1, -1
        for i, e in enumerate(nums):
            if intervals:
                low, high = intervals[-1]
                if nums[low] < e < nums[high]: return True # found
            # new interval
            if (i == 0 or nums[i - 1] >= nums[i]) and (i < len(nums) - 1 and nums[i + 1] > nums[i]):
                lmin = i
                continue # local minimum
            elif i and nums[i] > nums[i - 1]: lmax = i # increasing sequence
            else: continue # decreasing sequence, but not local minimum
            while intervals:
                low, high = intervals[-1]
                if nums[low] >= nums[lmax]: break # new interval is below previous ones
                elif nums[low] < nums[lmax] < nums[high]: return True # overlapping
                elif nums[high] <= nums[lmin]:
                    intervals.pop()
                    lmin = low # new interval is above previous one, merge
                else:
                    intervals.pop() # replace. Containing: lmin <= low < high <= lmax
            intervals.append([lmin, lmax]) # push new interval into stack
        return False

    # DONE: backward scan
    def _find132patternNumberStackFind3(self, nums):
        mins = [float('inf') for _ in range(len(nums))]
        stack = [] # stack of '2'
        for i in range(len(nums)):
            mins[i] = min(mins[i - 1] if i else float('inf'), nums[i]) # [-1, -1, -1]
        for i in range(len(nums) - 1, -1, -1):
            while stack and stack[-1] <= nums[i]:
                n2 = stack.pop()
                if mins[i] < n2 < nums[i]: return True
            stack.append(nums[i]) # [2]
        return False

    def _find132patternNumberStackFind1(self, nums):
        n2 = float('-inf')
        stack = [] # stack of '3'
        for n in reversed(nums):
            if n < n2: return True
            while stack and stack[-1] < n:
                n2 = stack.pop()
            stack.append(n)
        return False


def test():
    solution = Solution()

    assert solution.find132pattern([]) is False
    assert solution.find132pattern([-1]) is False
    assert solution.find132pattern([-1, 3]) is False
    assert solution.find132pattern([-1, 3, 2])
    assert solution.find132pattern([1, 2, 3, 4]) is False
    assert solution.find132pattern([3, 1, 4, 2])
    assert solution.find132pattern([-1, 3, 2, 0])
    assert solution.find132pattern([1, 5, -1, 0, -3, -2, 4])
    assert solution.find132pattern([1, 0, 1, -4, -3]) is False

    import yaml
    with open("./132Pattern.json", "r") as f:
        records = yaml.load(f)
    for record in records:
        assert solution.find132pattern(record['input']) == record['output']

    print("self test passed")

if __name__ == '__main__':
    test()
