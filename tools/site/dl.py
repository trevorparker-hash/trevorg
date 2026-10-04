import os as _os
_ROOT = _os.path.abspath(_os.path.join(_os.path.dirname(__file__), '..', '..'))
import json, os, subprocess, re
R=_ROOT
d=json.load(open(_os.path.join(_os.path.dirname(__file__), 'data', 'steam_games.json')))
keys={'library_hero_2x':'key_art','header_2x':'header','main_capsule_2x':'main_capsule','library_capsule_2x':'library_capsule','hero_capsule_2x':'hero_capsule'}
for g in d[:4]:
    gid=g['id']; out=f'{R}/assets/press/{gid}'; os.makedirs(out,exist_ok=True)
    jobs=[]
    for k,name in keys.items():
        jobs.append((g['assets'][k], f'{out}/{gid}_{name}.jpg'))
    for i,u in enumerate(g['screenshots'],1):
        jobs.append((u, f'{out}/{gid}_screenshot_{i:02d}.jpg'))
    for u,p in jobs:
        if not os.path.exists(p):
            subprocess.run(['curl','-sS','-f','--retry','3','-o',p,u],check=True)
    print(gid, len(jobs))
