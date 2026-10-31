import sys,math
sys.path[:0]=['tools','art/src']
import map_render as MR, review_ruins as RR, colors as C, review_yd as Y, ydtube as T
from review_redrock import bare
from PIL import Image
BOX=Y.BOX
c=MR.load('YdFreehold'); PIPE=Y.PIPE
pipes={k for k,v in c.items() if PIPE in v}
GLOW=(0xa8,0xd4,0x50)
RADIUS,STRENGTH=11.0,0.28
def field(cx,cy):
    d=9e9
    for a,b in pipes:
        dd=math.hypot(cx-(a+.5),(cy-(b+.5))*1.5)
        if dd<d: d=dd
    return STRENGTH*max(0,1-d/RADIUS)**1.5
corner={(x,y):round(field(x,y)/STRENGTH*7)/7*STRENGTH for x in range(81) for y in range(26)}
det=C.hex_rgb('c9a84a')
def run(x,y,dx,dy):
    n=1
    for sign in (1,-1):
        a,b=x+dx*sign,y+dy*sign
        while (a,b) in pipes: n+=1; a+=dx*sign; b+=dy*sign
    return n
cur=[None]
def sw(name,x,y,cells):
    if name==PIPE: cur[0]=(x,y); return None
    cur[0]=None; return RR.recording(name,x,y,cells)
def mkpo(fg):
    def po(name,t):
        if name==PIPE and cur[0]:
            x,y=cur[0]; st=lambda a,b:1 if (x+a,y+b) in pipes else 0
            m=T.straight(st(0,-1),st(1,0),st(0,1),st(-1,0),run(x,y,1,0),run(x,y,0,1))
            h=((x*73856093)^(y*19349663))&0x7fffffff
            rows=T.tube(*m,h%4==0,m[0]*8+m[1]*4+m[2]*2+m[3])
            pal={'1':C.ramp(fg,0),'2':C.ramp(fg,1),'3':C.ramp(fg,2),'4':C.ramp(det,0),'5':C.ramp(det,1),'w':(240,250,200)}
            im=Image.new('RGBA',(16,24),(0,0,0,0))
            for j,r in enumerate(rows):
                for i,ch in enumerate(r):
                    if ch!='.': im.putpixel((i,j),tuple(pal[ch])+(255,))
            return im.resize(t.size,Image.NEAREST)
        return Y.post(name,t)
    return po
base=None
frames=[]
G=lambda x,y:(0x20,0x3a,0x3b)
for lvl in (0,1,2,3,2,1):
    k=lvl/3
    fg=tuple(int(a+(b-a)*k) for a,b in zip((0x79,0xa0,0x40),(0xb4,0xdc,0x5e)))
    a=MR.render('YdFreehold','new',BOX,ground=G,bare=bare('reef'),swap=sw,post=mkpo(fg)).convert('RGB')
    Z=a.width//((BOX[2]-BOX[0])*16)
    if base is None:
        W,H=a.size; m=Image.new('L',(W,H)); p=m.load()
        for Y_ in range(H):
            for X in range(W):
                cx=BOX[0]+X/(16*Z); cy=BOX[1]+Y_/(24*Z); ix,iy=int(cx),int(cy); fx,fy=cx-ix,cy-iy
                v=corner[ix,iy]*(1-fx)*(1-fy)+corner[ix+1,iy]*fx*(1-fy)+corner[ix,iy+1]*(1-fx)*fy+corner[ix+1,iy+1]*fx*fy
                p[X,Y_]=int(v*255)
        base=m
    frames.append(Image.composite(Image.new('RGB',a.size,GLOW),a,base))
frames[3].save(sys.argv[1])
small=[f.resize((f.width*2//3,f.height*2//3),Image.NEAREST).convert('P',palette=Image.ADAPTIVE) for f in frames]
small[0].save(sys.argv[2],save_all=True,append_images=small[1:],duration=420,loop=0)
