import sys, struct, re
import cfb, sheetmodel as sm, xlsfix, blips, drawing as dr
from targets import TEXT, CHECK, CHECK_X_CELLS
A = cfb.CFB(open(sys.argv[1], 'rb').read()); B = cfb.CFB(open(sys.argv[2], 'rb').read())
pa = A.path(None); pb = B.path(None)
assert sorted(pa.values()) == sorted(pb.values())
for p in sorted(pa.values()):
    ea, eb = A.find(p), B.find(p)
    if ea.type != 2: continue
    same = A.read(p) == B.read(p)
    if not same: print('flujo modificado:', p, ea.size, '->', eb.size)
# cadenas FAT: sin sectores compartidos
used = {}
for idx, p in pb.items():
    e = B.entries[idx]
    if e.type == 2 and e.size >= B.cutoff:
        for s in B.chain(e.start):
            assert s not in used, ('sector compartido', p, used[s]); used[s] = p
for s in B.chain(B.dir_start): assert s not in used; used[s] = 'dir'
mf = B.chain(B.minifat_start) if B.nminifat else []
for s in mf: assert s not in used; used[s] = 'minifat'
for s in B.chain(B.root.start): assert s not in used; used[s] = 'ministream'
print('sectores en uso sin solaparse:', len(used))
wa, ra, sa, stra = sm.load(A); wbb, rb, sb, strb = sm.load(B)
assert strb[:len(stra)] == stra
print('SST:', len(stra), '->', len(strb))
# registros: tipos por hoja
for i, (x, y) in enumerate(zip(sa, sb)):
    from collections import Counter
    ca = Counter(t for p, t, d in x); cb_ = Counter(t for p, t, d in y)
    diff = {('%x' % k): (ca[k], cb_[k]) for k in set(ca) | set(cb_) if ca[k] != cb_[k]}
    print('subflujo', i, 'registros', len(x), '->', len(y), 'diferencias', diff)
    if i >= 2:
        assert [(t, d) for p, t, d in x if t not in (0x20B, 0xD7)] == [(t, d) for p, t, d in y if t not in (0x20B, 0xD7)]
# BOUNDSHEET
bs = [struct.unpack_from('<I', d)[0] for p, t, d in sb[0] if t == 0x85]
assert bs == [s[0][0] for s in sb[1:]], (bs, [s[0][0] for s in sb[1:]])
# INDEX/DBCELL idempotentes
for s in sb[1:]:
    base = s[0][0]; rr = [(t, d) for p, t, d in s]
    assert xlsfix.fix_sheet(rr, [p - base for p, t, d in s], base) == rr
# EXTSST
g = sb[0]; i = [k for k, r in enumerate(g) if r[1] == 0xFC][0]; idx = [i]; k = i + 1
while g[k][1] == 0x3C: idx.append(k); k += 1
st = xlsfix.sst_string_starts([g[j][2] for j in idx])
assert xlsfix.build_extsst(st, [g[j][0] for j in idx]) == [d for p, t, d in g if t == 0xFF][0]
tot, un = struct.unpack_from('<II', g[i][2])
nref = sum(1 for s in sb[1:] for p, t, d in s if t == 0xFD)
print('cstTotal', tot, 'LABELSST en hojas', nref, 'cstUnique', un, len(strb))
# DGG
dg, _ = blips.dgg_bytes(g); assert struct.unpack_from('<I', dg, 4)[0] + 8 == len(dg)
t, bst = blips.bstore(dg)
n_ok = 0
for b in bst['children']:
    try:
        blips.emf_of(dg, b); n_ok += 1
    except Exception: pass
print('imágenes EMF legibles:', n_ok, 'de', len(bst['children']))
# celdas
cells, merges, rows = sm.cells(sb[1], strb)
def pr(ref):
    m = re.match(r'([A-Z]+)(\d+)$', ref); c = 0
    for ch in m.group(1): c = c * 26 + ord(ch) - 64
    return int(m.group(2)) - 1, c - 1
bad = [r for r, v in TEXT.items() if cells.get(pr(r), (0, 0, None))[2] != v]
bad_x = [r for r in CHECK_X_CELLS if cells.get(pr(r), (0, 0, None))[2] != 'X']
print('campos con valor distinto al esperado:', bad)
print('casillas sin X literal:', bad_x)
assert not bad and not bad_x
cellsA, _, _ = sm.cells(sa[1], stra)
changed = [sm.ref(*k) for k in cellsA if cellsA[k] != cells.get(k)]
print('celdas cambiadas:', len(changed))
ctl = B.read('/Ctls'); ctlA = A.read('/Ctls')
diff = [i for i in range(len(ctl)) if ctl[i] != ctlA[i]]
print('bytes cambiados en Ctls:', len(diff), 'casillas esperadas:', len(CHECK))
assert len(diff) == len(CHECK)
