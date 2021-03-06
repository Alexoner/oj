# -*- encoding:utf-8 -*-


class Bit:

    def solve(self):
        n = int(raw_input())
        line = raw_input()
        arr = list(int(i) for i in line)
        carry = 1  # add 1
        changedNum = 0
        res = 0
        for i in xrange(n):
            res = arr[i] + carry
            carry = res / 2
            quotient = res % 2
            if quotient != arr[i]:
                changedNum += 1
                arr[i] = quotient

        return changedNum

if __name__ == "__main__":
    print Bit().solve()
