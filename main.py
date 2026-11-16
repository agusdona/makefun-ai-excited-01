import math
import os
import random
import struct
import zlib

W = H = 1024
random.seed(20261115)
pix = bytearray(W * H * 3)

def blend(x, y, c):
    if 0 <= x < W and 0 <= y < H:
        i = (int(y) * W + int(x)) * 3
        pix[i:i+3] = bytes(c)

def line(x1, y1, x2, y2, c, width=1):
    dx, dy = x2-x1, y2-y1
    n = max(1, int(max(abs(dx), abs(dy))))
    r = max(0, width//2)
    for k in range(n+1):
        x, y = int(x1 + dx*k/n), int(y1 + dy*k/n)
        for oy in range(-r, r+1):
            for ox in range(-r, r+1):
                if ox*ox+oy*oy <= r*r+1: blend(x+ox, y+oy, c)

def polygon(points, c):
    miny=max(0,int(min(y for x,y in points))); maxy=min(H-1,int(max(y for x,y in points)))
    for y in range(miny,maxy+1):
        xs=[]
        for i,(x1,y1) in enumerate(points):
            x2,y2=points[(i+1)%len(points)]
            if (y1 <= y < y2) or (y2 <= y < y1): xs.append(x1+(y-y1)*(x2-x1)/(y2-y1))
        xs.sort()
        for a,b in zip(xs[::2],xs[1::2]):
            for x in range(max(0,int(a)),min(W,int(b)+1)): blend(x,y,c)

def ellipse(cx,cy,rx,ry,c):
    ya=max(0,int(cy-ry)); yb=min(H,int(cy+ry+1))
    for y in range(ya,yb):
        q=1-((y-cy)/ry)**2
        if q>=0:
            dx=rx*math.sqrt(q)
            for x in range(max(0,int(cx-dx)),min(W,int(cx+dx+1))): blend(x,y,c)

# Sky gradient, slightly brighter at the folded horizon.
for y in range(H):
    t=y/(H-1)
    if t < .72:
        u=t/.72; a=(13,17,62); b=(105,31,112)
    else:
        u=(t-.72)/.28; a=(105,31,112); b=(230,91,112)
    row=tuple(int(a[k]*(1-u)+b[k]*u) for k in range(3))
    for x in range(W): blend(x,y,row)
# Fine stars and a full moon behind the fish.
for _ in range(180):
    x=random.randrange(W); y=random.randrange(720)
    col=(181,191,224) if random.random()<.7 else (255,211,123)
    blend(x,y,col)
ellipse(794,222,150,150,(247,218,148))
ellipse(794,222,136,136,(255,232,176))
# Folded sky planes, broad graphic diagonals.
polygon([(0,620),(392,452),(611,532),(312,720)],(45,39,103))
polygon([(0,620),(392,452),(322,476),(0,654)],(218,150,117))
line(0,620,392,452,(255,209,139),3)
polygon([(1024,396),(719,456),(858,572),(1024,523)],(79,43,120))
line(1024,396,719,456,(255,209,139),3)
polygon([(0,775),(328,678),(465,751),(155,854)],(193,95,126))
line(0,775,328,678,(255,211,139),3)
# Origami skyline built from folded paper facets.
for x,w,h in [(12,95,182),(110,112,252),(223,82,151),(307,120,286),(430,90,192),(526,120,330),(650,106,215),(761,98,292),(864,145,190)]:
    base=900; top=base-h
    lean= random.randint(-18,22)
    polygon([(x,base),(x+lean,top+25),(x+w//2,top),(x+w,top+22),(x+w,base)],(238,222,190))
    polygon([(x+lean,top+25),(x+w//2,top),(x+w//2+8,base),(x,base)],(255,244,215))
    polygon([(x+w//2,top),(x+w,top+22),(x+w,base),(x+w//2+8,base)],(201,190,177))
    line(x+lean,top+25,x+w//2,top,(255,205,117),2)
    line(x+w//2,top,x+w,top+22,(245,190,101),2)
    for wy in range(top+55,base-20,54):
        for wx in (x+22,x+58):
            if wx<x+w-8: polygon([(wx,wy),(wx+17,wy-2),(wx+17,wy+24),(wx,wy+26)],(255,198,76))
# Wind arcs behind the koi.
for offset in (0,1,2):
    pts=[]
    for i in range(100):
        t=i/99; pts.append((60+870*t, 700-350*math.sin(t*math.pi)+offset*13))
    for a,b in zip(pts,pts[1:]): line(*a,*b,(246,218,172) if offset==0 else (178,181,219),1)
# Koi leaps from lower-left to upper-right; tail and flowing fins first.
polygon([(167,728),(82,660),(34,605),(74,609),(27,554),(119,603),(224,651)],(221,105,42))
polygon([(136,685),(62,621),(111,631),(95,590),(170,649)],(255,186,71))
line(76,609,143,666,(255,224,153),3)
# sweeping lower fin
polygon([(353,699),(443,766),(533,824),(473,812),(529,865),(409,827),(329,756)],(216,105,49))
polygon([(359,718),(448,776),(497,817),(421,794)],(255,185,70))
# body center aligned diagonal
# layered shadow then white belly then golden body
ellipse(494,548,325,144,(102,48,61))
ellipse(493,533,326,139,(242,145,45))
ellipse(464,581,244,76,(255,237,209))
# head and snout
polygon([(690,464),(770,416),(865,410),(928,445),(902,486),(826,499),(744,515)],(246,155,49))
ellipse(864,449,61,42,(255,185,69))
# dorsal and pectoral fins
polygon([(360,433),(404,333),(444,415),(501,310),(521,431),(580,342),(575,454)],(224,114,48))
polygon([(595,560),(696,612),(751,683),(691,669),(650,635)],(227,119,53))
polygon([(613,564),(686,614),(719,653),(664,625)],(255,192,89))
line(603,565,685,617,(255,222,153),3)
line(685,617,724,664,(255,222,153),2)
# black sumi patches
for cx,cy,rx,ry in [(319,493,45,31),(420,461,36,28),(530,477,48,30),(591,513,31,23),(753,454,27,18)]:
    ellipse(cx,cy,rx,ry,(39,31,49))
# scales as crisp curved marks
for cx,cy in [(364,545),(423,523),(482,515),(543,525),(601,532)]:
    for j in range(3): line(cx+j*9,cy+j*5,cx+12+j*9,cy+8+j*5,(255,205,123),2)
# eye, gill and whiskers
ellipse(883,437,12,12,(32,29,43)); ellipse(886,434,4,4,(255,245,218))
line(809,429,792,477,(160,74,49),3)
line(907,468,967,495,(53,40,52),3); line(904,474,960,523,(53,40,52),2)
# golden splash droplets and small origami cranes
for x,y,r in [(189,580,7),(225,548,5),(271,518,4),(160,632,5),(298,468,4),(672,352,5),(710,326,4),(741,300,3)]: ellipse(x,y,r,r,(255,216,111))
for pts in [[(246,389),(276,359),(302,391),(276,382),(252,405)],[(170,442),(196,416),(222,443),(195,435),(177,458)],[(659,265),(682,242),(707,267),(681,258),(665,280)]]:
    polygon(pts,(247,241,221)); line(*pts[0],*pts[2],(255,216,135),1)
# Banner ribbon, with bold bitmap letters.
polygon([(24,42),(369,42),(396,81),(369,120),(24,120),(44,81)],(218,44,129))
polygon([(24,42),(48,58),(48,105),(24,120)],(151,31,106))
FONT={'H':['10001','10001','10001','11111','10001','10001','10001'],'E':['11111','10000','10000','11110','10000','10000','11111'],'Y':['10001','10001','01010','00100','00100','00100','00100'],'J':['00111','00010','00010','00010','10010','10010','01100'],'U':['10001','10001','10001','10001','10001','10001','01110'],'D':['11110','10001','10001','10001','10001','10001','11110'],'G':['01111','10000','10000','10111','10001','10001','01111'],'!':['00100','00100','00100','00100','00100','00000','00100'],' ':['000','000','000','000','000','000','000']}
def text(s,x,y,scale):
    for ch in s:
        glyph=FONT[ch]
        for yy,row in enumerate(glyph):
            for xx,on in enumerate(row):
                if on=='1':
                    # dark outline then ivory face
                    for oy in range(-1,2):
                        for ox in range(-1,2):
                            if ox or oy:
                                for py in range(scale):
                                    for px in range(scale): blend(x+xx*scale+px+ox*2,y+yy*scale+py+oy*2,(48,24,58))
                    for py in range(scale):
                        for px in range(scale): blend(x+xx*scale+px,y+yy*scale+py,(255,249,231))
        x+=(len(glyph[0])+1)*scale
text('HEY JUDGE!',56,60,7)
# PNG encoding: RGB rows, filter type 0, deterministic zlib stream.
raw=bytearray()
for y in range(H): raw.append(0); raw.extend(pix[y*W*3:(y+1)*W*3])
def chunk(tag,data): return struct.pack('>I',len(data))+tag+data+struct.pack('>I',zlib.crc32(tag+data)&0xffffffff)
png=b'\x89PNG\r\n\x1a\n'+chunk(b'IHDR',struct.pack('>IIBBBBB',W,H,8,2,0,0,0))+chunk(b'IDAT',zlib.compress(bytes(raw),9))+chunk(b'IEND',b'')
out=os.environ.get('MAKEFUN_OUTPUT_DIR','/output')
os.makedirs(out,exist_ok=True)
with open(os.path.join(out,'entry.png'),'wb') as f: f.write(png)
