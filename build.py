"""Builds the static pages from shared partials. Run: python3 build.py
Photos live in assets/photos/. Replace any placeholder by saving your photo over it with the same file name."""
import os

SUMMIT_PATH = 'M200 88 C213 140 225 198 248 246 C260 270 284 284 312 276 C292 300 250 304 226 290 C213 282 205 268 200 250 C195 268 187 282 174 290 C150 304 108 300 88 276 C116 284 140 270 152 246 C175 198 187 140 200 88 Z'
SEAL_FONT = "'Holtwood One SC',Georgia,serif"

DEFS = f'''<svg width="0" height="0" style="position:absolute" aria-hidden="true"><defs>
<symbol id="seal" viewBox="0 0 400 400">
  <path id="arcTop" d="M64 200 A136 136 0 0 1 336 200" fill="none"/>
  <path id="arcBot" d="M42 200 A158 158 0 0 0 358 200" fill="none"/>
  <circle cx="200" cy="200" r="182" fill="none" stroke="#2A2826" stroke-width="2"/>
  <circle cx="200" cy="200" r="118" fill="#B4572B"/>
  <text font-family="{SEAL_FONT}" font-size="14" letter-spacing="2" fill="#2A2826"><textPath href="#arcTop" startOffset="50%" text-anchor="middle">DURANGO · COLORADO</textPath></text>
  <text font-family="{SEAL_FONT}" font-size="14" letter-spacing="2" fill="#2A2826"><textPath href="#arcBot" startOffset="50%" text-anchor="middle">SAN JUAN MOUNTAINS</textPath></text>
  <path d="M38 192 H50 L45 200 L50 208 H38 L43 200 Z" fill="#2A2826" transform="rotate(90 44 200)"/>
  <path d="M350 192 H362 L357 200 L362 208 H350 L355 200 Z" fill="#2A2826" transform="rotate(90 356 200)"/>
  <path d="M186 140 H214 L204 150 L214 160 H186 L196 150 Z" fill="#ECE4D3"/>
  <text x="200" y="214" font-family="{SEAL_FONT}" font-size="30" letter-spacing="1" text-anchor="middle" fill="#ECE4D3">OPHIR</text>
  <path d="M186 240 H214 L204 250 L214 260 H186 L196 250 Z" fill="#ECE4D3"/>
</symbol>
<symbol id="summit" viewBox="40 40 320 320"><circle cx="200" cy="200" r="150" fill="#2A2826"/><path d="{SUMMIT_PATH}" fill="#ECE4D3"/></symbol>
</defs></svg>'''

NAV = [('/', 'Home', 'welcome', 'home'),
       ('/homes', 'The Collection', 'our homes', 'homes'),
       ('/stay', 'Your Stay', 'packages & details', 'stay'),
       ('/owners', 'Owners', 'apply & estimate', 'owners'),
       ('/journal', 'Journal', 'stories & guides', 'journal'),
       ('/about', 'About', 'who we are', 'about')]

import json as _json
LD = '<script type="application/ld+json">' + _json.dumps({
  "@context": "https://schema.org", "@type": "LodgingBusiness", "name": "Ophir Stays",
  "description": "Locally owned vacation rental management and trip planning for a private collection of 25 homes in Durango, Colorado.",
  "url": "https://ophirstays.com", "logo": "https://ophirstays.com/assets/email-mark.png", "image": "https://ophirstays.com/assets/og.jpg",
  "email": "casey@ophirstays.com", "founder": {"@type": "Person", "name": "Casey Roberts"},
  "address": {"@type": "PostalAddress", "addressLocality": "Durango", "addressRegion": "CO", "postalCode": "81301", "addressCountry": "US"},
  "areaServed": [{"@type": "City", "name": "Durango, Colorado"}, {"@type": "Place", "name": "Purgatory, Colorado"}, {"@type": "Place", "name": "Vallecito Lake, Colorado"}, {"@type": "AdministrativeArea", "name": "La Plata County, Colorado"}],
  "knowsAbout": ["vacation rental management", "short-term rental management", "Durango trip planning"]
}) + '</script>'

POST_LD = {p: '<script type="application/ld+json">' + _json.dumps({'@context':'https://schema.org','@type':'BlogPosting','headline':h,'image':f'https://ophirstays.com/assets/photos/{img}.jpg','datePublished':'2026-10-15','dateModified':'2026-10-17','author':{'@type':'Person','name':'Casey Roberts','url':'https://ophirstays.com/about'},'publisher':{'@type':'Organization','name':'Ophir Stays','logo':{'@type':'ImageObject','url':'https://ophirstays.com/assets/email-mark.png'}},'mainEntityOfPage':'https://ophirstays.com'+p}) + '</script>' for p,(h,img) in {'/journal/durango-rides': ('Five rides that show you Durango', 'rides'), '/journal/durango-home-earnings': ('What a Durango vacation home earns, and what decides it', 'journal-3'), '/journal/where-to-eat-durango': ('Where to eat in Durango, from a local', 'hero-coffee'), '/journal/durango-short-term-rental-rules': ('Can you rent your Durango home short-term? The rules, city and county', 'ophir')}.items()}

TRAIL_LD = '<script type="application/ld+json">' + _json.dumps({'@context': 'https://schema.org', '@graph': [{'@type': 'Map', '@id': 'https://ophirstays.com/trail-map#map', 'name': 'Ride Durango: Durango mountain bike trail map', 'mapType': 'https://schema.org/VenueMap', 'url': 'https://ophirstays.com/trail-map', 'image': 'https://ophirstays.com/assets/ophir-durango-trail-map.jpg', 'description': 'Free printable map of the mountain bike trail systems around Durango, Colorado, with trailheads, summits and contours.', 'about': {'@type': 'Place', 'name': 'Durango, Colorado', 'geo': {'@type': 'GeoCoordinates', 'latitude': 37.2753, 'longitude': -107.8801}}, 'spatialCoverage': {'@type': 'Place', 'name': 'Durango, Colorado'}, 'author': {'@type': 'Person', 'name': 'Casey Roberts', 'url': 'https://ophirstays.com/about'}, 'publisher': {'@type': 'Organization', 'name': 'Ophir Stays', 'url': 'https://ophirstays.com'}, 'datePublished': '2026-10-17', 'isAccessibleForFree': True, 'encoding': [{'@type': 'MediaObject', 'contentUrl': 'https://ophirstays.com/assets/ophir-durango-trail-map.pdf', 'encodingFormat': 'application/pdf'}, {'@type': 'MediaObject', 'contentUrl': 'https://ophirstays.com/assets/ophir-durango-trail-map.jpg', 'encodingFormat': 'image/jpeg'}]}, {'@type': 'ImageObject', 'contentUrl': 'https://ophirstays.com/assets/ophir-durango-trail-map.jpg', 'name': 'Durango mountain bike trail map', 'creator': {'@type': 'Organization', 'name': 'Ophir Stays'}, 'creditText': 'Ophir Stays. Trail data © OpenStreetMap contributors.', 'copyrightNotice': 'Ophir Stays', 'acquireLicensePage': 'https://ophirstays.com/trail-map#license', 'license': 'https://ophirstays.com/trail-map#license'}, {'@type': 'BreadcrumbList', 'itemListElement': [{'@type': 'ListItem', 'position': 1, 'name': 'Ophir Stays', 'item': 'https://ophirstays.com/'}, {'@type': 'ListItem', 'position': 2, 'name': 'Journal', 'item': 'https://ophirstays.com/journal'}, {'@type': 'ListItem', 'position': 3, 'name': 'Durango trail map', 'item': 'https://ophirstays.com/trail-map'}]}]}) + '</script>'

ROUTES = _json.load(open('data/routes.json'))
RBY = {r['slug']: r for r in ROUTES}
def profile_line(r, w=600, h=130):
    p = r['profile']; n = len(p)
    sm = [sum(p[max(0, i-2):i+3]) / len(p[max(0, i-2):i+3]) for i in range(n)]
    lo, hi = min(sm), max(sm); rng = max(hi - lo, 1)
    band = h * min(1.0, max(0.38, rng / 1500))
    X = lambda i: 4 + (w - 8) * i / (n - 1)
    Y = lambda e: h - 6 - band * (e - lo) / rng
    return 'M' + 'L'.join(f'{X(i):.1f} {Y(e):.1f}' for i, e in enumerate(sm))

def ptile(r, big=False, link=True):
    tag = 'a' if link else 'div'
    href = f' href="/trails/{r["slug"]}"' if link else ''
    w, h = (1000, 170) if big else (600, 130)
    return (f'<{tag} class="ptile{" ptile-big" if big else ""}"{href}>'
            f'<svg viewBox="0 0 {w} {h}" preserveAspectRatio="none" aria-hidden="true"><path d="{profile_line(r, w, h)}" fill="none" stroke="#ECE4D3" stroke-width="{3 if big else 2.4}" stroke-linejoin="round" stroke-linecap="round" vector-effect="non-scaling-stroke"/></svg>'
            f'<div class="pt-head"><b>{r["name"]}</b><span>{r["miles"]} mi</span></div>'
            f'<div class="pt-row"><span>Elevation</span><span>↑ {r["climb"]:,} ft &nbsp;↓ {r["descent"]:,} ft</span></div>'
            f'<div class="pt-row"><span>Difficulty</span><span>{r["difficulty"]}</span></div>'
            f'<div class="pt-row"><span>Area</span><span>{r["area"]}</span></div></{tag}>')


def head(title, desc, path, image='/assets/og.jpg'):
    return f'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{desc}">
<link rel="canonical" href="https://ophirstays.com{path}">
{LD if path == "/" else POST_LD.get(path, "")}{TRAIL_LD if path == "/trail-map" else ""}
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:image" content="https://ophirstays.com{image}">
<meta property="og:type" content="website">
<meta property="og:site_name" content="Ophir Stays">
<meta name="twitter:card" content="summary_large_image">
<meta name="theme-color" content="#FFFFFF">
<link rel="icon" href="/favicon.svg" type="image/svg+xml">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,500;1,500&family=Holtwood+One+SC&family=Jost:wght@400;500;600&display=swap" rel="stylesheet">
<link rel="stylesheet" href="/assets/styles.css">
<script>window.va=window.va||function(){{(window.vaq=window.vaq||[]).push(arguments)}};</script>
<script defer src="/_vercel/insights/script.js"></script>
</head>
<body>
<a class="skip" href="#main">Skip to content</a>
{DEFS}'''

def masthead(current):
    items = ''.join(
        f'<li><a href="{h}"{" aria-current=\"page\"" if k == current else ""}><b>{t}</b></a></li>'
        for h, t, s, k in NAV)
    return f'''<header class="masthead">
  <div class="wrap mh">
    <a class="logo" href="/" aria-label="Ophir Stays, home">
      <svg aria-hidden="true"><use href="#summit"/></svg>
      <span class="word">OPHIR</span>
      <span class="sub">STAYS</span>
    </a>
    <button class="menu-btn" aria-expanded="false" aria-controls="navlist">MENU</button>
    <nav class="mainnav" aria-label="Main"><ul id="navlist">{items}</ul></nav>
  </div>
</header>'''

FOOT = '''<footer class="site-foot">
  <div class="wrap">
    <svg role="img" aria-label="Ophir Stays seal"><use href="#seal"/></svg>
    <p style="margin:0;color:var(--muted)">A private collection of mountain homes in Durango, Colorado. Locally owned.</p>
    <form class="nl" id="nl-form" novalidate>
      <p class="nl-title">Durango, four times a year.</p>
      <p class="nl-sub">A short note each season: what's running, what's open, one great dinner. For owners, a quarterly letter from Casey.</p>
      <div class="nl-row">
        <label class="sr" for="nl-email">Email</label><input id="nl-email" name="email" type="email" autocomplete="email" placeholder="Your email" required>
        <label class="sr" for="nl-list">I am</label><select id="nl-list" name="list"><option value="guest">A traveler</option><option value="owner">A homeowner</option></select>
        <button class="btn" type="submit">Subscribe</button>
      </div>
      <div class="hp" aria-hidden="true"><input name="website" tabindex="-1" autocomplete="off"></div>
      <p class="nl-status" role="status" aria-live="polite"></p>
    </form>
    <nav class="foot-links" aria-label="Footer"><a href="/stay">Your Stay</a><a href="/basecamp">Basecamp</a><a href="/owners">Owners</a><a href="/buying">Buying a Rental</a><a href="/journal">Journal</a><a href="/trails">Bike Routes</a><a href="/trail-map">Trail Map</a><a href="/about">About</a><a href="mailto:casey@ophirstays.com">casey@ophirstays.com</a></nav>
    <div class="foot-base"><span>© 2026 Ophir Stays</span><span>Guest booking opens 2027</span></div>
  </div>
</footer>
<script>
(function(){var b=document.querySelector('.menu-btn'),l=document.getElementById('navlist');b.addEventListener('click',function(){var o=l.classList.toggle('open');b.setAttribute('aria-expanded',o)});
var io='IntersectionObserver' in window?new IntersectionObserver(function(es){es.forEach(function(e){if(e.isIntersecting){e.target.classList.add('in');io.unobserve(e.target)}})},{threshold:.1}):null;
document.querySelectorAll('.reveal').forEach(function(el){io?io.observe(el):el.classList.add('in')});})();
(function(){var f=document.getElementById('nl-form');if(!f)return;var st=f.querySelector('.nl-status');
f.addEventListener('submit',async function(e){e.preventDefault();
if(!/^[^@\\s]+@[^@\\s]+\\.[^@\\s]+$/.test(f.email.value)){st.textContent='Please check your email address.';return}
var b=f.querySelector('button');b.disabled=true;
try{var r=await fetch('/api/subscribe',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify(Object.fromEntries(new FormData(f)))});if(!r.ok)throw 0;
st.textContent='Thank you. The next note arrives with the season.';f.email.value='';}catch(_){st.textContent='Something went wrong. Please email hello@ophirstays.com.';}
b.disabled=false;});})();
</script>'''

def page(title, desc, path, current, body, extra_js='', image='/assets/og.jpg'):
    return head(title, desc, path, image) + masthead(current) + '\n<main id="main">\n' + body + '\n</main>\n' + FOOT + extra_js + '\n</body>\n</html>\n'

def photo(name, alt, cls='photo'):
    return f'<div class="{cls}"><img src="/assets/photos/{name}.jpg" alt="{alt}" loading="lazy"></div>'


# ---------------- THE COLLECTION (homes) ----------------
# Add a home: copy a block, set sample=False, and save 5 photos as assets/photos/homes/<slug>-1.jpg ... -5.jpg
# (1 = hero exterior or view, 2 = great room, 3 = kitchen, 4 = primary bedroom, 5 = hot tub / deck / view).
# SHOW_SAMPLES must be False before launch so no sample home is ever published.
SHOW_SAMPLES = False
BASECAMP_ON = False  # flip to True (with BASECAMP_ON=1 in Vercel) to show Basecamp Ready badges; mark homes with 'basecamp': True
HOMES = [
    dict(slug='sample-cliff-house', sample=True, name='The Cliff House', area='Glacier Club', beds=5, baths=5.5, sleeps=12,
         line='Stone, glass and a fairway view, twenty minutes from town.',
         features=['Hot tub on a deck facing the cliffs', 'Wood-burning stone fireplace', 'Gear room with boot dryers and bike storage',
                   'Chef\'s kitchen with a six-burner range', 'Golf cart for the course'],
         trip='Tee times held, a morning ride in Haflin Canyon, dinner on Main Avenue with the first round on the house.'),
]
LIVE_HOMES = [h for h in HOMES if SHOW_SAMPLES or not h['sample']]

def hphoto(slug, n, alt, cls='photo'):
    return f'<div class="{cls}"><img src="/assets/photos/homes/{slug}-{n}.jpg" alt="{alt}" loading="lazy"></div>'

def home_card(h):
    tag = '<span class="sample-tag" style="margin:14px 0 0">SAMPLE</span>' if h['sample'] else ''
    return f'''<a class="card reveal" href="/homes/{h['slug']}">{hphoto(h['slug'], 1, h['name'] + ', ' + h['area'], 'ph')}{tag}
        <p class="post-meta">{h['area']} · {h['beds']} bedrooms · sleeps {h['sleeps']}</p><h3><span class="ital">{h['name']}</span></h3><p>{h['line']}</p></a>'''

FOUNDING = '''<div class="band two reveal">
        <div><p class="eyebrow">Founding homes</p><h2 class="display">The first homes join the Collection in 2027.</h2>
        <p>Twenty-five places, chosen one at a time. Own a home in Durango that meets the standard?</p></div>
        <a class="btn btn-rust" href="/owners#estimate">Apply</a></div>'''

def collection_grid():
    return f'<div class="grid3">{"".join(home_card(h) for h in LIVE_HOMES)}</div>' if LIVE_HOMES else FOUNDING

# ---------------- HOME ----------------
# PHOTOS TO REPLACE (flagged Nov 2026):
#   hero-ski.jpg  - hazy, flat snow shot. Replace with a crisp bluebird Purgatory or backcountry photo, landscape, 2400px+.
#   hero-golf.jpg, golf.jpg - weak golf shots. Replace before golf goes back on any page.
# The homepage hero uses library/engineer-climb.jpg until a sharp winter photo is in.
HERO_IMG = '/assets/photos/library/needles-alpenglow-purgatory.jpg'
HERO_IMG_WIDE = HERO_IMG
HERO_ALT = 'Alpenglow on the snowy Needle Mountains above homes near Purgatory at dusk'

EXPS = [('ski', 'Ski Purgatory', '/purgatory-vacation-rentals', 'Twenty-five miles up the valley. Where to stay for a Purgatory ski trip, and when to book.'),
        ('bike', 'Ride from town', '/trails', 'Ten mountain bike routes, easy to advanced, each with a map, elevation profile and free GPX.'),
        ('coffee', 'Eat on Main', '/journal/where-to-eat-durango', 'Where we actually eat in Durango, from coffee to a late table downtown.')]
exps = ''.join(f'''<a class="card reveal" href="{u}">
        {photo(n, t + ' in Durango', 'ph')}
        <h3><span class="ital">{t}</span></h3><p>{d}</p><span class="link">Read more</span></a>''' for n, t, u, d in EXPS)

CHECKLIST = [('What the fee is charged on.', 'Nightly rent only, or cleaning and other guest fees too?'),
             ('Cleaning.', 'What the guest pays, what the cleaner is paid, and who keeps the difference.'),
             ('Maintenance.', 'Any markup on repairs, and any call-out fee for small jobs.'),
             ('Pass-through charges.', 'Linens, supplies, card processing and booking-site fees: which ones land on you?'),
             ('Your calendar.', 'Nights rented, nights you used, and nights that were blocked without a reason.'),
             ('Event pricing.', 'Compare the rate on Snowdown or Iron Horse weekend with an ordinary weekend. If they match, money was left behind.'),
             ('Your contract.', 'The notice period, any exit fee, and who owns the listing and its reviews if you leave.')]

home_body = f'''
  <section class="hero">
    <picture><source media="(min-width:721px)" srcset="{HERO_IMG_WIDE}"><img src="{HERO_IMG}" alt="{HERO_ALT}" fetchpriority="high"></picture>
    <div class="hero-in">
      <div class="wrap">
        <p class="eyebrow">Durango · Colorado</p>
        <h1 class="display">Durango homes, run by someone who lives here.</h1>
        <p class="hero-sub">Locally owned and capped at twenty-five homes.</p>
        <div class="hero-btns">
          <a class="btn btn-rust" href="/owners#estimate">Owners: free estimate</a>
          <a class="btn btn-light" href="#guest-list">Guests: join the 2027 list</a>
        </div>
      </div>
    </div>
  </section>

  <section class="offer">
    <div class="wrap">
      <div class="center reveal" style="margin-bottom:44px">
        <p class="eyebrow">For homeowners</p>
        <h2 class="display">Ten founding homes. A guarantee in writing.</h2>
      </div>
      <div class="offer-grid reveal">
        <div class="ocard">
          <p class="eyebrow">The guarantee</p>
          <h3 class="display">You keep more than last year, or we refund the difference.</h3>
          <p>If you take home less in your first twelve months with Ophir than in the twelve before, we refund the difference, up to our full fee.</p>
          <a class="link" href="/owners#guarantee">How the guarantee works</a>
        </div>
        <div class="ocard">
          <p class="eyebrow">Founding homes</p>
          <h3 class="display">22%, locked for as long as you stay.</h3>
          <p>The first ten homes keep our founding rate for life. We are taking on five before summer 2027, slowly and on purpose. Thirty days' notice to leave.</p>
          <a class="btn btn-rust" href="/owners#estimate">Get a free estimate</a>
        </div>
      </div>
    </div>
  </section>

  <section class="center tint">
    <div class="wrap narrow reveal">
      <p class="eyebrow">Small on purpose</p>
      <h2 class="display">One local, never more than twenty-five homes.</h2>
      <hr class="rule">
      <p class="lead">Owners get a direct line to the person running their home. Guests get a trip planned by someone who has skied, ridden and eaten here for twenty-three years, and a local they can text from 7am to 10pm.</p>
    </div>
  </section>

  <section id="fit">
    <div class="wrap">
      <div class="center reveal" style="margin-bottom:44px">
        <p class="eyebrow">Who Ophir is for</p>
        <h2 class="display">A good fit, and not.</h2>
      </div>
      <div class="fit reveal">
        <div>
          <h3>Ophir is a good fit if</h3>
          <ul>
            <li>You want one person to call, and you want that person to live in Durango.</li>
            <li>Your home is in town, the Animas Valley, Hermosa or near Purgatory, and nightly rentals are allowed there.</li>
            <li>You care how guests are treated as much as what they pay.</li>
            <li>You want the quiet weeks on your calendar working harder.</li>
          </ul>
        </div>
        <div>
          <h3>Ophir is probably not for you if</h3>
          <ul>
            <li>You are looking for the lowest fee in town and nothing else.</li>
            <li>You want to approve every booking yourself.</li>
            <li>You would rather not put anything back into the home: photos, linens, repairs.</li>
            <li>You need a manager with hundreds of homes and a call center. We will never be that.</li>
          </ul>
        </div>
      </div>
    </div>
  </section>

  <section class="tint" id="experiences">
    <div class="wrap">
      <div class="center reveal" style="margin-bottom:44px">
        <p class="eyebrow">For guests</p>
        <h2 class="display">Durango, from a local.</h2>
      </div>
      <div class="grid3">{exps}</div>
    </div>
  </section>

  <section id="signup">
    <div class="wrap">
      <div class="signups">
        <form class="su reveal" id="checklist-form" data-list="owner" data-source="checklist" novalidate>
          <p class="eyebrow">For owners</p>
          <h2 class="display">Seven things to check on your manager's statement</h2>
          <p>A one-page checklist from a local manager. Free, and useful even if you never call us.</p>
          <div class="nl-row">
            <label class="sr" for="ck-email">Email</label><input id="ck-email" name="email" type="email" autocomplete="email" placeholder="Your email" required>
            <button class="btn btn-rust" type="submit">Send me the checklist</button>
          </div>
          <div class="hp" aria-hidden="true"><input name="website" tabindex="-1" autocomplete="off"></div>
          <p class="nl-status" role="status" aria-live="polite"></p>
        </form>
        <form class="su reveal" id="guest-list" data-list="guest" data-source="guest-2027" novalidate>
          <p class="eyebrow">For guests</p>
          <h2 class="display">Booking opens in 2027.</h2>
          <p>Join the list and hear first when our homes open, with first pick of dates.</p>
          <div class="nl-row">
            <label class="sr" for="gl-email">Email</label><input id="gl-email" name="email" type="email" autocomplete="email" placeholder="Your email" required>
            <button class="btn" type="submit">Join the list</button>
          </div>
          <div class="hp" aria-hidden="true"><input name="website" tabindex="-1" autocomplete="off"></div>
          <p class="nl-status" role="status" aria-live="polite"></p>
        </form>
      </div>
    </div>
  </section>
'''

SIGNUP_JS = '''
<script>
document.querySelectorAll('form.su').forEach(function(f){var st=f.querySelector('.nl-status');
f.addEventListener('submit',async function(e){e.preventDefault();
if(!/^[^@\\s]+@[^@\\s]+\\.[^@\\s]+$/.test(f.email.value)){st.textContent='Please check your email address.';return}
var b=f.querySelector('button');b.disabled=true;
try{var r=await fetch('/api/subscribe',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({email:f.email.value,list:f.dataset.list,source:f.dataset.source,website:f.website.value})});if(!r.ok)throw 0;
st.innerHTML=f.dataset.list==='owner'?'Thank you. <a href="/owner-checklist">Open the checklist</a>.':'Thank you. You will hear from us first.';f.email.value='';}catch(_){st.textContent='Something went wrong. Please email casey@ophirstays.com.';}
b.disabled=false;});});
</script>'''

home = page('Ophir Stays · Durango Vacation Rental Management, Locally Owned',
            'A locally owned Durango vacation rental manager, capped at twenty-five homes. Founding owners keep 22% for life, with a written first-year guarantee. Guest booking opens in 2027.',
            '/', 'home', home_body, SIGNUP_JS, image=HERO_IMG)

checklist_body = '<section><div class="wrap narrow"><p class="eyebrow">For owners</p><h1 class="display">Seven things to check on your manager\'s statement</h1><hr class="rule" style="margin-left:0"><ol class="cklist">' + ''.join(f'<li><b>{t}</b> {d}</li>' for t, d in CHECKLIST) + '''</ol>
<p class="lead">Want a second opinion? Send us last year's statements and we will review them at no cost.</p>
<p style="margin-top:28px"><a class="btn btn-rust" href="/owners#estimate">Get a free estimate</a> &nbsp; <a class="link" href="mailto:casey@ophirstays.com">casey@ophirstays.com</a></p></div></section>'''
checklist_page = page("Seven Things to Check on Your Rental Manager's Statement · Ophir Stays",
                      "A one-page checklist for Durango vacation rental owners: fees, cleaning, repairs, pass-through charges, your calendar, event pricing and your contract.",
                      '/owner-checklist', 'owners', checklist_body)

# ---------------- OWNERS ----------------

FEATURE_OPTS = [('hot_tub','Hot tub'),('views','Mountain views'),('water','On the river or lake'),('ski_in','Ski-in, ski-out'),('gear','Garage or gear room'),('ac','Air conditioning'),('game','Game or media room'),('acreage','Private acreage'),('pets','Pet friendly')]
AREA_OPTS = [('downtown','Downtown Durango'),('valley','Animas Valley'),('purgatory','Purgatory and Durango Mountain'),('vallecito','Vallecito Lake and Bayfield'),('west','West of Durango (Hesperus, Lightner Creek)'),('east','East of Durango (Florida Road, Florida Mesa)'),('other','Somewhere else in La Plata County')]
ESTIMATE_FORM = f"""<form class="form" id="estimate-form" novalidate>
          <fieldset class="field full roles"><legend>I am</legend>
            <label class="chip"><input type="radio" name="role" value="owner" checked><span>The owner</span></label>
            <label class="chip"><input type="radio" name="role" value="agent"><span>A real estate agent</span></label>
            <label class="chip"><input type="radio" name="role" value="buyer"><span>Buying a home</span></label></fieldset>
          <div class="field"><label for="f-name">Your name</label><input id="f-name" name="name" autocomplete="name" required></div>
          <div class="field"><label for="f-email">Email</label><input id="f-email" name="email" type="email" autocomplete="email" required></div>
          <div class="field"><label for="f-phone">Phone</label><input id="f-phone" name="phone" type="tel" autocomplete="tel"></div>
          <div class="field agent-only"><label for="f-brk">Brokerage</label><input id="f-brk" name="brokerage" autocomplete="organization"></div>
          <div class="field agent-only"><label for="f-own">Owner's name</label><input id="f-own" name="owner_name"><span class="hint">Shown on the report.</span></div>
          <div class="field full"><label for="f-addr">Home address</label><input id="f-addr" name="address" autocomplete="street-address" required><span class="hint buyer-only">The home you're looking at, or paste the listing link.</span></div>
          <div class="field buyer-only"><label for="f-price">Asking price</label><input id="f-price" name="asking_price" inputmode="numeric" placeholder="e.g. $1,250,000"></div>
          <div class="field buyer-only"><label for="f-bagent">Your agent</label><input id="f-bagent" name="buyer_agent" placeholder="Optional"><span class="hint">We'll copy them if you like.</span></div>
          <div class="field"><label for="f-area">Area</label><select id="f-area" name="area">{''.join(f'<option value="{k}">{v}</option>' for k,v in AREA_OPTS)}</select></div>
          <div class="field"><label for="f-type">Type of home</label><select id="f-type" name="home_type"><option value="house">House</option><option value="cabin">Cabin</option><option value="townhome">Townhome</option><option value="condo">Condo</option></select></div>
          <div class="field"><label for="f-beds">Bedrooms</label><select id="f-beds" name="bedrooms" required><option value="">Select</option>{''.join(f'<option>{n}</option>' for n in range(1,9))}</select></div>
          <div class="field"><label for="f-baths">Bathrooms</label><input id="f-baths" name="baths" inputmode="decimal" placeholder="e.g. 3.5"></div>
          <div class="field"><label for="f-sleeps">Sleeps</label><input id="f-sleeps" name="sleeps" inputmode="numeric"></div>
          <div class="field"><label for="f-hoa">HOA</label><select id="f-hoa" name="hoa"><option value="">Not sure</option><option>No HOA</option><option>HOA allows nightly rentals</option><option>HOA restricts rentals</option></select></div>
          <fieldset class="field full"><legend>Features</legend><div class="chips">{''.join(f'<label class="chip"><input type="checkbox" name="features" value="{k}"><span>{v}</span></label>' for k,v in FEATURE_OPTS)}</div></fieldset>
          <div class="field"><label for="f-use">Rented now?</label><select id="f-use" name="current_use"><option value="">Select</option><option>Yes, I manage it myself</option><option>Yes, with a manager</option><option>Long-term rental</option><option>Not yet, personal use only</option></select></div>
          <div class="field"><label for="f-rev">Last 12 months' rent</label><input id="f-rev" name="current_rent" inputmode="numeric" placeholder="Optional"><span class="hint not-buyer">Sets the year-one guarantee baseline.</span><span class="hint buyer-only">The seller's numbers, if you have them.</span></div>
          <div class="field full"><label for="f-src">How did you hear about us?</label><input id="f-src" name="source" placeholder="A friend, an agent, a letter…"></div>
          <div class="field full"><label for="f-notes">Anything we should know?</label><textarea id="f-notes" name="notes"></textarea></div>
          <div class="hp" aria-hidden="true"><label for="f-web">Website</label><input id="f-web" name="website" tabindex="-1" autocomplete="off"></div>
          <button class="btn" type="submit">Send my request</button>
          <p class="form-status" role="status" aria-live="polite"></p>
        </form>"""

owners_body = f'''
  <section class="center" style="padding-bottom:56px">
    <div class="wrap narrow reveal">
      <p class="eyebrow">For homeowners</p>
      <h1 class="display">Your home, cared for like ours.</h1>
      <hr class="rule">
      <p class="lead">A small local manager, capped at twenty-five homes, with your first year's take-home guaranteed in writing.</p>
      <p style="margin-top:32px"><a class="btn btn-rust" href="#estimate">Get your free estimate</a></p>
    </div>
  </section>
  <div class="wrap">{photo('hero-fireplace', 'A great room with the fire lit and the chairs ready, in a mountain home cared for by Ophir')}</div>

  <section>
    <div class="wrap">
      <div class="reveal"><p class="eyebrow">How it works</p><h2 class="display">Four steps to your first guest.</h2></div>
      <ol class="steps reveal">
        <li><h3>Estimate</h3><p>Tell us about your home. Within two days you get a personal income estimate built from real Durango booking data.</p></li>
        <li><h3>Walkthrough</h3><p>We meet you at the house, or on a video call if you're out of state, and go through the standard together.</p></li>
        <li><h3>Ready</h3><p>Linens, photography, smart lock, gear room. We handle every item on the list and send you one bill.</p></li>
        <li><h3>Live</h3><p>Your home goes live. Every month you get a report: income, reviews, photos after each clean, and anything we fixed.</p></li>
      </ol>
    </div>
  </section>

  <section class="tint" id="guarantee">
    <div class="wrap split top">
      <div class="reveal">
        <p class="eyebrow">The guarantee</p>
        <h2 class="display">You keep more than last year, or we refund the difference.</h2>
        <p class="lead">If you take home less in your first twelve months with Ophir than in the twelve months before, we refund the difference, up to the full management fee we earned that year.</p>
      </div>
      <div class="reveal">
        <table class="terms">
          <tr><th scope="row">Who qualifies</th><td>Homes with at least twelve months of rental history we can see: Airbnb, VRBO or prior manager statements.</td></tr>
          <tr><th scope="row">Your baseline</th><td>Your take-home for the twelve months before you sign: nightly rent minus your old manager's fee, or the full rent if you managed it yourself. Cleaning fees, pet fees and taxes are excluded from both years.</td></tr>
          <tr><th scope="row">Example</th><td>Last year: $100,000 in rent at a 30% manager, so you kept $70,000. With Ophir at 22%, the same home only has to earn $89,800 for you to keep as much.</td></tr>
          <tr><th scope="row">Your own stays</th><td>Nights you block for yourself lower the baseline rent by that year's average nightly rate.</td></tr>
          <tr><th scope="row">Pricing</th><td>We set nightly rates and minimum stays. Nights you hold above our rate aren't covered.</td></tr>
          <tr><th scope="row">Not covered</th><td>Closures no one controls: wildfire or road closures, government orders, damage that keeps the home offline more than seven days.</td></tr>
          <tr><th scope="row">How it pays</th><td>We compare at month twelve and pay within thirty days.</td></tr>
          <tr><th scope="row">Leaving</th><td>Thirty days' notice, either way, no penalty.</td></tr>
        </table>
        <p class="fine">Summary only. Full terms are in the owner agreement.</p>
      </div>
    </div>
  </section>

  <section>
    <div class="wrap">
      <div class="reveal"><p class="eyebrow">Our promises</p><h2 class="display">What we put in writing.</h2></div>
      <div class="details four reveal">
        <div><span class="ital">i.</span><h3>Damage, covered</h3><p>Every guest pays a damage waiver. It covers your home up to $2,500 a stay, and you never file a claim.</p></div>
        <div><span class="ital">ii.</span><h3>Small fixes, included</h3><p>Bulbs, batteries, filters, a loose handle: fixed and never billed. Bigger repairs are billed at cost, with no markup and with photos, and nothing over $300 happens without your yes.</p></div>
        <div><span class="ital">iii.</span><h3>A local who answers</h3><p>You and your guests text Casey directly, 7am to 10pm. Urgent problems get a response any hour, and someone local comes to the house.</p></div>
        <div><span class="ital">iv.</span><h3>Priced every day</h3><p>Nightly rates move daily with the season, events and demand, set by live Durango data and checked by someone who lives here.</p></div>
      </div>
      <p class="fine reveal" style="margin-top:28px">Every stay in your home also gives $10 to Durango: our trails, adaptive skiing at Purgatory, and local housing. It comes from our fee, never yours. <a href="/about#give">How we give back</a>.</p>
    </div>
  </section>

  <section>
    <div class="wrap split top">
      <div class="reveal">
        <p class="eyebrow">The standard</p>
        <h2 class="display">What every home in the Collection has.</h2>
        <p class="lead">If your home falls short, we send you the list of what to fix. Often it's a weekend's work, and we can arrange it.</p>
      </div>
      <ul class="standard reveal">
        <li>Professional photography</li><li>Hotel-grade mattresses and white linens</li><li>A hot tub or a real view</li>
        <li>Room for gear: bikes, skis and boots</li><li>Fast Wi-Fi and a smart lock</li><li>A kitchen stocked for a real dinner</li>
        <li>No deferred maintenance</li><li>Within 45 minutes of town or Purgatory</li><li>Permitted for short-term rental</li>
      </ul>
    </div>
  </section>

  <section class="tint">
    <div class="wrap split">
      <div class="reveal">
        <p class="eyebrow">Your owner report</p>
        <h2 class="display">Know exactly how your home is doing.</h2>
        <p class="lead">Every month, in the app and in your inbox: income against last year, every review word for word, photos after every clean, and anything we fixed, with the receipt.</p>
      </div>
      <div class="reveal">
        <div class="report" role="img" aria-label="Sample owner report: July income $11,840, up 18 percent on last year, 26 nights booked, 4.97 guest rating">
          <div class="report-head"><div><small>OWNER REPORT · JULY</small><div style="font-size:18px;margin-top:4px">The Glacier Cliff Home</div></div><svg aria-hidden="true"><use href="#summit"/></svg></div>
          <div class="report-body">
            <span class="sample-tag">SAMPLE</span>
            <div class="kpis"><div class="kpi"><b>$11,840</b><span>Income <span class="up">+18%</span></span></div><div class="kpi"><b>26</b><span>Nights booked</span></div><div class="kpi"><b>4.97</b><span>Guest rating</span></div></div>
            <div class="legend"><span><i style="background:#CFC3AC"></i>Last year</span><span><i style="background:#B4572B"></i>With Ophir</span></div>
            <div class="bars" aria-hidden="true"><div><i style="height:52%"></i><i style="height:58%"></i></div><div><i style="height:40%"></i><i style="height:49%"></i></div><div><i style="height:61%"></i><i style="height:70%"></i></div><div><i style="height:78%"></i><i style="height:92%"></i></div></div>
            <div class="bar-labels" aria-hidden="true"><span>Apr</span><span>May</span><span>Jun</span><span>Jul</span></div>
            <div class="log"><p><span>Hot tub cover latch replaced</span><span>$85 · Jul 9</span></p><p><span>"Best trip our family has taken." · 5★</span><span>Jul 21</span></p><p><span>Turnover photos, 6 cleans</span><span>View all</span></p></div>
          </div>
        </div>
      </div>
    </div>
  </section>

  <section>
    <div class="wrap center">
      <div class="reveal"><p class="eyebrow">Pricing</p><h2 class="display">One fee. No surprises.</h2></div>
      <div class="price reveal">
        <div><b>22%</b><span>Founding rate for the first ten homes, locked for as long as you stay. 25% after. Everything included: pricing, guests, cleaning, photography, trip planning and your monthly report.</span></div>
        <div><b>$0</b><span>to join. Readiness work is quoted up front and billed at cost.</span></div>
        <div><b>30 days</b><span>notice to leave, either way. No long contracts.</span></div>
      </div>
      <div class="reveal" style="max-width:980px;margin:56px auto 0;text-align:left">
        <p class="eyebrow" style="text-align:center">How we compare</p>
        <h2 class="display" style="text-align:center;margin-bottom:28px">Ophir, on your own, or a large manager</h2>
        <table class="compare"><thead><tr><th scope="col"></th><th scope="col" class="us">Ophir</th><th scope="col">On your own</th><th scope="col">Large managers</th></tr></thead><tbody><tr><th scope="row">Fee</th><td class="us" data-l="Ophir">22% founding rate, all in</td><td data-l="On your own">0%, plus your time</td><td data-l="Large managers">Typically 25 to 40%, plus add-on fees</td></tr><tr><th scope="row">Hidden fees</th><td class="us" data-l="Ophir">None. Repairs at cost.</td><td data-l="On your own">None</td><td data-l="Large managers">Linen, setup, card and repair markups are common</td></tr><tr><th scope="row">Year-one guarantee</th><td class="us" data-l="Ophir">Yes, up to our fee</td><td data-l="On your own">No</td><td data-l="Large managers">Rarely</td></tr><tr><th scope="row">Contract</th><td class="us" data-l="Ophir">30 days’ notice</td><td data-l="On your own">None</td><td data-l="Large managers">Often 12 months, sometimes with an exit fee</td></tr><tr><th scope="row">Who answers</th><td class="us" data-l="Ophir">Casey, a 23-year local</td><td data-l="On your own">You, at 2am</td><td data-l="Large managers">A call center or a rotating team</td></tr><tr><th scope="row">Homes per manager</th><td class="us" data-l="Ophir">25, at most</td><td data-l="On your own">1</td><td data-l="Large managers">Hundreds</td></tr><tr><th scope="row">Trip planning for guests</th><td class="us" data-l="Ophir">Every stay</td><td data-l="On your own">No</td><td data-l="Large managers">Rarely</td></tr><tr><th scope="row">Pricing</th><td class="us" data-l="Ophir">Set daily, by season and event</td><td data-l="On your own">Usually set once</td><td data-l="Large managers">Software, set by region</td></tr></tbody></table>
        <p class="fine" style="margin-top:12px">Large managers means national and regional companies with hundreds of homes. Terms vary by company and contract; ask yours for a full fee schedule.</p>
      </div>
    </div>
  </section>

  <section id="basecamp">
    <div class="wrap split top">
      <div class="reveal">
        <p class="eyebrow">Now seeking five Basecamp homes</p>
        <h2 class="display">Guests for the weeks that sit empty.</h2>
        <p class="lead">Most Durango homes go quiet in May and October. Basecamp books riders, training camps and race-week athletes into exactly those weeks. We plan their routes, stock their fuel and book their shuttles and guides, so they stay longer and come back.</p>
        <p class="lead">It's part of the Ophir service, at no extra cost to you. We're choosing the first five homes now.</p>
        <p class="eyebrow" style="margin:32px 0 14px">Your home likely qualifies if it has</p>
        <ul class="standard">
          <li>A garage or locked bike storage</li><li>A hose or wash station</li><li>A mudroom or gear room</li><li>A spot in Durango, the Animas Valley, Hermosa or up toward Purgatory</li>
        </ul>
        <p class="fine" style="margin-top:14px">Missing a stand, a pump or a bike rack? We source them at cost, usually $300 to $600.</p>
        <p style="margin-top:18px"><a class="link" href="/basecamp">See Basecamp as guests see it</a></p>
      </div>
      <div class="reveal" id="bco-box">
        <h3 style="margin-bottom:18px">Think your home qualifies? Send us a message.</h3>
        <form class="form" id="bco-form" novalidate>
          <div class="field"><label for="o-name">Your name</label><input id="o-name" name="name" autocomplete="name" required></div>
          <div class="field"><label for="o-email">Email</label><input id="o-email" name="email" type="email" autocomplete="email" required></div>
          <div class="field"><label for="o-phone">Phone</label><input id="o-phone" name="phone" type="tel" autocomplete="tel"></div>
          <div class="field"><label for="o-beds">Bedrooms</label><select id="o-beds" name="bedrooms"><option>2</option><option selected>3</option><option>4</option><option>5</option><option>6 or more</option></select></div>
          <div class="field full"><label for="o-addr">Home address or neighborhood</label><input id="o-addr" name="address" required></div>
          <fieldset class="field full roles"><legend>It has</legend>
            <label class="chip"><input type="checkbox" name="has" value="garage"><span>Garage or bike storage</span></label>
            <label class="chip"><input type="checkbox" name="has" value="wash"><span>Hose or wash station</span></label>
            <label class="chip"><input type="checkbox" name="has" value="gear room"><span>Mudroom or gear room</span></label>
            <label class="chip"><input type="checkbox" name="has" value="room for a group"><span>Sleeps 6 or more</span></label></fieldset>
          <div class="field full"><label for="o-notes">Message</label><textarea id="o-notes" name="notes" placeholder="Who manages it now, and anything we should know"></textarea></div>
          <div class="hp" aria-hidden="true"><input name="website" tabindex="-1" autocomplete="off"></div>
          <div class="field full"><button class="btn btn-rust" type="submit">Send my home</button><p class="form-status" role="status" aria-live="polite"></p></div>
        </form>
        <div class="thanks" tabindex="-1"><h3>Thank you.</h3><p style="color:var(--muted);margin-top:8px">Casey will call you within a day to talk about your home.</p></div>
      </div>
    </div>
  </section>

  <section class="tint" id="estimate">
    <div class="wrap split top">
      <div class="reveal">
        <p class="eyebrow">Free estimate</p>
        <h2 class="display">What could your home earn?</h2>
        <p class="lead">Tell us about your home. Within 24 hours you get a three-page report: expected rent month by month, what you keep after every cost, comparable homes and our terms. Free, with no obligation.</p>
        <p class="fine" style="margin-top:16px"><a href="/assets/ophir-earnings-estimate-sample.pdf">See a sample report</a></p>
        <p class="fine" style="margin-top:28px">Prefer to talk? <a href="mailto:casey@ophirstays.com">casey@ophirstays.com</a></p>
        <p class="fine" style="margin-top:12px">Before you apply: <a href="/journal/durango-home-earnings">what a Durango vacation home earns</a> and <a href="/journal/durango-short-term-rental-rules">the city and county rental rules</a>. Own nearby? <a href="/areas/purgatory">Purgatory</a> · <a href="/areas/cascade">Cascade Village</a> · <a href="/areas/hermosa">Hermosa</a> · <a href="/areas/animas-valley">Animas Valley</a>. Switching? <a href="/journal/switch-rental-managers-durango">How to switch managers</a>.</p>
      </div>
      <div class="reveal" id="estimate-box">
        {ESTIMATE_FORM}
        <div class="thanks" tabindex="-1"><svg aria-hidden="true"><use href="#summit"/></svg><h3>Thank you. We have your request.</h3><p style="color:var(--muted);margin:12px 0 0">Casey will check the numbers and email your report within 24 hours.</p></div>
      </div>
    </div>
  </section>

  <section>
    <div class="wrap narrow">
      <p class="eyebrow">Questions</p>
      <h2 class="display" style="margin-bottom:24px">Before you apply.</h2>
      <div class="faq">
        <details><summary>I already have a manager. Can I switch?</summary><p>Yes, and we do the work. We read your current agreement, draft the notice for you to sign, and start the day after the last stay your manager keeps. Every booking that moves to us is honored at the same dates and price. Send us last year's owner statements and we'll show you, line by line, what you'd have kept with Ophir.</p></details>
        <details><summary>What if my contract has an exit fee?</summary><p>We cover it, up to $1,000, as a credit against our fees. You shouldn't pay a penalty to get better care for your home.</p></details>
        <details><summary>Can I still use my home?</summary><p>Of course. Block your dates in the app any time. Your own nights simply lower the guarantee baseline, so the comparison stays fair.</p></details>
        <details><summary>Where do you list my home?</summary><p>On Airbnb and VRBO, and on ophirstays.com, where returning guests book direct. Direct bookings skip platform fees, which means more for you.</p></details>
        <details><summary>Who cleans and maintains it?</summary><p>Local crews we've known for years, inspected after every clean. Small fixes are included. Nothing over $300 happens without your approval.</p></details>
        <details><summary>Why only twenty-five homes?</summary><p>Because the service only works if we know every home personally. When the Collection is full, new owners join a waiting list.</p></details>
      </div>
    </div>
  </section>
'''

FORM_JS = '''
<script>
(function(){
  var f=document.getElementById('estimate-form'),box=document.getElementById('estimate-box'),st=f.querySelector('.form-status');
  var setRole=function(){var v=f.role.value;f.querySelectorAll('.agent-only').forEach(function(el){el.hidden=v!=='agent'});f.querySelectorAll('.buyer-only').forEach(function(el){el.hidden=v!=='buyer'});f.querySelectorAll('.not-buyer').forEach(function(el){el.hidden=v==='buyer'})};[].forEach.call(f.role,function(r){r.onchange=setRole});
  var q=new URLSearchParams(location.search),r0=q.get('role')||f.dataset.role;if(r0==='agent'||r0==='buyer')f.role.value=r0;setRole();
  f.addEventListener('submit',async function(e){
    e.preventDefault();st.className='form-status';
    var miss=[].filter.call(f.querySelectorAll('[required]'),function(i){return !i.value.trim()});
    if(miss.length){st.textContent='Please fill in your name, email, the home address and bedrooms.';st.classList.add('err');miss[0].focus();return}
    if(!/^[^@\\s]+@[^@\\s]+\\.[^@\\s]+$/.test(f.email.value)){st.textContent='Please check your email address.';st.classList.add('err');f.email.focus();return}
    var btn=f.querySelector('button');btn.disabled=true;btn.textContent='Sending…';
    try{
      var fd=new FormData(f),o=Object.fromEntries(fd);o.features=fd.getAll('features');var r=await fetch('/api/estimate',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify(o)});
      if(!r.ok)throw 0;
      box.classList.add('sent');box.querySelector('.thanks').focus();
    }catch(_){
      st.textContent='Something went wrong. Please email casey@ophirstays.com and we\\'ll reply today.';st.classList.add('err');
      btn.disabled=false;btn.textContent='Send my request';
    }
  });
})();
</script>'''

import re as _re, html as _html
_faq = [(_html.unescape(_re.sub('<[^>]+>','',q)).strip(), _html.unescape(_re.sub('<[^>]+>','',x)).strip()) for q,x in _re.findall(r'<details><summary>(.*?)</summary><p>(.*?)</p></details>', owners_body, _re.S)]
POST_LD['/owners'] = '<script type="application/ld+json">' + _json.dumps({"@context":"https://schema.org","@graph":[
  {"@type":"ProfessionalService","name":"Ophir Stays","url":"https://ophirstays.com/owners","description":"Locally owned Durango vacation rental management: pricing, guests, cleaning, trip planning and a first-year income guarantee, for no more than 25 homes.","email":"casey@ophirstays.com","telephone":"+1-970-779-8992","address":{"@type":"PostalAddress","addressLocality":"Durango","addressRegion":"CO","postalCode":"81301","addressCountry":"US"},"areaServed":["Durango, CO","Purgatory, CO","Vallecito Lake, CO","La Plata County, CO"],"serviceType":"Vacation rental management","founder":{"@type":"Person","name":"Casey Roberts"}},
  {"@type":"FAQPage","mainEntity":[{"@type":"Question","name":q,"acceptedAnswer":{"@type":"Answer","text":x}} for q,x in _faq]}]}) + '</script>'

OWNER_BC_JS = '''
<script>
(function(){
  var f=document.getElementById('bco-form');if(!f)return;var st=f.querySelector('.form-status');
  f.addEventListener('submit',async function(e){
    e.preventDefault();st.className='form-status';
    var miss=[].filter.call(f.querySelectorAll('[required]'),function(i){return !i.value.trim()});
    if(miss.length){st.textContent='Please add your name, email and the home.';st.classList.add('err');miss[0].focus();return}
    if(!/^[^@\\s]+@[^@\\s]+\\.[^@\\s]+$/.test(f.email.value)){st.textContent='Please check your email address.';st.classList.add('err');f.email.focus();return}
    var btn=f.querySelector('button');btn.disabled=true;btn.textContent='Sending…';
    try{var fd=new FormData(f),o=Object.fromEntries(fd);o.has=fd.getAll('has');o.kind='owner';
      var r=await fetch('/api/basecamp',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify(o)});if(!r.ok)throw 0;
      var bx=document.getElementById('bco-box');bx.classList.add('sent');bx.querySelector('.thanks').focus();
    }catch(_){st.textContent='Something went wrong. Please email casey@ophirstays.com.';st.classList.add('err');btn.disabled=false;btn.textContent='Send my home'}
  });
})();
</script>'''
owners = page('Durango Vacation Rental Management · Ophir Stays',
              'Apply to the Ophir Collection: twenty-five Durango homes, one standard, and a first-year income guarantee. Get a free estimate of what your home could earn.',
              '/owners', 'owners', owners_body, FORM_JS + OWNER_BC_JS)


# ---------------- YOUR STAY (packages) ----------------
TIERS = [
  dict(name='The Stay', price='Included', unit='with every booking', lead='A beautiful home, kept to our standard, with a local on call.',
       items=['Home inspected before every arrival', 'Hotel-grade linens, robes and toiletries', 'A welcome kit: local coffee, chocolate and a card with our favorite spots',
              'Door code and house guide in the app', 'Weather-aware ideas for every day', 'A local host by text, 7am to 10pm. Urgent issues any hour']),
  dict(name='The Arranged Stay', price='$395', unit='per stay, up to 6 guests', lead='Tell us what you love. We plan the trip around it.', feature=True,
       items=['Everything in The Stay', 'Two Ophir tumblers to keep', 'A planning call before you arrive', 'Skis and boots sized to each guest and waiting in the gear room (rental extra)',
              'Bikes fitted to each rider and delivered (rental extra)', 'Lift tickets, guides, rafting and fly fishing booked (paid at partner rates)',
              'Dinner reservations held, first round on the house at our partner restaurants', 'Your itinerary in the app, moved when the weather moves'], note='Groups of 7 to 12: $595. The planning fee covers our work. Rentals, tickets and guides are paid separately, at our partners\u2019 rates.'),
  dict(name='The Private Stay', price='$1,950', unit='per stay, up to five nights', lead='A dedicated host. Nothing left for you to do.',
       items=['Everything in The Arranged Stay', 'Groceries shopped and the fridge stocked to your list (groceries at cost)', 'Fire laid, wine chosen, music on when you walk in',
              'Your own host, on call for the whole stay', 'Private chef, in-home massage or a sitter booked for you (their fee extra)',
              'Airport transfer booked (fare extra)', 'Mid-stay refresh: linens, towels, restock', 'Longer stays: $295 per additional night'], note='We book everything. You pay the chef, therapist, sitter, driver, rentals and groceries directly at their rates, in the app.'),
]
def tier_html(t):
    items=''.join(f'<li>{i}</li>' for i in t['items'])
    cls=' tier-feature' if t.get('feature') else ''
    return f'''<div class="tier{cls} reveal"><p class="eyebrow" style="margin-bottom:10px">{t['name']}</p>
        <div class="tier-price"><b>{t['price']}</b><span>{t['unit']}</span></div><p class="tier-lead">{t['lead']}</p><ul class="tier-list">{items}</ul>{f'<p class="tier-note">{t["note"]}</p>' if t.get('note') else ''}</div>'''

TIMELINE = [('30 days before', 'Tell us what you love', 'Skiing, riding, the river, a slow morning with good coffee. A short form in the app, or a call with your host.'),
            ('14 days before', 'Sizes and lists', 'Heights, boot sizes and riding styles for everyone in the party. Your grocery list, dietary needs and how you take your coffee.'),
            ('7 days before', 'Your itinerary', 'Every day planned and built around the forecast: tickets, tee times, guides and tables confirmed.'),
            ('Arrival day', 'Walk in', 'The fire is laid and the fridge is stocked. Skis, boots and bikes wait in the gear room, each labeled with a name. Your door code arrives at four.'),
            ('During your stay', 'We adjust', 'Storms coming in? Your ride moves to tomorrow and we suggest the hot springs. Text us anything, any time.'),
            ('After you leave', 'We remember', 'Your sizes, your coffee and your favorite table, saved for next time.')]
timeline = ''.join(f'<li class="reveal"><span class="when">{w}</span><div><h3>{h}</h3><p>{p}</p></div></li>' for w,h,p in TIMELINE)

stay_body = f'''
  <section class="center" style="padding-bottom:56px">
    <div class="wrap narrow reveal">
      <p class="eyebrow">Your Stay</p>
      <h1 class="display">We plan everything. You arrive.</h1>
      <hr class="rule">
      <p class="lead">Skis and boots in your size, bikes fitted, the fridge stocked and every table booked, before you land.</p>
    </div>
  </section>
  <div class="wrap">{photo('hero-fireplace', 'A great room with the fire lit at dusk, ready for arrival')}</div>

  <section>
    <div class="wrap">
      <div class="center reveal" style="margin-bottom:48px"><p class="eyebrow">The details</p><h2 class="display">How a stay unfolds</h2></div>
      <ol class="timeline">{timeline}</ol>
    </div>
  </section>

  <section class="tint" id="packages">
    <div class="wrap">
      <div class="center reveal" style="margin-bottom:52px">
        <p class="eyebrow">Packages</p>
        <h2 class="display">Choose how much we handle.</h2>
        <hr class="rule">
        <p class="lead">Every stay starts with the home. Add as much of the trip as you like, and upgrade any time before you arrive.</p>
      </div>
      <div class="tiers">{''.join(tier_html(t) for t in TIERS)}</div>
      <div class="addons reveal">
        <p class="eyebrow" style="text-align:center">Or add a single touch to any stay</p>
        <div class="addon-row">
          <div><b>Fridge stocked</b><span>$95 plus groceries</span></div>
          <div><b>Arrival setup</b><span>Fire laid, wine chosen, flowers · $95 plus wine</span></div>
          <div><b>Skis or bikes fitted and delivered</b><span>Delivery and pickup · $95 for up to 4, $20 each after, plus rental</span></div>
          <div><b>Mid-stay clean</b><span>Fresh linens, full clean, restock · $195</span></div>
          <div><b>Early check-in or late checkout</b><span>When the calendar allows · $95 each</span></div>
        </div>
      </div>
      <p class="fine center" style="margin-top:28px"><b>How it works:</b> package prices cover our planning, booking and hosting. Rentals, lift tickets, guides, chefs, massage, transport and groceries are paid separately at our partners' rates, with no markup to you. You see every price and confirm it in the app before anything is charged.</p>
    </div>
  </section>

  <section style="padding:40px 0">
    <div class="wrap narrow center reveal">
      <p class="eyebrow">Coming to ride or ski hard?</p>
      <p class="lead" style="margin-top:10px">Basecamp plans the San Juan high country for your group: routes, shuttles, fuel and repairs. <a class="link" href="/basecamp">See Basecamp</a></p>
    </div>
  </section>

  
  <section>
    <div class="wrap split">
      <div class="reveal">{photo('ski', 'Wooden skis against a cabin wall')}</div>
      <div class="reveal">
        <p class="eyebrow">Attention to detail</p>
        <h2 class="display">The small things are the whole thing.</h2>
        <ul class="standard" style="columns:1;margin-top:24px">
          <li>Tomorrow's snow report texted to you the night before</li>
          <li>Each guest's gear labeled with their name</li>
          <li>Your coffee order, already in the kitchen</li>
          <li>Kids' bikes and helmets in the right sizes</li>
          <li>A <a href="/trail-map">trail map</a> marked with the ride we planned for you</li>
          <li>Every preference remembered for your next stay</li>
        </ul>
      </div>
    </div>
  </section>

  <section class="tint center">
    <div class="wrap narrow">
      <p class="eyebrow reveal">Guest booking opens 2027</p>
      <h2 class="display reveal">Be first for the best dates.</h2>
      <p class="lead reveal">Tell us when you'd like to come, and we'll hold the first look at our homes for you.</p>
      <p class="reveal" style="margin-top:32px"><a class="btn btn-rust" href="mailto:casey@ophirstays.com?subject=First%20dates%20at%20Ophir%20Stays">Request first dates</a></p>
    </div>
  </section>
'''
stay_page = page('Durango Trip Planning, Ski and Bike Concierge · Ophir Stays',
                 'Skis and boots sized and waiting, bikes fitted, the fridge stocked and every table booked before you arrive. Ophir Stays packages for Durango, Colorado.',
                 '/stay', 'stay', stay_body)


# ---------------- BASECAMP ----------------
basecamp_body = f'''
  <section class="center" style="padding-bottom:48px">
    <div class="wrap narrow reveal">
      <p class="eyebrow">Ophir Basecamp</p>
      <h1 class="display">Come to ride. We handle everything else.</h1>
      <hr class="rule">
      <p class="lead">A home built for riders and skiers, and a local who plans the routes, books the shuttles, stocks the fuel and fixes what breaks. You bring the legs.</p>
      <p style="margin-top:28px;display:flex;gap:12px;justify-content:center;flex-wrap:wrap"><a class="btn btn-rust" href="#inquire">Plan a trip</a> <a class="btn" href="#rides">See the rides</a></p>
      <p class="fine">Basecamp opens for summer 2027. Tell us your trip now and we'll plan it with you.</p>
    </div>
  </section>

  <section style="padding:0 0 clamp(48px,6vw,88px)">
    <div class="wrap reveal"><div class="photo wide"><img src="/assets/photos/library/high-country-crew.jpg" alt="Four riders crossing golden tundra toward red and orange San Juan peaks" loading="lazy"></div></div>
  </section>

  <section style="padding-top:0">
    <div class="wrap split">
      <div class="reveal"><div class="photo tall"><video class="bg-video" src="/assets/video/lizard-head-pan.mp4" poster="/assets/video/lizard-head-pan.jpg" autoplay muted loop playsinline preload="metadata" aria-label="Pan from Lizard Head across fall high country to a parked bike and the San Juan peaks"></video></div></div>
      <div class="reveal">
        <p class="eyebrow">What Basecamp handles</p>
        <h2 class="display">Every day planned around your riders.</h2>
        <ul class="standard" style="grid-template-columns:1fr;margin-top:28px">
          <li>Routes matched to each rider, with GPX files before you arrive</li>
          <li>Shuttles booked with licensed local shuttle companies</li>
          <li>Tailwind and recovery basics stocked for every rider</li>
          <li>Bikes or skis fitted and delivered, mechanical help the same day</li>
          <li>A conditions text by 7am, and plans that move with the weather</li>
          <li>If someone gets hurt, we get the bike to the shop and rearrange the rest of the trip</li>
        </ul>
        <p class="fine">Basecamp homes have a garage or locked bike storage, a wash station and a gear room, in town, the Animas Valley or up toward Purgatory.</p>
      </div>
    </div>
  </section>

  <section class="tint" id="rides">
    <div class="wrap" style="max-width:980px">
      <div class="reveal center"><p class="eyebrow">The high country</p><h2 class="display">The San Juan rides we plan.</h2>
      <p class="lead" style="margin:18px auto 0;max-width:640px">Above 10,000 feet, from Coal Bank and Molas Pass. Ridden from mid-July to early October, started early, off the ridges by noon.</p></div>
      <table class="data wrap rides reveal" style="margin-top:36px"><thead><tr><th scope="col">Ride</th><th scope="col">Miles</th><th scope="col">Climbing</th><th scope="col">High point</th><th scope="col">Shuttle</th></tr></thead><tbody><tr><th scope="row"><a class="link" href="/trails/pass-creek-coal-creek">Pass Creek to Coal Creek</a></th><td>7.8</td><td>1,714 ft</td><td>11,884 ft</td><td>No, loop</td></tr><tr><th scope="row"><a class="link" href="/trails/pass-creek-engineer-cascade">Engineer Mountain Trail from Pass Creek</a></th><td>8.2</td><td>1,083 ft</td><td>11,731 ft</td><td>Yes</td></tr><tr><th scope="row"><a class="link" href="/trails/deer-creek">Deer Creek</a></th><td>8.6</td><td>1,558 ft</td><td>11,931 ft</td><td>Yes</td></tr><tr><th scope="row"><a class="link" href="/trails/engine-creek">Engine Creek</a></th><td>13.2</td><td>1,649 ft</td><td>11,802 ft</td><td>Yes</td></tr><tr><th scope="row"><a class="link" href="/trails/little-molas-engineer-cascade">Little Molas to Engineer Mountain</a></th><td>17.9</td><td>2,449 ft</td><td>12,190 ft</td><td>Yes</td></tr><tr><th scope="row"><a class="link" href="/trails/blackhawk-loop">Blackhawk Pass Loop</a></th><td>25.7</td><td>3,901 ft</td><td>11,992 ft</td><td>No, loop</td></tr><tr><th scope="row"><a class="link" href="/trails/little-molas-hermosa-corral-draw">Colorado Trail: Little Molas to Hermosa</a></th><td>52.7</td><td>6,675 ft</td><td>12,494 ft</td><td>Yes</td></tr></tbody></table>
      <div class="grid3 reveal" style="margin-top:36px">
        <div class="photo"><img src="/assets/photos/library/ridge-crew.jpg" alt="A rider descending a golden ridge as three others crest behind" loading="lazy"></div>
        <div class="photo"><img src="/assets/photos/library/engineer-climb.jpg" alt="A rider climbing meadow singletrack toward Engineer Mountain" loading="lazy"></div>
        <div class="photo"><img src="/assets/photos/library/scree-traverse.jpg" alt="A rider on red-dirt singletrack beside a huge scree slope" loading="lazy"></div>
      </div>
      <p class="fine">Closer to town: <a class="link" href="/trails">ten Durango rides</a> for arrival day and rest days. Trail data © OpenStreetMap contributors.</p>
    </div>
  </section>

  <section>
    <div class="wrap split">
      <div class="reveal">
        <p class="eyebrow">A sample week</p>
        <h2 class="display">Five days in July.</h2>
        <ol class="days" style="list-style:none;padding:0;margin:28px 0 0">
          <li><b>Day 1</b> Arrive, spin Telegraph and Sidewinder in town. 8.6 miles at 6,600 feet to settle in.</li>
          <li><b>Day 2</b> Pass Creek to Coal Creek from Coal Bank Pass. 7.8 miles, 1,700 feet, back to the car.</li>
          <li><b>Day 3</b> Engine Creek. 13 miles, mostly down, shuttle back from Cascade.</li>
          <li><b>Day 4</b> Rest. The river, a massage, an early dinner.</li>
          <li><b>Day 5</b> Little Molas to Engineer Mountain. 18 miles, 12,190 feet high, shuttled to Molas Pass.</li>
        </ol>
        <p class="fine">Every plan moves with the forecast and the group. Riders new to altitude start lower.</p>
      </div>
      <div class="reveal"><div class="photo tall"><video class="bg-video" src="/assets/video/tundra-ride.mp4" poster="/assets/video/tundra-ride.jpg" autoplay muted loop playsinline preload="metadata" aria-label="Red-dirt tundra ridge under blue sky with the Needle Mountains on the horizon"></video></div></div><script>if(matchMedia('(prefers-reduced-motion:reduce)').matches){{document.querySelectorAll('.bg-video').forEach(function(v){{v.removeAttribute('autoplay');v.pause();}});}}</script>
    </div>
  </section>

  <section class="tint">
    <div class="wrap">
      <div class="reveal center"><p class="eyebrow">Who it's for</p><h2 class="display">Built for groups who come to move.</h2></div>
      <div class="grid3" style="margin-top:44px">
        <div class="reveal">{photo('basecamp-trail', 'Singletrack across a green alpine meadow toward Engineer Mountain')}<h3 style="margin-top:18px">Bike trip crews</h3><p style="color:var(--muted);margin-top:8px">Four to eight riders, four to seven nights. Spring in the desert-edge trails, summer up high, fall in the aspens.</p></div>
        <div class="reveal">{photo('basecamp-notch', 'A rocky notch high in the San Juans looking down a forested valley')}<h3 style="margin-top:18px">Training camps</h3><p style="color:var(--muted);margin-top:8px">Clubs and teams training at altitude. A quiet house, big volume, fuel and recovery handled.</p></div>
        <div class="reveal"><div class="photo"><img src="/assets/photos/basecamp-backcountry.jpg" alt="Four backcountry skiers skinning across a meadow beneath snow-covered San Juan peaks" loading="lazy"></div><h3 style="margin-top:18px">Guided backcountry skiing</h3><p style="color:var(--muted);margin-top:8px">San Juan powder, always with certified, permitted mountain guides. Purgatory on the rest days, skis tuned and boots dry.</p></div>
      </div>
    </div>
  </section>

  <section style="padding:44px 0;background:var(--charcoal);color:#ECE4D3">
    <div class="wrap narrow center reveal">
      <p class="eyebrow" style="color:#E08A5C">For owners</p>
      <p class="lead" style="color:#ECE4D3;margin-top:10px">Own a home in town, the Animas Valley or up toward Purgatory? We're seeking five Basecamp homes for 2027. <a class="link" style="color:#fff" href="/owners#basecamp">See if yours qualifies</a></p>
    </div>
  </section>

  <section>
    <div class="wrap narrow center reveal">
      <p class="eyebrow">Pricing</p>
      <h2 class="display">$495 a stay.</h2>
      <p class="lead" style="margin-top:18px">For up to six guests. $795 for seven to twelve. Training camps of a week or more are quoted to the group.</p>
      <p class="fine">Shuttles, guides, rentals and lift tickets are booked at the partner's own rate, with no markup. Guided rides and backcountry days are led by permitted, certified guide services.</p>
    </div>
  </section>

  <section class="tint" id="inquire">
    <div class="wrap split top">
      <div class="reveal">
        <p class="eyebrow">Plan a trip</p>
        <h2 class="display">Tell us about your group.</h2>
        <p class="lead">Casey reads every one and replies within a day with a first plan and the homes that fit.</p>
        <p class="fine">Spring and fall camps fill first. Most groups book three months ahead.</p>
      </div>
      <div class="reveal" id="bc-box">
        <form class="form" id="bc-form" novalidate>
          <div class="field"><label for="b-name">Your name</label><input id="b-name" name="name" autocomplete="name" required></div>
          <div class="field"><label for="b-email">Email</label><input id="b-email" name="email" type="email" autocomplete="email" required></div>
          <div class="field"><label for="b-phone">Phone</label><input id="b-phone" name="phone" type="tel" autocomplete="tel"></div>
          <div class="field"><label for="b-type">The trip</label><select id="b-type" name="trip_type"><option value="bike">Bike trip</option><option value="camp">Training camp</option><option value="iron_horse">Iron Horse week</option><option value="ski">Ski trip</option><option value="other">Something else</option></select></div>
          <div class="field"><label for="b-size">Group size</label><select id="b-size" name="group_size"><option>2 to 4</option><option selected>5 to 8</option><option>9 to 12</option><option>13 or more</option></select></div>
          <div class="field"><label for="b-level">Riding level</label><select id="b-level" name="level"><option value="mixed">Mixed</option><option value="intermediate">Intermediate</option><option value="advanced">Advanced</option><option value="expert">Expert or racing</option></select></div>
          <div class="field full"><label for="b-when">When</label><input id="b-when" name="dates" placeholder="Dates, or a month and how many nights" required></div>
          <div class="field full"><label for="b-notes">Anything else</label><textarea id="b-notes" name="notes" placeholder="The rides you have in mind, e-bikes, kids, a race you're training for"></textarea></div>
          <div class="hp" aria-hidden="true"><input name="website" tabindex="-1" autocomplete="off"></div>
          <div class="field full"><button class="btn btn-rust" type="submit">Send my trip</button><p class="form-status" role="status" aria-live="polite"></p></div>
        </form>
        <div class="thanks" tabindex="-1"><h3>Thank you.</h3><p style="color:var(--muted);margin-top:8px">Your trip is with Casey. Expect a first plan within a day.</p></div>
      </div>
    </div>
  </section>
'''
BASECAMP_JS = '''
<script>
(function(){
  var f=document.getElementById('bc-form'),st=f.querySelector('.form-status');
  f.addEventListener('submit',async function(e){
    e.preventDefault();st.className='form-status';
    var miss=[].filter.call(f.querySelectorAll('[required]'),function(i){return !i.value.trim()});
    if(miss.length){st.textContent='Please add your name, email and when you want to come.';st.classList.add('err');miss[0].focus();return}
    if(!/^[^@\\s]+@[^@\\s]+\\.[^@\\s]+$/.test(f.email.value)){st.textContent='Please check your email address.';st.classList.add('err');f.email.focus();return}
    var btn=f.querySelector('button');btn.disabled=true;btn.textContent='Sending…';
    try{var r=await fetch('/api/basecamp',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify(Object.fromEntries(new FormData(f)))});if(!r.ok)throw 0;
      var bx=document.getElementById('bc-box');bx.classList.add('sent');bx.querySelector('.thanks').focus();
    }catch(_){st.textContent='Something went wrong. Please email casey@ophirstays.com and we\\'ll reply today.';st.classList.add('err');btn.disabled=false;btn.textContent='Send my trip'}
  });
})();
</script>'''
basecamp_page = page('Durango Mountain Bike and Ski Trips, Planned · Ophir Basecamp',
  'Ophir Basecamp: Durango homes built for riders and skiers, with San Juan high-country routes planned, shuttles booked, fuel stocked and repairs handled. Plan a bike trip, training camp or ski week.',
  '/basecamp', 'stay', basecamp_body, BASECAMP_JS, image='/assets/photos/basecamp-hero.jpg')

# ---------------- ABOUT ----------------
about_body = f'''
  <section class="center" style="padding-bottom:56px">
    <div class="wrap narrow reveal">
      <p class="eyebrow">About</p>
      <h1 class="display">Run from here. Not from a call center.</h1>
      <hr class="rule">
    </div>
  </section>
  <section style="padding-top:0">
    <div class="wrap split">
      <div class="reveal">{photo('casey', 'Casey Roberts laughing as he opens a bottle of champagne in the mountains', 'photo tall')}</div>
      <div class="reveal">
        <p class="eyebrow">The founder</p>
        <h2 class="display">Casey Roberts</h2>
        <p class="lead">I came to Durango in 2003 to play soccer at Fort Lewis College, won a national championship there in 2005, raced on the Fort Lewis cycling team, and never left.</p>
        <p style="color:var(--muted);margin-top:20px">Twenty-three years later I'm an orthopedic PA-C here and a dad. I founded Durango Bike Project, a coffee and bike shop, and spent years sending visitors to the right trail, the right river and the right table.</p>
        <p style="color:var(--muted);margin-top:20px">Ophir Stays is that same work, done properly: a small number of beautiful homes, cared for by people who live here, with every guest's trip planned by someone who knows this place. When you call, you get me.</p>
        <div class="facts"><div><b>23</b><span>years in Durango</span></div><div><b>25</b><span>homes, at most</span></div><div><b>15</b><span>minutes to a real reply</span></div></div>
      </div>
    </div>
  </section>
  <section style="padding-top:0">
    <div class="wrap">
      <p class="eyebrow reveal">Local since 2003</p>
      <div class="reveal" style="display:grid;grid-template-columns:repeat(auto-fit,minmax(220px,1fr));gap:16px;margin-top:18px">
        <figure style="margin:0">{photo('casey-soccer', 'Casey and his son on the Fort Lewis College soccer field after a game', 'photo tall')}<figcaption class="fine" style="margin-top:10px">Back on the Fort Lewis pitch, where it started in 2003.</figcaption></figure>
        <figure style="margin:0">{photo('casey-cx', 'Casey racing cyclocross on a frosty course in Durango', 'photo tall')}<figcaption class="fine" style="margin-top:10px">Racing cyclocross in Durango.</figcaption></figure>
        <figure style="margin:0">{photo('casey-trout', 'Casey holding a brown trout on a drift boat', 'photo tall')}<figcaption class="fine" style="margin-top:10px">A brown trout from a day on the river.</figcaption></figure>
      </div>
    </div>
  </section>
  <section id="give">
    <div class="wrap">
      <div class="center reveal" style="max-width:720px;margin:0 auto 40px">
        <p class="eyebrow">Ophir in Durango</p>
        <h2 class="display">$10 from every stay stays in Durango.</h2>
        <hr class="rule">
        <p class="lead">It comes from our fee, never the owner's. After booking, each guest chooses where their $10 goes.</p>
      </div>
      <div class="give reveal">
        <a class="cause" href="https://www.durangotrails.org" rel="noopener" target="_blank"><span class="mk">Trails</span><h3>Durango Trails</h3><p>The nonprofit that builds and cares for the singletrack our guests ride, from Horse Gulch to Animas Mountain.</p><span class="link">durangotrails.org</span></a>
        <a class="cause" href="https://www.asadurango.com" rel="noopener" target="_blank"><span class="mk">Mountain</span><h3>Adaptive Sports Association</h3><p>Ski and outdoor programs at Purgatory for people with disabilities, for more than forty years.</p><span class="link">asadurango.com</span></a>
        <a class="cause" href="https://swhousingsolutions.com" rel="noopener" target="_blank"><span class="mk">Home</span><h3>Housing Solutions for the Southwest</h3><p>Helping local families find and keep a home in La Plata County, where housing is the hardest thing to find.</p><span class="link">swhousingsolutions.com</span></a>
      </div>
      <div class="split top reveal" style="margin-top:48px;gap:40px">
        <div><h3 class="display" style="font-size:26px">Spent here, too</h3><p style="color:var(--muted)">Our cleaners, handymen, guides, shops, coffee and restaurants are local, and paid fairly. Each year we publish how much of every booking dollar stayed in La Plata County.</p></div>
        <div><h3 class="display" style="font-size:26px">Given so far</h3><p style="color:var(--muted)">Our first donations go out with our first guest stays, and we'll post each one here as it happens. We volunteer at Durango Trails work days, and owners and returning guests are welcome to join us.</p></div>
      </div>
    </div>
  </section>
  <section class="tint">
    <div class="wrap split">
      <div class="reveal">
        <p class="eyebrow">The name</p>
        <h2 class="display">Why Ophir</h2>
        <p class="lead">Ophir was the legendary land of gold. Miners carried the name into the San Juans and gave it to a town and a high pass between the peaks. They came looking for riches and found something better. We named our homes for that feeling.</p>
      </div>
      <div class="reveal">{photo('ophir', 'Ice Lake Basin in the San Juans near Ophir')}</div>
    </div>
  </section>
  <section class="center">
    <div class="wrap narrow">
      <h2 class="display reveal">Own a home in Durango?</h2>
      <p class="lead reveal">See what it could earn, and whether it belongs in the Collection.</p>
      <p class="reveal" style="margin-top:32px"><a class="btn btn-rust" href="/owners#estimate">Get your free estimate</a></p>
    </div>
  </section>
'''
about = page('About Casey Roberts, Durango Local · Ophir Stays', 'Ophir Stays is locally owned and run from Durango, Colorado, by Casey Roberts, a Durango local of twenty-three years.', '/about', 'about', about_body)

# ---------------- JOURNAL ----------------
journal_body = f'''
  <section class="center" style="padding-bottom:56px">
    <div class="wrap narrow reveal">
      <p class="eyebrow">The Journal</p>
      <h1 class="display">Notes from Durango.</h1>
      <hr class="rule">
      <p class="lead">Where to ride, ski, eat and slow down, from people who live here. And, for owners, what it takes to run a mountain home well.</p>
    </div>
  </section>
  <section style="padding-top:0">
    <div class="wrap grid3">
      <a class="card reveal" href="/journal/durango-rides">{photo('journal-1', 'Singletrack below Engineer Mountain', 'ph')}<p class="post-meta">Ride</p><h3>Five rides that show you Durango</h3><p>From a first lap at Horse Gulch to a long day on Hermosa Creek.</p><span class="link">Read</span></a>
      <a class="card reveal" href="/trails"><div class="ph"><img src="/assets/routes/telegraph-sidewinder.jpg" alt="Map of the Telegraph and Sidewinder mountain bike route, Durango" loading="lazy"></div><p class="post-meta">Ride</p><h3>Durango mountain bike routes</h3><p>Ten rides from town with maps, elevation profiles and free GPX downloads.</p><span class="link">Ride</span></a>
      <a class="card reveal" href="/trail-map"><div class="ph"><img src="/assets/trail-map-web.jpg?v=2" alt="Ophir Stays Durango mountain bike trail map" loading="lazy" style="object-position:top"></div><p class="post-meta">Ride</p><h3>Durango trail map</h3><p>Every trail system around town on one free, printable map.</p><span class="link">Open the map</span></a>
      <a class="card reveal" href="/journal/where-to-eat-durango">{photo('coffee', 'A latte at a Durango café table', 'ph')}<p class="post-meta">Eat</p><h3>Where to eat in Durango, from a local</h3><p>Thirteen places, sorted by the night you're having: a special dinner, a date, friends, kids, or lunch on the run.</p><span class="link">Read</span></a>
      <a class="card reveal" href="/journal/durango-home-earnings">{photo('journal-3', 'Gold aspens below Mount Sneffels', 'ph')}<p class="post-meta">Owners</p><h3>What a Durango vacation home earns, and what decides it</h3><p>Three data firms, three answers. What the numbers say, and the five things that separate the top homes.</p><span class="link">Read</span></a>
      <a class="card reveal" href="/journal/switch-rental-managers-durango">{photo('hero-fireplace', 'A great room with the fire lit in a Durango home', 'ph')}<p class="post-meta">Owners</p><h3>How to switch rental managers in Durango</h3><p>Your contract, booked stays, reviews, keys and taxes, on a 30 to 60 day timeline.</p><span class="link">Read</span></a>
      <a class="card reveal" href="/journal/la-plata-county-short-term-rental-permit">{photo('home-1', 'A mountain home in La Plata County', 'ph')}<p class="post-meta">Owners</p><h3>La Plata County rental permits, step by step</h3><p>No county permit yet. What you do need, and what may change in 2027.</p><span class="link">Read</span></a>
      <a class="card reveal" href="/journal/durango-short-term-rental-rules">{photo('ophir', 'Ice Lake Basin in the San Juans near Ophir', 'ph')}<p class="post-meta">Owners</p><h3>Can you rent your Durango home short-term?</h3><p>City permits, county taxes and the HOA question, in plain English.</p><span class="link">Read</span></a>
    </div>
  </section>
'''
journal = page('Durango Guides and Owner Notes · The Journal · Ophir Stays', 'Guides to riding, skiing, eating and slowing down in Durango, Colorado, plus notes for mountain-home owners.', '/journal', 'journal', journal_body)

post_body = f'''
  <section style="padding-bottom:40px">
    <div class="wrap narrow center reveal">
      <p class="eyebrow">Ride</p>
      <h1 class="display">Five rides that show you Durango</h1>
      <p class="post-meta">By Casey Roberts</p>
    </div>
  </section>
  <div class="wrap">{photo('rides', 'Riders resting on a sandstone point above Durango at dusk')}</div>
  <section style="padding-top:56px">
    <div class="wrap narrow article">
      <p>Durango has more good singletrack within a few minutes of town than most places have in a whole county. These are the five rides we send guests on first, from an easy shakeout to a full day out.</p>
      <figure style="margin:32px 0"><a href="/trail-map"><img src="/assets/trail-map-web.jpg?v=2" alt="Ride Durango: an Ophir Stays map of the trail systems around Durango, Colorado" loading="lazy" style="width:100%;height:auto;display:block;border:1px solid var(--line)"></a><figcaption class="fine" style="margin-top:10px">Our trail map of Durango. <a href="/trail-map">Open the full-size map</a> or <a href="/assets/ophir-durango-trail-map.pdf" download>download the PDF</a>.</figcaption></figure>
      <h2>1. Horse Gulch</h2>
      <p>Minutes from Main Avenue, a web of flowing trails through piñon and juniper. The right first ride: short loops, big views back over town, and easy to extend when your legs feel good.</p>
      <div class="pgrid pgrid-2" style="margin:8px 0 28px">{ptile(RBY['meadow-loop'])}{ptile(RBY['telegraph-sidewinder'])}</div>
      <h2>2. Animas Mountain</h2>
      <p>A steady climb on the north edge of town to views straight down the Animas Valley. Rocky in places, rewarding all the way. Go early in summer.</p>
      <div class="pgrid pgrid-1" style="margin:8px 0 28px">{ptile(RBY['animas-mountain-loop'])}</div>
      <h2>3. Log Chutes</h2>
      <p>Cool forest riding up Junction Creek Road, with smooth climbs and fun descents. A favorite on hot afternoons when town is baking.</p>
      <div class="pgrid pgrid-1" style="margin:8px 0 28px">{ptile(RBY['log-chutes'])}</div>
      <h2>4. The Colorado Trail from Junction Creek</h2>
      <p>The start, or the finish, of a 500-mile trail to Denver. Ride out and back as far as you like through some of the prettiest forest near town.</p>
      <h2>5. Hermosa Creek</h2>
      <p>The big one: a long day along a mountain creek, best done as a shuttle. We arrange the drop-off and have lunch packed.</p>
      <p style="margin-top:40px"><a href="/trails"><b>See all ten Durango routes with maps and GPX</b></a></p>
      <p>Staying with Ophir? Bikes are sized to each rider and delivered to the house, and we'll match the ride to the weather and your legs.</p>
    </div>
  </section>
'''
post = page('Five rides that show you Durango · The Journal · Ophir Stays',
            'The five Durango mountain bike rides we send guests on first: Horse Gulch, Animas Mountain, Log Chutes, the Colorado Trail and Hermosa Creek.',
            '/journal/durango-rides', 'journal', post_body)



post3_body = f'''
  <section style="padding-bottom:40px">
    <div class="wrap narrow center reveal">
      <p class="eyebrow">Eat</p>
      <h1 class="display">Where to eat in Durango, from a local</h1>
      <p class="post-meta">By Casey Roberts · October 2026</p>
    </div>
  </section>
  <div class="wrap">{photo('hero-coffee', 'A latte and pastry by the fire in a mountain café')}</div>
  <section style="padding-top:56px">
    <div class="wrap narrow article">
      <p><strong>I bartended at some of Durango’s best restaurants before PA school, and I’ve spent twenty-three years eating my way down Main Avenue. These are the thirteen places I send friends, sorted by the night you’re having.</strong></p>
      <p>A note on timing: summer weekends and Christmas week fill early everywhere on this list. Book a week or more ahead, or ask us and we’ll hold the table.</p>
      <h2>A night to remember</h2>
      <p><strong><a href="https://www.eolusdurango.com/" rel="noopener">Eolus Bar &amp; Dining</a></strong> <span class="fine">· 919 Main Ave</span><br>New American cooking and one of the few covered rooftops downtown, with the mountains in view. The pick for an anniversary. Book ahead.</p>
      <p><strong><a href="https://www.serafinassteakhouse.com/" rel="noopener">Serafina&#x27;s Steakhouse</a></strong> <span class="fine">· 144 E 9th St</span><br>The newest serious steakhouse in town, from the people behind Chimayo. A player piano, an intimate bar, and steak and seafood done properly. Open Thursday to Monday; reserve by phone.</p>
      <p><strong><a href="https://636mainave.com/" rel="noopener">636 Main Ave</a></strong> <span class="fine">· 636 Main Ave</span><br>The old Ken &amp; Sue&#x27;s, still one of the most reliable dinners on Main. Contemporary American with Asian touches and a good patio. Dinner only; book on Tock.</p>
      <h2>Date night</h2>
      <p><strong><a href="https://www.perbaccodurango.com/" rel="noopener">Perbacco Cucina Italiana</a></strong> <span class="fine">· 505 Main Ave</span><br>Classic pastas and risotto in a warm room on lower Main. Quiet enough to talk, good enough to come back. Reserve on OpenTable.</p>
      <p><strong><a href="https://www.primidurango.com/" rel="noopener">PRIMI Pasta &amp; Wine Bar</a></strong> <span class="fine">· 1201 Main Ave</span><br>Small, handmade pasta and an Italian wine list on north Main, with a patio when it’s warm. Call ahead; it fills up.</p>
      <p><strong><a href="https://elmorotavern.com/" rel="noopener">El Moro Spirits &amp; Tavern</a></strong> <span class="fine">· 945 Main Ave</span><br>Serious cocktails in a historic saloon building, with a gastropub menu to match. Book on weekends. Weekend brunch is worth knowing about.</p>
      <h2>Out with friends</h2>
      <p><strong><a href="https://eastbysouthwest.com/" rel="noopener">East by Southwest</a></strong> <span class="fine">· 160 E College Dr</span><br>Sushi and Pan-Asian plates, a sake lounge and a strong happy hour. The best option in town when someone at the table eats vegetarian or vegan.</p>
      <p><strong><a href="https://www.chimayodurango.com/" rel="noopener">Chimayo Stone Fired Kitchen</a></strong> <span class="fine">· 862 Main Ave</span><br>Stone-fired ovens, a long bar, a patio and a chef’s counter if you like to watch the kitchen. Lively without being loud.</p>
      <h2>With kids</h2>
      <p><strong><a href="http://www.fireduppizzeria.com" rel="noopener">Fired Up Pizzeria</a></strong> <span class="fine">· 735 Main Ave</span><br>Wood-fired Neapolitan pizza in a big room that handles families easily, with a rooftop patio in summer. Lunch is the calm time.</p>
      <p><strong><a href="https://www.carverbrewing.com" rel="noopener">Carver Brewing Co.</a></strong> <span class="fine">· 1022 Main Ave</span><br>Durango’s original brewery, pouring since 1988. Beer garden, a menu for everyone, open from breakfast to dinner. Walk in.</p>
      <p><strong><a href="https://www.steamworksbrewing.com" rel="noopener">Steamworks Brewing Co.</a></strong> <span class="fine">· 801 E 2nd Ave</span><br>Big, busy and happy to seat a group of twelve with three kids under ten. Brewpub food, a patio and parking.</p>
      <h2>Quick and good</h2>
      <p><strong><a href="https://ziataqueria.com/" rel="noopener">Zia Taqueria</a></strong> <span class="fine">· 2977 Main Ave and 400 S Camino del Rio</span><br>Counter service, burritos and tacos made from scratch, fast and cheap. A kids’ menu and two locations.</p>
      <p><strong><a href="https://rgpswraps.com/" rel="noopener">RGP&#x27;s Flame Grilled Wraps</a></strong> <span class="fine">· 835 Main Ave</span><br>Flame-grilled wraps at a weekday lunch counter downtown. Closed weekends, and not a dinner spot, but a great lunch.</p>
      <h2>Staying with Ophir?</h2>
      <p>Tell us what you’re in the mood for before you arrive. We book the tables, match them to your days, and at some of these places the first round is on us.</p>
      <p style="margin-top:32px"><a class="btn btn-rust" href="/stay">See how a stay works</a></p>
      <p class="fine" style="margin-top:40px">Details checked October 2026. Hours change with the season, so check with the restaurant before you go. No restaurant paid to be on this list.</p>
    </div>
  </section>
'''
post3 = page('Best Restaurants in Durango, CO: Where a Local Eats (2026) · Ophir Stays',
             'Thirteen Durango restaurants a local recommends, by occasion: special dinners at Eolus and Serafina\u2019s, date night at Perbacco, pizza with kids at Fired Up, and fast burritos at Zia.',
             '/journal/where-to-eat-durango', 'journal', post3_body)


post4_body = f"""
  <section style="padding-bottom:40px">
    <div class="wrap narrow center reveal">
      <p class="eyebrow">Owners</p>
      <h1 class="display">Can you rent your Durango home short-term? The rules, city and county</h1>
      <p class="post-meta">By Casey Roberts · October 2026</p>
    </div>
  </section>
  <div class="wrap">{photo('ophir', 'Ice Lake Basin in the San Juan Mountains near Ophir')}</div>
  <section style="padding-top:56px">
    <div class="wrap narrow article">
      <p><strong>It depends on one line on a map. Inside Durango city limits, short-term rentals need a city permit, and in the main residential zones those permits are capped and full. In unincorporated La Plata County, there is no county rental permit: you register to collect taxes, follow the county's good-neighbor guidelines, and check your HOA.</strong></p>
      <p>Here is what each side requires as of October 2026, and the questions to answer before you list.</p>

      <h2>Inside Durango city limits</h2>
      <p>The city regulates any stay of 1 to 29 nights. You need a Limited Use Permit before you advertise, plus a city business license, and you collect and remit the city's lodgers' and sales taxes.</p>
      <div class="table-wrap"><table class="data">
        <thead><tr><th scope="col">Zone</th><th scope="col">Permits allowed</th><th scope="col">Active</th><th scope="col">Waitlist</th></tr></thead>
        <tbody>
          <tr><th scope="row">EN-1 (established neighborhood)</th><td>22</td><td>21</td><td>26</td></tr>
          <tr><th scope="row">EN-2 (established neighborhood)</th><td>17</td><td>17</td><td>11</td></tr>
          <tr><th scope="row">Central Business, Mixed-Use, some Planned Developments</th><td>Set per development</td><td>87</td><td>Not published</td></tr>
        </tbody>
      </table></div>
      <p class="fine">Source: City of Durango, Vacation Rental Information, checked October 2026. About 125 permits are active citywide.</p>
      <p>Three things catch owners out. Permits don't transfer: a sale automatically ends the permit, so a buyer starts at the back of the line. In the EN zones, a second rental on the same block face needs Planning Commission approval and a third isn't allowed. And stays of 30 nights or more aren't regulated by the city at all, which is why some in-town owners rent by the month instead.</p>

      <h2>In unincorporated La Plata County</h2>
      <p>Most of the area's best rental homes sit outside city limits: Durango Mountain and Purgatory, the Animas Valley, Hermosa, Hesperus and Vallecito. Here the county does not issue a short-term rental permit or license. What it does require is taxes.</p>
      <p><strong>Required:</strong> collect and remit the county's 2% lodging tax and 2% county sales tax, plus state sales tax, on every stay. That means a Colorado sales tax license unless a manager handles collection for you. Booking platforms collect some of these taxes on their bookings; check which ones, and remit the rest.</p>
      <p><strong>Recommended by the county:</strong></p>
      <ul>
        <li>A local contact who can deal with problems, with that number shared with your neighbors.</li>
        <li>No more than two guests per bedroom, plus one.</li>
        <li>Enough parking on the property, and no campers or trailers unless there's room for them.</li>
        <li>A trash schedule that keeps up with turnovers.</li>
        <li>On a septic system, a check with La Plata County Public Health (970-247-5702) that it can handle rental use.</li>
      </ul>
      <p>The county has discussed regulating short-term rentals, but as of October 2026 it has not adopted a licensing program or a cap. That could change, so it's worth checking again before you buy a home on the strength of its rental income.</p>

      <h2>Then check your HOA. It's often the real answer.</h2>
      <p>County rules are light, but many subdivisions are not. Covenants can ban rentals shorter than 30 days, or six months, or set their own registration and fees. Read your declaration and any amendments, and ask the HOA in writing. Some neighborhoods inside the city also restrict rentals through their own development documents, even in zones where the city allows them.</p>

      <h2>Before you list: a short checklist</h2>
      <ul>
        <li>City or county? Look up your parcel on the county's map.</li>
        <li>In the city: do you hold a permit, or are you on the waitlist?</li>
        <li>HOA: written confirmation that short stays are allowed.</li>
        <li>Taxes: a sales tax license, or a manager who collects and remits for you.</li>
        <li>Insurance: a policy that covers short-term rental use. Most standard homeowner's policies don't.</li>
        <li>Septic: a capacity check if you're not on sewer.</li>
      </ul>

      <h2>How Ophir handles it</h2>
      <p>Before we sign a home, we check its zoning and HOA documents with the owner. Once it's live, we register for and remit taxes on direct bookings, act as the local contact, and keep occupancy and parking inside the county's guidelines. If you're not sure where your home stands, we'll look it up for you. Buying? We'll <a href="/buying">check a home and estimate its earnings</a> before you offer.</p>
      <p style="margin-top:32px"><a class="btn btn-rust" href="/owners#estimate">Get your free estimate</a></p>

      <h2 style="font-size:20px;margin-top:56px">Sources</h2>
      <p class="fine" style="margin:0">
        <a href="https://www.durangoco.gov/800/Vacation-Rental-Information" rel="noopener">City of Durango: Vacation Rental Information</a> (checked October 2026)<br>
        <a href="https://www.lpcgov.org/departments/finance___procurement/lodging_tax_information/be_a_good_neighbor_(vacation_rental).php" rel="noopener">La Plata County: Be a Good Neighbor (vacation rental)</a> (checked October 2026)<br>
        <a href="https://www.durangoherald.com/articles/voters-overwhelmingly-approve-la-plata-county-lodgers-tax-reallocation/" rel="noopener">Durango Herald: county lodgers tax capped at 2% by state law</a> (November 2024)<br>
        This is a plain-English summary, not legal advice. Rules change; confirm with the city, the county and your HOA before you rent.
      </p>
    </div>
  </section>
"""
post4 = page('Durango Short-Term Rental Rules (2026): City Permits, County Taxes, HOAs · Ophir Stays',
             'Durango short-term rental rules for 2026: city permits are capped and waitlisted; La Plata County has no rental permit but requires lodging and sales tax.',
             '/journal/durango-short-term-rental-rules', 'journal', post4_body)


TRAILS = [
 ('Horse Gulch', 'East of downtown, minutes from Main Avenue. A big web of rolling singletrack through piñon and juniper, with easy and intermediate loops near the trailhead and harder lines farther out. The best first ride in Durango.', 'Horse Gulch trailhead, at the end of Horse Gulch Road, east of downtown.'),
 ('Raider Ridge', 'The rocky spine above Fort Lewis College. Technical and exposed in places, with views over town and the La Platas the whole way. Best linked with Horse Gulch.', 'Ride up from Horse Gulch or from the college.'),
 ('Animas Mountain', 'The mountain that looks down on north Durango. A steep, rocky climb to big views of the Animas Valley, and a technical descent. It closes each winter for wildlife, so check the dates before you go.', 'Animas Mountain trailhead, at the north end of West 4th Avenue.'),
 ('Overend and Perins', 'Short, punchy trails on the west side of town in Overend Mountain Park, with rock gardens and quick loops. Easy to fit in before dinner.', 'Overend Mountain Park, west of downtown.'),
 ('Twin Buttes', 'Newer, flowing singletrack west of town below the Twin Buttes, built for riding. A good intermediate day.', 'Off US 160 west of town.'),
 ('Colorado Trail', 'The start, or the finish, of the 500-mile trail to Denver. A long, steady climb up Junction Creek through forest, then back down the same way. As big a day as you want.', 'Junction Creek trailhead, northwest of town on Junction Creek Road.'),
 ('Log Chutes', 'Forested loops off Junction Creek Road, higher and cooler than town in summer. Intermediate climbing and a fun, fast descent.', 'Off Junction Creek Road, past the Colorado Trail trailhead.'),
 ('Carbon Junction', 'A steep climb out of the river corridor south of town that ties into Horse Gulch. Great for a big loop starting from the Animas River Trail.', 'South of town near the US 160 and US 550 junction, off the Animas River Trail.'),
]
TRAIL_RIDES = {'Horse Gulch': '<p class="fine">Ride it: ' + ' · '.join(['<a href="/trails/meadow-loop">Meadow Loop</a>', '<a href="/trails/telegraph-sidewinder">Telegraph and Sidewinder</a>']) + '</p>', 'Raider Ridge': '<p class="fine">Ride it: ' + ' · '.join(['<a href="/trails/raider-ridge">Raider Ridge</a>']) + '</p>', 'Animas Mountain': '<p class="fine">Ride it: ' + ' · '.join(['<a href="/trails/animas-mountain-loop">Animas Mountain Loop</a>']) + '</p>', 'Overend and Perins': '<p class="fine">Ride it: ' + ' · '.join(['<a href="/trails/star-wars-8-bells">Star Wars and 8 Bells</a>', '<a href="/trails/star-wars-spirit">Star Wars and Spirit</a>']) + '</p>', 'Twin Buttes': '<p class="fine">Ride it: ' + ' · '.join(['<a href="/trails/twin-buttes-loop">Twin Buttes Loop</a>']) + '</p>', 'Log Chutes': '<p class="fine">Ride it: ' + ' · '.join(['<a href="/trails/log-chutes">Log Chutes</a>']) + '</p>', 'Carbon Junction': '<p class="fine">Ride it: ' + ' · '.join(['<a href="/trails/carbon-junction-skull-rock">Carbon Junction and Skull Rock</a>', '<a href="/trails/sale-barn-skull-rock">Sale Barn and Skull Rock</a>']) + '</p>'}
trails_html = ''.join(f'''
      <h3 id="{n.lower().replace(' and ','-').replace(' ','-')}"><span class="tm-num">{i}</span> {n}</h3>
      <p>{d}</p>
      <p class="fine">Start: {s}</p>{TRAIL_RIDES.get(n,'')}''' for i,(n,d,s) in enumerate(TRAILS,1))

trailmap_body = f"""
  <section style="padding-bottom:32px">
    <div class="wrap narrow center reveal">
      <p class="eyebrow">Ride</p>
      <h1 class="display">Durango mountain bike trail map</h1>
      <p class="lead">A free, printable map of the singletrack around Durango, Colorado, and where to start: Horse Gulch, Raider Ridge, Animas Mountain, Overend, Twin Buttes, the Colorado Trail, Log Chutes and Carbon Junction.</p>
      <p style="margin-top:20px;display:flex;gap:12px;justify-content:center;flex-wrap:wrap"><a class="btn" href="/assets/ophir-durango-trail-map.jpg" download>Download image</a> <a class="btn" href="/assets/ophir-durango-trail-map.pdf" download>Download PDF to print</a></p>
      <p class="fine" id="license" style="margin-top:10px">Free to download, print and share with credit to Ophir Stays. Trail data © OpenStreetMap contributors, under the Open Database License. The PDF prints sharp at 12 by 16 inches.</p>
    </div>
  </section>
  <section style="padding-top:0">
    <figure class="wrap" style="max-width:1000px;margin:0 auto"><img src="/assets/trail-map-web.jpg?v=2" width="1200" height="1600" alt="Durango mountain bike trail map showing Horse Gulch, Raider Ridge, Animas Mountain, Overend, Twin Buttes, the Colorado Trail, Log Chutes and Carbon Junction, with trailheads and shaded terrain" style="width:100%;height:auto;display:block;border:1px solid var(--line)"></figure>
    <div class="wrap narrow article" style="margin-top:40px">
      <h2>The trail systems on the map</h2>
      <p>Durango is one of the few towns where you can ride singletrack from your front door. Each number on the map is a trail system, and each P is a trailhead with parking.</p>{trails_html}
      <h2>Before you ride</h2>
      <p>Stay off trails when they're muddy: ruts last all season. Summer afternoons bring lightning, so start early. Town sits at 6,500 feet and the high points on this map are near 9,000, so drink more than you think and go easy the first day. For turn-by-turn navigation on the trail, use Trailforks or MTB Project.</p>
      <h2>Staying with Ophir?</h2>
      <p>Bikes are sized to each rider and delivered to the house, and we'll match the ride to the weather and your legs. <a href="/stay">See how a stay works</a>.</p>
      <p><a href="/trails"><b>Ten routes with maps, elevation profiles and GPX</b></a></p>
      <p><a href="/journal/durango-rides">Read: five rides that show you Durango</a></p>
      <p class="fine">Trail data © OpenStreetMap contributors. Elevation from USGS via Mapzen Terrain Tiles. Trail conditions and closures change; check with the City of Durango and the San Juan National Forest before you ride.</p>
    </div>
  </section>
"""
trailmap = page('Durango Mountain Bike Trail Map (Free PDF) · Ophir Stays',
                'Free printable Durango mountain bike trail map: Horse Gulch, Raider Ridge, Animas Mountain, Overend, Twin Buttes, the Colorado Trail, Log Chutes and Carbon Junction, with trailheads.',
                '/trail-map', 'journal', trailmap_body, image='/assets/og-trail-map.jpg')

# ---------------- HOMES PAGES ----------------
homes_body = f'''
  <section class="center" style="padding-bottom:56px">
    <div class="wrap narrow reveal">
      <p class="eyebrow">The Collection</p>
      <h1 class="display">Twenty-five homes. One standard.</h1>
      <hr class="rule">
      <p class="lead">Every home is chosen one at a time, inspected before every arrival, and comes with the whole trip handled.</p>
    </div>
  </section>
  <section style="padding-top:0"><div class="wrap">{collection_grid()}</div></section>
'''
homes_page = page('Durango Vacation Homes · The Collection · Ophir Stays', 'Luxury vacation homes in Durango, Colorado, each kept to one standard, each stay with the trip handled.', '/homes', 'homes', homes_body)

def home_page(h):
    slug = h['slug']
    feats = ''.join(f'<li>{f}</li>' for f in h['features'])
    sample = '<span class="sample-tag">SAMPLE · NOT A REAL LISTING</span>' if h['sample'] else ''
    body = f'''
  <section style="padding:48px 0 36px">
    <div class="wrap center reveal">{sample}
      <p class="eyebrow">{h['area']} · Durango</p>
      <h1 class="display">{h['name']}</h1>
      <p class="post-meta">{h['beds']} bedrooms · {h['baths']} baths · sleeps {h['sleeps']}</p>{'<p class="eyebrow" style="margin-top:14px">Basecamp Ready · garage, wash station, gear room, close to the trails</p>' if BASECAMP_ON and h.get('basecamp') else ''}
    </div>
  </section>
  <div class="wrap">
    <div class="gallery">
      {hphoto(slug, 1, h['name'] + ': exterior and view', 'g-main')}
      {hphoto(slug, 2, h['name'] + ': great room', 'g-a')}{hphoto(slug, 3, h['name'] + ': kitchen', 'g-b')}
      {hphoto(slug, 4, h['name'] + ': primary bedroom', 'g-c')}{hphoto(slug, 5, h['name'] + ': hot tub and deck', 'g-d')}
    </div>
  </div>
  <section>
    <div class="wrap split top">
      <div class="reveal">
        <p class="eyebrow">The home</p>
        <h2 class="display">{h['line']}</h2>
        <ul class="standard" style="columns:1;margin-top:28px">{feats}</ul>
      </div>
      <div class="reveal">
        <div class="band" style="grid-template-columns:1fr;text-align:left">
          <div><p class="eyebrow">A trip, already planned</p><p style="margin:0;font-family:var(--serif);font-style:italic;font-size:24px;line-height:1.35;color:var(--charcoal)">{h['trip']}</p></div>
          <div><p class="fine" style="margin:0 0 16px">Guest booking opens in 2027. Leave your name for first dates.</p>
          <a class="btn" href="mailto:casey@ophirstays.com?subject=First%20dates%20at%20{h['name'].replace(' ', '%20')}">Request first dates</a></div>
        </div>
      </div>
    </div>
  </section>
'''
    return page(f"{h['name']} · {h['area']} · Ophir Stays", f"{h['name']}: {h['beds']}-bedroom luxury home in {h['area']}, Durango, Colorado. {h['line']}", f"/homes/{slug}", 'homes', body)


post2_body = f'''
  <section style="padding-bottom:40px">
    <div class="wrap narrow center reveal">
      <p class="eyebrow">Owners</p>
      <h1 class="display">What a Durango vacation home earns, and what decides it</h1>
      <p class="post-meta">By Casey Roberts · October 2026</p>
    </div>
  </section>
  <div class="wrap">{photo('journal-3', 'Gold aspens below Mount Sneffels in autumn')}</div>
  <section style="padding-top:56px">
    <div class="wrap narrow article">
      <p><strong>A typical Durango short-term rental earns somewhere between $41,000 and $55,000 a year, depending on whose data you trust. The top homes earn roughly double that, and almost everything that separates them is in the owner's control.</strong></p>
      <p>Below is what the three most-cited data firms report for Durango, what moves a home from average to excellent, and how to think about your own.</p>

      <h2>The market, three ways</h2>
      <p>Each firm counts listings and revenue differently, so their numbers don't match. Taken together, they draw a clear picture.</p>
      <div class="table-wrap"><table class="data">
        <thead><tr><th scope="col"></th><th scope="col">Airbtics</th><th scope="col">Rabbu</th><th scope="col">BnbCalc</th></tr></thead>
        <tbody>
          <tr><th scope="row">Active listings</th><td>1,256</td><td>581</td><td>~1,950</td></tr>
          <tr><th scope="row">Revenue per year</th><td>$55,000</td><td>$45,478</td><td>~$41,000</td></tr>
          <tr><th scope="row">Average nightly rate</th><td>$262</td><td>$301</td><td>$357</td></tr>
          <tr><th scope="row">Occupancy</th><td>56%</td><td>37%</td><td>29–31%</td></tr>
          <tr><th scope="row">Period</th><td>Feb 2025–Jan 2026</td><td>To Apr 2026</td><td>Oct 2025–Sep 2026</td></tr>
        </tbody>
      </table></div>
      <p>One trend shows up everywhere: nightly rates are rising (up 12–16% year over year) while occupancy is flat or falling. Guests are paying more, but they're choosier about where they stay. That rewards the homes that stand out.</p>

      <h2>Size matters most</h2>
      <p>Bedrooms drive revenue more than anything else. The largest homes book slightly less often but command far higher rates.</p>
      <div class="table-wrap"><table class="data">
        <thead><tr><th scope="col">Bedrooms</th><th scope="col">Avg revenue / year</th><th scope="col">Avg nightly rate</th></tr></thead>
        <tbody>
          <tr><th scope="row">2</th><td>$40,854</td><td>$242</td></tr>
          <tr><th scope="row">3</th><td>$54,698</td><td>$350</td></tr>
          <tr><th scope="row">4</th><td>$76,780</td><td>$496</td></tr>
          <tr><th scope="row">5</th><td>$97,480</td><td>$724</td></tr>
          <tr><th scope="row">6+</th><td>$112,767</td><td>$861</td></tr>
        </tbody>
      </table></div>
      <p class="fine">Source: Rabbu, trailing twelve months to April 2026.</p>

      <h2>Summer is the season. The shoulders decide the year.</h2>
      <p>July is Durango's best month, averaging about $7,260 per home; April is the slowest, at about $1,710. That's a fourfold swing. Summer, June through September, carries the year, with a second bump at Christmas and in March for spring skiing.</p>
      <p>Almost every home fills in July. The difference between an average year and a great one is made in April, May, October and November, when guests need a reason to come.</p>

      <h2>What separates the top homes</h2>
      <p>BnbCalc puts Durango's high performers at around $77,000 a year and its low performers at around $19,000. The gap isn't luck. It comes down to five things:</p>
      <p><strong>1. Photography.</strong> Guests decide from the first image. Professional, naturally lit photos are the single cheapest upgrade an owner can make.</p>
      <p><strong>2. A hot tub.</strong> In Durango, homes with a hot tub are associated with about 22% more revenue (BnbCalc). After a day on the mountain, it's the amenity guests search for.</p>
      <p><strong>3. Pricing every day, not every season.</strong> With rates rising and occupancy falling, a set-and-forget price either leaves money on the table in July or sits empty in October. Rates should move with events, weather and demand.</p>
      <p><strong>4. Reviews and response time.</strong> Ranking on Airbnb and VRBO rewards five-star stays and fast replies. A local who answers in minutes, and fixes the hot tub the same afternoon, protects both.</p>
      <p><strong>5. A reason to come in the shoulder season.</strong> A fall aspen ride with bikes delivered, a spring ski weekend with lift tickets waiting. Homes that sell the trip, not just the beds, fill the months others don't.</p>

      <h2>What it means for your home</h2>
      <p>Start with your bedroom count and the table above, then ask honestly how your home scores on those five points. Every one of them is within an owner's control.</p>
      <p>If you'd like a real number for your home, built from its size, location and history, we'll send you a personal estimate within two business days. No obligation.</p>
      <p style="margin-top:32px"><a class="btn btn-rust" href="/owners#estimate">Get your free estimate</a></p>

      <h2 style="font-size:20px;margin-top:56px">Sources</h2>
      <p class="fine" style="margin:0">
        <a href="https://airbtics.com/annual-airbnb-revenue-in-durango-united-states" rel="noopener">Airbtics: Airbnb revenue in Durango</a> (data Feb 2025–Jan 2026)<br>
        <a href="https://rabbu.com/airbnb-data/durango-co" rel="noopener">Rabbu: Durango, CO Airbnb market data</a> (as of Apr 2026)<br>
        <a href="https://www.bnbcalc.com/markets/us/durango-co" rel="noopener">BnbCalc: Durango, CO market</a> (12 months to Sep 2026)<br>
        Figures are third-party estimates of Airbnb and VRBO listings and vary by method.
      </p>
    </div>
  </section>
'''
post2 = page('What a Durango vacation home earns, and what decides it · The Journal · Ophir Stays',
             'Durango short-term rentals earn about $41,000 to $55,000 a year on average; top homes earn roughly double. Revenue by bedroom count, seasonality, and the five things that separate the best homes.',
             '/journal/durango-home-earnings', 'journal', post2_body)


# ---------------- ROUTES ----------------
ROUTE_COPY = {
 'meadow-loop': (['Horse Gulch Road', 'Meadow Loop', 'Cuchillo', 'Drop Over'], 'The right first ride in Durango. Climb Horse Gulch Road out of town, circle the open meadow on smooth, rolling singletrack, and roll back down with town below you. Short enough for kids and a first day at altitude.'),
 'telegraph-sidewinder': (['Telegraph', 'Sidewinder', 'Manilla Vanilla', 'Mesa Connector', 'Horse Gulch Road'], 'The classic Horse Gulch loop. A long, steady climb on Telegraph, then Sidewinder and the mesa trails back toward town. Flowing, fast, and the ride most locals do after work.'),
 'raider-ridge': (['Half Ridge', 'Extended Ridge', 'Hyper-Extended Ridge', 'Sugar', 'Horse Gulch Road'], 'The rocky spine above Fort Lewis College. Steep, technical and exposed in places, with views over town and the La Platas the whole way out. Strong riders only.'),
 'animas-mountain-loop': (['Animas Mountain Trail', 'Animas Mountain Upper'], 'A steep, rocky climb to the overlook above the Animas Valley, then a technical descent back to the trailhead. The view from the top is the best in town. Closed each winter for wildlife, so check the dates before you go.'),
 'star-wars-8-bells': (['Star Wars', '8 Bells', 'Spirit', 'Perins Gulch', "Ned's Hill", 'Ella Vita'], 'A short, punchy loop in Overend Mountain Park, a few minutes from downtown. Quick climbs, rock gardens and tight turns. Easy to fit in before dinner.'),
 'star-wars-spirit': (['Spirit', 'Star Wars', 'Perins Gulch', "Ned's Hill", 'Ella Vita', 'Tech Cutoff'], 'The longer Overend loop. Spirit adds more climbing and more of the park, with the same rocky, playful riding as Star Wars.'),
 'twin-buttes-loop': (['Twin Buttes', 'Upper Twin Buttes', 'Upper Ed & Flo', 'Ed & Flo', 'Lightner Creek'], 'Purpose-built flow trails below the Twin Buttes, west of town. Smooth climbing, berms on the way down, and big views of Perins Peak.'),
 'log-chutes': (['Log Chutes 1', 'Log Chutes 2'], 'Forested loops off Junction Creek Road, a thousand feet higher and cooler than town. Pine needles, steady climbing and a fast descent. The pick for a hot summer afternoon.'),
 'carbon-junction-skull-rock': (['Carbon Junction', 'Skull Rock', 'Big Canyon', 'Sidewinder', 'Cowboy Upper'], 'A steep climb out of the river corridor south of town that ties into Skull Rock and the Horse Gulch network. A big, hilly loop with views back up the Animas Valley.'),
 'sale-barn-skull-rock': (['Sale Barn', 'Skull Rock', 'South Rim', 'Big Canyon', 'Cowboy Upper'], 'Rolling mesa riding south of town, with long views and fewer people than Horse Gulch. Dry early in spring when higher trails are still snowed in.'),
}
DIFF_ORDER = {'Easy': 0, 'Intermediate': 1, 'Advanced': 2}

def profile_svg(r, w=1000, h=220):
    p = r['profile']; n = len(p); lo = min(p); hi = max(p)
    span = max(hi - lo, 300); lo2 = lo - span * 0.12; hi2 = lo2 + span * 1.25
    pl, pr, pt, pb = 72, 8, 12, 34
    X = lambda i: pl + (w - pl - pr) * i / (n - 1)
    Y = lambda e: pt + (h - pt - pb) * (1 - (e - lo2) / (hi2 - lo2))
    line = 'M' + 'L'.join(f'{X(i):.1f} {Y(e):.1f}' for i, e in enumerate(p))
    area = line + f'L{X(n-1):.1f} {h-pb}L{X(0):.1f} {h-pb}Z'
    step = 100 if span < 600 else 250 if span < 1500 else 500
    ticks = ''.join(f'<line x1="{pl}" x2="{w-pr}" y1="{Y(t):.1f}" y2="{Y(t):.1f}" stroke="#E7E1D6"/><text x="{pl-8}" y="{Y(t)+4:.1f}" text-anchor="end">{t:,}</text>' for t in range(int(lo2 // step + 1) * step, int(hi2), step))
    mi = r['miles']; mstep = 1 if mi < 9 else 2
    xt = ''.join(f'<text x="{pl + (w-pl-pr)*m/mi:.1f}" y="{h-6}" text-anchor="middle">{m} mi</text>' for m in range(0, int(mi) + 1, mstep))
    return (f'<svg class="profile" viewBox="0 0 {w} {h}" role="img" aria-label="Elevation profile: {r["climb"]:,} feet of climbing, high point {r["high"]:,} feet" style="width:100%;height:auto;font-family:var(--sans);font-size:13px;fill:#6F685F">'
            f'{ticks}<path d="{area}" fill="#ECE4D3"/><path d="{line}" fill="none" stroke="#B4572B" stroke-width="2.5" stroke-linejoin="round"/>{xt}</svg>')


def route_stats(r):
    return (f'<div class="rstats"><div><span>Distance</span><b>{r["miles"]} mi</b></div><div><span>Climbing</span><b>{r["climb"]:,} ft</b></div>'
            f'<div><span>High point</span><b>{r["high"]:,} ft</b></div><div><span>Difficulty</span><b>{r["difficulty"]}</b></div></div>')

def route_page(r):
    trails, blurb = ROUTE_COPY[r['slug']]
    la, lo = r['start']
    faqs = [
        (f"How long is {r['name']}?", f"{r['miles']} miles with about {r['climb']:,} feet of climbing. Most riders take {max(1, round(r['miles'] / 5 + r['climb'] / 1500, 1))} to {round(r['miles'] / 3.5 + r['climb'] / 1000, 1)} hours."),
        (f"How hard is {r['name']}?", {'Easy': 'Easy. Smooth, rolling trail that suits new riders, kids and a first day at altitude.', 'Intermediate': 'Intermediate. Sustained climbs and some rocks and roots; comfortable for riders who ride singletrack regularly.', 'Advanced': 'Advanced. Steep, rocky and technical in places. Best for strong, experienced riders.'}[r['difficulty']]),
        (f"Where does {r['name']} start?", f"{r['trailhead']}. Use the directions button above for turn-by-turn driving directions to the start."),
        ("Can I download the route?", "Yes. The GPX file is free and loads into Trailforks, Strava, Garmin, Wahoo and most bike computers."),
    ]
    others = [o for o in ROUTES if o['slug'] != r['slug']][:0]
    same = [o for o in ROUTES if o['area'] == r['area'] and o['slug'] != r['slug']] + [o for o in ROUTES if o['area'] != r['area'] and o['slug'] != r['slug']]
    more = ''.join(f'<li><a href="/trails/{o["slug"]}">{o["name"]}</a> · {o["miles"]} mi · {o["difficulty"]}</li>' for o in same[:4])
    body = f"""
  <section style="padding-bottom:24px">
    <div class="wrap narrow reveal">
      <p class="eyebrow"><a href="/trails" style="text-decoration:none">Durango routes</a> · {r['area']}</p>
      <h1 class="display">{r['name']}</h1>
      <p class="lead">{blurb}</p>
      {route_stats(r)}
    </div>
  </section>
  <section style="padding-top:0">
    <div class="wrap" style="max-width:1000px">
      <img src="/assets/routes/{r['slug']}.jpg" width="1600" height="1024" alt="Map of the {r['name']} mountain bike route in {r['area']}, Durango, Colorado" style="width:100%;height:auto;border:1px solid var(--line)">
      <div style="margin-top:20px">{ptile(r, big=True, link=False)}</div>
      <p style="margin-top:20px;display:flex;gap:12px;flex-wrap:wrap"><a class="btn" href="/assets/routes/{r['slug']}.gpx" download>Download GPX</a> <a class="btn" href="/assets/routes/{r['slug']}-card.jpg" download>Save the route card</a> <a class="btn" href="https://www.google.com/maps/dir/?api=1&destination={la:.5f},{lo:.5f}" target="_blank" rel="noopener">Directions to the start</a></p>
    </div>
    <div class="wrap narrow article" style="margin-top:24px">
      <h2>The route</h2>
      <p>Start at {r['trailhead']}. The loop links {', '.join(trails[:-1])} and {trails[-1]}, {r['miles']} miles with about {r['climb']:,} feet of climbing, topping out near {r['high']:,} feet.</p>
      <p>Load the GPX into Trailforks, Strava or your bike computer to follow it turn by turn. Stay off the trails when they're muddy, and start early in summer to beat the afternoon storms.</p>
      <h2>Quick answers</h2>
      {''.join(f'<h3 class="faq-q">{q}</h3><p>{a}</p>' for q, a in faqs)}
      <h2>More Durango rides</h2>
      <ul>{more}</ul>
      <p><a href="/trail-map">See every trail system on our Durango trail map</a></p>
      <h2>Staying with Ophir?</h2>
      <p>We'll pick the ride for the day, size and deliver the bikes to the house, and set up a shuttle when the ride calls for one. <a href="/stay">See how a stay works</a>.</p>
      <p class="fine">Route from OpenStreetMap trail data, elevation from USGS. Trails and closures change; check current conditions before you ride.</p>
    </div>
  </section>
"""
    ld = {'@context': 'https://schema.org', '@graph': [
        {'@type': 'TouristAttraction', 'name': r['name'] + ' mountain bike route', 'description': blurb,
         'url': 'https://ophirstays.com/trails/' + r['slug'], 'image': ['https://ophirstays.com/assets/routes/' + r['slug'] + '.jpg', 'https://ophirstays.com/assets/routes/' + r['slug'] + '-card.jpg'],
         'touristType': 'Mountain biking', 'isAccessibleForFree': True,
         'geo': {'@type': 'GeoCoordinates', 'latitude': round(la, 5), 'longitude': round(lo, 5)},
         'containedInPlace': {'@type': 'City', 'name': 'Durango, Colorado'}},
        {'@type': 'BreadcrumbList', 'itemListElement': [
            {'@type': 'ListItem', 'position': 1, 'name': 'Ophir Stays', 'item': 'https://ophirstays.com/'},
            {'@type': 'ListItem', 'position': 2, 'name': 'Durango routes', 'item': 'https://ophirstays.com/trails'},
            {'@type': 'ListItem', 'position': 3, 'name': r['name'], 'item': 'https://ophirstays.com/trails/' + r['slug']}]},
        {'@type': 'FAQPage', 'mainEntity': [{'@type': 'Question', 'name': q, 'acceptedAnswer': {'@type': 'Answer', 'text': a}} for q, a in faqs]}]}
    html = page(f"{r['name']} · Durango Mountain Bike Route, Map and GPX · Ophir Stays",
                f"{r['name']} in {r['area']}, Durango: {r['miles']} miles, {r['climb']:,} ft of climbing, {r['difficulty'].lower()}. Free route map, elevation profile and GPX download.",
                '/trails/' + r['slug'], 'journal', body, image='/assets/routes/' + r['slug'] + '-card.jpg')
    return html.replace('</head>', '<script type="application/ld+json">' + _json.dumps(ld) + '</script>\n</head>', 1)

def route_card(r):
    return (f'<a class="rcard reveal" href="/trails/{r["slug"]}"><div class="ph"><img src="/assets/routes/{r["slug"]}.jpg" alt="Map of {r["name"]}, Durango" loading="lazy" width="1600" height="1024"></div>'
            f'<p class="post-meta">{r["area"]} · {r["difficulty"]}</p><h3>{r["name"]}</h3><p>{r["miles"]} mi · {r["climb"]:,} ft climbing</p></a>')


# ---------------- HIGH-COUNTRY ROUTES ----------------
import re as _re
HIGH_COUNTRY = _json.load(open('data/high_country.json'))
HC_ORDER = ['pass-creek-coal-creek', 'pass-creek-engineer-cascade', 'deer-creek', 'engine-creek', 'little-molas-engineer-cascade', 'blackhawk-loop', 'little-molas-hermosa-corral-draw']
HIGH_COUNTRY.sort(key=lambda r: HC_ORDER.index(r['slug']))
HC_GPX_LIVE = False  # flip to True once Casey has checked each line against his own rides
HC_COPY = {
 'pass-creek-coal-creek': 'The best short ride in the high country. Climb Pass Creek from Coal Bank Pass to the meadows under Engineer Mountain, cross on the Engineer Mountain Trail, then drop Coal Creek and spin a short stretch of US 550 back to the car. No shuttle needed.',
 'pass-creek-engineer-cascade': 'Climb Pass Creek to the shoulder of Engineer Mountain, then ride the Engineer Mountain Trail almost 2,700 feet down through meadow and spruce to Cascade. Short on climbing and long on descending, with a shuttle back up the pass.',
 'deer-creek': 'Up Pass Creek and across the Engineer Mountain Trail to the highest point of the day near 11,900 feet, then down Deer Creek to US 550. A quieter descent with a short shuttle back to Coal Bank.',
 'engine-creek': 'A big day for the miles. Climb Pass Creek, cross under Engineer Mountain, then descend Engine Creek and ride out Cascade Creek to Cascade, more than 3,200 feet down in all. Shuttled.',
 'little-molas-engineer-cascade': 'The high traverse. From Little Molas Lake the Colorado Trail stays above 11,000 feet for miles, tops out over 12,000, then joins the full Engineer Mountain Trail down to Cascade. Shuttled to Molas Pass.',
 'blackhawk-loop': 'A full backcountry loop from Hermosa Park. Climb the road to Bolam Pass, take the Colorado Trail over Blackhawk Pass, and drop Hotel Draw back to the car. Nearly 26 miles and 3,900 feet, with no shuttle.',
 'little-molas-hermosa-corral-draw': 'The big one. Fifty-three miles of the Colorado Trail from Little Molas Lake over Rolling Mountain and Bolam Pass, down Corral Draw and out Hermosa Creek. A full day for very fit riders, or two with support.',
}
HC_LEVEL = {'little-molas-hermosa-corral-draw': 'Expert', 'blackhawk-loop': 'Expert'}

def hc_track(slug):
    s = open(f'assets/routes/{slug}.gpx').read()
    pts = [(round(float(a), 5), round(float(b), 5)) for a, b in _re.findall(r'lat="([-\d.]+)" lon="([-\d.]+)"', s)]
    step = max(1, len(pts) // 400)
    return pts[::step] + ([pts[-1]] if (len(pts) - 1) % step else [])

def hc_level(r):
    return HC_LEVEL.get(r['slug'], 'Advanced')

def hc_page(r):
    lvl = hc_level(r)
    la, lo = r['start']; ela, elo = r['end']
    shuttle = ('Point to point. We book the shuttle with a licensed local company: drop at ' + r['trailhead'] + ', pickup at the finish.') if r['shuttle'] else 'A loop, back to the car. No shuttle needed.'
    stats = (f'<div class="rstats"><div><span>Distance</span><b>{r["miles"]} mi</b></div><div><span>Climbing</span><b>{r["climb"]:,} ft</b></div>'
             f'<div><span>High point</span><b>{r["high"]:,} ft</b></div><div><span>Shuttle</span><b>{"Yes" if r["shuttle"] else "No, loop"}</b></div></div>')
    gpx_btn = (f'<a class="btn" href="/assets/routes/{r["slug"]}.gpx" download>Download GPX</a> ' if HC_GPX_LIVE else '')
    faqs = [
        (f"How long is {r['name']}?", f"{r['miles']} miles with about {r['climb']:,} feet of climbing and {r['descent']:,} feet of descending. Most strong riders take {max(1.5, round(r['miles'] / 5 + r['climb'] / 1500, 1))} to {round(r['miles'] / 3.5 + r['climb'] / 1000, 1)} hours."),
        (f"When can you ride {r['name']}?", 'Usually mid-July to early October, once the snow is gone. Start early and be off the ridges by noon; summer afternoons bring lightning above treeline.'),
        (f"How hard is {r['name']}?", f"{lvl}. Everything here is above 10,000 feet, so riders coming from sea level should spend a day or two lower first." + (' This is a very long day with few bail-out points.' if lvl == 'Expert' else '')),
        ("Does it need a shuttle?", shuttle),
    ]
    coords = _json.dumps(hc_track(r['slug']), separators=(',', ':'))
    others = [o for o in HIGH_COUNTRY if o['slug'] != r['slug']]
    more = ''.join(f'<li><a href="/trails/{o["slug"]}">{o["name"]}</a> · {o["miles"]} mi · {o["climb"]:,} ft</li>' for o in others)
    body = f"""
  <section style="padding-bottom:24px">
    <div class="wrap narrow reveal">
      <p class="eyebrow"><a href="/trails#high-country" style="text-decoration:none">San Juan high country</a> · {r['area']}</p>
      <h1 class="display">{r['name']}</h1>
      <p class="lead">{HC_COPY[r['slug']]}</p>
      {stats}
    </div>
  </section>
  <section style="padding-top:0">
    <div class="wrap" style="max-width:1000px">
      <div id="hcmap" style="width:100%;aspect-ratio:1600/1024;border:1px solid var(--line);background:#F5F0E6"></div>
      <noscript><img src="/assets/routes/{r['slug']}.jpg" width="1600" height="1024" alt="Map of the {r['name']} route" style="width:100%;height:auto"></noscript>
      <div style="margin-top:20px">{profile_svg(r)}</div>
      <p style="margin-top:20px;display:flex;gap:12px;flex-wrap:wrap">{gpx_btn}<a class="btn btn-rust" href="/basecamp#inquire">Plan this ride with us</a> <a class="btn" href="https://www.google.com/maps/dir/?api=1&destination={la:.5f},{lo:.5f}" target="_blank" rel="noopener">Directions to the start</a></p>
    </div>
    <div class="wrap narrow article" style="margin-top:24px">
      <h2>The route</h2>
      <p>{r['route']}. {r['miles']} miles, about {r['climb']:,} feet up and {r['descent']:,} feet down, between {r['low']:,} and {r['high']:,} feet.</p>
      <p>{shuttle}</p>
      <h2>Riding up high</h2>
      <ul>
        <li>Start early. Plan to be off the ridges by noon from July through August.</li>
        <li>Bring a rain shell, a warm layer and more water and food than you think. Weather turns fast above 11,000 feet.</li>
        <li>Bikes are not allowed in the Weminuche Wilderness. This route stays outside it.</li>
        <li>New to altitude? Ride something in town on day one.</li>
      </ul>
      <h2>Quick answers</h2>
      {''.join(f'<h3 class="faq-q">{q}</h3><p>{a}</p>' for q, a in faqs)}
      <h2>More high-country rides</h2>
      <ul>{more}</ul>
      <p><a href="/trails">Ten rides closer to town</a> · <a href="/basecamp">Ophir Basecamp</a></p>
      <p class="fine">Route from OpenStreetMap trail data, elevation from USGS. Map tiles © OpenStreetMap contributors, SRTM, OpenTopoMap (CC-BY-SA). Trails, closures and snow change; check current conditions before you ride.</p>
    </div>
  </section>
"""
    js = ("<link rel=\"stylesheet\" href=\"https://unpkg.com/leaflet@1.9.4/dist/leaflet.css\">"
          "<script src=\"https://unpkg.com/leaflet@1.9.4/dist/leaflet.js\"></script><script>(function(){var c=" + coords + ";"
          "if(!window.L){document.getElementById('hcmap').innerHTML='<img src=\"/assets/routes/" + r['slug'] + ".jpg\" style=\"width:100%;height:auto\" alt=\"\">';return;}"
          "var m=L.map('hcmap',{scrollWheelZoom:false});"
          "L.tileLayer('https://{s}.tile.opentopomap.org/{z}/{x}/{y}.png',{maxZoom:17,attribution:'&copy; OpenStreetMap contributors, SRTM | &copy; OpenTopoMap (CC-BY-SA)'}).addTo(m);"
          "var l=L.polyline(c,{color:'#B4572B',weight:5,opacity:.95}).addTo(m);m.fitBounds(l.getBounds(),{padding:[24,24]});"
          "L.circleMarker(c[0],{radius:8,color:'#262422',fillColor:'#262422',fillOpacity:1}).addTo(m).bindTooltip('" + ('Start · finish' if not r['shuttle'] else 'Start') + "',{permanent:true,direction:'right'});"
          + ("" if not r['shuttle'] else "L.circleMarker(c[c.length-1],{radius:8,color:'#262422',weight:3,fillColor:'#F5F0E6',fillOpacity:1}).addTo(m).bindTooltip('Finish',{permanent:true,direction:'right'});")
          + "})();</script>")
    ld = {'@context': 'https://schema.org', '@graph': [
        {'@type': 'TouristAttraction', 'name': r['name'] + ' mountain bike route', 'description': HC_COPY[r['slug']],
         'url': 'https://ophirstays.com/trails/' + r['slug'], 'image': ['https://ophirstays.com/assets/routes/' + r['slug'] + '.jpg', 'https://ophirstays.com/assets/routes/' + r['slug'] + '-card.jpg'],
         'touristType': 'Mountain biking', 'isAccessibleForFree': True,
         'geo': {'@type': 'GeoCoordinates', 'latitude': la, 'longitude': lo},
         'containedInPlace': {'@type': 'Place', 'name': 'San Juan Mountains, Colorado'}},
        {'@type': 'BreadcrumbList', 'itemListElement': [
            {'@type': 'ListItem', 'position': 1, 'name': 'Ophir Stays', 'item': 'https://ophirstays.com/'},
            {'@type': 'ListItem', 'position': 2, 'name': 'Durango routes', 'item': 'https://ophirstays.com/trails'},
            {'@type': 'ListItem', 'position': 3, 'name': r['name'], 'item': 'https://ophirstays.com/trails/' + r['slug']}]},
        {'@type': 'FAQPage', 'mainEntity': [{'@type': 'Question', 'name': q, 'acceptedAnswer': {'@type': 'Answer', 'text': a}} for q, a in faqs]}]}
    html = page(f"{r['name']} · San Juan High-Country Mountain Bike Route · Ophir Stays",
                f"{r['name']} near Durango: {r['miles']} miles, {r['climb']:,} ft of climbing, high point {r['high']:,} ft. Route map, elevation profile and shuttle notes.",
                '/trails/' + r['slug'], 'journal', body, js, image='/assets/routes/' + r['slug'] + '-card.jpg')
    return html.replace('</head>', '<script type="application/ld+json">' + _json.dumps(ld) + '</script>\n</head>', 1)

hc_tiles = ''.join(ptile({**r, 'difficulty': hc_level(r)}) for r in HIGH_COUNTRY)

trails_index_body = f"""
  <section style="padding-bottom:32px">
    <div class="wrap narrow center reveal">
      <p class="eyebrow">Ride</p>
      <h1 class="display">Durango mountain bike routes</h1>
      <p class="lead">Ten rides from town, easy to advanced, each with a map, elevation profile and free GPX download. Every one starts within ten minutes of Main Avenue. Plus <a href="#high-country">seven high-country rides</a> up north.</p>
      <p style="margin-top:20px"><a class="btn" href="/trail-map">See the full trail map</a></p>
    </div>
  </section>
  <section style="padding-top:0">
    <div class="wrap"><div class="pgrid">{''.join(ptile(r) for r in sorted(ROUTES, key=lambda r: (DIFF_ORDER[r['difficulty']], r['miles'])))}</div></div>
  </section>
  <section class="tint" id="high-country">
    <div class="wrap narrow center reveal" style="margin-bottom:36px">
      <p class="eyebrow">The high country</p>
      <h2 class="display">Seven San Juan rides above 10,000 feet</h2>
      <p class="lead">From Coal Bank Pass, Molas Pass and Hermosa Park, 45 minutes north of town. Ridden mid-July to early October, started early, off the ridges by noon.</p>
    </div>
    <div class="wrap"><div class="pgrid">{hc_tiles}</div></div>
    <p class="fine center" style="margin-top:24px">Planning a trip around these? <a class="link" href="/basecamp">Ophir Basecamp</a> books the shuttles and plans the days.</p>
  </section>
  <section style="padding-top:0">
    <div class="wrap narrow article" style="margin-top:48px">
      <p>New to Durango? Start with the Meadow Loop to get used to the altitude, then work up to Telegraph and Sidewinder. Save Raider Ridge and Animas Mountain for when your legs and lungs have caught up.</p>
      <p class="fine">Routes from OpenStreetMap trail data, elevation from USGS. Trails and closures change; check current conditions before you ride.</p>
    </div>
  </section>
"""
trails_index = page('Durango Mountain Bike Routes: Maps, Elevation and GPX · Ophir Stays',
                    'Ten Durango mountain bike routes from town, easy to advanced: Horse Gulch, Raider Ridge, Animas Mountain, Overend, Twin Buttes, Log Chutes and more. Free maps, elevation profiles and GPX.',
                    '/trails', 'journal', trails_index_body, image='/assets/routes/telegraph-sidewinder-card.jpg').replace('</head>', '<script type="application/ld+json">' + _json.dumps({'@context': 'https://schema.org', '@type': 'ItemList', 'name': 'Durango mountain bike routes', 'itemListElement': [{'@type': 'ListItem', 'position': i + 1, 'url': 'https://ophirstays.com/trails/' + r['slug'], 'name': r['name']} for i, r in enumerate(sorted(ROUTES, key=lambda r: (DIFF_ORDER[r['difficulty']], r['miles'])))]}) + '</script>\n</head>', 1)


# ---------------- GUEST APP PREVIEW ----------------
guestapp_body = """
  <section style="padding-bottom:32px">
    <div class="wrap narrow center reveal">
      <p class="eyebrow">The guest app</p>
      <h1 class="display">Every stay arrives planned</h1>
      <p class="lead">Each Ophir guest gets a private trip page: what's ready when they arrive, every day planned around the forecast, add-ons they can book and pay for, and Ask Ophir for any question, any hour.</p>
    </div>
  </section>
  <section style="padding-top:0">
    <div class="wrap" style="max-width:1100px"><img src="/assets/guest-app-preview.jpg" width="2012" height="1300" alt="Four screens from the Ophir Stays guest app: arrival checklist, a day-by-day itinerary, suggested add-ons and Ask Ophir" style="width:100%;height:auto;display:block;border:1px solid var(--line)"></div>
    <div class="wrap narrow article" style="margin-top:32px">
      <p>A sample itinerary for a family ski week at a home near Purgatory. Every guest's page is built from what they tell us before they arrive, then adjusted as the weather changes.</p>
      <p><a href="/stay">See how a stay works</a> · <a href="/owners">For owners</a></p>
    </div>
  </section>
"""
guestapp = page('The Ophir Guest App · Ophir Stays', 'Every Ophir Stays guest gets a private trip page: arrival checklist, daily plans built around the forecast, add-ons and Ask Ophir.', '/guest-app', 'stay', guestapp_body, image='/assets/guest-app-preview.jpg')


estimate_body = f'''
  <section class="tint" id="estimate" style="padding-top:72px">
    <div class="wrap split top">
      <div class="reveal">
        <p class="eyebrow">Free earnings estimate</p>
        <h1 class="display">What could this home earn?</h1>
        <p class="lead">For owners and agents. Tell us about the home and within 24 hours you get a three-page report: expected rent month by month, what the owner keeps after every cost, comparable homes and our terms.</p>
        <p class="fine" style="margin-top:20px"><a href="/assets/ophir-earnings-estimate-sample.pdf">See a sample report</a></p>
        <p class="fine" style="margin-top:12px">Casey checks every number himself before it goes out. Questions? <a href="mailto:casey@ophirstays.com">casey@ophirstays.com</a> or 970-779-8992.</p>
      </div>
      <div class="reveal" id="estimate-box">
        {ESTIMATE_FORM}
        <div class="thanks" tabindex="-1"><svg aria-hidden="true"><use href="#summit"/></svg><h3>Thank you. We have your request.</h3><p style="color:var(--muted);margin:12px 0 0">Casey will check the numbers and email the report within 24 hours.</p></div>
      </div>
    </div>
  </section>
'''
estimate_page = page('Free Durango Vacation Rental Earnings Estimate · Ophir Stays', 'Owners and agents: tell us about a Durango home and get a free three-page earnings report within 24 hours, with monthly rent, what the owner keeps and comparable homes.', '/estimate', 'owners', estimate_body, FORM_JS)

# ---------------- BUYERS ----------------
BUY_FAQ = [
 ('Does it cost anything?', 'No. The estimate and the rental check are free, and you owe nothing unless you buy the home and sign with Ophir.'),
 ('Can you tell me if a home can rent nightly?', 'We check the parcel (city or county), the city permit status if it is in town, and the HOA covenants we can get. We tell you what we find and what to confirm in writing during your inspection period. It is not legal advice, and the final word is the HOA and the city.'),
 ('How fast can the home take guests after closing?', 'Usually two to four weeks: photos, linens, a smart lock, the gear room and listings. If you tell us your closing date early, we can have most of it lined up before you get the keys.'),
 ('I already have an agent. Does this change anything?', 'No. Keep your agent. We send the report to you, and to them if you like. Agents can also request it for you.'),
]
buy_faq_html = ''.join(f'<details><summary>{q}</summary><p>{a}</p></details>' for q,a in BUY_FAQ)
POST_LD['/buying'] = '<script type="application/ld+json">' + _json.dumps({"@context":"https://schema.org","@type":"FAQPage","mainEntity":[{"@type":"Question","name":q,"acceptedAnswer":{"@type":"Answer","text":a}} for q,a in BUY_FAQ]}) + '</script>'
buying_body = f"""
  <section class="center" style="padding-bottom:48px">
    <div class="wrap narrow reveal">
      <p class="eyebrow">For buyers</p>
      <h1 class="display">Buying a vacation rental in Durango?</h1>
      <hr class="rule">
      <p class="lead">Know what it will earn before you make an offer. Tell us about the home and within 24 hours you get a free earnings report from a local manager: rent month by month, what you keep after every cost, and whether the home can rent nightly at all.</p>
      <p style="margin-top:32px"><a class="btn btn-rust" href="#estimate">Get a free estimate</a></p>
    </div>
  </section>
  <div class="wrap">{photo('hero-fireplace', 'A great room with the fire lit at dusk in a Durango mountain home')}</div>

  <section>
    <div class="wrap narrow article">
      <h2>Three things to check before you offer</h2>
      <p><strong>1. City or county.</strong> Inside Durango city limits, nightly rentals need a city permit, the residential permits are capped with waitlists, and <strong>a permit ends when the home sells</strong>. If the listing says "great rental," ask whether the permit survives the sale. It doesn't. In unincorporated La Plata County there is no rental permit, only lodging and sales tax.</p>
      <p><strong>2. The HOA.</strong> In the county, the covenants are usually the real answer. Some of the area's best neighborhoods, including the Glacier Club, Edgemont and Sky Ridge, don't allow short-term rentals at all. Get it in writing from the HOA during your inspection period.</p>
      <p><strong>3. The seller's numbers.</strong> A seller's rental history reflects their manager, their pricing and how often they used the home themselves. We build your estimate from comparable Durango homes, then check it against the seller's numbers if you have them.</p>
      <p class="fine">More detail in <a href="/journal/durango-short-term-rental-rules">the full city and county rental rules</a>. A plain-English summary, not legal advice.</p>

      <h2>What you get</h2>
      <ul>
        <li><strong>A three-page earnings report within 24 hours.</strong> Expected rent by month, a range, and what you keep after booking fees, management, utilities, supplies and a repair reserve. <a href="/assets/ophir-earnings-estimate-sample.pdf">See a sample.</a></li>
        <li><strong>A rental check.</strong> City or county, permit status, and what we know about the HOA.</li>
        <li><strong>A setup list.</strong> What the home needs to rent well (hot tub, gear room, beds for a group) and roughly what it costs.</li>
        <li><strong>A manager lined up at closing.</strong> If you buy and choose Ophir, the home can be ready for guests within weeks of getting the keys, at our founding rate of 22% for the first ten homes.</li>
      </ul>
      <p>Casey Roberts runs Ophir and checks every number himself. He's lived in Durango for 23 years and rides, skis and fishes the places your guests will come for.</p>

      <h2>Questions buyers ask</h2>
      <div class="faq">{buy_faq_html}</div>
      <p class="fine" style="margin-top:20px">Agents: request a report for your buyer <a href="/estimate?role=agent">here</a>, or send them this page.</p>
    </div>
  </section>

  <section class="tint" id="estimate">
    <div class="wrap split top">
      <div class="reveal">
        <p class="eyebrow">Free earnings estimate</p>
        <h2 class="display">What could this home earn?</h2>
        <p class="lead">The address or listing link, bedrooms and asking price are enough to start. The more you tell us, the sharper the numbers.</p>
        <p class="fine" style="margin-top:20px">Questions? <a href="mailto:casey@ophirstays.com">casey@ophirstays.com</a> or 970-779-8992.</p>
      </div>
      <div class="reveal" id="estimate-box">
        {ESTIMATE_FORM.replace('id="estimate-form"', 'id="estimate-form" data-role="buyer"', 1)}
        <div class="thanks" tabindex="-1"><svg aria-hidden="true"><use href="#summit"/></svg><h3>Thank you. We have your request.</h3><p style="color:var(--muted);margin:12px 0 0">Casey will check the numbers and email your report within 24 hours.</p></div>
      </div>
    </div>
  </section>
"""
buying_page = page('Buying a Vacation Rental in Durango? Free Earnings Estimate · Ophir Stays',
                   'Buying a short-term rental in Durango, Colorado? Get a free earnings report within 24 hours from a local manager: monthly rent, what you keep, and whether the home can rent nightly.',
                   '/buying', 'owners', buying_body, FORM_JS, image='/assets/photos/hero-fireplace.jpg')

os.makedirs('journal', exist_ok=True); os.makedirs('homes', exist_ok=True); os.makedirs('trails', exist_ok=True)

# ---------------- AREA: PURGATORY ----------------
PURG_FAQ = [
 ('Can I rent my Purgatory condo or home nightly?', 'Usually yes. Unincorporated La Plata County, where Purgatory sits, has no short-term rental permit. The answer comes from your HOA covenants. Most resort condos and townhomes rent nightly today; Glacier Club homes do not. We check your documents before you sign anything.'),
 ('What does a Purgatory vacation home earn?', 'In our model, a 2-bedroom condo earns about $40,000 a year in rent, a 3-bedroom townhome with a hot tub about $64,000, and a 4-bedroom home with a hot tub and views about $94,000. About two-thirds of it comes in December through March. We send a free estimate for your home within 24 hours.'),
 ('I already have a manager. Can I switch in the middle of ski season?', 'Yes. We start the day after the last stay your current manager keeps, honor every reservation that moves to us, and handle the handoff. Many owners sign in the fall and start in January.'),
]
POST_LD['/areas/purgatory'] = '<script type="application/ld+json">' + _json.dumps({"@context":"https://schema.org","@graph":[
  {"@type":"Service","name":"Vacation rental management at Purgatory","serviceType":"Vacation rental management","provider":{"@type":"LocalBusiness","name":"Ophir Stays","url":"https://ophirstays.com","telephone":"+1-970-779-8992","address":{"@type":"PostalAddress","addressLocality":"Durango","addressRegion":"CO","postalCode":"81301","addressCountry":"US"}},"areaServed":{"@type":"Place","name":"Purgatory, Durango Mountain, Colorado"},"url":"https://ophirstays.com/areas/purgatory"},
  {"@type":"FAQPage","mainEntity":[{"@type":"Question","name":q,"acceptedAnswer":{"@type":"Answer","text":a}} for q,a in PURG_FAQ]},
  {"@type":"BreadcrumbList","itemListElement":[{"@type":"ListItem","position":1,"name":"Ophir Stays","item":"https://ophirstays.com/"},{"@type":"ListItem","position":2,"name":"For owners","item":"https://ophirstays.com/owners"},{"@type":"ListItem","position":3,"name":"Purgatory","item":"https://ophirstays.com/areas/purgatory"}]}]}) + '</script>'
purg_faq_html = ''.join(f'<details><summary>{q}</summary><p>{a}</p></details>' for q,a in PURG_FAQ)
purg_body = f"""
  <section class="center" style="padding-bottom:40px">
    <div class="wrap narrow reveal">
      <p class="eyebrow">Areas · Purgatory and Durango Mountain</p>
      <h1 class="display">Vacation rental management at Purgatory</h1>
      <p class="post-meta">By Casey Roberts · October 2026</p>
      <p class="fine" style="margin-top:14px">Looking for a place to stay? <a href="/purgatory-vacation-rentals">Where to stay at Purgatory Resort</a>.</p>
    </div>
  </section>
  <div class="wrap">{photo('hero-ski', 'Skiers touring below the San Juan peaks near Purgatory')}</div>
  <section style="padding-top:56px">
    <div class="wrap narrow article">
      <p><strong>Purgatory is the strongest rental market we serve. Most resort condos and homes can rent nightly, and about two-thirds of a home's year is earned from December through March. Here is what's allowed, what homes earn, and how we run them.</strong></p>

      <h2>Can you rent here?</h2>
      <p>Purgatory sits in unincorporated La Plata County. The county has no short-term rental permit, so the real answer is your HOA. This is where things stand for the neighborhoods we work in:</p>
      <div class="table-wrap"><table class="data wrap">
        <thead><tr><th scope="col">Neighborhood</th><th scope="col">Nightly rentals</th></tr></thead>
        <tbody>
          <tr><th scope="row">Purgatory Village condos (Angelhaus, Eolus, Needles, Sitzmark, Twilight View, Silverpick)</th><td>Yes</td></tr>
          <tr><th scope="row">Durango Mountain townhomes (Tacoma Village, Travertine, Alpenglow)</th><td>Yes</td></tr>
          <tr><th scope="row">Lake Purgatory, Lake of the Pines and Beaver Circle homes</th><td>Yes, check covenants</td></tr>
          <tr><th scope="row">Tamarron Lodge condos</th><td>Yes</td></tr>
          <tr><th scope="row">Glacier Club homes</th><td>No</td></tr>
          <tr><th scope="row">Cascade Village and homes north of the county line</th><td>San Juan County rules</td></tr>
        </tbody>
      </table></div>
      <p class="fine">"Yes" means homes in that neighborhood rent nightly today. Covenants differ by building and can change, so we read yours before you sign. Checked October 2026.</p>
      <p>Every stay owes the county's 2% lodging tax, 2% county sales tax and state sales tax. Airbnb and Vrbo collect some of these; we register for and remit the rest, including on direct bookings.</p>

      <h2>What a home here earns</h2>
      <div class="table-wrap"><table class="data">
        <thead><tr><th scope="col">Home</th><th scope="col">Rent a year</th><th scope="col">Owner keeps</th></tr></thead>
        <tbody>
          <tr><th scope="row">2-bedroom condo</th><td>$40,000</td><td>$18,200</td></tr>
          <tr><th scope="row">3-bedroom townhome, hot tub</th><td>$63,900</td><td>$28,700</td></tr>
          <tr><th scope="row">4-bedroom home, hot tub and views</th><td>$93,900</td><td>$47,600</td></tr>
        </tbody>
      </table></div>
      <p class="fine">From our estimate model for Purgatory. "Owner keeps" is after booking fees, Ophir's 22% founding rate, utilities, supplies, snow removal, a repair reserve and rental insurance, before mortgage and property tax. Your home will differ; your own estimate takes 24 hours.</p>
      <p>Winter carries the year. December through March brings in about two-thirds of the rent, July and August most of the rest. April, May and November are quiet, which is when we do the deep clean and the repairs, and when you can use the home yourself without costing much.</p>

      <h2>What guests come for</h2>
      <ul>
        <li>Ski days at Purgatory, with skis and boots sized and waiting in the gear room.</li>
        <li>Lift-served mountain biking and the alpine coaster in summer.</li>
        <li>Haviland Lake, Hermosa Creek Trail and the high passes toward Silverton.</li>
        <li>A hot tub at the end of the day. In our model it's one of the biggest lifts to a mountain home's rent.</li>
      </ul>

      <h2>Homes we take here</h2>
      <p>Every Ophir home meets one standard. At Purgatory that also means a ski room or closet for boots and gear, a plowed and reliable winter driveway, Wi-Fi of at least 100 Mbps, and beds for a group: most winter guests are families of six or more.</p>

      <h2>How we run a Purgatory home</h2>
      <ul>
        <li>The driveway is plowed and the walk cleared before every winter arrival.</li>
        <li>We check heat, heat tape and pipes in every cold snap, occupied or not.</li>
        <li>Rates move daily around holidays, spring break and powder forecasts.</li>
        <li>Guests are met on arrival, and their trip is planned before they come.</li>
        <li>Mud season brings a deep clean, a repair list for your approval and a photo report.</li>
      </ul>

      <h2>Questions owners ask</h2>
      <div class="faq">{purg_faq_html}</div>

      <p style="margin-top:36px"><a class="btn btn-rust" href="/owners#estimate">Get a free estimate for your Purgatory home</a></p>
      <p class="fine" style="margin-top:14px">Or read <a href="/journal/durango-short-term-rental-rules">the full city and county rental rules</a> and <a href="/owners">how Ophir works with owners</a>.</p>

      <h2 style="font-size:20px;margin-top:56px">Sources</h2>
      <p class="fine" style="margin:0">
        <a href="https://www.lpcgov.org/departments/finance___procurement/lodging_tax_information/be_a_good_neighbor_(vacation_rental).php" rel="noopener">La Plata County: Be a Good Neighbor (vacation rental)</a> (checked October 2026)<br>
        Neighborhood status from current nightly listings and HOA documents reviewed by Ophir, October 2026. This is a plain-English summary, not legal advice.
      </p>
    </div>
  </section>
"""
purg_page = page('Purgatory Vacation Rental Management for Owners · Ophir Stays',
                 'Vacation rental management at Purgatory and Durango Mountain: which condos and homes can rent nightly, what they earn, and how a local manager runs them.',
                 '/areas/purgatory', 'owners', purg_body, image='/assets/photos/hero-ski.jpg')

# ---------------- GUEST GUIDE: PURGATORY VACATION RENTALS ----------------
PG_FAQ = [
 ("How far is Purgatory from Durango?", "About 25 miles north on Highway 550, roughly 30 to 40 minutes by car in winter. Leave extra time on storm mornings; the road climbs over 2,000 feet."),
 ("Is it better to stay at Purgatory or in Durango?", "Stay at the mountain if skiing is the whole trip and you want to walk or drive five minutes to the lift. Stay in or near town if you want restaurants, the hot springs and a day or two off the slopes. Many families split it: a mountain home in the valley between the two."),
 ("When should I book a Purgatory vacation rental?", "For Christmas, New Year's, Presidents' Day and March spring break, book by early fall. January and early February are the quietest and best-value weeks of the season."),
 ("Does Ophir Stays have homes to book at Purgatory?", "Not yet. Our first homes open to guests in 2027. Join the list below and you'll hear first, with first pick of dates. Until then, we're happy to answer questions about where to stay."),
]
POST_LD['/purgatory-vacation-rentals'] = '<script type="application/ld+json">' + _json.dumps({"@context":"https://schema.org","@graph":[
  {"@type":"Article","headline":"Purgatory Resort vacation rentals: where to stay","datePublished":"2026-11-22","author":{"@type":"Person","name":"Casey Roberts","url":"https://ophirstays.com/about"},"publisher":{"@type":"Organization","name":"Ophir Stays"},"mainEntityOfPage":"https://ophirstays.com/purgatory-vacation-rentals"},
  {"@type":"FAQPage","mainEntity":[{"@type":"Question","name":q,"acceptedAnswer":{"@type":"Answer","text":a}} for q,a in PG_FAQ]}]}) + '</script>'
pg_faq_html = ''.join(f'<details><summary>{q}</summary><p>{a}</p></details>' for q,a in PG_FAQ)
pg_body = f'''
  <section class="center" style="padding-bottom:40px">
    <div class="wrap narrow reveal">
      <p class="eyebrow">For guests · Purgatory Resort</p>
      <h1 class="display">Purgatory Resort vacation rentals: where to stay</h1>
      <p class="post-meta">By Casey Roberts · November 2026</p>
    </div>
  </section>
  <div class="wrap"><div class="photo"><img src="/assets/photos/library/needles-alpenglow-purgatory.jpg" alt="Alpenglow on the Needle Mountains above homes near Purgatory Resort" loading="lazy"></div></div>
  <section style="padding-top:56px">
    <div class="wrap narrow article">
      <p><strong>Purgatory Resort sits 25 miles north of Durango on Highway 550. Where you stay decides your trip: slopeside condos for the most ski time, the valley in between for space, or town for restaurants and the hot springs. Here is how a local would choose.</strong></p>

      <h2>The four places to stay</h2>
      <div class="table-wrap"><table class="data wrap">
        <thead><tr><th scope="col">Where</th><th scope="col">To the lifts</th><th scope="col">Best for</th></tr></thead>
        <tbody>
          <tr><th scope="row">Purgatory Village, at the base</th><td>Walk</td><td>Ski-first trips and families who want to come in for lunch</td></tr>
          <tr><th scope="row">Durango Mountain homes and townhomes, just off the base</th><td>A few minutes by car or shuttle</td><td>Groups who want more room and a hot tub</td></tr>
          <tr><th scope="row">Cascade Village, a few minutes north</th><td>About 5 minutes</td><td>Quiet, views of the Needles, good value</td></tr>
          <tr><th scope="row">Tamarron and the valley toward Durango</th><td>15 to 30 minutes</td><td>Splitting the trip between skiing and town</td></tr>
        </tbody>
      </table></div>

      <h2>Purgatory Village</h2>
      <p>The condos at the base put you closest to the lifts: from many you can walk over in boots, and some let you ski back close to the door. It's the easiest choice with small kids. Evenings are quiet; most dinners mean a drive to Durango.</p>

      <h2>Homes and townhomes at Durango Mountain</h2>
      <p>The neighborhoods around the base, from the townhomes off the main road to the homes around Lake Purgatory, give a group more bedrooms, a kitchen worth cooking in and, often, a hot tub. Check whether a home is a drive or a walk to the lift before you book.</p>

      <h2>Cascade Village</h2>
      <p>A few minutes north of the base on Highway 550, under the Needle Mountains. Quieter than the village, with big views and condos that often cost less for the same space.</p>

      <h2>Tamarron, the valley and Durango</h2>
      <p>Staying farther south trades a short drive for everything else: Durango's restaurants on Main Avenue, Trimble Hot Springs, the train and a day off skiing that doesn't feel like a wait. From downtown, plan on 30 to 40 minutes each way.</p>

      <h2>What to look for in a Purgatory rental</h2>
      <ul>
        <li><strong>A place for gear:</strong> a ski room, boot dryers or at least a heated garage.</li>
        <li><strong>A plowed, reliable driveway</strong> and parking that fits your cars, and four-wheel drive or snow tires for the road.</li>
        <li><strong>Beds for your whole group.</strong> Many winter groups are six or more.</li>
        <li><strong>A hot tub.</strong> After a full ski day, it's the thing guests mention most.</li>
        <li><strong>Someone local to call</strong> if the heat or the hot water quits on a cold night.</li>
      </ul>

      <h2>When to book</h2>
      <p>The ski season usually runs from late November into early April. Christmas, New Year's, Presidents' Day and March spring break fill first, so book those by early fall. January and early February have the shortest lift lines and the best rates.</p>

      <h2>Make it a Durango trip</h2>
      <p>Mix in a day in town: <a href="/journal/where-to-eat-durango">where to eat in Durango</a>, the hot springs, and in summer the <a href="/trails">mountain bike routes</a> from town and the high country around the resort.</p>

      <h2>Questions guests ask</h2>
      <div class="faq">{pg_faq_html}</div>
    </div>
  </section>
  <section class="tint">
    <div class="wrap narrow">
      <form class="su reveal" id="guest-list" data-list="guest" data-source="purgatory-guide" novalidate>
        <p class="eyebrow">Ophir Stays</p>
        <h2 class="display">Our homes open in 2027.</h2>
        <p>Mountain homes near Purgatory and Durango, run by a local who skis here. Join the list for first pick of dates.</p>
        <div class="nl-row">
          <label class="sr" for="pg-email">Email</label><input id="pg-email" name="email" type="email" autocomplete="email" placeholder="Your email" required>
          <button class="btn btn-rust" type="submit">Join the list</button>
        </div>
        <div class="hp" aria-hidden="true"><input name="website" tabindex="-1" autocomplete="off"></div>
        <p class="nl-status" role="status" aria-live="polite"></p>
      </form>
      <p class="fine" style="margin-top:20px">Own a home at Purgatory? <a href="/areas/purgatory">Vacation rental management at Purgatory</a>.</p>
    </div>
  </section>
'''
pg_page = page('Purgatory Resort Vacation Rentals: Where to Stay (2026-27) · Ophir Stays',
               'Where to stay at Purgatory Resort near Durango, Colorado: slopeside condos, Durango Mountain homes, Cascade Village and the valley, with what each is like and when to book.',
               '/purgatory-vacation-rentals', 'stay', pg_body, SIGNUP_JS, image='/assets/photos/library/needles-alpenglow-purgatory.jpg')
os.makedirs('areas', exist_ok=True)

# ---------------- OWNER GUIDES + AREA PAGES (Nov 2026) ----------------
def lib(name, alt):
    return f'<div class="photo"><img src="/assets/photos/library/{name}.jpg" alt="{alt}" loading="lazy"></div>'

def guide_page(path, title, desc, eyebrow, h1, pic, body, faq=(), crumb='For owners', image='/assets/og.jpg', area=None):
    faq_html = ''.join(f'<details><summary>{q}</summary><p>{a}</p></details>' for q, a in faq)
    graph = [{"@type": "Article", "headline": h1, "datePublished": "2026-11-22", "author": {"@type": "Person", "name": "Casey Roberts", "url": "https://ophirstays.com/about"}, "publisher": {"@type": "Organization", "name": "Ophir Stays"}, "mainEntityOfPage": "https://ophirstays.com" + path},
             {"@type": "BreadcrumbList", "itemListElement": [{"@type": "ListItem", "position": 1, "name": "Ophir Stays", "item": "https://ophirstays.com/"}, {"@type": "ListItem", "position": 2, "name": crumb, "item": "https://ophirstays.com/owners"}, {"@type": "ListItem", "position": 3, "name": h1, "item": "https://ophirstays.com" + path}]}]
    if faq:
        graph.append({"@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in faq]})
    if area:
        graph.append({"@type": "Service", "name": f"Vacation rental management in {area}", "serviceType": "Vacation rental management", "provider": {"@type": "LocalBusiness", "name": "Ophir Stays", "url": "https://ophirstays.com", "telephone": "+1-970-779-8992"}, "areaServed": {"@type": "Place", "name": f"{area}, Colorado"}, "url": "https://ophirstays.com" + path})
    POST_LD[path] = '<script type="application/ld+json">' + _json.dumps({"@context": "https://schema.org", "@graph": graph}) + '</script>'
    html_body = f'''
  <section class="center" style="padding-bottom:40px">
    <div class="wrap narrow reveal">
      <p class="eyebrow">{eyebrow}</p>
      <h1 class="display">{h1}</h1>
      <p class="post-meta">By Casey Roberts · November 2026</p>
    </div>
  </section>
  <div class="wrap">{pic}</div>
  <section style="padding-top:56px">
    <div class="wrap narrow article">
{body}
      {('<h2>Questions owners ask</h2><div class="faq">' + faq_html + '</div>') if faq else ''}
      <p style="margin-top:36px"><a class="btn btn-rust" href="/owners#estimate">Get a free estimate</a></p>
      <p class="fine" style="margin-top:14px">Related: <a href="/journal/durango-short-term-rental-rules">city and county rental rules</a> · <a href="/journal/la-plata-county-short-term-rental-permit">La Plata County rentals, step by step</a> · <a href="/journal/switch-rental-managers-durango">how to switch managers</a> · <a href="/owner-checklist">the statement checklist</a></p>
    </div>
  </section>
'''
    return page(title, desc, path, 'owners', html_body, image=image)

AREA_NOTE = '<p class="fine">A plain-English summary from a local manager, not legal advice. HOA covenants differ by subdivision and change; we read yours before you sign anything. Checked November 2026.</p>'

# --- How to switch managers
SWITCH_FAQ = [
 ("Will I lose my reviews if I switch?", "It depends on whose account the listing lives on. If your Airbnb or Vrbo listing is under your own account, the reviews stay with you and we join as co-host. If it lives on your manager's account, the reviews usually stay with them, and your home starts a new listing. Ask your manager which it is before you give notice."),
 ("What happens to stays already booked?", "Every one is honored. Depending on your contract, your current manager either finishes the stays they booked, and we block those dates, or the reservations move to us. Either way the guest arrives to a home that's ready."),
 ("How long does a switch take?", "Most take 30 to 60 days from notice: your contract's notice period, then a week or two to photograph the home, set up the listing and stock it."),
 ("When is the best time to switch?", "In Durango, April to May or October to November. The calendar is quiet, so fewer stays are in the handoff and the home is ready before ski season or summer."),
 ("What does it cost to leave Ophir?", "Nothing. Thirty days' notice, no exit fee."),
]
switch_body = '''      <p><strong>Switching rental managers in Durango usually takes 30 to 60 days and costs nothing if you plan it around your contract. The work is in five places: your contract, your calendar, your listing, your home and your taxes. Here is how to handle each, in order.</strong></p>

      <h2>1. Read your contract first</h2>
      <p>Find four things before you say anything to anyone:</p>
      <ul>
        <li><strong>The notice period.</strong> Contracts commonly ask for 30 to 90 days, in writing.</li>
        <li><strong>Any termination fee.</strong> Some charge one in the first year, or a flat fee to leave.</li>
        <li><strong>Future bookings.</strong> Who keeps the stays already on the calendar, and whether the old manager earns a fee on them after you leave.</li>
        <li><strong>Who owns the listing.</strong> Whether your Airbnb and Vrbo listings, photos and reviews sit under your account or the manager's.</li>
      </ul>
      <p>Not sure what yours says? Send it to us and we'll read it with you before you decide anything.</p>

      <h2>2. Pick a start date</h2>
      <p>The best switches land in a quiet stretch: April to May, or October to November. Count back your notice period from that date, then give notice in writing. Email is usually enough; your contract says.</p>

      <h2>3. Plan for the stays already booked</h2>
      <p>Guests who booked your home should never feel the change. There are two common ways it goes:</p>
      <ul>
        <li><strong>Your old manager finishes their bookings.</strong> They host the stays they booked, and your new manager blocks those dates so nothing double-books.</li>
        <li><strong>The bookings move.</strong> Reservations transfer to the new manager, who contacts each guest with check-in details.</li>
      </ul>
      <p>At Ophir, every existing booking is honored either way, and the stays your old manager finishes count toward your first-year take-home under our guarantee.</p>

      <h2>4. Sort out the listing and the reviews</h2>
      <p>If the listing is on your own account, the switch is simple: the old manager is removed as co-host and the new one is added, and your reviews stay. If it's on the manager's account, your home will likely start a new listing. That costs some momentum for a few months, which is why good photos and early pricing matter most in the first season.</p>

      <h2>5. Hand over the home</h2>
      <ul>
        <li>Keys, garage remotes and lock codes. Change every code on the day of the switch.</li>
        <li>An inventory of what you own: linens, kitchen, gear, hot tub chemicals.</li>
        <li>Vendor contacts: cleaner, snow removal, hot tub, propane, trash.</li>
        <li>Your owner statements for the last twelve months. They set your baseline for our guarantee.</li>
      </ul>

      <h2>6. Update your taxes</h2>
      <p>Whoever collects lodging and sales tax on direct bookings changes with the manager. Make sure your old manager files through their last month, and your new one is registered from the first. In unincorporated La Plata County that means the state sales tax license that covers county sales and lodging tax; inside city limits, the city's taxes too.</p>

      <h2>A switch timeline</h2>
      <div class="table-wrap"><table class="data wrap">
        <thead><tr><th scope="col">When</th><th scope="col">What happens</th></tr></thead>
        <tbody>
          <tr><th scope="row">Week 1</th><td>Read the contract, pick a start date, get a free estimate and a copy of last year's statements.</td></tr>
          <tr><th scope="row">Week 1 to 2</th><td>Sign with the new manager and give written notice to the old one.</td></tr>
          <tr><th scope="row">During notice</th><td>Walkthrough, photos, listing setup. Booked stays are mapped and blocked.</td></tr>
          <tr><th scope="row">Start date</th><td>Codes change, the new listing goes live, the first guest is welcomed.</td></tr>
        </tbody>
      </table></div>
'''
switch_page = guide_page('/journal/switch-rental-managers-durango',
    'How to Switch Vacation Rental Managers in Durango · Ophir Stays',
    'Switching vacation rental managers in Durango, Colorado: your contract, booked stays, your listing and reviews, keys, taxes and a 30 to 60 day timeline, from a local manager.',
    'Owners', 'How to switch vacation rental managers in Durango', photo('hero-fireplace', 'A great room with the fire lit in a Durango mountain home'),
    switch_body, SWITCH_FAQ, image='/assets/photos/hero-fireplace.jpg')

# --- La Plata County permits, step by step
PERMIT_FAQ = [
 ("Do I need a short-term rental permit in La Plata County?", "Not outside city limits, as of November 2026. Unincorporated La Plata County has no short-term rental permit or license. You do need a Colorado sales tax license to collect state and county sales tax and the county lodging tax, and your HOA has to allow it. The county lists short-term rental rules as a future code amendment, targeted for the third quarter of 2027."),
 ("Is my home in the city or the county?", "Look up your parcel on the La Plata County assessor's map. An address that says Durango can still be in the county: most of the Animas Valley, Hermosa and Purgatory are."),
 ("Do Airbnb and Vrbo collect the taxes for me?", "On their own bookings, they collect and remit some or all of the state and local taxes. Check each platform's tax page for your address, and remit anything they don't collect. Direct bookings are always yours, or your manager's, to collect."),
]
permit_body = '''      <p><strong>There is no short-term rental permit in unincorporated La Plata County, as of November 2026. What you need is a Colorado sales tax license, your HOA's permission and a home that meets the county's good-neighbor guidelines. Inside Durango city limits it's different: you need a city permit first, and most are capped. Here are the steps for each.</strong></p>

      <h2>Step 1: City or county?</h2>
      <p>Everything depends on this. Look up your parcel on the La Plata County assessor's map. A Durango mailing address doesn't mean the city: most of the Animas Valley, Hermosa and the Purgatory area are unincorporated county.</p>

      <h2>In the county: five steps</h2>
      <ol>
        <li><strong>Get your HOA's answer in writing.</strong> In the county, covenants are usually the real rule. Some subdivisions ban stays under 30 days; others set their own registration.</li>
        <li><strong>Get a Colorado sales tax license.</strong> It's issued by the Colorado Department of Revenue, online. The state collects state sales tax, the county's 2% sales tax and the county lodging tax through it.</li>
        <li><strong>Check what the platforms collect.</strong> Airbnb and Vrbo collect some taxes on their own bookings. You file and remit the rest, including every direct booking.</li>
        <li><strong>Set the home up as the county recommends.</strong> A local contact who answers, shared with neighbors. Two guests per bedroom plus one. Parking on the property. Trash that keeps up. If you're on septic, ask La Plata County Public Health whether it can handle rental use.</li>
        <li><strong>Insure it for rental.</strong> Most homeowner's policies exclude short-term rental use. Get a policy that covers it.</li>
      </ol>
      <p>Hosting an event of 50 people or more, such as a wedding? That needs a separate county event permit.</p>

      <h2>Inside Durango city limits</h2>
      <ol>
        <li><strong>Check your zone.</strong> The city allows vacation rentals (stays of 1 to 29 nights) only in certain zones, and caps the permits in the main residential ones. Those caps are full, with waitlists.</li>
        <li><strong>Apply for a Limited Use Permit</strong> before you advertise, and get a city business license.</li>
        <li><strong>Register for city lodgers and sales taxes</strong> as well as the state license.</li>
        <li><strong>Know the permit doesn't transfer.</strong> A sale ends it, and a buyer starts again.</li>
      </ol>
      <p>Stays of 30 nights or more aren't regulated as vacation rentals by the city.</p>

      <h2>What could change</h2>
      <p>La Plata County lists short-term rentals among its planned code amendments, with a target of the third quarter of 2027. Nothing has been proposed in detail yet. If you're buying a home for its rental income, plan as if a county registration or permit could come, and watch for public hearings.</p>

      <h2>How Ophir handles it</h2>
      <p>Before we sign a home, we confirm city or county, read the HOA documents and check septic and parking. Once it's live, we hold the tax registration for direct bookings, remit monthly and act as the local contact.</p>

      <h2 style="font-size:20px;margin-top:48px">Sources</h2>
      <p class="fine" style="margin:0">
        <a href="https://www.lpcgov.org/services/community_development_services/planning/long_range_planning/code_amendments.php" rel="noopener">La Plata County: planned code amendments</a> (short-term rentals, target Q3 2027; checked November 2026)<br>
        <a href="https://cohost.freshdesk.com/support/solutions/articles/48000493608-la-plata-county-short-term-rental-guidelines" rel="noopener">La Plata County short-term rental guidelines, as summarized by a local manager</a><br>
        <a href="https://www.19pine.ai/short-term-rental-laws/colorado/durango/limited-use-permit" rel="noopener">City of Durango Limited Use Permit steps</a><br>
        A plain-English summary, not legal or tax advice. Confirm with the county, the city, the Colorado Department of Revenue and your HOA.
      </p>
'''
permit_page = guide_page('/journal/la-plata-county-short-term-rental-permit',
    'La Plata County Short-Term Rental Permit: Step by Step (2026) · Ophir Stays',
    "Do you need a short-term rental permit in La Plata County, Colorado? Not outside city limits, as of November 2026. The tax license, HOA, county guidelines and Durango city permit, step by step.",
    'Owners', 'La Plata County short-term rental permits, step by step', photo('home-1', 'A mountain home outside Durango in La Plata County'),
    permit_body, PERMIT_FAQ)

# --- Area pages
def area_body(lead, rent, guests, homes):
    return f'''      <p><strong>{lead}</strong></p>
      <h2>Can you rent here?</h2>
      {rent}
      {AREA_NOTE}
      <h2>What guests come for</h2>
      <ul>{''.join(f'<li>{g}</li>' for g in guests)}</ul>
      <h2>How we run a home here</h2>
      <ul>{''.join(f'<li>{h}</li>' for h in homes)}</ul>
      <p>Want numbers for your home? Our free estimate shows expected rent by month and what you keep, within 24 hours.</p>
'''

hermosa_page = guide_page('/areas/hermosa', 'Hermosa Vacation Rental Management · Ophir Stays',
    'Vacation rental management in Hermosa, north of Durango, Colorado: whether you can rent nightly, what guests come for, and how a local manager runs a Hermosa home.',
    'Areas · Hermosa', 'Vacation rental management in Hermosa', lib('bike-overlook', 'A mountain biker above the Animas Valley north of Durango'),
    area_body("Hermosa sits about ten miles north of downtown Durango on Highway 550, halfway between town and Purgatory. Homes here have room: acreage, valley views and space for gear. That makes them some of the best Basecamp homes we know.",
      '<p>Hermosa is unincorporated La Plata County, so there is no rental permit. You need a state sales tax license for county sales and lodging tax, and your HOA or covenants decide the rest. Many Hermosa homes sit on acreage with no HOA at all.</p>',
      ['Hermosa Creek Trail, one of the best long rides in Colorado, starting minutes away.',
       'Purgatory in about 20 minutes, without paying resort prices to stay at the base.',
       'Downtown Durango in 15 minutes for dinner.',
       'The Durango and Silverton train running up the valley below.'],
      ['Snow cleared from the drive and walks before every winter arrival.',
       'Septic and well checked before we list, and on a schedule after.',
       'A gear room set up for bikes in summer and skis in winter.',
       'Rates priced around Purgatory holidays and summer trail season.']),
    area='Hermosa')

valley_page = guide_page('/areas/animas-valley', 'Animas Valley Vacation Rental Management · Ophir Stays',
    'Vacation rental management in the Animas Valley north of Durango, Colorado: rental rules, what guests come for, and how a local manager runs a valley home.',
    'Areas · Animas Valley', 'Vacation rental management in the Animas Valley', lib('son-durango-overlook', 'Looking down on Durango and the Animas Valley'),
    area_body("The Animas Valley runs north from Durango along the river, with homes on the West Side Road, East Animas Road and Highway 550. It's the quiet side of a Durango stay: big views, the river, and town ten minutes away.",
      '<p>Most of the valley is unincorporated La Plata County, so there is no county rental permit. A few homes near the north edge of town are inside city limits, where a city permit applies and most are capped. Look up your parcel, then check your covenants: some valley subdivisions limit short stays.</p>',
      ['The Animas River for fishing, floating and the river trail into town.',
       'Trimble Hot Springs, a few minutes up the valley from town.',
       'Purgatory in about 30 minutes, downtown in 10.',
       'The Durango and Silverton train passing through the valley.'],
      ['Snow removal on the drive and walks before every winter arrival.',
       'Irrigation, well and septic checks on homes that have them.',
       'Pricing around river season, fall colors and ski holidays.',
       'A local host who meets guests and plans their trip.']),
    area='Animas Valley')

cascade_page = guide_page('/areas/cascade', 'Cascade Village Vacation Rental Management · Ophir Stays',
    'Vacation rental management at Cascade Village and the Purgatory area north of Durango, Colorado: which county, rental rules, what guests come for and how a local manager runs a condo here.',
    'Areas · Cascade and Purgatory', 'Vacation rental management at Cascade Village', lib('needles-alpenglow-purgatory', 'Alpenglow on the Needle Mountains above homes near Purgatory'),
    area_body("Cascade Village sits a few minutes north of Purgatory on Highway 550, under the Needle Mountains. Condos here earn most of the year in ski season, with a strong summer behind it.",
      '<p>Cascade Village sits near the line between La Plata and San Juan counties, and the county decides which rules and taxes apply. Check your parcel on the assessor\'s map. San Juan County sets its own rules and taxes, and we confirm the current requirements with the county before we take on a Cascade home. Then the condo association decides whether nightly stays are allowed. Most Cascade Village condos rent nightly today.</p><p>For the rest of the mountain, see <a href="/areas/purgatory">vacation rental management at Purgatory</a>.</p>',
      ['Ski days at Purgatory, minutes away.',
       'The San Juan Skyway north to Silverton and Ouray.',
       'Summer hiking, biking and fishing at the edge of the Weminuche.',
       'Quiet: no resort base crowds outside the door.'],
      ['The walk cleared and heat checked before every winter arrival.',
       'Heat tape and pipes checked in every cold snap, occupied or not.',
       'Rates moved daily around holidays, spring break and powder forecasts.',
       'A deep clean and a repair report every mud season.']),
    area='Cascade Village, Durango Mountain')

# --- Landing page for mailed letters (QR code target)
LETTER_FORM = ESTIMATE_FORM.replace('name="source" placeholder="A friend, an agent, a letter…"', 'name="source" value="Letter from Casey"').replace('<option>Yes, with a manager</option>', '<option selected>Yes, with a manager</option>', 1)
letter_body = f'''
  <section class="center" style="padding-bottom:40px">
    <div class="wrap narrow reveal">
      <p class="eyebrow">You got my letter</p>
      <h1 class="display">Thanks for scanning.</h1>
      <hr class="rule">
      <p class="lead">I'm Casey Roberts. I've lived in Durango for 23 years, and I run Ophir Stays, a local rental manager capped at twenty-five homes. Here's the short version, and a two-minute form for your free estimate.</p>
    </div>
  </section>
  <section style="padding-top:0">
    <div class="wrap">
      <div class="offer-grid">
        <div class="ocard"><p class="eyebrow">Keep more</p><h3 class="display">22%, locked for life.</h3><p>Our founding rate for the first ten homes. If you take home less in your first year than the year before, we refund the difference, up to our full fee.</p><a class="link" href="/owners#guarantee">How the guarantee works</a></div>
        <div class="ocard"><p class="eyebrow">Switch easily</p><h3 class="display">Every booked stay honored.</h3><p>Thirty days' notice to leave, no fee, no long contract. Here's <a href="/journal/switch-rental-managers-durango">how a switch works</a>, step by step.</p><a class="link" href="/owner-checklist">Check your current statement</a></div>
      </div>
    </div>
  </section>
  <section class="tint" id="estimate">
    <div class="wrap split top">
      <div class="reveal">
        <p class="eyebrow">Free estimate</p>
        <h2 class="display">What would you keep with Ophir?</h2>
        <p class="lead">Send last year's rent if you have it, and I'll show you, line by line, what you would have kept. If I don't think we can do better, I'll tell you that too.</p>
        <p class="fine" style="margin-top:20px">Or call or text me: 970-779-8992 · <a href="mailto:casey@ophirstays.com">casey@ophirstays.com</a></p>
      </div>
      <div class="reveal" id="estimate-box">
        {LETTER_FORM}
        <div class="thanks" tabindex="-1"><svg aria-hidden="true"><use href="#summit"/></svg><h3>Thank you. I have your request.</h3><p style="color:var(--muted);margin:12px 0 0">I'll check the numbers myself and email your estimate within 24 hours.</p></div>
      </div>
    </div>
  </section>
'''
letter_page = page('Your Letter from Ophir Stays · Free Estimate', 'For Durango owners who received a letter from Casey Roberts at Ophir Stays: the founding rate, the guarantee and a free estimate.',
                   '/letter', 'owners', letter_body, FORM_JS).replace('<meta name="viewport"', '<meta name="robots" content="noindex">\n<meta name="viewport"', 1)

os.makedirs('areas', exist_ok=True)
for name, html in [('index.html', home), ('owners.html', owners), ('about.html', about), ('journal.html', journal), ('journal/durango-rides.html', post), ('journal/durango-home-earnings.html', post2), ('journal/where-to-eat-durango.html', post3), ('journal/durango-short-term-rental-rules.html', post4), ('trail-map.html', trailmap), ('trails.html', trails_index), ('guest-app.html', guestapp), ('estimate.html', estimate_page), ('homes.html', homes_page), ('stay.html', stay_page), ('areas/purgatory.html', purg_page), ('basecamp.html', basecamp_page), ('buying.html', buying_page), ('owner-checklist.html', checklist_page), ('journal/switch-rental-managers-durango.html', switch_page), ('journal/la-plata-county-short-term-rental-permit.html', permit_page), ('areas/hermosa.html', hermosa_page), ('areas/animas-valley.html', valley_page), ('areas/cascade.html', cascade_page), ('letter.html', letter_page), ('purgatory-vacation-rentals.html', pg_page)] + [(f"homes/{h['slug']}.html", home_page(h)) for h in LIVE_HOMES] + [(f"trails/{r['slug']}.html", route_page(r)) for r in ROUTES] + [(f"trails/{r['slug']}.html", hc_page(r)) for r in HIGH_COUNTRY]:
    open(name, 'w').write(html)
open('sitemap.xml', 'w').write('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:image="http://www.google.com/schemas/sitemap-image/1.1">\n' +
    ''.join(f'<url><loc>https://ophirstays.com{p}</loc><lastmod>2026-10-18</lastmod>' + ('<image:image><image:loc>https://ophirstays.com/assets/ophir-durango-trail-map.jpg</image:loc></image:image>' if p == '/trail-map' else ''.join(f'<image:image><image:loc>https://ophirstays.com/assets/routes/{p[8:]}{x}.jpg</image:loc></image:image>' for x in ('', '-card')) if p.startswith('/trails/') else '') + '</url>\n' for p in ['/', '/stay', '/homes', '/owners', '/about', '/journal', '/journal/durango-rides', '/journal/durango-home-earnings', '/journal/where-to-eat-durango', '/journal/durango-short-term-rental-rules', '/trail-map', '/trails', '/guest-app', '/estimate', '/areas/purgatory', '/basecamp', '/buying', '/owner-checklist', '/journal/switch-rental-managers-durango', '/journal/la-plata-county-short-term-rental-permit', '/areas/hermosa', '/areas/animas-valley', '/areas/cascade', '/purgatory-vacation-rentals'] + [f"/trails/{r['slug']}" for r in ROUTES + HIGH_COUNTRY] + [f"/homes/{h['slug']}" for h in HOMES if not h['sample']]) + '</urlset>\n')
print('built')
