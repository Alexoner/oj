#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
215. Kth Largest Element in an Array

Total Accepted: 89831
Total Submissions: 245221
Difficulty: Medium
Contributors: Admin

Find the kth largest element in an unsorted array. Note that it is the kth largest element in
the sorted order, not the kth distinct element.

For example,
Given [3,2,1,5,6,4] and k = 2, return 5.

Note:
You may assume k is always valid, 1 ≤ k ≤ array's length.

===============================================================================================
SOLUTION

1. Sort.
Complexity: O(NlogN)

----------------------------------------------------------------------------------------------
SELECTION ALGORITHM to find the kth ORDER STATISTICS.

2. Min heap

Maintain a MIN HEAP of size k, and scan the list, if the current number is bigger then the
heap top element, then replace the heap top with the current element, and then maintain the
heap structure. The heap top element is the kth largest element.

Complexity: O(NlogK)

3. Maintain a sorted list of size k, do insert with BINARY SEARCH.
Complexity: O(NlogK)

4. Quick select: divide and conquer by PARTITIONING

In quick sort, in each iteration, we need to select a pivot and then PARTITION the array into
three parts:
    1. Elements smaller than the pivot;
    2. Elements equal to the pivot;(for three-way partition)
    3. Elements larger than the pivot.

To find the kth largest element,
    1. Initialize left to be 0 and right to be nums.size() - 1;
    2. Partition the array, if the pivot is at the k-1-th position, return it (we are done);
    3. If the pivot is right to the k-1-th position, update right to be the left neighbor of
the pivot;
    4. Else update left to be the right neighbor of the pivot.
    5. Repeat 2.

Time Complexity:
    So, in the average sense, the problem is reduced to approximately half of its original size,
giving the recursion
        T(n) = T(n/2) + O(n)
in which O(n) is the time for partition. This recursion, once solved, gives
        T(n) = O(logn) + O(n) = O(n)
and thus we have a linear time solution. Note that since we only need to consider one half
of the array, the time complexity is O(n).

If we need to consider both the two halves of the array, like quicksort, then the recursion will be
        T(n) = 2T(n/2) + O(n)
and the complexity will be O(nlogn).

Of course, O(n) is the average time complexity. In the worst case, the recursion may become
        T(n) = T(n - 1) + O(n) and the complexity will be O(N²).

----------------------------------------------------------------------------------------------
Divide and Conquer time complexity analysis
Master theorem - time complexity given the recurrence relation.

The ultimate time complexity master theorem, given the recurrence relation.

1. T(n) = 2T(n/2) + O(n) = O(NlogN),
This is the case considering both parts of the division.

Expand the expression:
    T(n) = 2T(n/2) + O(n)
         = O(n) + 2T(n/2)
         = O(n) + 2[2T(n/4) + O(n/2)]
         = O(n) + 2²T(n/2²) + 2O(n/2)
         = O(n) + O(n) + 2²T(n/2²)
         = 2O(n) + 2²T(n/2²)
         = nO(n) + 2^(log₂n)T(n/(2^log₂n))
         = ...
         = log₂n O(n) + n(T(1))
         = O(nlog₂n) + n
         = O(nlog₂n)

2. T(n) = 2T(n/2) + O(logN) = O(NlogN)
This is a scenario where pre-process to build a data structure, like tree, to achieve O(logN)
query. But the tree is a static data structure, meaning the subproblem T(n/2) still needs O(logN),
not O(log(n/2)) time complexity.

Expand the expression:
T(n) = 2T(n/2) + O(logN)
     = 2(2(T(n/2²) + O(logn))) + O(logn)
     = 2²T(n/2²) + 2¹O(logn) + O(logn)
     = O(logn) + 2¹O(logn) + 2²T(n/2²)
     = O(logn) + 2¹O(logn) + ... + 2^{logn - 1}O(logn) + 2^{logn}T(n/2^{logn})
     = O(logn) + 2¹O(logn) + ... + 2^{logn - 1}O(logn) + 2^{logn}T(n/2^{logn})
     = ... # using geometric progression sum formula
     = nO(log₂n) + n
     = O(nlog₂n)

3. T(n) = 2T(n/2) + O(1) = O(n)

Expand the expression:
T(n) = 2T(n/2) + O(1)
     = 2(2(T(n/2²) + O(1))) + O(1)
     = O(1) + 2¹O(1) + ... + 2^{logn}O(1) + 2^{logn}T(n/2^{logn})
     = O(1) + 2¹O(1) + ... + 2^{logn}O(1) + 2^{logn}T(1)
     = O(1) + 2¹O(1) + ... + 2^{logn}O(1) + n
     = O(1) + 2¹O(1) + ... + 2^{logn}O(1) + n
     = O(3n - 1)
     = O(n)

4.  T(n) = T(n/2) + O(n) = O(n),
This is the case considering single part of the division.

Expand the expression:
    T(n) = T(n/2) + O(n)
         = O(n) + T(n/2)
         = O(n) + (T(n/4 + O(n/2))
         = O(n) + T(n/2²) + O(n/2)
         = O(n) + O(n/2) + T(n/2²)
         = 1/2⁰O(n) + O(n/2¹) + T(n/2²)
         = 1/2⁰O(n) + O(n/2¹) + O(n/2²) + ...  + O(n/2^{log₂n}) + T(n/2^{log₂n})
         = ... # forming an geometric progression
         = O(n) (1x(1 - (1/2)^{log₂n})/ (1 - 1/2)) + T(n/n)
         = O(n) (1x(1 - (1/2)^{log₂n})/ (1 - 1/2)) + T(1)
         = O(n) 2(1 - 1/n) + T(1)
         = O(2n -2)  + T(1)
         = O(n)

5. T(n) = T(n/2) + O(1) = O(logn)
Expand the expression:
    T(n) = T(n/2) + O(1)
         = O(1) + O(1) + T(n/2²)
         = O(1) + O(1) + ... + O(1) + T(n/2^{logn})
         = logn O(1) + T(1)
         = O(logn)

6. T(n) = T(n - 1) + O(n) = O(n²)
Similar expansion like above.
Expand the expression:
    T(n) = T(n - 1) + O(n)
         = T(n - 2) + O(n) + O(n - 1)
         = ...
         = T(1) + O(n) + O(n - 1) + ... + O(1)
         = O(n(n+1)/2) + T(1)

7. T(n) = T(n-1)+T(n-2)+...+T(1)
=> T(n+1) = T(n)+T(n-1)+T(n-2)+...+T(1)
=>T(n+1) = 2T(n)

T(n) = O(2ⁿ)

'''

from heapq import heappush, heappop
import random

class Solution(object):

    def findKthLargest(self, nums, k):
        """
        :type nums: List[int]
        :type k: int
        :rtype: int
        """
        # result = self._findKthLargestSort(nums, k)
        # result = self._findKthLargestHeap(nums, k)
        result = self._findKthLargestPartition(nums, k)

        print(nums, k, " => ", result)

        return result

    def _findKthLargestSort(self, nums, k):
        """
        :type nums: List[int]
        :type k: int
        :rtype: int
        """
        return sorted(nums, reverse=True)[k - 1]

    def _findKthLargestBinarySearch(self, nums, k):
        """
        :type nums: List[int]
        :type k: int
        :rtype: int
        """
        # TODO: binary search insertion sort

    def _findKthLargestHeap(self, nums, k):
        """
        :type nums: List[int]
        :type k: int
        :rtype: int
        """
        # DONE: min heap
        heap = []
        for num in nums:
            if len(heap) < k:
                heappush(heap, num)
            elif heap[0] < num:
                heappop(heap)
                heappush(heap, num)

        return heap[0]

    def _findKthLargestPartition(self, nums: list, k: int) -> int:
        def partition(arr, low, high):
            pivot = arr[high]
            i = low # partition pointer: all elements on left are SMALLER than pivot!
            # SWEEP the sequence
            for j in range(low, high):
                if arr[j] <= pivot:
                    arr[i], arr[j] = arr[j], arr[i]
                    i += 1
            arr[i], arr[high] = arr[high], arr[i]
            # print(low, high, i, arr)
            return i

        def partitionThreeWay(arr: list, low: int, high: int):
            """
            Dutch national flag partition method, robust to repeated elements.

            Partition the array into three parts with two partition pointers:
                smaller than pivot, equal to pivot, larger than pivot.

            Reference: https://en.wikipedia.org/wiki/Dutch_national_flag_problem
            """
            pivot = arr[high]
            smaller, j, greater = low, low, high
            while j <= greater:
                if arr[j] < pivot:
                    arr[smaller], arr[j] = arr[j], arr[smaller]
                    smaller += 1
                    j += 1
                elif arr[j] > pivot:
                    arr[j], arr[greater] = arr[greater], arr[j]
                    greater -= 1
                else: j += 1
            return smaller, greater

        def partitionRandomized(arr, low, high, randomize=True):
            # DONE: randomized partition
            # randomly CHOOSE THE PIVOT
            rand = random.randint(low, high)
            arr[rand], arr[high] = arr[high], arr[rand]

            return partition(arr, low, high)

       # DONE: quick select, partition to divide and conquer
        idx = len(nums) - k # the target order statistics index
        low, high = 0, len(nums) - 1
        while low <= high:
            # q = partition(nums, low, high)
            q = partitionRandomized(nums, low, high)
            if q < idx:
                low = q + 1
            elif q > idx:
                high = q - 1
            else:
                return nums[q]

def test():
    solution = Solution()
    arr = [2, 8, 7, 1, 8, 3, 5, 6, 4, 2]
    # partition(arr, 0, len(arr) - 1)
    # assert arr == [2, 1, 2, 8, 8, 3, 5, 6, 4, 7]
    # arr = [6, 5]
    # partition(arr, 0, 1)
    # assert arr == [5, 6]

    assert solution.findKthLargest([1], 1) == 1
    assert solution.findKthLargest([3, 2, 1, 5, 6, 4], 2) == 5
    print('self test passed')

test()
