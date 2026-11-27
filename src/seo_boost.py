"""Organic-SEO layer (2026-11-27 keyword research): stronger H1s, podcast-page sections + FAQ,
and per-page structured data. Imported by prod.py after theme, so it only adds to the page content.

Keyword targets (Google autocomplete IL, Nov 2026): אולפן פודקאסט תל אביב / במרכז, הקלטת פודקאסט (מחיר),
צילום פודקאסט, הקלטת פודקאסט משפחתי / מתנה, אולפן הקלטות (תל אביב), הקלטת שיר באולפן.
The homepage title stays exactly as it was: it ranks #1 for "אולפן הקלטות" and "אולפן הקלטות תל אביב".
"""
import html, re
import build, theme
from build import PAGES

SITE = "https://www.tamuzstudios.co.il"

# ---- H1 per page (nav labels stay short; only the page heading carries the full phrase)
H1 = {
    "podcast-recording": "הקלטת פודקאסט וצילום פודקאסט בתל אביב",
    "songs-recordings": "הקלטת שירים באולפן",
    "mixing-audio-edits": "מיקס ועריכות סאונד",
    "music-production": "הפקה מוזיקלית",
}
for _s, _h in H1.items():
    PAGES[_s]["h1"] = _h

_orig_hero = theme.page_hero
def page_hero(p, crumbs, slug=None, lead=None):
    out = _orig_hero(p, crumbs, slug, lead)
    if p.get("h1"):
        out = out.replace(f"<h1>{p['title']}</h1>", f"<h1>{p['h1']}</h1>", 1)
    return out
theme.page_hero = build.page_hero = page_hero

# ---- FAQ block: ("faq", [(question, answer), ...]) rendered as visible Q&A + FAQPage schema
FAQ = {}
_orig_render = build.render_blocks
def render_blocks(slug, blocks):
    out, plain = [], []
    for b in blocks:
        if b[0] == "faq":
            if plain: out.append(_orig_render(slug, plain)); plain = []
            items = "".join(f'<details class="faq-i"><summary><h3>{build.inline(q)}</h3></summary><p>{build.inline(a)}</p></details>' for q, a in b[1])
            out.append(f'<div class="faq">{items}</div>')
            FAQ[slug] = b[1]
        elif b[0] == "steps":
            if plain: out.append(_orig_render(slug, plain)); plain = []
            out.append('<ol class="steps">' + "".join(f"<li><b>{build.inline(t)}</b> {build.inline(d)}</li>" for t, d in b[1]) + "</ol>")
        else:
            plain.append(b)
    if plain: out.append(_orig_render(slug, plain))
    return "\n".join(out)
build.render_blocks = theme.render_blocks = render_blocks

# ---- Podcast page: keyword-led opening, video / family-podcast / how-it-works sections, FAQ
pod = PAGES["podcast-recording"]["blocks"]
pod[0] = ("p", "תמוז הוא אולפן פודקאסט מקצועי בצפון תל אביב: הקלטת פודקאסט, צילום פודקאסט בשלוש מצלמות, עריכת סאונד ווידאו ועיצוב סאונד, הכל במקום אחד ועם טכנאי מוסמך לאורך כל הסשן. מעבר לעבודה באולפן אנחנו מקימים גם [[אולפן הקלטות נייד|mobile-recording-studio]] להקלטת פודקאסט במשרדי החברה, בבית העסק או באירוע.")
_i = next(i for i, b in enumerate(pod) if b[0] == "p" and b[1].startswith("בנוסף אנו מספקים שירות צילום"))
pod.insert(_i, ("h", "צילום פודקאסט: פרק מצולם מוכן ליוטיוב ולרשתות"))
_i = next(i for i, b in enumerate(pod) if b[0] == "p" and b[1].startswith("עלות הקלטת פודקאסט"))
pod[_i:_i] = [
    ("h", "פודקאסט משפחתי, פודקאסט אישי ופודקאסט במתנה"),
    ("p", "לא כל פודקאסט נועד לספוטיפיי. אצלנו מוקלטים גם פודקאסטים משפחתיים ואישיים: שיחה עם סבא וסבתא, סיפור חיים של בן משפחה, או מסר מרגש לקראת אירוע. כל משתתף מקבל מיקרופון משלו, הצוות דואג שהשיחה תזרום ושהצד הטכני יישאר מאחורי הקלעים, ובסוף נשארת הקלטה באיכות אולפן שאפשר לשמור לדורות. זה גם רעיון למתנה מקורית ליום הולדת עגול, לבר או בת מצווה או ליום נישואין."),
    ("h", "איך מקליטים פודקאסט אצלנו"),
    ("steps", [
        ("שיחת תיאום.", "מספרים לנו על הפודקאסט, כמה משתתפים יהיו ואם צריך גם צילום וידאו."),
        ("יום ההקלטה.", "מגיעים לאולפן, הטכנאי מתאים מיקרופון לכל משתתף, ומתחילים להקליט. אין צורך בניסיון או בציוד."),
        ("עריכה.", "עריכת סאונד, ניקוי ואיזון של הקולות, ולפי הצורך עריכת וידאו וקטעים קצרים לרשתות."),
        ("מסירה.", "מקבלים קבצים מוכנים להעלאה לספוטיפיי, לאפל פודקאסטס וליוטיוב."),
    ]),
    ("h", "כמה עולה הקלטת פודקאסט?"),
]
_last = next(i for i, b in enumerate(pod) if b[0] == "p" and b[1].startswith("לפרטים נוספים בנוגע להקלטת"))
pod[_last:_last] = [
    ("h", "שאלות נפוצות על הקלטת פודקאסט"),
    ("faq", [
        ("כמה עולה הקלטת פודקאסט באולפן?", "המחיר תלוי בזמן האולפן, בצילום (אודיו בלבד או שלוש מצלמות) ובהיקף העריכה. ספרו לנו מה אתם צריכים ונחזור אליכם עם הצעת מחיר מדויקת."),
        ("כמה משתתפים אפשר להקליט יחד?", "חדר ההקלטה מרווח ומאפשר הקלטה של כמה משתתפים בו זמנית, כל אחד עם מיקרופון משלו. לפאנל גדול נתאים את הסט מראש."),
        ("צריך להביא ציוד או ניסיון קודם?", "לא. כל הציוד נמצא באולפן, והטכנאי מטפל בכל הצד הטכני. מספיק להגיע עם התוכן."),
        ("אפשר גם לצלם את הפודקאסט?", "כן. צילום הפודקאסט נעשה בשלוש מצלמות מקצועיות עם תאורת אולפן וניתוב וידאו בזמן אמת, כך שמקבלים פרק מצולם מלא עם סאונד אולפני, וגם חומר לקטעים קצרים לרשתות."),
        ("איפה האולפן ויש חניה?", "האולפן נמצא ברחוב אריה דיסנצ׳יק 9 בצפון תל אביב, דקות נסיעה מרמת השרון, הרצליה ורמת גן. יש חניה בשפע, מעלית ונגישות מלאה."),
        ("אפשר להקליט פודקאסט מחוץ לאולפן?", "כן. אנחנו מקימים [[אולפן הקלטות נייד|mobile-recording-studio]] במשרד, בבית העסק או באירוע."),
        ("אפשר לשדר מהאולפן בשידור חי?", "כן. יש לנו גם [[אולפן שידור|livestreaming]] לשידורים חיים בזום מתוך האולפן, עם שלוש מצלמות, תאורה וסאונד אולפני."),
    ]),
]
# small typo fixes in the original Wix text
PAGES["podcast-recording"]["blocks"] = [(k, v.replace("שרות הקלטת", "שירות הקלטת").replace("בשרותים שלנו", "בשירותים שלנו") if isinstance(v, str) else v) for k, v in pod]

# ---- Recording-studio page: location + FAQ (local intent: אולפן הקלטות בתל אביב / במרכז)
rec = PAGES["recording-studio-tel-aviv"]["blocks"]
rec += [
    ("h", "אולפן הקלטות בצפון תל אביב"),
    ("p", "האולפן נמצא ברחוב אריה דיסנצ׳יק 9 בצפון תל אביב, עם חניה בשפע, מעלית ונגישות מלאה, ונוח להגיע אליו מכל אזור המרכז: רמת השרון, הרצליה, רמת גן, גבעתיים ופתח תקווה. כאן מקליטים שירים, להקות ותופים, [[מפיקים מוזיקה|music-production]], [[מקליטים ומצלמים פודקאסטים|podcast-recording]] ועושים [[מיקס|mixing-audio-edits]] ופוסט פרודקשן."),
    ("h", "שאלות נפוצות"),
    ("faq", [
        ("אפשר להגיע עם טכנאי או מפיק משלי?", "כן. טכנאים ומפיקים מוזמנים לעבוד אצלנו, בליווי עוזר טכנאי של האולפן שמכיר את החדרים והציוד. האולפן לא מושכר ללא טכנאי."),
        ("כמה עולה שעת אולפן?", "סשנים מתומחרים לפי זמן האולפן שהוזמן ולפי סוג העבודה. השאירו פרטים ונחזור אליכם עם הצעת מחיר."),
        ("מה אפשר להקליט באולפן?", "שירה, להקות בהקלטת לייב, תופים, כלי קשת ונשיפה, קריינות ופודקאסטים. חדר ההקלטה תוכנן על ידי אקוסטיקאים, וחדר הבקרה משלב ציוד אנלוגי ודיגיטלי."),
    ]),
]

# ---- Structured data for every page
BUSINESS_EXTRA = {
    "geo": {"@type": "GeoCoordinates", "latitude": 32.1174305, "longitude": 34.8268416},
    "hasMap": "https://maps.google.com/?cid=11110570161742506020",
    "areaServed": ["תל אביב-יפו", "רמת השרון", "הרצליה", "רמת גן", "גבעתיים", "פתח תקווה", "ישראל"],
    "knowsAbout": ["הקלטת שירים", "הקלטת פודקאסט", "צילום פודקאסט", "הפקה מוזיקלית", "מיקס", "עיצוב סאונד", "פוסט פרודקשן"],
    "founder": {"@type": "Person", "name": "רז בורג", "url": "https://www.razburg.com"},
    # Hours from the studio's Calendly booking page (bookable slots Sun-Thu, 09:00-22:00)
    "openingHoursSpecification": [{"@type": "OpeningHoursSpecification",
        "dayOfWeek": ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday"], "opens": "09:00", "closes": "22:00"}],
}

HOURS = "א׳–ה׳ 09:00–22:00"
_orig_lines = build.contact_lines
def contact_lines(cls="contact-lines"):
    return _orig_lines(cls).replace("</ul>", f'  <li><span class="lbl">שעות</span><span>{HOURS}</span></li>\n</ul>', 1)
build.contact_lines = theme.contact_lines = contact_lines

SERVICE_TYPE = {
    "podcast-recording": "הקלטת פודקאסט וצילום פודקאסט",
    "recording-studio-tel-aviv": "אולפן הקלטות",
    "songs-recordings": "הקלטת שירים",
    "mixing-audio-edits": "מיקס ועריכת סאונד",
    "post-production-sound-design": "פוסט פרודקשן ועיצוב סאונד",
    "mobile-recording-studio": "אולפן הקלטות נייד",
    "music-production": "הפקה מוזיקלית",
    "music-production-singer-songwriter": "הפקה מוזיקלית לזמרים",
    "music-production-bands": "הפקה מוזיקלית ללהקות",
    "music-production-commercials": "מוזיקה לפרסומות",
    "original-music-movies-commercials": "מוזיקה מקורית לסרטים ופרסומות",
    "playbacks": "הפקת פלייבקים",
    "livestreaming": "אולפן שידור",
}

def strip(t):
    return re.sub(r"\[\[(.+?)\|.+?\]\]", r"\1", t)

def page_schema(slug, title, desc):
    """Extra JSON-LD objects for an inner page: breadcrumb, service, FAQ."""
    out = []
    if slug in ("", "404"):
        return out
    trail = [("ראשי", SITE + "/")]
    if slug in theme.SECTION_OF and theme.SECTION_OF[slug][0] != slug:
        top = theme.SECTION_OF[slug][0]
        trail.append((PAGES[top]["title"], f"{SITE}/{top}"))
    trail.append((PAGES[slug].get("h1") or PAGES[slug]["title"], f"{SITE}/{slug}"))
    out.append({"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": i + 1, "name": n, "item": u} for i, (n, u) in enumerate(trail)]})
    if slug in SERVICE_TYPE:
        out.append({"@context": "https://schema.org", "@type": "Service", "name": PAGES[slug].get("h1") or PAGES[slug]["title"],
                    "serviceType": SERVICE_TYPE[slug], "description": desc, "url": f"{SITE}/{slug}",
                    "provider": {"@id": SITE + "/#studio"}, "areaServed": {"@type": "City", "name": "תל אביב-יפו"}})
    if slug in FAQ:
        out.append({"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
            {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": strip(a)}} for q, a in FAQ[slug]]})
    return out
