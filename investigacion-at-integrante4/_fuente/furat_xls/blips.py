import struct, zlib
import drawing as dr

def dgg_bytes(g):
    dg = b''
    idx = []
    for k, (p, t, d) in enumerate(g):
        if t == 0xEB:
            dg += d; idx.append(k)
        elif t == 0x3c and idx and idx[-1] == k - 1:
            dg += d; idx.append(k)
    return dg, idx

def bstore(dg):
    t = dr.art_records(dg, 0, struct.unpack_from('<I', dg, 4)[0] + 8)
    bs = [n for n in t[0]['children'] if n['type'] == 0xF001][0]
    return t, bs

def emf_of(dg, bse):
    b0 = bse['body'][0] + 36
    bl = dr.art_records(dg, b0, bse['body'][1])[0]
    p = bl['body'][0] + 16
    cbSize, = struct.unpack_from('<I', dg, p)
    rc = struct.unpack_from('<iiii', dg, p + 4)
    pt = struct.unpack_from('<ii', dg, p + 20)
    cbSave, comp, filt = struct.unpack_from('<IBB', dg, p + 28)
    raw = dg[p + 34:p + 34 + cbSave]
    data = zlib.decompress(raw) if comp == 0 else raw
    assert len(data) == cbSize
    return bl, data, (rc, pt, comp, filt)

EMR = {1:'HEADER',14:'EOF',9:'SETWINDOWEXTEX',10:'SETWINDOWORGEX',11:'SETVIEWPORTEXTEX',12:'SETVIEWPORTORGEX',
       17:'SETMAPMODE',18:'SETBKMODE',19:'SETPOLYFILLMODE',20:'SETROP2',22:'SETTEXTALIGN',24:'SETTEXTCOLOR',25:'SETBKCOLOR',
       27:'MOVETOEX',33:'SAVEDC',34:'RESTOREDC',37:'SELECTOBJECT',38:'CREATEPEN',39:'CREATEBRUSHINDIRECT',40:'DELETEOBJECT',
       42:'ELLIPSE',43:'RECTANGLE',54:'LINETO',76:'BITBLT',81:'STRETCHDIBITS',82:'EXTCREATEFONTINDIRECTW',84:'EXTTEXTOUTW',
       86:'POLYGON16',87:'POLYLINE16',88:'POLYBEZIERTO16',89:'POLYLINETO16',90:'POLYPOLYLINE16',91:'POLYPOLYGON16',95:'EXTCREATEPEN',
       70:'GDICOMMENT',30:'INTERSECTCLIPRECT',67:'SELECTCLIPPATH',75:'EXTSELECTCLIPRGN',59:'BEGINPATH',60:'ENDPATH',62:'FILLPATH',
       98:'SETICMMODE',115:'SETLAYOUT',13:'SETBRUSHORGEX',21:'SETSTRETCHBLTMODE',16:'SETMAPPERFLAGS',36:'MODIFYWORLDTRANSFORM',35:'SETWORLDTRANSFORM',
       58:'SETMITERLIMIT',39:'CREATEBRUSHINDIRECT',80:'SETDIBITSTODEVICE'}

def emf_records(data):
    out = []; p = 0
    while p < len(data):
        t, n = struct.unpack_from('<II', data, p)
        out.append((t, p, data[p:p + n])); p += n
        if t == 14: break
    return out
