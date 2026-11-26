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


# ---------------------------------------------------------------------------
# Visitor paths (Raz, 2026-11-26): the home screen splits visitors by what they came for,
# and each of the three audiences then stays on its own route with its own proof and CTA.
PATHS = {
    "rec": dict(top="recording-studio-tel-aviv", pages=RECORDING, label="הקלטה ומיקס", photo="fb-078",
        door="מקליטים או ממקססים", door_sub="שירים, להקות, תופים, הופעות ומיקס",
        tagline="חדר הקלטה אקוסטי, ציוד אנלוגי ודיגיטלי, וטכנאי שמכיר כל פינה בחדר. משיר אחד ועד אלבום שלם.",
        promise=["הקלטת זמרים, להקות ותופים", "מיקס ועריכות סאונד, גם לחומר שהוקלט במקום אחר", "הקלטת הופעות ואולפן נייד", "פלייבקים ושיעורי פרו טולס"],
        steps=[("מתאמים", "מספרים לנו מה מקליטים, ומתכננים יחד את הסשן."), ("מקליטים", "מגיעים לאולפן מוכן: מיקרופונים, אוזניות וסאונד, וזמן לנסות."), ("מיקס ומאסטר", "מקבלים מיקס, סבב תיקונים, וקבצים מוכנים להפצה.")],
        cta="קביעת סשן הקלטה", topic="הקלטה ומיקס"),
    "pod": dict(top="podcast-recording", pages=MEDIA, label="פודקאסטים ומדיה", photo="fb-045",
        door="מקליטים פודקאסט", door_sub="אודיו ווידאו, סטים מעוצבים, עריכה",
        tagline="מגיעים, מתיישבים ומדברים. את כל השאר אנחנו עושים: סאונד, צילום בשלוש מצלמות, עריכה וקבצים מוכנים להעלאה.",
        promise=["צילום וידאו בשלוש זוויות עם תאורה מקצועית", "סטים מעוצבים לשיחה של 1 עד 4 משתתפים", "עריכה, ניקוי סאונד וקטעים קצרים לרשתות", "הקלטה גם אצלכם, במשרד או באירוע"],
        steps=[("שיחת היכרות", "מספרים לנו על הפודקאסט, ובוחרים יחד סט ופורמט."), ("יום הקלטה", "מגיעים לאולפן והכל מוכן. אתם רק מדברים."), ("פרק מוכן", "מקבלים פרק ערוך באודיו ובווידאו, מוכן לספוטיפיי וליוטיוב.")],
        cta="קביעת סשן פודקאסט", topic="פודקאסט"),
    "prod": dict(top="music-production", pages=PRODUCE, label="הפקה מוזיקלית", photo="fb-061",
        door="מפיקים שיר", door_sub="לזמרים, יוצרים, להקות ופרסומות",
        tagline="מרעיון או סקיצה בטלפון ועד שיר מוכן לרדיו. רז בורג מלווה כל הפקה מההתחלה ועד הסוף.",
        promise=["עיבוד והפקה לזמרים ויוצרים", "הפקה ללהקות", "מוזיקה מקורית לסרטים ולפרסומות", "הקלטה, מיקס ומאסטר באותו מקום"],
        steps=[("נפגשים", "מקשיבים לשיר ולרפרנסים, ומגדירים יחד את הכיוון."), ("מפיקים", "עיבוד, נגנים והקלטות באולפן, עם עדכונים לאורך הדרך."), ("משחררים", "מיקס ומאסטר, ושיר מוכן לרדיו ולפלטפורמות.")],
        cta="שיחת היכרות על הפקה", topic="הפקה מוזיקלית"),
}
PATH_ORDER = ["rec", "pod", "prod"]
PATH_OF = {s: k for k, p in PATHS.items() for s in p["pages"]}
TOPICS = [("הקלטה ומיקס", "rec"), ("פודקאסט", "pod"), ("הפקה מוזיקלית", "prod"), ("משהו אחר", "")]

def form(fid, path=None):
    opts = "".join(f'<option value="{t}"{" selected" if k and k == path else ""} data-path="{k}">{t}</option>' for t, k in TOPICS)
    base = build.form(fid)
    sel = f'<label for="{fid}-tp">במה מדובר?<select id="{fid}-tp" name="topic" data-topic>{opts}</select></label>\n  '
    return base.replace('<label for="' + fid + '-msg">', sel + '<label for="' + fid + '-msg">', 1)

def _pods(n=None):
    return "".join(build.pod_fig(*p) for p in (PODCASTS[:n] if n else PODCASTS))

def _covers(lst=None):
    return "".join(f'<figure class="cv"><img src="/img/{c}.jpg" alt="{html.escape(a)} – {html.escape(t)}" loading="lazy" width="360" height="360"><figcaption><b dir="ltr">{html.escape(a)}</b><span dir="ltr">{html.escape(t)}</span></figcaption></figure>' for c, a, t in (lst or COVERS))

def _quotes(lst=None):
    return "".join(f'<blockquote><p>{html.escape(q)}</p><footer>{html.escape(w)}</footer></blockquote>' for q, w in (lst or QUOTES))

ROOMS = [("fb-043", "חדר הבקרה", "מוניטורים, פריאמפים וחלון לחדר ההקלטה"), ("ig-026", "חדר ההקלטה", "תופים, להקות והרכבים"), ("fb-055", "תא ההקלטה", "שירה, כלי מיתר ודיבור")]
SETS = [("fb-045", "סט הלבנים", ["2–4 משתתפים", "כורסאות", "צילום וידאו"]), ("fb-021", "סט הקיר האדום", ["1–2 משתתפים", "תאורת מראה", "צילום וידאו"])]

def _room(r, cls=""):
    return f'<figure class="room{cls}" style="--img:url(\'/img/{r[0]}{"" if cls else "-m"}.jpg\')"><figcaption><b>{r[1]}</b><span>{r[2]}</span></figcaption></figure>'

def _rooms():
    return f'<div class="rooms">{_room(ROOMS[0], " r1")}<div class="rstack">{_room(ROOMS[1])}{_room(ROOMS[2])}</div></div>'

def _sets():
    return '<div class="sets">' + "".join(f'<figure class="set"><img src="/img/{im}-m.jpg" alt="{t} באולפן תמוז" loading="lazy" width="900" height="600"><figcaption><b>{t}</b><span class="spec">{"".join(f"<span>{x}</span>" for x in sp)}</span></figcaption></figure>' for im, t, sp in SETS) + "</div>"

def path_proof(k):
    """The evidence each audience cares about."""
    if k == "pod":
        return f'''<div class="sh"><div><p class="eyebrow">הסטים</p><h2 class="sec-h">בוחרים סט ומתיישבים</h2></div><p>כל סט מוכן לצילום: תאורה, מיקרופונים ומצלמות.</p></div>{_sets()}
  <h3 class="sub-h">{len(PODCASTS)} פודקאסטים הוקלטו אצלנו</h3><div class="pod-grid">{_pods()}</div>'''
    if k == "rec":
        return f'''<div class="sh"><div><p class="eyebrow">האולפן</p><h2 class="sec-h">לבנים, עץ ואור טונגסטן</h2></div><p>חדר הקלטה אקוסטי ומרווח וחדר בקרה עם מיטב הציוד. <a href="/recording-studio-equipment">לרשימת הציוד</a></p></div>{_rooms()}
  <h3 class="sub-h">הוקלט ומוקס בתמוז</h3><div class="covers">{_covers()}</div>
  <div class="quotes">{_quotes(QUOTES[:2])}</div>'''
    return f'''<div class="sh"><div><p class="eyebrow">המפיק</p><h2 class="sec-h">רז בורג</h2></div><p>מפיק מוזיקלי, נגן ומעצב סאונד, הבעלים של תמוז מאז 2006. עבודות נוספות של רז: <a href="https://www.razburg.com">razburg.com</a></p></div>
  <div class="quotes">{_quotes(QUOTES[2:] + QUOTES[:1])}</div>
  <h3 class="sub-h">עבודות שעברו באולפן</h3><div class="covers">{_covers()}</div>'''

def path_steps(k):
    st = "".join(f'<li><span class="num">{i}</span><b>{t}</b><p>{d}</p></li>' for i, (t, d) in enumerate(PATHS[k]["steps"], 1))
    return f'<ol class="steps">{st}</ol>'

def path_cta(k, fid):
    p = PATHS[k]
    return f'''<section class="cta-band path-cta" id="book"><div class="wrap contact-grid">
  <div><p class="eyebrow">{p["label"]}</p><p class="cta-h">{p["cta"]}</p><p>ספרו לנו בכמה מילים מה אתם מתכננים, ונחזור אליכם עוד היום עם הצעה.</p>
  <a class="big-phone" href="tel:036481791" dir="ltr">{PHONE}</a></div>
  {form(fid, k)}
</div></section>'''

def hub_page(slug):
    k = PATH_OF[slug]; P = PATHS[k]; p = PAGES[slug]
    subs = [s for s in P["pages"] if s != slug]
    subcards = "".join(f'<a class="mini" href="{link(s)}"><span class="mini-im" style="--img:url(\'/img/{PHOTO.get(s) or P["photo"]}-m.jpg\')"></span><span class="mini-t">{PAGES[s]["title"]}</span></a>' for s in subs)
    promise = "".join(f"<li>{x}</li>" for x in P["promise"])
    blocks = [b for b in p["blocks"] if b[0] != "podcasts"]
    body = render_blocks(slug, blocks)
    bg = f' style="--img:url(\'{media(p["img"], 1920)}\')"'
    return f'''<header class="phero has-img hub-hero"{bg}>
  <div class="wrap"><nav class="crumbs" aria-label="מיקום באתר"><a href="/">תמוז</a></nav>
  <p class="eyebrow">{P["label"]}</p><h1>{p["title"]}</h1><p class="hero-sub">{P["tagline"]}</p>
  <ul class="ticks">{promise}</ul>
  <div class="hero-actions"><a class="btn btn-accent" href="#book">{P["cta"]}</a><a class="btn btn-ghost" href="#proof">לראות עבודות</a></div></div>
</header>
<section class="block"><div class="wrap">
  <div class="sh"><div><p class="eyebrow">איך זה עובד</p><h2 class="sec-h">שלושה צעדים</h2></div></div>{path_steps(k)}
</div></section>
<section class="block alt" id="proof"><div class="wrap">{path_proof(k)}</div></section>
<section class="block"><div class="wrap">
  <div class="sh"><div><p class="eyebrow">במסלול הזה</p><h2 class="sec-h">מה עוד אפשר לעשות</h2></div></div><div class="minis">{subcards}</div>
</div></section>
<div class="wrap narrow prose hub-text">{body}</div>''' + path_cta(k, slug)

def inner_page(slug):
    p = PAGES[slug]
    if slug in PATH_OF and slug == PATHS[PATH_OF[slug]]["top"]:
        return hub_page(slug)
    crumbs = crumbs_for(slug)
    body = render_blocks(slug, p["blocks"])
    if slug == "recording-studio-equipment":
        intro, racks = body.split('<div class="racks"', 1)
        return page_hero(p, crumbs) + f'<div class="wrap gear-intro prose">{intro}</div><div class="wrap"><div class="racks"{racks}</div>' + path_cta("rec", slug)
    if slug in ("privacy", "blog"):
        return page_hero(p, "") + f'<div class="wrap narrow prose">{body}</div>'
    if slug in PATH_OF:
        return page_hero(p, crumbs) + f'<div class="wrap split"><article class="prose">{body}</article>{aside(slug)}</div>' + path_cta(PATH_OF[slug], slug)
    return page_hero(p, crumbs) + f'<div class="wrap split"><article class="prose">{body}</article>{aside(slug)}</div>' + cta_band()

def aside(slug):
    k = PATH_OF.get(slug)
    if not k:
        lst, head, btn = SERVICES, "שירותים", ("/contact", "שלחו הודעה")
    else:
        lst, head, btn = PATHS[k]["pages"], "מסלול " + PATHS[k]["label"], ("#book", PATHS[k]["cta"])
    lis = "".join(f'<li><a href="{link(s)}"{" aria-current=\"page\"" if s == slug else ""}>{PAGES[s]["title"]}</a></li>' for s in lst)
    return f'''<aside class="side">
  <nav class="side-nav" aria-label="{head}"><p class="eyebrow">{head}</p><ul>{lis}</ul></nav>
  <div class="side-card"><p class="eyebrow">דברו איתנו</p><a class="big-phone" href="tel:036481791" dir="ltr">{PHONE}</a><a class="btn btn-accent" href="{btn[0]}">{btn[1]}</a></div>
</aside>'''

def home():
    doors = "".join(f'''<a class="door" href="{link(PATHS[k]["top"])}" style="--img:url('/img/{PATHS[k]["photo"]}-m.jpg')"><span class="door-q">{PATHS[k]["door"]}</span><span class="door-sub">{PATHS[k]["door_sub"]}</span><span class="door-go">למסלול {PATHS[k]["label"]} <span aria-hidden="true">←</span></span></a>''' for k in PATH_ORDER)
    strip = "".join(f'<img src="/img/{p}-m.jpg" alt="" loading="lazy">' for p in ["ig-018", "fb-063", "ig-029", "fb-075", "ig-004", "fb-066"])
    def teaser(k, inner, alt=""):
        P = PATHS[k]
        return f'''<section class="block{alt} teaser" id="path-{k}"><div class="wrap">
  <div class="sh"><div><p class="eyebrow">{P["label"]}</p><h2 class="sec-h">{P["door"]}?</h2></div><p>{P["tagline"]}</p></div>
  {inner}
  <p class="center"><a class="btn btn-accent" href="{link(P["top"])}">למסלול {P["label"]} <span aria-hidden="true">←</span></a></p>
</div></section>'''
    return f'''<header class="hero home-hero" style="--img:url('/img/brick.jpg')">
  <div class="wrap hero-inner">
    <p class="eyebrow">מאז 2004 · צפון תל אביב</p>
    <h1>אולפן הקלטות ופודקאסטים</h1>
    <p class="hero-sub">מה מביא אתכם לתמוז?</p>
    <div class="doors">{doors}</div>
    <div class="stats"><div><b class="num">2004</b><span>שנת ההקמה</span></div><div><b class="num">+{(len(PODCASTS) // 5) * 5}</b><span>פודקאסטים הוקלטו כאן</span></div><div><b class="num">4.8</b><span>בגוגל, 54 ביקורות</span></div></div>
  </div>
</header>
{teaser("rec", _rooms() + f'<div class="covers covers-short">{_covers(COVERS[:6])}</div>')}
{teaser("pod", _sets() + f'<div class="pod-grid pod-short">{_pods(12)}</div>', " alt")}
{teaser("prod", f'<div class="quotes">{_quotes(QUOTES[2:])}</div>')}
<div class="strip" aria-hidden="true">{strip}</div>
<section class="block alt"><div class="wrap">
  <div class="sh"><div><p class="eyebrow">אומרים עלינו</p><h2 class="sec-h">4.8 בגוגל</h2></div></div>
  <div class="quotes">{_quotes(QUOTES[:2])}</div>
</div></section>
<section class="block"><div class="wrap about">
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

build.nav, build.page_hero, build.aside, build.cta_band, build.inner_page = nav, page_hero, aside, cta_band, inner_page
build.home, build.contact, build.services, build.footer = home, contact, services, footer
