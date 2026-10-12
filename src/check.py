import json, re, urllib.request, urllib.parse, html
seo = json.load(open("seo.json", encoding="utf-8"))
urls = [l.strip() for l in open("site-urls.txt", encoding="utf-8") if l.strip()]
B = "http://127.0.0.1:8765"
seen, bad, links = set(), [], set()
def get(u):
    try:
        r = urllib.request.urlopen(B + urllib.parse.quote(u)); return r.status, r.read().decode()
    except urllib.error.HTTPError as e: return e.code, ""
for u in urls:
    st, h = get(u)
    slug = u.strip("/")
    t = html.unescape(re.search(r"<title>(.*?)</title>", h).group(1))
    h1 = len(re.findall(r"<h1[ >]", h))
    can = re.search(r'rel="canonical" href="([^"]+)"', h).group(1)
    d = re.search(r'name="description" content="([^"]*)"', h)
    ok = st == 200 and h1 == 1 and d and d.group(1) and urllib.parse.unquote(can) == "https://www.tamuzstudios.co.il" + (u if u != "/" else "")
    if slug in seo["titles"] and t != seo["titles"][slug]: ok = False
    if "noindex" in h or "טיוטת" in h: ok = False
    for m in re.findall(r'href="(/[^"]*)"', h): links.add(m)
    for m in re.findall(r'href="#([^"]*)"', h):
        if m != "main": bad.append((u, "#" + m))
    for m in re.findall(r'<img [^>]*>', h):
        if 'alt="' not in m: bad.append((u, "img without alt"))
    if not ok: bad.append((u, st, h1, t, can, bool(d)))
    print(st, h1, u, "|", t)
for l in sorted(links):
    st, _ = get(urllib.parse.unquote(l))
    if st != 200: bad.append(("link", l, st))
print("internal links checked:", len(links))
for x in ["/nope", "/blog/hashtags/x"]: print(x, get(x)[0])
print("PROBLEMS:", bad or "none")
