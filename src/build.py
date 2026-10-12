import html, re, sys
from content_d import *

def media(fid, w=1600, h=None, q=80):
    if not fid: return ""
    size = f"w_{w},h_{h}" if h else f"w_{w},h_{int(w*0.62)}"
    return f"https://static.wixstatic.com/media/{fid}/v1/fill/{size},al_c,q_{q},enc_auto/{fid}"

ADDRESS = "דיסנצ׳יק 9, תל אביב 69356"
PHONE = "03-6481791"
EMAIL = "tamuzstudios@gmail.com"
MAPS = "https://www.google.com/maps/search/?api=1&query=%D7%AA%D7%9E%D7%95%D7%96+%D7%90%D7%95%D7%9C%D7%A4%D7%9F+%D7%94%D7%A7%D7%9C%D7%98%D7%95%D7%AA+%D7%93%D7%99%D7%A1%D7%A0%D7%A6%D7%A3%D7%99%D7%A7+9"
SOCIAL = [("Facebook","https://www.facebook.com/tamuzstudios/"),("Instagram","https://www.instagram.com/tamuzstudios/"),("YouTube","https://www.youtube.com/playlist?list=PL52C78DA7C5339843"),("Vimeo","https://vimeo.com/razburg")]

SERVICES = ["podcast-recording","songs-recordings","recording-studio-tel-aviv","mixing-audio-edits","post-production-sound-design","live-recording","mobile-recording-studio","sound-protools-lessons","original-music-movies-commercials","playbacks","livestreaming"]
PRODUCTION = ["music-production-singer-songwriter","music-production-bands","music-production-commercials"]

# Home and contact pages
PAGES[""] = dict(title="אולפן הקלטות", img=IMG_HOME, group="top", blocks=[])
PAGES["contact"] = dict(title="צור קשר", img=IMG_CONTACT, group="top", blocks=[])
PAGES["services"] = dict(title="מחירון עבודות אולפן", img="2e12dd24497c4cbe8de2f9d7376f7ce1.jpg", group="top", blocks=[])

def link(slug):
    return "#" + (slug or "home")

def inline(t):
    t = html.escape(t, quote=False).replace("&lt;b&gt;","<b>").replace("&lt;/b&gt;","</b>")
    return re.sub(r"\[\[(.+?)\|(.+?)\]\]", lambda m: f'<a href="{link(m.group(2))}">{m.group(1)}</a>', t)

def contact_lines(cls="contact-lines"):
    return f'''<ul class="{cls}">
  <li><span class="lbl">כתובת</span><a href="{MAPS}" target="_blank" rel="noopener">{ADDRESS}</a></li>
  <li><span class="lbl">טלפון</span><a href="tel:036481791" dir="ltr">{PHONE}</a></li>
  <li><span class="lbl">דוא״ל</span><a href="mailto:{EMAIL}" dir="ltr">{EMAIL}</a></li>
</ul>'''

def form(fid):
    return f'''<form class="cform" data-form novalidate>
  <div class="row2">
    <label for="{fid}-fn">שם פרטי<input id="{fid}-fn" name="fn" autocomplete="given-name" required></label>
    <label for="{fid}-ln">שם משפחה<input id="{fid}-ln" name="ln" autocomplete="family-name"></label>
  </div>
  <div class="row2">
    <label for="{fid}-em">דוא״ל<input id="{fid}-em" name="em" type="email" dir="ltr" autocomplete="email" required></label>
    <label for="{fid}-ph">טלפון<input id="{fid}-ph" name="ph" type="tel" dir="ltr" autocomplete="tel"></label>
  </div>
  <label for="{fid}-msg">הודעה<textarea id="{fid}-msg" name="msg" rows="4"></textarea></label>
  <button class="btn btn-accent" type="submit">שלח הודעה</button>
  <p class="form-ok" hidden>תודה שפנית, ניצור קשר בהקדם</p>
</form>'''

def card(slug):
    p = PAGES[slug]
    return f'<a class="svc" href="{link(slug)}"><span class="svc-t">{p["title"]}</span><span class="svc-arrow" aria-hidden="true">←</span></a>'

def render_blocks(slug, blocks):
    out = []
    for b in blocks:
        k = b[0]
        if k == "p": out.append(f"<p>{inline(b[1])}</p>")
        elif k == "h": out.append(f"<h2>{inline(b[1])}</h2>")
        elif k == "q": out.append(f'<p class="pull">{inline(b[1])}</p>')
        elif k == "meta": out.append(f'<p class="meta">{inline(b[1])}</p>')
        elif k == "list": out.append("<ul class=\"qs\">" + "".join(f"<li>{inline(x)}</li>" for x in b[1]) + "</ul>")
        elif k == "sub": out.append('<div class="svc-grid">' + "".join(card(s) for s in b[1]) + "</div>")
        elif k == "price":
            rows = "".join(f'<div class="price-row"><span>{a}</span><span class="num">{v}</span></div>' for a, v in b[1])
            out.append(f'<div class="price">{rows}<p class="price-note">{inline(b[2])}</p></div>')
        elif k == "podcasts":
            imgs = "".join(f'<figure class="pod"><img loading="lazy" src="{media(f,320,320)}" alt="{html.escape(t)}" width="160" height="160"><figcaption>{html.escape(t)}</figcaption></figure>' for t, f in PODCASTS)
            out.append(f'<section class="pods" aria-label="פודקאסטים שהוקלטו באולפן"><p class="eyebrow">הוקלטו אצלנו</p><div class="pod-grid">{imgs}</div></section>')
        elif k == "gear":
            cols = []
            for name, items, rent in GEAR:
                lis = "".join(f"<li>{html.escape(i)}</li>" for i in items)
                r = ""
                if rent:
                    r = f'<p class="rent">{RENT}</p><ul>' + "".join(f"<li>{html.escape(i)}</li>" for i in rent) + "</ul>"
                cols.append(f'<section class="rack"><h2 class="rack-h" dir="ltr">{name}</h2><ul>{lis}</ul>{r}</section>')
            out.append(f'<div class="racks" dir="ltr">{"".join(cols)}</div>')
        elif k == "posts":
            items = "".join(f'<article class="post"><p class="meta">{d}</p><h2><a href="{link(u)}">{html.escape(t)}</a></h2>{f"<p>{html.escape(x)}</p>" if x else ""}<span class="url" dir="ltr">/{html.escape(u)}</span></article>' for u, t, d, x in POSTS)
            out.append(f'<div class="posts">{items}</div>')
    return "\n".join(out)

def aside(slug):
    group = PAGES[slug]["group"]
    lst = PRODUCTION if group == "production" else SERVICES
    head = "הפקה מוזיקלית" if group == "production" else "שירותים נוספים"
    lis = "".join(f'<li><a href="{link(s)}"{" aria-current=\"page\"" if s==slug else ""}>{PAGES[s]["title"]}</a></li>' for s in lst)
    return f'''<aside class="side">
  <nav class="side-nav" aria-label="{head}"><p class="eyebrow">{head}</p><ul>{lis}</ul></nav>
  <div class="side-card"><p class="eyebrow">דברו איתנו</p><a class="big-phone" href="tel:036481791" dir="ltr">{PHONE}</a><a class="btn btn-ghost" href="{link('contact')}">שלחו הודעה</a></div>
</aside>'''

def page_hero(p, crumbs):
    bg = f' style="--img:url(\'{media(p["img"],1920,700)}\')"' if p.get("img") else ""
    return f'''<header class="phero{" has-img" if p.get("img") else ""}"{bg}>
  <div class="wrap"><nav class="crumbs" aria-label="מיקום בעמוד"><a href="{link('')}">תמוז</a>{crumbs}</nav><h1>{p["title"]}</h1></div>
</header>'''

def inner_page(slug):
    p = PAGES[slug]
    crumbs = ""
    if p["group"] == "production" and slug != "music-production":
        crumbs = f'<span>/</span><a href="{link("music-production")}">הפקה מוזיקלית</a>'
    elif p["group"] == "services":
        crumbs = '<span>/</span><span>שירותים</span>'
    body = render_blocks(slug, p["blocks"])
    if slug == "recording-studio-equipment":
        return page_hero(p, crumbs) + f'<div class="wrap gear-intro prose">{body.split("<div class=\"racks\"")[0]}</div><div class="wrap">{"<div class=\"racks\"" + body.split("<div class=\"racks\"")[1]}</div>' + cta_band()
    if p["group"] in ("legal", "top") and slug in ("privacy", "blog"):
        return page_hero(p, "") + f'<div class="wrap narrow prose">{body}</div>'
    return page_hero(p, crumbs) + f'<div class="wrap split"><article class="prose">{body}</article>{aside(slug)}</div>' + cta_band()

def cta_band():
    return f'''<section class="cta-band"><div class="wrap cta-inner">
  <div><p class="eyebrow">צרו קשר</p><p class="cta-h">דברו איתנו</p></div>
  <div class="cta-actions"><a class="btn btn-accent" href="tel:036481791" dir="ltr">{PHONE}</a><a class="btn btn-ghost-inv" href="{link('contact')}">שלחו הודעה</a></div>
</div></section>'''

def home():
    h = PAGES[""]
    cards = [
        ("recording-studio-tel-aviv","אולפן הקלטות בתל אביב","אולפן הקלטות מקצועי בתל אביב המציע שרותי הקלטה מכל הסוגים בסביבה מקצועית ונעימה",IMG_STUDIO),
        ("music-production","הפקה מוסיקלית לאמנים","הפקה מוסיקלית לזמרים ויוצרים בשילוב נגני אולפן מקצועיים החל משלב הסקיצה ועד לתוצר הסופי",IMG_PROD),
        ("mixing-audio-edits","מיקס ועריכות סאונד","עריכות סאונד ומיקס מקצועי על מערכת פרוטולס בשילוב ציוד דיגיטלי ואנלוגי",IMG_GEAR),
        ("post-production-sound-design","פוסט פרודקשן ועיצוב סאונד","פוסט פרודקשן ועיצוב סאונד לוידאו. מיקס סאונד ומוסיקה לסרטים ופרסומות",IMG_BLOG),
    ]
    feat = "".join(f'''<a class="feat" href="{link(s)}"><span class="feat-img" style="--img:url('{media(i,900,600)}')"></span><span class="feat-body"><span class="feat-t">{t}</span><span class="feat-d">{d}</span><span class="more">לפרטים נוספים <span aria-hidden="true">←</span></span></span></a>''' for s, t, d, i in cards)
    more = "".join(card(s) for s in ["podcast-recording","songs-recordings","live-recording","mobile-recording-studio","livestreaming","playbacks","original-music-movies-commercials","sound-protools-lessons"])
    return f'''<header class="hero" style="--img:url('{media(IMG_HOME,1920,1100)}')">
  <div class="wrap hero-inner">
    <p class="eyebrow on-dark">תמוז · אולפן הקלטות ושירותי סאונד · תל אביב</p>
    <h1>אולפן הקלטות מקצועי</h1>
    <p class="hero-sub">תמוז הינו אולפן הקלטות בתל אביב המהווה בית למוזיקאים ומפיקים ומספק שרותי הקלטה ומיקס, הפקה מוסיקלית ושרותי סאונד שונים.</p>
    <div class="hero-actions"><a class="btn btn-accent" href="{link('contact')}">דברו איתנו</a><a class="btn btn-ghost-inv" href="{link('recording-studio-tel-aviv')}">לפרטים נוספים</a></div>
  </div>
</header>
<div class="facts" aria-label="עובדות על האולפן"><div class="wrap facts-row">
  <div class="fact"><span class="fact-k">מאז</span><span class="fact-v num">2004</span></div>
  <div class="fact"><span class="fact-k">הקלטה עד</span><span class="fact-v num" dir="ltr">192kHz / 24bit</span></div>
  <div class="fact"><span class="fact-k">מערכות</span><span class="fact-v" dir="ltr">Protools · Cubase</span></div>
  <div class="fact"><span class="fact-k">נגישות</span><span class="fact-v">מעלית · חניה בשפע</span></div>
</div></div>
<section class="wrap block">
  <div class="feat-grid">{feat}</div>
</section>
<section class="about"><div class="wrap about-grid">
  <div class="about-img" style="--img:url('{media(IMG_STUDIO,1200,1400)}')" role="img" aria-label="חדר ההקלטה באולפן תמוז"></div>
  <div class="prose">
    <p class="eyebrow">על האולפן</p>
    <h2 class="sec-h">תמוז אולפן הקלטות ושרותי סאונד</h2>
    <p>בתמוז אולפן הקלטות מקצועי המחולק לחדר הקלטה אקוסטי ומרווח שתוכנן בקפידה ומאפשר ביצוע הקלטות מכל הסוגים, ולחדר בקרה מרווח המצוייד במיטב המכשור האנלוגי והדיגיטלי.</p>
    <p>מעבר לאקוסטיקה ולמכשירים - חשוב לנו להוות עבורכם יותר מ"עוד" אולפן הקלטות כחלק מהחזון שלנו אנו שמים דגש רב על יחס אישי, אוירה ביתית ונוחות מקסימאלית וכל אלו לצד אולפן הקלטות מקצועי בסטנדרטים גבוהים וללא פשרות.</p>
    <p>האולפן ממוקם בצפון תל אביב באיזור שקט, קל ונוח להגעה ועם חניה בשפע בסביבה. האולפן נגיש לנכים ובכלל ומציע מעלית וגישה נוחה, ובנוסף מטבח מאובזר ולובי מרווח לנוחות האורחים והאמנים.</p>
    <a class="btn btn-ghost" href="{link('recording-studio-equipment')}">ציוד האולפן</a>
  </div>
</div></section>
<section class="wrap block">
  <p class="eyebrow">השירותים שלנו</p>
  <div class="svc-grid">{more}</div>
</section>
<section class="contact-home"><div class="wrap contact-grid">
  <div><p class="eyebrow">צרו קשר</p><h2 class="sec-h">דברו איתנו</h2>{contact_lines()}</div>
  {form("home")}
</div></section>'''

def contact():
    p = PAGES["contact"]
    soc = "".join(f'<li><a href="{u}" target="_blank" rel="noopener">{n}</a></li>' for n, u in SOCIAL)
    return page_hero(p, "") + f'''<div class="wrap contact-grid block">
  <div><h2 class="sec-h">דברו איתנו</h2><a class="big-phone" href="tel:036481791" dir="ltr">{PHONE}</a>{contact_lines()}<p class="eyebrow" style="margin-top:2rem">חפשו אותנו</p><ul class="social">{soc}</ul></div>
  <div><h2 class="sec-h">שלח הודעה</h2>{form("contact")}</div>
</div>'''

def services():
    p = PAGES["services"]
    return page_hero(p, "") + f'''<div class="wrap contact-grid block">
  <div><h2 class="sec-h">צרו קשר</h2>{contact_lines()}</div>
  <div>{form("services")}</div>
</div>'''

NAV = [("", "אולפן הקלטות", None), ("music-production", "הפקה מוזיקלית", PRODUCTION), (None, "שירותים", SERVICES), ("recording-studio-equipment", "ציוד האולפן", None), ("blog", "בלוג", None), ("contact", "צור קשר", None)]

def nav():
    items = []
    for i, (slug, label, sub) in enumerate(NAV):
        if sub:
            top = f'<a href="{link(slug)}">{label}</a>' if slug is not None else f'<span class="nav-label">{label}</span>'
            subl = "".join(f'<li><a href="{link(s)}">{PAGES[s]["title"]}</a></li>' for s in sub)
            items.append(f'<li class="has-sub">{top}<button class="sub-toggle" type="button" aria-expanded="false" aria-controls="sub{i}" aria-label="פתיחת תפריט {label}"><span aria-hidden="true">▾</span></button><ul class="sub" id="sub{i}">{subl}</ul></li>')
        else:
            items.append(f'<li><a href="{link(slug)}">{label}</a></li>')
    return "".join(items)

def footer():
    svc = "".join(f'<li><a href="{link(s)}">{PAGES[s]["title"]}</a></li>' for s in ["recording-studio-tel-aviv","songs-recordings","podcast-recording","mixing-audio-edits","post-production-sound-design","mobile-recording-studio","music-production","original-music-movies-commercials","playbacks"])
    soc = "".join(f'<li><a href="{u}" target="_blank" rel="noopener">{n}</a></li>' for n, u in SOCIAL)
    return f'''<footer class="foot"><div class="wrap foot-grid">
  <div><p class="logo-word">תמוז</p><p class="foot-tag">אולפן הקלטות ושירותי סאונד</p>{contact_lines("contact-lines on-dark")}</div>
  <div><p class="eyebrow on-dark">השירותים שלנו</p><ul class="foot-list">{svc}</ul></div>
  <div><p class="eyebrow on-dark">חפשו אותנו</p><ul class="foot-list">{soc}</ul></div>
</div><div class="wrap foot-base"><span>© Raz Burg \\ Tamuz Studios 2026</span><a href="{link('privacy')}">מדיניות פרטיות</a></div></footer>'''

def main():
    sections = [f'<section class="page" data-page="home" aria-label="אולפן הקלטות">{home()}</section>',
                f'<section class="page" data-page="contact" hidden>{contact()}</section>',
                f'<section class="page" data-page="services" hidden>{services()}</section>']
    for slug in PAGES:
        if slug in ("", "contact", "services"): continue
        sections.append(f'<section class="page" data-page="{slug}" hidden>{inner_page(slug)}</section>')
    
    TITLES = {("home" if s=="" else s): PAGES[s]["title"] for s in PAGES}
    import json
    tpl = open("template.html", encoding="utf-8").read()
    out = (tpl.replace("{{NAV}}", nav()).replace("{{PAGES}}", "\n".join(sections)).replace("{{FOOTER}}", footer())
              .replace("{{TITLES}}", json.dumps(TITLES, ensure_ascii=False)).replace("{{PHONE}}", PHONE))
    open(sys.argv[1], "w", encoding="utf-8").write(out)
    print("pages:", len(sections), "bytes:", len(out.encode()))

if __name__ == "__main__":
    main()
