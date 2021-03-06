#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
342. Power of Four

Total Accepted: 53539
Total Submissions: 142365
Difficulty: Easy
Contributors: Admin

Given an integer (signed 32 bits), write a function to check whether it is a power of 4.

Example:
Given num = 16, return true. Given num = 5, return false.

Follow up: Could you solve it without loops/recursion?

==============================================================================================
SOLUTION

1. Recursively divide by 4, check whether the result is 1.

2. Bit manipulation - function mapping - square of power of 2
Every power of 4 has a corresponding power of 2, which is the square root.
4ⁿ = 2ⁿ*2ⁿ

And for each power of 2,
2ⁿ = 0b10...0, where there are n zeroes after 1. Removing last bit 1 gives 0.
4ⁿ = 2ⁿ*2ⁿ = 0b10...0,  2n zeroes after 1.
2n zeroes after 1, which means bit 1 is on odd bits!
Then use mask 0b0101=0x5!

Complexity: O(32)

3. Bit manipulation - power of 2 and modulo 3 .

4. Bit manipulation - convert to double and check

'''

class Solution(object):

    def isPowerOfFour(self, num):
        """
        :type num: int
        :rtype: bool
        """
        # return self.isPowerOfFourRecursion(num)
        return self.isPowerOfFourBitSquareOfPowerOfTwo(num)
        # return self.isPowerOfFourBit2(num)

    def isPowerOfFourRecursion(self, num):
        while num > 1:
            num /= 4.0
        return num == 1

    def isPowerOfFourBitSquareOfPowerOfTwo(self, num):
        """
        Validate only one bit 1, and it's on odd position.
        """
        # return num > 0 and (num & (num-1)) == 0 and (num & 0x55555555) == num
        return num > 0 and (num & (num-1)) == 0 and (num & 0b01010101010101010101010101010101) == num

    def isPowerOfFourBit2(self, num):
        '''
        Use n & (n - 1) to eliminate the trailing 1, validating whether it's
        power of 2.

        Lemma: All power of four integers n, (n-1) is always divisible by 3.
        Proof: 4^x - 1 = (2^x + 1)(2^x - 1). And 2^x % 3 in {1, 2}.
        If 2^x % 3 = 1, then 2^x - 1 % 3 = 0, proved. And it's likewise with 2.
        '''
        return (num & (num - 1) == 0) and (num - 1) % 3 == 0

def test():
    solution = Solution()

    assert solution.isPowerOfFour(16)
    assert not solution.isPowerOfFour(6)
    assert not solution.isPowerOfFour(5)
    assert solution.isPowerOfFour(4)

    print("self test passed")

if __name__ == '__main__':
    test()
