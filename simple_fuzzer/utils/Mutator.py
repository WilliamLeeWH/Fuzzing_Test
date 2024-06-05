import math
import random
import struct
from typing import Any


def insert_random_character(s: str) -> str:
    """
    向 s 中下标为 pos 的位置插入一个随机 byte
    pos 为随机生成，范围为 [0, len(s)]
    插入的 byte 为随机生成，范围为 [32, 127]
    """
    # TODO
    i = random.randint(0, len(s))
    s = s[0:i]+chr(random.randint(32, 127))+s[i:len(s)]

    return s


def flip_random_bits(s: str) -> str:
    """
    基于 AFL 变异算法策略中的 bitflip 与 random havoc 实现相邻 N 位翻转（N = 1, 2, 4），其中 N 为随机生成
    从 s 中随机挑选一个 bit，将其与其后面 N - 1 位翻转（翻转即 0 -> 1; 1 -> 0）
    注意：不要越界
    """
    # TODO
    N = 1 << random.randint(0, 2)
    ii = random.randint(0, 7)
    i = random.randint(0, len(s)-1 if ii + N <= 7 else len(s) - 2)
    if ii + N > 8:
        # s[i] = chr(ord(s[i]) ^ (1 << (7-ii)))
        s = s[:i] + chr(ord(s[i]) ^ (1 << (7-ii))) + s[i+1:]
        i += 1
        N = ii + N - 8
        ii = 0
    # s[i] = chr(ord(s[i]) ^ ((1 << (7-ii)) - 1 << (7-ii-N)))
    s = s[:i] + chr(ord(s[i]) ^ ((1 << (7-ii)) - 1 << (7-ii-N))) + s[i+1:]

    return s


def arithmetic_random_bytes(s: str) -> str:
    """
    基于 AFL 变异算法策略中的 arithmetic inc/dec 与 random havoc 实现相邻 N 字节随机增减（N = 1, 2, 4），其中 N 为随机生成
    字节随机增减：
        1. 取其中一个 byte，将其转换为数字 num1；
        2. 将 num1 加上一个 [-35, 35] 的随机数，得到 num2；
        3. 用 num2 所表示的 byte 替换该 byte
    从 s 中随机挑选一个 byte，将其与其后面 N - 1 个 bytes 进行字节随机增减
    注意：不要越界；如果出现单个字节在添加随机数之后，可以通过取模操作使该字节落在 [0, 255] 之间
    """
    # TODO
    N = 1 << random.randint(0, 2)
    i = random.randint(0, len(s)-N)
    while N > 0:
        # s[i] = chr((ord(s[i]) + random.randint(-35, 35)) % 256)
        s = s[:i] + chr((ord(s[i]) + random.randint(-35, 35)) % 256) + s[i+1:]
        i += 1
        N -= 1

    return s


def interesting_random_bytes(s: str) -> str:
    """
    基于 AFL 变异算法策略中的 interesting values 与 random havoc 实现相邻 N 字节随机替换为 interesting_value（N = 1, 2, 4），其中 N 为随机生成
    interesting_value 替换：
        1. 构建分别针对于 1, 2, 4 bytes 的 interesting_value 数组；
        2. 随机挑选 s 中相邻连续的 1, 2, 4 bytes，将其替换为相应 interesting_value 数组中的随机元素；
    注意：不要越界
    """
    # TODO
    interesting_values = {
        1: '.',
        2: '<>',
        4: '-<>.'
    }
    N = 1 << random.randint(0, 2)
    i = random.randint(0, len(s)-N)
    s = s[:i] + interesting_values[N] + s[i+1:]

    return s


def havoc_random_insert(s: str) -> str:
    """
    基于 AFL 变异算法策略中的 random havoc 实现随机插入
    随机选取一个位置，插入一段的内容，其中 75% 的概率是插入原文中的任意一段随机长度的内容，25% 的概率是插入一段随机长度的 bytes
    """
    # TODO
    i = random.randint(0, len(s))
    a = random.randint(0, len(s)-1)
    b = random.randint(a, len(s))

    p = random.randint(0, 3)
    if p:
        for x in range(a, b):
            s = s[0:i]+chr(random.randint(0, 255))+s[i:len(s)]
    else:
        s = s[0:i]+s[a:b]+s[i:len(s)]

    return s


def havoc_random_replace(s: str) -> str:
    """
    基于 AFL 变异算法策略中的 random havoc 实现随机替换
    随机选取一个位置，替换随后一段随机长度的内容，其中 75% 的概率是替换为原文中的任意一段随机长度的内容，25% 的概率是替换为一段随机长度的 bytes
    """
    # TODO
    i = random.randint(0, len(s))
    l = random.randint(1, len(s)-i+1)

    p = random.randint(0, 3)
    if p:
        while l > 0:
            # s[i] = chr(random.randint(0, 255))
            s = s[:i] + chr(random.randint(0, 255)) + s[i+1:]
            i += 1
            l -= 1
    else:
        _i = random.randint(0, len(s) - l)
        s = s[:i] + s[_i:_i+l] + s[i+l:]

    return s


def my_delete_random_bytes(s: str) -> str:
    """
    删除相邻的N字节(N = 1, 2, 4)
    """

    N = 1 << random.randint(0, 2)
    if len(s) < N:
        return s
    i = random.randint(0, len(s) - N)
    s = s[0:i]+s[i+N:len(s)]

    return s


def my_havoc_random_delete(s: str) -> str:
    a = random.randint(0, len(s)-1)
    b = random.randint(a, len(s))

    s = s[0:a] + s[b:len(s)]
    return s


def my_splice_and_reverse(s: str) -> str:
    i = random.randint(0, len(s))

    s = s[i:len(s)] + s[0:i]
    return s


def my_splice_and_shuffle(s: str) -> str:
    i = random.randint(1, 5)
    ii = []
    for i in range(0, i):
        ii.append(random.randint(0, len(s)))
    ii.sort()
    ii.append(0)
    ii.append(len(s))

    sub = []
    for _i in range(0, i+1):
        sub.append(s[ii[_i]:ii[_i+1]])

    _s = ""
    while len(sub):
        _s += sub.pop(random.randint(0, len(sub)-1))

    return _s


def my_havoc_replace_all(s: str) -> str:
    a = random.randint(0, len(s)-1)
    b = random.randint(0, len(s)-1)

    s = s.replace(s[a], s[b])
    return s


class Mutator:

    def __init__(self) -> None:
        """Constructor"""
        self.mutators = [
            insert_random_character,
            flip_random_bits,
            arithmetic_random_bytes,
            interesting_random_bytes,
            havoc_random_insert,
            havoc_random_replace,

            my_delete_random_bytes,
            my_havoc_random_delete,
            my_splice_and_reverse,
            my_splice_and_shuffle,
            my_havoc_replace_all,
        ]

    def mutate(self, inp: Any) -> Any:
        mutator = random.choice(self.mutators)
        try:
            return mutator(inp)
        except:
            return inp
