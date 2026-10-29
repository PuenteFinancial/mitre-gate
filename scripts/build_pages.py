"""Build every page of the Mitre site: shared head, island header and footer around each page's main.

Run from anywhere:  python3 scripts/build_pages.py
Every HTML page is generated; edit this file (and v2/site.css), never the HTML. See DESIGN.md.
"""
import hashlib, pathlib, re, sys

ROOT = pathlib.Path(sys.argv[1]) if len(sys.argv) > 1 else pathlib.Path(__file__).resolve().parent.parent
def ver(rel):
    return hashlib.sha1((ROOT / rel).read_bytes()).hexdigest()[:8]

TABS = [("/", "Home"), ("/services/", "Services"), ("/financing/", "Financing"), ("/industries/", "Industries"), ("/careers/", "Careers")]
INDUSTRIES = [("/consumer-goods/", "Consumer Goods"), ("/wholesale-distribution/", "Wholesale &amp; Distribution"),
              ("/logistics/", "Logistics"), ("/supply-chain/", "Supply Chain"), ("/specialty-finance/", "Specialty Finance"),
              ("/smb/", "SMB")]
IND_PATHS = {p for p, _ in INDUSTRIES}
MAIL = "info@mitregate.com"


def cur(href, path):
    return ' aria-current="page"' if href == path else ""


def head(path, title, desc, noindex):
    robots = '\n  <meta name="robots" content="noindex" />' if noindex else ""
    d = f'\n  <meta name="description" content="{desc}" />\n  <meta property="og:description" content="{desc}" />' if desc else ""
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />{robots}
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>{title}</title>
  <link rel="canonical" href="https://mitregate.com{path}" />{d}
  <meta property="og:type" content="website" />
  <meta property="og:site_name" content="Mitre" />
  <meta property="og:title" content="{title}" />
  <meta property="og:url" content="https://mitregate.com{path}" />
  <meta name="twitter:card" content="summary" />
  <link rel="icon" type="image/svg+xml" href="/favicon.svg?v={ver('favicon.svg')}" />
  <link rel="icon" type="image/png" sizes="32x32" href="/favicon-32.png?v={ver('favicon-32.png')}" />
  <link rel="apple-touch-icon" href="/apple-touch-icon.png?v={ver('apple-touch-icon.png')}" />
  <link rel="preconnect" href="https://fonts.googleapis.com" />
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
  <link href="https://fonts.googleapis.com/css2?family=Manrope:wght@400;600;700&amp;family=Red+Hat+Mono:wght@500&amp;family=Spectral:wght@500&amp;display=swap" rel="stylesheet" />
  <link rel="stylesheet" href="/v2/site.css?v={ver('v2/site.css')}" />
</head>
<body>
"""


def header(path):
    in_ind = path in IND_PATHS or path == "/industries/"
    links = []
    for href, label in TABS:
        if href == "/industries/":
            subs = "\n".join(f'              <li><a href="{h}"{cur(h, path)}>{l}</a></li>' for h, l in INDUSTRIES)
            cls = "island__parent is-current" if in_ind else "island__parent"
            links.append(f"""          <div class="island__group">
            <a class="{cls}" href="{href}"{cur(href, path)}>{label}<span class="island__chev" aria-hidden="true">▾</span></a>
            <div class="island__drop">
              <ul class="island__panel" aria-label="Industries">
{subs}
              </ul>
            </div>
          </div>""")
        else:
            links.append(f'          <a href="{href}"{cur(href, path)}>{label}</a>')
    mobile = []
    for href, label in TABS:
        mobile.append(f'    <a href="{href}"{cur(href, path)}>{label}</a>')
        if href == "/industries/":
            subs = "\n".join(f'      <a href="{h}"{cur(h, path)}>{l}</a>' for h, l in INDUSTRIES)
            mobile.append(f'    <div class="mmenu__sub">\n{subs}\n    </div>')
    mobile.append(f'    <a href="/contact/"{cur("/contact/", path)}>Contact</a>')
    return f"""  <header class="hdr" id="nav">
    <div class="hdr__in">
      <div class="island island--nav">
        <button class="island__menu" id="navMenu" aria-label="Menu" aria-expanded="false" aria-controls="mobileMenu">≡</button>
        <a class="island__brand" href="/"><img src="/public/brand/mitre-wordmark-blue.svg" alt="Mitre" width="101" height="24" /></a>
        <nav class="island__links" aria-label="Primary">
{chr(10).join(links)}
        </nav>
      </div>
      <a class="island island--cta" href="/contact/"{cur("/contact/", path)}>Contact <span aria-hidden="true">→</span></a>
    </div>
  </header>
  <nav class="mmenu" id="mobileMenu" aria-label="Menu" aria-hidden="true">
{chr(10).join(mobile)}
  </nav>
"""


def footer():
    nav = "\n".join(f'          <a href="{h}">{l}</a>' for h, l in TABS + [("/contact/", "Contact")])
    return f"""
  <footer class="foot">
    <div class="wrap">
      <div class="foot__top">
        <p class="foot__tag">Level up through AI transformation.</p>
        <nav class="foot__nav" aria-label="Footer">
{nav}
        </nav>
        <div class="foot__help">
          <h3>How can we help?</h3>
          <p>Tell us what you're working on. A real person reads every note.</p>
          <a class="btn btn--primary" href="/contact/">Contact <span aria-hidden="true">→</span></a>
        </div>
      </div>
      <div class="foot__bot">
        <a href="/"><img src="/public/brand/mitre-wordmark-blue.svg" alt="Mitre" width="101" height="24" /></a>
        <span>© 2026 Mitre Global. All rights reserved.</span>
        <a href="mailto:{MAIL}">{MAIL}</a>
      </div>
    </div>
  </footer>
  <script src="/v2/site.js?v={ver('v2/site.js')}"></script>
</body>
</html>
"""


def ph(kind, label, extra=""):
    return f'<div class="ph ph--{kind}{(" " + extra) if extra else ""}" role="img" aria-label="{label}"><span class="ph__label">{label}</span></div>'


def pills(label="Industries"):
    links = "\n".join(f'          <a href="{h}">{l}</a>' for h, l in INDUSTRIES)
    return f"""      <nav class="pills" aria-label="{label}">
        <div class="pills__in">
          <span class="pills__k">{label}</span>
{links}
        </div>
      </nav>"""


# ---------------- homepage ----------------
SLIDE_TONES = ["", "ph--g", "ph--dark", "ph--mix", "", "ph--g"]
slides = []
SLIDE_ALT = {
    "/consumer-goods/": "Two models in oversized hoodies against a blue studio backdrop",
    "/wholesale-distribution/": "A long, skylit industrial hall with blue steel columns",
    "/logistics/": "A fully loaded container ship at sea",
    "/supply-chain/": "Close-up of tubing and fittings on a production line",
    "/specialty-finance/": "A glass skyscraper against a blue sky",
    "/smb/": "A small storefront with a green awning on a city street",
}
# carousel order differs from the nav order: Specialty Finance and Logistics trade places
CAROUSEL = [INDUSTRIES[k] for k in (0, 1, 4, 3, 2, 5)]
for i, (tone, (href, industry)) in enumerate(zip(SLIDE_TONES, CAROUSEL), 1):
    slug = href.strip("/")
    v = ver("assets/carousel/" + slug + ".jpg")
    img = f'<img src="/assets/carousel/{slug}.jpg?v={v}" alt="{SLIDE_ALT[href]}" width="733" height="1100" loading="{"eager" if i < 4 else "lazy"}" decoding="async" />'
    slides.append(f"""          <div class="slide" role="group" aria-roledescription="slide" aria-label="{i} of {len(SLIDE_TONES)}">
            <div class="slide__media">{img}</div>
            <span class="slide__chip">{industry}</span>
            <div class="slide__card">
              <h2 class="slide__title">Title placeholder</h2>
              <p class="slide__desc">Short description placeholder for this industry.</p>
              <a class="btn btn--primary btn--sm" href="#" data-placeholder="link">Learn more <span aria-hidden="true">→</span></a>
            </div>
          </div>""")

LOGOS = [("smuckers.svg", "Smucker's", "logo--badge logo--light"), ("vivint.png", "Vivint", ""), ("savi.svg", "Savi", "logo--tall"),
         ("boostly.svg", "Boostly", ""), ("goldman-sachs.svg", "Goldman Sachs", "logo--badge"),
         ("capital-one.svg", "Capital One", "logo--tall"), ("amazon.svg", "Amazon", ""), ("home-depot.svg", "The Home Depot", "logo--badge")]
logos = "\n".join(f'              <img src="/assets/logos/{f}" alt="{a}"{f" class={chr(34)}{c}{chr(34)}" if c else ""} loading="lazy" />' for f, a, c in LOGOS)

logos_dup = re.sub(r' alt="[^"]*"', ' alt=""', logos)

OFFER = [
    ("01", "Strategy", "Data Led Strategy",
     "We interview the people who run each function and measure where time and money go. Every opportunity is scored on value against cost, so your roadmap is ranked by return and priced by the engineers who would build it.",
     "Animation: opportunities ranked by return"),
    ("02", "Implementation", "Embedded Implementation",
     "We build the data foundation first, then the agents and applications on top of it, all reading from one current model of your business.",
     "Animation: one Manifest under every agent"),
    ("03", "Performance", "Continual Performance Improvement",
     "Every system is measured against how the work ran before, and tested again with every change. It earns its place by beating that baseline.",
     "Animation: weekly scores against the baseline"),
]
cards = "\n".join(f"""        <article class="card">
          {ph("anim", anim, "ph--g" if n == "02" else "")}
          <div class="card__chip"><b>{n}</b><span>{chip}</span></div>
          <div class="card__panel">
            <h3>{title}</h3>
            <div class="card__more"><div>
              <p>{body}</p>
              <a class="btn btn--primary" href="/services/">Our Service <span aria-hidden="true">→</span></a>
            </div></div>
          </div>
        </article>""" for n, chip, title, body, anim in OFFER)

HOME_MAIN = f"""
  <main id="page">
    <section class="hero" aria-labelledby="hero-title">
      <div class="wrap">
        <p class="eyebrow">Welcome to Mitre Global</p>
        <h1 class="h-display" id="hero-title">AI implementation that drives real operational efficiency</h1>
      </div>
      <div class="wrap car" data-carousel role="region" aria-roledescription="carousel" aria-label="Featured stories">
        <div class="car__stage">
{chr(10).join(slides)}
        </div>
        <div class="car__ctrl">
          <button type="button" data-car-pause aria-label="Pause carousel">❚❚</button>
          <button type="button" data-car-prev aria-label="Previous slide">‹</button>
          <button type="button" data-car-next aria-label="Next slide">›</button>
        </div>
      </div>
      <div class="wrap">
{pills()}
      </div>
    </section>

    <section class="wrap promo" aria-labelledby="promo-title">
      <div class="promo__card">
        <div class="promo__bg" aria-hidden="true"></div>
        <h2 id="promo-title">The leading AI department for global commerce.</h2>
        <div>
          <p>Mitre engineers deploy alongside your organization to discover and rank where AI can create the largest measurable impact. We then architect and build the systems that realize&nbsp;it.</p>
          <a class="btn btn--light" href="/services/">Our services <span aria-hidden="true">→</span></a>
        </div>
        <div class="logos">
          <p class="logos__k">Experience working on diverse teams</p>
          <div class="logos__mask">
            <div class="logos__track">
              <div class="logos__row">
  {logos}
              </div>
              <div class="logos__row" aria-hidden="true">
  {logos_dup}
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>

    <section class="sec" id="offering" aria-labelledby="offer-title">
      <div class="wrap">
        <div class="sec__head">
          <div>
            <h2 class="h-section" id="offer-title">From strategy to systems that run.</h2>
            <p class="lede">We find where AI pays off, build the systems that capture it, and measure every one against how the work ran before.</p>
          </div>
          <a class="more" href="/services/">See our full service</a>
        </div>
        <div class="cards">
{cards}
        </div>
      </div>
    </section>

    <section class="feature" aria-labelledby="feature-title">
      <div class="wrap feature__in">
        <div>
          <p class="eyebrow">Trade Financing</p>
          <h2 class="h-section" id="feature-title">Payments and cash management that accelerate growth.</h2>
          <p class="lede">Growth stalls when cash is tied up in inventory and unpaid invoices. We help you fund purchases, pay suppliers on time and collect faster, with a clear view of your cash built into the systems you already run.</p>
          <a class="btn btn--primary" href="/financing/">Explore Financing <span aria-hidden="true">→</span></a>
        </div>
        {ph("anim", "Animation placeholder: Trade Financing", "ph--g feature__vis")}
      </div>
    </section>

    <section class="sec" aria-labelledby="promise-title">
      <div class="wrap split">
        {ph("photo", "Photo placeholder", "split__ph")}
        <div>
          <p class="eyebrow">Careers at Mitre</p>
          <h2 class="h-section" id="promise-title">Extreme ownership is the only qualification.</h2>
          <p class="lede">We're a small team that embeds with operators and owns the result, not just the deliverable. If you take responsibility before anyone asks you to, you'll fit right in.</p>
          <a class="btn btn--primary" href="/careers/">Explore Careers <span aria-hidden="true">→</span></a>
        </div>
      </div>
    </section>

    <section class="reach" id="contact" aria-labelledby="reach-title">
      <div class="wrap reach__in">
        <div class="reach__txt">
          <p class="eyebrow">Contact us</p>
          <h2 class="h-section" id="reach-title">Ready to put AI to work?</h2>
          <p class="lede">Tell us what you're working on. A real person reads every note.</p>
          <p class="reach__alt">Prefer email? <a class="reach__mail" href="mailto:{MAIL}">{MAIL}</a></p>
        </div>
        <form class="form" data-placeholder="form" novalidate>
          <div class="form__row">
            <label class="field"><span class="field__label">Name</span>
              <input class="field__input" name="name" autocomplete="name" required></label>
            <label class="field"><span class="field__label">Company</span>
              <input class="field__input" name="company" autocomplete="organization" required></label>
          </div>
          <label class="field"><span class="field__label">Work email</span>
            <input class="field__input" type="email" name="email" autocomplete="email" required></label>
          <label class="field"><span class="field__label">How can we help?</span>
            <textarea class="field__input field__input--area" name="message" rows="5" required></textarea></label>
          <div class="form__foot">
            <button class="btn btn--primary" type="submit">Send <span aria-hidden="true">→</span></button>
            <p class="form__status" role="status" aria-live="polite"></p>
          </div>
        </form>
      </div>
    </section>
  </main>
"""


def write(path, html):
    out = ROOT / path.strip("/") / "index.html" if path != "/" else ROOT / "index.html"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(html)


HOME_DESC = "Mitre embeds engineers in your business to find where AI creates value and build the systems that capture it. AI implementation that drives real operational efficiency."
write("/", head("/", "Mitre Global | AI implementation that drives real operational efficiency", HOME_DESC, False) + header("/") + HOME_MAIN + footer())

# ---------------- placeholder subpages ----------------
def subpage(path, eyebrow, h1, lede, extra="", banner=True, title=None):
    main = f"""
  <main id="page">
    <section class="phero">
      <div class="wrap">
        <p class="eyebrow">{eyebrow}</p>
        <h1 class="h-display">{h1}</h1>
        <p class="lede">{lede}</p>{extra}
      </div>
    </section>
    <section class="sec" style="padding-top:0">
      <div class="wrap">{ph("anim", "Page content coming soon", "phero__ph") if banner else ""}</div>
    </section>
  </main>
"""
    title = f"{title or eyebrow} | Mitre"
    write(path, head(path, title, "", True) + header(path) + main + footer())


subpage("/services/", "Services", "Services", "What we build with you, and how we work. This page is on its way.")
subpage("/financing/", "Financing", "Financing", "How we make the work easy to fund. This page is on its way.")
subpage("/industries/", "Industries", "Where we work.", "We embed with operators in six industries. Pick yours to see how we help.",
        extra="\n" + pills("Choose an industry"))
CAREERS_MAIN = f"""
  <main id="page">
    <section class="phero">
      <div class="wrap">
        <p class="eyebrow">Careers at Mitre</p>
        <h1 class="h-display">Extreme ownership is the only qualification.</h1>
        <p class="lede">We're a small team that embeds with operators and owns the result, not just the deliverable.</p>
      </div>
    </section>
    <section class="sec" style="padding-top:0" aria-labelledby="roles-title">
      <div class="wrap">
        <div class="roles">
          <div class="roles__card">
            <h2 class="roles__title" id="roles-title">Open roles</h2>
            <p class="roles__none">No open roles right now.</p>
            <p class="roles__txt">We're always glad to meet people who take responsibility before anyone asks. Tell us about yourself.</p>
            <a class="btn btn--primary" href="mailto:{MAIL}?subject=Careers%20at%20Mitre">Introduce yourself <span aria-hidden="true">→</span></a>
          </div>
        </div>
      </div>
    </section>
  </main>
"""
write("/careers/", head("/careers/", "Careers | Mitre", "", False) + header("/careers/") + CAREERS_MAIN + footer())
subpage("/contact/", "Contact", "Talk to us.", "Tell us what you're working on. A real person reads every note.",
        extra=f'\n        <a class="btn btn--primary" href="mailto:{MAIL}">Email {MAIL} <span aria-hidden="true">→</span></a>')
for p, label in INDUSTRIES:
    subpage(p, "Industries", label, f"How Mitre puts AI to work for {label}. This page is on its way.", title=label.replace("&amp;", "&"))
print("ok")
