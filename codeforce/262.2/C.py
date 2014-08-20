# -*- coding:utf-8 -*-

'''
C. Present
time limit per test2 seconds
memory limit per test256 megabytes
inputstandard input
outputstandard output
Little beaver is a beginner programmer, so informatics is his favorite subject. Soon his informatics teacher is going to have a birthday and the beaver has decided to prepare a present for her. He planted n flowers in a row on his windowsill and started waiting for them to grow. However, after some time the beaver noticed that the flowers stopped growing. The beaver thinks it is bad manners to present little flowers. So he decided to come up with some solutions.

There are m days left to the birthday. The height of the i-th flower (assume that the flowers in the row are numbered from 1 to n from left to right) is equal to ai at the moment. At each of the remaining m days the beaver can take a special watering and water w contiguous flowers (he can do that only once at a day). At that each watered flower grows by one height unit on that day. The beaver wants the height of the smallest flower be as large as possible in the end. What maximum height of the smallest flower can he get?

Input
The first line contains space-separated integers n, m and w (1 ≤ w ≤ n ≤ 105; 1 ≤ m ≤ 105). The second line contains space-separated integers a1, a2, ..., an (1 ≤ ai ≤ 109).

Output
Print a single integer — the maximum final height of the smallest flower.

Sample test(s)
input
6 2 3
2 2 2 2 1 1
output
2
input
2 5 1
5 8
output
9
Note
In the first sample beaver can water the last 3 flowers at the first day. On the next day he may not to water flowers at all. In the end he will get the following heights: [2, 2, 2, 3, 2, 2]. The smallest flower has height equal to 2. It's impossible to get height 3 in this test.
'''

import sys


def input():
    line = sys.stdin.readline().split()
    n = int(line[0])
    m = int(line[1])
    w = int(line[2])
    line = sys.stdin.readline().split()
    a = []
    for i in range(len(line)):
        a.append(int(line[i]))

    a.sort()
    for i in range(m):
        for j in range(w):
            a[j] += 1
        a.sort()

    return a

if __name__ == "__main__":
    print input()[0]
