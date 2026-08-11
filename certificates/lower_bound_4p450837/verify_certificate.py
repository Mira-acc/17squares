#!/usr/bin/env python3
"""Separate exact-integer checker for the strict lower-bound certificate at 4.450837."""
from __future__ import annotations

import pathlib
import sys
from dataclasses import dataclass

Q = 1 << 40
XS = 1_000_000 * Q
LS = 4_450_837 * Q
LO = 500_000 * Q
HI = 3_950_837 * Q
DEN = 1_000_000

POINTS = (
    ( 967095,  988674), (1584591,  989280),
    (2477806,  929750), (3452882,  920541),
    ( 998081, 1794317), (1992852, 1799448),
    (2973306, 1794450), (3522479, 1795033),
    ( 925919, 2658468), (1494140, 2660211),
    (2483891, 2663100), (3452714, 2667020),
    ( 998038, 3524908), (1963307, 3513845),
    (2850741, 3459296), (3456188, 3456188),
)

@dataclass(frozen=True, slots=True)
class Box:
    xl: int
    xh: int
    yl: int
    yh: int
    tl: int
    th: int
    depth: int


def min_abs_t(b: Box) -> int:
    if b.tl <= 0 <= b.th:
        return 0
    return min(abs(b.tl), abs(b.th))


def less_than_half_extent(a_num: int, u_num: int) -> bool:
    if a_num < 0:
        return True
    return 4 * a_num * a_num * (Q * Q + u_num * u_num) < \
           XS * XS * (Q + u_num) * (Q + u_num)


def infeasible(b: Box) -> bool:
    u = min_abs_t(b)
    return (
        less_than_half_extent(b.xh, u)
        or less_than_half_extent(LS - b.xl, u)
        or less_than_half_extent(b.yh, u)
        or less_than_half_extent(LS - b.yl, u)
    )


def covers(b: Box, p: tuple[int, int]) -> bool:
    px, py = p
    dxl = px * XS - b.xh * DEN
    dxh = px * XS - b.xl * DEN
    dyl = py * XS - b.yh * DEN
    dyh = py * XS - b.yl * DEN

    tdy = (b.tl * dyl, b.tl * dyh, b.th * dyl, b.th * dyh)
    a0 = dxl * Q + min(tdy)
    a1 = dxh * Q + max(tdy)
    ma = max(abs(a0), abs(a1))

    ntl, nth = -b.th, -b.tl
    ndx = (ntl * dxl, ntl * dxh, nth * dxl, nth * dxh)
    b0 = min(ndx) + dyl * Q
    b1 = max(ndx) + dyh * Q
    mb = max(abs(b0), abs(b1))

    u = min_abs_t(b)
    rhs = (Q * Q + u * u) * DEN * DEN * XS * XS
    return 4 * ma * ma < rhs and 4 * mb * mb < rhs


def split(b: Box, dim: int) -> tuple[Box, Box]:
    d = b.depth + 1
    if dim == 0:
        m = (b.xl + b.xh) // 2
        if m in (b.xl, b.xh):
            raise ValueError("x grid exhausted")
        return (
            Box(b.xl, m, b.yl, b.yh, b.tl, b.th, d),
            Box(m, b.xh, b.yl, b.yh, b.tl, b.th, d),
        )
    if dim == 1:
        m = (b.yl + b.yh) // 2
        if m in (b.yl, b.yh):
            raise ValueError("y grid exhausted")
        return (
            Box(b.xl, b.xh, b.yl, m, b.tl, b.th, d),
            Box(b.xl, b.xh, m, b.yh, b.tl, b.th, d),
        )
    if dim == 2:
        m = (b.tl + b.th) // 2
        if m in (b.tl, b.th):
            raise ValueError("t grid exhausted")
        return (
            Box(b.xl, b.xh, b.yl, b.yh, b.tl, m, d),
            Box(b.xl, b.xh, b.yl, b.yh, m, b.th, d),
        )
    raise ValueError(f"bad split dimension {dim}")


def verify(path: pathlib.Path) -> None:
    cert = path.read_bytes()
    cursor = 0
    stack = [Box(LO, HI, LO, HI, -Q, Q, 0)]
    nodes = covered = impossible = branches = 0
    max_depth = 0

    while stack:
        b = stack.pop()
        if cursor >= len(cert):
            raise ValueError(f"certificate ends early at node {nodes + 1}")
        op = cert[cursor]
        cursor += 1
        nodes += 1
        max_depth = max(max_depth, b.depth)

        if op == 0:
            if not infeasible(b):
                raise ValueError(f"false infeasibility claim at node {nodes}")
            impossible += 1
        elif 1 <= op <= 16:
            if not covers(b, POINTS[op - 1]):
                raise ValueError(f"false witness {op} at node {nodes}")
            covered += 1
        elif 17 <= op <= 19:
            a, c = split(b, op - 17)
            stack.append(c)
            stack.append(a)
            branches += 1
        else:
            raise ValueError(f"unknown opcode {op} at node {nodes}")

    if cursor != len(cert):
        raise ValueError(f"{len(cert) - cursor} trailing certificate bytes")
    if covered + impossible != branches + 1:
        raise ValueError("certificate is not a full binary partition tree")

    print("PYTHON_INTEGER_CERTIFICATE_VALID")
    print("L=4450837/1000000")
    print(f"nodes={nodes}")
    print(f"split={branches}")
    print(f"covered={covered}")
    print(f"infeasible={impossible}")
    print(f"max_depth={max_depth}")


if __name__ == "__main__":
    cert_path = pathlib.Path(
        sys.argv[1] if len(sys.argv) > 1 else "square17_lb_4p450837.cert"
    )
    verify(cert_path)
