#!/usr/bin/env python3
"""Static site generator for razburg.com.

Usage: RB_EMAIL=<public email> python3 build.py <out_dir> [--base /prefix]
Keeps the four Wix URLs: /, /studio, /about, /contact.
Data: discography.json (gallery), gear.json, studio_photos.txt.
The public contact email is read from the RB_EMAIL environment variable;
without it the email line is left out.
"""
import json, html, sys, os, shutil, datetime
from pathlib import Path

SRC = Path(__file__).parent
OUT = Path(sys.argv[1] if len(sys.argv) > 1 else "dist")
BASE = ""
if "--base" in sys.argv:
    BASE = sys.argv[sys.argv.index("--base") + 1].rstrip("/")

SITE = "https://www.razburg.com"
EMAIL = os.environ.get("RB_EMAIL", "")
PHONE_DISPLAY = "+972-3-648-1791"
PHONE_TEL = "+97236481791"
YEAR = datetime.date.today().year
WEB3FORMS_KEY = os.environ.get("WEB3FORMS_KEY", "")

SOCIAL = [
    ("Spotify", "https://open.spotify.com/search/Raz%20Burg/artists"),
    ("Apple Music", "https://music.apple.com/us/artist/raz-burg/305453239"),
    ("Instagram", "https://www.instagram.com/razburg.music"),
    ("Facebook", "https://www.facebook.com/razburgmusic"),
    ("SoundBetter", "https://soundbetter.com/profiles/76317-raz-burg"),
    ("Artlist", "https://artlist.io/royalty-free-music/artist/raz-burg/1002"),
    ("Vimeo", "https://vimeo.com/razburg"),
    ("LinkedIn", "https://www.linkedin.com/in/razburg/"),
]
SAME_AS = [u for n, u in SOCIAL if "search" not in u] + [
    "https://www.discogs.com/artist/1504636-Raz-Burg",
    "https://soundcloud.com/razburg",
]

def esc(s):
    return html.escape(s, quote=True)

IMAGES = {}  # local file name -> Wix CDN URL, written to images.json for tools/fetch_images.py
LOCAL_IMAGES = (SRC / "img").is_dir() and any((SRC / "img").iterdir())

def wix(media_id, w, h=None, mode="fill"):
    """Image URL. Uses self-hosted copies in src/img/ when present, else the Wix CDN."""
    h = h or w
    ext = media_id.rsplit(".", 1)[-1].lower()
    ext = "jpg" if ext == "jpeg" else ext
    stem = media_id.split("~")[0]
    name = stem + "." + media_id.rsplit(".", 1)[-1]
    remote = f"https://static.wixstatic.com/media/{media_id}/v1/{mode}/w_{w},h_{h},al_c,q_82/{name}"
    local = f"{stem}-{w}x{h}{'' if mode == 'fill' else '-' + mode}.{ext}"
    IMAGES[local] = remote
    if LOCAL_IMAGES and (SRC / "img" / local).exists():
        return (SITE if ABS_IMG else BASE) + "/img/" + local
    return remote

ABS_IMG = False

def url(path):
    if path == "/":
        return BASE + "/"
    return BASE + path

HERO_IMG = "3fb1a9_3055ee8fa2234886902f9bd698232aa1~mv2.jpg"
PORTRAIT_IMG = "3fb1a9_b5493d42f62f4f3b9730e77de72b9586~mv2.jpg"

PERSON = {
    "@type": "Person",
    "@id": SITE + "/#raz",
    "name": "Raz Burg",
    "url": SITE + "/",
    "image": None,
    "jobTitle": ["Sound Designer", "Composer", "Music Producer", "Mixing & Mastering Engineer"],
    "knowsAbout": ["Mixing", "Mastering", "Music production", "Sound design", "Recording", "Film and commercial music"],
    "worksFor": {"@type": "RecordingStudio", "name": "Tamuz Studios", "url": "https://www.tamuzstudios.co.il/",
                 "address": {"@type": "PostalAddress", "streetAddress": "Arie Disenchik 9", "addressLocality": "Tel Aviv", "addressCountry": "IL"},
                 "telephone": PHONE_TEL},
    "address": {"@type": "PostalAddress", "addressLocality": "Tel Aviv", "addressCountry": "IL"},
    "sameAs": SAME_AS,
}
def abs_img(*a, **k):
    global ABS_IMG
    ABS_IMG = True
    try:
        return wix(*a, **k)
    finally:
        ABS_IMG = False

PERSON["image"] = abs_img(PORTRAIT_IMG, 1200, 1200)
if EMAIL:
    PERSON["email"] = "mailto:" + EMAIL

NAV = [("/", "Work"), ("/studio", "Studio"), ("/about", "About"), ("https://audiocrafts.razburg.com", "Plugins"), ("/contact", "Contact")]

def links_list():
    return "".join(f'<li><a href="{esc(u)}" target="_blank" rel="me noopener">{esc(n)}</a></li>' for n, u in SOCIAL)

def page(path, title, desc, body, active, og_img=HERO_IMG, extra_ld=None):
    canonical = SITE + ("/" if path == "/" else path)
    ld = [dict(PERSON, **{"@context": "https://schema.org"})]
    ld += extra_ld or []
    if path != "/":
        ld.append({"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Raz Burg", "item": SITE + "/"},
            {"@type": "ListItem", "position": 2, "name": active, "item": canonical}]})
    nav = "".join(
        (f'<a href="{p}" target="_blank" rel="noopener">{esc(n)}</a>' if p.startswith("http") else
         f'<a href="{url(p)}"{" aria-current=page" if p == path else ""}>{esc(n)}</a>') for p, n in NAV)
    tpl = (SRC / "template.html").read_text()
    return (tpl.replace("{{TITLE}}", esc(title))
               .replace("{{DESC}}", esc(desc))
               .replace("{{CANONICAL}}", canonical)
               .replace("{{OG_IMG}}", abs_img(og_img, 1200, 630))
               .replace("{{LD}}", "\n".join(f'<script type="application/ld+json">{json.dumps(x, ensure_ascii=False)}</script>' for x in ld))
               .replace("{{NAV}}", nav)
               .replace("{{SOCIAL}}", links_list())
               .replace("{{BODY}}", body)
               .replace("{{YEAR}}", str(YEAR))
               .replace("{{BASE}}", BASE)
               .replace("{{HOME}}", url("/"))
               .replace("{{CONTACT}}", url("/contact")))

# ---------------------------------------------------------------- data
disc = [d for d in json.loads((SRC / "discography.json").read_text()) if not d.get("hidden")]
gear = json.loads((SRC / "gear.json").read_text())
studio_photos = [l.strip() for l in (SRC / "studio_photos.txt").read_text().splitlines() if l.strip()]
artists = sorted({d["artist"] for d in disc if not d["own"]})

def platform(link):
    for k, n in (("spotify", "Spotify"), ("apple.com", "Apple Music"), ("bandcamp", "Bandcamp"), ("youtube", "YouTube")):
        if k in link:
            return n
    return "Listen"

def cover(d, i):
    label = f'{d["artist"]}{" – " + d["title"] if d["title"] else ""}'
    img = (f'<img src="{wix(d["img"], 360)}" srcset="{wix(d["img"], 240)} 240w, {wix(d["img"], 360)} 360w, {wix(d["img"], 560)} 560w" '
           f'sizes="(min-width: 1200px) 200px, (min-width: 700px) 22vw, 45vw" width="360" height="360" '
           f'alt="{esc(label)} album cover" loading="{"eager" if i < 6 else "lazy"}" decoding="async">')
    cap = f'<span class="cap"><b>{esc(d["artist"])}</b>{"<span>" + esc(d["title"]) + "</span>" if d["title"] else ""}</span>'
    kind = "own" if d["own"] else "artist"
    search = esc(label.lower())
    if d["link"]:
        return (f'<li class="cover" data-kind="{kind}" data-s="{search}"><a href="{esc(d["link"])}" target="_blank" rel="noopener" '
                f'aria-label="{esc(label)}, listen on {platform(d["link"])}">{img}{cap}<span class="plat">{platform(d["link"])}</span></a></li>')
    return f'<li class="cover" data-kind="{kind}" data-s="{search}"><div>{img}{cap}</div></li>'

# ---------------------------------------------------------------- pages
def home():
    n_releases = len(disc)
    covers = "".join(cover(d, i) for i, d in enumerate(disc))
    services = [
        ("Mixing & Mastering", "Mixes that translate on every system, and masters ready for streaming, vinyl and broadcast. Attended or remote sessions."),
        ("Music Production", "From demo to finished record: arrangement, recording, editing and production for artists and bands, in any genre."),
        ("Sound Design & Post", "Sound design, editing and post-production for film, TV, games, commercials and podcasts."),
        ("Original Music", "Scores and library music for film, media and brands. Twenty albums of my music are licensed worldwide through Artlist."),
    ]
    svc = "".join(f'<li><h3>{esc(t)}</h3><p>{esc(p)}</p></li>' for t, p in services)
    body = f'''
<section class="hero">
  <img class="hero-bg" src="{wix(HERO_IMG, 1600, 900)}" srcset="{wix(HERO_IMG, 800, 700)} 800w, {wix(HERO_IMG, 1600, 900)} 1600w, {wix(HERO_IMG, 2400, 1300)} 2400w" sizes="100vw" alt="" fetchpriority="high">
  <div class="wrap hero-in">
    <h1>Raz Burg<span>Sound designer, composer, mixing &amp; mastering engineer</span></h1>
    <p class="lede">I produce, mix and master records for artists and bands, and design sound and music for film and media. My home base is Tamuz Studios in Tel Aviv.</p>
    <div class="btns"><a class="btn" href="#work">Listen to the work</a><a class="tlink" href="{url('/contact')}">Start a project →</a></div>
  </div>
</section>
<section class="wrap services" aria-labelledby="svc-h">
  <h2 id="svc-h">What I do</h2>
  <ul class="svc">{svc}</ul>
</section>
<section class="wrap work" id="work" aria-labelledby="work-h">
  <div class="work-head">
    <h2 id="work-h">Discography</h2>
    <p>Records I produced, recorded, mixed or mastered, and my own albums. Tap a cover to listen.</p>
  </div>
  <div class="filters" role="group" aria-label="Filter discography">
    <button type="button" class="chip" aria-pressed="true" data-f="all">All</button>
    <button type="button" class="chip" aria-pressed="false" data-f="artist">Artists</button>
    <button type="button" class="chip" aria-pressed="false" data-f="own">My albums</button>
    <label class="search"><span class="sr">Search artist or title</span><input type="search" placeholder="Search artist or title" id="q" autocomplete="off"></label>
  </div>
  <p class="count" id="count" aria-live="polite"></p>
  <ul class="grid" id="grid">{covers}</ul>
</section>
<section class="cta"><div class="wrap">
  <h2>Have a record that needs finishing?</h2>
  <p>Send me a rough mix or a reference, and I'll get back to you within a day or two.</p>
  <a class="btn" href="{url('/contact')}">Get in touch</a>
</div></section>'''
    item_list = {"@context": "https://schema.org", "@type": "ItemList", "name": "Raz Burg discography",
                 "numberOfItems": len(disc),
                 "itemListElement": [{"@type": "ListItem", "position": i + 1,
                                      "item": {"@type": "MusicRecording" if "/track/" in d["link"] else "MusicAlbum",
                                               "name": d["title"] or d["artist"],
                                               "byArtist": {"@type": "MusicGroup", "name": d["artist"]},
                                               **({"url": d["link"]} if d["link"] else {})}}
                                     for i, d in enumerate(disc)]}
    website = {"@context": "https://schema.org", "@type": "WebSite", "name": "Raz Burg", "url": SITE + "/"}
    return page("/", "Raz Burg | Sound Designer, Mixing & Mastering Engineer, Music Producer",
                "Raz Burg is a Tel Aviv sound designer, composer and mixing & mastering engineer. Discography of 120+ releases, music production and sound for film and media.",
                body, "Work", extra_ld=[website, item_list])

def studio():
    racks = "".join(
        f'<section class="rack"><h3>{esc(t)}</h3><ul>{"".join("<li>" + esc(x) + "</li>" for x in items)}</ul></section>'
        for t, items in gear)
    photos = "".join(
        f'<li><a href="{wix(p, 960, 960, "fit")}" target="_blank" rel="noopener"><img src="{wix(p, 960, 640)}" width="960" height="640" '
        f'alt="Tamuz Studios Tel Aviv, studio photo {i + 1}" loading="lazy" decoding="async"></a></li>'
        for i, p in enumerate(studio_photos))
    body = f'''
<header class="page-head wrap">
  <p class="eyebrow">Tamuz Studios · Tel Aviv</p>
  <h1>The Studio</h1>
  <p class="lede">I work out of Tamuz Studios, the recording and mixing studio I founded in Tel Aviv in 2006. It is acoustically treated throughout and built for tracking bands, vocals, voice-over and podcasts, and for mixing and mastering.</p>
</header>
<section class="wrap rooms">
  <div><h2>Studio A</h2><p>A control room and a live recording room, for full band tracking, vocals and acoustic instruments.</p></div>
  <div><h2>Studio B</h2><p>A second control room linked to Studio A, so we can record live across all spaces at once.</p></div>
  <div><h2>Remote work</h2><p>Mixing and mastering are also done remotely: send stems, get mixes back with notes and revisions online.</p></div>
</section>
<section class="wrap" aria-labelledby="ph-h">
  <h2 id="ph-h">Inside the studio</h2>
  <ul class="photos">{photos}</ul>
</section>
<section class="wrap gear" aria-labelledby="gear-h">
  <h2 id="gear-h">Equipment</h2>
  <p class="note">The list changes from time to time as gear is added or serviced. Ask me if you need something specific.</p>
  <div class="racks">{racks}</div>
</section>
<section class="cta"><div class="wrap">
  <h2>Book studio time</h2>
  <p>Recording, podcast and studio bookings are handled through Tamuz Studios.</p>
  <div class="btns center"><a class="btn" href="{url('/contact')}">Contact me</a><a class="btn ghost" href="https://www.tamuzstudios.co.il/" target="_blank" rel="noopener">Tamuz Studios website</a></div>
</div></section>'''
    return page("/studio", "Studio | Raz Burg, Tamuz Studios Tel Aviv",
                "Tamuz Studios in Tel Aviv: two linked control rooms, a live room, Neve, RCA and Crane Song outboard, Pro Tools and ATC monitoring. Full equipment list.",
                body, "Studio")

def about():
    body = f'''
<header class="page-head wrap">
  <p class="eyebrow">About</p>
  <h1>Raz Burg</h1>
</header>
<section class="wrap about">
  <figure class="portrait"><img src="{wix(PORTRAIT_IMG, 960, 717, "fit")}" width="960" height="717" alt="Raz Burg in the studio" loading="eager"></figure>
  <div class="bio">
    <p class="lede">I'm a sound designer, composer, music producer and mixing &amp; mastering engineer based in Tel Aviv.</p>
    <p>I started out as a kid on piano and synthesizers. In 1998 I built my first home studio to record my own music and the musicians around me, and spent the following years recording in studios and on stage.</p>
    <p>In 2006 I founded Tamuz Studios in Tel Aviv. It has since become a home for many artists, bands and producers, and today it also hosts podcasts, voice-over and audiobook work. Over the years I have recorded, produced, mixed and mastered more than a hundred releases across many genres.</p>
    <p>Alongside records, I write and design sound for film, commercials and media, and my own instrumental albums are licensed worldwide through Artlist. I also develop audio plugins under the name Raz Burg AudioCrafts.</p>
    <p>My aim is simple: give every artist everything their music needs to sound its best, from the first take to the final master.</p>
    <h2>Services</h2>
    <ul class="ticks">
      <li>Mixing and mastering, attended or remote</li>
      <li>Music production and arrangement</li>
      <li>Studio and live recording</li>
      <li>Sound design, editing and post-production</li>
      <li>Original music for film, TV, commercials and games</li>
    </ul>
    <h2>Elsewhere</h2>
    <ul class="links">{links_list()}<li><a href="https://audiocrafts.razburg.com" target="_blank" rel="noopener">AudioCrafts plugins</a></li></ul>
    <div class="btns"><a class="btn" href="{url('/contact')}">Work with me</a></div>
  </div>
</section>'''
    return page("/about", "About | Raz Burg, Sound Designer & Music Producer",
                "Raz Burg: sound designer, composer and mixing & mastering engineer since 1998, founder of Tamuz Studios Tel Aviv (2006), Artlist composer and AudioCrafts plugin developer.",
                body, "About", og_img=PORTRAIT_IMG,
                extra_ld=[{"@context": "https://schema.org", "@type": "ProfilePage", "mainEntity": {"@id": SITE + "/#raz"}}])

def contact():
    key_field = f'<input type="hidden" name="access_key" value="{esc(WEB3FORMS_KEY)}">' if WEB3FORMS_KEY else ""
    email_row = f'<li><span>Email</span><a href="mailto:{esc(EMAIL)}">{esc(EMAIL)}</a></li>' if EMAIL else ""
    body = f'''
<header class="page-head wrap">
  <p class="eyebrow">Contact</p>
  <h1>Let's talk about your project</h1>
  <p class="lede">Tell me what you're working on: a mix, a master, a production or sound for picture. I usually reply within one business day.</p>
</header>
<section class="wrap contact">
  <div class="direct">
    <h2>Direct</h2>
    <ul class="clist">
      {email_row}
      <li><span>Phone</span><a href="tel:{PHONE_TEL}">{PHONE_DISPLAY}</a></li>
      <li><span>Studio</span><a href="https://www.tamuzstudios.co.il/" target="_blank" rel="noopener">Tamuz Studios, Arie Disenchik 9, Tel Aviv</a></li>
    </ul>
    <h2>Follow</h2>
    <ul class="links">{links_list()}</ul>
  </div>
  <form class="form" id="contact-form" action="https://api.web3forms.com/submit" method="POST" data-email="{esc(EMAIL)}">
    {key_field}
    <input type="hidden" name="subject" value="New message from razburg.com">
    <input type="checkbox" name="botcheck" class="sr" tabindex="-1" autocomplete="off" aria-hidden="true">
    <label>Name<input name="name" required autocomplete="name"></label>
    <label>Email<input name="email" type="email" required autocomplete="email"></label>
    <label>Phone <small>(optional)</small><input name="phone" type="tel" autocomplete="tel"></label>
    <label>What do you need?
      <select name="service">
        <option>Mixing</option><option>Mastering</option><option>Music production</option>
        <option>Sound design / post</option><option>Original music</option><option>Studio recording</option><option>Something else</option>
      </select></label>
    <label>Message<textarea name="message" rows="6" required placeholder="A few words about the project, links to demos or references"></textarea></label>
    <button class="btn" type="submit">Send message</button>
    <p class="form-status" role="status"></p>
  </form>
</section>'''
    return page("/contact", "Contact | Raz Burg, Mixing, Mastering & Sound Design",
                "Contact Raz Burg for mixing, mastering, music production, sound design and original music. Tamuz Studios, Tel Aviv. Phone or the contact form.",
                body, "Contact",
                extra_ld=[{"@context": "https://schema.org", "@type": "ContactPage", "mainEntity": {"@id": SITE + "/#raz"}}])

def notfound():
    body = f'''<header class="page-head wrap"><p class="eyebrow">404</p><h1>Page not found</h1>
<p class="lede">The page you were looking for isn't here. Try the <a href="{url('/')}">discography</a> or <a href="{url('/contact')}">get in touch</a>.</p></header>'''
    return page("/404", "Page not found | Raz Burg", "Page not found.", body, "404")

# ---------------------------------------------------------------- write
if OUT.exists():
    shutil.rmtree(OUT)
OUT.mkdir(parents=True)
(OUT / "index.html").write_text(home())
(OUT / "studio.html").write_text(studio())
(OUT / "about.html").write_text(about())
(OUT / "contact.html").write_text(contact())
nf = notfound().replace('<link rel="canonical" href="https://www.razburg.com/404">', '<meta name="robots" content="noindex">')
(OUT / "404.html").write_text(nf)
for f in ("site.css", "site.js", "favicon.svg"):
    shutil.copy(SRC / f, OUT / f)
if LOCAL_IMAGES:
    (OUT / "img").mkdir()
    for local in IMAGES:
        if (SRC / "img" / local).exists():
            shutil.copy(SRC / "img" / local, OUT / "img" / local)
(SRC / "images.json").write_text(json.dumps(IMAGES, indent=1, sort_keys=True))
today = datetime.date.today().isoformat()
(OUT / "sitemap.xml").write_text(
    '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' +
    "".join(f"  <url><loc>{SITE}{p}</loc><lastmod>{today}</lastmod></url>\n" for p in ("/", "/studio", "/about", "/contact")) +
    "</urlset>\n")
(OUT / "robots.txt").write_text(f"User-agent: *\nAllow: /\n\nSitemap: {SITE}/sitemap.xml\n")
# Old Wix sitemap URL -> new sitemap; preview hosts stay out of the index.
(OUT / "_redirects").write_text("/pages-sitemap.xml /sitemap.xml 301\n")
(OUT / "_headers").write_text("https://:project.pages.dev/*\n  X-Robots-Tag: noindex\nhttps://:worker.:account.workers.dev/*\n  X-Robots-Tag: noindex\n/*\n  X-Content-Type-Options: nosniff\n  Referrer-Policy: strict-origin-when-cross-origin\n")
print("built", OUT, len(disc), "releases")
