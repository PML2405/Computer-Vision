#!/usr/bin/env python3
"""Map extracted image XObjects to the slide pages that USE them (via Do ops).
Uses pdf_text2's object model. Usage: map_figures.py SLIDE.pdf"""
import sys, re, os, importlib.util
# self-locating: import pdf_text2.py from the same tools/ directory
_here=os.path.dirname(os.path.abspath(__file__))
spec=importlib.util.spec_from_file_location("pt", os.path.join(_here,"pdf_text2.py"))
pt=importlib.util.module_from_spec(spec); spec.loader.exec_module(pt)

def xobjects_of_page(objmap, pagebody):
    # find /Resources -> /XObject << /Im0 12 0 R ... >>
    res_ref=pt.ref(pagebody,'/Resources')
    resbody = objmap.get(res_ref) if res_ref else None
    if resbody is None:
        mm=re.search(rb'/Resources\s*<<(.*)', pagebody, re.DOTALL)
        resbody=mm.group(0) if mm else pagebody
    xm=re.search(rb'/XObject\s*<<(.*?)>>', resbody, re.DOTALL)
    xref=None
    if not xm:
        xoref=pt.ref(resbody,'/XObject')
        xb=objmap.get(xoref) if xoref else None
        if xb is None: return {}
        xm=re.search(rb'<<(.*?)>>', xb, re.DOTALL)
        if not xm: return {}
    mapping={}
    for name,onum in re.findall(rb'/([A-Za-z0-9_.\-]+)\s+(\d+)\s+\d+\s+R', xm.group(1)):
        mapping[name.decode()]=int(onum)
    return mapping

def main():
    fn=sys.argv[1]
    data=open(fn,'rb').read()
    objmap=pt.build_objmap(data)
    order=pt.ordered_pages(objmap)
    # which obj numbers are images (Subtype/Image)
    img_objs=set()
    for n,b in objmap.items():
        head=b[:600]
        if b'/Image' in head and (b'/Width' in head):
            img_objs.add(n)
    for idx,pnum in enumerate(order):
        body=objmap.get(pnum,b'')
        xobjs=xobjects_of_page(objmap, body)
        # which referenced xobjects are images (directly or via nested form xobjects)
        imgs=[]
        for name,onum in xobjs.items():
            if onum in img_objs:
                ob=objmap.get(onum,b'')
                wm=re.search(rb'/Width\s+(\d+)',ob); hm=re.search(rb'/Height\s+(\d+)',ob)
                w=wm.group(1).decode() if wm else '?'; h=hm.group(1).decode() if hm else '?'
                imgs.append(f"obj{onum}({w}x{h})")
        if imgs:
            print(f"PAGE {idx:2d} (obj {pnum}): {', '.join(imgs)}")
        else:
            print(f"PAGE {idx:2d} (obj {pnum}): -")

if __name__=='__main__':
    main()
