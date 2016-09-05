"""
Given a collection of distinct numbers, return all possible permutations.

For example,
[1,2,3] have the following permutations:
[
  [1,2,3],
  [1,3,2],
  [2,1,3],
  [2,3,1],
  [3,1,2],
  [3,2,1]
]
"""


class Solution(object):

    def __init__(self):
        pass

    def permute(self, nums):
        """
        :type nums: List[int]
        :rtype: List[List[int]]
        """
        # solutions = self.permuteBacktrack(nums)
        solutions = self.permuteDP(nums)
        # solutions = self.permuteDPRollingArray(nums)
        return solutions

    def permuteDP(self, nums):
        """
        :type nums: List[int]
        :rtype: List[List[int]]

        Dynamic Programming solution to permutations problem
        state transition relationship:
            permutations[n] = n * permutations[n - 1]

        performance: 98.06%, 2016-09-04 18:32 CST
        """
        permutations = []

        if nums:
            permutations.append([[nums[0]]])
            # the dynamic programming
            for i in range(1, len(nums)):
                permutations_i = []
                permutations.append(permutations_i)
                #  state transition process
                for permutation_previous in permutations[i - 1]:
                    for j in range(i + 1):
                        permutation = list(permutation_previous)
                        permutation.insert(j, nums[i])
                        permutations_i.append(permutation)
        return permutations[-1]

    def permuteDPRollingArray(self, nums):
        """
        :type nums: List[int]
        :rtype: List[List[int]]

        Dynamic Programming solution to permutations problem
        state transition relationship:
            permutations[n] = n * permutations[n - 1]

        This is a dynamic programming solution with optimized space complexity. We are
        using rolling array here, so we don't have to store all those 1! + 2! + ... + (n - 1)!
        partial solutions

        Runtime performance:  beats 100.00%. 2016-09-05 14:33, CST
        """

        if not nums:
            return []

        permutations_curr = []
        permutations_curr.append([nums[0]])
        # the dynamic programming
        for i in range(1, len(nums)):
            permutations_prev = permutations_curr
            permutations_curr = []
            #  state transition process
            for permutation_prev in permutations_prev:
                for j in range(i + 1):
                    permutation = list(permutation_prev)
                    permutation.insert(j, nums[i])
                    permutations_curr.append(permutation)
        return permutations_curr

    def permuteBacktrack(self, nums, start=0):
        """
        :type nums: List[int]
        :rtype: List[List[int]]
        """
        if not hasattr(self, 'permutations'):
            self.permutations = []
        n = len(nums)
        if n - 1 <= start:
            self.permutations.append(list(nums))
        else:
            for i in range(start, n):
                self._swap(start, i, nums)
                self.permuteBacktrack(nums, start + 1)
                self._swap(start, i, nums)

        if not start:
            return self.permutations
        return

    @classmethod
    def _swap(cls, i, j, nums):
        nums[i], nums[j] = nums[j], nums[i]

    def permuteBacktrackIterative(self, nums):
        """
        :type nums: List[int]
        :rtype: List[List[int]]
        """
        if not hasattr(self, 'permutations'):
            self.permutations = []

        n = len(nums)

        class StackFrame(object):

            def __init__(self, start=-1, current=-1, candidate=-1):
                self.start = start
                # self.end       = end
                self.current = current
                self.candidate = candidate

        stack = []
        stack.append(StackFrame(0, 0, -1))
        while stack:
            frame = stack[-1]
            # generate and so on ...
            # when to pop or push
            if frame.start == n - 1 or frame.current == n - 1:
                stack.pop()
                self.permutations.append(list(nums))
            else:
                stack_new = StackFrame(frame.start + 1, 0, 0)
                stack.append(stack_new)
        pass

    def permuteLexicographic(self, nums):
        """
        :type nums: List[int]
        :rtype: List[List[int]]
        """
        pass

def test():
    for nums in [
        [1, 2, 3],
        [1],
    ]:
        print(Solution().permuteBacktrack(nums))
        print(Solution().permuteDP(nums))
        print(Solution().permuteDPRollingArray(nums))

if __name__ == '__main__':
    test()
