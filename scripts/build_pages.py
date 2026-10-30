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


def contact_form():
    """The contact form (name, company, work email, message). Validates on the page; no backend yet."""
    return """        <form class="form" data-placeholder="form" novalidate>
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
        </form>"""


def reach(eyebrow, h2, lede):
    """Dark blue contact band with the contact form. One source for every page that ends with it."""
    return f"""    <section class="reach" id="contact" aria-labelledby="reach-title">
      <div class="wrap reach__in">
        <div class="reach__txt">
          <p class="eyebrow">{eyebrow}</p>
          <h2 class="h-section" id="reach-title">{h2}</h2>
          <p class="lede">{lede}</p>
          <p class="reach__alt">Prefer email? <a class="reach__mail" href="mailto:{MAIL}">{MAIL}</a></p>
        </div>
{contact_form()}
      </div>
    </section>"""


def home_reach():
    """The homepage "Ready to engage with Mitre?" band. Also closes every industry page."""
    return reach("Contact us", "Ready to engage with Mitre?", "Tell us what you're working on. A real person reads every note.")


# ---------------- industry copy ----------------
# Each industry supplies only its lead line, paragraph and five "Where we help" tags; the rest is shared.
IND_COPY = {
    "/consumer-goods/": (
        "More time on the brand, less on the back office.",
        "Consumer brands win on product, demand and margin. Behind that sits a heavy operational load: forecasting demand, managing inventory across channels, coordinating overseas suppliers and production runs, tracking landed costs, and reconciling sales from every marketplace and retailer. Mitre embeds with your team to take that work off your operators' plates, sharpen forecasting and inventory decisions, and give leadership a clear, current view of margin by product and channel.",
        ["Demand &amp; inventory planning", "Supplier &amp; production coordination", "Margin by product &amp; channel", "Landed cost tracking", "Marketplace &amp; retail reconciliation"]),
    "/wholesale-distribution/": (
        "Thin margins reward fast, accurate operations.",
        "Distributors win on volume at thin margins. Value comes from buying right, keeping the right stock in the right place, quoting and fulfilling orders quickly, and collecting on time. Much of that still runs on email, spreadsheets and manual order entry. Mitre works alongside your team to automate order intake and quoting, improve purchasing and replenishment decisions, and shorten the path from order to cash, so your people spend their time on customers and suppliers.",
        ["Order intake &amp; quoting", "Purchasing &amp; replenishment", "Order to cash", "Inventory placement", "Pricing &amp; margin"]),
    "/logistics/": (
        "Move more freight with the team you have.",
        "For 3PLs, freight forwarders and warehouse operators, every shipment generates documents, updates and exceptions. Quoting, booking, customs paperwork, tracking, billing and customer communication absorb hours that should go to growing accounts. Mitre embeds with your operations team to automate document handling and status updates, catch exceptions before your customers do, and tighten billing so accessorials don't slip through, letting you scale volume without scaling headcount.",
        ["Quoting &amp; booking", "Documents &amp; exceptions", "Billing &amp; customer updates", "Shipment tracking", "Customs paperwork"]),
    "/supply-chain/": (
        "See the whole chain, from supplier to shipment.",
        "Sourcing teams, manufacturers, and supply chain consultants and brokers create value by finding the right suppliers, negotiating cost, keeping production on schedule and managing risk across borders. That work depends on information scattered across supplier emails, purchase orders, quality reports and spreadsheets. Mitre works with your team to unify that data, automate supplier communication and PO tracking, and surface cost, lead time and risk signals early, so decisions are made with the full picture.",
        ["Supplier sourcing &amp; management", "PO &amp; production tracking", "Cost &amp; risk visibility", "Supplier communication", "Quality reporting"]),
    "/specialty-finance/": (
        "Underwrite faster. Monitor smarter.",
        "For factors, PO financiers and small business lenders, returns come down to how quickly and accurately you evaluate a deal, verify what stands behind it, and watch the book once it funds. Much of that still means collecting documents, spreading financials, verifying invoices and chasing collections by hand. Mitre embeds with your team to automate intake and verification, give underwriters richer data to decide on, and flag portfolio risk early, so you grow volume without adding risk or headcount.",
        ["Intake &amp; underwriting", "Invoice &amp; collateral verification", "Portfolio monitoring &amp; collections", "Document collection", "Financial spreading"]),
    "/smb/": (
        "Big-company capability, sized for your business.",
        "Small operators run every function with a lean team, and sales, operations, finance and customer service often sit with the same few people. Hours lost to manual work and disconnected tools come straight out of growth. Mitre works with owners and their teams to find where AI frees up the most time and money, then builds simple systems around how you already work, so you can stay focused on customers and the business itself.",
        ["Operations &amp; admin", "Finance &amp; reporting", "Customer communication", "Sales &amp; lead follow-up", "Tool consolidation"]),
}

# Homepage carousel: a short goal per industry; the card previews the start of that industry's paragraph
SLIDE_TITLE = {
    "/consumer-goods/": "Focus on your product",
    "/wholesale-distribution/": "Win on every order",
    "/logistics/": "Streamline your operation",
    "/supply-chain/": "Act with more insight",
    "/specialty-finance/": "Grow your book of business",
    "/smb/": "Do more with less",
}


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
              <h2 class="slide__title">{SLIDE_TITLE[href]}</h2>
              <p class="slide__desc">{IND_COPY[href][1]}</p>
              <a class="btn btn--primary btn--sm" href="{href}">Learn more <span aria-hidden="true">→</span></a>
            </div>
          </div>""")

LOGOS = [("smuckers.svg", "Smucker's", "logo--badge logo--light"), ("vivint.png", "Vivint", ""), ("savi.svg", "Savi", "logo--tall"),
         ("boostly.svg", "Boostly", ""), ("goldman-sachs.svg", "Goldman Sachs", "logo--badge"),
         ("capital-one.svg", "Capital One", "logo--tall"), ("amazon.svg", "Amazon", ""), ("home-depot.svg", "The Home Depot", "logo--badge")]
logos = "\n".join(f'              <img src="/assets/logos/{f}" alt="{a}"{f" class={chr(34)}{c}{chr(34)}" if c else ""} loading="lazy" />' for f, a, c in LOGOS)

logos_dup = re.sub(r' alt="[^"]*"', ' alt=""', logos)

OFFER = [
    ("01", "Assess", "Identify the opportunity",
     "We map where time and money go, rank every opportunity by its return, and agree on the outcomes we'll be measured by.",
     "Animation: opportunities ranked by return"),
    ("02", "Build", "Deploy within your team",
     "We unify your data, then embed with your team to build the agents, workflows and software in your proposal, and stay through adoption.",
     "Animation: agents and apps built on the data layer"),
    ("03", "Prove", "Measure the outcome",
     "Every system is measured against the outcomes agreed up front, with a regular scorecard of hours saved, costs cut and insight gained.",
     "Animation: scorecard against the baseline"),
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

def offering(industry=None):
    """The "Assess, build, prove." section. One source for the homepage and every industry page;
    on an industry page the services link names that industry."""
    more = f"See our full service for {industry}" if industry else "See our full service"
    return f"""    <section class="sec" id="offering" aria-labelledby="offer-title">
      <div class="wrap">
        <div class="sec__head">
          <div>
            <h2 class="h-section" id="offer-title">Assess, build, prove.</h2>
            <p class="lede">We find where AI pays off in your business, build the data pipelines and systems to capture it, and measure every result against agreed outcomes.</p>
          </div>
          <a class="more" href="/services/">{more}</a>
        </div>
        <div class="cards">
{cards}
        </div>
      </div>
    </section>"""


HOME_MAIN = f"""
  <main id="page">
    <section class="hero" aria-labelledby="hero-title">
      <div class="wrap">
        <p class="eyebrow">Welcome to Mitre Global</p>
        <h1 class="h-display" id="hero-title">AI implementation that drives <br class="br-wide" />operational and cash efficiency</h1>
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

{offering()}

    <section class="feature" aria-labelledby="feature-title">
      <div class="wrap feature__in">
        <div>
          <p class="eyebrow eyebrow--row">Trade Financing <span class="badge"><span class="badge__dot" aria-hidden="true"></span>Coming soon</span></p>
          <h2 class="h-section" id="feature-title">Payments and cash management that accelerate growth.</h2>
          <p class="lede">Growth stalls when cash is tied up in inventory and unpaid invoices. We help you fund purchases, pay suppliers on time and collect faster, with a clear view of your cash across all the systems you already run.</p>
          <a class="btn btn--primary" href="/financing/">Explore Financing <span aria-hidden="true">→</span></a>
        </div>
        {ph("anim", "Animation placeholder: Trade Financing", "ph--g feature__vis")}
      </div>
    </section>

    <section class="sec" aria-labelledby="promise-title">
      <div class="wrap split">
        <img class="split__ph split__img" src="/assets/photos/mitre-building.jpg?v={ver("assets/photos/mitre-building.jpg")}" alt="The Mitre logo on the front of an office building against a blue sky" width="1600" height="1066" loading="lazy" decoding="async" />
        <div>
          <p class="eyebrow">Careers at Mitre</p>
          <h2 class="h-section" id="promise-title">Extreme ownership is the only qualification.</h2>
          <p class="lede">We're a lean team that embeds with operators, allowing them to focus on what they do best. If you take pride in owning the result, not just the deliverable, you will fit right in.</p>
          <a class="btn btn--primary" href="/careers/">Explore Careers <span aria-hidden="true">→</span></a>
        </div>
      </div>
    </section>

{home_reach()}
  </main>
"""


def write(path, html):
    out = ROOT / path.strip("/") / "index.html" if path != "/" else ROOT / "index.html"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(html)


HOME_DESC = "Mitre embeds engineers in your business to find where AI creates value and build the systems that capture it. AI implementation that drives operational and cash efficiency."
write("/", head("/", "Mitre Global | AI implementation that drives operational and cash efficiency", HOME_DESC, False) + header("/") + HOME_MAIN + footer())

# ---------------- services ----------------
TILES = [
    ("01", "Lower your costs",
     "Cut manual hours and retire tools you've outgrown. We replace rented software with systems you own, so you run leaner with fewer vendors."),
    ("02", "Focus on your core",
     "We streamline your operations and communications and remove the busywork that pulls your team away from what makes you win: the brand, the deals, the job itself."),
    ("03", "Unlock insight from your data",
     "Your data is spread across a dozen tools, and some of it isn't captured at all. We unify it and fill the gaps, turning it into insight your operators and your AI can act on."),
]
tiles = "\n".join(f"""          <article class="tile">
            <p class="tile__n">{n}</p>
            <h3 class="tile__title">{t}</h3>
            <p class="tile__body">{b}</p>
          </article>""" for n, t, b in TILES)

# (number, short name, title, description, tags, deliverable, link, animation label)
PHASES = [
    ("01", "Assess", "Find where AI pays off",
     "In two weeks, we connect to your data, sit down with the people who run each function, and map where time and money go. We rank every opportunity by its impact against the cost to build it, and agree on the outcomes we'll be measured by.",
     ["Connect data", "Team interviews", "Rank by return", "Set outcomes", "Proposal"],
     "You leave with a ranked roadmap and a proposal, before any long-term commitment.",
     ("Start with an assessment", "/contact/"),
     "Animation: opportunities ranked by return"),
    ("02", "Unify", "Build your data layer",
     "We pull the data spread across your tools and workflows into one unified data layer, enrich it with context, and start capturing what isn't tracked today. It becomes the single source of truth for your team and every system we build on top of it.",
     ["Consolidate", "Enrich", "Capture new sources", "Single source of truth"], None, None,
     "Animation: scattered sources flowing into one data layer"),
    ("03", "Build", "Deploy alongside your team",
     "Our engineers embed with your team, in person wherever we can, to build the agents, workflows, software and reporting agreed in your proposal. We stay through adoption, so the new systems become part of how your team works.",
     ["AI agents", "Workflows", "Custom software", "Reporting", "Adoption"], None, None,
     "Animation: agents and apps built on the data layer"),
    ("04", "Prove", "Measure against the outcomes",
     "Every system is measured against the outcomes set in Phase 01. You get a regular scorecard, on a cadence that fits your business, showing hours saved, costs cut and insight gained.",
     ["Benchmark", "Scorecard", "Cost savings", "Time saved", "New insight"], None, None,
     "Animation: scorecard against the baseline"),
    ("05", "Run", "Choose how we continue",
     "When the work is proven, you choose what comes next.",
     None, None, None, None),
]
PATHS = [
    ("Your team runs it.", "We hand over the systems, code and documentation, and train your team to run and extend them."),
    ("We run it with you.", "We keep operating and improving what we built, and take on the next opportunities on your roadmap."),
]


def phase_panel(n, name, title, desc, tags, deliv, link, anim):
    extra = ""
    if tags:
        chips = "".join(f"<li>{t}</li>" for t in tags)
        extra += f'\n              <ul class="tags" aria-label="What this phase covers">{chips}</ul>'
    if deliv:
        extra += f'\n              <p class="phase__deliv">{deliv}</p>'
    if link:
        extra += f'\n              <a class="more phase__link" href="{link[1]}">{link[0]}</a>'
    if anim:
        side = ph("anim", anim, "phase__vis")
    else:
        cards = "\n".join(f"""              <div class="path">
                <h4 class="path__title">{t}</h4>
                <p>{b}</p>
              </div>""" for t, b in PATHS)
        side = f'<div class="paths">\n{cards}\n            </div>'
    return f"""          <section class="phase" id="phase-{n}" aria-labelledby="phase-{n}-title">
            <div class="phase__txt">
              <p class="phase__label">Phase {n} · {name}</p>
              <h3 class="phase__title" id="phase-{n}-title">{title}</h3>
              <p class="phase__desc">{desc}</p>{extra}
            </div>
            {side}
          </section>"""


phase_tabs = "\n".join(
    f'            <button type="button" class="phases__tab" role="tab" id="phase-{n}-tab" aria-controls="phase-{n}">'
    f'<span class="phases__n">{n}</span> {name}</button>'
    for n, name, *_ in PHASES)
phase_panels = "\n".join(phase_panel(*ph_) for ph_ in PHASES)

FAQ = [
    ("How does an engagement start?", "With a two-week assessment that ends in a ranked roadmap and a proposal. There's no long-term commitment until you've seen it."),
    ("How is Mitre paid?", "Our fees are tied to the value we create and earned as we deliver, not paid all up front. We'll walk through specifics on a call."),
    ("How do you handle our data?", "We work inside your systems with the access our agreement defines, and we hold to the security standards your industry expects."),
    ("Do we have to replace our current tools?", "No. We connect to what you already use. Where custom software would serve you better than a tool you're paying for, we'll show you the math."),
    ("Do you work on site?", "Yes, wherever we can. Our engineers embed with your team in person and work remotely when that serves the project better."),
    ("Which AI models do you use?", "Whichever fit the job and your preferences. We're model-agnostic, and nothing we build locks you into one provider."),
]
faq = "\n".join(f"""          <details class="faq__item">
            <summary class="faq__q">{q}<span class="faq__icon" aria-hidden="true"></span></summary>
            <p class="faq__a">{a}</p>
          </details>""" for q, a in FAQ)

SERVICES_MAIN = f"""
  <main id="page">
    <section class="phero phero--photo phero--tight" aria-labelledby="svc-title">
      <div class="wrap">
       <div class="phero__box">
        <img class="phero__bg" src="/assets/photos/water.jpg?v={ver("assets/photos/water.jpg")}" alt="" width="2000" height="1125" fetchpriority="high" decoding="async" />
        <p class="eyebrow">Services</p>
        <h1 class="h-display" id="svc-title">We build AI capabilities into your business and prove what it's worth.</h1>
        <p class="lede">Mitre engineers work alongside your team to find where AI creates real value, build the data and systems to capture it, and measure every result against outcomes we agree on up front.</p>
        <a class="btn btn--light" href="#deliver">See how <span aria-hidden="true">↓</span></a>
       </div>
      </div>
    </section>

    <section class="sec" id="deliver" aria-labelledby="deliver-title">
      <div class="wrap">
        <div class="sec__head">
          <div>
            <p class="eyebrow">What we deliver</p>
            <h2 class="h-section" id="deliver-title">Value you can measure.</h2>
          </div>
        </div>
        <div class="tiles">
{tiles}
        </div>
      </div>
    </section>

    <section class="feature feature--compact" aria-labelledby="saas-title">
      <div class="wrap feature__in">
        <div>
          <p class="eyebrow">Own your software</p>
          <h2 class="h-section" id="saas-title">Shrink your vendor stack.</h2>
          <p class="lede">Many of the tools you pay for every month can be replaced with custom software built around how you actually work. You own it outright and stop paying for seats and features you don't use.</p>
        </div>
        {ph("anim", "Animation placeholder: vendor tools consolidating into one owned system", "ph--g feature__vis")}
      </div>
    </section>

    <section class="sec" aria-labelledby="engage-title">
      <div class="wrap">
        <div class="sec__head">
          <div>
            <p class="eyebrow">How we engage</p>
            <h2 class="h-section" id="engage-title">From first look to lasting results.</h2>
            <p class="lede">Every engagement follows the same path. Each phase builds on the last, and nothing moves forward without your sign-off.</p>
          </div>
        </div>
        <div class="phases" data-phases>
          <div class="phases__tabs" role="tablist" aria-label="Engagement phases" hidden>
{phase_tabs}
          </div>
          <div class="phases__panels">
{phase_panels}
          </div>
          <div class="phases__nav" hidden>
            <button type="button" class="btn btn--outline" data-phase-prev><span aria-hidden="true">←</span> Previous</button>
            <button type="button" class="btn btn--primary" data-phase-next>Next <span aria-hidden="true">→</span></button>
          </div>
        </div>
      </div>
    </section>

    <section class="wrap promo promo--page" aria-labelledby="own-title">
      <div class="promo__card">
        <div class="promo__bg" aria-hidden="true"></div>
        <div>
          <p class="eyebrow">Yours, outright</p>
          <h2 id="own-title">You own everything built.</h2>
        </div>
        <p>The code, data, products and processes are yours from day one, whether we hand off or continue supporting. We're model-agnostic, so everything runs on the AI models and tools already selected by your company. Your data stays secure and within your own environments.</p>
      </div>
    </section>

    <section class="sec" aria-labelledby="faq-title">
      <div class="wrap">
        <div class="sec__head">
          <div>
            <p class="eyebrow">FAQ</p>
            <h2 class="h-section" id="faq-title">Common questions.</h2>
          </div>
        </div>
        <div class="faq">
{faq}
        </div>
      </div>
    </section>

{reach("Get started", "Let's talk about your business.", "Tell us what you're working on. Most engagements start with an assessment.")}
  </main>
"""
SERVICES_DESC = "Mitre engineers embed with your team to find where AI pays off, build the systems to capture it, and measure every result."
write("/services/", head("/services/", "Services | Mitre", SERVICES_DESC, False) + header("/services/") + SERVICES_MAIN + footer())

# ---------------- placeholder subpages ----------------
def subpage(path, eyebrow, h1, lede, extra="", banner=True, title=None, banner_label="Page content coming soon", pre="", hero_cls=""):
    body = ""
    if banner or pre:
        body = f"""    <section class="sec" style="padding-top:0">
      <div class="wrap">{pre}{ph("anim", banner_label, "phero__ph") if banner else ""}</div>
    </section>"""
    main = f"""
  <main id="page">
    <section class="phero{(" " + hero_cls) if hero_cls else ""}">
      <div class="wrap">
        <p class="eyebrow">{eyebrow}</p>
        <h1 class="h-display">{h1}</h1>
        <p class="lede">{lede}</p>{extra}
      </div>
    </section>
{body}
  </main>
"""
    title = f"{title or eyebrow} | Mitre"
    write(path, head(path, title, "", True) + header(path) + main + footer())


FIN_PRODUCTS = [
    ("SMB Lending", "Working capital for growing businesses, to fund inventory, hiring or expansion."),
    ("Purchase Order Financing", "Funding to pay suppliers on confirmed customer orders, so you can fill large orders without draining cash."),
    ("Factoring", "Turn unpaid invoices into cash now instead of waiting on customer payment terms."),
    ("Letters of Credit", "A bank-backed payment guarantee that gives suppliers, especially overseas, the confidence to ship."),
]
fin_tiles = "\n".join(f"""          <article class="tile">
            <p class="tile__n">{i:02d}</p>
            <h3 class="tile__title">{t}</h3>
            <p class="tile__body">{b}</p>
          </article>""" for i, (t, b) in enumerate(FIN_PRODUCTS, 1))
FINANCING_MAIN = f"""
  <main id="page">
    <section class="phero phero--photo phero--busy" aria-labelledby="fin-title">
      <div class="wrap">
       <div class="phero__box">
        <img class="phero__bg" src="/assets/photos/glass-towers.jpg?v={ver("assets/photos/glass-towers.jpg")}" alt="" width="2000" height="1125" fetchpriority="high" decoding="async" />
        <p class="eyebrow eyebrow--row">Trade Financing <span class="badge"><span class="badge__dot" aria-hidden="true"></span>Coming soon</span></p>
        <h1 class="h-display" id="fin-title">Payments and cash management that accelerate growth.</h1>
        <p class="lede">Growth stalls when cash is tied up in inventory and unpaid invoices. We help you fund purchases, pay suppliers on time and collect faster, with a clear view of your cash across all the systems you already run.</p>
        <a class="btn btn--light" href="/contact/">Be the first to know <span aria-hidden="true">→</span></a>
       </div>
      </div>
    </section>
    <section class="sec" aria-labelledby="fin-products-title">
      <div class="wrap">
        <h2 class="fin__k" id="fin-products-title">What's coming</h2>
        <div class="tiles tiles--4">
{fin_tiles}
        </div>
      </div>
    </section>
  </main>
"""
write("/financing/", head("/financing/", "Financing | Mitre", "", True) + header("/financing/") + FINANCING_MAIN + footer())
subpage("/industries/", "Industries", "See the impact Mitre can have in your industry.", "Select your industry to learn more.",
        extra="\n" + pills("Choose an industry"), banner=False, hero_cls="phero--end")
def select(name, label, options, extra=""):
    opts = "".join(f'<option value="{v}">{t}</option>' for v, t in options)
    return f'            <span class="filter__select{extra}"><select name="{name}" aria-label="{label}">{opts}</select></span>'


JOB_FILTERS = f"""
        <form class="jobfilter" data-jobfilter role="search" aria-label="Filter open roles" onsubmit="return false">
          <div class="jobfilter__row">
            <input class="filter__input filter--search" type="search" name="q" placeholder="Search roles" aria-label="Search roles" autocomplete="off" />
{select("team", "Team", [("", "All teams"), ("engineering", "Engineering"), ("strategy", "Strategy"), ("operations", "Operations")])}
{select("location", "Location", [("", "All locations"), ("on-site", "On site"), ("hybrid", "Hybrid"), ("remote", "Remote")])}
{select("type", "Type", [("", "All types"), ("full-time", "Full-time"), ("contract", "Contract"), ("internship", "Internship")])}
{select("sort", "Sort by", [("newest", "Sort: Newest"), ("title", "Sort: Title A to Z")])}
          </div>
          <div class="jobfilter__bar">
            <p class="jobfilter__count" role="status" aria-live="polite"><span data-job-count>0</span> open <span data-job-noun>roles</span></p>
            <button type="reset" class="jobfilter__reset">Clear filters</button>
          </div>
        </form>
        <ul class="jobs" data-jobs aria-label="Open roles"></ul>
"""
subpage("/careers/", "Work with us", "Careers", "Explore roles at Mitre.", title="Careers", banner_label="No open roles at this time.", pre=JOB_FILTERS)
CONTACT_MAIN = f"""
  <main id="page">
    <section class="phero" aria-labelledby="contact-title">
      <div class="wrap">
        <p class="eyebrow">Contact</p>
        <h1 class="h-display" id="contact-title">Talk with a Mitre engineer.</h1>
        <p class="lede">Tell us what you're working on. A real person reads every note.</p>
      </div>
    </section>
    <section class="sec contact-sec" aria-label="Contact form">
      <div class="wrap contact">
        <aside class="contact__panel">
          <div class="promo__bg" aria-hidden="true"></div>
          <p class="eyebrow">Get started</p>
          <h2 class="contact__title">Most engagements start with an assessment.</h2>
          <p class="contact__txt">Share a little about your business and where you want to go. We'll follow up to set up a first conversation.</p>
          <div class="contact__mail">
            <span>Prefer email?</span>
            <a href="mailto:{MAIL}">{MAIL}</a>
          </div>
        </aside>
{contact_form()}
      </div>
    </section>
  </main>
"""
write("/contact/", head("/contact/", "Contact | Mitre", "", True) + header("/contact/") + CONTACT_MAIN + footer())
# ---------------- industry pages ----------------


def industry_page(path, name):
    lead, para, helps = IND_COPY[path]
    chips = "".join(f"<li>{t}</li>" for t in helps)
    main = f"""
  <main id="page">
    <section class="phero" aria-labelledby="ind-title">
      <div class="wrap">
        <p class="eyebrow">Industries</p>
        <h1 class="h-display" id="ind-title">{name}</h1>
        <p class="lede">{lead}</p>
      </div>
    </section>
    <section class="sec ind" aria-label="About {name}">
      <div class="wrap">
        <div class="ind__panel">
          <div class="promo__bg" aria-hidden="true"></div>
          <p class="ind__body">{para}</p>
          <div class="ind__help">
            <p class="phase__label">Where we help</p>
            <ul class="tags">{chips}</ul>
          </div>
        </div>
        <p class="ind__cta"><a class="btn btn--primary" href="/services/">Our service <span aria-hidden="true">→</span></a></p>
      </div>
    </section>

{offering(name)}

{home_reach()}
  </main>
"""
    write(path, head(path, f"{name.replace('&amp;', '&')} | Mitre", "", True) + header(path) + main + footer())


for p, label in INDUSTRIES:
    industry_page(p, label)
print("ok")
