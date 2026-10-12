"""Production build: one static HTML file per existing tamuzstudios.co.il URL.

Usage: python3 prod.py <outdir>
Cloudflare Pages serves /slug from slug.html, so every Wix URL keeps its exact path.
"""
import html, json, os, re, sys, shutil
from datetime import datetime
from urllib.parse import quote
import build
from build import PAGES, PHONE, EMAIL, SOCIAL, media

SITE = "https://www.tamuzstudios.co.il"
GSV = "EXoOyeKinw5BlF2SdU-F8Uy3_yW1Qa8wmjCi9j_l2Go"
WEB3FORMS_KEY = os.environ.get("WEB3FORMS_KEY", "")  # filled in once Raz creates the key
SEO = json.load(open("seo.json", encoding="utf-8"))
POSTS_RAW = json.load(open("posts.json", encoding="utf-8"))["posts"]
MONTHS = ["ינואר", "פברואר", "מרץ", "אפריל", "מאי", "יוני", "יולי", "אוגוסט", "ספטמבר", "אוקטובר", "נובמבר", "דצמבר"]

build.link = lambda slug: "/" + (slug or "")

def url(path):
    return SITE + ("/" + quote(path) if path else "")

def hdate(iso):
    d = datetime.fromisoformat(iso.replace("Z", "+00:00"))
    return f"{d.day} ב{MONTHS[d.month - 1]} {d.year}"

# Real dates on the blog list (the draft had one missing)
by_slug = {p["slug"]: p for p in POSTS_RAW}
build.POSTS[:] = [(u, t, hdate(by_slug[u[5:]]["firstPublishedDate"]), x or by_slug[u[5:]]["excerpt"]) for u, t, d, x in build.POSTS]

BUSINESS = {
    "@context": "https://schema.org", "@type": "RecordingStudio", "@id": SITE + "/#studio",
    "name": "תמוז אולפן הקלטות | Tamuz Studios", "alternateName": "Tamuz Studios",
    "url": SITE + "/", "telephone": "+972-3-6481791", "email": EMAIL, "foundingDate": "2004",
    "image": media(build.IMG_STUDIO, 1200, 630),
    "address": {"@type": "PostalAddress", "streetAddress": "דיסנצ׳יק 9", "addressLocality": "תל אביב-יפו", "postalCode": "69356", "addressCountry": "IL"},
    "sameAs": ["https://www.facebook.com/tamuzstudios/", "https://www.instagram.com/tamuzstudios/", "https://www.youtube.com/TamuzStudios", "https://vimeo.com/razburg"],
}

def ld(obj):
    return '<script type="application/ld+json">' + json.dumps(obj, ensure_ascii=False).replace("</", "<\\/") + "</script>"

def head(path, title, desc, img, og_type="website", extra=""):
    a = lambda s: html.escape(s, quote=True)
    can = url(path)
    return f'''<title>{a(title)}</title>
<meta name="description" content="{a(desc)}">
<link rel="canonical" href="{can}">
<meta name="google-site-verification" content="{GSV}">
<meta property="og:locale" content="he_IL">
<meta property="og:site_name" content="Tamuz Studios">
<meta property="og:type" content="{og_type}">
<meta property="og:title" content="{a(title)}">
<meta property="og:description" content="{a(desc)}">
<meta property="og:url" content="{can}">
<meta property="og:image" content="{a(img)}">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta name="twitter:card" content="summary_large_image">
<meta name="theme-color" content="#1b2630">
<link rel="icon" href="/favicon.svg" type="image/svg+xml">
<link rel="stylesheet" href="/site.css">
{extra}'''.rstrip()

def mark_current(nav_html, path):
    href = "/" + path
    return nav_html.replace(f'<a href="{href}">', f'<a href="{href}" aria-current="page">', 1) if path else nav_html

def clean(body):
    # Draft-only URL labels on blog cards become a read-more link
    return re.sub(r'<span class="url" dir="ltr">/([^<]+)</span>', lambda m: f'<a class="more" href="/{m.group(1)}">להמשך קריאה <span aria-hidden="true">←</span></a>', body)

def form_wire(body):
    hidden = (f'<input type="hidden" name="access_key" value="{WEB3FORMS_KEY}">'
              '<input type="hidden" name="subject" value="פנייה חדשה מאתר תמוז">'
              '<input type="hidden" name="from_name" value="אתר תמוז אולפנים">'
              '<input type="checkbox" name="botcheck" class="hp" tabindex="-1" autocomplete="off" aria-hidden="true">')
    body = body.replace('<form class="cform" data-form novalidate>', f'<form class="cform" data-form action="https://api.web3forms.com/submit" method="POST" novalidate>{hidden}')
    return body.replace('<p class="form-ok" hidden>', '<p class="form-err" hidden>ההודעה לא נשלחה. אפשר להתקשר אלינו ב-<a href="tel:036481791" dir="ltr">03-6481791</a></p><p class="form-ok" hidden>')

def page(tpl, path, head_html, body, nav_html):
    return (tpl.replace("{{HEAD}}", head_html).replace("{{NAV}}", mark_current(nav_html, path))
               .replace("{{PAGES}}", form_wire(clean(body))).replace("{{FOOTER}}", build.footer()).replace("{{PHONE}}", PHONE))

def og_img(p):
    return media(p.get("img") or build.IMG_STUDIO, 1200, 630)

# ---- blog posts
def run_html(r):
    t = html.escape(r["textData"]["text"], quote=False)
    decos = {d["type"] for d in r["textData"].get("decorations", [])}
    if "BOLD" in decos: t = f"<strong>{t}</strong>"
    for d in r["textData"].get("decorations", []):
        if d["type"] == "LINK":
            t = f'<a href="{html.escape(d["linkData"]["link"]["url"])}">{t}</a>'
    return t

def rich(nodes, title):
    out = []
    for n in nodes:
        if n["type"] == "PARAGRAPH":
            lines, cur = [], []
            for r in n["nodes"]:
                parts = r["textData"]["text"].split("\n")
                for i, part in enumerate(parts):
                    if i: lines.append(cur); cur = []
                    if part: cur.append(dict(r, textData=dict(r["textData"], text=part)))
            lines.append(cur)
            for ln in lines:
                if not ln or not "".join(r["textData"]["text"] for r in ln).strip(): continue
                if all(any(d["type"] == "BOLD" for d in r["textData"].get("decorations", [])) for r in ln if r["textData"]["text"].strip()):
                    out.append("<h2>" + html.escape("".join(r["textData"]["text"] for r in ln).strip(), quote=False) + "</h2>")
                else:
                    out.append("<p>" + "".join(run_html(r) for r in ln) + "</p>")
        elif n["type"] == "HEADING":
            lv = min(max(n["headingData"]["level"], 2), 3)
            out.append(f"<h{lv}>" + "".join(run_html(r) for r in n["nodes"]) + f"</h{lv}>")
        elif n["type"] == "IMAGE":
            im = n["imageData"]["image"]
            w, h = im.get("width", 1200), im.get("height", 800)
            if w > 1200: h, w = int(h * 1200 / w), 1200
            out.append(f'<figure class="post-fig"><img src="{media(im["src"]["id"], w, h)}" alt="{html.escape(title)}" width="{w}" height="{h}" loading="lazy"></figure>')
        else:
            raise SystemExit(f"unhandled node {n['type']}")
    return "\n".join(out)

def post_page(p):
    title = p["title"].strip()
    path = "post/" + p["slug"]
    img = p["media"]["wixMedia"]["image"]["id"]
    tags = "".join(f"<li>#{html.escape(t)}</li>" for t in p.get("hashtags", []))
    crumbs = '<span>/</span><a href="/blog">בלוג</a>'
    hero = build.page_hero(dict(title=title, img=img), crumbs)
    body = hero + f'''<div class="wrap narrow prose post-body">
<p class="meta"><time datetime="{p["firstPublishedDate"][:10]}">{hdate(p["firstPublishedDate"])}</time> · רז בורג</p>
{rich(p["richContent"]["nodes"], title)}
{f'<ul class="tags">{tags}</ul>' if tags else ""}
<p><a class="btn btn-ghost" href="/blog">לכל המאמרים</a></p>
</div>''' + build.cta_band()
    schema = {"@context": "https://schema.org", "@type": "BlogPosting", "headline": title, "datePublished": p["firstPublishedDate"],
              "dateModified": p["lastPublishedDate"], "image": media(img, 1200, 630), "mainEntityOfPage": url(path),
              "author": {"@type": "Person", "name": "רז בורג"}, "publisher": {"@id": SITE + "/#studio"}}
    h = head(path, title, p["excerpt"].strip(), media(img, 1200, 630), "article", ld(schema))
    return path, h, body

def main(outdir):
    if os.path.exists(outdir): shutil.rmtree(outdir)
    os.makedirs(os.path.join(outdir, "post"))
    tpl = open("template_prod.html", encoding="utf-8").read()
    css = re.search(r"<style>\n(.*?)</style>\n", tpl, re.S)
    tpl = tpl.replace(css.group(0), "")
    open(os.path.join(outdir, "site.css"), "w", encoding="utf-8").write(css.group(1) + open("extra.css", encoding="utf-8").read())
    shutil.copy("site.js", outdir); shutil.copy("favicon.svg", outdir)
    nav_html = build.nav()
    written = []

    def write(path, h, body):
        fn = os.path.join(outdir, (path or "index") + ".html")
        open(fn, "w", encoding="utf-8").write(page(tpl, path, h, body, nav_html))
        written.append(path)

    for slug, p in PAGES.items():
        extra = ""
        if slug == "":
            body = build.home()
            extra = ld(BUSINESS) + ld({"@context": "https://schema.org", "@type": "WebSite", "name": "Tamuz Studios", "url": SITE + "/", "inLanguage": "he"})
        elif slug == "contact":
            body = build.contact(); extra = ld(BUSINESS)
        elif slug == "services":
            body = build.services()
        else:
            body = build.inner_page(slug)
        write(slug, head(slug, SEO["titles"][slug], SEO["desc"][slug], og_img(p), extra=extra), body)
    for p in POSTS_RAW:
        write(*post_page(p))

    nf = build.page_hero(dict(title="העמוד לא נמצא", img=None), "") + '<div class="wrap narrow prose"><p>ייתכן שהכתובת השתנתה. אפשר לחזור <a href="/">לעמוד הבית</a> או <a href="/contact">ליצור קשר</a>.</p></div>'
    open(os.path.join(outdir, "404.html"), "w", encoding="utf-8").write(
        page(tpl, "404", '<title>העמוד לא נמצא | Tamuz Studios</title>\n<meta name="robots" content="noindex">\n<link rel="stylesheet" href="/site.css">\n<link rel="icon" href="/favicon.svg" type="image/svg+xml">', nf, nav_html))

    today = datetime.now().strftime("%Y-%m-%d")
    urls = "".join(f"<url><loc>{url(p)}</loc><lastmod>{today}</lastmod></url>\n" for p in written)
    open(os.path.join(outdir, "sitemap.xml"), "w", encoding="utf-8").write(
        f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n{urls}</urlset>\n')
    open(os.path.join(outdir, "robots.txt"), "w").write(f"User-agent: *\nAllow: /\n\nSitemap: {SITE}/sitemap.xml\n")
    # Old Wix sub-sitemaps and blog listing variants, so nothing Google already knows ends in a 404
    open(os.path.join(outdir, "_redirects"), "w", encoding="utf-8").write(
        "/pages-sitemap.xml /sitemap.xml 301\n/blog-posts-sitemap.xml /sitemap.xml 301\n/blog-categories-sitemap.xml /sitemap.xml 301\n"
        "/blog-hashtags-sitemap.xml /sitemap.xml 301\n/blog/* /blog 301\n/home /  301\n/index.html / 301\n")
    open(os.path.join(outdir, "_headers"), "w").write(
        "/*\n  X-Content-Type-Options: nosniff\n  Referrer-Policy: strict-origin-when-cross-origin\n\n/site.css\n  Cache-Control: public, max-age=86400\n/site.js\n  Cache-Control: public, max-age=86400\n")
    open(outdir.rstrip("/") + "-urls.txt", "w", encoding="utf-8").write("\n".join("/" + p for p in written) + "\n")
    print("pages:", len(written))

if __name__ == "__main__":
    main(sys.argv[1])
