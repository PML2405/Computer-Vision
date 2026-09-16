#!/usr/bin/env python3
"""Extract embedded raster images from a PDF. DCTDecode -> .jpg (direct),
DeviceRGB/Gray FlateDecode -> .png (rebuilt). Pure stdlib. Also maps which
images appear on which page via Do operators when possible.
Usage: extract_images.py FILE OUTDIR [min_pixels]"""
import sys, re, zlib, struct, os

def png_write(path, w, h, mode, raw):
    # mode: 'gray' (1 byte/px) or 'rgb' (3 bytes/px)
    ch = 1 if mode == 'gray' else 3
    ctype = 0 if mode == 'gray' else 2
    stride = w * ch
    # add filter byte (0) per scanline
    out = bytearray()
    for y in range(h):
        out.append(0)
        out.extend(raw[y*stride:(y+1)*stride])
    comp = zlib.compress(bytes(out), 6)
    def chunk(typ, data):
        c = struct.pack('>I', len(data)) + typ + data
        c += struct.pack('>I', zlib.crc32(typ + data) & 0xffffffff)
        return c
    sig = b'\x89PNG\r\n\x1a\n'
    ihdr = struct.pack('>IIBBBBB', w, h, 8, ctype, 0, 0, 0)
    with open(path, 'wb') as f:
        f.write(sig)
        f.write(chunk(b'IHDR', ihdr))
        f.write(chunk(b'IDAT', comp))
        f.write(chunk(b'IEND', b''))

def find_objects(data):
    objs = {}
    for m in re.finditer(rb'(\d+)\s+(\d+)\s+obj\b', data):
        num = int(m.group(1))
        start = m.end()
        e = data.find(b'endobj', start)
        if e == -1: continue
        objs[num] = data[start:e]
    return objs

def get_stream(body):
    s = body.find(b'stream')
    if s == -1: return None
    j = s + 6
    if body[j:j+2] == b'\r\n': j += 2
    elif body[j:j+1] in (b'\n', b'\r'): j += 1
    e = body.find(b'endstream', j)
    if e == -1: return None
    return body[j:e]

def num(body, key):
    m = re.search(key.encode() + rb'\s+(\d+)', body)
    return int(m.group(1)) if m else None

def main():
    fn = sys.argv[1]; outdir = sys.argv[2]
    minpx = int(sys.argv[3]) if len(sys.argv) > 3 else 40000
    os.makedirs(outdir, exist_ok=True)
    data = open(fn, 'rb').read()
    objs = find_objects(data)
    manifest = []
    for numid, body in objs.items():
        head = body[:600]
        if b'/Subtype' not in head or b'/Image' not in head:
            # sometimes dict longer; check whole body head region up to 'stream'
            si = body.find(b'stream')
            head = body[:si if si!=-1 else 600]
            if b'/Image' not in head: continue
        w = num(head, '/Width'); h = num(head, '/Height')
        if not w or not h: continue
        if w*h < minpx: continue
        raw = get_stream(body)
        if raw is None: continue
        is_dct = b'/DCTDecode' in head
        is_flate = b'/FlateDecode' in head
        cs = 'rgb'
        if b'/DeviceGray' in head or b'/CalGray' in head: cs = 'gray'
        elif b'/DeviceCMYK' in head: cs = 'cmyk'
        bpc = num(head, '/BitsPerComponent') or 8
        base = f"img_obj{numid}_{w}x{h}"
        try:
            if is_dct:
                path = os.path.join(outdir, base + ".jpg")
                open(path,'wb').write(raw)
                manifest.append((numid, w, h, 'jpg', cs, path))
            elif is_flate and bpc == 8 and cs in ('rgb','gray'):
                dec = zlib.decompress(raw)
                expect = w*h*(1 if cs=='gray' else 3)
                if len(dec) >= expect:
                    path = os.path.join(outdir, base + ".png")
                    png_write(path, w, h, cs, dec[:expect])
                    manifest.append((numid, w, h, 'png', cs, path))
                else:
                    manifest.append((numid, w, h, 'skip-size', cs, f'got {len(dec)} need {expect}'))
            else:
                manifest.append((numid, w, h, 'skip-fmt', cs, 'dct=%s flate=%s bpc=%s'%(is_dct,is_flate,bpc)))
        except Exception as ex:
            manifest.append((numid, w, h, 'err', cs, str(ex)[:60]))
    manifest.sort(key=lambda r: -(r[1]*r[2]))
    for r in manifest:
        print(f"obj {r[0]:5d}  {r[1]}x{r[2]:5d}  {r[3]:9s} {r[4]:5s}  {r[5]}")
    saved = sum(1 for r in manifest if r[3] in ('jpg','png'))
    print(f"\n[saved {saved} images to {outdir}]", file=sys.stderr)

if __name__ == '__main__':
    main()
