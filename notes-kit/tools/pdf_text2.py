#!/usr/bin/env python3
"""Font-aware, page-ORDERED PDF text extraction (pure stdlib).
Handles: classic objects + /ObjStm, page-tree order, TrueType (1-byte) fonts,
Type0/CID (2-byte) fonts, per-font /ToUnicode CMaps, literal (..) and <hex> strings.
Usage: pdf_text2.py FILE OUTFILE [start_page] [end_page]
"""
import sys, re, zlib

# ---------------- object model ----------------
def get_stream_bytes(body):
    s = body.find(b'stream')
    if s == -1: return None
    j = s+6
    if body[j:j+2]==b'\r\n': j+=2
    elif body[j:j+1] in (b'\n',b'\r'): j+=1
    e = body.find(b'endstream', j)
    if e==-1: return None
    return body[j:e]

def inflate(raw):
    if raw is None: return None
    for a in (raw, raw.rstrip(b'\r\n'), raw.rstrip()):
        try: return zlib.decompress(a)
        except Exception: pass
    try: return zlib.decompressobj(-zlib.MAX_WBITS).decompress(raw)
    except Exception: return None

def build_objmap(data):
    objmap = {}
    for m in re.finditer(rb'(\d+)\s+(\d+)\s+obj\b', data):
        num=int(m.group(1)); start=m.end()
        e=data.find(b'endobj', start)
        if e==-1: continue
        objmap[num]=data[start:e]
    for n in [n for n,b in objmap.items() if b'/ObjStm' in b[:400]]:
        body=objmap[n]; raw=get_stream_bytes(body); dec=inflate(raw)
        if dec is None: continue
        mN=re.search(rb'/N\s+(\d+)', body); mF=re.search(rb'/First\s+(\d+)', body)
        if not mN or not mF: continue
        N=int(mN.group(1)); first=int(mF.group(1))
        nums=[int(x) for x in re.findall(rb'\d+', dec[:first])][:2*N]
        for i in range(0,len(nums),2):
            onum=nums[i]; off=nums[i+1]
            nxt=nums[i+3] if i+3<len(nums) else None
            seg=dec[first+off: first+nxt] if nxt is not None else dec[first+off:]
            if onum not in objmap: objmap[onum]=seg
    return objmap

def ref(body, key):
    m=re.search(re.escape(key.encode())+rb'\s+(\d+)\s+\d+\s+R', body)
    return int(m.group(1)) if m else None

def ordered_pages(objmap):
    root=None
    for n,b in objmap.items():
        if b'/Type/Catalog' in b or b'/Type /Catalog' in b: root=n; break
    if root is None: return []
    pages_ref=ref(objmap[root],'/Pages')
    order=[]; seen=set()
    def walk(num, depth=0):
        if num in seen or depth>60: return
        seen.add(num)
        b=objmap.get(num)
        if b is None: return
        is_node = (b'/Type/Pages' in b) or (b'/Type /Pages' in b)
        if is_node:
            km=re.search(rb'/Kids\s*\[(.*?)\]', b, re.DOTALL)
            if km:
                for k in [int(x) for x in re.findall(rb'(\d+)\s+\d+\s+R', km.group(1))]:
                    walk(k, depth+1)
        else:
            order.append(num)
    walk(pages_ref)
    return order

# ---------------- CMap (ToUnicode) parsing ----------------
def parse_tounicode(cmap_bytes):
    m={}
    for blk in re.findall(rb'beginbfchar(.*?)endbfchar', cmap_bytes, re.DOTALL):
        for a,b in re.findall(rb'<([0-9A-Fa-f]+)>\s*<([0-9A-Fa-f]+)>', blk):
            try:
                src=int(a,16)
                dst=bytes.fromhex(b.decode())
                m[src]=dst.decode('utf-16-be','replace')
            except Exception: pass
    for blk in re.findall(rb'beginbfrange(.*?)endbfrange', cmap_bytes, re.DOTALL):
        for lo,hi,dst in re.findall(rb'<([0-9A-Fa-f]+)>\s*<([0-9A-Fa-f]+)>\s*<([0-9A-Fa-f]+)>', blk):
            try:
                l=int(lo,16); h=int(hi,16); base=bytes.fromhex(dst.decode())
                bu=base.decode('utf-16-be','replace')
                start_cp=ord(bu[-1]) if bu else 0
                for k,code in enumerate(range(l,h+1)):
                    m[code]=(bu[:-1]+chr(start_cp+k)) if bu else ''
            except Exception: pass
    return m

def codespace_bytes(cmap_bytes):
    mm=re.search(rb'begincodespacerange(.*?)endcodespacerange', cmap_bytes, re.DOTALL)
    if mm:
        h=re.search(rb'<([0-9A-Fa-f]+)>', mm.group(1))
        if h: return max(1, len(h.group(1))//2)
    return None

def get_page_fonts(objmap, pagebody):
    """Return {resource_name: (tounicode_map or None, code_bytes)}"""
    res_ref=ref(pagebody,'/Resources')
    resbody = objmap.get(res_ref) if res_ref else None
    if resbody is None:
        mm=re.search(rb'/Resources\s*<<(.*)', pagebody, re.DOTALL)
        resbody = mm.group(0) if mm else pagebody
    fm=re.search(rb'/Font\s*<<(.*?)>>', resbody, re.DOTALL)
    fonts={}
    if not fm:
        fref=ref(resbody,'/Font')
        fbody=objmap.get(fref) if fref else None
        if fbody is None: return fonts
        fm=re.search(rb'<<(.*?)>>', fbody, re.DOTALL)
        if not fm: return fonts
    for name,onum in re.findall(rb'/([A-Za-z0-9_.\-]+)\s+(\d+)\s+\d+\s+R', fm.group(1)):
        fobj=objmap.get(int(onum))
        if fobj is None: continue
        is_type0 = b'/Type0' in fobj
        cbytes = 2 if is_type0 else 1
        tu=None
        turef=ref(fobj,'/ToUnicode')
        if turef is not None:
            tub=objmap.get(turef)
            if tub is not None:
                dec=inflate(get_stream_bytes(tub)) or b''
                tu=parse_tounicode(dec)
                cb=codespace_bytes(dec)
                if cb: cbytes=cb
        fonts[name.decode('latin-1')]=(tu, cbytes)
    return fonts

# ---------------- content stream text extraction ----------------
def unescape_bytes(b):
    out=bytearray(); i=0
    while i<len(b):
        c=b[i]
        if c==0x5c:
            i+=1
            if i>=len(b): break
            n=b[i]
            mp={0x6e:0x0a,0x72:0x0d,0x74:0x09,0x62:0x08,0x66:0x0c,0x28:0x28,0x29:0x29,0x5c:0x5c}
            if n in mp: out.append(mp[n])
            elif 0x30<=n<=0x37:
                o=chr(n)
                for _ in range(2):
                    if i+1<len(b) and 0x30<=b[i+1]<=0x37: i+=1; o+=chr(b[i])
                    else: break
                out.append(int(o,8)&0xff)
            else: out.append(n)
        else: out.append(c)
        i+=1
    return bytes(out)

def decode_string(raw_bytes, font):
    """raw_bytes: the decoded bytes of a string operand. font: (tu, cbytes)."""
    tu, cbytes = font if font else (None,1)
    s=[]
    if cbytes==2:
        for i in range(0,len(raw_bytes)-1,2):
            code=(raw_bytes[i]<<8)|raw_bytes[i+1]
            if tu and code in tu: s.append(tu[code])
            else: s.append('')
    else:
        for by in raw_bytes:
            if tu and by in tu: s.append(tu[by])
            elif 32<=by<127: s.append(chr(by))
            else: s.append('')
    return ''.join(s)

STR_OR_HEX = re.compile(rb'\((?:\\.|[^()\\])*\)|<[0-9A-Fa-f\s]*>', re.DOTALL)
CTOK = re.compile(rb"(?P<s>\((?:\\.|[^()\\])*\))|(?P<h><[0-9A-Fa-f\s]*>)|(?P<a>\[(?:\\.|[^\[\]\\]|\\.)*\])|(?P<n>-?\d+\.?\d*)|(?P<op>Tj|TJ|Td|TD|T\*|Tf|'|\")|(?P<name>/[A-Za-z0-9_.+\-]+)", re.DOTALL)

def rawbytes_of(tok):
    if tok.startswith(b'('):
        return unescape_bytes(tok[1:-1])
    else:  # hex
        h=re.sub(rb'\s','',tok[1:-1])
        if len(h)%2: h+=b'0'
        try: return bytes.fromhex(h.decode())
        except Exception: return b''

def extract_page_text(content, fonts):
    parts=[]; stack=[]; cur=None
    for m in CTOK.finditer(content):
        k=m.lastgroup; v=m.group()
        if k=='op':
            op=v.decode()
            if op=='Tf':
                # operand before Tf: /Name size  -> name is 2 tokens back
                names=[t for t in stack if t[0]=='name']
                if names: cur=fonts.get(names[-1][1][1:].decode('latin-1'))
            elif op=='Tj' and stack and stack[-1][0] in ('s','h'):
                parts.append(decode_string(rawbytes_of(stack[-1][1]), cur))
            elif op in ("'",'"'):
                parts.append('\n')
                for t in stack:
                    if t[0] in ('s','h'): parts.append(decode_string(rawbytes_of(t[1]), cur))
            elif op=='TJ' and stack and stack[-1][0]=='a':
                buf=[]
                for em in re.finditer(rb'\((?:\\.|[^()\\])*\)|<[0-9A-Fa-f\s]*>|-?\d+\.?\d*', stack[-1][1]):
                    ev=em.group()
                    if ev.startswith(b'(') or ev.startswith(b'<'):
                        buf.append(decode_string(rawbytes_of(ev), cur))
                    else:
                        try:
                            if float(ev)<=-140: buf.append(' ')
                        except: pass
                parts.append(''.join(buf))
            elif op in ('Td','TD'):
                nums=[t for t in stack if t[0]=='n']
                if len(nums)>=2:
                    try:
                        ty=float(nums[-1][1]); parts.append('\n' if abs(ty)>0.1 else ' ')
                    except: parts.append(' ')
            elif op=='T*': parts.append('\n')
            stack=[]
        elif k in ('s','h','a','n','name'):
            stack.append((k,v))
    return ''.join(parts)

def normalize(t):
    try: t=t.encode('latin-1','ignore').decode('utf-8','ignore')
    except Exception: pass
    t=(t.replace('–','-').replace('—','-').replace('‘',"'").replace('’',"'")
        .replace('“','"').replace('”','"').replace('ﬁ','fi').replace('ﬂ','fl'))
    t=re.sub(r'[ \t]+',' ',t); t=re.sub(r' *\n *','\n',t); t=re.sub(r'\n{3,}','\n\n',t)
    return t.strip()

def page_text(objmap, pagenum):
    b=objmap.get(pagenum)
    if b is None: return ''
    fonts=get_page_fonts(objmap, b)
    cm=re.search(rb'/Contents\s*\[(.*?)\]', b, re.DOTALL)
    if cm: conts=[int(x) for x in re.findall(rb'(\d+)\s+\d+\s+R', cm.group(1))]
    else:
        r=ref(b,'/Contents'); conts=[r] if r is not None else []
    chunks=[]
    for cn in conts:
        cb=objmap.get(cn)
        if cb is None: continue
        dec=inflate(get_stream_bytes(cb))
        if dec: chunks.append(dec)
    return normalize(extract_page_text(b'\n'.join(chunks), fonts))

def main():
    fn=sys.argv[1]; outfile=sys.argv[2]
    start=int(sys.argv[3]) if len(sys.argv)>3 else 0
    end=int(sys.argv[4]) if len(sys.argv)>4 else 10**9
    data=open(fn,'rb').read()
    objmap=build_objmap(data)
    order=ordered_pages(objmap)
    out=[]
    for idx,pnum in enumerate(order):
        if idx<start: continue
        if idx>=end: break
        out.append(f"\n\n===== PAGE {idx} (obj {pnum}) =====\n{page_text(objmap,pnum)}")
    open(outfile,'w').write(''.join(out))
    sys.stderr.write(f"[objs={len(objmap)} pages={len(order)} wrote={min(end,len(order))-start} -> {outfile}]\n")

if __name__=='__main__':
    main()
