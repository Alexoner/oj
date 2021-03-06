#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
395. Longest Substring with At Least K Repeating Characters

Find the length of the longest substring T of a given string (consists of lowercase letters only)
such that every character in T appears no less than k times.

Example 1:

Input:
s = "aaabb", k = 3

Output:
3

The longest substring is "aaa", as 'a' is repeated 3 times.
Example 2:

Input:
s = "ababbc", k = 2

Output:
5

The longest substring is "ababb", as 'a' is repeated 2 times and 'b' is repeated 3 times.


================================================================================
SOLUTION

1. Brute force
Enumerate all possible substrings and verify.

Complexity: O(N²)

2. Divide and conquer

The method above involves duplicate computations, some which can be eliminated by
divide and conquer.

If a character appears less than k times, then the target sub-string can never include it.
Divide the string into several parts without this character, and get the largest one.

For example, s = "ababbc", k = 2, divide it into s1 = "ababb" and s2 = "c"

And actually, this resembles the graph search process.

Complexity
Average case is T(n) = 2T(n/2) + n, giving T(n) = O(NlogN).
Similar to quick sort partition, if each partition only gets [0, n - 1] and [n, n].
Then the worst case is O(N²).


3. Optimization of above divide and conquer algorithm
1) More efficient range query?
The problem of above solution is, after dividing the string, how to efficiently decide
whether there is a character that appears less than k times?

This is a range query problem, binary index tree or segment tree?

2) Reduce the worst case complexity
Instead dividing the string into two parts using just one character, we can partition
the original string into multiple parts. Split the string using all character that
are not eligible.

2. Greedy strategy?
Some greedy strategy.

3. State transition - prefix sum/count
Prefix sum?

Build a prefix sum of character occurrences count.
Then, the occurrences count function is MONOTONE INCREASING!
This means we can use BINARY SEARCH!

At each position, we have 26 characters to consider.
If a character, say it's 'a', occurs c times. Then we need to find
the lower bound index at which 'a' occurs c - k times or c times.
Now the search space is shrunk for next character 'b'. Repeat the process.

Since binary search is guaranteed to be O(logn), the complexity is always
O(nlogn).

4. State transition - Two pointers?

Initialize two pointers i = 0, j = n - 1?

A sliding window of what constraints?
When to shrink the window?

We don't know when to shrink the window because there are multiple different
characters, and they may make up for the missing count later.

The trick is to maintain a sliding window with at most specific number of
distinct characters.
A substring, contains at most 26 distinct characters. And it can be exhausted.
Then we can maintain a siding window containing at most h distinct characters,
where h is in [1, 26]. Shrink the window when distinct characters exceed h.
And a match is found when all character occurrences in window exceed k.

Complexity: O(26n).

'''


from collections import Counter

class Solution(object):

    def longestSubstring(self, s, k):
        """
        :type s: str
        :type k: int
        :rtype: int
        """
        # result = self._longestSubstringSlidingWindow(s, k)
        result = self._longestSubstringDivideAndConquer(s, k)
        print(s, k, "result: ", result)
        return result

    def _longestSubstringSlidingWindow(self, s, k):
        counter = Counter(s)
        pass

    def _longestSubstringDivideAndConquer(self, s, k):
        def dfs(string):
            if not string:
                return 0
            if len(string) < k:
                return 0
            count = [[] for _ in range(26)]
            for i, c in enumerate(string):
                count[ord(c) - ord('a')].append(i) # a: [0,1,2], b: [3,4]
            for i, _ in enumerate(count):
                if len(count[i]) >= k or len(count[i]) == 0: continue
                result = 0
                count[i].append(len(string)) # add a dummy sentinel # b: [3,4,5]
                for j, idx in enumerate(count[i]):
                    begin = (count[i][j - 1] + 1) if j else 0
                    result = max(result, dfs(string[begin:idx]))
                return result

            return len(string)
        return dfs(s)

    # TODO: optimization. Import worst case performance?
    # TODO: linear solution?

def test():
    solution = Solution()

    assert solution.longestSubstring("", 3) == 0
    assert solution.longestSubstring("", 0) == 0
    assert solution.longestSubstring("a", 0) == 1
    assert solution.longestSubstring("a", 1) == 1
    assert solution.longestSubstring("a", 2) == 0
    assert solution.longestSubstring("ab", 2) == 0
    assert solution.longestSubstring("ab", 1) == 2
    assert solution.longestSubstring("aba", 1) == 3
    assert solution.longestSubstring("aabaaa", 2) == 3
    assert solution.longestSubstring("aadaabccc", 2) == 3
    assert solution.longestSubstring("aabaaa", -2) == 6
    assert solution.longestSubstring("abcde", 3) == 0
    assert solution.longestSubstring("abcde", 2) == 0
    assert solution.longestSubstring("abcde", 1) == 5
    assert solution.longestSubstring("aaabb", 3) == 3
    assert solution.longestSubstring("aacbb", 3) == 0
    assert solution.longestSubstring("aacbbb", 3) == 3
    assert solution.longestSubstring("ababbc", 2) == 5
    assert solution.longestSubstring("ababa", 2) == 5
    assert solution.longestSubstring("abcdabcd", 2) == 8

    print("self test passed")

if __name__ == '__main__':
    test()

