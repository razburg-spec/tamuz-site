"""v2 design (Nov 2026): Secular One + Heebo, brick/wood/tungsten palette, real studio photos.

Imported by prod.py right after `build`; it swaps the page builders that changed and keeps
all page texts, URLs and SEO data from the v1 generator.
"""
import html
import build
from build import PAGES, PHONE, EMAIL, ADDRESS, MAPS, SOCIAL, SERVICES, PRODUCTION, contact_lines, form, render_blocks, inline
from content_c import PODCASTS

_wix_media = build.media

def media(fid, w=1600, h=None, q=80):
    """Local photos are named 'img:<file>'; everything else still comes from Wix until it is self-hosted."""
    if fid and fid.startswith("img:"):
        name = fid[4:]
        return f"/img/{name}-m.jpg" if w <= 900 else f"/img/{name}.jpg"
    return _wix_media(fid, w, h, q)

build.media = media

# Hero photo for every page (all picked and approved by Raz, Nov 2026)
PHOTO = {
    "": "brick", "recording-studio-tel-aviv": "fb-078", "songs-recordings": "ig-027", "mixing-audio-edits": "fb-024",
    "post-production-sound-design": "fb-050", "podcast-recording": "fb-045", "livestreaming": "fb-021",
    "live-recording": "ig-026", "mobile-recording-studio": "ig-038", "sound-protools-lessons": "fb-053",
    "original-music-movies-commercials": "fb-046", "playbacks": "ig-030", "music-production": "fb-061",
    "music-production-singer-songwriter": "ig-034", "music-production-bands": "ig-036",
    "music-production-commercials": "fb-013", "recording-studio-equipment": "fb-025", "contact": "fb-043",
    "services": "fb-014", "blog": "fb-008", "privacy": None,
}
for slug, ph in PHOTO.items():
    if slug in PAGES:
        PAGES[slug]["img"] = f"img:{ph}" if ph else None

# The three main sections
RECORDING = ["recording-studio-tel-aviv", "songs-recordings", "mixing-audio-edits", "live-recording", "mobile-recording-studio", "playbacks", "sound-protools-lessons"]
MEDIA = ["podcast-recording", "livestreaming", "post-production-sound-design"]
PRODUCE = ["music-production", "music-production-singer-songwriter", "music-production-bands", "music-production-commercials", "original-music-movies-commercials"]
SECTIONS = [("recording-studio-tel-aviv", "הקלטה ומיקס", RECORDING), ("podcast-recording", "פודקאסטים ומדיה", MEDIA), ("music-production", "הפקה מוזיקלית", PRODUCE)]
SECTION_OF = {s: (top, label, lst) for top, label, lst in SECTIONS for s in lst}

link = lambda slug: "/" + (slug or "")

def nav():
    items = []
    for i, (top, label, sub) in enumerate(SECTIONS):
        subl = "".join(f'<li><a href="{link(s)}">{PAGES[s]["title"]}</a></li>' for s in sub)
        items.append(f'<li class="has-sub"><a href="{link(top)}">{label}</a><button class="sub-toggle" type="button" aria-expanded="false" aria-controls="sub{i}" aria-label="פתיחת תפריט {label}"><span aria-hidden="true">▾</span></button><ul class="sub" id="sub{i}">{subl}</ul></li>')
    for slug, label in [("recording-studio-equipment", "ציוד"), ("blog", "בלוג"), ("contact", "צור קשר")]:
        items.append(f'<li><a href="{link(slug)}">{label}</a></li>')
    return "".join(items)

def page_hero(p, crumbs):
    bg = f' style="--img:url(\'{media(p["img"], 1920)}\')"' if p.get("img") else ""
    return f'''<header class="phero{" has-img" if p.get("img") else ""}"{bg}>
  <div class="wrap"><nav class="crumbs" aria-label="מיקום באתר"><a href="/">תמוז</a>{crumbs}</nav><h1>{p["title"]}</h1></div>
</header>'''

def crumbs_for(slug):
    if slug in SECTION_OF:
        top, label, _ = SECTION_OF[slug]
        return "" if slug == top else f'<span>/</span><a href="{link(top)}">{label}</a>'
    return ""

def aside(slug):
    top, head, lst = SECTION_OF.get(slug, ("", "שירותים", SERVICES))
    lis = "".join(f'<li><a href="{link(s)}"{" aria-current=\"page\"" if s == slug else ""}>{PAGES[s]["title"]}</a></li>' for s in lst)
    return f'''<aside class="side">
  <nav class="side-nav" aria-label="{head}"><p class="eyebrow">{head}</p><ul>{lis}</ul></nav>
  <div class="side-card"><p class="eyebrow">דברו איתנו</p><a class="big-phone" href="tel:036481791" dir="ltr">{PHONE}</a><a class="btn btn-ghost" href="/contact">שלחו הודעה</a></div>
</aside>'''

def cta_band():
    return f'''<section class="cta-band"><div class="wrap cta-inner">
  <div><p class="eyebrow">צרו קשר</p><p class="cta-h">בואו לבקר באולפן</p></div>
  <div class="cta-actions"><a class="btn btn-accent" href="tel:036481791" dir="ltr">{PHONE}</a><a class="btn btn-ghost" href="/contact">שלחו הודעה</a></div>
</div></section>'''

def inner_page(slug):
    p = PAGES[slug]
    crumbs = crumbs_for(slug)
    body = render_blocks(slug, p["blocks"])
    if slug == "recording-studio-equipment":
        intro, racks = body.split('<div class="racks"', 1)
        return page_hero(p, crumbs) + f'<div class="wrap gear-intro prose">{intro}</div><div class="wrap"><div class="racks"{racks}</div>' + cta_band()
    if slug in ("privacy", "blog"):
        return page_hero(p, "") + f'<div class="wrap narrow prose">{body}</div>'
    return page_hero(p, crumbs) + f'<div class="wrap split"><article class="prose">{body}</article>{aside(slug)}</div>' + cta_band()

COVERS = [("c51", "Yoni Rechter", "Svivenu"), ("c144", "Ariel Zilber", "Hee Hashir"), ("c75", "Voca People", "Voca Dance"),
          ("c33", "Kobi Oz", "Chalom Akevotaich"), ("c118", "Hanan Yovel", "Erev Kaitz Ham"), ("c45", "Noam Rotem", "Neshoret"),
          ("c67", "Noam Rotem & Itamar Rothchild", "Ezra Bad"), ("c84", "Hanan Yovel, Ori Harpaz & Dorit Reuveni", "Shloshtenu Behofaa Haya"),
          ("c85", "Nathan Slor & Oshik Levi", "Tmuna"), ("c113", "Elai Botner", "Nipagesh Bachalomot"), ("c104", "Jonathan Bitton", "Shoshanat Haamakim"),
          ("c99", "Amir Pery", "Nofel Lemala"), ("c37", "Igal Toledano", "Hageshem Harishon"), ("c124", "Rotem Leshem", "Yesh Li Bait")]

QUOTES = [("אולפן ההקלטות \"תמוז\" הינו בית הקלטות עבורי. ציוד ומיכשור אינם מספיקים בלא אישיותו המקצועית והמלבבת של רז בורג.", "יאיר שרגאי"),
          ("הקלטתי תופים באולפני תמוז לאלבום של הלהקה שלי ולפרויקטים אחרים והייתי מאוד מרוצה מהתוצאות.", "גור שפיגל, מתופף"),
          ("רז פשוט גאון מוזיקלי! מקצוען אמיתי, קשוב, סבלני, יצירתי ומקסים.", "טלי אליהו, זמרת וכותבת")]

def home():
    svc = [
        ("recording-studio-tel-aviv", "הקלטה ומיקס", "fb-078", ["הקלטת להקות, זמרים ותופים", "מיקס ועריכות סאונד", "הקלטת הופעות ואולפן נייד"]),
        ("podcast-recording", "פודקאסטים ומדיה", "fb-045", ["הקלטה וצילום וידאו", "סטים מעוצבים לשיחה", "אולפן שידור ופוסט פרודקשן"]),
        ("music-production", "הפקה מוזיקלית", "fb-061", ["הפקה לזמרים, יוצרים ולהקות", "מוזיקה מקורית לסרטים ופרסומות", "הפקת פלייבקים"]),
    ]
    cards = "".join(f'''<a class="card" href="{link(s)}"><span class="card-im" style="--img:url('/img/{im}-m.jpg')"></span><span class="card-bd"><span class="card-t">{t}</span><ul>{"".join(f"<li>{x}</li>" for x in li)}</ul><span class="more">לפרטים <span aria-hidden="true">←</span></span></span></a>''' for s, t, im, li in svc)
    rooms = [("fb-043", "חדר הבקרה", "מוניטורים, פריאמפים וחלון לחדר ההקלטה"), ("ig-026", "חדר ההקלטה", "תופים, להקות והרכבים"), ("fb-055", "תא ההקלטה", "שירה, כלי מיתר ודיבור")]
    room = lambda r, cls="": f'<figure class="room{cls}" style="--img:url(\'/img/{r[0]}{"" if cls else "-m"}.jpg\')"><figcaption><b>{r[1]}</b><span>{r[2]}</span></figcaption></figure>'
    sets = [("fb-045", "סט הלבנים", ["2–4 משתתפים", "כורסאות", "צילום וידאו"]), ("fb-021", "סט הקיר האדום", ["1–2 משתתפים", "תאורת מראה", "צילום וידאו"])]
    sets_html = "".join(f'<figure class="set"><img src="/img/{im}-m.jpg" alt="{t} באולפן תמוז" loading="lazy" width="900" height="600"><figcaption><b>{t}</b><span class="spec">{"".join(f"<span>{x}</span>" for x in sp)}</span></figcaption></figure>' for im, t, sp in sets)
    pods = "".join(build.pod_fig(*p) for p in PODCASTS)
    covers = "".join(f'<figure class="cv"><img src="/img/{c}.jpg" alt="{html.escape(a)} – {html.escape(t)}" loading="lazy" width="360" height="360"><figcaption><b dir="ltr">{html.escape(a)}</b><span dir="ltr">{html.escape(t)}</span></figcaption></figure>' for c, a, t in COVERS)
    quotes = "".join(f'<blockquote><p>{html.escape(q)}</p><footer>{html.escape(w)}</footer></blockquote>' for q, w in QUOTES)
    strip = "".join(f'<img src="/img/{p}-m.jpg" alt="" loading="lazy">' for p in ["ig-018", "fb-063", "ig-029", "fb-075", "ig-004", "fb-066"])
    return f'''<header class="hero" style="--img:url('/img/brick.jpg')">
  <div class="wrap hero-inner">
    <p class="eyebrow">מאז 2004 · צפון תל אביב</p>
    <h1>אולפן הקלטות ופודקאסטים</h1>
    <p class="hero-sub">הקלטה ומיקס, פודקאסטים ומדיה, והפקה מוזיקלית. בחדר עם לבנים, עץ ואור חם, ועם יחס אישי בכל סשן.</p>
    <div class="hero-actions"><a class="btn btn-accent" href="/contact">בואו לבקר באולפן</a><a class="btn btn-ghost" href="#credits">לשמוע עבודות</a></div>
    <div class="stats"><div><b class="num">2004</b><span>שנת ההקמה</span></div><div><b class="num">+45</b><span>פודקאסטים הוקלטו כאן</span></div><div><b class="num">4.8</b><span>בגוגל, 54 ביקורות</span></div></div>
  </div>
</header>
<section class="block"><div class="wrap">
  <div class="sh"><div><p class="eyebrow">מה עושים כאן</p><h2 class="sec-h">שלושה תחומים, אולפן אחד</h2></div><p>כל פרויקט מקבל את אותו החדר, את אותו הציוד ואת אותו היחס האישי, משיר אחד ועד עונה שלמה של פודקאסט.</p></div>
  <div class="cards">{cards}</div>
</div></section>
<section class="block alt"><div class="wrap">
  <div class="sh"><div><p class="eyebrow">האולפן</p><h2 class="sec-h">לבנים, עץ ואור טונגסטן</h2></div><p>חדר הקלטה אקוסטי ומרווח וחדר בקרה עם מיטב הציוד האנלוגי והדיגיטלי. מעלית, חניה בשפע ומטבח מאובזר.</p></div>
  <div class="rooms">{room(rooms[0], " r1")}<div class="rstack">{room(rooms[1])}{room(rooms[2])}</div></div>
  <p class="center"><a class="btn btn-ghost" href="/recording-studio-equipment">לרשימת הציוד</a></p>
</div></section>
<section class="block" id="podcasts"><div class="wrap">
  <div class="sh"><div><p class="eyebrow">פודקאסטים ומדיה</p><h2 class="sec-h">הסטים שלנו</h2></div><p>כל סט מוכן לצילום: תאורה, מיקרופונים ומצלמות. בוחרים סט, מתיישבים ומקליטים.</p></div>
  <div class="sets">{sets_html}</div>
  <h3 class="sub-h">פודקאסטים שהוקלטו אצלנו</h3>
  <div class="pod-grid">{pods}</div>
  <p class="center"><a class="btn btn-ghost" href="/podcast-recording">הקלטת פודקאסט</a></p>
</div></section>
<section class="block alt" id="credits"><div class="wrap">
  <div class="sh"><div><p class="eyebrow">קרדיטים</p><h2 class="sec-h">הוקלט ומוקס בתמוז</h2></div><p>מיוני רכטר ואריאל זילבר ועד Voca People. חלק מהאלבומים שעברו כאן.</p></div>
  <div class="covers">{covers}</div>
</div></section>
<div class="strip" aria-hidden="true">{strip}</div>
<section class="block"><div class="wrap">
  <div class="sh"><div><p class="eyebrow">אומרים עלינו</p><h2 class="sec-h">4.8 בגוגל</h2></div></div>
  <div class="quotes">{quotes}</div>
</div></section>
<section class="block alt"><div class="wrap about">
  <div class="prose"><p class="eyebrow">אודות</p><h2 class="sec-h">עשרים שנה של סאונד בצפון תל אביב</h2>
  <p>תמוז הוקם בשנת 2004, ומאז 2006 הוא בבעלות רז בורג, מפיק מוזיקלי, טכנאי ומעצב סאונד, שמנהל בעצמו כל סשן.</p>
  <p>האולפן תוכנן על ידי אקוסטיקאים ומאפשר הקלטות מכל הסוגים: תופים, רביעיית כלי קשת, כלי הקשה, שירה ואקפלה. חשוב לנו להיות יותר מעוד אולפן, עם אווירה ביתית ויחס אישי.</p>
  <p>להכיר את רז ואת העבודות שלו: <a href="https://www.razburg.com">razburg.com</a></p></div>
  <div class="about-im" style="--img:url('/img/fb-062-m.jpg')" role="img" aria-label="רז בורג באולפן תמוז"></div>
</div></section>
<section class="contact-home" id="contact"><div class="wrap contact-grid">
  <div><p class="eyebrow">צרו קשר</p><h2 class="sec-h">בואו לבקר באולפן</h2><p>ספרו לנו מה אתם רוצים להקליט, ונחזור אליכם עם הצעה.</p>{contact_lines()}</div>
  {form("home")}
</div></section>'''

def contact():
    p = PAGES["contact"]
    soc = "".join(f'<li><a href="{u}" target="_blank" rel="noopener">{n}</a></li>' for n, u in SOCIAL)
    return page_hero(p, "") + f'''<div class="wrap contact-grid block">
  <div><h2 class="sec-h">דברו איתנו</h2><a class="big-phone" href="tel:036481791" dir="ltr">{PHONE}</a>{contact_lines()}<p class="eyebrow" style="margin-top:2rem">חפשו אותנו</p><ul class="social">{soc}</ul></div>
  <div><h2 class="sec-h">שלחו הודעה</h2>{form("contact")}</div>
</div>'''

def services():
    p = PAGES["services"]
    return page_hero(p, "") + f'''<div class="wrap contact-grid block">
  <div><h2 class="sec-h">צרו קשר</h2>{contact_lines()}</div>
  <div>{form("services")}</div>
</div>'''

def footer():
    col = lambda lst: "".join(f'<li><a href="{link(s)}">{PAGES[s]["title"]}</a></li>' for s in lst)
    soc = "".join(f'<li><a href="{u}" target="_blank" rel="noopener">{n}</a></li>' for n, u in SOCIAL)
    return f'''<footer class="foot"><div class="wrap foot-grid">
  <div><p class="logo-word">תמוז</p><p class="foot-tag">אולפן הקלטות ופודקאסטים, מאז 2004</p>{contact_lines("contact-lines")}</div>
  <div><p class="eyebrow">הקלטה ומיקס</p><ul class="foot-list">{col(RECORDING[:5])}</ul></div>
  <div><p class="eyebrow">פודקאסטים ומדיה</p><ul class="foot-list">{col(MEDIA)}</ul><p class="eyebrow" style="margin-top:1.4rem">הפקה מוזיקלית</p><ul class="foot-list">{col(PRODUCE[:1] + PRODUCE[4:])}</ul></div>
  <div><p class="eyebrow">חפשו אותנו</p><ul class="foot-list">{soc}<li><a href="https://www.razburg.com">רז בורג · razburg.com</a></li></ul></div>
</div><div class="wrap foot-base"><span>© Raz Burg \\ Tamuz Studios 2026</span><a href="/privacy">מדיניות פרטיות</a></div></footer>'''

build.nav, build.page_hero, build.aside, build.cta_band, build.inner_page = nav, page_hero, aside, cta_band, inner_page
build.home, build.contact, build.services, build.footer = home, contact, services, footer
