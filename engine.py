import struct,math

# --- single-line Zero Circle pulse ---
zc_pulse=lambda n=256,K=4096,E=64,fb=0.3:[((lambda e,v,f:((v:=((abs(e:=((math.exp(-0.5*((t-n/2)/(n/8))**2))+fb*(f if t else 0))))**1)*(1 if e>=0 else-1)),(f:=v),(v:=int((v+1)/2*(E-1))%E)))[2]for t in range(n)]

# --- single-line WAD accepter ---
wad_accept=lambda p:(lambda f,l:(f,[(o,s,n.rstrip(b"\0").decode())for o,s,n in l]))(*(lambda f:(f,[struct.unpack("<ii8s",f.read(16))for _ in range(struct.unpack("<4sii",f.read(12))[1])]))(open(p,"rb")))

# --- lump fetch ---
def lump(f,lumps,name):
    for p,s,n in lumps:
        if n==name:
            f.seek(p); return f.read(s)
    return None

# --- parsers ---
def parse_vertices(data):
    return [struct.unpack("<hh",data[i:i+4]) for i in range(0,len(data),4)]

def parse_linedefs(data):
    out=[]
    for i in range(0,len(data),14):
        v1,v2,_,_,_,_,_=struct.unpack("<hhhhhhh",data[i:i+14])
        out.append((v1,v2))
    return out

# --- vector renderer ---
def render_vec(verts,lines):
    for v1,v2 in lines:
        x1,y1=verts[v1]; x2,y2=verts[v2]
        print(f"LINE {x1},{y1}->{x2},{y2}")

# --- engine loop ---
def run(path):
    wad,lumps=wad_accept(path)
    verts=parse_vertices(lump(wad,lumps,"VERTEXES"))
    lines=parse_linedefs(lump(wad,lumps,"LINEDEFS"))
    pulse=zc_pulse()

    for tick in range(64):
        print(f"\nTICK {tick}  PULSE={pulse[tick%len(pulse)]}")
        render_vec(verts,lines)
