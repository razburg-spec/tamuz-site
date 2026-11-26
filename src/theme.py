"""v3 design (Nov 2026, Raz's pick "שחור מוחלט"): pure black, the Tamuz Studios logo, thin Heebo
Hebrew with small Bodoni Latin labels, and one cinematic grade on every photo (files <id>-c.jpg / -cm.jpg).

Imported by prod.py right after `build`; it swaps the page builders and keeps every page text,
URL and SEO field from the v1 generator.
"""
import html
import build
from build import PAGES, PHONE, EMAIL, ADDRESS, MAPS, SOCIAL, SERVICES, PRODUCTION, contact_lines, render_blocks, inline
from content_c import PODCASTS

_wix_media = build.media

def media(fid, w=1600, h=None, q=80):
    """Local photos are 'img:<id>' and always use the graded copies."""
    if fid and fid.startswith("img:"):
        name = fid[4:]
        return f"/img/{name}-cm.jpg" if w <= 900 else f"/img/{name}-c.jpg"
    return _wix_media(fid, w, h, q)

build.media = media
G = lambda i, small=False: f"/img/{i}-{'cm' if small else 'c'}.jpg"

# Hero photo per page. All photos approved by Raz; never use ig-029 / fb-025 (not studio gear) or fb-017.
PHOTO = {
    "": "fb-043e", "recording-studio-tel-aviv": "fb-043e", "songs-recordings": "ig-027", "mixing-audio-edits": "fb-024",
    "post-production-sound-design": "fb-050", "podcast-recording": "fb-045", "livestreaming": "fb-021",
    "live-recording": "ig-026", "mobile-recording-studio": "ig-038", "sound-protools-lessons": "fb-053",
    "original-music-movies-commercials": "fb-046", "playbacks": "ig-030", "music-production": "fb-061",
    "music-production-singer-songwriter": "ig-034", "music-production-bands": "ig-036",
    "music-production-commercials": "fb-013", "recording-studio-equipment": "fb-024", "contact": "fb-078",
    "services": "fb-014", "blog": "fb-008", "privacy": None,
}
for slug, ph in PHOTO.items():
    if slug in PAGES:
        PAGES[slug]["img"] = f"img:{ph}" if ph else None

RECORDING = ["recording-studio-tel-aviv", "songs-recordings", "mixing-audio-edits", "live-recording", "mobile-recording-studio", "playbacks", "sound-protools-lessons"]
MEDIA = ["podcast-recording", "livestreaming", "post-production-sound-design"]
PRODUCE = ["music-production", "music-production-singer-songwriter", "music-production-bands", "music-production-commercials", "original-music-movies-commercials"]
SECTIONS = [("recording-studio-tel-aviv", "הקלטה ומיקס", "Recording & Mixing", RECORDING),
            ("podcast-recording", "פודקאסטים ומדיה", "Podcasts & Media", MEDIA),
            ("music-production", "הפקה מוזיקלית", "Music Production", PRODUCE)]
SECTION_OF = {s: (top, he, en, lst) for top, he, en, lst in SECTIONS for s in lst}
LATIN = {"recording-studio-equipment": "Equipment", "contact": "Contact", "blog": "Journal", "services": "Services", "privacy": "Privacy"}

link = lambda slug: "/" + (slug or "")

def latin_for(slug):
    return SECTION_OF[slug][2] if slug in SECTION_OF else LATIN.get(slug, "Tamuz Studios")

COVERS = [("c51", "יוני רכטר", "Svivenu"), ("c144", "אריאל זילבר", "Hee Hashir"), ("c75", "Voca People", "Voca Dance"),
          ("c33", "קובי אוז", "Chalom Akevotaich"), ("c118", "חנן יובל", "Erev Kaitz Ham"), ("c45", "נועם רותם", "Neshoret"),
          ("c67", "נועם רותם ואיתמר רוטשילד", "Ezra Bad"), ("c84", "חנן יובל, אורי הרפז ודורית ראובני", "Shloshtenu"),
          ("c85", "נתן סלור ואושיק לוי", "Tmuna"), ("c113", "אלאי בוטנר", "Nipagesh Bachalomot"), ("c104", "ג׳ונתן ביטון", "Shoshanat Haamakim"),
          ("c99", "אמיר פרי", "Nofel Lemala"), ("c37", "יגאל טולדנו", "Hageshem Harishon"), ("c124", "רותם לשם", "Yesh Li Bait")]

TOPICS = [("הקלטה ומיקס", "rec"), ("פודקאסט", "pod"), ("הפקה מוזיקלית", "prod"), ("משהו אחר", "")]
TOPIC_OF = {"recording-studio-tel-aviv": "rec", "podcast-recording": "pod", "music-production": "prod"}

def form(fid, path=None):
    opts = "".join(f'<option value="{t}"{" selected" if k and k == path else ""} data-path="{k}">{t}</option>' for t, k in TOPICS)
    base = build.form(fid)
    sel = f'<label for="{fid}-tp">במה מדובר?<select id="{fid}-tp" name="topic" data-topic>{opts}</select></label>\n  '
    return base.replace(f'<label for="{fid}-msg">', sel + f'<label for="{fid}-msg">', 1)

def covers(n=None):
    return "".join(f'<figure class="cv"><img src="/img/{c}.jpg" alt="{html.escape(a)} – {html.escape(t)}" loading="lazy" width="360" height="360"><figcaption>{html.escape(a)}</figcaption></figure>' for c, a, t in (COVERS[:n] if n else COVERS))

def pods(n=None):
    return "".join(build.pod_fig(*p) for p in (PODCASTS[:n] if n else PODCASTS))

def nav():
    items = []
    for i, (top, he, en, sub) in enumerate(SECTIONS):
        subl = "".join(f'<li><a href="{link(s)}">{PAGES[s]["title"]}</a></li>' for s in sub)
        items.append(f'<li class="has-sub"><a href="{link(top)}">{he}</a><button class="sub-toggle" type="button" aria-expanded="false" aria-controls="sub{i}" aria-label="פתיחת תפריט {he}"><span aria-hidden="true">▾</span></button><ul class="sub" id="sub{i}">{subl}</ul></li>')
    for slug, label in [("recording-studio-equipment", "ציוד"), ("blog", "בלוג"), ("contact", "צור קשר")]:
        items.append(f'<li><a href="{link(slug)}">{label}</a></li>')
    return "".join(items)

def crumbs_for(slug):
    if slug in SECTION_OF:
        top, he, _, _ = SECTION_OF[slug]
        return "" if slug == top else f'<span>/</span><a href="{link(top)}">{he}</a>'
    return ""

def page_hero(p, crumbs, slug=None, lead=None):
    img = p.get("img")
    bg = f' style="--img:url(\'{media(img, 1920)}\')"' if img else ""
    lead_html = f'<p class="ph-lead">{lead}</p>' if lead else ""
    return f'''<header class="phero{" has-img" if img else ""}"{bg}>
  <div class="wrap"><nav class="crumbs" aria-label="מיקום באתר"><a href="/">Tamuz Studios</a>{crumbs}</nav>
  <p class="kick" lang="en">{latin_for(slug)}</p><h1>{p["title"]}</h1>{lead_html}</div>
</header>'''

def aside(slug):
    if slug in SECTION_OF:
        top, head, en, lst = SECTION_OF[slug]
    else:
        head, en, lst = "שירותים", "Services", SERVICES
    lis = "".join(f'<li><a href="{link(s)}"{" aria-current=\"page\"" if s == slug else ""}>{PAGES[s]["title"]}</a></li>' for s in lst)
    return f'''<aside class="side">
  <nav class="side-nav" aria-label="{head}"><p class="kick" lang="en">{en}</p><p class="side-h">{head}</p><ul>{lis}</ul></nav>
  <div class="side-card"><p class="kick" lang="en">Book a session</p><a class="big-phone" href="tel:036481791" dir="ltr">{PHONE}</a><a class="btn btn-line" href="#book">שלחו הודעה</a></div>
</aside>'''

def cta_band(slug=None):
    path = TOPIC_OF.get(SECTION_OF[slug][0]) if slug in SECTION_OF else None
    return f'''<section class="book" id="book"><div class="wrap contact-grid">
  <div><p class="kick" lang="en">Book a session</p><h2 class="sec-h">דברו איתנו</h2><p class="muted">ספרו לנו בכמה מילים מה אתם מתכננים, ונחזור אליכם עם הצעה.</p>{contact_lines()}</div>
  {form("b-" + (slug or "x"), path)}
</div></section>'''

INTRO = {
    "recording-studio-tel-aviv": "חדר הקלטה שתוכנן על ידי אקוסטיקאים, חדר בקרה עם ציוד אנלוגי ודיגיטלי, וטכנאי שמכיר כל פינה בחדר.",
    "podcast-recording": "סטים מעוצבים, צילום בשלוש מצלמות, סאונד ברמת אולפן ועריכה. מגיעים ומדברים, ואת כל השאר עושים אנחנו.",
    "music-production": "מרעיון או סקיצה ועד שיר מוכן לרדיו: עיבוד, נגנים, הקלטה, מיקס ומאסטר, באותו חדר ועם אותו מפיק.",
}

def hub_page(slug):
    top, he, en, lst = SECTION_OF[slug]
    p = PAGES[slug]
    tiles = "".join(f'<a class="tile" href="{link(s)}"><span class="tile-im" style="--img:url(\'{G(PHOTO.get(s) or PHOTO[slug], True)}\')"></span><span class="tile-t">{PAGES[s]["title"]}</span><span class="tile-go" aria-hidden="true">←</span></a>' for s in lst if s != slug)
    proof = {
        "recording-studio-tel-aviv": f'<div class="sh"><p class="kick" lang="en">Selected credits</p><h2 class="sec-h">הוקלט ומוקס בתמוז</h2></div><div class="covers">{covers()}</div>',
        "podcast-recording": f'<div class="sh"><p class="kick" lang="en">Recorded here</p><h2 class="sec-h">{len(PODCASTS)} פודקאסטים הוקלטו בתמוז</h2></div><div class="pod-grid">{pods()}</div>',
        "music-production": f'<div class="sh"><p class="kick" lang="en">Producer</p><h2 class="sec-h">רז בורג</h2></div><p class="muted narrowp">מפיק מוזיקלי, נגן ומעצב סאונד, הבעלים של Tamuz Studios. עבודות הפקה נבחרות באתר האישי: <a href="https://www.razburg.com">razburg.com</a></p><div class="covers">{covers(7)}</div>',
    }[slug]
    blocks = [b for b in p["blocks"] if b[0] != "podcasts"]
    return page_hero(p, "", slug, INTRO.get(slug)) + f'''
<section class="block"><div class="wrap"><div class="sh"><p class="kick" lang="en">Services</p><h2 class="sec-h">מה עושים כאן</h2></div><div class="tiles">{tiles}</div></div></section>
<section class="block alt"><div class="wrap">{proof}</div></section>
<div class="wrap split"><article class="prose">{render_blocks(slug, blocks)}</article>{aside(slug)}</div>''' + cta_band(slug)

def inner_page(slug):
    p = PAGES[slug]
    if slug in TOPIC_OF:
        return hub_page(slug)
    crumbs = crumbs_for(slug)
    body = render_blocks(slug, p["blocks"])
    if slug == "recording-studio-equipment":
        intro, racks = body.split('<div class="racks"', 1)
        return page_hero(p, crumbs, slug) + f'<div class="wrap gear-intro prose">{intro}</div><div class="wrap"><div class="racks"{racks}</div>' + cta_band(slug)
    if slug in ("privacy", "blog"):
        return page_hero(p, "", slug) + f'<div class="wrap narrow prose">{body}</div>'
    return page_hero(p, crumbs, slug) + f'<div class="wrap split"><article class="prose">{body}</article>{aside(slug)}</div>' + cta_band(slug)

COLLAGE = ["dbx-013", "fb-024", "fb-045", "ig-018", "ig-030", "fb-051"]
WORLDS = [
    ("recording-studio-tel-aviv", "fb-043e", ["הקלטת שירים", "מיקס ועריכות", "הקלטת הופעות", "אולפן נייד", "פלייבקים"], "covers"),
    ("podcast-recording", "fb-045", ["הקלטת פודקאסט", "צילום וידאו בשלוש מצלמות", "שידור חי", "פוסט פרודקשן"], "pods"),
    ("music-production", "fb-061", ["זמרים ויוצרים", "להקות", "פרסומות", "מוזיקה לסרטים"], "lead"),
]

def home():
    col = "".join(f'<div style="background-image:url(\'{G(i)}\')"></div>' for i in COLLAGE)
    idx = "".join(f'<a href="{link(top)}"><em class="kick" lang="en">{en}</em><span>{he}</span></a>' for top, he, en, _ in SECTIONS)
    worlds = ""
    for n, (top, ph, items, kind) in enumerate(WORLDS):
        _, he, en, _ = SECTION_OF[top]
        extra = {"covers": f'<div class="mini-grid">{covers(6)}</div>', "pods": f'<div class="mini-grid pods-mini">{pods(12)}</div>', "lead": f'<p class="lead">{INTRO[top]}</p>'}[kind]
        worlds += f'''<section class="world{" flip" if n % 2 else ""}"><a class="w-ph" href="{link(top)}" style="--img:url('{G(ph)}')" aria-label="{he}"></a>
  <div class="w-tx"><p class="kick" lang="en">{en}</p><h2>{he}</h2><ul>{"".join(f"<li>{x}</li>" for x in items)}</ul>{extra}<a class="more" href="{link(top)}">{he} בתמוז <span aria-hidden="true">←</span></a></div></section>'''
    return f'''<header class="hero"><div class="h-collage" aria-hidden="true">{col}</div>
  <div class="h-text"><h1 class="h-logo"><img src="/img/logo-white.png" alt="Tamuz Studios" width="900" height="220"></h1>
  <p class="h-claim">סאונד בלי פשרות. בכל תחום.</p><p class="h-sub">הקלטה ומיקס · פודקאסטים ומדיה · הפקה מוזיקלית</p></div>
</header>
<nav class="index" aria-label="התחומים שלנו">{idx}</nav>
{worlds}
<section class="block about-b"><div class="wrap about">
  <div class="about-im" style="--img:url('{G("fb-062", True)}')" role="img" aria-label="רז בורג באולפן"></div>
  <div class="prose"><p class="kick" lang="en">About</p><h2 class="sec-h">Tamuz Studios</h2>
  <p>האולפן הוקם בשנת 2004, ומאז 2006 הוא בבעלות רז בורג, מפיק מוזיקלי, טכנאי ומעצב סאונד, שמנהל בעצמו כל סשן.</p>
  <p>האולפן תוכנן על ידי אקוסטיקאים ומאפשר הקלטות מכל הסוגים: תופים, רביעיית כלי קשת, כלי הקשה, שירה ואקפלה, לצד סטים מעוצבים לפודקאסטים וצילום וידאו.</p>
  <p>להכיר את רז ואת העבודות שלו: <a href="https://www.razburg.com">razburg.com</a></p></div>
</div></section>
<section class="book" id="contact"><div class="wrap contact-grid">
  <div><p class="kick" lang="en">Contact</p><h2 class="sec-h">בואו לבקר באולפן</h2><p class="muted">ספרו לנו מה אתם רוצים להקליט, ונחזור אליכם עם הצעה.</p>{contact_lines()}</div>
  {form("home")}
</div></section>'''

def contact():
    p = PAGES["contact"]
    soc = "".join(f'<li><a href="{u}" target="_blank" rel="noopener">{n}</a></li>' for n, u in SOCIAL)
    return page_hero(p, "", "contact") + f'''<div class="wrap contact-grid block">
  <div><h2 class="sec-h">דברו איתנו</h2><a class="big-phone" href="tel:036481791" dir="ltr">{PHONE}</a>{contact_lines()}<p class="kick" lang="en" style="margin-top:2rem">Follow</p><ul class="social">{soc}</ul></div>
  <div><h2 class="sec-h">שלחו הודעה</h2>{form("contact")}</div>
</div>'''

def services():
    p = PAGES["services"]
    return page_hero(p, "", "services") + f'''<div class="wrap contact-grid block">
  <div><h2 class="sec-h">צרו קשר</h2>{contact_lines()}</div>
  <div>{form("services")}</div>
</div>'''

def footer():
    col = lambda lst: "".join(f'<li><a href="{link(s)}">{PAGES[s]["title"]}</a></li>' for s in lst)
    soc = "".join(f'<li><a href="{u}" target="_blank" rel="noopener">{n}</a></li>' for n, u in SOCIAL)
    return f'''<footer class="foot"><div class="wrap foot-grid">
  <div><img class="foot-logo" src="/img/logo-white.png" alt="Tamuz Studios" width="900" height="220" loading="lazy"><p class="foot-tag">סאונד בלי פשרות. בכל תחום.</p>{contact_lines("contact-lines")}</div>
  <div><p class="kick" lang="en">Recording &amp; Mixing</p><ul class="foot-list">{col(RECORDING[:5])}</ul></div>
  <div><p class="kick" lang="en">Podcasts &amp; Media</p><ul class="foot-list">{col(MEDIA)}</ul><p class="kick" lang="en" style="margin-top:1.4rem">Music Production</p><ul class="foot-list">{col(PRODUCE[:1] + PRODUCE[4:])}</ul></div>
  <div><p class="kick" lang="en">Follow</p><ul class="foot-list">{soc}<li><a href="https://www.razburg.com">רז בורג · razburg.com</a></li></ul></div>
</div><div class="wrap foot-base"><span>© Raz Burg \\ Tamuz Studios 2026</span><a href="/privacy">מדיניות פרטיות</a></div></footer>'''

build.nav, build.page_hero, build.aside, build.cta_band, build.inner_page = nav, page_hero, aside, cta_band, inner_page
build.home, build.contact, build.services, build.footer = home, contact, services, footer
