# Tamuz Studios website

אתר תמוז אולפן הקלטות (tamuzstudios.co.il), אתר סטטי שמחליף את Wix עם אותן כתובות בדיוק.

## מבנה

- `site/` האתר עצמו, מוכן להעלאה ל-Cloudflare Pages (תיקיית פלט: `site`, בלי פקודת build).
- `src/` הקוד שמייצר את האתר: התוכן של כל עמוד (`content_*.py`), העיצוב (`template_prod.html`, `extra.css`) ותגיות ה-SEO (`seo.json`).

## עדכון האתר

```
cd src
python3 prod.py ../site
mv ../site-urls.txt .
python3 serve.py ../site &   # שרת מקומי בכתובת 127.0.0.1:8765
python3 check.py              # בודק שכל הכתובות הישנות עונות תקין
```

`WEB3FORMS_KEY` (משתנה סביבה) מחבר את טופס יצירת הקשר לדוא״ל של האולפן.
