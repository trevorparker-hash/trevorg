import os as _os
_ROOT = _os.path.abspath(_os.path.join(_os.path.dirname(__file__), '..', '..'))
import json, os, subprocess
R=_ROOT; W=os.path.dirname(os.path.abspath(__file__)); O=f'{W}/og'
F=f'file://{R}/assets/fonts'
FONTS=f"""
@font-face{{font-family:Unbounded;src:url({F}/unbounded-latin.woff2) format('woff2');font-weight:400 900}}
@font-face{{font-family:Inter;src:url({F}/inter-latin.woff2) format('woff2');font-weight:400 900}}
@font-face{{font-family:Saira;src:url({F}/saira-800italic-latin.woff2) format('woff2');font-weight:800;font-style:italic}}
@font-face{{font-family:Kanit;src:url({F}/kanit-700italic-latin.woff2) format('woff2');font-weight:700;font-style:italic}}
@font-face{{font-family:Archivo;src:url({F}/archivo-expanded-800italic-latin.woff2) format('woff2');font-weight:800;font-style:italic;font-stretch:125%}}
@font-face{{font-family:Cinzel;src:url({F}/cinzel-700-latin.woff2) format('woff2');font-weight:700}}
*{{box-sizing:border-box}} html,body{{margin:0;width:1200px;height:630px;background:#0B0C0E;color:#F3F2EE;font-family:Inter;overflow:hidden}}
.wm{{font-family:Unbounded;font-weight:800;letter-spacing:-.02em;line-height:1}} .wm b{{color:#C8F250;font-weight:800}}
"""
GAMES=[('engagement','Engagement',"font-family:Saira;font-style:italic;font-weight:800;text-transform:uppercase;font-size:104px;letter-spacing:.01em",'One capital ship. Fifteen minutes until relief.','#58A9D5'),
 ('fight','FIGHT',"font-family:Kanit;font-style:italic;font-weight:700;font-size:150px;letter-spacing:.01em;line-height:.9",'Queue your moves. Commit blind. Watch both plans collide.','#E51828'),
 ('street-takeover','Street Takeover',"font-family:Archivo;font-style:italic;font-weight:800;font-stretch:125%;text-transform:uppercase;font-size:80px;line-height:.95",'Police chases. Damage that stays.','#DD5A3B'),
 ('field-surgeon','Field Surgeon',"font-family:Cinzel;font-weight:700;font-size:92px;letter-spacing:.03em;line-height:1",'Surgery in a plague-ridden free city at war.','#ECB885')]
jobs=[]
def page(name, body, css=''):
    p=f'{O}/{name}.html'
    open(p,'w').write(f'<!doctype html><meta charset=utf-8><style>{FONTS}{css}</style>{body}')
    jobs.append({'html':p,'out':f'{O}/{name}.png','w':1200,'h':630})
for gid,name,tcss,line,acc in GAMES:
    art=f'file://{R}/assets/img/{gid}/card-1920.jpg'
    page(gid, f'''<div class=art></div><div class=shade></div>
<div class=txt><div class=t>{name}</div><p>{line}</p></div>
<div class=strip><span class=wm>Trevor<b>Games</b></span><span class=cta><i></i>Free demo on Steam</span></div>''',
f'''.art{{position:absolute;left:0;top:0;width:1200px;height:530px;background:url({art}) center/cover}}
.shade{{position:absolute;left:0;top:0;width:1200px;height:530px;background:linear-gradient(90deg,rgba(11,12,14,.86) 0,rgba(11,12,14,.55) 45%,rgba(11,12,14,0) 75%),linear-gradient(0deg,rgba(11,12,14,.7) 0,rgba(11,12,14,0) 45%)}}
.txt{{position:absolute;left:64px;bottom:150px;width:760px}} .t{{{tcss};text-shadow:0 2px 24px rgba(0,0,0,.6)}}
.txt p{{font:600 30px/1.25 Inter;margin:18px 0 0;max-width:640px;text-shadow:0 2px 12px rgba(0,0,0,.7)}}
.strip{{position:absolute;left:0;bottom:0;width:1200px;height:100px;background:#0B0C0E;border-top:4px solid {acc};display:flex;align-items:center;justify-content:space-between;padding:0 64px}}
.strip .wm{{font-size:38px}} .cta{{font:700 20px Inter;letter-spacing:.13em;text-transform:uppercase;display:flex;align-items:center;gap:14px}}
.cta i{{width:0;height:0;border-left:13px solid #C8F250;border-top:9px solid transparent;border-bottom:9px solid transparent}}''')
panels=''.join(f'<div class=p style="background-image:url(file://{R}/assets/img/{g[0]}/card-960.jpg)"><span>{g[1].upper()}</span></div>' for g in GAMES)
common='''.panels{position:absolute;left:48px;right:48px;top:48px;height:300px;display:grid;grid-template-columns:repeat(4,1fr);gap:8px}
.p{background-size:cover;background-position:center;position:relative;filter:brightness(.88)} .p span{position:absolute;left:0;right:0;bottom:14px;text-align:center;font:700 15px Inter;letter-spacing:.1em;text-shadow:0 1px 8px rgba(0,0,0,.9)}
.p::after{content:"";position:absolute;inset:0;background:linear-gradient(0deg,rgba(11,12,14,.75),rgba(11,12,14,0) 45%)} .p span{z-index:1}
.lock{position:absolute;left:48px;right:48px;bottom:52px;display:flex;align-items:flex-end;justify-content:space-between}
.lock .wm{font-size:80px;white-space:nowrap} .right{display:flex;flex-direction:column;align-items:flex-end;gap:10px} .one{font:800 24px Unbounded;letter-spacing:-.01em;white-space:nowrap} .sub{font:700 22px Inter;letter-spacing:.13em;text-transform:uppercase;display:flex;align-items:center;gap:14px;padding-bottom:6px;white-space:nowrap}
.sub i{width:0;height:0;border-left:14px solid #C8F250;border-top:10px solid transparent;border-bottom:10px solid transparent}
.tag{position:absolute;left:48px;bottom:170px;font:800 34px Unbounded;letter-spacing:-.01em}'''
page('home', f'<div class=panels>{panels}</div><div class=lock><span class=wm>Trevor<b>Games</b></span><span class=right><span class=one>One developer. Four games.</span><span class=sub><i></i>Free demos on Steam</span></span></div>', common.replace('top:48px;height:300px','top:48px;height:330px'))
page('press', f'<div class=panels>{panels}</div><div class=lock><span class=wm>Trevor<b>Games</b></span><span class=right><span class=one>Press kit</span><span class=sub><i></i>Four games on Steam</span></span></div>', common.replace('top:48px;height:300px','top:48px;height:330px'))
json.dump(jobs,open(f'{O}/jobs.json','w'))
subprocess.run(['node',f'{W}/render.mjs',f'{O}/jobs.json'],check=True)
os.makedirs(f'{R}/assets/img/og',exist_ok=True)
for j in jobs:
    n=os.path.basename(j['out'])[:-4]
    subprocess.run(['convert',j['out'],'-strip','-interlace','Plane','-sampling-factor','4:2:0','-quality','82',f'{R}/assets/img/og/{n}.jpg'],check=True)
print('ok')
