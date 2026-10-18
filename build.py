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

def head(title, desc, path, image='/assets/og.jpg'):
    return f'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{desc}">
<link rel="canonical" href="https://ophirstays.com{path}">
{LD if path == "/" else POST_LD.get(path, "")}
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
</head>
<body>
<a class="skip" href="#main">Skip to content</a>
{DEFS}'''

def masthead(current):
    items = ''.join(
        f'<li><a href="{h}"{" aria-current=\"page\"" if k == current else ""}><b>{t}</b><i>{s}</i></a></li>'
        for h, t, s, k in NAV)
    return f'''<div class="topbar"><div class="wrap"><span>Durango · Colorado</span><a href="/owners#estimate">Owner inquiry →</a></div></div>
<header class="masthead">
  <a class="logo" href="/" aria-label="Ophir Stays, home">
    <svg aria-hidden="true"><use href="#summit"/></svg>
    <span class="word">OPHIR</span>
    <span class="sub">STAYS</span>
  </a>
</header>
<nav class="mainnav" aria-label="Main">
  <button class="menu-btn" aria-expanded="false" aria-controls="navlist">MENU</button>
  <ul id="navlist">{items}</ul>
</nav>'''

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
    <nav class="foot-links" aria-label="Footer"><a href="/stay">Your Stay</a><a href="/owners">Owners</a><a href="/journal">Journal</a><a href="/about">About</a><a href="mailto:casey@ophirstays.com">casey@ophirstays.com</a></nav>
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

def page(title, desc, path, current, body, extra_js=''):
    return head(title, desc, path) + masthead(current) + '\n<main id="main">\n' + body + '\n</main>\n' + FOOT + extra_js + '\n</body>\n</html>\n'

def photo(name, alt, cls='photo'):
    return f'<div class="{cls}"><img src="/assets/photos/{name}.jpg" alt="{alt}" loading="lazy"></div>'


# ---------------- THE COLLECTION (homes) ----------------
# Add a home: copy a block, set sample=False, and save 5 photos as assets/photos/homes/<slug>-1.jpg ... -5.jpg
# (1 = hero exterior or view, 2 = great room, 3 = kitchen, 4 = primary bedroom, 5 = hot tub / deck / view).
# SHOW_SAMPLES must be False before launch so no sample home is ever published.
SHOW_SAMPLES = False
HOMES = [
    dict(slug='sample-cliff-house', sample=True, name='The Cliff House', area='Glacier Club', beds=5, baths=5.5, sleeps=12,
         line='Stone, glass and a fairway view, twenty minutes from town.',
         features=['Hot tub on a deck facing the cliffs', 'Wood-burning stone fireplace', 'Gear room with boot dryers and bike storage',
                   'Chef\'s kitchen with a six-burner range', 'Golf cart for the course'],
         trip='Tee times held, a morning ride in Haflin Canyon, dinner on Main Avenue with the first round on us.'),
]
LIVE_HOMES = [h for h in HOMES if SHOW_SAMPLES or not h['sample']]

def hphoto(slug, n, alt, cls='photo'):
    return f'<div class="{cls}"><img src="/assets/photos/homes/{slug}-{n}.jpg" alt="{alt}" loading="lazy"></div>'

def home_card(h):
    tag = '<span class="sample-tag" style="margin:14px 0 0">SAMPLE</span>' if h['sample'] else ''
    return f'''<a class="card reveal" href="/homes/{h['slug']}">{hphoto(h['slug'], 1, h['name'] + ', ' + h['area'], 'ph')}{tag}
        <p class="post-meta">{h['area']} · {h['beds']} bedrooms · sleeps {h['sleeps']}</p><h3><span class="ital">{h['name']}</span></h3><p>{h['line']}</p></a>'''

FOUNDING = '''<div class="band reveal" style="grid-template-columns:1fr auto">
        <div><p class="eyebrow">Founding homes</p><h2 class="display">The first homes join the Collection in 2027.</h2>
        <p>Twenty-five places, chosen one at a time. Own a home in Durango that meets the standard?</p></div>
        <a class="btn btn-rust" href="/owners#estimate">Apply</a></div>'''

def collection_grid():
    return f'<div class="grid3">{"".join(home_card(h) for h in LIVE_HOMES)}</div>' if LIVE_HOMES else FOUNDING

# ---------------- HOME ----------------
SLIDES = [('hero-ski', 'Winter', 'First chair, fresh snow, home by the fire.', 'Purgatory village at night beneath snow-covered peaks'),
          ('hero-bike', 'Summer', 'High passes, big days, home for dinner.', 'A mountain biker climbing a high pass in the San Juan Mountains'),
          ('hero-golf', 'Play', 'Tee times held, clubs waiting.', 'A striped fairway framed by autumn aspens below a sandstone cliff'),
          ('hero-fireplace', 'Evenings', 'The fire is lit before you arrive.', 'A great room with a stone fireplace lit at dusk'),
          ('hero-spa', 'Restore', 'A hot tub, a view and nowhere to be.', 'A steaming wood-fired hot tub on a deck at sunset'),
          ('hero-coffee', 'Mornings', 'Your coffee order, already known.', 'A latte and pastry by the fire in a mountain café')]

slides = ''.join(f'''<figure class="slide{' on' if i == 0 else ''}" aria-roledescription="slide" aria-label="{i+1} of {len(SLIDES)}">
      <img src="/assets/photos/{n}.jpg" alt="{alt}"{' fetchpriority="high"' if i == 0 else ' loading="lazy"'}>
      <figcaption class="cap"><span>{k}</span><p>{c}</p></figcaption></figure>''' for i, (n, k, c, alt) in enumerate(SLIDES))
thumbs = ''.join(f'<button type="button" aria-label="Show slide {i+1}: {k}"{" aria-current=\"true\"" if i == 0 else ""}><img src="/assets/photos/t/{n}.jpg" alt="" loading="lazy"></button>' for i, (n, k, c, a) in enumerate(SLIDES))

EXPS = [('ski', 'Ski', 'Purgatory is thirty minutes up the valley. Rentals fitted at the house, lift tickets waiting, boots warm in the dryer.'),
        ('spa', 'Spa', 'Hot springs, in-home massage and a hot tub at every home. We book the treatments; you choose the hour.'),
        ('golf', 'Golf', 'Tee times arranged at the best courses in the valley, with a cart and a cooler ready when you arrive.'),
        ('bike', 'Mountain bike', 'Some of the best singletrack in the West. Bikes sized to each rider and delivered, routes picked for your level.'),
        ('coffee', 'Coffee & town', 'Main Avenue, its cafés and its kitchens. Your table is held and the first round is on us.'),
        ('fireplace', 'Fireside', 'Evenings at the house: firewood stacked, blankets out, a bottle chosen for the night.')]
exps = ''.join(f'''<a class="card reveal" href="/owners#estimate" style="pointer-events:none">
        {photo(n, t + ' in Durango', 'ph')}
        <h3><span class="ital">{t}</span></h3><p>{d}</p></a>''' for n, t, d in EXPS)

home_body = f'''
  <div class="wrap">
    <div class="show" id="show" aria-roledescription="carousel" aria-label="Life at Ophir">
      <div class="slides">{slides}
        <button class="arrow prev" type="button" aria-label="Previous slide"><svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6"><path d="M15 5l-7 7 7 7"/></svg></button>
        <button class="arrow next" type="button" aria-label="Next slide"><svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6"><path d="M9 5l7 7-7 7"/></svg></button>
      </div>
      <div class="thumbs">{thumbs}</div>
    </div>
  </div>

  <section class="center">
    <div class="wrap narrow reveal">
      <p class="eyebrow">Durango · Colorado</p>
      <h1 class="display">A private collection of mountain homes.</h1>
      <hr class="rule">
      <p class="lead">Twenty-five homes in the San Juans, each kept to one standard, each stay with the whole trip handled. Locally owned, by people who live here.</p>
    </div>
    <div class="wrap">
      <div class="pillars reveal">
        <div class="pillar"><div class="num">i.</div><h3>THE HOMES</h3><p>Hotel-grade linens, a hot tub or a view, a gear room. Inspected before every arrival.</p></div>
        <div class="pillar"><div class="num">ii.</div><h3>THE TRIP</h3><p>Tell us what you love. Gear delivered, guides booked, tables held. The plan moves with the weather.</p></div>
        <div class="pillar"><div class="num">iii.</div><h3>THE CARE</h3><p>A real person, twenty-three years in Durango, answering within fifteen minutes.</p></div>
      </div>
    </div>
  </section>

  <section id="collection" style="padding-top:0">
    <div class="wrap">
      <div class="center reveal" style="margin-bottom:52px">
        <p class="eyebrow">The Collection</p>
        <h2 class="display">Homes worth the trip.</h2>
      </div>
      {collection_grid()}
      <p class="center reveal" style="margin-top:44px"><a class="link" href="/homes">View the Collection</a></p>
    </div>
  </section>

  <section>
    <div class="wrap">
      <div class="center reveal" style="margin-bottom:56px">
        <p class="eyebrow">Before you arrive</p>
        <h2 class="display">Every detail, already done.</h2>
        <hr class="rule">
        <p class="lead">We plan everything. You arrive, and the trip begins.</p>
      </div>
      <div class="details reveal">
        <div><span class="ital">i.</span><h3>Skis and boots, waiting</h3><p>Sized to each guest before you land, in the gear room with your name on them.</p></div>
        <div><span class="ital">ii.</span><h3>Bikes, fitted</h3><p>The right frame for every rider, tuned and ready by the door.</p></div>
        <div><span class="ital">iii.</span><h3>The fridge, stocked</h3><p>Your list, shopped that morning. Coffee the way you take it.</p></div>
        <div><span class="ital">iv.</span><h3>The fire, laid</h3><p>Firewood stacked, blankets out, a bottle chosen for the first night.</p></div>
        <div><span class="ital">v.</span><h3>Every booking, made</h3><p>Lift tickets, guides, tee times and tables, all confirmed in the app.</p></div>
        <div><span class="ital">vi.</span><h3>The plan, flexible</h3><p>Storms after one? Your ride moves to tomorrow, and we tell you first.</p></div>
      </div>
      <p class="center reveal" style="margin-top:52px"><a class="btn" href="/stay">See how a stay works</a></p>
    </div>
  </section>

  <section class="tint" id="experiences">
    <div class="wrap">
      <div class="center reveal" style="margin-bottom:52px">
        <p class="eyebrow">Experiences</p>
        <h2 class="display">Every season, arranged.</h2>
      </div>
      <div class="grid3">{exps}</div>
    </div>
  </section>

  <section>
    <div class="wrap">
      <div class="band reveal">
        <svg role="img" aria-label="Ophir Stays seal"><use href="#seal"/></svg>
        <div>
          <p class="eyebrow">For homeowners</p>
          <h2 class="display">We beat your last year, or we refund the difference.</h2>
          <p>If your home earns less in its first twelve months with Ophir than in the twelve before, we refund our fee on the difference. Twenty-five homes only.</p>
        </div>
        <a class="btn btn-rust" href="/owners">Apply</a>
      </div>
    </div>
  </section>

  <section class="tint">
    <div class="wrap split">
      <div class="reveal">{photo('ophir', 'Ice Lake Basin in the San Juan Mountains near Ophir')}</div>
      <div class="reveal">
        <p class="eyebrow">The name</p>
        <h2 class="display">Why Ophir</h2>
        <p class="lead">Ophir was the legendary land of gold. Miners carried the name into the San Juans and gave it to a town and a high pass between the peaks. They came for riches and found something better: country that stops you in your tracks. We named our homes for that feeling.</p>
        <p style="margin-top:28px"><a class="link" href="/about">Our story</a></p>
      </div>
    </div>
  </section>

  <section>
    <div class="wrap">
      <div class="center reveal" style="margin-bottom:52px">
        <p class="eyebrow">The Journal</p>
        <h2 class="display">Notes from Durango</h2>
      </div>
      <div class="grid3">
        <a class="card reveal" href="/journal/durango-rides">{photo('journal-1', 'Singletrack below Engineer Mountain', 'ph')}<p class="post-meta">Ride</p><h3>Five rides that show you Durango</h3><span class="link">Read</span></a>
        <a class="card reveal" href="/journal/where-to-eat-durango">{photo('coffee', 'A latte at a Durango café table', 'ph')}<p class="post-meta">Eat</p><h3>Where to eat in Durango, from a local</h3><span class="link">Read</span></a>
        <a class="card reveal" href="/journal/durango-home-earnings">{photo('journal-3', 'Gold aspens below Mount Sneffels', 'ph')}<p class="post-meta">Owners</p><h3>What a Durango vacation home earns</h3><span class="link">Read</span></a>
      </div>
    </div>
  </section>
'''

SLIDE_JS = '''
<script>
(function(){
  var root=document.getElementById('show');if(!root)return;
  var s=root.querySelectorAll('.slide'),t=root.querySelectorAll('.thumbs button'),i=0,timer;
  var still=window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  function go(n){s[i].classList.remove('on');t[i]&&t[i].removeAttribute('aria-current');i=(n+s.length)%s.length;s[i].classList.add('on');t[i]&&t[i].setAttribute('aria-current','true')}
  function play(){if(still)return;clearInterval(timer);timer=setInterval(function(){go(i+1)},6000)}
  root.querySelector('.prev').onclick=function(){go(i-1);play()};
  root.querySelector('.next').onclick=function(){go(i+1);play()};
  t.forEach(function(b,k){b.onclick=function(){go(k);play()}});
  root.addEventListener('mouseenter',function(){clearInterval(timer)});root.addEventListener('mouseleave',play);
  root.addEventListener('keydown',function(e){if(e.key==='ArrowLeft'){go(i-1);play()}if(e.key==='ArrowRight'){go(i+1);play()}});
  play();
})();
</script>'''

home = page('Ophir Stays · Durango Vacation Rentals, Every Trip Planned',
            'Twenty-five homes in Durango, Colorado, each kept to one standard, each stay with the whole trip handled: ski, spa, golf and mountain biking. Locally owned.',
            '/', 'home', home_body, SLIDE_JS)

# ---------------- OWNERS ----------------
owners_body = f'''
  <section class="center" style="padding-bottom:56px">
    <div class="wrap narrow reveal">
      <p class="eyebrow">For homeowners</p>
      <h1 class="display">Your home, cared for like ours.</h1>
      <hr class="rule">
      <p class="lead">Owners don't hire Ophir. They apply. Twenty-five homes, one standard, and your first year's income guaranteed.</p>
      <p style="margin-top:32px"><a class="btn btn-rust" href="#estimate">Get your free estimate</a></p>
    </div>
  </section>
  <div class="wrap">{photo('home-1', 'A Collection home in the mountains above Durango')}</div>

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
        <h2 class="display">We beat your last year, or we refund the difference.</h2>
        <p class="lead">If your home earns less in its first twelve months with Ophir than in the twelve months before, we refund the difference, up to the full management fee we earned that year.</p>
      </div>
      <div class="reveal">
        <table class="terms">
          <tr><th scope="row">Who qualifies</th><td>Homes with at least twelve months of rental history we can see: Airbnb, VRBO or prior manager statements.</td></tr>
          <tr><th scope="row">Your baseline</th><td>Gross booking revenue for the twelve months before you sign.</td></tr>
          <tr><th scope="row">Your own stays</th><td>Nights you block for yourself lower the baseline by that year's average nightly rate.</td></tr>
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
        <div><span class="ital">ii.</span><h3>Small fixes, included</h3><p>Bulbs, batteries, filters, a loose handle: fixed and never billed. Bigger repairs are billed at cost plus 10%, with photos, and nothing over $300 happens without your yes.</p></div>
        <div><span class="ital">iii.</span><h3>Fifteen minutes</h3><p>Guests and owners hear back within fifteen minutes, 7am to 10pm. Someone is at your house within thirty minutes, any hour.</p></div>
        <div><span class="ital">iv.</span><h3>Priced every day</h3><p>Nightly rates move daily with the season, events and demand, set by live Durango data and checked by someone who lives here.</p></div>
      </div>
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
        <li>A gear room: bikes, skis, boot dryers</li><li>Fast Wi-Fi and a smart lock</li><li>A kitchen stocked for a real dinner</li>
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
        <div><b>22%</b><span>of booking revenue. Pricing, guests, cleaning, trip planning and your monthly report.</span></div>
        <div><b>$0</b><span>to join. Readiness work is quoted up front and billed at cost.</span></div>
        <div><b>30 days</b><span>notice to leave, either way. No long contracts.</span></div>
      </div>
    </div>
  </section>

  <section class="tint" id="estimate">
    <div class="wrap split top">
      <div class="reveal">
        <p class="eyebrow">Free estimate</p>
        <h2 class="display">What could your home earn?</h2>
        <p class="lead">Tell us about your home. Casey will send you a personal estimate within two business days, with no obligation.</p>
        <p class="fine" style="margin-top:28px">Prefer to talk? <a href="mailto:casey@ophirstays.com">casey@ophirstays.com</a></p>
        <p class="fine" style="margin-top:12px">Before you apply: <a href="/journal/durango-home-earnings">what a Durango vacation home earns</a> and <a href="/journal/durango-short-term-rental-rules">the city and county rental rules</a>.</p>
      </div>
      <div class="reveal" id="estimate-box">
        <form class="form" id="estimate-form" novalidate>
          <div class="field"><label for="f-name">Your name</label><input id="f-name" name="name" autocomplete="name" required></div>
          <div class="field"><label for="f-email">Email</label><input id="f-email" name="email" type="email" autocomplete="email" required></div>
          <div class="field"><label for="f-phone">Phone</label><input id="f-phone" name="phone" type="tel" autocomplete="tel"></div>
          <div class="field"><label for="f-beds">Bedrooms</label><select id="f-beds" name="bedrooms"><option value="">Select</option><option>1–2</option><option>3</option><option>4</option><option>5</option><option>6+</option></select></div>
          <div class="field full"><label for="f-addr">Home address in Durango</label><input id="f-addr" name="address" autocomplete="street-address" required></div>
          <div class="field"><label for="f-renting">Rented now?</label><select id="f-renting" name="renting"><option value="">Select</option><option>Yes, I manage it myself</option><option>Yes, with a manager</option><option>Not yet</option></select></div>
          <div class="field"><label for="f-rev">Last 12 months' income</label><input id="f-rev" name="revenue" inputmode="numeric" placeholder="Optional"><span class="hint">Sets your guarantee baseline.</span></div>
          <div class="field full"><label for="f-notes">Anything we should know?</label><textarea id="f-notes" name="notes"></textarea></div>
          <div class="hp" aria-hidden="true"><label for="f-web">Website</label><input id="f-web" name="website" tabindex="-1" autocomplete="off"></div>
          <button class="btn" type="submit">Send my request</button>
          <p class="form-status" role="status" aria-live="polite"></p>
        </form>
        <div class="thanks" tabindex="-1"><svg aria-hidden="true"><use href="#summit"/></svg><h3>Thank you. We have your request.</h3><p style="color:var(--muted);margin:12px 0 0">Casey will email your estimate within two business days.</p></div>
      </div>
    </div>
  </section>

  <section>
    <div class="wrap narrow">
      <p class="eyebrow">Questions</p>
      <h2 class="display" style="margin-bottom:24px">Before you apply.</h2>
      <div class="faq">
        <details><summary>I already have a manager. Can I switch?</summary><p>Yes. Most agreements need thirty to sixty days' notice. We handle the handover and move your future bookings across.</p></details>
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
  f.addEventListener('submit',async function(e){
    e.preventDefault();st.className='form-status';
    var miss=[].filter.call(f.querySelectorAll('[required]'),function(i){return !i.value.trim()});
    if(miss.length){st.textContent='Please fill in your name, email and the home address.';st.classList.add('err');miss[0].focus();return}
    if(!/^[^@\\s]+@[^@\\s]+\\.[^@\\s]+$/.test(f.email.value)){st.textContent='Please check your email address.';st.classList.add('err');f.email.focus();return}
    var btn=f.querySelector('button');btn.disabled=true;btn.textContent='Sending…';
    try{
      var r=await fetch('/api/estimate',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify(Object.fromEntries(new FormData(f)))});
      if(!r.ok)throw 0;
      box.classList.add('sent');box.querySelector('.thanks').focus();
    }catch(_){
      st.textContent='Something went wrong. Please email casey@ophirstays.com and we\\'ll reply today.';st.classList.add('err');
      btn.disabled=false;btn.textContent='Send my request';
    }
  });
})();
</script>'''

owners = page('Durango Vacation Rental Management · Ophir Stays',
              'Apply to the Ophir Collection: twenty-five Durango homes, one standard, and a first-year income guarantee. Get a free estimate of what your home could earn.',
              '/owners', 'owners', owners_body, FORM_JS)


# ---------------- YOUR STAY (packages) ----------------
TIERS = [
  dict(name='The Stay', price='Included', unit='with every booking', lead='A beautiful home, kept to our standard, with a local on call.',
       items=['Home inspected before every arrival', 'Hotel-grade linens, robes and toiletries', 'Welcome card and Ophir tumblers to keep',
              'Door code and house guide in the app', 'Weather-aware ideas for every day', 'A local host by text, replies within fifteen minutes']),
  dict(name='The Arranged Stay', price='$395', unit='per stay', lead='Tell us what you love. We plan the trip around it.', feature=True,
       items=['Everything in The Stay', 'A planning call before you arrive', 'Skis and boots sized to each guest, waiting in the gear room',
              'Bikes fitted to each rider and delivered', 'Lift tickets, guides, rafting and fly fishing booked',
              'Dinner reservations held, first round on us', 'Your itinerary in the app, moved when the weather moves']),
  dict(name='The Private Stay', price='$1,250', unit='per stay, up to five nights', lead='A dedicated host. Nothing left for you to do.',
       items=['Everything in The Arranged Stay', 'Groceries shopped and the fridge stocked to your list', 'Fire laid, wine chosen, music on when you walk in',
              'Your own host, on call for the whole stay', 'Private chef, in-home massage or a sitter arranged',
              'Airport arrival arranged', 'Mid-stay refresh: linens, towels, restock', 'Longer stays: $150 per additional night']),
]
def tier_html(t):
    items=''.join(f'<li>{i}</li>' for i in t['items'])
    cls=' tier-feature' if t.get('feature') else ''
    return f'''<div class="tier{cls} reveal"><p class="eyebrow" style="margin-bottom:10px">{t['name']}</p>
        <div class="tier-price"><b>{t['price']}</b><span>{t['unit']}</span></div><p class="tier-lead">{t['lead']}</p><ul class="tier-list">{items}</ul></div>'''

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
          <div><b>Arrival setup</b><span>Fire laid, wine chosen, flowers · $75</span></div>
          <div><b>Skis or bikes fitted and delivered</b><span>$45 plus rental</span></div>
        </div>
      </div>
      <p class="fine center" style="margin-top:28px">Gear, guides, lift tickets, groceries and partner services are billed at our partners' rates, with no markup to you.</p>
    </div>
  </section>

  <section>
    <div class="wrap split">
      <div class="reveal">{photo('ski', 'Wooden skis against a cabin wall')}</div>
      <div class="reveal">
        <p class="eyebrow">Attention to detail</p>
        <h2 class="display">The small things are the whole thing.</h2>
        <ul class="standard" style="columns:1;margin-top:24px">
          <li>Boots warmed in the dryer on powder mornings</li>
          <li>Each guest's gear labeled with their name</li>
          <li>Your coffee order, already in the kitchen</li>
          <li>Kids' bikes and helmets in the right sizes</li>
          <li>A trail map marked with the ride we planned for you</li>
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
      <div class="reveal">{photo('casey', 'Casey Roberts, founder of Ophir Stays, holding a brown trout on a drift boat', 'photo tall')}</div>
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
      <a class="card reveal" href="/journal/where-to-eat-durango">{photo('coffee', 'A latte at a Durango café table', 'ph')}<p class="post-meta">Eat</p><h3>Where to eat in Durango, from a local</h3><p>Thirteen places, sorted by the night you're having: a special dinner, a date, friends, kids, or lunch on the run.</p><span class="link">Read</span></a>
      <a class="card reveal" href="/journal/durango-home-earnings">{photo('journal-3', 'Gold aspens below Mount Sneffels', 'ph')}<p class="post-meta">Owners</p><h3>What a Durango vacation home earns, and what decides it</h3><p>Three data firms, three answers. What the numbers say, and the five things that separate the top homes.</p><span class="link">Read</span></a>
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
      <h2>1. Horse Gulch</h2>
      <p>Minutes from Main Avenue, a web of flowing trails through piñon and juniper. The right first ride: short loops, big views back over town, and easy to extend when your legs feel good.</p>
      <h2>2. Animas Mountain</h2>
      <p>A steady climb on the north edge of town to views straight down the Animas Valley. Rocky in places, rewarding all the way. Go early in summer.</p>
      <h2>3. Log Chutes</h2>
      <p>Cool forest riding up Junction Creek Road, with smooth climbs and fun descents. A favorite on hot afternoons when town is baking.</p>
      <h2>4. The Colorado Trail from Junction Creek</h2>
      <p>The start, or the finish, of a 500-mile trail to Denver. Ride out and back as far as you like through some of the prettiest forest near town.</p>
      <h2>5. Hermosa Creek</h2>
      <p>The big one: a long day along a mountain creek, best done as a shuttle. We arrange the drop-off and have lunch packed.</p>
      <p style="margin-top:40px">Staying with Ophir? Bikes are sized to each rider and delivered to the house, and we'll match the ride to the weather and your legs.</p>
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
post3 = page('Where to eat in Durango, from a local · The Journal · Ophir Stays',
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
      <p>Before we sign a home, we check its zoning and HOA documents with the owner. Once it's live, we register for and remit taxes on direct bookings, act as the local contact, and keep occupancy and parking inside the county's guidelines. If you're not sure where your home stands, we'll look it up for you.</p>
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
post4 = page('Can you rent your Durango home short-term? City and county rules · Ophir Stays',
             'Durango short-term rental rules for 2026: city permits are capped and waitlisted; La Plata County has no rental permit but requires lodging and sales tax.',
             '/journal/durango-short-term-rental-rules', 'journal', post4_body)

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
      <p class="post-meta">{h['beds']} bedrooms · {h['baths']} baths · sleeps {h['sleeps']}</p>
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

os.makedirs('journal', exist_ok=True); os.makedirs('homes', exist_ok=True)
for name, html in [('index.html', home), ('owners.html', owners), ('about.html', about), ('journal.html', journal), ('journal/durango-rides.html', post), ('journal/durango-home-earnings.html', post2), ('journal/where-to-eat-durango.html', post3), ('journal/durango-short-term-rental-rules.html', post4), ('homes.html', homes_page), ('stay.html', stay_page)] + [(f"homes/{h['slug']}.html", home_page(h)) for h in LIVE_HOMES]:
    open(name, 'w').write(html)
open('sitemap.xml', 'w').write('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' +
    ''.join(f'<url><loc>https://ophirstays.com{p}</loc><lastmod>2026-10-17</lastmod></url>\n' for p in ['/', '/stay', '/homes', '/owners', '/about', '/journal', '/journal/durango-rides', '/journal/durango-home-earnings', '/journal/where-to-eat-durango', '/journal/durango-short-term-rental-rules'] + [f"/homes/{h['slug']}" for h in HOMES if not h['sample']]) + '</urlset>\n')
print('built')
