#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
406. Queue Reconstruction by Height

Total Accepted: 8375
Total Submissions: 15557
Difficulty: Medium
Contributors: Admin

Suppose you have a random list of people standing in a queue. Each person is described
by a pair of integers (h, k), where h is the height of the person and k is the number
of people in front of this person who have a height greater than or equal to h. Write
an algorithm to reconstruct the queue.

Note:
The number of people is less than 1,100.

Example

Input:
[[7,0], [4,4], [7,1], [5,0], [6,1], [5,2]]

Output:
[[5,0], [7,0], [5,2], [6,1], [4,4], [7,1]]


Hints:
What can you say about the position of the shortest person?
If the position of the shortest person is i, how many people would be in front of the shortest person?

Once you fix the position of the shortest person, what can you say about the position of the second shortest person?

================================================================================
SOLUTION

This problem has "larger than and before relation" involved.

1. Brute-force, greedy.

In a bubble sort manner?

VALUE COMPARISON involved, consider the ORDERING / MONOTONICITY and EXTREMUM.

2. Sort and insert - backward, decreasing order

Process the list backward, in a descending height order.
Add the elements into the result array. Then each element already in the result
array is greater than or equal to the current one to insert.

In another word, for current (h, k), k is the position to insert it!

Complexity: O(n²), O(n)

3. Sort and insert - increasing order

We can sort the array with height first, and then insert in an increasing order.
For the first element, k is its index in output array.
An increasing order, empty slots indicates larger or equal elements coming after.
So, for each element (h, k), it should be placed at the kth EMPTY SLOT.

How about elements with same height?
Insert one with larger k first will be easier since same h with smaller k can
take empty slots before larger k!

And finding such empty slots takes O(n).

Complexity: O(N²), O(N²)

4. Sort and insert - increasing order - binary search - range sum as count
The above solution takes O(N) to find right empty slot position.
Can we use binary search to speed up?
To use binary search, we need to know how many positions are taken before,
for each index i in [0,n-1].
And, this is RANGE QUERY! We can count as sum, with range query data structure!
We can use a binary indexed tree to store range sum(count of take positions).

Then for each element, finding an empty slot to insert takes O(log²N).

Complexity: O(Nlog²N)

3. Optimizing inserting with order statistics tree

To enable O(logn) insert, we can augment a balanced binary search tree
as order statistics tree.

But the implementation is absolutely nontrivial.

Complexity: O(nlogn), O(n)

4. Optimize inserting process - SQUARE ROOT DECOMPOSITION

Inserting an element at a index in the list is O(N). And this why the "sort and insert"
takes O(N²).

How to optimize it?

Well, the trick is to SQUARE ROOT DECOMPOSE the list into blocks.
Inserting takes O(N) because there are average N elements to move when inserting.
But how to keep the buckets balanced?

Decompose given array into small chunks specifically of size sqrt(n)!

Complexity: O(n sqrtn) = O(n√n)

5. Divide and conquer - merge sort - number of larger elements before self

Complexity: O(nlogn)

'''

class Solution(object):

    def reconstructQueue(self, people):
        """
        :type people: List[List[int]]
        :rtype: List[List[int]]
        """
        # result = self._reconstructQueueNaive(people)
        # result = self._reconstructQueueByHeightSortAndInsert(people)
        result = self._reconstructQueueByHeightSortAndInsertWithSqrtDecomposition(people)

        print(people, " => ", result)

        return result

    def _reconstructQueueNaive(self, people):
        """
        :type people: List[List[int]]
        :rtype: List[List[int]]

        At each round, find the most front one that can be appended into the queue
        """
        # FIXME: time limit exceeded
        queue = []

        def canInsert(person):
            num_higher = 0
            for front in queue:
                if front[0] >= person[0]:
                    num_higher += 1
            return num_higher == person[1]

        while people:
            print(queue, '<=====', people)
            next_person = None
            for i, person in enumerate(people):
                if canInsert(person) and (
                        next_person is None or person < people[next_person]):
                    next_person = i
                pass
            if next_person is not None:
                queue.append(people.pop(next_person))
            else:
                break

        return queue

    def _reconstructQueueByHeightSortAndInsert(self, people: list):
        """
        :type people: List[List[int]]
        :rtype: List[List[int]]

        Because in tuple (h, k), k is only affected by people in front of him that are of
        greater or equal height, inserting people with smaller height won't interfere its
        validity. Then we can reconstruct the queue in a descending order of height to reduce
        the time complexity when finding the next person to insert.
        """
        queue = []
        people.sort(key=lambda x: (-x[0], x[1]))
        for p in people:
            queue.insert(p[1], p)
        return queue

    # DONE: square root decomposition
    def _reconstructQueueByHeightSortAndInsertWithSqrtDecomposition(self, people: list):
        blocks = [[]]
        # sort by descending height h, ascending k
        for (h, k) in sorted(people, key=lambda p: (-p[0], p[1])):
            index = k
            block = blocks[0]
            for i, block in enumerate(blocks):
                m = len(block)
                if index <= m:
                    break
                index -= m

            block.insert(index, (h, k)) # O(sqrt(n))
            # XXX: rebalance
            if m * m > len(people):
                blocks.insert(i + 1, block[m//2:]) # amortized O(sqrt(n))
                del block[m//2:]

        return [p for block in blocks for p in block]

    # TODO: solution binary indexed tree with count as sum

def test():
    solution = Solution()
    people = [[7, 0], [4, 4], [7, 1], [5, 0], [6, 1], [5, 2]]
    assert solution.reconstructQueue(people)
    assert solution.reconstructQueue([]) == []

    print('self test passed')

    # Generate a large test case and time it.
    from bisect import bisect
    from random import randint, shuffle
    from timeit import timeit
    n = 300000
    heights = [randint(1, n) for _ in range(n)]
    standing = []
    people = []
    for h in heights:
        i = bisect(standing, -h)
        standing.insert(i, -h)
        people.append([h, i])
    shuffle(people)
    for solution in solution._reconstructQueueByHeightSortAndInsert, solution._reconstructQueueByHeightSortAndInsertWithSqrtDecomposition:
        print(timeit(lambda: solution(people), number=1))

if __name__ == '__main__':
    test()
