"""Writes the TrevorGames static site into /home/user/trevorg.
The output is plain hand-editable HTML; this script is only an authoring aid."""
import os as _os
_ROOT = _os.path.abspath(_os.path.join(_os.path.dirname(__file__), '..', '..'))
import json, os, re, html, subprocess
from about import about, G as STORE

R = _ROOT
BASE = 'https://trevorparker-hash.github.io/trevorg/'
TODAY = '2026-10-03'
E = html.escape

SOCIALS = [
    ('X', '@TrevorGamesHQ', 'https://x.com/TrevorGamesHQ', 'x'),
    ('Bluesky', '@trevorgameshq.bsky.social', 'https://bsky.app/profile/trevorgameshq.bsky.social', 'bluesky'),
    ('TikTok', '@trevorgameshq', 'https://www.tiktok.com/@trevorgameshq', 'tiktok'),
    ('YouTube', '@TrevorGamesHQ', 'https://www.youtube.com/@TrevorGamesHQ', 'youtube'),
]
# Official brand glyphs, single filled paths from Simple Icons 13.21.0 (CC0): x, bluesky, tiktok, youtube.
ICON = {
    'x': '<path fill="currentColor" d="M18.901 1.153h3.68l-8.04 9.19L24 22.846h-7.406l-5.8-7.584-6.638 7.584H.474l8.6-9.83L0 1.154h7.594l5.243 6.932ZM17.61 20.644h2.039L6.486 3.24H4.298Z"/>',
    'bluesky': '<path fill="currentColor" d="M12 10.8c-1.087-2.114-4.046-6.053-6.798-7.995C2.566.944 1.561 1.266.902 1.565.139 1.908 0 3.08 0 3.768c0 .69.378 5.65.624 6.479.815 2.736 3.713 3.66 6.383 3.364.136-.02.275-.039.415-.056-.138.022-.276.04-.415.056-3.912.58-7.387 2.005-2.83 7.078 5.013 5.19 6.87-1.113 7.823-4.308.953 3.195 2.05 9.271 7.733 4.308 4.267-4.308 1.172-6.498-2.74-7.078a8.741 8.741 0 0 1-.415-.056c.14.017.279.036.415.056 2.67.297 5.568-.628 6.383-3.364.246-.828.624-5.79.624-6.478 0-.69-.139-1.861-.902-2.206-.659-.298-1.664-.62-4.3 1.24C16.046 4.748 13.087 8.687 12 10.8Z"/>',
    'tiktok': '<path fill="currentColor" d="M12.525.02c1.31-.02 2.61-.01 3.91-.02.08 1.53.63 3.09 1.75 4.17 1.12 1.11 2.7 1.62 4.24 1.79v4.03c-1.44-.05-2.89-.35-4.2-.97-.57-.26-1.1-.59-1.62-.93-.01 2.92.01 5.84-.02 8.75-.08 1.4-.54 2.79-1.35 3.94-1.31 1.92-3.58 3.17-5.91 3.21-1.43.08-2.86-.31-4.08-1.03-2.02-1.19-3.44-3.37-3.65-5.71-.02-.5-.03-1-.01-1.49.18-1.9 1.12-3.72 2.58-4.96 1.66-1.44 3.98-2.13 6.15-1.72.02 1.48-.04 2.96-.04 4.44-.99-.32-2.15-.23-3.02.37-.63.41-1.11 1.04-1.36 1.75-.21.51-.15 1.07-.14 1.61.24 1.64 1.82 3.02 3.5 2.87 1.12-.01 2.19-.66 2.77-1.61.19-.33.4-.67.41-1.06.1-1.79.06-3.57.07-5.36.01-4.03-.01-8.05.02-12.07z"/>',
    'youtube': '<path fill="currentColor" d="M23.498 6.186a3.016 3.016 0 0 0-2.122-2.136C19.505 3.545 12 3.545 12 3.545s-7.505 0-9.377.505A3.017 3.017 0 0 0 .502 6.186C0 8.07 0 12 0 12s0 3.93.502 5.814a3.016 3.016 0 0 0 2.122 2.136c1.871.505 9.376.505 9.376.505s7.505 0 9.377-.505a3.015 3.015 0 0 0 2.122-2.136C24 15.93 24 12 24 12s0-3.93-.502-5.814zM9.545 15.568V8.432L15.818 12l-6.273 3.568z"/>',
}
ARROW = '<svg viewBox="0 0 24 24" aria-hidden="true" focusable="false"><path d="M7 4.5v15l12.5-7.5z" fill="currentColor"/></svg>'

def icon(k):
    return f'<svg viewBox="0 0 24 24" aria-hidden="true" focusable="false">{ICON[k]}</svg>'

def steam(gid, campaign):
    return f"{GAMES[gid]['store']}?utm_source=website&amp;utm_medium=web&amp;utm_campaign={campaign}&amp;utm_content={gid}"

def devpage(campaign):
    return f"https://store.steampowered.com/search/?developer=Trevor&amp;utm_source=website&amp;utm_medium=web&amp;utm_campaign={campaign}&amp;utm_content=trevorgames"

CAT_NAMES = {'#category_playable_at_your_own_pace': 'Playable at your own pace'}

# ---------------------------------------------------------------- copy
GAMES = {
 'engagement': dict(
   name='Engagement', store='https://store.steampowered.com/app/5195200/Engagement/', appid=5195200,
   eyebrow='Action · Strategy · RPG', fx='50%', shot_ar='2.4 / 1', rows=[3, 3, 3, 3],
   card='One capital ship, fifteen minutes until relief. Every level bolts something new onto your hull, and the escorts who survive get promoted.',
   pitch='One capital ship. Fifteen minutes until relief. Bolt salvaged guns onto your hull, raise a fleet of named escorts who rank up and branch, and hold the lane against a Hollow swarm that grows every minute you survive.',
   short='One capital ship. Fifteen minutes until relief. Bolt salvaged guns onto your hull, raise a fleet of named escorts who rank up and branch, and hold the lane against a Hollow swarm that grows every minute you survive.',
   meta='Engagement: one capital ship, fifteen minutes until relief, and a Hollow swarm that grows every minute. A game by solo developer Trevor. Free demo on Steam.',
   art_alt='Engagement key art: a capital ship and its escorts in front of a ringed planet',
   press_paras=[0, 1, 2, 3],
   font='saira-800italic-latin.woff2',
   shots=[
     'A capital ship in its yard cradle above a ringed planet, under the sector title Belt of Ashes',
     'The capital ship sliding out of a long orbital dock',
     'The capital ship firing its turrets into a swarm of enemy fighters',
     'Beam fire hitting the Hollow Crown, seen from behind the player ship',
     'The Hold the lane countdown at the start of a run, near a ringed planet',
     'The Hollow Crown arrives, glowing red, with its name across the screen',
     'Relief fleet arrived: a large relief ship reaches the player ship',
     'The Reaver, a spiked Hollow capital ship, entering the lane',
     'The Choose a refit screen, offering a Wasp bomber, shield domes or a flak battery',
     'The lane held: the player ship and its escorts after surviving a run',
     'The Maw, a long ribbed Hollow ship, passing a planet',
     'The player ship trading fire with the Maw',
   ],
   clips=['Every level bolts something onto your hull', 'Then they send capital ships', 'Boss fight: the Hollow Crown'],
   # v1 plays a website copy re-cut with the same hook; the social file engagement/engagement_v1.mp4 still says the old one.
   clip_src={1: 'assets/video/engagement_v1.mp4'},
   wide_label='Gameplay: the Reaver, the Maw and the Hollow Crown (26 seconds)',
 ),
 'fight': dict(
   name='FIGHT', store='https://store.steampowered.com/app/5200410/FIGHT/', appid=5200410,
   eyebrow='Action · Strategy · Early Access', fx='60%', shot_ar='16 / 9', rows=[2, 4, 4],
   card='A tactical fighting game about hidden plans. Queue steps, guards and strikes on a shared timeline, commit blind, then watch both plans collide in real time.',
   pitch='Queue your steps, guards and strikes, then commit blind and watch both plans collide. Master over twenty weapon-bound fighters, posture breaks, parries and projectiles, with real-time replays to watch the battle back.',
   short="Let's FIGHT. Queue your steps, guards, and strikes, then commit blind and watch both plans collide into skill-based warfare. Master over twenty weapon-bound fighters, posture breaks, parries and projectiles, with real-time replays to watch the battle back in style.",
   meta='FIGHT is a tactical fighting game about hidden plans. Queue moves on a shared timeline, commit blind, then watch both plans meet in real time. Free demo on Steam.',
   art_alt='FIGHT key art: a white and blue samurai and a hooded fighter with a red greatsword clash in the snow',
   press_paras=[0, 1, 3, 4],
   font='kanit-700italic-latin.woff2',
   shots=[
     'The Barbarian and the Sorcerer trade blows on a pale stone stage, with the move timeline along the bottom',
     'The Berserker stands over the knocked-down Paladin in a torchlit arena',
     'The Ronin lands a hit on the Knight beside standing stones',
     'A Knockdown callout as a fighter falls on a sunset stage',
     'The Ranger and the Ninja fight on an orange beach stage',
     'The Ronin and the Knight square up on a meadow while the move timeline is planned',
     'A close camera on an armoured fighter mid-swing on a night stage',
     'A bright flash as two fighters clash on a night stage',
     'The Battlemage and the Tengu duel on a snow stage, with the move timeline below',
     'Two fighters clash in the rain on a night stage',
   ],
   clips=['Knockdown after knockdown', 'You plan blind. So does he.', 'Rock, paper, scissors with swords'],
   wide_label='Gameplay: blind plans, then the rules for guards, throws, strikes and posture (26 seconds)',
 ),
 'street-takeover': dict(
   name='Street Takeover', store='https://store.steampowered.com/app/5311310/Street_Takeover/', appid=5311310,
   eyebrow='Racing', fx='40%', shot_ar='16 / 9', rows=[3, 4, 4, 4],
   card='A racing game about police chases and damage that stays with the car. Run the getaway campaign, then play the same ten nights as the police.',
   pitch="A racing game about high-speed police chases, wrecked and damaged car physics, and taking on the county from the racer's seat or leading its police force in cleaning up the town.",
   short="Drive Fast. Pit Harder. Takeover. Street Takeover is a racing game about high-speed police chases, wrecked and damaged car physics, and taking on the county from the racer's seat or leading its police force in cleaning up the town.",
   meta='Street Takeover is a racing game about police chases and damage that stays. Run from the county police, then play the same ten nights as them. Free demo on Steam.',
   art_alt='Street Takeover key art: an orange muscle car with police cruisers behind it on a wet city street at night',
   press_paras=[0, 1, 2, 3, 4, 5, 6],
   font='archivo-expanded-800italic-latin.woff2',
   shots=[
     'Police cruisers box in a car on a city street at night, next to a truck',
     'Police cruisers chase a car down a snowy highway, seen from above',
     'An orange muscle car gets air over a rise in a small town at dusk',
     'A police cruiser jammed against a truck after a crash',
     'An orange muscle car on a wet city street at night, with the route map and dispatch feed on screen',
     'Police cruisers chase a car along a forest road at sunset, seen from above',
     'An orange muscle car and a red off-roader race on a dirt track lined with snowy trees',
     'Headlights closing in on a dark road at night',
     'A police cruiser alongside a muscle car on a tree-lined road at sunset',
     'A police cruiser spins out in a pile-up on a city street at night',
     'A car with its headlights on, racing down a dark highway',
     'Cars smash into each other in a floodlit demolition derby arena',
     'Police cruisers swarm a car on a city street at night, with dispatch calls for the orange muscle car on screen',
     'An orange muscle car on a palm-lined coast road at Vela Point at sundown, with a roadblock warning 260 m ahead',
     'An orange muscle car and a red off-roader on a muddy dirt track',
   ],
   clips=['Night run. Then the sirens start.', 'Every cop in town wants this car', 'Snow chase. The cop is gaining.'],
   wide_label='Gameplay: a night getaway turns into police chases across the county (23 seconds)',
 ),
 'field-surgeon': dict(
   name='Field Surgeon', store='https://store.steampowered.com/app/5339030/Field_Surgeon/', appid=5339030,
   eyebrow='RPG · Simulation', fx='38%', shot_ar='16 / 9', rows=[2, 3, 3],
   card='Scrub in at the hospice of a plague-ridden free city at war. Draw arrows from bone, close sabre cuts and saw shattered limbs for humans, dwarves, elves, orcs, hornfolk and giants.',
   pitch='Scrub in as a field surgeon in a plague-ridden free city at war. Humans, dwarves, elves, orcs, hornfolk and giants come to your table. Draw arrows from bone, close sabre cuts, saw shattered limbs, and face the Malison: a curse that fights back from inside your patients.',
   short='Scrub in as a field surgeon in a plague-ridden free city at war. Humans, dwarves, elves, orcs, hornfolk and giants come to your table. Draw arrows from bone, close sabre cuts, saw shattered limbs, and face the Malison: a curse that fights back from inside your patients.',
   meta='Field Surgeon is a surgery-action game set in a plague-ridden free city at war. Six races, eight period instruments, and curses that fight back. Free demo on Steam.',
   art_alt='Field Surgeon key art: a surgeon operates on an armoured patient by lantern light in a war tent',
   press_paras=[0, 1, 2, 3, 4],
   font='cinzel-700-latin.woff2',
   shots=[
     'A patient with knife wounds across his chest, as Sister Alisa says to zig-zag the gut thread across the wound',
     'The Mother Sings: sores on a patient\'s chest that must be drawn out by hand',
     'An opened abdomen held back with pins, with two green growths on the organs',
     'A wide wound pinned open on a patient, in the case The Boar Hunt',
     'The Mother Sings, The Stone Sickness: a crust of stone plates over a patient\'s cuts',
     'A bruised patient with a stab wound, as Sister Alisa notes the wound is still there',
     'Inquisitor Stroh of the Ash Tribunal in a timbered street at dusk: "A plague case. In the Watch\'s own hospital."',
     'The Mother Sings, All Eight Plagues: an opened abdomen with a Miss marker on the incision',
   ],
   clips=['First, get his armour off', 'Open him up. Find the rot.', 'Surgery in a city at war'],
   wide_label='Gameplay: armour off, then the operating table (15 seconds)',
 ),
}
ORDER = ['engagement', 'fight', 'street-takeover', 'field-surgeon']
for gid in ORDER:
    s = STORE[gid]
    GAMES[gid]['genres'] = s['genres']
    GAMES[gid]['cats'] = [CAT_NAMES.get(c, c) for c in s['categories']]

def dims(path):
    out = subprocess.run(['identify', '-format', '%w %h', path], capture_output=True, text=True, check=True).stdout
    w, h = out.split()[:2]
    return int(w), int(h)

def mb(path):
    n = os.path.getsize(path)
    return f'{n/1048576:.1f} MB' if n >= 1048576 else f'{round(n/1024)} KB'

# ---------------------------------------------------------------- shared parts
def head(p, *, title, desc, path, og, og_alt, ogtitle=None, ld=None, extra_font=None, base=None, noindex=False, assets=True):
    canon = BASE + path
    ogimg = BASE + f'assets/img/og/{og}.jpg'
    ogtitle = ogtitle or title
    lines = ['<!doctype html>', '<html lang="en">', '<head>', '<meta charset="utf-8">',
             '<meta name="viewport" content="width=device-width, initial-scale=1">']
    if base:
        lines += base
    lines += [f'<title>{E(title)}</title>',
              f'<meta name="description" content="{E(desc)}">',
              f'<link rel="canonical" href="{canon}">']
    if noindex:
        lines.append('<meta name="robots" content="noindex">')
    lines += ['<meta name="theme-color" content="#0B0C0E">',
              '<meta name="color-scheme" content="dark">',
              '<meta property="og:type" content="website">',
              '<meta property="og:site_name" content="TrevorGames">',
              f'<meta property="og:title" content="{E(ogtitle)}">',
              f'<meta property="og:description" content="{E(desc)}">',
              f'<meta property="og:url" content="{canon}">',
              f'<meta property="og:image" content="{ogimg}">',
              '<meta property="og:image:width" content="1200">',
              '<meta property="og:image:height" content="630">',
              f'<meta property="og:image:alt" content="{E(og_alt)}">',
              '<meta property="og:locale" content="en_US">',
              '<meta name="twitter:card" content="summary_large_image">',
              '<meta name="twitter:site" content="@TrevorGamesHQ">',
              f'<meta name="twitter:title" content="{E(ogtitle)}">',
              f'<meta name="twitter:description" content="{E(desc)}">',
              f'<meta name="twitter:image" content="{ogimg}">',
              f'<meta name="twitter:image:alt" content="{E(og_alt)}">',
              f'<link rel="icon" href="{p}favicon.ico" sizes="16x16 32x32 48x48">',
              f'<link rel="icon" href="{p}assets/icons/favicon-32.png" sizes="32x32" type="image/png">',
              f'<link rel="apple-touch-icon" href="{p}assets/icons/apple-touch-icon.png">']
    if assets:  # 404.html writes its own stylesheet and script tags once its base is known
        lines += [f'<link rel="preload" href="{p}assets/fonts/unbounded-latin.woff2" as="font" type="font/woff2" crossorigin>',
                  f'<link rel="preload" href="{p}assets/fonts/inter-latin.woff2" as="font" type="font/woff2" crossorigin>']
        if extra_font:
            lines.append(f'<link rel="preload" href="{p}assets/fonts/{extra_font}" as="font" type="font/woff2" crossorigin>')
        lines += [f'<link rel="stylesheet" href="{p}assets/css/site.css">',
                  f'<script src="{p}assets/js/site.js" defer></script>']
    if ld:
        lines.append('<script type="application/ld+json">\n' + json.dumps(ld, indent=2, ensure_ascii=False) + '\n</script>')
    lines.append('</head>')
    return '\n'.join(lines)

def header(p, home_link, current=None, home=False):
    games = '#games' if home else f'{home_link}#games'
    brand = (f'<a class="monogram" href="{home_link}" aria-label="TrevorGames home">T<span class="g">G</span></a>' if home
             else f'<a class="wordmark" href="{home_link}" aria-label="TrevorGames home">Trevor<span class="g">Games</span></a>')
    cur = lambda k: ' aria-current="page"' if current == k else ''
    return f'''<a class="skip-link" href="#main">Skip to content</a>
<header class="site-header">
  <div class="wrap">
    {brand}
    <nav class="nav" aria-label="Main">
      <a href="{games}">Games</a>
      <a href="{p}press/"{cur('press')}>Press<span class="nav-long">&nbsp;kit</span></a>
      <a href="#follow">Follow</a>
    </nav>
  </div>
</header>'''

def follow():
    items = '\n'.join(
        f'''      <li><a href="{url}" rel="me">{icon(k)}<span><span class="name">{name}</span><span class="handle">{handle}</span></span></a></li>'''
        for name, handle, url, k in SOCIALS)
    return f'''<section id="follow" class="section follow" aria-labelledby="follow-title">
  <div class="wrap">
    <h2 id="follow-title" class="section-title">Follow</h2>
    <p class="section-lede">Clips from all four games, posted as @TrevorGamesHQ.</p>
    <ul class="follow-list">
{items}
    </ul>
  </div>
</section>'''

def footer(p, campaign):
    return f'''<footer class="site-footer">
  <div class="wrap">
    <p>&copy; 2026 TrevorGames</p>
    <nav aria-label="Footer">
      <a href="{p}press/">Press kit</a>
      <a href="{devpage(campaign)}">Steam developer page</a>
    </nav>
  </div>
</footer>
</body>
</html>
'''

def write(rel, text):
    path = os.path.join(R, rel)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    text = re.sub(r'[ \t]+\n', '\n', text)
    open(path, 'w').write(text)
    print('wrote', rel, len(text.encode()), 'bytes')

def srcset(prefix, gid, name, widths):
    return ', '.join(f'{prefix}assets/img/{gid}/{name}-{w}.jpg {w}w' for w in widths)

# ---------------------------------------------------------------- home
def home():
    p = ''
    ld = {
        '@context': 'https://schema.org', '@type': 'Organization', 'name': 'TrevorGames', 'url': BASE,
        'logo': BASE + 'trevorgames/avatar_400.png',
        'description': 'TrevorGames is Trevor, a solo game developer. Four games on Steam: Engagement, FIGHT, Street Takeover and Field Surgeon.',
        'founder': {'@type': 'Person', 'name': 'Trevor'},
        'sameAs': [s[2] for s in SOCIALS] + ['https://store.steampowered.com/search/?developer=Trevor'],
    }
    cards = []
    for gid in ORDER:
        g = GAMES[gid]
        cards.append(f'''      <article class="card t-{gid}">
        <a class="card-art" href="games/{gid}/" tabindex="-1" aria-hidden="true">
          <img src="assets/img/{gid}/card-960.jpg" srcset="{srcset(p, gid, 'card', [960, 1920])}" sizes="(min-width: 1280px) 586px, (min-width: 800px) calc(50vw - 56px), calc(100vw - 32px)" width="960" height="540" alt="{E(g['art_alt'])}" loading="lazy" decoding="async">
        </a>
        <div class="card-body">
          <p class="eyebrow">{g['eyebrow']}</p>
          <h3 class="card-title"><a href="games/{gid}/">{g['name']}</a></h3>
          <p class="card-pitch">{E(g['card'])}</p>
          <div class="actions">
            <a class="btn btn-primary" href="{steam(gid, 'home')}">Free demo on Steam</a>
            <a class="btn btn-ghost" href="games/{gid}/" aria-label="{g['name']} details">Details</a>
          </div>
        </div>
      </article>''')
    body = f'''{head(p, title='TrevorGames · One developer. Four games.', ogtitle='TrevorGames: one developer, four games',
        desc='TrevorGames is Trevor, a solo developer. Engagement, FIGHT, Street Takeover and Field Surgeon are on Steam, and each one has a free demo.',
        path='', og='home', og_alt='TrevorGames: key art from Engagement, FIGHT, Street Takeover and Field Surgeon above the wordmark', ld=ld)}
<body class="page-home">
{header(p, './', home=True)}
<main id="main">
  <section class="home-hero" aria-labelledby="site-title">
    <div class="wrap">
      <div class="hero-copy">
        <h1 id="site-title" class="wordmark wordmark-xl">Trevor<span class="g">Games</span></h1>
        <p class="tagline"><span>One developer.</span> <span>Four games.</span></p>
        <p class="intro">I'm Trevor, and I make games on my own. Four of them have free demos on Steam.</p>
        <div class="actions">
          <a class="btn btn-primary" href="#games">See the four games</a>
          <a class="btn btn-ghost" href="{devpage('home')}">All on Steam</a>
        </div>
      </div>
      <figure class="hero-video">
        <div class="player" data-label="Play the TrevorGames trailer">
          <video controls playsinline preload="none" poster="assets/img/home/trailer-poster.jpg" width="1920" height="1080" src="trevorgames/trevorgames_trailer.mp4" aria-label="TrevorGames trailer"></video>
        </div>
        <figcaption>Studio trailer: Engagement, FIGHT, Street Takeover and Field Surgeon in 49 seconds.</figcaption>
      </figure>
    </div>
  </section>

  <section id="games" class="section games" aria-labelledby="games-title">
    <div class="wrap">
      <h2 id="games-title" class="section-title">The games</h2>
      <div class="cards">
{chr(10).join(cards)}
      </div>
    </div>
  </section>

  <section class="more" aria-label="Coming later">
    <div class="wrap">
      <p>More games are on the way.</p>
    </div>
  </section>

{follow()}
</main>
{footer(p, 'home')}'''
    write('index.html', body)

# ---------------------------------------------------------------- game pages
def gallery_items(gid, p):
    g = GAMES[gid]
    items = []
    spans = []
    for cols in g['rows']:
        spans += [12 // cols] * cols
    n = len(g['shots'])
    assert len(spans) == n, (gid, len(spans), n)
    for i, alt in enumerate(g['shots'], 1):
        w, h = dims(f'{R}/assets/img/{gid}/shots/{i:02d}-640.jpg')
        span = spans[i - 1]
        px = round(1200 * span / 12)
        mwide = ' class="m-wide"' if (n % 2 == 1 and i == 1) else ''
        items.append(f'''        <li{mwide} style="--span:{span}"><a class="shot" href="{p}assets/img/{gid}/shots/{i:02d}-1600.jpg"><img src="{p}assets/img/{gid}/shots/{i:02d}-640.jpg" srcset="{p}assets/img/{gid}/shots/{i:02d}-640.jpg 640w, {p}assets/img/{gid}/shots/{i:02d}-1600.jpg 1600w" sizes="(min-width: 1280px) {px}px, (min-width: 1024px) {round(100*span/12)}vw, 50vw" width="{w}" height="{h}" alt="{E(alt)}" loading="lazy" decoding="async"></a></li>''')
    return '\n'.join(items)

def game(gid):
    g = GAMES[gid]
    p = '../../'
    path = f'games/{gid}/'
    ld = {
        '@context': 'https://schema.org', '@type': 'VideoGame', 'name': g['name'], 'url': BASE + path,
        'description': g['short'], 'genre': g['genres'], 'gamePlatform': 'PC', 'applicationCategory': 'Game',
        'image': BASE + f'assets/img/{gid}/keyart-1920.jpg',
        'author': {'@type': 'Organization', 'name': 'TrevorGames', 'url': BASE},
        'publisher': {'@type': 'Organization', 'name': 'TrevorGames', 'url': BASE},
        'sameAs': [g['store']],
    }
    about_html = '\n'.join('        ' + l for l in about(gid).split('\n'))
    genres = '\n'.join(f'            <li>{E(x)}</li>' for x in g['genres'])
    cats = '\n'.join(f'            <li>{E(x)}</li>' for x in g['cats'])
    clips = []
    for v, hook in enumerate(g['clips'], 1):
        clips.append(f'''          <li>
            <figure>
              <div class="player vertical" data-label="Play {E(g['name'])} clip: {E(hook)}">
                <video controls playsinline preload="none" poster="{p}assets/img/{gid}/v{v}-poster.jpg" width="1080" height="1920" src="{p}{g.get('clip_src', {}).get(v, f'{gid}/{gid}_v{v}.mp4')}" aria-label="{E(g['name'])} clip: {E(hook)}"></video>
              </div>
              <figcaption>{E(hook)}</figcaption>
            </figure>
          </li>''')
    shot_ar = g['shot_ar']
    body = f'''{head(p, title=f"{g['name']} · Free demo on Steam · TrevorGames", ogtitle=f"{g['name']}: free demo on Steam",
        desc=g['meta'], path=path, og=gid, og_alt=f"{g['name']}: {g['art_alt'].split(': ',1)[1]}", ld=ld, extra_font=g['font'])}
<body class="page-game t-{gid}">
{header(p, p)}
<main id="main">
  <section class="g-hero" aria-labelledby="game-title">
    <picture class="g-hero-art" style="--fx:{g['fx']}">
      <source media="(max-width: 719px)" srcset="{p}assets/img/{gid}/keyart-m-960.jpg" width="960" height="720">
      <img src="{p}assets/img/{gid}/keyart-1920.jpg" srcset="{srcset(p, gid, 'keyart', [960, 1920, 2880])}" sizes="(min-width: 1858px) 100vw, (min-width: 1500px) 1858px, (min-width: 850px) 124vw, 1053px" width="1920" height="620" alt="{E(g['art_alt'])}" fetchpriority="high" decoding="async">
    </picture>
    <div class="wrap g-hero-body">
      <p class="eyebrow">{g['eyebrow']}</p>
      <h1 id="game-title" class="g-title">{g['name']}</h1>
      <p class="g-pitch">{E(g['pitch'])}</p>
      <div class="actions">
        <a class="btn btn-primary" href="{steam(gid, 'game')}">Free demo on Steam</a>
        <a class="btn btn-ghost" href="{steam(gid, 'game')}">Wishlist on Steam</a>
      </div>
    </div>
  </section>

  <div class="wrap g-main">
    <div class="g-col">
      <section class="prose" aria-labelledby="about-title">
        <h2 id="about-title" class="section-title">About</h2>
{about_html}
      </section>
    </div>
    <aside class="g-side" aria-label="{E(g['name'])} facts">
      <div class="side-block">
        <h2 class="side-title">Facts</h2>
        <dl class="facts">
          <dt>Developer</dt><dd>Trevor (solo)</dd>
          <dt>Studio</dt><dd>TrevorGames</dd>
          <dt>Platform</dt><dd>PC, on Steam</dd>
          <dt>Demo</dt><dd>Free on Steam</dd>
        </dl>
        <h2 class="side-title">Genres</h2>
        <ul class="tags">
{genres}
        </ul>
        <h2 class="side-title">Features</h2>
        <ul class="tags">
{cats}
        </ul>
      </div>
    </aside>
  </div>

  <section class="section wrap" aria-labelledby="shots-title">
    <h2 id="shots-title" class="section-title">Screenshots</h2>
    <ul class="gallery" data-lightbox style="--shot-ar:{shot_ar}">
{gallery_items(gid, p)}
    </ul>
  </section>

  <section class="section wrap" aria-labelledby="clips-title" style="padding-top:0">
    <h2 id="clips-title" class="section-title">Clips</h2>
    <div class="clips">
      <figure class="clip-wide">
        <div class="player" data-label="Play {E(g['name'])} gameplay clip">
          <video controls playsinline preload="none" poster="{p}assets/img/{gid}/wide-poster.jpg" width="1920" height="1080" src="{p}{gid}/{gid}_wide.mp4" aria-label="{E(g['name'])} gameplay clip"></video>
        </div>
        <figcaption>{E(g['wide_label'])}</figcaption>
      </figure>
      <ul class="clip-row">
{chr(10).join(clips)}
      </ul>
    </div>
  </section>

  <nav class="wrap page-links" aria-label="More">
    <a class="btn btn-ghost" href="{p}">All four games</a>
    <a class="btn btn-ghost" href="{p}press/#{gid}">Press kit for {g['name']}</a>
  </nav>

{follow()}
</main>
{footer(p, 'game')}'''
    write(f'games/{gid}/index.html', body)

# ---------------------------------------------------------------- press
def paras(gid):
    h = about(gid)
    ps = re.findall(r'<p>.*?</p>', h)
    feats = re.search(r'<ul>.*?</ul>', h, flags=re.S)
    return [ps[i] for i in GAMES[gid]['press_paras']], (feats.group(0) if feats else None)

def press():
    p = '../'
    files = [('key_art', 'Key art, no logo'), ('header', 'Header capsule'), ('main_capsule', 'Main capsule'),
             ('library_capsule', 'Library capsule (portrait)'), ('hero_capsule', 'Hero capsule')]
    sections = []
    for gid in ORDER:
        g = GAMES[gid]
        d = f'{R}/assets/press/{gid}'
        dl = []
        for key, label in files:
            f = f'{d}/{gid}_{key}.jpg'
            w, h = dims(f)
            dl.append(f'          <li><a href="{p}assets/press/{gid}/{gid}_{key}.jpg" download><span class="label">{label}</span><span class="meta">{w} × {h} JPG, {mb(f)}</span></a></li>')
        logo = f'{d}/{gid}_logo.png'
        logo_fig = ''
        if os.path.exists(logo):
            w, h = dims(logo)
            dl.append(f'          <li><a href="{p}assets/press/{gid}/{gid}_logo.png" download><span class="label">Logo</span><span class="meta">{w} × {h} PNG, {mb(logo)}</span></a></li>')
            src = 'main capsule' if gid == 'field-surgeon' else 'library capsule'
            logo_fig = f'''
      <figure class="press-logo">
        <img src="{p}assets/press/{gid}/{gid}_logo.png" width="{w}" height="{h}" alt="{E(g['name'])} logo" loading="lazy">
        <figcaption>Logo, cropped from the Steam {src} with its background.</figcaption>
      </figure>'''
        shots = []
        for i, alt in enumerate(g['shots'], 1):
            f = f'{d}/{gid}_screenshot_{i:02d}.jpg'
            w, h = dims(f)
            shots.append(f'        <li><a href="{p}assets/press/{gid}/{gid}_screenshot_{i:02d}.jpg"><img src="{p}assets/img/{gid}/shots/{i:02d}-640.jpg" width="640" height="{round(640*h/w)}" alt="{E(alt)} (full size, {w} × {h})" loading="lazy" decoding="async"></a></li>')
        sizes = sorted({dims(f'{d}/{gid}_screenshot_{i:02d}.jpg') for i in range(1, len(g['shots']) + 1)})
        size_txt = ' or '.join(f'{w} × {h}' for w, h in sizes)
        ps, feats = paras(gid)
        desc = '\n'.join('          ' + x for x in ps)
        feats_html = f'''
          <h3>Features</h3>
          <div class="prose">
{chr(10).join('            ' + l for l in feats.split(chr(10)))}
          </div>''' if feats else ''
        genres = '\n'.join(f'            <li>{E(x)}</li>' for x in g['genres'])
        sections.append(f'''  <section class="section press-game t-{gid}" id="{gid}" aria-labelledby="p-{gid}">
    <div class="wrap">
    <div class="press-game-head">
      <div>
        <h2 id="p-{gid}">{g['name']}</h2>
        <div class="actions" style="margin-top:16px">
          <a class="btn btn-primary" href="{steam(gid, 'press')}">Steam store page</a>
          <a class="btn btn-ghost" href="{p}games/{gid}/">Game page</a>
        </div>
      </div>{logo_fig}
    </div>
    <div class="press-cols">
      <div>
          <h3>Short description</h3>
          <div class="prose"><p>{E(g['short'])}</p></div>
          <h3>Description</h3>
          <div class="prose">
{desc}
          </div>{feats_html}
          <h3>Genres</h3>
          <ul class="tags">
{genres}
          </ul>
      </div>
      <div>
        <h3>Key art and logo</h3>
        <ul class="downloads">
{chr(10).join(dl)}
        </ul>
        <p class="press-note">Files are the full-size store art. The key art has no logo on it.</p>
      </div>
    </div>
    <h3 class="side-title" style="margin-top:36px">Screenshots ({len(g['shots'])})</h3>
    <ul class="shot-grid" style="--shot-ar:{g['shot_ar']}">
{chr(10).join(shots)}
    </ul>
    <p class="press-note">Each thumbnail links to the full-size file ({size_txt} JPG).</p>
    </div>
  </section>''')
    socials = '\n'.join(f'            <li><a href="{u}" rel="me">{n} {h}</a></li>' for n, h, u, _ in SOCIALS)
    games_list = '\n'.join(f'            <li><a href="#{gid}">{GAMES[gid]["name"]}</a></li>' for gid in ORDER)
    trailer = f'{R}/trevorgames/trevorgames_trailer.mp4'
    jump = '\n'.join(f'      <li><a href="#{gid}">{GAMES[gid]["name"]}</a></li>' for gid in ORDER)
    body = f'''{head(p, title='Press kit · TrevorGames', ogtitle='TrevorGames press kit',
        desc='Press kit for TrevorGames: factsheet, descriptions, key art, logos and full-size screenshots for Engagement, FIGHT, Street Takeover and Field Surgeon.',
        path='press/', og='press', og_alt='TrevorGames press kit: key art from all four games above the wordmark')}
<body class="page-press">
{header(p, p, current='press')}
<main id="main">
  <section class="press-head" aria-labelledby="press-title">
    <div class="wrap">
      <h1 id="press-title">Press kit</h1>
      <p>Facts, descriptions, key art and screenshots for the four TrevorGames games. All assets on this page may be used for coverage of the games.</p>
      <p>Contact: message <a href="https://x.com/TrevorGamesHQ">@TrevorGamesHQ on X</a> or <a href="https://bsky.app/profile/trevorgameshq.bsky.social">on Bluesky</a>.</p>
      <ul class="jump" aria-label="Jump to a game">
      <li><a href="#factsheet">Factsheet</a></li>
{jump}
      </ul>
    </div>
  </section>

  <section class="section" id="factsheet" aria-labelledby="fact-title" style="padding-top:40px">
    <div class="wrap">
      <h2 id="fact-title" class="section-title">Factsheet</h2>
      <dl class="factsheet">
        <div><dt>Developer</dt><dd>Trevor (solo)</dd></div>
        <div><dt>Studio</dt><dd>TrevorGames</dd></div>
        <div><dt>Website</dt><dd><a href="{p}">{BASE}</a></dd></div>
        <div><dt>Games</dt><dd>
          <ul class="inline-list">
{games_list}
          </ul>
          Each one has a free demo on Steam.</dd></div>
        <div><dt>Steam developer page</dt><dd><a href="{devpage('press')}">store.steampowered.com/search/?developer=Trevor</a></dd></div>
        <div><dt>Socials</dt><dd>
          <ul class="inline-list">
{socials}
          </ul></dd></div>
        <div><dt>Contact</dt><dd>Message @TrevorGamesHQ on X or Bluesky.</dd></div>
        <div><dt>Studio assets</dt><dd>
          <ul class="inline-list">
            <li><a href="{p}trevorgames/avatar_1080.png" download>TG monogram, 1080 × 1080 PNG</a></li>
            <li><a href="{p}trevorgames/trevorgames_trailer.mp4" download>Studio trailer, 1920 × 1080, 49 s, {mb(trailer)}</a></li>
            <li><a href="{p}trevorgames/trevorgames_trailer_thumb.jpg" download>Trailer thumbnail, 1920 × 1080 JPG</a></li>
          </ul></dd></div>
        <div><dt>Usage</dt><dd>All assets on this page may be used for coverage of the games.</dd></div>
      </dl>
    </div>
  </section>

{chr(10).join(sections)}

{follow()}
</main>
{footer(p, 'press')}'''
    write('press/index.html', body)

# ---------------------------------------------------------------- 404
def notfound():
    p = ''
    base = ['<script>',
            '/* GitHub Pages serves this file at whatever URL was missing, at any depth, so relative links need a base.',
            '   On *.github.io the site lives under /<repo>/; on a custom domain it is the root.',
            '   The base is made here, before anything is fetched, and the stylesheet and script are written after it,',
            '   so every request goes to the right place on either host. */',
            '(function () {',
            '  if (location.protocol !== "file:") {',
            '    var m = location.pathname.match(/^\\/[^\\/]+\\//);',
            '    var b = document.createElement("base");',
            '    b.href = location.protocol + "//" + location.host + (/\\.github\\.io$/i.test(location.hostname) && m ? m[0] : "/");',
            '    document.head.appendChild(b);',
            '    /* In-page links (#main, #follow) would resolve against the base and leave this page. */',
            '    document.addEventListener("DOMContentLoaded", function () {',
            '      var here = location.pathname + location.search;',
            '      document.querySelectorAll(\'a[href^="#"]\').forEach(function (a) { a.setAttribute("href", here + a.getAttribute("href")); });',
            '    });',
            '  }',
            '  document.write(\'<link rel="stylesheet" href="assets/css/site.css"><script src="assets/js/site.js" defer><\\/script>\');',
            '})();',
            '</script>']
    games = '\n'.join(f'        <li><a class="btn btn-ghost" href="games/{gid}/">{GAMES[gid]["name"]}</a></li>' for gid in ORDER)
    body = f'''{head(p, title='Page not found · TrevorGames', desc='This page does not exist. Engagement, FIGHT, Street Takeover and Field Surgeon are on the TrevorGames home page.',
        path='404.html', og='home', og_alt='TrevorGames: key art from Engagement, FIGHT, Street Takeover and Field Surgeon above the wordmark', base=base, noindex=True, assets=False)}
<body class="page-404">
{header(p, './')}
<main id="main">
  <section class="notfound">
    <div class="wrap">
      <p class="code">404</p>
      <h1>Page not found</h1>
      <p>There is nothing at this address. It may have moved, or the link has a typo.</p>
      <div class="actions" style="margin-top:24px">
        <a class="btn btn-primary" href="./">Go to the home page</a>
        <a class="btn btn-ghost" href="press/">Press kit</a>
      </div>
      <ul class="games-list" aria-label="The games">
{games}
      </ul>
    </div>
  </section>
{follow()}
</main>
{footer(p, 'home')}'''
    write('404.html', body)

# ---------------------------------------------------------------- robots, sitemap
def extras():
    pages = ['', 'games/engagement/', 'games/fight/', 'games/street-takeover/', 'games/field-surgeon/', 'press/']
    urls = '\n'.join(f'  <url>\n    <loc>{BASE}{u}</loc>\n    <lastmod>{TODAY}</lastmod>\n  </url>' for u in pages)
    write('sitemap.xml', f'''<?xml version="1.0" encoding="UTF-8"?>
<!--
  Base URL for now: {BASE}
  When the site moves to its own domain, replace that base everywhere it appears:
  every <loc> below, the Sitemap line in robots.txt, the canonical, og:url, og:image
  and twitter:image tags in the <head> of each page, and the JSON-LD blocks.
  One search-and-replace across the repo does it. (404.html works out its own base.)
-->
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
{urls}
</urlset>
''')
    write('robots.txt', f'''# TrevorGames website.
# Crawlers only read robots.txt from the root of a host, so on
# trevorparker-hash.github.io this file (under /trevorg/) is ignored.
# It takes effect once the site is served from its own domain.
# Change the Sitemap URL below at the same time (see sitemap.xml).
User-agent: *
Allow: /

Sitemap: {BASE}sitemap.xml
''')
    write('.nojekyll', '')

if __name__ == '__main__':
    home()
    for gid in ORDER:
        game(gid)
    press()
    notfound()
    extras()
