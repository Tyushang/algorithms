#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# __author__="Frank Jing"


"""
LCS 的最优子结构： 令 X = <x1, x2, ..., xm>, Y = <y1, y2, ...,yn> 为两个序列, Z = <z1, z2, ..., zk> 为 X,Y 的任意 LCS. 有:
1. 如果 xm = yn , 则 zk = xm = yn 且 Z[:-1] 是 X[:-1] & Y[:-1] 的一个 LCS.
2. 如果 xm != yn, 则 zk != xm 意味着 Z 是 X[:-1] & Y 的一个 LCS.
3. 如果 xm != yn, 则 zk != yn 意味着 Z 是 X & Y[:-1] 的一个 LCS.

对于 xm != yn 的情况, 在实际操作中我们通过判断 len_x = len_of_lcs(X[:-1], Y) & len_y = len_of_lcs(X, Y[:-1]) 的大小, 从而可以确定:
a. 若 len_x == len_y, 说明随便去掉哪一个尾部元素不影响结果, 即当前 LCS 等于去掉 X[-1] 或 Y[-1] 的 LCS (对于一个确定的 LCS , 不考虑多个 LCS 的情况);
b. 若 len_x <  len_y, 说明去掉 X[-1] 之后影响了结果, 而去掉 Y[-1] 并不影响结果, 所以当前 LCS 等于去掉 Y[-1] 之后的 LCS;
c. 若 len_x >  len_y, 说明去掉 Y[-1] 之后影响了结果, 而去掉 X[-1] 并不影响结果, 所以当前 LCS 等于去掉 X[-1] 之后的 LCS;
如此, 我们就能通过 len_x, len_y 的状态来分别对原问题缩减规模, 直到缩减至平凡问题.

注意: LCS 可能不止一个, 而这里我们只求取其中的一个. bottom-up 方法是否可以全部求取出来?
"""

X = ['B', 'A', 'B', 'C', 'B', 'D', 'A', 'B', 'C', 'B', 'D', 'B', 'C', 'A', ]
Y = ['B', 'D', 'C', 'A', 'B', 'A', 'A', 'B', 'C', 'A', 'B', 'A', ]

# results[(m, n)] = [(0,0), (1,3), (5,8)] 表示: Xm & Yn 的 LCS 是 [x0, x1, x5] 或 [y1, y3, y8]
# 这里对每一个 key , 直接存储了 LCS 分别在 X & Y 中的索引, 这样便于理解一些!
# 可以将 results 优化为指向其他 key 的指针, 这就变成了<算法导论>中的结果保存方式.
results = {}


def top_down_lcs(x_seq, y_seq):

    def trivial_problem(v, seq, is_value_of_x=True):
        if v in seq:
            return [(0, seq.index(v)), ] if is_value_of_x else [(seq.index(v), 0), ]
        else:
            return []

    def recursive(xs: list, ys: list):
        xlen_ylen = (len(xs), len(ys))
        if len(xs) == 1:
            results[xlen_ylen] = trivial_problem(xs[0], ys, True)
        if len(ys) == 1:
            results[xlen_ylen] = trivial_problem(ys[0], xs, False)

        if xlen_ylen in results.keys():
            return results[xlen_ylen]

        # 1. 如果 xm = yn , 则 zk = xm = yn 且 Z[:-1] 是 X[:-1] & Y[:-1] 的一个 LCS.
        if xs[-1] == ys[-1]:
            results[xlen_ylen] = [*recursive(xs[: -1], ys[: -1]), (len(xs) - 1, len(ys) - 1)]
            return results[xlen_ylen]
        else:
            sub_x_result = recursive(xs[: -1], ys)
            sub_y_result = recursive(xs, ys[: -1])

            # a. 若 len_x == len_y, 说明随便去掉哪一个尾部元素不影响结果,
            # 即当前 LCS 等于去掉 X[-1] 或 Y[-1] 的 LCS (对于一个确定的 LCS , 不考虑多个 LCS 的情况);
            if len(sub_x_result) == len(sub_y_result):
                results[xlen_ylen] = sub_x_result
            # b. 若 len_x <  len_y, 说明去掉 X[-1] 之后影响了结果, 而去掉 Y[-1] 并不影响结果,
            # 所以当前 LCS 等于去掉 Y[-1] 之后的 LCS;
            elif len(sub_x_result) < len(sub_y_result):
                results[xlen_ylen] = sub_y_result
            # c. 若 len_x >  len_y, 说明去掉 Y[-1] 之后影响了结果, 而去掉 Y[-1] 并不影响结果,
            # 所以当前 LCS 等于去掉 X[-1] 之后的 LCS;
            else:
                results[xlen_ylen] = sub_x_result

            return results[xlen_ylen]

    return recursive(x_seq, y_seq)


ans = top_down_lcs(X, Y)
print(X)
print(list(map(lambda ixiy: X[ixiy[0]], ans)))
print(list(map(lambda ixiy: Y[ixiy[1]], ans)))
print(Y)



