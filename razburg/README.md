# razburg.com (draft)

Static rebuild of razburg.com that keeps the four Wix URLs: `/`, `/studio`, `/about`, `/contact`.

- `src/build.py` generates the site. `python3 src/build.py dist` builds for production;
  `--base /razburg-preview` builds the temporary preview served under the Tamuz preview Worker.
- `src/discography.json` is the album gallery (artist, title, link, Wix media id). Add albums here.
  `hidden: true` keeps an entry out of the page.
- `src/gear.json` is the studio equipment list.
- Contact email comes from the `RB_EMAIL` environment variable, the form key from `WEB3FORMS_KEY`.
- Images are still served from the Wix CDN (`wix()` in build.py) and must be self-hosted before Wix is cancelled.

## Layout as its own repository (razburg-site)
- `src/` generator and data, `site/` the built output that Cloudflare serves (committed, no build step on Cloudflare).
- `./build.sh` rebuilds `site/`. `tools/fetch_images.py` downloads all images from Wix into `src/img/` once; after that the build uses the local copies.
- `wrangler.jsonc` defines the Worker `razburg-site`.
