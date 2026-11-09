# -*- coding: utf-8 -*-
"""Recalcula INDEX, DBCELL, EXTSST y BOUNDSHEET de un flujo Workbook BIFF8."""
import struct
from biff import Reader

CELL_TYPES = {0x0006, 0x00FD, 0x0201, 0x00BE, 0x0203, 0x027E, 0x00BD, 0x0204, 0x0205, 0x0221, 0x04BC, 0x0236,
              0x0207}


def serialize(recs):
    """recs: lista de (tipo, datos). Devuelve (bytes, posiciones)."""
    out = bytearray()
    pos = []
    for t, d in recs:
        pos.append(len(out))
        out += struct.pack('<HH', t, len(d)) + d
    return out, pos


def fix_sheet(recs, pos, base):
    """Recalcula DBCELL e INDEX de una hoja. recs/pos relativos a la hoja; base = posición absoluta del BOF."""
    recs = list(recs)
    # bloques: ROW... celdas... DBCELL
    block_rows, first_cell = [], {}
    dbcells = []
    for i, (t, d) in enumerate(recs):
        if t == 0x0208:
            block_rows.append(i)
        elif t in CELL_TYPES and t not in (0x0207, 0x0221, 0x04BC, 0x0236):
            r = struct.unpack_from('<H', d)[0]
            first_cell.setdefault(r, i)
        elif t == 0x00D7:
            rows = block_rows
            dbRtrw = pos[i] - pos[rows[0]]
            offs = []
            prev = pos[rows[1]] if len(rows) > 1 else pos[rows[0]] + 4 + len(recs[rows[0]][1])
            # primera: desde el inicio del 2.º ROW (fin del 1.er ROW si es único) hasta la 1.ª celda de la 1.ª fila
            ref = pos[rows[0]] + 4 + len(recs[rows[0]][1])  # fin del primer ROW
            cur_ref = None
            rownums = [struct.unpack_from('<H', recs[ri][1])[0] for ri in rows]
            cellpos = []
            for k, r in enumerate(rownums):
                fc = first_cell.get(r)
                if fc is None:   # fila sin celdas: se usa la primera celda de las filas siguientes
                    nxt = [first_cell[x] for x in rownums[k + 1:] if x in first_cell]
                    cellpos.append(pos[nxt[0]] if nxt else pos[i])
                else:
                    cellpos.append(pos[fc])
            start = pos[rows[1]] if len(rows) > 1 else pos[rows[0]] + 4 + len(recs[rows[0]][1])
            offs = [cellpos[0] - start] + [cellpos[k] - cellpos[k - 1] for k in range(1, len(cellpos))]
            d = struct.pack('<I', dbRtrw) + b''.join(struct.pack('<H', o) for o in offs)
            recs[i] = (t, d)
            dbcells.append(i)
            block_rows, first_cell = [], {}
    # INDEX
    for i, (t, d) in enumerate(recs):
        if t == 0x020B:
            res, rwMic, rwMac, ibXF = struct.unpack_from('<IIII', d)
            dcw = [k for k, (tt, dd) in enumerate(recs) if tt == 0x0055]
            ibXF = base + pos[dcw[0]] if dcw else ibXF
            n = (len(d) - 16) // 4
            assert n == len(dbcells), (n, len(dbcells))
            nd = struct.pack('<IIII', res, rwMic, rwMac, ibXF) + b''.join(struct.pack('<I', base + pos[k]) for k in dbcells)
            recs[i] = (t, nd)
    return recs


def sst_string_starts(chunks):
    """Para cada cadena: (índice de fragmento, desplazamiento dentro del fragmento)."""
    r = Reader(chunks)
    r.u32(); n = r.u32()
    starts = []
    for _ in range(n):
        ci, p = r.ci, r.pos
        if p == len(chunks[ci]):
            ci, p = ci + 1, 0
        starts.append((ci, p))
        r.xlstring()
    return starts


def build_extsst(starts, chunk_abs, dsst=8):
    """chunk_abs[i] = posición absoluta del encabezado del registro del fragmento i."""
    out = struct.pack('<H', dsst)
    for k in range(0, len(starts), dsst):
        ci, p = starts[k]
        ib = chunk_abs[ci] + 4 + p
        out += struct.pack('<IHH', ib, 4 + p, 0)
    return out
