# jenniferbrown.xyz

A modernized, fully responsive static rebuild of the old *jenniferbernstone.com* site
for Jennifer Brown — performer, voice/piano/acting teacher, and fitness coach in Rome, NY.

All original page content was preserved and reorganized; the last name was updated
throughout from **Bernstone → Brown**, and the look & functionality were rebuilt to
work cleanly on desktop and mobile.

## What changed from the original
- **Name & contact** updated to Jennifer Brown / `jennifer@jenniferbrown.xyz`.
- **Modern responsive design** — mobile-first CSS, sticky header with an animated
  hamburger drawer + accordion submenus, a split hero with an image carousel,
  pricing/rate cards, a performance timeline, a filterable resume, a photo gallery
  with a keyboard-accessible lightbox, and a contact form.
- **No framework / no build tooling required to view** — plain HTML, one CSS file,
  one JS file. Works by opening the files directly or via any static host.
- Replaced the old jQuery plugins (Superfish, Nivo slider, Fancybox) with ~5 KB of
  vanilla JS.
- Progressive enhancement: all content is visible without JavaScript; JS only adds
  the menu, carousel, lightbox, and scroll animations.

## Project layout
```
index.html, bio.html, performances.html, resume.html, photos.html, media.html,
lessons-singing.html, lessons-piano.html, lessons-acting.html,
lessons-workshops.html, personal-training.html, zumba.html,
fitness-classes.html, contact.html      ← generated pages
assets/css/styles.css                    ← design system
assets/js/main.js                        ← nav, carousel, lightbox, reveal, form
assets/img/                              ← home / headshots / portfolio images
build.py                                 ← generates every page from one template
.claude/launch.json                      ← local preview server config
```

## Editing & rebuilding
The 14 pages share one HTML template, so **edit `build.py`, not the `.html` files**
(they are overwritten on each build). Then:

```bash
python3 build.py        # regenerates all *.html
```

## Preview locally
```bash
python3 -m http.server 8099
# open http://localhost:8099
```

## Notes / things to confirm
- **Contact details** (phone `646-526-8312`, Rome NY studio, Facebook link) were
  carried over from the original site — verify they are still current.
- The email defaults to `jennifer@jenniferbrown.xyz`; update in `build.py` (`EMAIL`)
  and `assets/js/main.js` if a different address is preferred.
- The contact form has no backend — it opens the visitor's mail client (`mailto:`).
  Swap in a form service (Formspree, Netlify Forms, etc.) if server-side handling is
  wanted.
- Dated material (class session schedules, performance list ending 2012) was kept as
  historical content; the class pages point visitors to "contact for the current
  schedule."
- One source headshot (`orange_shirt_copy.jpg`) was corrupt at the origin and omitted.
