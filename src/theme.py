"""v3 design (Nov 2026, Raz's pick "שחור מוחלט"): pure black, the Tamuz Studios logo, thin Heebo
Hebrew with small Bodoni Latin labels, and one cinematic grade on every photo (files <id>-c.jpg / -cm.jpg).

Imported by prod.py right after `build`; it swaps the page builders and keeps every page text,
URL and SEO field from the v1 generator.
"""
import html
import build
from build import PAGES, PHONE, EMAIL, ADDRESS, MAPS, SOCIAL, SERVICES, PRODUCTION, contact_lines, render_blocks, inline
from content_c import PODCASTS
from credits_tamuz import CREDITS
from credits_prod import PRODUCED
import legal  # terms + accessibility pages

# Raz 2026-11-26: no live recording, no Pro Tools lessons, no YouTube/Vimeo links on the site.
REMOVED = {"live-recording": "recording-studio-tel-aviv", "sound-protools-lessons": "recording-studio-tel-aviv", "blog": ""}  # blog dropped by Raz 2026-11-26
for _s in REMOVED:
    PAGES.pop(_s, None)
    if _s in SERVICES: SERVICES.remove(_s)
SOCIAL[:] = [("פייסבוק", u) for n, u in SOCIAL if n == "Facebook"] + [("אינסטגרם", u) for n, u in SOCIAL if n == "Instagram"]

# Live streaming: Zoom only (Raz 2026-11-26)
PAGES["livestreaming"]["blocks"] = [
    ("p", "אנו מספקים שירותי שידור חי בזום מתוך האולפן, לכל צורך: הרצאה, פאנל, וובינר, פודקאסט, השקה או מופע מוזיקלי קטן."),
    ("p", "השידור מתקיים מתוך חדר ההקלטה של האולפן, חדר אקוסטי מקצועי שיכול לארח 3–4 משתתפים בו זמנית לפאנלים, הרצאות ופודקאסטים, או עד שלושה זמרים ונגנים במופע מוזיקלי."),
    ("p", "השידור באולפני תמוז מתבצע עם 3 מצלמות איכותיות המחוברות לנתב וידאו, כך שאפשר לעבור בין זוויות צילום בזמן אמת. באולפן תאורת LED המתאימה לשידור וקו אינטרנט קווי מהיר ויעודי לשידור בלבד."),
    ("p", "השידור עובר ישירות אל משתמש הזום שלכם, לפגישה או לוובינר, ואתם מנהלים את המשתתפים כרגיל."),
    ("p", "הסאונד שעובר לשידור הוא באיכות אולפנית. בנוסף אנו מקליטים את ערוצי הסאונד בנפרד, כך שההקלטה נשמרת לכם ותוכל לשמש אתכם בהמשך ליצירת תוכן אודיו ווידאו."),
    ("q", "שדרו בזום כמו מקצוענים, מתוך אולפן אמיתי."),
    ("p", "לפרטים נוספים והזמנות [[צרו קשר כאן|contact]] ונשמח לעזור"),
]

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
    "mobile-recording-studio": "ig-038",
    "original-music-movies-commercials": "fb-066", "playbacks": "ig-030", "music-production": "fb-061",
    "music-production-singer-songwriter": "ig-030", "music-production-bands": "ig-036",
    "music-production-commercials": "ig-031", "recording-studio-equipment": "fb-024", "contact": "fb-078",
    "services": "fb-014", "blog": "fb-008", "privacy": None,
}
for slug, ph in PHOTO.items():
    if slug in PAGES:
        PAGES[slug]["img"] = f"img:{ph}" if ph else None

RECORDING = ["recording-studio-tel-aviv", "songs-recordings", "mixing-audio-edits", "mobile-recording-studio", "playbacks"]
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

COVERS = CREDITS  # (path, artist, title), approved by Raz

TOPICS = [("הקלטה ומיקס", "rec"), ("פודקאסט", "pod"), ("הפקה מוזיקלית", "prod"), ("משהו אחר", "")]
TOPIC_OF = {"recording-studio-tel-aviv": "rec", "podcast-recording": "pod", "music-production": "prod"}

def form(fid, path=None):
    opts = "".join(f'<option value="{t}"{" selected" if k and k == path else ""} data-path="{k}">{t}</option>' for t, k in TOPICS)
    base = build.form(fid)
    sel = f'<label for="{fid}-tp">במה מדובר?<select id="{fid}-tp" name="topic" data-topic>{opts}</select></label>\n  '
    return base.replace(f'<label for="{fid}-msg">', sel + f'<label for="{fid}-msg">', 1)

def covers(n=None):
    return "".join(f'<figure class="cv"><img src="/img/{c}.jpg" alt="{html.escape(a)} – {html.escape(t)}" loading="lazy" width="360" height="360"><figcaption>{html.escape(a)}</figcaption></figure>' for c, a, t in (COVERS[:n] if n else COVERS))

def prod_covers():
    return "".join(f'<figure class="cv"><img src="/img/{c}.jpg" alt="{html.escape(a)} – {html.escape(t)}" loading="lazy" width="360" height="360"><figcaption>{html.escape(a)}</figcaption></figure>' for c, a, t in PRODUCED)

def pods(n=None):
    return "".join(build.pod_fig(*p) for p in (PODCASTS[:n] if n else PODCASTS))

def nav():
    items = []
    for i, (top, he, en, sub) in enumerate(SECTIONS):
        subl = "".join(f'<li><a href="{link(s)}">{PAGES[s]["title"]}</a></li>' for s in sub)
        items.append(f'<li class="has-sub"><a href="{link(top)}">{he}</a><button class="sub-toggle" type="button" aria-expanded="false" aria-controls="sub{i}" aria-label="פתיחת תפריט {he}"><span aria-hidden="true">▾</span></button><ul class="sub" id="sub{i}">{subl}</ul></li>')
    for slug, label in [("recording-studio-equipment", "ציוד"), ("contact", "צור קשר")]:
        items.append(f'<li><a href="{link(slug)}">{label}</a></li>')
    return "".join(items)

def crumbs_for(slug):
    if slug in SECTION_OF:
        top, he, _, _ = SECTION_OF[slug]
        return "" if slug == top else f'<span>/</span><a href="{link(top)}">{he}</a>'
    return ""

POS = {"playbacks": "center 28%", "music-production-singer-songwriter": "center 28%"}  # keep the singer's face and mic in frame

def page_hero(p, crumbs, slug=None, lead=None):
    img = p.get("img")
    bg = f' style="--img:url(\'{media(img, 1920)}\');--pos:{POS.get(slug, "center")}"' if img else ""
    lead_html = f'<p class="ph-lead">{lead}</p>' if lead else ""
    return f'''<header class="phero{" has-img" if img else ""}"{bg}>
  <div class="wrap">{f'<nav class="crumbs" aria-label="מיקום באתר"><a href="/">ראשי</a>{crumbs}</nav>' if crumbs else ""}
  <h1>{p["title"]}</h1>{lead_html}</div>
</header>'''

def aside(slug):
    if slug in SECTION_OF:
        top, head, en, lst = SECTION_OF[slug]
    else:
        head, en, lst = "שירותים", "Services", SERVICES
    lis = "".join(f'<li><a href="{link(s)}"{" aria-current=\"page\"" if s == slug else ""}>{PAGES[s]["title"]}</a></li>' for s in lst)
    return f'''<aside class="side">
  <nav class="side-nav" aria-label="{head}"><p class="side-h">{head}</p><ul>{lis}</ul></nav>
  <div class="side-card"><p class="side-h">קביעת סשן</p><a class="big-phone" href="tel:036481791" dir="ltr">{PHONE}</a><a class="btn btn-line" href="#book">שלחו הודעה</a></div>
</aside>'''

def cta_band(slug=None):
    path = TOPIC_OF.get(SECTION_OF[slug][0]) if slug in SECTION_OF else None
    return f'''<section class="book" id="book"><div class="wrap contact-grid">
  <div><h2 class="sec-h">דברו איתנו</h2><p class="muted">ספרו לנו בכמה מילים מה אתם מתכננים, ונחזור אליכם עם הצעה.</p>{contact_lines()}</div>
  {form("b-" + (slug or "x"), path)}
</div></section>'''

INTRO = {
    "recording-studio-tel-aviv": "חדרי הקלטה ובקרה שתוכננו ונבנו בקפידה, חדר בקרה עם ציוד קצה דיגיטלי ואנלוגי, וצוות שמכיר כל פינה בחדר.",
    "podcast-recording": "אולפן מעוצב, סטים שונים של ישיבה, צילום בשלוש זוויות וסאונד אולפני משובח. מגיעים ומדברים, ואת כל השאר אנחנו עושים.",
    "music-production": "מהרעיון הראשון ועד השיר המוגמר: עיבוד, נגנים, הקלטה, מיקס ומאסטר, עם מפיק שמלווה אתכם בכל שלב.",
}

def marquee(items, cls="", secs=60):
    """Auto-scrolling strip: the set is rendered twice and the track slides by half its width."""
    return (f'<div class="mq-box"><button class="mq-btn" type="button" aria-pressed="false" data-mq>עצירת התנועה</button>'
            f'<div class="mq {cls}" style="--secs:{secs}s"><div class="mq-track">'
            f'<div class="mq-set">{items}</div><div class="mq-set" aria-hidden="true" inert>{items}</div></div></div></div>')

def vmarquee(items, rev=False, secs=90):
    return (f'<div class="vq{" rev" if rev else ""}" style="--secs:{secs}s"><div class="vq-track">'
            f'<div class="vq-set">{items}</div><div class="vq-set" aria-hidden="true" inert>{items}</div></div></div>')

def hub_page(slug):
    top, he, en, lst = SECTION_OF[slug]
    p = PAGES[slug]
    blocks = [b for b in p["blocks"] if b[0] != "podcasts"]
    text = render_blocks(slug, blocks)
    if slug == "podcast-recording":
        # Text first; the episode covers run up and down the margins (desktop) or slide below it (mobile).
        half = (len(PODCASTS) + 1) // 2
        left = "".join(build.pod_fig(*x) for x in PODCASTS[:half])
        right = "".join(build.pod_fig(*x) for x in PODCASTS[half:])
        return page_hero(p, "", slug, INTRO[slug]) + f"""
<section class="pod-frame" aria-label="פודקאסטים שהוקלטו אצלנו"><button class="mq-btn pf-btn" type="button" aria-pressed="false" data-mq>עצירת התנועה</button><div class="pf-wrap">
  {vmarquee(left)}
  <article class="prose pf-text">{text}</article>
  {vmarquee(right, rev=True, secs=110)}
</div>
<div class="pf-mobile"><h2 class="sec-h wrap">פודקאסטים שהוקלטו אצלנו</h2>{marquee(pods(), "pods-2row", 120)}</div>
</section>""" + cta_band(slug)
    tiles = "".join(f'<a class="tile" href="{link(s)}"><span class="tile-im" style="--img:url(\'{G(PHOTO.get(s) or PHOTO[slug], True)}\')"></span><span class="tile-t">{PAGES[s]["title"]}</span><span class="tile-go" aria-hidden="true">←</span></a>' for s in lst if s != slug)
    proof = {
        "recording-studio-tel-aviv": f'<div class="sh"><h2 class="sec-h">העבודות שלנו</h2></div><div class="covers">{covers()}</div>',
        "music-production": f'<div class="sh"><h2 class="sec-h">רז בורג</h2></div><p class="muted narrowp">מפיק מוזיקלי, נגן ומעצב סאונד, הבעלים של האולפן. עבודות הפקה נבחרות באתר האישי: <a href="https://www.razburg.com">razburg.com</a></p>{marquee(prod_covers(), "covers-mq", 160)}',
    }[slug]
    return page_hero(p, "", slug, INTRO.get(slug)) + f"""
<section class="block"><div class="wrap"><div class="sh"><h2 class="sec-h">מה אנחנו עושים</h2></div><div class="tiles">{tiles}</div></div></section>
<section class="block alt"><div class="wrap">{proof}</div></section>
<div class="wrap split"><article class="prose">{text}</article>{aside(slug)}</div>""" + cta_band(slug)

def inner_page(slug):
    p = PAGES[slug]
    if slug in TOPIC_OF:
        return hub_page(slug)
    crumbs = crumbs_for(slug)
    body = render_blocks(slug, p["blocks"])
    if slug == "recording-studio-equipment":
        intro, racks = body.split('<div class="racks"', 1)
        return page_hero(p, crumbs, slug) + f'<div class="wrap gear-intro prose">{intro}</div><div class="wrap"><div class="racks"{racks}</div>' + cta_band(slug)
    if slug in ("privacy", "terms", "accessibility"):
        return page_hero(p, "", slug) + f'<div class="wrap narrow prose">{body}</div>'
    return page_hero(p, crumbs, slug) + f'<div class="wrap split"><article class="prose">{body}</article>{aside(slug)}</div>' + cta_band(slug)

COLLAGE = ["fb-043e", "fb-045", "fb-061"]  # Raz 2026-11-26: option 3, slow crossfade between the three rooms
WORLDS = [
    ("recording-studio-tel-aviv", "fb-043e", ["הקלטת שירים", "מיקס ועריכות", "אולפן נייד", "פלייבקים"], "covers"),
    ("podcast-recording", "fb-045", ["הקלטה וצילום פודקאסטים", "עריכת סאונד ווידאו", "שידורי זום", "פוסט פרודקשן"], "pods"),
    ("music-production", "fb-061", ["זמרים ויוצרים", "להקות", "פרסומות", "מוזיקה לסרטים"], "lead"),
]

def home():
    col = "".join(f'<div class="hf" style="background-image:url(\'{G(i)}\')"></div>' for i in COLLAGE)
    idx = "".join(f'<a href="{link(top)}"><span>{he}</span></a>' for top, he, en, _ in SECTIONS)
    worlds = ""
    for n, (top, ph, items, kind) in enumerate(WORLDS):
        _, he, en, _ = SECTION_OF[top]
        extra = {"covers": marquee(covers(), "covers-mq", 90), "pods": marquee(pods(), "pods-2row", 120), "lead": f'<p class="lead">{INTRO[top]}</p>'}[kind]
        worlds += f"""<section class="world{" flip" if n % 2 else ""}"><a class="w-ph" href="{link(top)}" style="--img:url('{G(ph)}')" aria-label="{he}"></a>
  <div class="w-tx"><h2>{he}</h2><ul>{"".join(f"<li>{x}</li>" for x in items)}</ul>{extra}<a class="more" href="{link(top)}">{he} בתמוז <span aria-hidden="true">←</span></a></div></section>"""
    return f"""<header class="hero"><div class="h-fade" aria-hidden="true">{col}</div>
  <div class="h-text"><h1 class="h-logo"><img src="/img/logo-white.png" alt="Tamuz Studios תמוז אולפן הקלטות ואולפן פודקאסטים בתל אביב" width="900" height="220"></h1>
  <p class="h-claim">סאונד בלי פשרות. בכל תחום.</p><p class="h-sub">הקלטה ומיקס · פודקאסטים ומדיה · הפקה מוזיקלית</p></div>
</header>
<nav class="index" aria-label="התחומים שלנו">{idx}</nav>
{worlds}
<section class="block about-b"><div class="wrap about">
  <div class="about-im" style="--img:url('{G("fb-043e", True)}')" role="img" aria-label="חדר הבקרה של האולפן"></div>
  <div class="prose"><h2 class="sec-h">על האולפן</h2>
  <p>אולפני תמוז, אולפן הקלטות ואולפן פודקאסטים בצפון תל אביב, הוקמו בשנת 2004, והחל משנת 2006 הם בבעלותו ובניהולו של רז בורג, מפיק מוזיקלי, טכנאי ומעצב סאונד, שמנהל יחד עם צוות האולפן את הסשנים השונים.</p>
  <p>האולפן תוכנן בקפידה, והאקוסטיקה שלו מאפשרת הקלטות מכל הסוגים, לצד סטים מעוצבים להקלטה וצילום של פודקאסטים ולשידורים מהאולפן.</p>
  <p>כאן אפשר להכיר את רז בורג ואת העבודות שלו: <a href="https://www.razburg.com">razburg.com</a></p></div>
</div></section>
<section class="book" id="contact"><div class="wrap contact-grid">
  <div><h2 class="sec-h">בואו לבקר באולפן</h2><p class="muted">ספרו לנו מה אתם רוצים להקליט, ונחזור אליכם עם הצעה.</p>{contact_lines()}</div>
  {form("home")}
</div></section>"""

def contact():
    p = PAGES["contact"]
    soc = "".join(f'<li><a href="{u}" target="_blank" rel="noopener">{n}</a></li>' for n, u in SOCIAL)
    return page_hero(p, "", "contact") + f'''<div class="wrap contact-grid block">
  <div><h2 class="sec-h">דברו איתנו</h2><a class="big-phone" href="tel:036481791" dir="ltr">{PHONE}</a>{contact_lines()}<ul class="social">{soc}</ul></div>
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
  <div><p class="foot-h">הקלטה ומיקס</p><ul class="foot-list">{col(RECORDING)}</ul></div>
  <div><p class="foot-h">פודקאסטים ומדיה</p><ul class="foot-list">{col(MEDIA)}</ul><p class="foot-h" style="margin-top:1.4rem">הפקה מוזיקלית</p><ul class="foot-list">{col(PRODUCE[:1] + PRODUCE[4:])}</ul></div>
  <div><p class="foot-h">עקבו אחרינו</p><ul class="foot-list">{soc}<li><a href="https://www.razburg.com">רז בורג · razburg.com</a></li></ul></div>
</div><div class="wrap foot-base"><span>© 2026 אולפני תמוז · רז בורג</span><span class="foot-legal"><a href="/terms">תנאי שימוש ומדיניות</a><a href="/privacy">מדיניות פרטיות</a><a href="/accessibility">הצהרת נגישות</a></span></div></footer>'''

build.nav, build.page_hero, build.aside, build.cta_band, build.inner_page = nav, page_hero, aside, cta_band, inner_page
build.home, build.contact, build.services, build.footer = home, contact, services, footer
