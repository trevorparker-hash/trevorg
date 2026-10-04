import os as _os
_ROOT = _os.path.abspath(_os.path.join(_os.path.dirname(__file__), '..', '..'))
import os, subprocess, glob
R=_ROOT
J=['-strip','-interlace','Plane','-sampling-factor','4:2:0','-quality','80']
def run(*a): subprocess.run(list(a),check=True)
# x0 for 16:9 card crop (2204x1240) and 4:3 mobile crop (1653x1240) from 3840x1240 key art
FOCUS={'engagement':(798,1123),'fight':(1048,1323),'street-takeover':(560,573),'field-surgeon':(400,574)}
POSTER_T={'engagement':18,'fight':12,'street-takeover':8,'field-surgeon':10}
for g,(cx,mx) in FOCUS.items():
    src=f'{R}/assets/press/{g}/{g}_key_art.jpg'; out=f'{R}/assets/img/{g}'; os.makedirs(out+'/shots',exist_ok=True)
    run('convert',src,'-filter','Lanczos','-resize','1920x',*J,f'{out}/keyart-1920.jpg')
    run('convert',src,'-filter','Lanczos','-resize','960x',*J,f'{out}/keyart-960.jpg')
    run('convert',src,'-crop',f'2204x1240+{cx}+0','+repage','-filter','Lanczos','-resize','1920x1080!',*J,f'{out}/card-1920.jpg')
    run('convert',src,'-crop',f'2204x1240+{cx}+0','+repage','-filter','Lanczos','-resize','960x540!',*J,f'{out}/card-960.jpg')
    run('convert',src,'-crop',f'1653x1240+{mx}+0','+repage','-filter','Lanczos','-resize','960x720!',*J,f'{out}/keyart-m-960.jpg')
    for s in sorted(glob.glob(f'{R}/assets/press/{g}/{g}_screenshot_*.jpg')):
        n=s.rsplit('_',1)[1][:2]
        run('convert',s,'-filter','Lanczos','-resize','1600x',*J,f'{out}/shots/{n}-1600.jpg')
        run('convert',s,'-filter','Lanczos','-resize','640x',*J,f'{out}/shots/{n}-640.jpg')
    # clip posters
    t=POSTER_T[g]
    run('ffmpeg','-v','error','-y','-ss',str(t),'-i',f'{R}/{g}/{g}_wide.mp4','-frames:v','1','-q:v','1','/tmp/_p.png')
    run('convert','/tmp/_p.png','-filter','Lanczos','-resize','1280x720',*J,f'{out}/wide-poster.jpg')
    for v in (1,2,3):
        run('ffmpeg','-v','error','-y','-ss','0.6','-i',f'{R}/{g}/{g}_v{v}.mp4','-frames:v','1','-q:v','1','/tmp/_p.png')
        run('convert','/tmp/_p.png','-filter','Lanczos','-resize','540x960',*J,f'{out}/v{v}-poster.jpg')
    print('done',g)
# favicons
ic=f'{R}/assets/icons'; os.makedirs(ic,exist_ok=True)
a=f'{R}/trevorgames/avatar_400.png'
run('convert',a,'-filter','Lanczos','-resize','32x32','-strip',f'{ic}/favicon-32.png')
run('convert',a,'-filter','Lanczos','-resize','180x180','-strip',f'{ic}/apple-touch-icon.png')
run('convert',a,'-filter','Lanczos','-define','icon:auto-resize=48,32,16',f'{R}/favicon.ico')
