"""
Given a n,m which means the row and column of the 2D matrix and an array of pair A( size k). Originally, the 2D matrix
is all 0 which means there is only sea in the matrix. The list pair has k operator and each operator has two integer
A[i].x, A[i].y means that you can change the grid matrix[A[i].x][A[i].y] from sea to island. Return how many island are
there in the matrix after each operator.

Example
Given n = 3, m = 3, array of pair A = [(0,0),(0,1),(2,2),(2,1)].

return [1,1,2,2].

Note
0 is represented as the sea, 1 is represented as the island. If two 1 is adjacent, we consider them in the same island.
We only consider up/down/left/right adjacent.
"""
__author__ = 'Daniel'


class Point:
    def __init__(self, a=0, b=0):
        self.x = a
        self.y = b


class UnionFind(object):
    """
    Weighted Union Find with path compression
    """

    def __init__(self, rows, cols):
        # hashing will cause TLE; use direct array access instead
        self.pi = [-1 for _ in xrange(rows*cols)]  # item -> pi
        self.sz = [-1 for _ in xrange(rows*cols)]  # root -> size
        self.count = 0

    def add(self, item):
        if self.pi[item] == -1:
            self.pi[item] = item
            self.sz[item] = 1
            self.count += 1

    def union(self, a, b):
        pi1 = self._pi(a)
        pi2 = self._pi(b)

        if pi1 != pi2:
            if self.sz[pi1] > self.sz[pi2]:
                pi1, pi2 = pi2, pi1

            self.pi[pi1] = pi2
            self.sz[pi2] += self.sz[pi1]
            self.count -= 1

    def _pi(self, item):
        pi = self.pi[item]
        if item != pi:
            self.pi[item] = self._pi(pi)

        return self.pi[item]


class Solution:
    def __init__(self):
        self.dirs = ((-1, 0), (1, 0), (0, -1), (0, 1))

    def numIslands2(self, n, m, operators):
        """

        :type n: int
        :type m: int
        :type operators: list[Point]
        :rtype: list[int]
        """
        rows = n
        cols = m
        id = lambda x, y: x*cols+y  # hash will be slower
        mat = [[0 for _ in xrange(cols)] for _ in xrange(rows)]
        uf = UnionFind(rows, cols)
        ret = []
        for op in operators:
            uf.add(id(op.x, op.y))
            mat[op.x][op.y] = 1
            for dir in self.dirs:
                x1 = op.x+dir[0]
                y1 = op.y+dir[1]
                if 0 <= x1 < rows and 0 <= y1 < cols and mat[x1][y1] == 1:
                    uf.union(id(op.x, op.y), id(x1, y1))

            ret.append(uf.count)

        return ret


if __name__ == "__main__":
    assert Solution().numIslands2(3, 3, map(lambda x: Point(x[0], x[1]), [(0, 0), (0, 1), (2, 2), (2, 1)])) == [1, 1, 2,
                                                                                                                2]
