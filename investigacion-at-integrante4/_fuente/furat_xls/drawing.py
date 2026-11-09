# -*- coding: utf-8 -*-
"""Objetos de dibujo (OfficeArt) y OBJ de una hoja BIFF8; controles ActiveX."""
import struct


def art_records(data, pos=0, end=None, depth=0):
    end = len(data) if end is None else end
    out = []
    while pos + 8 <= end:
        verinst, rt, ln = struct.unpack_from("<HHI", data, pos)
        ver = verinst & 0xF
        inst = verinst >> 4
        body = (pos + 8, pos + 8 + ln)
        node = {"type": rt, "inst": inst, "ver": ver, "pos": pos, "body": body, "children": []}
        if ver == 0xF:
            node["children"] = art_records(data, body[0], body[1], depth + 1)
        out.append(node)
        pos = body[1]
    return out


def fopt_props(data, node):
    n = node["inst"]
    pos = node["body"][0]
    props = {}
    complex_data = pos + 6 * n
    entries = []
    for i in range(n):
        pid, val = struct.unpack_from("<HI", data, pos + 6 * i)
        entries.append((pid, val))
    cd = complex_data
    for pid, val in entries:
        num = pid & 0x3FFF
        if pid & 0x8000:
            props[num] = data[cd:cd + val]
            cd += val
        else:
            props[num] = val
    return props


def shapes(sheet_recs):
    """Devuelve lista de figuras con su anclaje y su OBJ asociado."""
    draw = b""
    marks = []        # (offset en flujo de dibujo, indice registro)
    objs = []
    for k, (pos, t, d) in enumerate(sheet_recs):
        if t == 0x00EC:
            draw += d
        elif t == 0x003C and k and sheet_recs[k - 1][1] in (0x00EC, 0x005D, 0x003C) and draw:
            draw += d
        elif t == 0x005D:
            objs.append((k, pos, d))
    tree = art_records(draw)
    found = []

    def walk(nodes):
        for nd in nodes:
            if nd["type"] == 0xF004:
                info = {}
                for ch in nd["children"]:
                    if ch["type"] == 0xF00A:
                        info["spid"], info["flags"] = struct.unpack_from("<II", draw, ch["body"][0])
                        info["shape_type"] = ch["inst"]
                    elif ch["type"] == 0xF010:
                        info["anchor"] = struct.unpack_from("<HHHHHHHHH", draw, ch["body"][0])
                    elif ch["type"] == 0xF00B:
                        props = fopt_props(draw, ch)
                        if 0x0380 in props and isinstance(props[0x0380], (bytes, bytearray)):
                            info["name"] = props[0x0380].decode("utf-16-le").rstrip("\x00")
                    elif ch["type"] == 0xF011:
                        info["clientdata"] = True
                if "anchor" in info:
                    found.append(info)
            if nd["children"]:
                walk(nd["children"])
    walk(tree)
    return found, objs, draw


def parse_obj(d):
    """Subregistros de OBJ: ftCmo y ftPictFmla."""
    out = {}
    pos = 0
    while pos + 4 <= len(d):
        ft, cb = struct.unpack_from("<HH", d, pos)
        body = d[pos + 4:pos + 4 + cb]
        if ft == 0x15:
            ot, oid, flags = struct.unpack_from("<HHH", body)
            out["ot"], out["id"], out["flags"] = ot, oid, flags
        elif ft == 0x09:
            out["pictfmla_off"] = pos
            out["pictfmla"] = body
            # ObjFmla: cbFmla(2) + Fmla (cce(2), unused(4), rgce)
            cbf = struct.unpack_from("<H", body)[0]
            fm = body[2:2 + cbf]
            cce = struct.unpack_from("<H", fm)[0]
            rgce = fm[6:6 + cce]
            prog = None
            # PtgTbl / embedded string: buscar "Forms."
            i = rgce.find(b"Forms.")
            if i >= 0:
                prog = rgce[i:].split(b"\x00")[0].decode("latin-1")
            out["progid"] = prog
            rest = body[2 + cbf:]
            if len(rest) >= 8:
                out["lPosInCtlStm"], out["cbBufInCtlStm"] = struct.unpack_from("<II", rest)
                out["pict_rest_off"] = pos + 4 + 2 + cbf
        elif ft == 0x00:
            break
        if ft == 0x09:
            # ftPictFmla puede tener cb incorrecto; se respeta cb del registro
            pass
        pos += 4 + cb
    return out
