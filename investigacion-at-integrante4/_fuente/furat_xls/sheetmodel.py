# -*- coding: utf-8 -*-
"""Modelo de celdas de una hoja BIFF8."""
import struct
from biff import records, substreams, parse_sst, col_name


def load(c):
    wb = c.read('/Workbook')
    recs = records(wb)
    subs = substreams(recs)
    g = subs[0]
    i = [k for k, r in enumerate(g) if r[1] == 0x00FC][0]
    conts, k = [], i + 1
    while g[k][1] == 0x003C:
        conts.append(g[k][2])
        k += 1
    total, uniq, strs = parse_sst(g[i][2], conts)
    return wb, recs, subs, strs


def cells(sheet_recs, strs):
    out = {}
    merges = []
    rows = {}
    for pos, t, d in sheet_recs:
        if t == 0x00FD:
            r, cc, xf, isst = struct.unpack_from('<HHHI', d)
            out[(r, cc)] = ('S', xf, strs[isst])
        elif t == 0x0201:
            r, cc, xf = struct.unpack_from('<HHH', d)
            out[(r, cc)] = ('B', xf, None)
        elif t == 0x00BE:
            r, c1 = struct.unpack_from('<HH', d)
            n = (len(d) - 6) // 2
            for j in range(n):
                xf = struct.unpack_from('<H', d, 4 + 2 * j)[0]
                out[(r, c1 + j)] = ('B', xf, None)
        elif t in (0x0203, 0x027E, 0x00BD, 0x0204, 0x0006, 0x0205):
            r, cc = struct.unpack_from('<HH', d)
            out[(r, cc)] = ('O%x' % t, None, None)
        elif t == 0x00E5:
            n = struct.unpack_from('<H', d)[0]
            for j in range(n):
                merges.append(struct.unpack_from('<HHHH', d, 2 + 8 * j))
        elif t == 0x0208:
            r, c1, c2, h = struct.unpack_from('<HHHH', d)
            rows[r] = h
    return out, merges, rows


def merge_of(merges, r, c):
    for (r1, r2, c1, c2) in merges:
        if r1 <= r <= r2 and c1 <= c <= c2:
            return (r1, r2, c1, c2)
    return None


def ref(r, c):
    return '%s%d' % (col_name(c), r + 1)


def rng(m):
    r1, r2, c1, c2 = m
    return ref(r1, c1) + (':' + ref(r2, c2) if (r1, c1) != (r2, c2) else '')
