#!/usr/bin/env python3
"""
Static site generator for jenniferbrown.xyz
Renders every page from a shared template so the chrome stays DRY.
Run:  python3 build.py   (outputs *.html into the project root)
"""
import os, html

ROOT = os.path.dirname(os.path.abspath(__file__))

SITE_NAME = "Jennifer Brown"
TAGLINE = "Music &amp; Wellness Studio"
EMAIL = "JenniferBrownStudio@gmail.com"
PHONE = "646-526-8312"
LOCATION = "Rome, New York"
FACEBOOK = "https://www.facebook.com/jennifer.brown.815600"
INSTAGRAM = "https://www.instagram.com/HealthyMusicNut"
INSTAGRAM_HANDLE = "@HealthyMusicNut"

# ----------------------------------------------------------------------------
# Navigation model: (label, href, [submenu])
# ----------------------------------------------------------------------------
NAV = [
    ("Home", "index.html", None, "home"),
    ("Performing", "performances.html", [
        ("Performance Dates", "performances.html"),
        ("Resume", "resume.html"),
        ("Photos", "photos.html"),
        ("Media &amp; Press", "media.html"),
    ], "performing"),
    ("Teaching", "lessons-singing.html", [
        ("Singing", "lessons-singing.html"),
        ("Piano", "lessons-piano.html"),
        ("Acting", "lessons-acting.html"),
        ("Ballet", "lessons-ballet.html"),
        ("Workshops &amp; Group", "lessons-workshops.html"),
    ], "teaching"),
    ("Fitness", "personal-training.html", [
        ("Personal Training", "personal-training.html"),
        ("Nutrition", "nutrition.html"),
        ("Age Well &amp; Vibrantly", "age-well.html"),
    ], "fitness"),
    ("Bio", "bio.html", None, "bio"),
    ("Contact", "contact.html", None, "contact"),
]


def nav_html(active):
    items = []
    for label, href, sub, key in NAV:
        cls = []
        if key == active:
            cls.append("is-current")
        if sub:
            cls.append("has-sub")
        cls = (' class="%s"' % " ".join(cls)) if cls else ""
        if sub:
            subitems = "".join(
                '<li><a href="%s">%s</a></li>' % (h, l) for l, h in sub
            )
            items.append(
                '<li%s><a href="%s">%s</a><ul class="submenu">%s</ul></li>'
                % (cls, href, label, subitems)
            )
        else:
            items.append('<li%s><a href="%s">%s</a></li>' % (cls, href, label))
    return "\n        ".join(items)


def page(filename, title, description, body, active, hero=False):
    head_title = "%s — %s" % (title, "Jennifer Brown") if title != "Jennifer Brown" else \
        "Jennifer Brown — Music &amp; Wellness Studio"
    doc = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <script>document.documentElement.classList.add('js');</script>
  <title>{head_title}</title>
  <meta name="description" content="{html.escape(description, quote=True)}">
  <meta property="og:title" content="{head_title}">
  <meta property="og:description" content="{html.escape(description, quote=True)}">
  <meta property="og:type" content="website">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,500;0,700;1,500&family=Inter:wght@400;500;600&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="assets/css/styles.css">
</head>
<body>
  <a class="skip-link" href="#main" style="position:absolute;left:-999px;top:0">Skip to content</a>

  <header class="site-header">
    <div class="container nav">
      <div class="brand">
        <a href="index.html">
          <span class="brand__name">Jennifer Brown</span>
          <span class="brand__tag">Music &amp; Wellness Studio</span>
        </a>
      </div>
      <button class="nav-toggle" aria-label="Toggle menu" aria-controls="primary-menu" aria-expanded="false"><span></span></button>
      <ul class="menu" id="primary-menu">
        {nav_html(active)}
      </ul>
    </div>
  </header>
  <div class="nav-backdrop"></div>

  <main id="main">
{body}
  </main>

  <footer class="site-footer">
    <div class="container">
      <div class="footer-grid">
        <div class="footer-brand">
          <span class="brand__name">Jennifer Brown</span>
          <p>Voice, piano &amp; acting instruction, fitness coaching, and live performance — based in {LOCATION}.</p>
          <div class="social" style="margin-top:1rem">
            <a href="{FACEBOOK}" target="_blank" rel="noopener" aria-label="Facebook">f</a>
            <a href="{INSTAGRAM}" target="_blank" rel="noopener" aria-label="Instagram">IG</a>
            <a href="mailto:{EMAIL}" aria-label="Email">@</a>
          </div>
        </div>
        <div>
          <h4>Explore</h4>
          <ul class="footer-links">
            <li><a href="performances.html">Performing</a></li>
            <li><a href="lessons-singing.html">Teaching</a></li>
            <li><a href="personal-training.html">Fitness</a></li>
            <li><a href="bio.html">Bio</a></li>
          </ul>
        </div>
        <div>
          <h4>Get in touch</h4>
          <ul class="footer-links">
            <li><a href="tel:+16465268312">{PHONE}</a></li>
            <li><a href="mailto:{EMAIL}">{EMAIL}</a></li>
            <li>{LOCATION}</li>
            <li><a href="contact.html">Contact &amp; location →</a></li>
          </ul>
        </div>
      </div>
      <div class="footer-bottom">
        <span>&copy; <span id="year">2026</span> Jennifer Brown. All rights reserved.</span>
        <span>Music &amp; Wellness Studio · {LOCATION}</span>
      </div>
    </div>
  </footer>

  <script src="assets/js/main.js"></script>
</body>
</html>
"""
    with open(os.path.join(ROOT, filename), "w") as f:
        f.write(doc)
    print("wrote", filename)


# ----------------------------------------------------------------------------
# Reusable fragments
# ----------------------------------------------------------------------------
def page_head(eyebrow, title, intro, crumbs):
    crumb_html = " / ".join(crumbs)
    intro_html = ('<p>%s</p>' % intro) if intro else ""
    return f"""    <section class="page-head">
      <div class="container">
        <div class="breadcrumbs">{crumb_html}</div>
        <p class="eyebrow">{eyebrow}</p>
        <h1>{title}</h1>
        {intro_html}
      </div>
    </section>"""


def cta_band():
    return f"""    <section class="section">
      <div class="container">
        <div class="cta-band reveal">
          <h2>Let's make something together</h2>
          <p>Lessons, training, or a performance booking — reach out and Jennifer will get right back to you.</p>
          <a class="btn btn--gold" href="contact.html">Get in touch</a>
        </div>
      </div>
    </section>"""


# ============================ HOME ============================
HOME = """    <section class="hero">
      <div class="hero__split">
        <div class="hero__panel">
          <p class="eyebrow" style="color:var(--gold)">Performer &middot; Teacher &middot; Fitness Coach</p>
          <h1>A voice for the stage, a heart for teaching.</h1>
          <p>Jennifer Brown brings twenty years of professional performance to private voice, piano, acting &amp; ballet lessons &ndash; plus energizing fitness classes &ndash; right here in Rome, New York and online.</p>
          <div class="hero__cta">
            <a class="btn btn--gold" href="contact.html">Book a lesson</a>
            <a class="btn btn--ghost" href="performances.html" style="color:#fff;border-color:rgba(255,255,255,.6)">See performances</a>
          </div>
        </div>
        <div class="hero__media">
          <div class="hero__slides">
            <div class="hero__slide is-active" style="background-image:url('assets/img/headshots/jennifer-brown-headshot.jpg');background-position:center 25%"></div>
            <div class="hero__slide" style="background-image:url('assets/img/portfolio/romance_romance/RomanceWaltz.jpg')"></div>
            <div class="hero__slide" style="background-image:url('assets/img/home/Kenzie-piano_copy.jpg')"></div>
            <div class="hero__slide" style="background-image:url('assets/img/portfolio/fitness/yoga2.jpg')"></div>
          </div>
          <div class="hero__dots" aria-hidden="false"></div>
        </div>
      </div>
    </section>

    <section class="section">
      <div class="container center" style="max-width:720px">
        <p class="eyebrow">Three ways to work together</p>
        <h2>Performing, teaching &amp; wellness under one roof</h2>
        <p class="lead">Whether you want to take the stage, learn an instrument, or get moving, Jennifer meets you exactly where you are.</p>
      </div>
      <div class="container" style="margin-top:2.5rem">
        <div class="pillars">
          <article class="pillar reveal">
            <div class="pillar__img" style="background-image:url('assets/img/portfolio/annie/Annie-me_dressed_up.jpg')"></div>
            <div class="pillar__body">
              <h3>Performing</h3>
              <p class="pillar__lead">Acting, singing and choreography honed on stages in 46 of the 50 states.</p>
              <ul class="pillar__links">
                <li><a href="perform-acting.html">Acting</a></li>
                <li><a href="perform-singing.html">Singing</a></li>
                <li><a href="perform-choreography.html">Choreography</a></li>
                <li><a href="perform-emcee.html">Emcee/Speaker</a></li>
              </ul>
              <a class="btn btn--sm" href="performances.html">Explore performing</a>
            </div>
          </article>
          <article class="pillar reveal">
            <div class="pillar__img" style="background-image:url('assets/img/home/Kenzie-piano_copy.jpg')"></div>
            <div class="pillar__body">
              <h3>Teaching</h3>
              <p class="pillar__lead">Private voice, piano, acting and ballet lessons for all ages &mdash; structured, encouraging and a lot of fun.</p>
              <ul class="pillar__links">
                <li><a href="lessons-singing.html">Singing</a></li>
                <li><a href="lessons-piano.html">Piano</a></li>
                <li><a href="lessons-acting.html">Acting</a></li>
                <li><a href="lessons-ballet.html">Ballet</a></li>
                <li><a href="lessons-workshops.html">Group</a></li>
              </ul>
              <a class="btn btn--sm" href="lessons-singing.html">Explore teaching</a>
            </div>
          </article>
          <article class="pillar reveal">
            <div class="pillar__img" style="background-image:url('assets/img/portfolio/fitness/yoga2.jpg')"></div>
            <div class="pillar__body">
              <h3>Fitness &amp; Wellness</h3>
              <p class="pillar__lead">Personal training, nutrition coaching and vibrant healthy-aging &mdash; in person and online.</p>
              <ul class="pillar__links">
                <li><a href="personal-training.html">Personal Training</a></li>
                <li><a href="nutrition.html">Nutrition</a></li>
                <li><a href="age-well.html">Age Well &amp; Vibrantly</a></li>
              </ul>
              <a class="btn btn--sm" href="personal-training.html">Explore fitness</a>
            </div>
          </article>
        </div>
      </div>
    </section>

    <section class="section section--cream2">
      <div class="container split">
        <div class="split__img reveal">
          <img src="assets/img/headshots/jennifer-brown-portrait.jpg" alt="Jennifer Brown">
        </div>
        <div class="reveal">
          <p class="eyebrow">A little about me</p>
          <h2>From Iowa cornfields to stages nationwide</h2>
          <p>Jennifer grew up as a tom-boy thrilled by the glow of fireflies and the music of Lawrence Welk. With the cornfields of Iowa as the backdrop to her hometown of Carlisle, she learned the satisfaction of a job well done and a healthy sense of competition &mdash; values she still brings to every lesson and class.</p>
          <a class="btn" href="bio.html">Read Jennifer's story</a>
        </div>
      </div>
    </section>

    <section class="section">
      <div class="container grid grid--2">
        <div class="card reveal">
          <p class="eyebrow">My teaching style</p>
          <h3>"My job is to teach you to not need me anymore."</h3>
          <p>Whether it's piano, singing, pilates, losing weight or general fitness, my goal is for you to be comfortable with your developed craft and skill &mdash; so that I become your coach and mentor, not just your teacher.</p>
          <p>Each time we work together, I want the student to take the lead by asking questions or sharing their practice experiences. It is fun to learn! I learn the most when you ask me the <em>hard</em> questions.</p>
        </div>
        <div class="card reveal" style="display:flex;flex-direction:column;justify-content:center">
          <p class="eyebrow">Words to keep</p>
          <blockquote class="quote">Peter did not feel very brave; indeed, he felt he was going to be sick. But that made no difference to what he had to do.
            <cite>&mdash; C. S. Lewis, <em>The Lion, the Witch and the Wardrobe</em></cite>
          </blockquote>
        </div>
      </div>
    </section>
""" + cta_band()


# ============================ BIO ============================
BIO = page_head("About", "Meet Jennifer", "Performer, teacher and coach with a voice hailed as &ldquo;the voice of a nightingale.&rdquo;",
    ['<a href="index.html">Home</a>', 'Bio']) + """
    <section class="section">
      <div class="container grid grid--sidebar">
        <div class="prose reveal">
          <p>Jennifer grew up as a tom-boy who was thrilled by the glow of fireflies and the music of Lawrence Welk. With the cornfields of Iowa as the backdrop to her hometown of Carlisle, Jennifer learned the satisfaction of a job well done and developed a healthy sense of competition. The neighborhood was filled with kids who would gather to play kick-ball, race home-made go-carts, see who could climb the tree fastest or catch the most fireflies. Their energies were always replenished by Mom's special chocolate chip cookies and kool aid. Sunday nights were Family Night and began with a huge bowl of popcorn and watching <em>The Lawrence Welk Show</em>. Curled up in &ldquo;Dad's black recliner,&rdquo; Jennifer recalls that &ldquo;the slow, pretty songs always made me cry. I didn't understand it at such a young age, but I relished the fact that music and song can truly touch our souls.&rdquo;</p>

          <p>Jennifer's interest in singing began very early. She humorously claims her desire to sing prompted her to learn to read. &ldquo;I wanted to sing the hymns in church, but not knowing the words made that difficult.&rdquo; Throughout grade school and high school she sang in choirs, played many leading roles in the school plays and performed with Celebration Iowa, a touring production cast with the &lsquo;cream of the crop&rsquo; of Iowa's musically gifted teenagers.</p>

          <p>Her desire to perform was enhanced by attending Luther College on a vocal scholarship. Initially she chose to major in pre-medicine, but this denial of her true talents only added flame to the fire once she switched to earn a theater-dance degree. Jennifer graduated and went on to dance with Co'Motion Dance Company before moving to NYC. For twenty years she traveled all over the country performing regionally, nationally and on international cruise ship productions of plays, musicals, films and her one-woman musical cabarets.</p>

          <p>In addition to her love of the stage, Jennifer enjoys writing, reading, hiking, watching Lawrence Welk re-runs and catching fireflies with her daughter &amp; husband.</p>

          <h3>On stage</h3>
          <p>With a voice and a stage presence that has captivated audiences across the country, Jennifer's soprano voice has been hailed as the voice of a nightingale and heard in such roles as Guenevere (<em>Camelot</em>), Johanna (<em>Sweeney Todd</em>), Grace (<em>Annie</em>) and Liesl (<em>The Sound of Music</em>) &mdash; on stages in 46 of the 50 states.</p>

          <h3>In the classroom</h3>
          <p>Jennifer has taught, guest-lectured and been an artist-in-residence and fitness-coach-in-residence for all ages (3&ndash;100) utilizing 45-minute workshops, single-afternoon programs, weekend programs, evening programs and one- to six-week workshops.</p>

          <p>Jennifer currently resides just north of Rome, NY, where she teaches voice, piano, ballet and acting privately in her studio and coaches individuals wishing to create a healthier body and mind.</p>
        </div>
        <aside class="reveal">
          <div class="card">
            <img src="assets/img/headshots/bio-denim.jpg" alt="Jennifer Brown" style="border-radius:10px;margin-bottom:1rem">
            <a class="btn btn--sm" href="resume.html">View full resume</a>
          </div>
        </aside>
      </div>
    </section>
""" + cta_band()


# ===================== TEACHING: SINGING =====================
LESSONS_SINGING = page_head("Teaching · Voice", "Singing Lessons",
    "Private voice lessons for every age and ability &mdash; structured, encouraging and a lot of fun.",
    ['<a href="index.html">Home</a>', 'Teaching', 'Singing']) + """
    <section class="section">
      <div class="container grid grid--sidebar">
        <div class="prose reveal">
          <blockquote class="quote">Jennifer makes you want to take lessons. She's fun, encouraging, and knows what she's talking about &mdash; which is so refreshing. My time with her as both a vocal and acting coach was so valuable, and helped me get into school to pursue a degree in Music Theater. I couldn't have done it without her guidance.
            <cite>&mdash; Michael B., student at University of Buffalo</cite>
          </blockquote>
          <p>All ages are welcome! If you have always wanted to sing but believe that you cannot carry a tune in a bucket, I would <em>love</em> to help you disprove that theory. If you were blessed with a great ear and the vocal chops to match, I'd very much enjoy helping you become the strongest, healthiest singer possible &mdash; so you can enjoy your talent for years to come without any vocal issues.</p>
          <p>Lessons are structured but a lot of fun! Homework will be assigned and expected to be worked on in order to get the most out of the next session. Most lessons are 30 minutes. Students can increase to a 45-minute lesson based on focus, vocal maturity, and what would be most fun for them.</p>
          <p>A strict 24-hour cancellation policy that applies to the student and to me, the teacher. If the lesson is for a child, the parent is welcome to have a cup of tea at my kitchen table while reading a book or enjoy a walk outside.</p>
          <p class="signoff">&mdash; Jennifer</p>
        </div>
        <aside class="reveal">
          <img src="assets/img/home/Kiersten-voice.jpg" alt="A student during a voice lesson" style="border-radius:12px;box-shadow:var(--shadow-md);margin-bottom:1.5rem">
          <div class="rate">
            <h4>45-minute lesson</h4>
            <ul>
              <li>First lesson <span class="price">$40</span></li>
              <li>Single lesson <span class="price">$55</span></li>
              <li>5 lessons <span class="price">$250 <small>/ 6 wks</small></span></li>
              <li>10 lessons <span class="price">$400 <small>/ 12 wks</small></span></li>
            </ul>
          </div>
          <div class="rate" style="margin-top:1rem">
            <h4>30-minute lesson</h4>
            <ul>
              <li>First lesson <span class="price">$30</span></li>
              <li>Single lesson <span class="price">$40</span></li>
              <li>5 lessons <span class="price">$180 <small>/ 6 wks</small></span></li>
              <li>10 lessons <span class="price">$300 <small>/ 12 wks</small></span></li>
            </ul>
          </div>
          <p class="note" style="margin-top:1rem">As always, a 24-hour cancellation notice is required, otherwise, the lesson will be forfeit.<br>This applies to me as well. &#128522;<br>A package of 5 lessons expires in 6 weeks.<br>A package of 10 lessons expires in 12 weeks.</p>
          <a class="btn" href="contact.html" style="margin-top:1rem">Book a voice lesson</a>
        </aside>
      </div>
    </section>
""" + cta_band()


# ===================== TEACHING: PIANO =====================
LESSONS_PIANO = page_head("Teaching · Piano", "Piano Lessons",
    "For children and adults, beginner to intermediate.",
    ['<a href="index.html">Home</a>', 'Teaching', 'Piano']) + """
    <section class="section">
      <div class="container grid grid--sidebar">
        <div class="prose reveal">
          <div class="grid grid--2" style="margin-bottom:1.6rem">
            <blockquote class="quote">Jennifer brings a wonderful attitude and energy to everything she does. Her light-hearted approach makes learning fun and encourages people to keep on learning.
              <cite>&mdash; Larry B., retired State worker</cite>
            </blockquote>
            <blockquote class="quote">The inner joy I feel for music is now able to be expressed outwardly because of Jennifer's competent, pleasant and caring instruction. I'm amazed at what I can play due to her individualized lessons.
              <cite>&mdash; Vicki C., retired biologist</cite>
            </blockquote>
          </div>
          <p>If you have always wanted to learn to read music and begin to play your favorite hymns or radio tunes, this is where you want to start!</p>
          <p>I've been playing piano for over 45 years and teaching for 30+. My forte is teaching the beginner student and taking them to an intermediate level. The <em>Bastien Piano</em> books are my preference, I can send you the link, but if you have lesson books you have already been using &mdash; let&rsquo;s use those! Lessons are structured but a lot of fun with homework assigned between sessions.</p>
          <p>I teach weekends and weekdays, with a strict 24-hour cancellation policy that applies to me too. Most lessons are 30 minutes. Students can increase to a 45-minute lesson based on focus, vocal maturity, and what would be most fun for them.</p>
          <p class="signoff">&mdash; Jennifer</p>
        </div>
        <aside class="reveal">
          <img src="assets/img/home/Kenzie-piano_copy.jpg" alt="A student at the piano" style="border-radius:12px;box-shadow:var(--shadow-md);margin-bottom:1.5rem">
          <div class="rate">
            <h4>45-minute lesson</h4>
            <ul>
              <li>First lesson <span class="price">$40</span></li>
              <li>Single lesson <span class="price">$55</span></li>
              <li>5 lessons <span class="price">$250 <small>/ 6 wks</small></span></li>
              <li>10 lessons <span class="price">$400 <small>/ 12 wks</small></span></li>
            </ul>
          </div>
          <div class="rate" style="margin-top:1rem">
            <h4>30-minute lesson</h4>
            <ul>
              <li>First lesson <span class="price">$30</span></li>
              <li>Single lesson <span class="price">$40</span></li>
              <li>5 lessons <span class="price">$180 <small>/ 6 wks</small></span></li>
              <li>10 lessons <span class="price">$300 <small>/ 12 wks</small></span></li>
            </ul>
          </div>
          <p class="note" style="margin-top:1rem">As always, a 24-hour cancellation notice is required, otherwise, the lesson will be forfeit.<br>This applies to me as well. &#128522;<br>A package of 5 lessons expires in 6 weeks.<br>A package of 10 lessons expires in 12 weeks.</p>
          <a class="btn" href="contact.html" style="margin-top:1rem">Book a piano lesson</a>
        </aside>
      </div>
    </section>
""" + cta_band()


# ===================== TEACHING: ACTING =====================
LESSONS_ACTING = page_head("Teaching · Acting", "Acting Lessons",
    "Private coaching from a working actor of 30+ years &mdash; auditions, scenes, on-camera and more.",
    ['<a href="index.html">Home</a>', 'Teaching', 'Acting']) + """
    <section class="section">
      <div class="container grid grid--sidebar">
        <div class="prose reveal">
          <div class="grid grid--2" style="margin-bottom:1.6rem">
            <blockquote class="quote">Jennifer not only has a great deal of talent and experience in the performing arts, she is also a talented teacher. She has a deep understanding of how the &ldquo;human instrument&rdquo; works and how to apply that knowledge to bring out the best performance possible in her students.
              <cite>&mdash; Connie B., retired day-care owner</cite>
            </blockquote>
            <blockquote class="quote">Jennifer understood my son's musical and acting needs, which made his lessons enjoyable.
              <cite>&mdash; parent of Peter C.</cite>
            </blockquote>
          </div>
          <p>Have an audition coming up that you want to nail? Got a part in the school play or community theater and aren't sure what to do with it? Or do you simply love acting and you're preparing for college or a move to NYC? I've been in this crazy acting business for 30+ years &mdash; wherever you are, I have been there too, and I'd really enjoy helping you.</p>
          <ul>
            <li>Monologues</li>
            <li>Scene study</li>
            <li>Commercial</li>
            <li>Voice over</li>
            <li>Improvisation</li>
            <li>Script analysis</li>
            <li>The business &amp; marketing of the business</li>
            <li>Public Speaking</li>
          </ul>
          <p>Lessons are structured but a lot of fun, with homework between sessions. I teach weekends and weekdays, with a strict 24-hour cancellation policy that applies to me too. Most lessons are 30 minutes. Students can increase to a 45-minute lesson based on focus, vocal maturity, and what would be most enjoyable for them.</p>
          <p class="note">Looking for a group setting? See <a href="lessons-workshops.html">Second Saturdays workshops</a> and the &ldquo;Business of the Business&rdquo; seminar.</p>
          <p class="signoff">&mdash; Jennifer</p>
        </div>
        <aside class="reveal">
          <div class="rate">
            <h4>45-minute lesson</h4>
            <ul>
              <li>First lesson <span class="price">$40</span></li>
              <li>Single lesson <span class="price">$55</span></li>
              <li>5 lessons <span class="price">$250 <small>/ 6 wks</small></span></li>
              <li>10 lessons <span class="price">$400 <small>/ 12 wks</small></span></li>
            </ul>
          </div>
          <div class="rate" style="margin-top:1rem">
            <h4>30-minute lesson</h4>
            <ul>
              <li>First lesson <span class="price">$30</span></li>
              <li>Single lesson <span class="price">$40</span></li>
              <li>5 lessons <span class="price">$180 <small>/ 6 wks</small></span></li>
              <li>10 lessons <span class="price">$300 <small>/ 12 wks</small></span></li>
            </ul>
          </div>
          <p class="note" style="margin-top:1rem">As always, a 24-hour cancellation notice is required, otherwise, the lesson will be forfeit.<br>This applies to me as well. &#128522;<br>A package of 5 lessons expires in 6 weeks.<br>A package of 10 lessons expires in 12 weeks.</p>
          <a class="btn" href="contact.html" style="margin-top:1rem">Book an acting lesson</a>
        </aside>
      </div>
    </section>
""" + cta_band()


# ===================== TEACHING: WORKSHOPS =====================
LESSONS_WORKSHOPS = page_head("Teaching · Group", "Workshops &amp; Seminars",
    "Second Saturdays group workshops for acting &amp; singing, plus the &ldquo;Business of the Business&rdquo; seminar.",
    ['<a href="index.html">Home</a>', 'Teaching', 'Workshops &amp; Group']) + """
    <section class="section">
      <div class="container">
        <div class="grid grid--2">
          <div class="card reveal">
            <p class="eyebrow">Second Saturdays</p>
            <h3>Workshops for Acting &amp; Singing</h3>
            <ul class="facts">
              <li><span class="k">When</span> 5&ndash;7pm, the second Saturday of the month</li>
              <li><span class="k">Where</span> Jennifer's studio, ~5 min N of Stokes Elementary, Rome (call for directions)</li>
              <li><span class="k">Who</span> Private students &amp; drop-ins · beginner to advanced</li>
              <li><span class="k">Size</span> Minimum 5, maximum 10 participants</li>
              <li><span class="k">Cost</span> $20 per participant</li>
            </ul>
            <p class="note">Reservations and payment are due no later than two weeks before the workshop date.</p>
          </div>
          <div class="reveal">
            <div class="card" style="margin-bottom:1.4rem">
              <h3>Acting Workshop</h3>
              <p>The first 30 minutes are spent on a warm-up and group exercises, followed by small-group scenes (typically 2&ndash;3 actors). Each participant gets one-on-one time to develop their own skills, with the goal of a polished monologue. Open to junior high through adult &mdash; also great for anyone developing public-speaking skills.</p>
            </div>
            <div class="card">
              <h3>Singing Workshop</h3>
              <p>The first 20 minutes are a group vocal and physical warm-up, followed by 10&ndash;15 minutes of stage-presence exercises. Each participant gets one-on-one time to develop a song of their choice, building toward a solid repertoire book for future endeavors. Open to all ages and skill levels.</p>
            </div>
          </div>
        </div>

        <div class="card reveal" style="margin-top:1.6rem">
          <p class="eyebrow">On demand</p>
          <h3>The Business of the Business Seminar</h3>
          <p>This 2.5-hour seminar is available on demand. If you'd like to bring it to your organization or a group of interested friends, please <a href="contact.html">contact Jennifer</a>. For performing artists of all kinds &mdash; singers, actors, dancers, models. Participants under 18 must be accompanied by an adult (no charge for the accompanying adult).</p>
          <div class="grid grid--2" style="margin-top:1rem">
            <div>
              <h4 style="font-family:var(--serif);color:var(--plum-deep);margin-bottom:.5rem">A must-attend for</h4>
              <ul>
                <li>The beginning performing artist who wants to make an intelligent career or hobby choice</li>
                <li>The performing artist looking to take their craft to the highest artistic level</li>
              </ul>
              <p style="margin-top:.6rem"><strong>Fee:</strong> $30 &middot; minimum 6 participants to run.</p>
            </div>
            <div>
              <h4 style="font-family:var(--serif);color:var(--plum-deep);margin-bottom:.5rem">Topics include</h4>
              <ol style="columns:2;column-gap:1.4rem;margin-left:1.1rem">
                <li>Required business tools</li>
                <li>Headshot &amp; resume</li>
                <li>Working office space</li>
                <li>Knowing your product</li>
                <li>Improving your craft</li>
                <li>Your marketing plan</li>
                <li>The audition</li>
                <li>The job search</li>
                <li>Taxes</li>
                <li>&ldquo;I have an agent, now what?&rdquo;</li>
              </ol>
            </div>
          </div>
          <p class="note" style="margin-top:1rem">Bring a headshot &amp; resume (if available, not required) and a notebook &amp; pen.</p>
        </div>
      </div>
    </section>
""" + cta_band()


# ===================== TEACHING: BALLET =====================
LESSONS_BALLET = page_head("Teaching · Ballet", "Ballet Lessons",
    "Private ballet instruction for children and adults &mdash; from first positions to refining your technique.",
    ['<a href="index.html">Home</a>', 'Teaching', 'Ballet']) + """
    <section class="section">
      <div class="container grid grid--sidebar">
        <div class="prose reveal">
          <p>Trained in ballet and a retired professional dancer, I bring a lifetime of movement to private ballet lessons for children and adults. Whether your little one dreams of their first <em>plié</em>, you're an adult who always wanted to try, or you're a dancer looking to polish technique, lessons meet you exactly where you are.</p>
          <p>We build a strong foundation &mdash; posture, alignment, barre work, port de bras and musicality &mdash; in a way that is structured but genuinely joyful. As with all of my teaching, the goal is for you to grow into your own confident dancer, not to need your teacher forever.</p>
          <p>Lessons are tailored to age and level. For younger dancers, creative movement keeps things playful while building real skills; for teens and adults, we focus on technique, strength and grace. Homework (yes, ballet has homework!) is assigned so you get the most from each session.</p>
          <p>I teach on weekends as well as weekdays, with a strict 24-hour cancellation policy that applies to me too. Most lessons are 30 minutes. Students can increase to a 45-minute lesson based on focus, vocal maturity, and what would be most enjoyable for them.</p>
          <p class="signoff">&mdash; Jennifer</p>
        </div>
        <aside class="reveal">
          <div class="rate">
            <h4>45-minute lesson</h4>
            <ul>
              <li>First lesson <span class="price">$40</span></li>
              <li>Single lesson <span class="price">$55</span></li>
              <li>5 lessons <span class="price">$250 <small>/ 6 wks</small></span></li>
              <li>10 lessons <span class="price">$400 <small>/ 12 wks</small></span></li>
            </ul>
          </div>
          <div class="rate" style="margin-top:1rem">
            <h4>30-minute lesson</h4>
            <ul>
              <li>First lesson <span class="price">$30</span></li>
              <li>Single lesson <span class="price">$40</span></li>
              <li>5 lessons <span class="price">$180 <small>/ 6 wks</small></span></li>
              <li>10 lessons <span class="price">$300 <small>/ 12 wks</small></span></li>
            </ul>
          </div>
          <p class="note" style="margin-top:1rem">As always, a 24-hour cancellation notice is required, otherwise, the lesson will be forfeit.<br>This applies to me as well. &#128522;<br>A package of 5 lessons expires in 6 weeks.<br>A package of 10 lessons expires in 12 weeks.</p>
          <a class="btn" href="contact.html" style="margin-top:1rem">Book a ballet lesson</a>
          <div class="card" style="margin-top:1.2rem">
            <h3>Good to know</h3>
            <ul class="prose" style="margin-top:.5rem">
              <li>Children &amp; adults welcome</li>
              <li>Absolute beginners encouraged</li>
              <li>In person near Rome, NY</li>
            </ul>
          </div>
        </aside>
      </div>
    </section>
""" + cta_band()


# ===================== FITNESS: PERSONAL TRAINING =====================
PERSONAL_TRAINING = page_head("Fitness · Training", "Personal Training",
    "Virtual or in-person, 1-on-1 training that fits your goals, your space and your budget.",
    ['<a href="index.html">Home</a>', 'Fitness', 'Personal Training']) + """
    <section class="section">
      <div class="container grid grid--sidebar">
        <div class="prose reveal">
          <h3>Goals you might have</h3>
          <ul style="columns:2;column-gap:1.6rem">
            <li>Remove 10&ndash;100 lbs</li>
            <li>Lower A1C</li>
            <li>Feel comfortable in a swimsuit</li>
            <li>Champion perimenopause</li>
            <li>Get off blood-pressure medicine</li>
            <li>Drop 2 dress sizes for a wedding</li>
            <li>Gain 20 lbs &amp; muscle mass</li>
          </ul>
          <h3>My belief system</h3>
          <p>Wherever you are today in your fitness and nutrition journey is where you are. It's not bad or good; it simply is. Rather than an overhaul, we'll find places to tweak. As overused as the term is, we will create a lifestyle change: I want it to feel <em>off</em> for your body to not move every single day, and to feel <em>off</em> when you eat too much sugar or not enough protein or fiber. I have my own demons too &mdash; I'm truly addicted to sugar &mdash; so I know what you're going through. I'm here to help you create behavioral changes to achieve your goals.</p>
          <p>Yes, we can meet in your home (additional travel fee) or a gym or outdoors at a park (that&rsquo;s always fun!). But most prefer to work together via Zoom or FaceTime simply due to time constraints. We can meet in your living room, kitchen, or office &mdash; anytime that works for your schedule. Not having to drive to a gym or pay for a gym membership is very helpful.</p>
          <p>If you have equipment at home such as dumbbells, exercise ball, resistance bands, I'll help you learn how to use them most effectively. However, walls, floors and chairs make for incredible workouts! Together we will create a daily routine you can do anytime, not just when we're together.</p>
        </div>
        <aside class="reveal">
          <img src="assets/img/portfolio/fitness/wall.jpg" alt="Bodyweight wall workout" style="border-radius:12px;box-shadow:var(--shadow-md);margin-bottom:1.5rem">
          <div class="rate">
            <h4>One-on-one · per 1-hr session</h4>
            <ul>
              <li>Single session <span class="price">$40</span></li>
              <li>10 sessions <span class="price">$35 <small>ea ($350)</small></span></li>
              <li>15 sessions <span class="price">$30 <small>ea ($450)</small></span></li>
            </ul>
          </div>
          <div class="rate" style="margin-top:1rem">
            <h4>Train with a friend · per session</h4>
            <ul>
              <li>Single session <span class="price">$60</span></li>
              <li>10 sessions <span class="price">$55 <small>ea ($550)</small></span></li>
              <li>15 sessions <span class="price">$50 <small>ea ($750)</small></span></li>
            </ul>
          </div>
          <p class="note" style="margin-top:1rem">Training is available one-on-one, in person near Rome, NY or online (Zoom or FaceTime) &mdash; and pairs naturally with <a href="nutrition.html">Nutrition Coaching</a>.</p>
          <a class="btn" href="contact.html" style="margin-top:1rem">Start training</a>
        </aside>
      </div>
    </section>
"""


# ===================== FITNESS: NUTRITION =====================
NUTRITION = page_head("Fitness &amp; Wellness · Nutrition", "Behavioral Nutrition",
    "Sustainable, grace-filled nutrition coaching.",
    ['<a href="index.html">Home</a>', 'Fitness', 'Behavioral Nutrition']) + """
    <section class="section">
      <div class="container grid grid--sidebar">
        <div class="prose reveal">
          <p>Wherever you are today in your nutrition journey is where you are. It's not bad or good; it simply is &mdash; and it can always be improved upon. As your nutrition coach, I won't hand you an overhaul or a fad. Instead, we find realistic places to tweak, one habit at a time, until eating well stops feeling like a project and starts feeling like <em>you</em>.</p>
          <p>The goal is to create behaviors for a lifestyle, not a diet.</p>
          <p>This is where science meets simplicity, and where you learn how to truly nourish your body and mind.</p>
          <p>Here&rsquo;s what you&rsquo;ll discover:</p>
          <ul>
            <li><strong>The power of protein:</strong> when to eat it and how it fuels your metabolism.</li>
            <li><strong>True portion size:</strong> what balance really looks like on your plate.</li>
            <li><strong>Smart supplementation:</strong> why adding the right support matters.</li>
            <li><strong>Gut health non-negotiables:</strong> the 3 daily essentials for lasting wellness.</li>
            <li><strong>Low-glycemic grocery shopping:</strong> how to make confident choices that stabilize blood sugar.</li>
            <li>7 healthy habits you&rsquo;ll repeat for life.</li>
            <li><strong>Brain training:</strong> wash away old patterns and replace them with empowering thoughts and behaviors.</li>
          </ul>
          <p>And that&rsquo;s just the beginning.</p>
          <p>You&rsquo;ll gain clarity and confidence as we celebrate progress, not perfection.</p>
          <p>&#10024; I&rsquo;m here as your coach, ready to guide you step by step toward a lifestyle that feels sustainable, strong, and joyful.</p>
          <p>By the way, I have my own demons too &mdash; so this is a partnership, not a lecture.</p>
          <p class="signoff">&mdash; Jennifer</p>
        </div>
        <aside class="reveal">
          <div class="card">
            <h3>Work with Jennifer</h3>
            <p style="color:var(--muted)">Every body and goal is different, so nutrition coaching is tailored to you. Reach out and we'll find the right starting point.</p>
            <a class="btn btn--sm" href="contact.html" style="margin-top:.6rem">Start a conversation</a>
          </div>
        </aside>
      </div>
    </section>
""" + cta_band()


# ===================== FITNESS: AGE WELL & VIBRANTLY =====================
AGE_WELL = page_head("Fitness &amp; Wellness · Healthy Aging", "Age Well &amp; Vibrantly",
    "A behavioral program for a lifestyle, not a diet.",
    ['<a href="index.html">Home</a>', 'Fitness', 'Age Well &amp; Vibrantly']) + """
    <section class="section">
      <div class="container">
        <div class="prose reveal" style="max-width:760px">
          <p class="lead">Goal is NOT to be skinny (but no one ever said &lsquo;no&rsquo; to less fat).</p>
          <p>Goal IS to be in our 80s and:</p>
          <ul>
            <li>doing our own grocery shopping</li>
            <li>living independently</li>
            <li>having FUN w/ family</li>
            <li>not being a burden to our family</li>
            <li>walking and hiking with ease</li>
            <li>no medicines</li>
          </ul>
          <p>And in the meantime, learning daily behaviors and habits that are easily stackable, so that we live better NOW and stronger later.</p>
          <p style="font-weight:700">This is a behavioral program for a lifestyle, not a diet.</p>
          <p>This is where science meets simplicity, and where you learn how to truly nourish your body and mind.</p>
          <p>Here&rsquo;s what you&rsquo;ll discover&hellip;</p>
          <ul>
            <li><strong>The power of protein:</strong> when to eat it and how it fuels your metabolism.</li>
            <li><strong>True portion size:</strong> what balance really looks like on your plate.</li>
            <li><strong>Smart supplementation:</strong> why adding the right support matters.</li>
            <li><strong>Gut health non-negotiables:</strong> the 3 daily essentials for lasting wellness.</li>
            <li><strong>Low-glycemic grocery shopping:</strong> how to make confident choices that stabilize blood sugar.</li>
            <li><strong>The 6-week plan:</strong> easy to follow, built around 7 healthy habits you&rsquo;ll repeat for life.</li>
            <li><strong>Brain training:</strong> wash away old patterns and replace them with empowering thoughts and behaviors.</li>
          </ul>
          <p>And that&rsquo;s just the beginning.</p>
          <p>You&rsquo;ll gain clarity, confidence, and a community that celebrates progress, not perfection.</p>
          <p>&#10024; I&rsquo;m here as your coach, ready to guide you step by step toward a lifestyle that feels sustainable, strong, and joyful.</p>
          <figure style="margin:2rem 0 0;text-align:center">
            <a href="assets/img/fitness/age-well-vibrantly.jpg" target="_blank" rel="noopener">
              <img src="assets/img/fitness/age-well-vibrantly.jpg" alt="Age Well &amp; Vibrantly — 6-week educational program flyer. Begins July 19, 2026. $30 one-time fee. A behavioral program, not a diet; Mon&ndash;Fri exercise sessions; the closest thing to having a personal trainer; smart food choices; recipe ideas; and a supportive community — all on a private Facebook page." loading="lazy" style="max-width:440px;width:100%;margin:0 auto;border-radius:12px;box-shadow:var(--shadow-md)">
            </a>
          </figure>
          <div class="note" style="margin-top:1.6rem">
            <p style="margin:0">Tell me a little about your goals and any concerns, because each of us is unique.</p>
            <a class="btn btn--sm" href="contact.html" style="margin-top:.9rem">Let's Talk</a>
          </div>
        </div>
      </div>
    </section>
""" + cta_band()


# ===================== PERFORMING: PERFORMANCE DATES =====================
_PERFS = [
    ("May 25, 2012", "&ldquo;Songs of the 1910s&rdquo; Concert &mdash; Elder Haven, Canastota, NY"),
    ("Dec 28, 2011", "Christmas Concerts &mdash; Ava Dorfman Center, Rome &amp; Elder Haven, Canastota, NY"),
    ("Aug 16, 2011", "&ldquo;Too Darn Hot&rdquo; Concert &mdash; Elder Haven, Canastota, NY"),
    ("Dec 24, 2010", "Christmas Eve Service &mdash; Holy Cross Lutheran Church, Carlisle, IA"),
    ("Dec 20, 2010", "Christmas Concert &mdash; Elder Haven, Canastota, NY"),
    ("Nov 13, 2010", "MC, Statewide 912 Patriots Dinner &mdash; Kallet Civic Center, Oneida, NY"),
    ("Aug 14, 2010", "Tribute Song &mdash; Canastota Kids' Day Festival, Canastota, NY"),
    ("Jul 14, 2010", "&ldquo;Summer Fling&rdquo; Concert &mdash; Elder Haven, Canastota, NY"),
    ("May 23, 2010", "National Center for Missing &amp; Exploited Children Benefit &mdash; Staley Upper Elementary, Rome, NY"),
    ("Mar 16, 2010", "St. Patty's Concert &mdash; Elder Haven, Canastota, NY"),
    ("Jul 12, 2009", "Boilermaker Post-Race Party &mdash; F.X. Matt Brewing Company, Utica, NY"),
    ("Jul 4, 2009", "Ft. Stanwix Patriots Tea Party Rally &amp; Declare Your Independence &mdash; Rome, NY"),
    ("Jun 6, 2009", "Relay for Life Luminary Ceremony &mdash; Oneida High School, Oneida, NY"),
    ("Nov 14, 2008", "Skits-O-Phrenia (Director) &mdash; VVS High School, Verona, NY"),
    ("Jul 10&ndash;20, 2008", "The Robber Bridegroom (Choreographer; Airie &amp; Raven) &mdash; Bristol Valley Theater, Naples, NY"),
    ("Jun 12&ndash;22, 2008", "The Musical of Musicals (The Musical!) &mdash; Bristol Valley Theater, Naples, NY"),
    ("Oct 20&ndash;21, 2007", "&ldquo;Love Is Like&hellip;&rdquo; Concerts &mdash; Bristol Valley Theater, Naples, NY"),
    ("Aug 1, 2007", "The Sweetest Sounds: Broadway of the 1960s&ndash;90s &mdash; Old Westbury Gardens, NY"),
    ("Jul 12&ndash;22, 2007", "Man of La Mancha (Antonia) &mdash; Bristol Valley Theater, Naples, NY"),
    ("Jun 16&ndash;24, 2007", "Lend Me a Tenor (Maggie) &mdash; Bristol Valley Theater, Naples, NY"),
    ("Jun 6, 2007", "Heard the Voice, St. John's Lutheran Choir Concert (Director) &mdash; Rome, NY"),
    ("Apr 15 &amp; 22, 2007", "Earthly Delights &mdash; Emerging Artists Theatre, NYC"),
    ("Feb 9&ndash;10, 2007", "&ldquo;Love Is Like&hellip;&rdquo; &mdash; 4th Street Theatre, Des Moines, IA"),
    ("Nov 12, 2006", "Earthly Delights &mdash; The Composers Chamber Theatre, NYC"),
    ("Jul 27&ndash;Aug 6, 2006", "Sweeney Todd (Johanna) &mdash; Bristol Valley Theater, Naples, NY"),
    ("Jul 4, 2006", "Traveling Back Home, Concert in the Park &mdash; North Park Bandstand, Carlisle, IA"),
]
_perf_items = "\n".join(
    '          <li><span class="date">%s</span><span class="what">%s</span></li>' % (d, w)
    for d, w in _PERFS
)
PERFORMANCES = page_head("Performing · Dates", "Performance History",
    "A selection of concerts, productions and appearances across the country.",
    ['<a href="index.html">Home</a>', 'Performing', 'Performance Dates']) + f"""
    <section class="section">
      <div class="container grid grid--sidebar">
        <div class="reveal">
          <ul class="timeline">
{_perf_items}
          </ul>
          <p class="note" style="margin-top:1.5rem">Interested in booking Jennifer for a concert, benefit or event? <a href="contact.html">Get in touch</a> &mdash; she performs cabaret, concert and theatrical programs for all kinds of occasions.</p>
        </div>
        <aside class="reveal">
          <img src="assets/img/home/performance_dates_pic.jpg" alt="Jennifer performing" style="border-radius:12px;box-shadow:var(--shadow-md);margin-bottom:1.2rem">
          <div class="card">
            <h3>Book a performance</h3>
            <p style="font-size:.95rem;color:var(--muted)">Concerts &middot; cabaret &middot; benefits &middot; church &amp; community events.</p>
            <a class="btn btn--sm" href="contact.html" style="margin-top:.6rem">Check availability</a>
          </div>
        </aside>
      </div>
    </section>
"""


# ===================== PERFORMING: RESUME =====================
def credits_table(caption, rows):
    body = "\n".join(
        '          <tr><th>%s</th><td class="role">%s</td><td class="house">%s</td></tr>' % r
        for r in rows
    )
    return f"""        <table class="credits">
          <caption>{caption}</caption>
{body}
        </table>"""

_FILM = [
    ("Fertility Drug (drama)", "Lead", "Sable Brush Productions"),
    ("Decision Final (drama)", "Lead", "In Your Face Productions"),
    ("Angel's Blade (horror)", "Supporting Lead", "Stock's Eye Productions"),
    ("Black Cougar (kids' superhero)", "Supporting Lead", "Silvio DiSalvatore Production"),
    ("Paper Trail (drama)", "Supporting Lead", "48 Hr Film Project"),
    ("Precipice (comedy)", "Supporting Lead", "Sri Productions"),
    ("Many Shades of Mulberry", "Lead", "Syracuse U Film"),
    ("House of Fall &amp; Leaves", "Lead", "Syracuse U Film"),
    ("Slaughtered Lamb (silent)", "Lead", "NYU Film"),
    ("Where'd He Go? (action)", "Lead", "NYU Film"),
    ("Mona Lisa Smile", "Student (Taft-Hartley)", "Shoelace Productions"),
]
_NY = [
    ("Earthly Delights (reading)", "Chastity (lead)", "Emerging Artists Theatre"),
    ("Marion Anderson &mdash; Her Story", "Dancer / Greek Chorus", "National Black Theater"),
    ("Fare for All", "Sarah (lead)", "DramaMuse Productions"),
    ("A Little Night Music", "Mrs. Nordstrom", "Prospect Theater"),
    ("Measure for Measure", "Lead soprano / nun", "Todo Con Nada"),
    ("Romeo &amp; Juliet &mdash; Tribal", "Balthasar", "La Mama Theater"),
    ("Moods in Music", "Lead soprano", "Maverick Theatre"),
]
_REGIONAL = [
    ("Sweeney Todd", "Johanna (&amp; clarinet)", "Bristol Valley Theater"),
    ("The Musical of Musicals", "June", "Bristol Valley Theater"),
    ("The Robber Bridegroom", "Raven &amp; Goat's Mother", "Bristol Valley Theater"),
    ("Vanities", "Joanne", "Bristol Valley Theater"),
    ("Lend Me a Tenor", "Maggie", "Bristol Valley Theater"),
    ("Man of La Mancha", "Antonia", "Bristol Valley Theater"),
    ("Seven Keys to Baldpate", "Mary Norton", "Bristol Valley Theater"),
    ("Romance / Romance", "Lina / Barb", "Bristol Valley Theater"),
    ("Annie", "Grace Farrell", "Broadway Palm West &amp; Circa '21"),
    ("Singin' in the Rain", "Lina Lamont", "Perry Productions"),
    ("The Sound of Music", "Liesl", "Ingersoll Dinner Theater"),
    ("Quilters", "Ensemble", "Roxy Regional Theatre"),
]
_TOURS = [
    ("Camelot", "Guenevere U/S (performed)", "Troika Productions"),
    ("Seabourn Legend", "Asst. Cruise Director, cabaret &amp; ensemble", "Seabourn Cruise Lines"),
    ("American Queen", "Soprano (quartet) &amp; dance captain", "Delta Queen Steamboat Co."),
]
_CABARET = [
    ("Love Is Like&hellip;", "Solo show", "Regionally performed"),
    ("Finding Home", "Solo show", "Regionally performed"),
    ("Dessert First", "Solo show", "Regionally performed"),
    ("Phases of Love", "Solo show", "Regionally performed"),
    ("Travels &amp; Daydreams", "Solo show", "Regionally performed"),
    ("Sister Angelica", "Tourier", "Dorian Opera Theatre"),
    ("The Magic Flute", "Chorus", "Dorian Opera Theatre"),
]
_CHOREO = [
    ("The Robber Bridegroom", "Cast of 11", "Bristol Valley Theater, NY"),
    ("Man of La Mancha", "Combat scene &amp; Moors", "Bristol Valley Theater, NY"),
    ("The Screwtape Letters", "Choreographer", "Theatre 315, NYC"),
    ("Celebration Iowa", "Touring company of 20", "Midwest, USA"),
    ("The Christmas Star", "Dinner theater", "Chatham Theatre, NY"),
    ("Competitive Swing Choirs", "Multiple high schools", "IA, MN &amp; WI"),
    ("The Devil &amp; Daniel Webster", "Audition &amp; show choreo", "Dorian Opera Theater, IA"),
    ("The Music Man", "Audition &amp; show choreo", "Dorian Opera Theater, IA"),
    ("South Pacific / Oklahoma!", "Show choreography", "High school, IA"),
]

RESUME = page_head("Performing · Resume", "Resume",
    "Actor &middot; Singer &middot; Dancer &middot; Choreographer &mdash; soprano, 3+ octaves.",
    ['<a href="index.html">Home</a>', 'Performing', 'Resume']) + f"""
    <section class="section">
      <div class="container">
        <div class="resume-tabs reveal">
          <a class="btn btn--sm" href="#performance">Acting / Performance</a>
          <a class="btn btn--sm btn--ghost" href="#choreo">Choreography</a>
        </div>

        <div class="reveal" id="performance">
          <h2 style="margin-bottom:.3rem">Acting / Performance</h2>
          <div class="resume-meta">
            <span><b>Voice:</b> Soprano</span><span><b>Height:</b> 5&prime;6&Prime;</span>
            <span><b>Size:</b> 6</span><span><b>Hair:</b> Sandy-blonde</span><span><b>Eyes:</b> Blue</span>
          </div>
{credits_table('Film', _FILM)}
{credits_table('New York Theater', _NY)}
{credits_table('Regional Theater', _REGIONAL)}
{credits_table('National Tours &amp; Boats', _TOURS)}
{credits_table('Cabaret &amp; Opera', _CABARET)}
          <div class="card">
            <h3>Training</h3>
            <p><strong>BA in Theater / Dance</strong> &mdash; Luther College.</p>
            <p><strong>Acting:</strong> Creative Acting Studio (12-month intensive &mdash; film, commercial, sitcom, soap, advanced scene study, improv); Actor's Connection; Career Breakthroughs Unlimited (3-day transformational intensive).</p>
            <p><strong>Dance:</strong> West Side Dance Project &mdash; modern, ballet, jazz, liturgical, improv. Workshops with Bella Lewitzky, Twyla Tharp, Lar Lubovitch, Urban Bush Women.</p>
            <p><strong>Sport skills:</strong> Rollerblading &amp; skating, rock climbing, running, basketball, tennis, racquetball, swimming, softball, biking, water &amp; snow skiing, cross-country skiing, football, ultimate frisbee, tae bo, yoga.</p>
            <p><strong>Special skills:</strong> Sight-read music, play clarinet, some sign language, drive stick-shift, great with children.</p>
          </div>
        </div>

        <div class="reveal" id="choreo" style="margin-top:3rem">
          <h2 style="margin-bottom:.6rem">Choreography</h2>
{credits_table('As Choreographer', _CHOREO)}
          <div class="card">
            <h3>Also as dancer &amp; dance captain</h3>
            <p>Principal modern dancer with Co'Motion Dance Company (IA) and Celebration Iowa (touring); principal dancer in <em>American Jubilee</em> (Carousel Dinner Theatre, OH); ensemble dancer, <em>The Magic Flute</em> (Dorian Opera Theater); liturgical dance soloist across IA, MN, WI &amp; NY. Performer &amp; dance captain aboard the American Queen (Delta Queen Steamboat Co.) and for American Entertainment Company (Santa's Village, Chicago).</p>
          </div>
        </div>
      </div>
    </section>
""" + cta_band()


# ===================== PERFORMING: PHOTOS =====================
_GALLERIES = [
    ("Headshots", "headshots", [
        ("headshots/jbernstone179.jpg", "Headshot"),
        ("headshots/jbernstone26.jpg", "Headshot"),
        ("headshots/jbernstone145.jpg", "Headshot"),
        ("headshots/brown_shirt_copy.jpg", "Headshot"),
        ("headshots/Copy_of_green.jpg", "Headshot"),
    ]),
    ("Annie", "annie", [
        ("portfolio/annie/Annie-me_dressed_up.jpg", "Annie &mdash; Grace Farrell"),
        ("portfolio/annie/Annie-3dressed_up.jpg", "Annie"),
        ("portfolio/annie/Annie-MsHandMe.jpg", "Annie"),
        ("portfolio/annie/Annie-tugofwar.jpg", "Annie"),
    ]),
    ("Sweeney Todd", "sweeney", [
        ("portfolio/sweeney_todd/withJudge.jpg", "Sweeney Todd &mdash; Johanna"),
        ("portfolio/sweeney_todd/birdcage.jpg", "Sweeney Todd"),
        ("portfolio/sweeney_todd/final_bows.jpg", "Sweeney Todd &mdash; final bows"),
    ]),
    ("Man of La Mancha", "mlm", [
        ("portfolio/man_of_lamancha/MLM-cast.jpg", "Man of La Mancha &mdash; cast"),
        ("portfolio/man_of_lamancha/MLM-Thinking-of-Him.jpg", "Man of La Mancha"),
        ("portfolio/man_of_lamancha/MLM-my-buttocks.jpg", "Man of La Mancha"),
    ]),
    ("Lend Me a Tenor", "tenor", [
        ("portfolio/tenor/LMT-opening.jpg", "Lend Me a Tenor"),
        ("portfolio/tenor/LMT-kiss.jpg", "Lend Me a Tenor"),
        ("portfolio/tenor/LMT-3-on-couch.jpg", "Lend Me a Tenor"),
        ("portfolio/tenor/LMT-MakeUp.jpg", "Lend Me a Tenor"),
        ("portfolio/tenor/LMT-Silent-Movie.jpg", "Lend Me a Tenor"),
    ]),
    ("Romance / Romance", "romance", [
        ("portfolio/romance_romance/RomanceWaltz.jpg", "Romance / Romance"),
        ("portfolio/romance_romance/RomanceRedHat.jpg", "Romance / Romance"),
        ("portfolio/romance_romance/Romance2Group.jpg", "Romance / Romance"),
        ("portfolio/romance_romance/Romance2gameshow.jpg", "Romance / Romance"),
        ("portfolio/romance_romance/Romance2oldfolks.jpg", "Romance / Romance"),
    ]),
    ("Vanities", "vanities", [
        ("portfolio/vanities/VanitiesPreShow.jpg", "Vanities &mdash; Joanne"),
        ("portfolio/vanities/VanitiesCheer1.jpg", "Vanities"),
        ("portfolio/vanities/VanitiesMirror.jpg", "Vanities"),
        ("portfolio/vanities/VanitiesDrunk.jpg", "Vanities"),
        ("portfolio/vanities/VanitiesWantMore.jpg", "Vanities"),
    ]),
    ("Seven Keys to Baldpate", "baldpate", [
        ("portfolio/seven_keys_to_baldpate/BaldpateGroup.jpg", "Seven Keys to Baldpate"),
        ("portfolio/seven_keys_to_baldpate/BaldpateKiss.jpg", "Seven Keys to Baldpate"),
        ("portfolio/seven_keys_to_baldpate/BaldpateHide.jpg", "Seven Keys to Baldpate"),
        ("portfolio/seven_keys_to_baldpate/BaldpateHands.jpg", "Seven Keys to Baldpate"),
    ]),
    ("Quilters", "quilters", [
        ("portfolio/quilters/quilt11.jpg", "Quilters"),
        ("portfolio/quilters/quilt22.jpg", "Quilters"),
    ]),
    ("A Christmas Star", "xmas", [
        ("portfolio/a_christmas_star/XmasStarFairy.jpg", "A Christmas Star"),
    ]),
    ("Concert &amp; Cabaret", "ely", [
        ("portfolio/ely_pinto/weddingdress.jpg", "In concert"),
        ("portfolio/ely_pinto/purpledress.jpg", "In concert"),
        ("portfolio/ely_pinto/purplesuit.jpg", "In concert"),
        ("portfolio/ely_pinto/flinghair.jpg", "In concert"),
    ]),
    ("Fitness", "fitness", [
        ("portfolio/fitness/wall.jpg", "Fitness"),
        ("portfolio/fitness/yoga2.jpg", "Fitness"),
        ("portfolio/fitness/boxing.jpg", "Fitness"),
        ("portfolio/fitness/boxing1.jpg", "Fitness"),
        ("portfolio/fitness/bike2.jpg", "Fitness"),
    ]),
]

def gallery_html():
    out = []
    for title, gid, imgs in _GALLERIES:
        cells = "\n".join(
            '            <a href="assets/img/%s" data-lightbox data-caption="%s"><img src="assets/img/%s" alt="%s" loading="lazy"></a>'
            % (src, cap, src, cap.replace('&mdash;', '-'))
            for src, cap in imgs
        )
        out.append(f"""        <div class="gallery-group reveal">
          <h3>{title}</h3>
          <div class="gallery">
{cells}
          </div>
        </div>""")
    return "\n".join(out)

PHOTOS = page_head("Performing · Photos", "Photo Gallery",
    "Headshots and production photography from across Jennifer's career. Tap any image to view it full size.",
    ['<a href="index.html">Home</a>', 'Performing', 'Photos']) + f"""
    <section class="section">
      <div class="container">
{gallery_html()}
      </div>
    </section>
"""


# ===================== PERFORMING: SINGING =====================
PERFORM_SINGING = page_head("Performing · Singing", "Singing",
    "Soprano with a 3+ octave range &mdash; a voice the press has called &ldquo;the voice of a nightingale.&rdquo;",
    ['<a href="index.html">Home</a>', '<a href="performances.html">Performing</a>', 'Singing']) + """
    <section class="section">
      <div class="container grid grid--sidebar">
        <div class="reveal">
          <p class="lead">From cabaret and concert to musical theater and opera, Jennifer brings twenty years of professional stage experience to every performance. She has sung leading roles in regional theaters, on national tours and aboard cruise ships, and performs solo cabaret programs for concerts, benefits, churches and community events across the country.</p>
          <p>Her solo album <em>&ldquo;Traveling This World&rdquo;</em> showcases the warmth and range that have earned praise from <em>The Des Moines Register</em>, <em>The Arizona Republic</em> and beyond.</p>
          <div class="resume-tabs" style="margin-top:1.4rem">
            <a class="btn btn--sm" href="resume.html">See full resume</a>
            <a class="btn btn--sm btn--ghost" href="photos.html">Photo gallery</a>
            <a class="btn btn--sm btn--ghost" href="media.html">Recordings &amp; press</a>
          </div>
        </div>
        <aside class="reveal">
          <div class="card">
            <h3>Book Jennifer to sing</h3>
            <p style="font-size:.95rem;color:var(--muted)">Concerts &middot; cabaret &middot; benefits &middot; church &amp; community events.</p>
            <a class="btn btn--sm" href="contact.html" style="margin-top:.6rem">Check availability</a>
          </div>
        </aside>
      </div>
    </section>
""" + cta_band()


# ===================== PERFORMING: ACTING =====================
PERFORM_ACTING = page_head("Performing · Acting", "Acting",
    "Stage, film and commercial work spanning 30+ years and stages in 46 of the 50 states.",
    ['<a href="index.html">Home</a>', '<a href="performances.html">Performing</a>', 'Acting']) + """
    <section class="section">
      <div class="container grid grid--sidebar">
        <div class="reveal">
          <p class="lead">Jennifer has played leading roles in regional and New York theater, film and national commercials &mdash; from Johanna in <em>Sweeney Todd</em> and Grace Farrell in <em>Annie</em> to lead and supporting roles in independent film. Trained at Luther College and New York's Creative Acting Studio, she is equally at home on camera and on stage.</p>
          <p>Browse headshots and production photography from across her career, or view the full credits on her resume.</p>
          <div class="resume-tabs" style="margin-top:1.4rem">
            <a class="btn btn--sm" href="photos.html">Headshots &amp; show photos</a>
            <a class="btn btn--sm btn--ghost" href="resume.html">See full resume</a>
          </div>
        </div>
        <aside class="reveal">
          <div class="card">
            <h3>Casting &amp; booking</h3>
            <p style="font-size:.95rem;color:var(--muted)">Theater &middot; film &middot; commercial &middot; voice-over.</p>
            <a class="btn btn--sm" href="contact.html" style="margin-top:.6rem">Get in touch</a>
          </div>
        </aside>
      </div>
    </section>
""" + cta_band()


# ===================== PERFORMING: CHOREOGRAPHY =====================
PERFORM_CHOREOGRAPHY = page_head("Performing · Choreography", "Choreography",
    "Show choreography, combat and dance staging for theater, opera and competitive choirs.",
    ['<a href="index.html">Home</a>', '<a href="performances.html">Performing</a>', 'Choreography']) + f"""
    <section class="section">
      <div class="container">
        <p class="lead reveal">A retired professional dancer and dance captain, Jennifer has choreographed musicals, combat scenes and competitive swing choirs across the Midwest, New York and beyond.</p>
        <div class="reveal" style="margin-top:1.4rem">
{credits_table('Selected Choreography Credits', _CHOREO)}
        </div>
        <p class="note reveal" style="margin-top:1.5rem">For dance and dance-captain credits, see the <a href="resume.html#choreo">full resume</a>. Interested in choreography for your production? <a href="contact.html">Get in touch</a>.</p>
      </div>
    </section>
""" + cta_band()


# ===================== PERFORMING: EMCEE / SPEAKER =====================
# Two distinct roles on one page:
#   Emcee  = host/entertainer for fun events (galas, benefits, pageants...)
#   Speaker = keynote / educator role (talks, seminars, conferences...)
# Add events as (date, event, location).
_EMCEE_EVENTS = [
    ("June 27, 2026", "Mitzvah", "DoubleTree by Hilton"),
    ("June 13, 2026", "Mitzvah", "Embassy Suites, Destiny USA"),
    ("June 6, 2026", "Mitzvah", "Marriott Syracuse Downtown"),
    ("Feb 7, 2026", "Mitzvah", "Drumlins"),
    ("Nov 15, 2025", "Mitzvah", "Traditions at the Links"),
    ("Nov 1, 2025", "Wedding", "Traditions at the Links"),
    ("Oct 25, 2025", "Mitzvah", "Embassy Suites, Destiny USA"),
    ("Sept 26, 2025", "Wedding", "Traditions at the Links"),
    ("Sept 20, 2025", "Wedding", "Heritage Hill Brewhouse"),
    ("Aug 9, 2025", "Wedding", "Wolf Oak Acres"),
    ("June 7, 2025", "Bar Mitzvah", "Onondaga Country Club"),
    ("Jan 4, 2025", "Mitzvah", "Drumlin's"),
    ("Dec 7, 2024", "Christmas Party", "Syracuse Corvette Club"),
    ("Nov 23, 2024", "Corporate Party", "Turning Stone Resort"),
    ("Oct 26, 2024", "Wedding", "Clay, NY (Halloween wedding reception)"),
    ("Oct 19, 2024", "Bat Mitzvah", "Drumlin's"),
    ("Oct 12, 2024", "Wedding", "Embassy Suites, Destiny USA"),
    ("Sept 19, 2024", "Wedding", "Tricolla Farms"),
    ("Aug 23, 2024", "Wedding", "Traditions at the Links"),
    ("June 22, 2024", "Wedding", "Traditions at the Links"),
    ("May 4, 2024", "Mitzvah", "Embassy Suites, Destiny USA"),
    ("Mar 9, 2024", "Mitzvah", "Sheraton Syracuse University"),
    ("Feb 17, 2024", "Mitzvah", "Breezes"),
    ("Dec 23, 2023", "Mitzvah", "Temple Beth Sholom"),
    ("Dec 9, 2023", "Christmas Party", "Syracuse Corvette Club"),
    ("Nov 11, 2023", "Anniversary Event", "The Temple &mdash; 150th Anniversary"),
    ("Oct 21, 2023", "Wedding", "Traditions at the Links"),
    ("Oct 8, 2023", "Wedding", "Arrowhead Lodge"),
    ("Sept 23, 2023", "Wedding", "Traditions at the Links"),
    ("Sept 2, 2023", "Wedding", "Woods Valley"),
    ("Aug 19, 2023", "Pool Party", "Private pool/housewarming party"),
    ("July 16, 2023", "Wedding", "Syracuse Zoo"),
    ("July 8, 2023", "Wedding", "Dinosaur BBQ"),
    ("June 24, 2023", "Mitzvah", "Drumlin's"),
    ("May 20, 2023", "Wedding", "Jake's Grub &amp; Grog"),
    ("March 25, 2023", "Mitzvah", "Embassy Suites, Destiny USA"),
    ("March 18, 2023", "Mitzvah", "The Temple"),
    ("Dec 25, 2022", "Christmas Party", "Greystone"),
    ("Dec 2, 2022", "Christmas Party", "Syracuse Corvette Club"),
    ("Nov 5, 2022", "Mitzvah", "Traditions at the Links"),
    ("Oct 22, 2022", "Wedding", "Chantelle Marie Lakehouse"),
    ("Oct 8, 2022", "Wedding", "Drumlin's"),
    ("Oct 8, 2022", "Mitzvah", "The Temple"),
    ("Oct 1, 2022", "Wedding", "Mirabeau Farm"),
    ("Sept 24, 2022", "Bat Mitzvah", "Sky Armory"),
    ("Sept 17, 2022", "Wedding", "Timber Banks Golf Resort"),
    ("Aug 26, 2022", "Wedding", "Heritage Farm"),
    ("Aug 21, 2022", "Wedding", "Private family barn"),
    ("Aug 20, 2022", "Wedding", "Copper Top Tavern"),
    ("Aug 13, 2022", "Wedding", "Lakeshore Yacht Club"),
    ("July 2, 2022", "Wedding", "Mirabeau Farm"),
    ("Jun 5, 2022", "Bat Mitzvah", "Ithaca Farmers Market"),
    ("May 29, 2022", "Bat Mitzvah", "Private home, Manlius"),
    ("May 7, 2022", "Bat Mitzvah", "Lemongrass"),
    ("Jan 16, 2022", "Wedding", "Alexandria's, Oswego"),
    ("Jan 15, 2022", "Wedding", "Tailwater Lodge"),
    ("Dec 4, 2021", "Christmas Party", "Syracuse Corvette Club"),
    ("Nov 13, 2021", "Wedding", "Greystone"),
    ("Oct 23, 2021", "Wedding", "Greystone"),
    ("Oct 16, 2021", "Mitzvah", "Sheraton Syracuse University"),
    ("Oct 9, 2021", "Wedding", "Collaco Winery"),
    ("Oct 9, 2021", "Wedding", "Greystone"),
    ("Oct 2, 2021", "Bat Mitzvah", "Embassy Suites, Destiny USA"),
    ("Sept 25, 2021", "Wedding", "Greystone"),
    ("Sept 19, 2021", "Wedding", "Greystone"),
    ("Sept 12, 2021", "Wedding", "Arrowhead Lodge"),
    ("Sept 5, 2021", "Wedding", "Lafayette Hotel, Buffalo"),
    ("Sept 4, 2021", "Wedding", "Traditions at the Links"),
    ("August 28, 2021", "Wedding", "MKJ Farm"),
    ("Aug 21, 2021", "Wedding", "Greystone"),
    ("July 11, 2021", "Wedding", "Private home, Central Square NY"),
    ("July 4, 2021", "Wedding", "Traditions at the Links"),
    ("May 29, 2021", "Wedding", "Greystone"),
]
_SPEAKER_EVENTS = [
    # ("Month DD, YYYY", "Talk / topic", "Venue, City, ST"),
]

def _event_list_html(events, empty_msg):
    if not events:
        return f'          <p class="note">{empty_msg}</p>'
    items = "\n".join(
        '            <li><span class="time">%s</span><div><strong>%s</strong><br>%s</div></li>' % e
        for e in events
    )
    return f'          <ul class="timeline">\n{items}\n          </ul>'

def _events_by_year_html(events, empty_msg):
    """Render (date, type, venue) events grouped under year sub-headings.
    Assumes events are pre-sorted newest-first. The per-row date drops the
    year since it's shown as the group heading."""
    if not events:
        return f'          <p class="note">{empty_msg}</p>'
    from collections import OrderedDict
    groups = OrderedDict()
    for date, typ, venue in events:
        year = date.rsplit(",", 1)[-1].strip()
        short = date.rsplit(",", 1)[0].strip()
        groups.setdefault(year, []).append((short, typ, venue))
    blocks = []
    for year, evs in groups.items():
        rows = "\n".join(
            '            <li><span class="time">%s</span><div><strong>%s</strong><br>%s</div></li>' % e
            for e in evs
        )
        blocks.append(
            f'          <h4 class="event-year" style="margin:1.6rem 0 .5rem;color:var(--gold)">{year}</h4>\n'
            f'          <ul class="timeline">\n{rows}\n          </ul>'
        )
    return "\n".join(blocks)

_EMCEE_EMPTY = 'Emcee &amp; hosting dates will be listed here soon &mdash; check back, or <a href="contact.html">get in touch</a> to book Jennifer for your event.'
_SPEAKER_EMPTY = 'Speaking engagements will be listed here soon &mdash; or <a href="contact.html">get in touch</a> to book Jennifer for your conference or event.'
_EMCEE_LIST = _events_by_year_html(_EMCEE_EVENTS, _EMCEE_EMPTY)
_SPEAKER_LIST = _event_list_html(_SPEAKER_EVENTS, _SPEAKER_EMPTY)

PERFORM_EMCEE = page_head("Performing · Emcee &amp; Speaker", "Emcee &amp; Speaker",
    "Two roles, one stage presence &mdash; the charismatic host of your event, and the keynote speaker who teaches and inspires.",
    ['<a href="index.html">Home</a>', '<a href="performances.html">Performing</a>', 'Emcee &amp; Speaker']) + f"""
    <section class="section">
      <div class="container">
        <div class="resume-tabs reveal">
          <a class="btn btn--sm" href="#emcee">Emcee / Host</a>
          <a class="btn btn--sm btn--ghost" href="#speaker">Keynote Speaker</a>
        </div>
      </div>
    </section>

    <section class="section" id="emcee" style="padding-top:0">
      <div class="container grid grid--sidebar">
        <div class="reveal">
          <p class="eyebrow">Emcee / Host</p>
          <h2 style="margin-top:.2rem">Host of your event</h2>
          <p class="lead">With decades on stage and a natural ease with a live audience, Jennifer is a confident, charismatic host for weddings, bar &amp; bat mitzvahs, holiday and corporate parties, and community celebrations &mdash; keeping the energy up, the program moving and the room engaged. Since 2021 she has emceed {len(_EMCEE_EVENTS)}+ events across Central New York in partnership with The Great Music Company.</p>

          <figure style="margin:1.6rem 0">
            <img src="assets/img/emcee/emcee-hosting.jpg" alt="Jennifer Brown emceeing an event, microphone in hand, on the dance floor of a ballroom" style="width:100%;border-radius:12px;box-shadow:var(--shadow-md)">
          </figure>

          <h3 style="margin-top:1.8rem">Events Jennifer has emceed</h3>
{_EMCEE_LIST}
        </div>
        <aside class="reveal">
          <div class="card">
            <h3>Book Jennifer to host</h3>
            <p style="font-size:.95rem;color:var(--muted)">Galas &middot; benefits &middot; pageants &middot; award nights &middot; community events.</p>
            <a class="btn btn--sm" href="contact.html" style="margin-top:.6rem">Check availability</a>
          </div>
        </aside>
      </div>
    </section>

    <section class="section" id="speaker" style="padding-top:0">
      <div class="container grid grid--sidebar">
        <div class="reveal">
          <p class="eyebrow">Keynote Speaker</p>
          <h2 style="margin-top:.2rem">Speaker &amp; educator</h2>
          <p class="lead">As a keynote speaker, Jennifer steps into her educator role &mdash; sharing what she has learned across performance, teaching and wellness to inform, encourage and equip an audience. Engaging, practical and warm, her talks are tailored to your group and occasion.</p>

          <figure style="margin:1.6rem 0">
            <img src="assets/img/emcee/speaker-main.jpg" alt="Jennifer Brown speaking, arms wide open and animated, presenting to a group" style="width:100%;border-radius:12px;box-shadow:var(--shadow-md)">
          </figure>

          <h3 style="margin-top:1.8rem">Speaking engagements</h3>
{_SPEAKER_LIST}

          <h3 style="margin-top:2rem">More from the podium</h3>
          <p class="note" style="margin-bottom:1rem">Moments from Jennifer's wellness talks and keynotes. Tap any image to view it full size.</p>
          <div class="gallery">
            <a href="assets/img/emcee/speaker-cny-1.jpg" data-lightbox data-caption="Jennifer Brown presenting a wellness talk"><img src="assets/img/emcee/speaker-cny-1.jpg" alt="Jennifer Brown addressing the room during a wellness talk" loading="lazy"></a>
            <a href="assets/img/emcee/speaker-cny-2.jpg" data-lightbox data-caption="Jennifer Brown, mid-gesture during a talk"><img src="assets/img/emcee/speaker-cny-2.jpg" alt="Jennifer Brown engaged and gesturing during a talk" loading="lazy"></a>
            <a href="assets/img/emcee/speaker-cny-3.jpg" data-lightbox data-caption="Jennifer Brown speaking"><img src="assets/img/emcee/speaker-cny-3.jpg" alt="Jennifer Brown with a warm expression while speaking" loading="lazy"></a>
            <a href="assets/img/emcee/speaker-sitrin-1.jpg" data-lightbox data-caption="Jennifer Brown delivering a keynote to a larger audience"><img src="assets/img/emcee/speaker-sitrin-1.jpg" alt="Jennifer Brown delivering a keynote presentation" loading="lazy"></a>
            <a href="assets/img/emcee/speaker-sitrin-2.jpg" data-lightbox data-caption="Jennifer Brown speaking to a group"><img src="assets/img/emcee/speaker-sitrin-2.jpg" alt="Jennifer Brown speaking to a seated audience" loading="lazy"></a>
          </div>
        </div>
        <aside class="reveal">
          <div class="card">
            <h3>Book Jennifer to speak</h3>
            <p style="font-size:.95rem;color:var(--muted)">Keynotes &middot; conferences &middot; seminars &middot; workshops &middot; panels.</p>
            <a class="btn btn--sm" href="contact.html" style="margin-top:.6rem">Check availability</a>
          </div>
        </aside>
      </div>
    </section>
""" + cta_band()


# ===================== PERFORMING: MEDIA / PRESS =====================
MEDIA = page_head("Performing · Media", "Media &amp; Press",
    "Reviews, voice-over and commercial reels, film, and recorded music.",
    ['<a href="index.html">Home</a>', 'Performing', 'Media &amp; Press']) + """
    <section class="section">
      <div class="container">
        <p class="eyebrow reveal">Press</p>
        <div class="press-grid reveal" style="margin-bottom:2.5rem">
          <div class="pullquote">
            <p>&ldquo;The knock-'em-dead role here is Jennifer as Grace&hellip; Her fine voice and control of mercurial mood shifts were impressive.&rdquo;</p>
            <cite>&mdash; The Arizona Republic &middot; <em>Annie</em></cite>
          </div>
          <div class="pullquote">
            <p>&ldquo;&hellip;the voice of a nightingale&hellip;&rdquo;</p>
            <cite>&mdash; The Leaf Chronicle, Clarksville, TN &middot; <em>Phases of Love</em></cite>
          </div>
          <div class="pullquote">
            <p>&ldquo;Jennifer's eloquent voice&hellip; is a highlight of the evening.&rdquo;</p>
            <cite>&mdash; The Des Moines Register &middot; <em>The Sound of Music</em></cite>
          </div>
        </div>

        <div class="grid grid--sidebar">
          <div class="reveal">
            <div class="grid grid--2">
              <div class="card">
                <h3>Voice Over</h3>
                <ul class="linklist">
                  <li>Voice Over Demo &mdash; On the Air Studios</li>
                  <li>Vanities radio spot</li>
                  <li>Romance / Romance radio spot</li>
                </ul>
              </div>
              <div class="card">
                <h3>Film</h3>
                <ul class="linklist">
                  <li>The Ghost of Lucy Frost</li>
                  <li>Black Cougar</li>
                  <li>Where'd He Go?</li>
                  <li>Paper Trails, the Extra</li>
                </ul>
              </div>
            </div>
            <div class="card" style="margin-top:1.4rem">
              <h3>Commercials</h3>
              <ul class="linklist" style="columns:2;column-gap:2rem">
                <li>Corning Museum of Glass</li>
                <li>Fast Track Woman #1 &amp; #2</li>
                <li>NY Jets Training Camp '09 &mdash; Don't Cross a Jet</li>
                <li>First National Bank of Dryden &mdash; Equity</li>
                <li>FNBD &mdash; Business &amp; Biz Checking</li>
                <li>FNBD &mdash; Switching &amp; Community</li>
                <li>FNBD &mdash; Safety &amp; Security</li>
                <li>FNBD &mdash; Familiarity &amp; Availability</li>
              </ul>
            </div>
          </div>
          <aside class="reveal">
            <div class="card">
              <img src="assets/img/home/cd_cover_small.jpg" alt="Traveling This World album cover" style="border-radius:8px;margin-bottom:1rem">
              <h3>Vocal &mdash; &ldquo;Traveling This World&rdquo;</h3>
              <p style="font-size:.95rem">&ldquo;&hellip;the voice of a nightingale&rdquo; only begins to describe the beautiful tones and vocal stylings heard in each masterfully performed piece of Jennifer's solo CD.</p>
              <a class="btn btn--sm" href="contact.html">Ask about the CD</a>
            </div>
          </aside>
        </div>
      </div>
    </section>
"""


# ===================== CONTACT =====================
CONTACT = page_head("Get in touch", "Contact &amp; Studio Location",
    "Questions about lessons, coaching, or a performance booking? Send a note &mdash; Jennifer will get right back to you.",
    ['<a href="index.html">Home</a>', 'Contact']) + f"""
    <section class="section">
      <div class="container contact-grid">
        <div class="reveal">
          <form id="contact-form" novalidate>
            <div class="field">
              <label for="name">Name</label>
              <input type="text" id="name" name="name" required>
            </div>
            <div class="field">
              <label for="email">Email</label>
              <input type="email" id="email" name="email" required>
            </div>
            <div class="field">
              <label for="subject">I'm interested in</label>
              <select id="subject" name="subject">
                <option>Voice / piano / acting / ballet lessons</option>
                <option>Personal training, nutrition or healthy aging</option>
                <option>Booking a performance, emcee or speaker</option>
                <option>Workshops &amp; seminars</option>
                <option>Something else</option>
              </select>
            </div>
            <div class="field">
              <label for="message">Message</label>
              <textarea id="message" name="message" required></textarea>
            </div>
            <button class="btn" type="submit">Send message</button>
            <p class="form-note" id="form-status">This form opens your email app. Prefer to write directly? Email <a href="mailto:{EMAIL}">{EMAIL}</a>.</p>
          </form>
        </div>
        <aside class="reveal">
          <div class="card" style="margin-bottom:1.4rem">
            <h3>Reach Jennifer</h3>
            <ul class="contact-info">
              <li><span class="ico">&#9742;</span><div><strong>Phone</strong><br><a href="tel:+16465268312">{PHONE}</a></div></li>
              <li><span class="ico">&#9993;</span><div><strong>Email</strong><br><a href="mailto:{EMAIL}">{EMAIL}</a></div></li>
              <li><span class="ico">&#9826;</span><div><strong>Facebook</strong><br><a href="{FACEBOOK}" target="_blank" rel="noopener">Jennifer Brown</a></div></li>
              <li><span class="ico">&#9826;</span><div><strong>Instagram</strong><br><a href="{INSTAGRAM}" target="_blank" rel="noopener">{INSTAGRAM_HANDLE}</a></div></li>
            </ul>
          </div>
          <div class="card">
            <h3>Studio &mdash; Rome, NY</h3>
            <p>A bright, welcoming studio very near Route 26 and Stokes Road. Please contact Jennifer for the specific address. Lessons and coaching are also available online.</p>
          </div>
        </aside>
      </div>
    </section>
"""


# ============================ BUILD ============================
if __name__ == "__main__":
    page("index.html", "Jennifer Brown", "Jennifer Brown — performer, voice/piano/acting teacher and fitness coach in Rome, New York. Lessons, classes and live performance.", HOME, "home")
    page("bio.html", "Bio", "The story of Jennifer Brown — from Iowa cornfields to stages in 46 states, and into the studio as a teacher and coach.", BIO, "bio")
    page("performances.html", "Performance History", "A selection of Jennifer Brown's concerts, productions and appearances across the country.", PERFORMANCES, "performing")
    page("resume.html", "Resume", "Acting, performance and choreography resume for Jennifer Brown — actor, singer, dancer, soprano.", RESUME, "performing")
    page("photos.html", "Photo Gallery", "Headshots and production photography from Jennifer Brown's performing career.", PHOTOS, "performing")
    page("media.html", "Media & Press", "Press quotes, voice-over and commercial reels, film and recorded music from Jennifer Brown.", MEDIA, "performing")
    page("perform-singing.html", "Singing", "Jennifer Brown — soprano, cabaret, concert and musical theater singer available for concerts, benefits and events.", PERFORM_SINGING, "performing")
    page("perform-acting.html", "Acting", "Jennifer Brown — stage, film and commercial actor. Headshots, show photos and full performance resume.", PERFORM_ACTING, "performing")
    page("perform-choreography.html", "Choreography", "Show choreography, combat staging and dance direction by Jennifer Brown for theater, opera and competitive choirs.", PERFORM_CHOREOGRAPHY, "performing")
    page("perform-emcee.html", "Emcee & Speaker", "Book Jennifer Brown to emcee or host your gala, benefit, pageant or community event.", PERFORM_EMCEE, "performing")
    page("lessons-singing.html", "Singing Lessons", "Private voice lessons for all ages and abilities with Jennifer Brown in Rome, NY.", LESSONS_SINGING, "teaching")
    page("lessons-piano.html", "Piano Lessons", "Private piano lessons, one-on-one or with a friend, for children and adults.", LESSONS_PIANO, "teaching")
    page("lessons-acting.html", "Acting Lessons", "Year-round private acting coaching — auditions, scene study, on-camera and more.", LESSONS_ACTING, "teaching")
    page("lessons-ballet.html", "Ballet Lessons", "Private ballet lessons for children and adults with retired professional dancer Jennifer Brown in Rome, NY.", LESSONS_BALLET, "teaching")
    page("lessons-workshops.html", "Workshops & Seminars", "Second Saturdays group workshops for acting and singing, plus the Business of the Business seminar.", LESSONS_WORKSHOPS, "teaching")
    page("personal-training.html", "Personal Training", "Certified in-home personal training and sports nutrition tailored to your goals.", PERSONAL_TRAINING, "fitness")
    page("nutrition.html", "Behavioral Nutrition", "Sustainable, grace-filled nutrition coaching with Jennifer Brown — behavioral changes for a lifestyle, not a diet, in person in Rome, NY or online.", NUTRITION, "fitness")
    page("age-well.html", "Age Well & Vibrantly", "Strength, balance and mobility coaching for healthy, vibrant aging — all ages, in person or online.", AGE_WELL, "fitness")
    page("contact.html", "Contact", "Contact Jennifer Brown about lessons, coaching or performance bookings in Rome, NY.", CONTACT, "contact")

    # Custom domain for GitHub Pages (kept on every build so it's never lost)
    with open(os.path.join(ROOT, "CNAME"), "w") as f:
        f.write("jenniferbrownstudio.fit\n")

    print("\nDone — 18 pages generated.")
