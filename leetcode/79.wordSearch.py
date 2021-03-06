'''
79. Word Search

Total Accepted: 91301
Total Submissions: 373731
Difficulty: Medium
Given a 2D board and a word, find if the word exists in the grid.

The word can be constructed from letters of sequentially adjacent cell, where
"adjacent" cells are those horizontally or vertically neighboring. The same
letter cell may not be used more than once.

For example,
Given board =

[
  ['A','B','C','E'],
  ['S','F','C','S'],
  ['A','D','E','E']
]
word = "ABCCED", -> returns true,
word = "SEE", -> returns true,
word = "ABCB", -> returns false.

==============================================================================================
SOLUTION

1. Treat this problem as a graph search problem, then DEPTH-FIRST or
BREADTH-FIRST search can be utilized.

2. Trie (prefix tree)
Preprocess the table to build a TRIE tree data structure for text retrieval.

3. Combine the DFS and TRIE procedure: along with depth-first search routine,
we build the partial trie tree simultaneously.

----------------------------------------------------------------------------------------------
Optimization

    To save memory, we can use encode with bit representation: `cell ^= 255` to
mark visited cells.

'''

# the lambda expression to get an array's depth recursively

depth = lambda L: isinstance(L, list) and (max(map(depth, L)) + 1) if L else 1

class np:

    depth = depth

    @classmethod
    def shape(cls, a):
        '''
        get a multiple-dimensional list's shape
        Empty lists
        '''
        a_child = a
        while isinstance(a_child, list):
            yield len(a_child)
            if a_child:
                a_child = a_child[0]
            else:
                break

    @classmethod
    def at(cls, a, index):
        '''
        a: multiple dimensional array(list)
        index: iterable, shape
        '''
        try:
            element = a
            for index in index:
                if not element:
                    break
                element = element[index]
        except IndexError as e:
            raise e

        return element

    @classmethod
    def indices(cls, shape):
        # generate all possible indices given an array's shape
        if not shape or 0 in shape:
            # cannot use `return` with a value to exit generator
            yield []
            return
        dimension = len(shape)
        point = [0] * dimension
        def add(point, addend=1):
            point[-1] += addend
            i = dimension - 1
            while i >= 0 and point[i] >= shape[i]:
                # carry operation
                point[i] = 0
                point[i - 1] += 1
                i -= 1

            return i >= 0

        while True:
            yield tuple(point)
            if not add(point):
                break

class Solution(object):

    def __init__(self, cycle=False, verbose=False):
        self.size    = [] # the board(matrix) size
        self.visit   = set() # visit table maintains the visited cells, (c1, c2) -> bool
        self.cycle   = cycle
        self.verbose = verbose
        # TODO: to tackle multipe-dimension arrays, library numpy would be much better than
        # doing it from scratch

    def exist(self, board, word):
        """
        :type board: List[List[str]]
        :type word: str
        :rtype: bool
        """
        # if not board:
            # return False
        # self.size = list(np.shape(board))
        # self.visit = set() # visit table maintains the visited cells, (c1, c2) -> bool
        # result = self._existDfsUgly(board, word)

        result = self._existDfs(board, word)

        return result

    def neighbors(self, coordinate, size, cycle=True):
        """
        :type coordinate: two-tuple (c1, c2)
        :type size: two-tuple (M, N), the matrix(board) size
        :cycle: take modulo arithmetic to get remainder, to cycle
        :rtype: iterator of (c1, c2)

        """
        D = len(size)
        vectors = []
        for d in range(D):
            vector = [0] * D
            vector[d] = 1 # step is increasing or decreasing by 1 on a single dimension
            vectors.append(vector)

            vector = [0] * D
            vector[d] = -1
            vectors.append(vector)

        # vectors = [
            # (0, 1),
            # (0, -1),
            # (1, 0),
            # (-1, 0),
        # ]
        for vector in vectors:
            if cycle:
                coordinate_next = tuple(map(
                    lambda x1, x2, d: (x1 + x2) % d,
                    vector, coordinate, size))
            else:
                coordinate_next = tuple(map(
                    lambda x1, x2, d: (x1 + x2) if (0 <= x1 + x2 < d) else -1,
                    vector, coordinate, size
                ))
            if -1 not in coordinate_next:
                yield coordinate_next
        pass

    @classmethod
    def _cellLetter(cls, board, coordinate):
        return np.at(board, coordinate)

    def neighbors2(self, coordinate, size, cycle=False):
        """
        :type coordinate: two-tuple (c1, c2)
        :type size: two-tuple (M, N), the matrix(board) size
        :cycle: take modulo arithmetic to get remainder, to cycle
        :rtype: iterator of (c1, c2)

        There is a trade-off between code abstractness and speed.
        This implementation may be faster, but it doesn't generalize to N-dimension.
        """
        if coordinate[0] - 1 >= 0:
            yield (coordinate[0] - 1, coordinate[1])
        if coordinate[0] + 1 < size[0]:
            yield (coordinate[0] + 1, coordinate[1])
        if coordinate[1] - 1 >= 0:
            yield (coordinate[0], coordinate[1] - 1)
        if coordinate[1] + 1 < size[1]:
            yield (coordinate[0], coordinate[1] + 1)

    @classmethod
    def _cellLetter2(cls, board, coordinate):
        return board[coordinate[0]][coordinate[1]]

    def _existDfsUgly(self, board, word, coordinate=None):
      def dfs(board, word, coordinate=None):
          # TODO: (DONE) multiple dimensional: 1-d, 2-d, ...
          # start depth-first search
          if not coordinate:
              for index in np.indices(self.size):
                  if dfs(board, word, index): return True
              return  False

          result = False
          cellLetter = self._cellLetter(board, coordinate)

          if not word or word == cellLetter:
              return True

          # check traversal condition
          if word.startswith(cellLetter):
              self.visit.add(coordinate)
              if self.verbose: print('visited', cellLetter, word, coordinate)
              # the RECURSIVE routine
              for neighbor in self.neighbors(coordinate, self.size, cycle=self.cycle):
                  if neighbor not in self.visit:
                      result = dfs(board, word[len(cellLetter):], neighbor)
                      if result:
                          break
              # BACKTRACKING: revert state
              self.visit.remove(coordinate)

          return result
      result = dfs(board, word, coordinate)

    # DONE: for god's sake, simplify the implementation...
    def _existDfs(self, board, word):
        if not word: return True
        if not board or not board[0]: return False

        m, n = len(board), len(board[0])
        visited = [[False for _ in range(n)] for _ in range(m)]
        def dfs(i, j, w):
            # print(i, j, w)
            if not w: return True
            if w[0] != board[i][j]: return False
            if len(w) == 1: return True

            visited[i][j] = True
            # c = board[i][j]
            # board[i][j] = '#'
            for x, y in ((i - 1, j), (i + 1, j), (i, j - 1), (i, j + 1)):
                if not (0 <= x < m and 0 <= y < n): continue
                if visited[x][y]: continue
                # if board[x][y] == '#': continue
                if dfs(x, y, w[1:]):
                    # board[i][j] = c
                    visited[i][j] = False
                    return True
            visited[i][j] = False
            # board[i][j] = c
            return False

        for i in range(m):
            for j in range(n):
                if dfs(i, j, word): return True

        return False

    def existTrie(self, board, word):
        pass

def test():
    assert np.at([[1], [2]], [1, 0]) == 2
    # print(list(np.indices([2, 5])))
    # print(list(np.indices([1])))

    solution = Solution('cycle', 'verbose')

    assert solution.exist([], "")
    assert solution.exist([[]], "")
    assert solution.exist([["a"]], "a")

    board = [
        ['A', 'B', 'C', 'E'],
        ['S', 'F', 'C', 'S'],
        ['A', 'D', 'E', 'E'],
    ]
    assert solution.exist(board, "")
    assert solution.exist(board, 'ABCCED'), 'ABCCED should be in the board'
    assert solution.exist(board, 'SEE'), 'SEE should be in the board'
    # assert solution.exist(board, 'SSFB'), 'SSFB should be in the board'
    assert not solution.exist(board, 'ABCB'), 'ABCB should not be in the board'
    # assert solution.exist(['a'], 'a'), 'a should be in the board'
    assert solution.exist([['a']], 'a'), 'a should be in the board'
    assert not solution.exist([], 'a'), 'a should not be in the board'
    # assert not solution.exist(
        # ["aaa", "abb", "abb", "bbb", "bbb", "aaa", "bbb", "abb", "aab", "aba"],
        # "aabaaaabbb"), 'aabaaaabbb should not be in the board';
    # assert solution.exist(
        # ["aaa", "abb", "abb", "bbb", "bbb", "aaa", "bbb", "abb", "aab", "aba"],
        # "abbaaaabaaab"), 'aabaaaabbb should be in the board'

    solution = Solution(cycle=False, verbose=True)
    assert solution.exist([['A', 'B', 'C', 'E'],
                           ["S", "F", "C", "S"],
                           ["A", "D", "E", "E"]],
                          "ABCCED")
    assert not solution.exist([
        [u'a', u'a', u'a'],
        [u'a', u'b', u'b'],
        [u'a', u'b', u'b'],
        [u'b', u'b', u'b'],
        [u'b', u'b', u'b'],
        [u'a', u'a', u'a'],
        [u'b', u'b', u'b'],
        [u'a', u'b', u'b'],
        [u'a', u'a', u'b'],
        [u'a', u'b', u'a']],
        'aabaaaabbb')
    print('\nAll tests have passed')

if __name__ == '__main__':
    test()
