# -*- coding: utf-8 -*-
"""Diligencia el FURAT original de ARL SURA (furat.xls, BIFF8) sin rehacer el archivo.

Cambios que hace, y solo esos:
  * Hoja "FORMATO FURAT": escribe textos en las celdas en blanco de cada campo (conservando su formato)
    y reemplaza las letras guía D/M/A/H por los dígitos (con un formato existente de letra negra).
  * Marca las casillas ActiveX (Value = "1" en el flujo Ctls), dibuja una X en su imagen guardada
    y escribe una X literal en la celda inferior para que se vea también sin soporte ActiveX.
  * Agrega las cadenas nuevas al final de la tabla SST y recalcula EXTSST, DBCELL, INDEX y BOUNDSHEET.
El proyecto VBA, las demás hojas y los demás flujos quedan iguales.
"""
import re
import struct
import sys
import textwrap
import zlib

import blips
import cfb
import drawing as dr
import sheetmodel as sm
import xlsfix
from targets import TEXT, CHECK, CHECK_X_CELLS, DESC

SRC = sys.argv[1] if len(sys.argv) > 1 else "furat_original.xls"
DST = sys.argv[2] if len(sys.argv) > 2 else "furat_diligenciado.xls"

# Formatos existentes idénticos a los de las letras guía, pero con letra negra (Bookman 8)
XF_DIGIT = {119: 429, 121: 429, 128: 430, 347: 430}
XF_DAY_X = 445          # mismo recuadro del día, letra negra en negrita
DESC_FIRST_ROW = 110    # E111 (base 0)
DESC_ROWS = 16          # E111:U126
DESC_WIDTH = 50         # caracteres por renglón (E:U, Bookman Old Style 8)


def parse_ref(ref):
    m = re.match(r"([A-Z]+)(\d+)$", ref)
    col = 0
    for ch in m.group(1):
        col = col * 26 + ord(ch) - 64
    return int(m.group(2)) - 1, col - 1


def xlstr(s):
    """XLUnicodeString para SST (comprimida si todos los caracteres son < 256)."""
    if all(ord(ch) < 256 for ch in s):
        return struct.pack("<HB", len(s), 0) + s.encode("latin-1")
    return struct.pack("<HB", len(s), 1) + s.encode("utf-16-le")


# ------------------------------------------------------------------ imagen de casilla marcada
CHECK_GLYPH = ["#.....#",
               ".#...#.",
               "..#.#..",
               "...#...",
               "..#.#..",
               ".#...#.",
               "#.....#"]


def checked_bits(bits, w, h, stride):
    """Dibuja una X centrada en el interior blanco de la casilla (24 bpp, filas de abajo hacia arriba)."""
    b = bytearray(bits)
    px = lambda x, y: bytes(b[y * stride + 3 * x:y * stride + 3 * x + 3])
    dark = [(x, y) for y in range(h) for x in range(w) if px(x, y) == b"\x69\x69\x69"]
    top = max(y for x, y in dark) - 1          # primera fila blanca bajo el borde oscuro superior
    left = min(x for x, y in dark) + 1
    right = left
    while right + 1 < w and px(right + 1, top) == b"\xff\xff\xff":
        right += 1
    bottom = top
    while bottom - 1 >= 0 and px(left, bottom - 1) == b"\xff\xff\xff":
        bottom -= 1
    iw, ih = right - left + 1, top - bottom + 1
    assert iw >= 7 and ih >= 7, (iw, ih)
    x0 = left + (iw - 7) // 2
    y0 = top - (ih - 7) // 2
    for y, line in enumerate(CHECK_GLYPH):
        for x, ch in enumerate(line):
            if ch == "#":
                o = (y0 - y) * stride + (x0 + x) * 3
                b[o:o + 3] = b"\x00\x00\x00"
    return bytes(b)


def patch_emf(emf):
    out = bytearray(emf)
    old_bits = new_bits = None
    for t, p, r in blips.emf_records(emf):
        if t == 81:   # EMR_STRETCHDIBITS
            ob, cb, obits, cbits = struct.unpack_from("<IIII", r, 48)
            _, w, h, _, bpp = struct.unpack_from("<IiiHH", r, ob)
            assert bpp == 24 and h > 0, (w, h, bpp)
            stride = ((w * bpp + 31) // 32) * 4
            old_bits = r[obits:obits + cbits]
            new_bits = checked_bits(old_bits, w, h, stride)
            out[p + obits:p + obits + cbits] = new_bits
    assert old_bits is not None
    # copia WMF embebida en el comentario GDIC (si contiene el mismo mapa de bits)
    k = bytes(out).find(old_bits)
    n_wmf = 0
    while k >= 0:
        out[k:k + len(old_bits)] = new_bits
        n_wmf += 1
        k = bytes(out).find(old_bits, k + 1)
    return bytes(out), n_wmf


def rebuild_dgg(dg, pibs_to_check):
    """Devuelve el bloque OfficeArtDggContainer con las imágenes de las casillas marcadas reemplazadas."""
    tree, bs = blips.bstore(dg)
    dgg_end = struct.unpack_from("<I", dg, 4)[0] + 8
    pieces = []          # (inicio, fin, bytes nuevos)
    report = []
    for pib in pibs_to_check:
        bse = bs["children"][pib - 1]
        d0 = bse["body"][0]
        cref = struct.unpack_from("<I", dg, d0 + 24)[0]
        assert cref == 1, "imagen compartida"
        bl, emf, info = blips.emf_of(dg, bse)
        new_emf, n_wmf = patch_emf(emf)
        comp = zlib.compress(new_emf, 9)
        p = bl["body"][0] + 16            # OfficeArtMetafileHeader
        hdr = bytearray(dg[p:p + 34])
        struct.pack_into("<I", hdr, 28, len(comp))
        hdr[32] = 0                       # compresión DEFLATE
        blip_body = dg[bl["body"][0]:p] + bytes(hdr) + comp
        blip_rec = dg[bl["pos"]:bl["pos"] + 4] + struct.pack("<I", len(blip_body)) + blip_body
        bse_fixed = bytearray(dg[d0:d0 + 36])
        struct.pack_into("<I", bse_fixed, 20, len(blip_rec))      # size
        new_bse = dg[bse["pos"]:bse["pos"] + 4] + struct.pack("<I", 36 + len(blip_rec)) + bytes(bse_fixed) + blip_rec
        pieces.append((bse["pos"], bse["body"][1], new_bse))
        report.append((pib, len(emf), n_wmf))
    pieces.sort()
    out = bytearray()
    cur = 0
    for a, b, nb in pieces:
        out += dg[cur:a] + nb
        cur = b
    out += dg[cur:]
    delta = len(out) - len(dg)
    # longitudes de los contenedores: DggContainer (pos 0) y BStoreContainer
    struct.pack_into("<I", out, 4, struct.unpack_from("<I", dg, 4)[0] + delta)
    struct.pack_into("<I", out, bs["pos"] + 4, struct.unpack_from("<I", dg, bs["pos"] + 4)[0] + delta)
    assert len(out) == dgg_end + delta
    return bytes(out), report


def chunks(data, n=8224):
    return [data[i:i + n] for i in range(0, len(data), n)] or [b""]


# ------------------------------------------------------------------ principal
def main():
    raw = open(SRC, "rb").read()
    c = cfb.CFB(raw)
    wb, recs, subs, strs = sm.load(c)
    glob, sheet = subs[0], subs[1]

    # ---------- celdas a escribir
    writes = {}                     # (r, c) -> (texto, xf o None)
    for ref, val in TEXT.items():
        writes[parse_ref(ref)] = (val, None)
    for ref, xf in CHECK_X_CELLS.items():
        writes[parse_ref(ref)] = ("X", xf)
    lines = textwrap.wrap(DESC, DESC_WIDTH)
    assert len(lines) <= DESC_ROWS, "descripción de %d renglones" % len(lines)
    for i, ln in enumerate(lines):
        writes[(DESC_FIRST_ROW + i, 4)] = (ln, None)
    writes[parse_ref("AL55")] = ("X", XF_DAY_X)    # día jueves: X en la casilla JU

    cells, merges, rows = sm.cells([r for r in sheet], strs)
    insertable = {parse_ref(ref) for ref in CHECK_X_CELLS}
    for (r, cc), (val, xf) in writes.items():
        k = cells.get((r, cc))
        if k is None:
            assert (r, cc) in insertable, "celda inexistente: " + sm.ref(r, cc)
            assert xf is not None, "la celda nueva necesita formato: " + sm.ref(r, cc)
            continue
        m = sm.merge_of(merges, r, cc)
        assert m is None or (m[0], m[2]) == (r, cc), "no es la celda superior izquierda: " + sm.ref(r, cc)

    # ---------- SST: cadenas nuevas
    new_strings = []
    index = {s: i for i, s in reversed(list(enumerate(strs)))}
    isst_of = {}
    for (r, cc), (val, xf) in sorted(writes.items()):
        if val in index:
            isst_of[(r, cc)] = index[val]
        else:
            index[val] = len(strs) + len(new_strings)
            new_strings.append(val)
            isst_of[(r, cc)] = index[val]

    # ---------- registros de la hoja
    new_sheet = []
    replaced_sst_refs = 0
    done = set()
    for pos, t, d in sheet:
        if t == 0x0201:               # BLANK
            r, cc, xf = struct.unpack_from("<HHH", d)
            if (r, cc) in writes:
                val, nxf = writes[(r, cc)]
                new_sheet.append((0x00FD, struct.pack("<HHHI", r, cc, nxf if nxf is not None else xf, isst_of[(r, cc)])))
                done.add((r, cc))
                continue
        elif t == 0x00BE:             # MULBLANK
            r, c1 = struct.unpack_from("<HH", d)
            n = (len(d) - 6) // 2
            xfs = [struct.unpack_from("<H", d, 4 + 2 * j)[0] for j in range(n)]
            if any((r, c1 + j) in writes for j in range(n)):
                run = []

                def flush(run):
                    if len(run) == 1:
                        new_sheet.append((0x0201, struct.pack("<HHH", r, run[0][0], run[0][1])))
                    elif run:
                        new_sheet.append((0x00BE, struct.pack("<HH", r, run[0][0]) +
                                          b"".join(struct.pack("<H", x) for _, x in run) +
                                          struct.pack("<H", run[-1][0])))
                for j in range(n):
                    col = c1 + j
                    if (r, col) in writes:
                        flush(run)
                        run = []
                        val, nxf = writes[(r, col)]
                        new_sheet.append((0x00FD, struct.pack("<HHHI", r, col, nxf if nxf is not None else xfs[j],
                                                              isst_of[(r, col)])))
                        done.add((r, col))
                    else:
                        run.append((col, xfs[j]))
                flush(run)
                continue
        elif t == 0x00FD:             # LABELSST (letras guía)
            r, cc, xf, isst = struct.unpack_from("<HHHI", d)
            if (r, cc) in writes:
                val, nxf = writes[(r, cc)]
                if nxf is None:
                    nxf = XF_DIGIT.get(xf, xf)
                new_sheet.append((0x00FD, struct.pack("<HHHI", r, cc, nxf, isst_of[(r, cc)])))
                replaced_sst_refs += 1
                done.add((r, cc))
                continue
        new_sheet.append((t, d))
    missing = set(writes) - done
    cell_records = {0x0006, 0x00FD, 0x0201, 0x00BE, 0x0203, 0x027E, 0x00BD, 0x0204, 0x0205}
    for r, cc in sorted(missing):
        val, nxf = writes[(r, cc)]
        assert nxf is not None, "la celda nueva necesita formato: " + sm.ref(r, cc)
        insert_at = None
        for j, (t, d) in enumerate(new_sheet):
            if t in cell_records:
                rr, c1 = struct.unpack_from("<HH", d)
                if (rr, c1) > (r, cc):
                    insert_at = j
                    break
        assert insert_at is not None, "sin posición para insertar " + sm.ref(r, cc)
        new_sheet.insert(insert_at, (0x00FD, struct.pack("<HHHI", r, cc, nxf, isst_of[(r, cc)])))
        done.add((r, cc))
    missing = set(writes) - done
    assert not missing, [sm.ref(*k) for k in missing]

    # ---------- casillas ActiveX
    found, objs, _ = dr.shapes(sheet)
    by_name = {}
    for f, (k, p, d) in zip(found, objs):
        by_name[f["name"]] = (f, dr.parse_obj(d))
    ctls = bytearray(c.read("/Ctls"))
    draw = b""
    for k, (p, t, d) in enumerate(sheet):
        if t == 0xEC:
            draw += d
        elif t == 0x3C and draw and sheet[k - 1][1] in (0xEC, 0x5D, 0x3C):
            draw += d
    pib_of = {}

    def walk(ns):
        for n in ns:
            if n["type"] == 0xF004:
                for ch in n["children"]:
                    if ch["type"] == 0xF00B:
                        pr = dr.fopt_props(draw, ch)
                        if 0x380 in pr:
                            pib_of[pr[0x380].decode("utf-16-le").rstrip("\x00")] = pr.get(0x104)
            walk(n["children"])
    walk(dr.art_records(draw))
    pibs = []
    for name in CHECK:
        f, o = by_name[name]
        off = o["lPosInCtlStm"]
        blob = ctls[off:off + o["cbBufInCtlStm"]]
        assert blob[:16] == bytes.fromhex("401dd28b42ecce119e0d00aa006002f3"), name     # CLSID CheckBox
        assert blob[16:28] == bytes.fromhex("000248004001c08001000000"), name           # PropMask
        assert blob[32:36] == b"\x01\x00\x00\x80" and blob[52] == 0x30, name           # Value = "0"
        ctls[off + 52] = 0x31                                                           # Value = "1"
        pibs.append(pib_of[name])

    # ---------- globales
    dg_raw, dg_idx = blips.dgg_bytes(glob)
    dgg_len = struct.unpack_from("<I", dg_raw, 4)[0] + 8
    assert dgg_len == len(dg_raw)
    new_dg, blip_report = rebuild_dgg(dg_raw, pibs)

    i_sst = [k for k, r in enumerate(glob) if r[1] == 0x00FC][0]
    sst_idx = [i_sst]
    k = i_sst + 1
    while glob[k][1] == 0x003C:
        sst_idx.append(k)
        k += 1
    sst_chunks = [bytearray(glob[j][2]) for j in sst_idx]
    total, uniq = struct.unpack_from("<II", sst_chunks[0])
    assert uniq == len(strs)
    for s in new_strings:
        b = xlstr(s)
        assert len(b) <= 8224
        if len(sst_chunks[-1]) + len(b) <= 8224:
            sst_chunks[-1] += b
        else:
            sst_chunks.append(bytearray(b))
    new_total = total - replaced_sst_refs + len(writes)
    struct.pack_into("<II", sst_chunks[0], 0, new_total, uniq + len(new_strings))

    new_glob = []
    for k, (p, t, d) in enumerate(glob):
        if k == dg_idx[0]:
            for j, ch in enumerate(chunks(new_dg)):
                new_glob.append((0x00EB if j == 0 else 0x003C, ch))
        elif k in dg_idx[1:]:
            continue
        elif k == i_sst:
            for j, ch in enumerate(sst_chunks):
                new_glob.append((0x00FC if j == 0 else 0x003C, bytes(ch)))
        elif k in sst_idx[1:]:
            continue
        elif t == 0x00FF:
            n_b = (uniq + len(new_strings) + 7) // 8
            new_glob.append((t, b"\x00" * (2 + 8 * n_b)))
        else:
            new_glob.append((t, d))

    # ---------- ensamblar y recalcular posiciones
    others = [[(t, d) for p, t, d in s] for s in subs[2:]]
    sheets = [new_sheet] + others
    gbytes, gpos = xlsfix.serialize(new_glob)
    sheet_bases = []
    cur = len(gbytes)
    for s in sheets:
        sheet_bases.append(cur)
        cur += len(xlsfix.serialize(s)[0])
    # BOUNDSHEET
    bi = 0
    for k, (t, d) in enumerate(new_glob):
        if t == 0x0085:
            new_glob[k] = (t, struct.pack("<I", sheet_bases[bi]) + d[4:])
            bi += 1
    assert bi == len(sheets)
    # EXTSST
    gbytes, gpos = xlsfix.serialize(new_glob)
    k_sst = [k for k, (t, d) in enumerate(new_glob) if t == 0x00FC][0]
    sst_rec_idx = list(range(k_sst, k_sst + len(sst_chunks)))
    starts = xlsfix.sst_string_starts([bytes(x) for x in sst_chunks])
    ext = xlsfix.build_extsst(starts, [gpos[j] for j in sst_rec_idx])
    k_ext = [k for k, (t, d) in enumerate(new_glob) if t == 0x00FF][0]
    assert len(ext) == len(new_glob[k_ext][1])
    new_glob[k_ext] = (0x00FF, ext)
    gbytes, gpos = xlsfix.serialize(new_glob)
    out = bytearray(gbytes)
    for base, s in zip(sheet_bases, sheets):
        sb, sp = xlsfix.serialize(s)
        fixed = xlsfix.fix_sheet(s, sp, base)
        fb, _ = xlsfix.serialize(fixed)
        assert len(fb) == len(sb)
        assert len(out) == base
        out += fb
    # bytes que había después del último EOF (relleno), si los hay
    last = subs[-1][-1]
    tail = wb[last[0] + 4 + len(last[2]):]
    covered = sum(len(xlsfix.serialize([(t, d) for p, t, d in s])[0]) for s in subs)
    assert covered == last[0] + 4 + len(last[2]), "hay registros fuera de BOF/EOF"
    out += tail

    c.write_stream("/Workbook", bytes(out))
    c.write_stream("/Ctls", bytes(ctls))
    open(DST, "wb").write(c.bytes())
    print("celdas escritas:", len(writes), "| cadenas nuevas:", len(new_strings), "| casillas:", len(CHECK))
    print("renglones de descripción:", len(lines))
    for ln in lines:
        print("   |" + ln)
    print("imágenes de casilla actualizadas (pib, bytes EMF, copias WMF):", blip_report[:3], "...")
    print("Workbook:", len(wb), "->", len(out), "bytes")


if __name__ == "__main__":
    main()
