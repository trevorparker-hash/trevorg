import os as _os
_ROOT = _os.path.abspath(_os.path.join(_os.path.dirname(__file__), '..', '..'))
import os, re, sys
from html.parser import HTMLParser
from urllib.parse import urlsplit, unquote
R = _ROOT
PAGES = ['index.html', 'games/engagement/index.html', 'games/fight/index.html', 'games/street-takeover/index.html',
         'games/field-surgeon/index.html', 'press/index.html', '404.html']
class P(HTMLParser):
    def __init__(s):
        super().__init__(); s.refs = []; s.ids = set()
    def handle_starttag(s, tag, attrs):
        a = dict(attrs)
        if 'id' in a: s.ids.add(a['id'])
        for k in ('href', 'src', 'poster'):
            if k in a and a[k] is not None and not (tag == 'base'):
                s.refs.append((tag, k, a[k]))
        if 'srcset' in a:
            for part in a['srcset'].split(','):
                s.refs.append((tag, 'srcset', part.strip().split()[0]))
        if tag == 'meta' and a.get('property', a.get('name', '')) in ('og:image', 'twitter:image', 'og:url'):
            s.refs.append((tag, a.get('property', a.get('name')), a['content']))
parsed = {}
for pg in PAGES:
    p = P(); p.feed(open(os.path.join(R, pg)).read()); parsed[pg] = p
BASE = 'https://trevorparker-hash.github.io/trevorg/'
bad = []; n = 0; ext = set(); abs_internal = 0
def target(pg, ref):
    base_dir = '' if pg == '404.html' else os.path.dirname(pg)
    u = urlsplit(ref)
    path = unquote(u.path)
    full = os.path.normpath(os.path.join(base_dir, path)) if path else pg
    if path.endswith('/') or path in ('', './') and not u.fragment and path:
        full = os.path.join(full, 'index.html')
    elif os.path.isdir(os.path.join(R, full)):
        full = os.path.join(full, 'index.html')
    return full, u.fragment
for pg, p in parsed.items():
    for tag, k, ref in p.refs:
        n += 1
        if ref.startswith(BASE):
            abs_internal += 1
            ref_rel = ref[len(BASE):]
            full, frag = target('404.html', ref_rel or './')
            if not os.path.exists(os.path.join(R, full)): bad.append((pg, k, ref, 'missing abs-internal ' + full))
            continue
        if re.match(r'^(https?:)?//', ref):
            ext.add(ref.split('?')[0]); continue
        if ref.startswith(('mailto:', 'tel:')): continue
        if ref.startswith('/'):
            bad.append((pg, k, ref, 'root-absolute path')); continue
        full, frag = target(pg, ref)
        if not os.path.exists(os.path.join(R, full)):
            bad.append((pg, k, ref, 'missing ' + full)); continue
        if frag and full.endswith('.html'):
            ids = parsed.get(full).ids if full in parsed else None
            if ids is not None and frag not in ids:
                bad.append((pg, k, ref, f'missing #{frag} in {full}'))
print(f'{n} references checked across {len(PAGES)} pages; {abs_internal} absolute github.io URLs (og/canonical) also mapped to files')
print('external URLs:', len(ext)); [print('  ', e) for e in sorted(ext)]
print('PROBLEMS:', len(bad)); [print('  ', b) for b in bad]
