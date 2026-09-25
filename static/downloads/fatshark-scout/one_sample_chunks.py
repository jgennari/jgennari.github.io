#!/usr/bin/env python3
"""Expand nonfragmented MP4 chunk tables without changing media payloads."""
import struct
import sys
from pathlib import Path


def u32(b, p=0):
    return struct.unpack_from('>I', b, p)[0]


def box(kind, payload):
    return struct.pack('>I4s', 8 + len(payload), kind) + payload


def boxes(data):
    pos = 0
    while pos < len(data):
        size = u32(data, pos)
        assert 8 <= size <= len(data) - pos, (pos, size)
        yield data[pos+4:pos+8], data[pos+8:pos+size]
        pos += size
    assert pos == len(data)


def rewrite(kind, payload):
    if kind == b'stbl':
        children = list(boxes(payload))
        table = dict(children)
        assert b'stco' in table and b'co64' not in table
        sz, sc, co = (table[t] for t in (b'stsz', b'stsc', b'stco'))
        sample_size, sample_count = u32(sz, 4), u32(sz, 8)
        sizes = ([sample_size] * sample_count if sample_size else
                 [u32(sz, 12+4*i) for i in range(sample_count)])
        entries = [struct.unpack_from('>III', sc, 8+12*i)
                   for i in range(u32(sc, 4))]
        offsets = [u32(co, 8+4*i) for i in range(u32(co, 4))]
        assert entries and entries[0][0] == 1
        assert len({e[2] for e in entries}) == 1
        expanded, sample_index, entry_index = [], 0, 0
        for chunk, offset in enumerate(offsets, 1):
            while entry_index+1 < len(entries) and entries[entry_index+1][0] <= chunk:
                entry_index += 1
            for _ in range(entries[entry_index][1]):
                assert sample_index < sample_count
                expanded.append(offset)
                offset += sizes[sample_index]
                sample_index += 1
        assert sample_index == sample_count
        new_sc = struct.pack('>IIIII', 0, 1, 1, 1, entries[0][2])
        new_co = struct.pack('>II', 0, sample_count) + b''.join(
            struct.pack('>I', offset) for offset in expanded)
        print(f'{len(offsets)} chunks -> {sample_count} single-sample chunks')
        payload = b''.join(box(t, new_sc if t == b'stsc' else
                              new_co if t == b'stco' else p)
                           for t, p in children)
    elif kind in (b'moov', b'trak', b'mdia', b'minf'):
        payload = b''.join(rewrite(t, p) for t, p in boxes(payload))
    return box(kind, payload)


def convert(source, destination):
    # Stream the media prefix so a feature-length movie need not fit in RAM.
    length = source.stat().st_size
    with source.open('rb') as src:
        top, pos = [], 0
        while pos < length:
            src.seek(pos)
            header = src.read(8)
            assert len(header) == 8
            size, kind = struct.unpack('>I4s', header)
            assert 8 <= size <= length - pos, (pos, size)
            top.append((kind, pos, size))
            pos += size
        assert pos == length
        assert top[-1][0] == b'moov', 'Requires moov after all media data'
        assert sum(t == b'moov' for t, _, _ in top) == 1
        assert any(t == b'mdat' for t, _, _ in top)
        assert not any(t == b'moof' for t, _, _ in top)
        _, prefix_size, moov_size = top[-1]
        src.seek(prefix_size + 8)
        payload = src.read(moov_size - 8)
        assert len(payload) == moov_size - 8
        new_moov = rewrite(b'moov', payload)
        src.seek(0)
        with destination.open('xb') as dst:
            remaining = prefix_size
            while remaining:
                block = src.read(min(1024 * 1024, remaining))
                assert block
                dst.write(block)
                remaining -= len(block)
            dst.write(new_moov)


if __name__ == '__main__':
    convert(Path(sys.argv[1]), Path(sys.argv[2]))
