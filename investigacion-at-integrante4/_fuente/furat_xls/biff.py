# -*- coding: utf-8 -*-
"""Lectura de registros BIFF8 (MS-XLS) y del SST."""
import struct

NAMES = {0x0809: "BOF", 0x000A: "EOF", 0x0085: "BOUNDSHEET", 0x00FC: "SST", 0x003C: "CONTINUE", 0x00FF: "EXTSST",
         0x020B: "INDEX", 0x0200: "DIMENSIONS", 0x0208: "ROW", 0x0201: "BLANK", 0x00BE: "MULBLANK", 0x00FD: "LABELSST",
         0x0203: "NUMBER", 0x027E: "RK", 0x00BD: "MULRK", 0x0204: "LABEL", 0x0006: "FORMULA", 0x0205: "BOOLERR",
         0x00D7: "DBCELL", 0x00E5: "MERGEDCELLS", 0x00EC: "MSODRAWING", 0x005D: "OBJ", 0x01B6: "TXO", 0x023E: "WINDOW2",
         0x007D: "COLINFO", 0x0055: "DEFCOLWIDTH", 0x00E0: "XF", 0x0031: "FONT", 0x041E: "FORMAT", 0x0018: "LBL",
         0x01AE: "SUPBOOK", 0x0017: "EXTERNSHEET", 0x00EB: "MSODRAWINGGROUP", 0x0207: "STRING", 0x0225: "DEFAULTROWHEIGHT",
         0x001B: "HORIZONTALPAGEBREAKS", 0x0014: "HEADER", 0x0015: "FOOTER", 0x00A1: "SETUP", 0x002F: "FILEPASS",
         0x0868: "FEAT", 0x0867: "FEATHDR", 0x01B8: "HLINK", 0x00EF: "PHONETIC", 0x01BA: "CODENAME", 0x00D3: "OBPROJ",
         0x0099: "STANDARDWIDTH", 0x0012: "PROTECT", 0x0013: "PASSWORD", 0x0019: "WINDOWPROTECT", 0x00DD: "SCENPROTECT",
         0x0063: "OBJPROTECT", 0x01B0: "CONDFMT", 0x01B1: "CF", 0x01B2: "DVAL", 0x01BE: "DV", 0x0236: "TABLE",
         0x0221: "ARRAY", 0x04BC: "SHRFMLA", 0x001D: "SELECTION", 0x00A0: "SCL", 0x0041: "PANE", 0x0293: "STYLE"}


def records(stream, start=0, end=None):
    """Lista de (posición, tipo, datos)."""
    out = []
    pos = start
    end = len(stream) if end is None else end
    while pos + 4 <= end:
        t, n = struct.unpack_from("<HH", stream, pos)
        out.append((pos, t, bytes(stream[pos + 4:pos + 4 + n])))
        pos += 4 + n
        if t == 0x000A and end is not None and start != 0:
            pass
    return out


def substreams(recs):
    """Separa globales y hojas por BOF/EOF."""
    subs, cur = [], None
    for r in recs:
        if r[1] == 0x0809:
            cur = [r]
        elif cur is not None:
            cur.append(r)
            if r[1] == 0x000A:
                subs.append(cur)
                cur = None
    return subs


class Reader:
    """Lector de cadenas Unicode BIFF8 que puede cruzar registros CONTINUE."""

    def __init__(self, chunks):
        self.chunks = chunks       # lista de bytes (datos de SST + CONTINUE)
        self.ci = 0
        self.pos = 0

    def _need(self, n):
        if self.pos + n > len(self.chunks[self.ci]):
            if self.pos == len(self.chunks[self.ci]):
                self.ci += 1
                self.pos = 0
            else:
                raise ValueError("estructura cortada entre registros")

    def u8(self):
        self._need(1)
        v = self.chunks[self.ci][self.pos]
        self.pos += 1
        return v

    def u16(self):
        self._need(2)
        v = struct.unpack_from("<H", self.chunks[self.ci], self.pos)[0]
        self.pos += 2
        return v

    def u32(self):
        self._need(4)
        v = struct.unpack_from("<I", self.chunks[self.ci], self.pos)[0]
        self.pos += 4
        return v

    def skip(self, n):
        while n:
            if self.pos == len(self.chunks[self.ci]):
                self.ci += 1
                self.pos = 0
            take = min(n, len(self.chunks[self.ci]) - self.pos)
            self.pos += take
            n -= take

    def xlstring(self):
        if self.pos == len(self.chunks[self.ci]):
            self.ci += 1
            self.pos = 0
        cch = self.u16()
        flags = self.u8()
        high = flags & 1
        rich = flags & 8
        ext = flags & 4
        crun = self.u16() if rich else 0
        cbext = self.u32() if ext else 0
        chars = []
        left = cch
        while left:
            if self.pos == len(self.chunks[self.ci]):
                self.ci += 1
                self.pos = 0
                high = self.chunks[self.ci][0] & 1
                self.pos = 1
            avail = len(self.chunks[self.ci]) - self.pos
            if high:
                n = min(left, avail // 2)
                chars.append(self.chunks[self.ci][self.pos:self.pos + 2 * n].decode("utf-16-le"))
                self.pos += 2 * n
            else:
                n = min(left, avail)
                chars.append(self.chunks[self.ci][self.pos:self.pos + n].decode("latin-1"))
                self.pos += n
            left -= n
        self.skip(4 * crun + cbext)
        return "".join(chars)


def parse_sst(sst_data, continues):
    r = Reader([sst_data] + continues)
    total = r.u32()
    unique = r.u32()
    strings = [r.xlstring() for _ in range(unique)]
    return total, unique, strings


def short_xlstring(data, off):
    cch = data[off]
    flags = data[off + 1]
    if flags & 1:
        return data[off + 2:off + 2 + 2 * cch].decode("utf-16-le")
    return data[off + 2:off + 2 + cch].decode("latin-1")


def col_name(c):
    s = ""
    c += 1
    while c:
        c, r = divmod(c - 1, 26)
        s = chr(65 + r) + s
    return s
