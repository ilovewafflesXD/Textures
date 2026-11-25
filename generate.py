import json, os, sys, hashlib, zipfile, random
from PIL import Image
OUT = sys.argv[1]
PAL = {
 'o': (36, 22, 10, 255), 'g': (240, 176, 56, 255), 'h': (255, 224, 128, 255), 'd': (184, 116, 26, 255),
 'p': (126, 46, 190, 255), 'P': (190, 120, 255, 255), 'b': (122, 78, 38, 255), 'B': (84, 52, 24, 255), 'e': (96, 20, 140, 255),
}
VAN=os.environ.get('VANILLA_DIR','/tmp/van')
MAP={(35,16,18):(36,22,10),(22,8,20):(36,22,10),(47,33,34):(60,36,16),(50,39,39):(60,36,16),(79,60,62):(150,92,20),
 (96,52,50):(122,78,38),(115,69,67):(150,100,50),(74,41,64):(126,46,190),(59,57,59):(150,92,20),(67,64,67):(184,116,26),
 (81,68,78):(184,116,26),(93,86,93):(240,176,56),(112,103,112):(250,200,80),(134,123,134):(255,224,128),
 (30,34,41):(36,22,10),(46,51,59):(150,92,20),(66,71,82):(184,116,26),(85,92,105):(210,140,34),(102,108,122):(240,176,56),
 (124,132,145):(250,200,80),(153,161,174):(255,224,128),(35,66,105):(84,52,24),(80,99,144):(122,78,38),
 (122,130,196):(150,100,50),(181,165,202):(220,170,255),(191,206,231):(255,240,170)}
def vanilla(name):
    src=Image.open(os.path.join(VAN,name+'.png')).convert('RGBA')
    im=Image.new('RGBA',src.size,(0,0,0,0))
    for y in range(src.size[1]):
        for x in range(src.size[0]):
            r,g_,b,a=src.getpixel((x,y))
            if a==0: continue
            c=MAP.get((r,g_,b))
            if c is None:
                l=(r+g_+b)//3
                c=(36,22,10) if l<40 else (184,116,26) if l<90 else (240,176,56) if l<140 else (255,224,128)
            im.putpixel((x,y),c+(255,))
    return im
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
def paint(g,rows,ox=0,oy=0):
    for y,r in enumerate(rows):
        for x,c in enumerate(r):
            if c!='.': put(g,x+ox,y+oy,c)
def handle(g,x0,y0,x1,y1):
    n=max(abs(x1-x0),abs(y1-y0))
    for i in range(n+1):
        x=x0+(x1-x0)*i//n; y=y0+(y1-y0)*i//n
        put(g,x,y,'b' if i%2==0 else 'B')
def axe():
    g=blank()
    handle(g,1,14,10,5)
    paint(g,[
    ".......gggg.....",
    "....ggggggggp...",
    "..gggggggggggp..",
    ".gggPPggggbbgp..",
    ".ggPPggggbbbp...",
    "..gggggggbb.....",
    "...pgggpbb......",
    ])
    return finish(g)
def hammer():
    g=blank()
    handle(g,1,14,9,6)
    paint(g,[
    "....ggggggg.....",
    "..ggggPPPgggg...",
    ".gggp....gggggp.",
    ".ggp......bgggp.",
    ".gp.......bbgggp",
    ".p........bb.ggp",
    "..........b...pp",
    ])
    return finish(g)
def mace():
    g=blank()
    handle(g,1,14,8,7)
    paint(g,[
    ".......p........",
    "....p.gggg.p....",
    "....gggPPggg....",
    "...pgPPhhPPgp...",
    "..ggggPhhPgggg..",
    "...pgPPPPPPgp...",
    "....gggPPggg....",
    "....p.gggg.p....",
    ".......p........",
    ])
    return finish(g,False)
def shovel():
    g=blank()
    for i in range(9): put(g,2+i,14-i,'b' if i%2==0 else 'B')
    rect(g,10,1,13,5,'g'); rect(g,11,0,12,0,'g'); rect(g,11,6,12,6,'g')
    put(g,13,5,'p'); put(g,12,6,'p'); put(g,10,5,'p'); rect(g,11,2,12,3,'P'); put(g,11,2,'h')
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
def shield():
    g=blank()
    rect(g,3,1,12,1,'p')
    rect(g,3,2,12,8,'g'); rect(g,3,2,3,8,'p'); rect(g,12,2,12,8,'p')
    rect(g,4,9,11,9,'g'); rect(g,5,10,10,10,'g'); rect(g,6,11,9,11,'g'); rect(g,7,12,8,12,'g')
    put(g,4,9,'p'); put(g,11,9,'p'); put(g,5,10,'p'); put(g,10,10,'p'); put(g,6,11,'p'); put(g,9,11,'p'); rect(g,7,13,8,13,'p')
    rect(g,7,3,8,10,'P'); rect(g,4,5,11,6,'P'); put(g,7,5,'h')
    return finish(g)
def _v(n):
    return lambda: n
ITEMS={'legend_elytra':(_v('elytra'),'generated'),'legend_shield':(shield,'generated'),'legend_spear':(_v('netherite_spear'),'handheld'),'legend_mace':(_v('mace'),'handheld'),'legend_shovel':(_v('netherite_shovel'),'handheld'),'legend_axe':(_v('netherite_axe'),'handheld'),'legend_hammer':(_v('netherite_pickaxe'),'handheld'),
       'legend_helmet':(helmet,'generated'),'legend_chestplate':(chest,'generated'),'legend_leggings':(legs,'generated'),'legend_boots':(boots,'generated')}
def worn(leg):
    im=Image.new('RGBA',(64,32),(0,0,0,0))
    def plate(x0,y0,x1,y1,trim=True):
        for y in range(y0,y1+1):
            for x in range(x0,x1+1):
                c=PAL['g']
                if x%4==0 or y%4==0: c=PAL['d']
                elif (x%4==1 and y%4==1): c=PAL['h']
                if trim and y==y1: c=PAL['p'] if x%4 else PAL['e']
                im.putpixel((x,y),c)
    if not leg:
        plate(8,0,15,7,False)
        for r in ((0,8,7,11),(8,8,15,9),(16,8,23,11),(24,8,31,12)): plate(*r)
        plate(20,16,27,19,False)
        for r in ((20,20,27,28),(32,20,39,29),(16,20,19,24),(28,20,31,24)): plate(*r)
        plate(44,16,47,19,False)
        for r in ((40,20,43,24),(44,20,47,24),(48,20,51,24),(52,20,55,24)): plate(*r)
        plate(8,16,11,19,False)
        for r in ((0,28,3,31),(4,28,7,31),(8,28,11,31),(12,28,15,31)): plate(*r)
        for y in range(22,25):
            for x in range(23,25): im.putpixel((x,y),PAL['P'])
        for x in range(8,16): im.putpixel((x,10),PAL['o'])
    else:
        plate(28,16,35,19,False)
        for r in ((16,29,19,31),(20,29,27,31),(28,29,31,31),(32,29,39,31)): plate(*r)
        plate(4,16,7,19,False)
        for r in ((0,20,3,25),(4,20,7,25),(8,20,11,25),(12,20,15,25)): plate(*r)
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
    im=vanilla(fn()) if isinstance(fn(),str) else img(fn())
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
w(os.path.join(B,'manifest.json'),{"format_version":2,"header":{"name":"WaffleMC Items","description":"WaffleMC custom item textures","uuid":"7f1a2c3e-5b6d-4e8f-9a0b-1c2d3e4f5a6b","version":[1,0,10],"min_engine_version":[1,21,0]},
 "modules":[{"type":"resources","uuid":"8e2b3d4f-6c7e-4f90-8b1c-2d3e4f5a6b7c","version":[1,0,10],"description":"textures"}]})
w(os.path.join(B,'textures','item_texture.json'),{"resource_pack_name":"wafflemc","texture_name":"atlas.items","texture_data":bt})
Image.new('RGBA',(64,64),PAL['g']).save(os.path.join(B,'pack_icon.png'))
sp=os.path.join(A,'textures','item','legend_spear_in_hand.png'); vanilla('netherite_spear_in_hand').save(sp)
os.makedirs(os.path.join(B,'textures','items'),exist_ok=True)
w(os.path.join(A,'models','item','legend_spear_in_hand.json'),{"parent":"minecraft:item/spear_in_hand","textures":{"layer0":"wafflecore:item/legend_spear_in_hand"}})
w(os.path.join(A,'models','item','legend_spear.json'),{"parent":"minecraft:item/generated","textures":{"layer0":"wafflecore:item/legend_spear"}})
w(os.path.join(A,'items','legend_spear.json'),{"model":{"type":"minecraft:select","property":"minecraft:display_context","cases":[{"when":["gui","ground","fixed","on_shelf"],"model":{"type":"minecraft:model","model":"wafflecore:item/legend_spear"}}],"fallback":{"type":"minecraft:model","model":"wafflecore:item/legend_spear_in_hand"}},"swap_animation_scale":1.95})
w(os.path.join(A,'items','legend_shield.json'),{"model":{"type":"minecraft:select","property":"minecraft:display_context","cases":[{"when":["gui","ground","fixed","on_shelf"],"model":{"type":"minecraft:model","model":"wafflecore:item/legend_shield"}}],"fallback":{"type":"minecraft:condition","property":"minecraft:using_item","on_false":{"type":"minecraft:special","base":"minecraft:item/shield","model":{"type":"minecraft:shield"}},"on_true":{"type":"minecraft:special","base":"minecraft:item/shield_blocking","model":{"type":"minecraft:shield"}}}}})
w(os.path.join(A,'equipment','waffle_elytra.json'),{"layers":{"wings":[{"texture":"wafflecore:waffle_elytra","use_player_texture":True}]}})
wp=os.path.join(A,'textures','entity','equipment','wings','waffle_elytra.png'); os.makedirs(os.path.dirname(wp),exist_ok=True); vanilla('elytra_wings').save(wp)
maps={}
for name,base in (('legend_axe','minecraft:netherite_axe'),('legend_hammer','minecraft:netherite_pickaxe'),('legend_mace','minecraft:mace'),('legend_spear','minecraft:netherite_spear'),('legend_elytra','minecraft:elytra'),('legend_shield','minecraft:shield'),('legend_shovel','minecraft:netherite_shovel')):
    maps.setdefault(base,[]).append({"type":"definition","model":"wafflecore:"+name,"bedrock_identifier":"wafflecore:"+name,
      "bedrock_options":{"icon":"wafflecore:"+name,"allow_offhand":True,"display_handheld":True,"creative_category":"items"}})
w(os.path.join(OUT,'waffle_items.json'),{"format_version":2,"items":maps})
for e in maps['minecraft:elytra']:
    if e['bedrock_identifier']=='wafflecore:legend_elytra':
        e['bedrock_options']={"icon":"wafflecore:legend_elytra","allow_offhand":False,"protection_value":0,"creative_category":"equipment"}
        e['components']={"minecraft:equippable":{"slot":"chest"},"minecraft:max_stack_size":1}
w(os.path.join(B,'attachables','legend_elytra.attachable.json'),{"format_version":"1.10.0","minecraft:attachable":{"description":{
  "identifier":"wafflecore:legend_elytra","materials":{"default":"elytra","enchanted":"elytra_glint"},
  "textures":{"default":"textures/models/armor/waffle_elytra","enchanted":"textures/misc/enchanted_actor_glint"},
  "geometry":{"default":"geometry.elytra"},
  "animations":{"default_controller":"controller.animation.elytra.default","default":"animation.elytra.default","gliding":"animation.elytra.gliding","sneaking":"animation.elytra.sneaking","sleeping":"animation.elytra.sleeping","swimming":"animation.elytra.swimming"},
  "scripts":{"parent_setup":"variable.chest_layer_visible = 0.0;","animate":["default_controller"]},
  "render_controllers":["controller.render.armor"]}}})
_ep=os.path.join(B,'textures','models','armor','waffle_elytra.png'); os.makedirs(os.path.dirname(_ep),exist_ok=True); vanilla('elytra_wings').save(_ep)
vanilla('elytra_wings').save(os.path.join(B,'textures','models','armor','elytra.png'))
os.makedirs(os.path.join(B,'textures','entity'),exist_ok=True); import shutil as _sh; _sh.copy(os.path.join(os.path.dirname(os.path.abspath(__file__)),'shield_gold.png'),os.path.join(B,'textures','entity','shield.png'))
ARMOR={'helmet':('head','helmet_layer_visible','1',3),'chestplate':('chest','chest_layer_visible','1',8),'leggings':('legs','leg_layer_visible','2',6),'boots':('feet','boot_layer_visible','1',3)}
for part,(slot,var,layer,prot) in ARMOR.items():
    ident='wafflecore:legend_'+part
    w(os.path.join(B,'attachables','legend_'+part+'.attachable.json'),{"format_version":"1.8.0","minecraft:attachable":{"description":{
      "identifier":ident,"materials":{"default":"armor","enchanted":"armor_enchanted"},
      "textures":{"default":"textures/models/armor/waffle_"+layer,"enchanted":"textures/misc/enchanted_actor_glint","baby":"textures/models/armor/waffle_"+layer},
      "geometry":{"default":"geometry.humanoid.armor."+part,"baby":"geometry.humanoid.baby.armor."+part},
      "scripts":{"parent_setup":"v."+var+" = false;","pre_animation":["v.use_baby_geo = q.is_baby && c.owning_entity->v.use_dedicated_baby_armor;"]},
      "render_controllers":["controller.render.armor.v2"]}}})
    maps.setdefault('minecraft:netherite_'+part,[]).append({"type":"definition","model":ident,"bedrock_identifier":ident,
      "bedrock_options":{"icon":ident,"allow_offhand":False,"protection_value":prot,"creative_category":"equipment"},
      "components":{"minecraft:equippable":{"slot":slot},"minecraft:max_stack_size":1}})
for layer,leg in (('1',False),('2',True)):
    p=os.path.join(B,'textures','models','armor','waffle_'+layer+'.png'); os.makedirs(os.path.dirname(p),exist_ok=True); worn(leg).save(p)
maps.pop("minecraft:shield",None)
w(os.path.join(OUT,'waffle_items.json'),{"format_version":2,"items":maps})
def add_outlines(J):
    import shutil
    O=os.environ.get('OUTLINES_DIR','/tmp/eo')
    if not os.path.isdir(O): return
    def cp(src,dst):
        for root,_,files in os.walk(src):
            for f in files:
                if f=='.DS_Store': continue
                full=os.path.join(root,f); rel=os.path.relpath(full,src); out=os.path.join(dst,rel)
                os.makedirs(os.path.dirname(out),exist_ok=True); shutil.copyfile(full,out)
    cp(os.path.join(O,'assets'),os.path.join(J,'assets'))
    src=json.load(open(os.path.join(O,'pack.mcmeta')))
    keep=('1-21-1','1-21-5','1-21-6','1-21-9','26-1','26-3')
    ents=[e for e in src['overlays']['entries'] if e['directory'] in keep]
    for e in ents: cp(os.path.join(O,e['directory']),os.path.join(J,e['directory']))
    m=json.load(open(os.path.join(J,'pack.mcmeta')))
    m['overlays']={'entries':ents}
    open(os.path.join(J,'pack.mcmeta'),'w').write(json.dumps(m,indent=2)+"\n")
    shutil.copyfile(os.path.join(O,'credits.txt'),os.path.join(J,'credits.txt'))
def zipdir(src,dst):
    with zipfile.ZipFile(dst,'w',zipfile.ZIP_DEFLATED) as z:
        for root,_,files in os.walk(src):
            for f in sorted(files):
                full=os.path.join(root,f); z.write(full,os.path.relpath(full,src).replace(os.sep,'/'))
add_outlines(J); zipdir(J,os.path.join(OUT,'WaffleMC-Pack.zip')); zipdir(B,os.path.join(OUT,'WaffleMC-Bedrock.mcpack'))
for f in ('WaffleMC-Pack.zip','WaffleMC-Bedrock.mcpack'):
    d=open(os.path.join(OUT,f),'rb').read(); print(f,len(d),hashlib.sha1(d).hexdigest())
