#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# __author__="Frank Jing"


"""
在河上有一座独木桥，一只青蛙想沿着独木桥从河的一侧跳到另一侧。 在桥上有一些石子，青蛙很讨厌踩在这些石子上。
由于桥的长度和青蛙一次跳过的距离都是正整数，我们可以把独木桥上青蛙可能到达的点看成数轴上的一串整点：0，1，……，L（其中L是桥的长度）。
坐标为0的点表示桥的起点，坐标为L的点表示桥的终点。
青蛙从桥的起点开始，不停的向终点方向跳跃。一次跳跃的距离是S到T之间的任意正整数（包括S,T）。
当青蛙跳到或跳过坐标为L的点时，就算青蛙已经跳出了独木桥。

题目给出独木桥的长度L，青蛙跳跃的距离范围S,T，桥上石子的位置。你的任务是确定青蛙要想过河，最少需要踩到的石子数。

输入描述:
第一行有一个正整数L（1<=L<=109），表示独木桥的长度。
第二行有三个正整数S，T，M，分别表示青蛙一次跳跃的最小距离，最大距离，及桥上石子的个数，其中1<=S<=T<=10，1<=M<=100。
第三行有M个不同的正整数分别表示这M个石子在数轴上的位置（数据保证桥的起点和终点处没有石子）。
所有相邻的整数之间用一个空格隔开。
输出描述:
只包括一个整数，表示青蛙过河最少需要踩到的石子数。
示例1
输入
10
2 3 5
2 3 5 6 7
输出
2
备注:
对于30%的数据，L<=10000；
对于全部的数据，L<=10e9。
"""

L = 100
S, T = 5, 7
STONES = {3, 6, 7, 10, 30, 31, 32, 33, 34, 35, 36, 37, 39, 40}


def bottom_up_frog(ll, s, t, stones):
    losses = {0: 0}         # losses[9] = 2 表示从 0 到 9 的最小损失是 2 .
    traces = {0: 'start'}   # traces[8] = 5 表示 step 8 的最优前驱 step 是 5 .

    if 'trivial':
        for i in range(1, s):
            losses[i] = float('inf')  # inf means unreachable.
        for i in range(s, t+1):
            losses[i] = 1 if i in stones else 0
            traces[i] = 0

    # 当青蛙跳到或跳过坐标为L的点时，就算青蛙已经跳出了独木桥。
    # 所以需要考虑 [ll, ..., ll+t-1] , 从中选取最优解.
    while max(losses.keys()) < ll + t - 1:
        cur_step      = max(losses.keys()) + 1
        # 青蛙跳跃区间设定为左开右闭, 即石头在跳跃起点不计入损失, 石头在跳跃终点计入损失.
        cur_step_loss = 1 if cur_step in stones else 0

        min_loss  = float('inf')
        tmp_trace = None
        # 从 n -> n+1 , 从当前 step 的所有前驱 step 中, 选最小损失的 step 作为最优前驱节点.
        for j in range(s, t + 1):
            if losses[cur_step - j] < min_loss:  # inf < inf : False
                min_loss  = losses[cur_step - j] + cur_step_loss
                tmp_trace = cur_step - j
        losses[cur_step] = min_loss
        if tmp_trace is not None:
            traces[cur_step] = tmp_trace

    final_loss = float('inf')
    for step in range(ll, ll + t):
        if losses[step] < final_loss:
            final_loss = losses[step]
            traces['end'] = step

    return final_loss, traces


def print_trace(traces):
    lst  = []
    prev = traces['end']
    while prev in traces:
        lst.insert(0, prev)
        prev = traces[prev]
    print(lst)


ans_loss, ans_traces = bottom_up_frog(L, S, T, STONES)
print_trace(ans_traces)
