import json, os, sys, hashlib, zipfile, random
from PIL import Image
OUT = sys.argv[1]
PAL = {
 'o': (36, 22, 10, 255), 'g': (240, 176, 56, 255), 'h': (255, 224, 128, 255), 'd': (184, 116, 26, 255),
 'p': (126, 46, 190, 255), 'P': (190, 120, 255, 255), 'b': (122, 78, 38, 255), 'B': (84, 52, 24, 255), 'e': (96, 20, 140, 255),
}
def blank(): return [['.']*16 for _ in range(16)]
def put(g,x,y,c):
    if 0<=x<16 and 0<=y<16: g[y][x]=c
def rect(g,x0,y0,x1,y1,c):
    for y in range(y0,y1+1):
        for x in range(x0,x1+1): put(g,x,y,c)
def finish(g, grid=True):
    if grid:
        for y in range(16):
            for x in range(16):
                if g[y][x]=='g' and ((x+y)%4==0 and (x-y)%4==0): g[y][x]='d'
    for y in range(16):
        for x in range(16):
            if g[y][x]=='g':
                up=g[y-1][x] if y>0 else '.'; lf=g[y][x-1] if x>0 else '.'
                if up in '.o' or lf in '.o': g[y][x]='h'
    filled=[[c!='.' for c in r] for r in g]
    for y in range(16):
        for x in range(16):
            if g[y][x]=='.':
                for dx,dy in ((1,0),(-1,0),(0,1),(0,-1)):
                    nx,ny=x+dx,y+dy
                    if 0<=nx<16 and 0<=ny<16 and filled[ny][nx]: g[y][x]='o'; break
    return g
def img(g):
    im=Image.new('RGBA',(16,16),(0,0,0,0))
    for y in range(16):
        for x in range(16):
            if g[y][x]!='.': im.putpixel((x,y),PAL[g[y][x]])
    return im
def sword():
    g=blank()
    for t in range(0,8):
        x,y=13-t,2+t
        put(g,x,y,'g'); put(g,x+1,y,'h'); put(g,x,y+1,'d')
    put(g,14,1,'h'); put(g,13,1,'h'); put(g,14,2,'h')
    for k in range(-2,3): put(g,5+k,10+k,'p')
    put(g,5,10,'P')
    for i in range(3): put(g,4-i,11+i,'b' if i%2==0 else 'B')
    put(g,1,14,'P')
    return finish(g,False)
def axe():
    g=blank()
    for i in range(9): put(g,2+i,14-i,'b' if i%2==0 else 'B')
    rows={2:(10,13),3:(9,14),4:(9,14),5:(9,13),6:(10,12),7:(10,11)}
    for y,(a,b) in rows.items():
        for x in range(a,b+1): put(g,x,y,'g')
        put(g,b,y,'p')
    put(g,11,4,'P')
    return finish(g)
def hammer():
    g=blank()
    for i in range(8): put(g,2+i,14-i,'b' if i%2==0 else 'B')
    rect(g,5,1,14,6,'g')
    for x in range(5,15): put(g,x,6,'d')
    rect(g,5,1,5,6,'p'); rect(g,14,1,14,6,'p')
    rect(g,9,3,10,4,'P'); put(g,9,3,'h')
    return finish(g)
def helmet():
    g=blank()
    rect(g,3,3,12,10,'g'); put(g,3,3,'.'); put(g,12,3,'.')
    rect(g,3,10,4,12,'g'); rect(g,11,10,12,12,'g')
    rect(g,5,7,10,12,'.')
    rect(g,7,1,8,3,'p'); put(g,7,1,'P')
    rect(g,3,6,12,6,'p')
    return finish(g)
def chest():
    g=blank()
    rect(g,4,3,11,14,'g'); rect(g,1,3,4,7,'g'); rect(g,11,3,14,7,'g')
    rect(g,6,3,9,4,'.')
    rect(g,1,7,4,7,'p'); rect(g,11,7,14,7,'p'); rect(g,4,14,11,14,'p')
    rect(g,7,8,8,10,'P'); put(g,7,8,'h')
    return finish(g)
def legs():
    g=blank()
    rect(g,4,2,11,5,'g'); rect(g,4,6,6,14,'g'); rect(g,9,6,11,14,'g')
    rect(g,4,5,11,5,'p'); rect(g,7,3,8,4,'P'); rect(g,4,14,6,14,'p'); rect(g,9,14,11,14,'p')
    return finish(g)
def boots():
    g=blank()
    rect(g,3,4,6,10,'g'); rect(g,2,10,7,12,'g'); rect(g,9,4,12,10,'g'); rect(g,8,10,13,12,'g')
    rect(g,3,5,6,5,'p'); rect(g,9,5,12,5,'p'); rect(g,2,12,7,12,'p'); rect(g,8,12,13,12,'p')
    return finish(g)
ITEMS={'legend_sword':(sword,'handheld'),'legend_axe':(axe,'handheld'),'legend_hammer':(hammer,'handheld'),
       'legend_helmet':(helmet,'generated'),'legend_chestplate':(chest,'generated'),'legend_leggings':(legs,'generated'),'legend_boots':(boots,'generated')}
def worn(leg):
    im=Image.new('RGBA',(64,32),(0,0,0,0))
    random.seed(7 if not leg else 9)
    for y in range(32):
        for x in range(64):
            c=PAL['g']
            if x%4==0 or y%4==0: c=PAL['d']
            elif (x%4==1 and y%4==1): c=PAL['h']
            if y%16 in (14,15) : c=PAL['p'] if (x%4)!=0 else PAL['e']
            im.putpixel((x,y),c)
    if not leg:
        for y in range(21,25):
            for x in range(22,26): im.putpixel((x,y),PAL['P'] if (x in(23,24) and y in(22,23)) else PAL['p'])
        for x in range(8,16): im.putpixel((x,12),PAL['o'])
    return im
def w(path,data):
    os.makedirs(os.path.dirname(path),exist_ok=True)
    open(path,'w').write(json.dumps(data,indent=2)+"\n")
J=os.path.join(OUT,'java'); B=os.path.join(OUT,'bedrock'); A=os.path.join(J,'assets','wafflecore')
w(os.path.join(J,'pack.mcmeta'),{"pack":{"description":"WaffleMC custom items","min_format":65,"max_format":999}})
Image.new('RGBA',(64,64),PAL['g']).save(os.path.join(J,'pack.png'))
prev=Image.new('RGBA',(16*len(ITEMS)*4,64),(60,60,70,255))
bt={}
for i,(name,(fn,parent)) in enumerate(ITEMS.items()):
    im=img(fn())
    p=os.path.join(A,'textures','item',name+'.png'); os.makedirs(os.path.dirname(p),exist_ok=True); im.save(p)
    bp=os.path.join(B,'textures','items',name+'.png'); os.makedirs(os.path.dirname(bp),exist_ok=True); im.save(bp)
    w(os.path.join(A,'models','item',name+'.json'),{"parent":"minecraft:item/"+parent,"textures":{"layer0":"wafflecore:item/"+name}})
    w(os.path.join(A,'items',name+'.json'),{"model":{"type":"minecraft:model","model":"wafflecore:item/"+name}})
    bt['wafflecore:'+name]={"textures":["textures/items/"+name]}
    prev.paste(im.resize((64,64),Image.NEAREST),(i*64*1,0))
prev.save(os.path.join(OUT,'preview.png'))
w(os.path.join(A,'equipment','waffle.json'),{"layers":{"humanoid":[{"texture":"wafflecore:waffle"}],"humanoid_leggings":[{"texture":"wafflecore:waffle"}]}})
for d,leg in (('humanoid',False),('humanoid_leggings',True)):
    p=os.path.join(A,'textures','entity','equipment',d,'waffle.png'); os.makedirs(os.path.dirname(p),exist_ok=True); worn(leg).save(p)
w(os.path.join(B,'manifest.json'),{"format_version":2,"header":{"name":"WaffleMC Items","description":"WaffleMC custom item textures","uuid":"7f1a2c3e-5b6d-4e8f-9a0b-1c2d3e4f5a6b","version":[1,0,0],"min_engine_version":[1,21,0]},
 "modules":[{"type":"resources","uuid":"8e2b3d4f-6c7e-4f90-8b1c-2d3e4f5a6b7c","version":[1,0,0],"description":"textures"}]})
w(os.path.join(B,'textures','item_texture.json'),{"resource_pack_name":"wafflemc","texture_name":"atlas.items","texture_data":bt})
Image.new('RGBA',(64,64),PAL['g']).save(os.path.join(B,'pack_icon.png'))
maps={}
for name,base in (('legend_sword','minecraft:netherite_sword'),('legend_axe','minecraft:netherite_axe'),('legend_hammer','minecraft:netherite_pickaxe')):
    maps.setdefault(base,[]).append({"type":"definition","model":"wafflecore:"+name,"bedrock_identifier":"wafflecore:"+name,
      "bedrock_options":{"icon":"wafflecore:"+name,"allow_offhand":True,"display_handheld":True,"creative_category":"items"}})
w(os.path.join(OUT,'waffle_items.json'),{"format_version":2,"items":maps})
def zipdir(src,dst):
    with zipfile.ZipFile(dst,'w',zipfile.ZIP_DEFLATED) as z:
        for root,_,files in os.walk(src):
            for f in sorted(files):
                full=os.path.join(root,f); z.write(full,os.path.relpath(full,src).replace(os.sep,'/'))
zipdir(J,os.path.join(OUT,'WaffleMC-Pack.zip')); zipdir(B,os.path.join(OUT,'WaffleMC-Bedrock.mcpack'))
for f in ('WaffleMC-Pack.zip','WaffleMC-Bedrock.mcpack'):
    d=open(os.path.join(OUT,f),'rb').read(); print(f,len(d),hashlib.sha1(d).hexdigest())
