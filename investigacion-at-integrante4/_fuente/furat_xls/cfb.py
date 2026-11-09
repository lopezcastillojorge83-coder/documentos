# -*- coding: utf-8 -*-
"""Lectura y modificación de archivos Compound File Binary (MS-CFB), sin dependencias."""
import struct

FREESECT, ENDOFCHAIN, FATSECT, DIFSECT = 0xFFFFFFFF, 0xFFFFFFFE, 0xFFFFFFFD, 0xFFFFFFFC
NOSTREAM = 0xFFFFFFFF


class Entry:
    def __init__(self, idx, raw):
        self.idx = idx
        self.raw = bytearray(raw)
        nlen = struct.unpack_from("<H", raw, 64)[0]
        self.name = raw[:max(nlen - 2, 0)].decode("utf-16-le")
        self.type = raw[66]          # 1 storage, 2 stream, 5 root
        self.left, self.right, self.child = struct.unpack_from("<III", raw, 68)
        self.start = struct.unpack_from("<I", raw, 116)[0]
        self.size = struct.unpack_from("<Q", raw, 120)[0]

    def set_start_size(self, start, size):
        self.start, self.size = start, size
        struct.pack_into("<I", self.raw, 116, start)
        struct.pack_into("<Q", self.raw, 120, size)


class CFB:
    def __init__(self, data):
        self.data = bytearray(data)
        h = self.data[:512]
        assert h[:8] == bytes.fromhex("d0cf11e0a1b11ae1"), "no es un archivo OLE2"
        self.major = struct.unpack_from("<H", h, 26)[0]
        self.ssz = 1 << struct.unpack_from("<H", h, 30)[0]
        self.mssz = 1 << struct.unpack_from("<H", h, 32)[0]
        assert self.ssz == 512, "solo se soporta sector de 512 bytes"
        self.nfat = struct.unpack_from("<I", h, 44)[0]
        self.dir_start = struct.unpack_from("<I", h, 48)[0]
        self.cutoff = struct.unpack_from("<I", h, 56)[0]
        self.minifat_start, self.nminifat = struct.unpack_from("<II", h, 60)
        self.difat_start, self.ndifat = struct.unpack_from("<II", h, 68)
        difat = list(struct.unpack_from("<109I", h, 76))
        s = self.difat_start
        for _ in range(self.ndifat):
            sec = self.sector(s)
            vals = struct.unpack("<128I", sec)
            difat += vals[:127]
            s = vals[127]
        self.fat_sectors = [x for x in difat if x not in (FREESECT, ENDOFCHAIN)][:self.nfat]
        self.fat = []
        for fs in self.fat_sectors:
            self.fat += struct.unpack("<128I", self.sector(fs))
        dir_bytes = self.read_chain(self.dir_start)
        self.dir_chain = self.chain(self.dir_start)
        self.entries = [Entry(i, dir_bytes[i * 128:(i + 1) * 128]) for i in range(len(dir_bytes) // 128)]
        self.root = self.entries[0]
        self.minifat = []
        if self.nminifat:
            mf = self.read_chain(self.minifat_start)
            self.minifat = list(struct.unpack("<%dI" % (len(mf) // 4), mf))
        self.ministream = self.read_chain(self.root.start)[:self.root.size] if self.root.start != ENDOFCHAIN else b""

    # ---------------------------------------------------------------- lectura
    def sector(self, n):
        off = 512 + n * 512
        return bytes(self.data[off:off + 512])

    def chain(self, start, fat=None):
        fat = self.fat if fat is None else fat
        out, s, seen = [], start, set()
        while s not in (ENDOFCHAIN, FREESECT):
            assert s not in seen, "cadena circular"
            seen.add(s)
            out.append(s)
            s = fat[s]
        return out

    def read_chain(self, start):
        return b"".join(self.sector(s) for s in self.chain(start))

    def path(self, e):
        """Rutas completas de las entradas (recorre el árbol rojo-negro)."""
        paths = {}

        def walk(idx, prefix):
            if idx == NOSTREAM:
                return
            en = self.entries[idx]
            walk(en.left, prefix)
            walk(en.right, prefix)
            p = prefix + "/" + en.name
            paths[idx] = p
            if en.child != NOSTREAM:
                walk(en.child, p)
        walk(self.root.child, "")
        return paths

    def find(self, path):
        for idx, p in self.path(None).items():
            if p == path:
                return self.entries[idx]
        raise KeyError(path)

    def read(self, path):
        e = self.find(path)
        if e.size < self.cutoff:
            out = b"".join(self.ministream[s * 64:(s + 1) * 64] for s in self.chain(e.start, self.minifat))
        else:
            out = self.read_chain(e.start)
        return out[:e.size]

    # ---------------------------------------------------------------- escritura
    def _write_sector(self, n, payload):
        off = 512 + n * 512
        need = off + 512
        if len(self.data) < need:
            self.data.extend(b"\x00" * (need - len(self.data)))
        self.data[off:off + 512] = payload.ljust(512, b"\x00")

    def _alloc(self):
        """Nuevo sector al final del archivo (amplía la FAT si hace falta)."""
        n = (len(self.data) - 512) // 512
        while len(self.fat) <= n:
            self._grow_fat()
            n = (len(self.data) - 512) // 512
        self.fat[n] = ENDOFCHAIN
        self._write_sector(n, b"")
        return n

    def _grow_fat(self):
        n = (len(self.data) - 512) // 512
        assert len(self.fat_sectors) < 109, "se requeriría DIFAT adicional"
        self.fat_sectors.append(n)
        self.fat += [FREESECT] * 128
        self.fat[n] = FATSECT
        self._write_sector(n, b"")

    def write_stream(self, path, newdata):
        """Reemplaza el contenido de un flujo regular (>= cutoff) conservando el resto del archivo."""
        e = self.find(path)
        assert e.size >= self.cutoff and len(newdata) >= self.cutoff, "solo flujos regulares"
        old = self.chain(e.start)
        need = (len(newdata) + 511) // 512
        secs = old[:need]
        for s in old[need:]:
            self.fat[s] = FREESECT
        while len(secs) < need:
            secs.append(self._alloc())
        for a, b in zip(secs, secs[1:]):
            self.fat[a] = b
        self.fat[secs[-1]] = ENDOFCHAIN
        for i, s in enumerate(secs):
            self._write_sector(s, bytes(newdata[i * 512:(i + 1) * 512]))
        e.set_start_size(secs[0], len(newdata))
        self._flush_meta()

    def _flush_meta(self):
        # FAT
        for i, fs in enumerate(self.fat_sectors):
            self.fat[fs] = FATSECT
        for i, fs in enumerate(self.fat_sectors):
            self._write_sector(fs, struct.pack("<128I", *self.fat[i * 128:(i + 1) * 128]))
        # directorio
        for i, s in enumerate(self.dir_chain):
            blob = b"".join(bytes(en.raw) for en in self.entries[i * 4:(i + 1) * 4])
            self._write_sector(s, blob)
        # encabezado
        struct.pack_into("<I", self.data, 44, len(self.fat_sectors))
        difat = self.fat_sectors + [FREESECT] * (109 - len(self.fat_sectors))
        struct.pack_into("<109I", self.data, 76, *difat)

    def bytes(self):
        return bytes(self.data)
