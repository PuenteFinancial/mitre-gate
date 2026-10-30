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
MAIL = "info@mitre.global"
# Google Apps Script web app behind every contact form: adds the lead to a Google Sheet and emails it
LEAD_URL = "https://script.google.com/macros/s/AKfycbzndSovCUsRlUzlvAE9N_1Qu8-oQ8eQlys31hT71fkJ3C6FxKIMhEebZtipMYPrRMc/exec"


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
  <link rel="canonical" href="https://mitre.global{path}" />{d}
  <meta property="og:type" content="website" />
  <meta property="og:site_name" content="Mitre" />
  <meta property="og:title" content="{title}" />
  <meta property="og:url" content="https://mitre.global{path}" />
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
    """The contact form (name, company and work email required; message optional). site.js validates it,
    then posts it to LEAD_URL. The hidden "website" field is a honeypot for spam bots."""
    return f"""        <form class="form" data-lead-form="{LEAD_URL}" novalidate>
          <div class="form__row">
            <label class="field"><span class="field__label">Name</span>
              <input class="field__input" name="name" autocomplete="name" required></label>
            <label class="field"><span class="field__label">Company</span>
              <input class="field__input" name="company" autocomplete="organization" required></label>
          </div>
          <label class="field"><span class="field__label">Work email</span>
            <input class="field__input" type="email" name="email" autocomplete="email" required></label>
          <label class="field"><span class="field__label">How can we help? <span class="field__opt">(optional)</span></span>
            <textarea class="field__input field__input--area" name="message" rows="5"></textarea></label>
          <input type="text" name="website" tabindex="-1" autocomplete="off" aria-hidden="true" style="position:absolute;left:-9999px;width:1px;height:1px;opacity:0">
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


# Phase 01 visual: opportunities ranked by return (from the mitre-bars artwork), in the shared glass style.
# Bars grow in a shuffled order, slide into rank order, values fade in, then the minimum engagement line
# appears and the bars under it turn to clear glass. Values are illustrative.
RANK = [9.5, 7.2, 5.8, 4.1, 2.7, 1.9]
RANK_MIN = 4.0          # minimum engagement threshold
RANK_START = [1, 3, 5, 0, 4, 2]   # unsorted slot each ranked bar starts in (reads 4.1, 9.5, 1.9, 7.2, 2.7, 5.8)


def rank_anim():
    p, W, H = "rk", 720, 540
    left, base, unit = 206, 452, 30                      # plot origin; 30 units of height per 1x
    step, w = 76, 56                                     # column pitch and bar width
    right = left + 5 * step + w
    tmin = base - RANK_MIN * unit
    grid = "".join(f'<path class="an-gridh" d="M{left - 10} {base - k * unit} H{right + 10}"/>' for k in (2, 6, 8))
    cols = []
    for i, (v, start) in enumerate(zip(RANK, RANK_START)):
        x, h = left + i * step, v * unit
        out = v < RANK_MIN
        frost = f'<g class="a-fade"{d(3.5, t=".6s")}>{glass(p, x, base - h, w, h, 12)}</g>' if out else ""
        val = "an-t an-t--sm an-t--mute" if out else "an-t an-t--sm"
        # --i: rank, --dx: offset from the ranked slot back to the starting slot
        cols.append(f'<g class="rk-col" style="--i:{i};--dx:{(start - i) * step}px">'
                    f'<g class="a-gy"{d(.3 + start * .1, t=".7s")}>{glass(p, x, base - h, w, h, 12, "tint")}</g>{frost}'
                    f'<text class="{val} a-fade" x="{x + w / 2}" y="{base - h - 14}" text-anchor="middle"{d(2.7 + i * .07, t=".4s")}>{v}x</text></g>')
    label = (f"Six opportunities ranked by return, from {RANK[0]}x to {RANK[-1]}x. "
             f"{sum(v >= RANK_MIN for v in RANK)} clear the minimum engagement threshold.")
    return (svg_open("rk", W, H, label) + glass_defs(p)
            + f'<g class="a-pop">{glass(p, 30, 30, 660, 480, 20)}'
            + f'<text class="an-t" x="58" y="72">Opportunities</text>'
            + f'<text class="an-m" x="662" y="72" text-anchor="end">Ranked by return</text></g>'
            + f'<g class="a-fade"{d(.2)}>{grid}<path class="an-axis" d="M{left - 10} {base} H{right + 10}"/></g>'
            + "".join(cols)
            # x axis: the ranked opportunities above the threshold read as a roadmap, 01 to 04
            + f'<g class="a-fade"{d(2.6, t=".5s")}><text class="an-m an-m--min" x="{left - 22}" y="{base + 30}" text-anchor="end">Roadmap</text>'
            + "".join(f'<text class="an-m" x="{left + k * step + w / 2}" y="{base + 30}" text-anchor="middle">{k + 1:02d}</text>' for k in range(sum(v >= RANK_MIN for v in RANK)))
            + "</g>"
            + f'<g class="a-fade"{d(3.5, t=".6s")}><path class="an-min" d="M{left - 10} {tmin} H{right + 10}"/>'
            + f'<circle class="an-live" cx="{left - 10}" cy="{tmin}" r="5"/>'
            + f'<text class="an-m an-m--min" x="{left - 22}" y="{tmin + 4}" text-anchor="end">Min. engagement</text></g>'
            + "</svg>")

# ---------------- services animations: shared glass + motion toolkit ----------------
# Every animation is an inline SVG in a <figure class="anim">. site.js adds .is-armed, then .is-play when
# it is in view; the motion classes (a-pop, a-rise, a-drop, a-gx, a-gy, a-draw, a-to, a-flow) are in site.css
# and read their delay from --d. Without JS, or with reduced motion, the finished frame shows.
ICONS = {
    "crm": '<circle cx="12" cy="8" r="4"/><path d="M4 21c0-4 4-6 8-6s8 2 8 6"/>',
    "billing": '<rect x="2" y="5" width="20" height="14" rx="2"/><path d="M2 10h20M6 15h4"/>',
    "inventory": '<path d="M3 7l9-4 9 4v10l-9 4-9-4z"/><path d="M3 7l9 4 9-4M12 11v10"/>',
    "reports": '<path d="M5 20v-8M12 20V5M19 20v-5"/>',
    "email": '<rect x="3" y="5" width="18" height="14" rx="2"/><path d="M3 7l9 6 9-6"/>',
    "calendar": '<rect x="3" y="5" width="18" height="16" rx="2"/><path d="M3 10h18M8 3v4M16 3v4"/>',
    "sheet": '<rect x="4" y="3" width="16" height="18" rx="2"/><path d="M4 9h16M4 15h16M10 3v18"/>',
    "erp": '<rect x="3" y="4" width="18" height="6" rx="1.5"/><rect x="3" y="14" width="18" height="6" rx="1.5"/><path d="M7 7h.01M7 17h.01"/>',
    "calls": '<path d="M5 4h4l2 5-2.5 1.5a11 11 0 0 0 5 5L15 13l5 2v4a2 2 0 0 1-2 2A16 16 0 0 1 3 6a2 2 0 0 1 2-2"/>',
    "agent": '<path d="M12 3l2 5.5L19.5 10 14 12l-2 5.5L10 12 4.5 10 10 8.5z"/><path d="M19 16l.8 2 2 .8-2 .8-.8 2-.8-2-2-.8 2-.8z"/>',
    "flow": '<circle cx="5" cy="6" r="2.5"/><circle cx="19" cy="6" r="2.5"/><circle cx="12" cy="18" r="2.5"/><path d="M7.5 6h9M6.5 8.2l4.2 7.6M17.5 8.2l-4.2 7.6"/>',
    "app": '<rect x="3" y="4" width="18" height="16" rx="2"/><path d="M3 9h18M7 13h6M7 16h4"/>',
    "time": '<circle cx="12" cy="12" r="9"/><path d="M12 7v5l3 2"/>',
    "cost": '<circle cx="12" cy="12" r="9"/><path d="M15 9.5c-.6-1-1.7-1.5-3-1.5-1.7 0-3 .8-3 2s1.3 1.7 3 2 3 .8 3 2-1.3 2-3 2c-1.3 0-2.4-.5-3-1.5M12 6v2M12 16v2"/>',
    "insight": '<path d="M9 18h6M10 21h4M12 3a6 6 0 0 0-3.5 10.9c.6.5 1 1.3 1 2.1h5c0-.8.4-1.6 1-2.1A6 6 0 0 0 12 3z"/>',
    "check": '<path d="M5 12.5l4.5 4.5L19 7.5"/>',
    "manual": '<rect x="5" y="4" width="14" height="17" rx="2"/><path d="M9 4V3h6v1M9 10h6M9 14h6M9 18h3"/>',
    "coin": '<circle cx="12" cy="12" r="8"/><path d="M12 8v8M9.5 10.5c0-1 1.1-1.6 2.5-1.6s2.5.6 2.5 1.6-1.1 1.4-2.5 1.5-2.5.6-2.5 1.6 1.1 1.6 2.5 1.6 2.5-.6 2.5-1.6"/>',
    "handoff": '<path d="M4 12h12M12 7l5 5-5 5"/><path d="M20 4v16"/>',
    "team": '<circle cx="9" cy="8" r="3.5"/><path d="M2.5 20c0-3.5 3-5.5 6.5-5.5s6.5 2 6.5 5.5"/><circle cx="17" cy="9" r="2.8"/><path d="M17 14.5c2.8 0 4.5 1.6 4.5 4.5"/>',
}


def icon(name, x, y, size=24, cls="an-ico"):
    return f'<g class="{cls}" transform="translate({x} {y}) scale({size / 24})">{ICONS[name]}</g>'


def glass_defs(p):
    """Gradients and filters for one SVG. Ids are per SVG (prefix p) so a hidden phase never breaks another."""
    return f"""<defs>
                <linearGradient id="{p}-g" x1="0" y1="0" x2="0" y2="1"><stop class="gl-g0" offset="0"/><stop class="gl-gm" offset=".55"/><stop class="gl-g1" offset="1"/></linearGradient>
                <linearGradient id="{p}-gh" x1="0" y1="0" x2="1" y2="0"><stop class="gl-g0" offset="0"/><stop class="gl-gm" offset=".6"/><stop class="gl-g1" offset="1"/></linearGradient>
                <linearGradient id="{p}-f" x1="0" y1="0" x2="0" y2="1"><stop class="gl-f0" offset="0"/><stop class="gl-f1" offset="1"/></linearGradient>
                <linearGradient id="{p}-l" x1="0" y1="0" x2="1" y2="0"><stop class="gl-l0" offset="0"/><stop class="gl-l1" offset=".3"/><stop class="gl-l1" offset=".75"/><stop class="gl-l2" offset="1"/></linearGradient>
                <linearGradient id="{p}-e" x1="0" y1="0" x2="1" y2="1"><stop class="gl-e0" offset="0"/><stop class="gl-e1" offset=".6"/></linearGradient>
                <linearGradient id="{p}-c" x1="0" y1="0" x2="0" y2="1"><stop class="gl-c0" offset="0"/><stop class="gl-c1" offset="1"/></linearGradient>
                <filter id="{p}-sh" x="-30%" y="-30%" width="160%" height="170%"><feDropShadow class="gl-sh" dx="0" dy="8" stdDeviation="8"/></filter>
              </defs>"""


def glass(p, x, y, w, h, r=14, kind="frost"):
    """One glass shape: body (tint = see-through brand blue to teal, tinth = the same running sideways,
    frost = clear panel), side lighting, a soft top cap and a bright edge, with a soft shadow."""
    body = {"tint": "g", "tinth": "gh", "frost": "f"}[kind]
    cap = min(26, h / 3)
    return (f'<g filter="url(#{p}-sh)">'
            f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{r}" fill="url(#{p}-{body})"/>'
            f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{r}" fill="url(#{p}-l)"/>'
            f'<rect x="{x + 3}" y="{y + 3}" width="{w - 6}" height="{cap}" rx="{max(r - 3, 2)}" fill="url(#{p}-c)"/>'
            f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{r}" fill="none" stroke="url(#{p}-e)" stroke-width="1.5"/></g>')


def svg_open(cls, vw, vh, label):
    tid = cls + "-title"
    return f'<svg class="anim__svg {cls}" viewBox="0 0 {vw} {vh}" role="img" aria-labelledby="{tid}"><title id="{tid}">{label}</title>'


def d(sec, **extra):
    """Inline style for a motion delay (and any other custom properties)."""
    props = [f"--d:{sec:g}s"] + [f"--{k}:{v}" for k, v in extra.items()]
    return f' style="{";".join(props)}"'


# ---- vendor tools consolidating into one owned system (16:9) ----
VENDORS = [("crm", "CRM"), ("billing", "Billing"), ("inventory", "Inventory"),
           ("reports", "Reports"), ("email", "Email"), ("calendar", "Scheduling")]


def vendor_anim():
    p, W, H = "vd", 960, 540
    px, py, pw, ph_ = 300, 54, 360, 432                  # the owned system panel
    cx, cy = px + pw / 2, py + ph_ / 2
    tw, th = 236, 100
    spots = [(20, 34), (20, 220), (20, 406), (704, 34), (704, 220), (704, 406)]
    tiles = []
    for i, ((key, name), (x, y)) in enumerate(zip(VENDORS, spots)):
        dx, dy = cx - (x + tw / 2), cy - (y + th / 2)
        tiles.append(f'<g class="a-to"{d(1.7 + i * .06, dx=f"{dx:g}px", dy=f"{dy:g}px")}><g class="a-pop"{d(i * .12)}>'
                     f'{glass(p, x, y, tw, th, 18)}{icon(key, x + 22, y + 34, 32)}'
                     f'<text class="an-t an-t--lg" x="{x + 70}" y="{y + 46}">{name}</text>'
                     f'<text class="an-m an-m--lg" x="{x + 70}" y="{y + 76}">Per seat</text></g></g>')
    rows = []
    for i, (key, name) in enumerate(VENDORS):
        ry = py + 114 + i * 44
        rows.append(f'<g class="a-rise"{d(2.5 + i * .1)}>{icon(key, px + 30, ry - 14, 28)}'
                    f'<text class="an-t an-t--lg" x="{px + 72}" y="{ry + 9}">{name}</text>'
                    f'{icon("check", px + pw - 58, ry - 14, 28, "an-ico an-ico--ok")}</g>')
    # once the tools fold in, a small card beside the panel shows monthly cost stepping down (no figures)
    kx, ky, kw, kh = 684, 196, 252, 148
    pts = [(kx + 24 + k * 40, v) for k, v in enumerate((0, 4, 18, 22, 36, 40))]
    trend = "M" + " L".join(f"{x:g} {ky + 92 + v:g}" for x, v in pts)
    savings = (f'<g class="a-pop"{d(3.4)}>{glass(p, kx, ky, kw, kh, 18)}'
               f'<g>{glass(p, kx + 20, ky + 20, 40, 40, 12, "tint")}</g>{icon("coin", kx + 29, ky + 29, 22, "an-ico an-ico--on")}'
               f'<text class="an-m an-m--lg" x="{kx + 74}" y="{ky + 46}">Monthly cost</text></g>'
               f'<path class="an-line an-line--save a-draw" pathLength="1" d="{trend}"{d(3.8, t="1.1s")}/>'
               f'<circle class="an-ok a-pop" cx="{pts[-1][0]}" cy="{ky + 92 + pts[-1][1]}" r="6"{d(4.8)}/>')
    return (svg_open("vd", W, H, "Six rented tools, each billed per seat, fold into one system you own, and monthly cost steps down.")
            + glass_defs(p)
            + f'<g class="a-pop"{d(2.0)}>{glass(p, px, py, pw, ph_, 20)}'
            + f'<text class="an-t an-t--xl" x="{px + 30}" y="{py + 58}">Your system</text>'
            + f'<path class="an-rule" d="M{px + 30} {py + 82} H{px + pw - 30}"/></g>'
            + f'<g class="a-pop"{d(3.2)}>{glass(p, cx - 78, py + ph_ - 60, 156, 42, 21)}'
            + f'<circle class="an-ok" cx="{cx - 50}" cy="{py + ph_ - 39}" r="11"/>{icon("check", cx - 58, py + ph_ - 47, 16, "an-ico an-ico--on")}'
            + f'<text class="an-m an-m--lg an-m--ok" x="{cx - 30}" y="{py + ph_ - 32}">Owned</text></g>'
            + savings + "".join(rows) + "".join(tiles) + "</svg>")


# ---- phase 02: scattered sources flowing into one data layer ----
TRACKED = [("sheet", "Spreadsheets"), ("erp", "ERP"), ("crm", "CRM")]                 # above the layer, flowing down
UNTRACKED = [("email", "Email"), ("calls", "Calls"), ("manual", "Manual workflows")]     # below it: captured, flowing up


def unify_anim():
    p, W, H = "un", 720, 540
    sx, sy, sw, sh = 50, 206, 620, 112                  # the data layer, in the middle
    chh = 44
    xs = [168, 360, 552]
    def chip(key, name, cx, cy):
        cw = max(96, 58 + len(name) * 8.8)               # fit each label, with room to breathe
        x, y = cx - cw / 2, cy - chh / 2
        body = (f'{glass(p, x, y, cw, chh, 22)}{icon(key, x + 14, y + 12, 20)}'
                f'<text class="an-t an-t--sm" x="{x + 42}" y="{y + 28}">{name}</text>')
        return x, y, cw, body
    parts, lines, flows = [], [], []
    for i, ((key, name), cx) in enumerate(zip(TRACKED, xs)):
        x, y, cw, body = chip(key, name, cx, 62)
        tx = 360 + (cx - 360) * .5
        path = f"M{cx} {y + chh} C{cx} {y + chh + 70} {tx} {sy - 70} {tx} {sy}"
        lines.append(f'<path class="an-link a-draw" pathLength="1" d="{path}"{d(1.0 + i * .12, t=".8s")}/>')
        flows.append(f'<path class="an-flow a-flow" pathLength="1" d="{path}"{d(1.8 + i * .12)}/>')
        parts.append(f'<g class="a-pop"{d(.2 + i * .12)}>{body}</g>')
    for i, ((key, name), cx) in enumerate(zip(UNTRACKED, xs)):
        x, y, cw, body = chip(key, name, cx, 444)
        cap = 2.4 + i * .4                                # each one is captured in turn
        tx = 360 + (cx - 360) * .5
        path = f"M{cx} {y} C{cx} {y - 70} {tx} {sy + sh + 70} {tx} {sy + sh}"
        lines.append(f'<path class="an-link a-draw" pathLength="1" d="{path}"{d(cap + .3, t=".8s")}/>')
        flows.append(f'<path class="an-flow a-flow" pathLength="1" d="{path}"{d(cap + 1.1)}/>')
        parts.append(f'<g class="a-out"{d(cap - .1)}><g class="a-fade"{d(.6)}>'
                     f'<rect class="an-ghost" x="{x}" y="{y}" width="{cw}" height="{chh}" rx="22"/></g></g>'
                     f'<g class="a-pop"{d(cap)}>{body}</g>')
    recs = "".join(f'<rect class="an-rec a-gx" x="{sx + 24}" y="{sy + 58 + k * 18}" width="{w}" height="8" rx="4"{d(1.9 + k * .6, t="1s")}/>'
                   for k, w in enumerate((420, 520, 340)))
    return (svg_open("un", W, H, "Spreadsheets, ERP and CRM flow into one unified data layer, then email, calls and manual workflows, which were not tracked before, are captured into it too.")
            + glass_defs(p)
            + "".join(lines) + "".join(flows)
            + f'<g class="a-pop"{d(.4)}>{glass(p, sx, sy, sw, sh, 20, "tinth")}'
            + f'<text class="an-t an-t--on" x="{sx + 24}" y="{sy + 38}">Unified data layer</text>'
            + f'<text class="an-m an-m--on" x="{sx + sw - 24}" y="{sy + 38}" text-anchor="end">Single source of truth</text></g>'
            + recs
            + f'<g class="a-out"{d(2.3)}><text class="an-m a-fade" x="360" y="510" text-anchor="middle"{d(.6)}>Not tracked yet</text></g>'
            + "".join(parts) + "</svg>")

# ---- phase 03: agents and apps built on the data layer ----
BUILDS = [("agent", "AI agents"), ("flow", "Workflows"), ("app", "Custom software"), ("reports", "Reporting")]


def build_anim():
    p, W, H = "bd", 720, 540
    sx, sy, sw, sh = 50, 438, 620, 62                   # the data layer, at the base
    tw, th = 240, 104
    lx, rx = 58, 422                                     # tile columns; the gap between them carries the top links
    spots = [(lx, 290), (rx, 290), (lx, 66), (rx, 66)]  # bottom row first: the build grows upward
    bt, tt = 290 + th, 66 + th                           # bottom edges of the two rows
    routes = [
        f"M200 {sy} C200 {sy - 24} {lx + tw / 2} {bt + 24} {lx + tw / 2} {bt}",              # gentle S into the bottom tiles
        f"M520 {sy} C520 {sy - 24} {rx + tw / 2} {bt + 24} {rx + tw / 2} {bt}",
        f"M345 {sy} C345 280 {lx + tw - 40} 300 {lx + tw - 40} {tt}",                        # up the middle gap, arcing
        f"M375 {sy} C375 280 {rx + 40} 300 {rx + 40} {tt}",                                  # into the top tiles
    ]
    nodes, links, flows, tiles = [], [], [], []
    for i, ((key, name), (x, y), path) in enumerate(zip(BUILDS, spots, routes)):
        top = i >= 2
        t_link = .5 + i * .12
        t_tile = t_link + (.75 if top else .45)
        sxp = float(path.split()[0][1:])
        nodes.append(f'<circle class="an-node a-pop" cx="{sxp}" cy="{sy}" r="6"{d(.35 + i * .08)}/>')
        links.append(f'<path class="an-link an-link--strong a-draw" pathLength="1" d="{path}"{d(t_link, t=(".8s" if top else ".5s"))}/>')
        flows.append(f'<path class="an-flow a-flow" pathLength="1" d="{path}"{d(t_tile + .3 + i * .25)}/>')
        tiles.append(f'<g class="a-rise"{d(t_tile)}>{glass(p, x, y, tw, th, 18)}'
                     f'<g>{glass(p, x + 18, y + 18, 46, 46, 13, "tint")}</g>{icon(key, x + 29, y + 29, 24, "an-ico an-ico--on")}'
                     f'<text class="an-t" x="{x + 78}" y="{y + 47}">{name}</text>'
                     f'<g class="a-pop"{d(2.5 + i * .15)}><circle class="an-live" cx="{x + 26}" cy="{y + 84}" r="5"/>'
                     f'<text class="an-m" x="{x + 40}" y="{y + 89}">Live</text></g></g>')
    return (svg_open("bd", W, H, "AI agents, workflows, custom software and reporting built out from the unified data layer.")
            + glass_defs(p)
            + f'<g class="a-pop">{glass(p, sx, sy, sw, sh, 20, "tinth")}'
            + f'<text class="an-t an-t--on" x="{sx + 24}" y="{sy + 38}">Unified data layer</text></g>'
            + "".join(links) + "".join(flows) + "".join(nodes) + "".join(tiles) + "</svg>")

# ---- phase 04: scorecard against the baseline ----
KPIS = [("time", "Time saved", .86), ("cost", "Cost savings", .74), ("insight", "New insight", .92)]


def prove_anim():
    p, W, H = "pv", 720, 540
    cards = []
    for i, (key, name, v) in enumerate(KPIS):
        x, y, w, h = 30 + i * 226, 30, 208, 132
        rx0, rx1, ry = x + 20, x + w - 20, y + 96
        base = rx0 + (rx1 - rx0) * .42
        cards.append(f'<g class="a-pop"{d(i * .12)}>{glass(p, x, y, w, h, 18)}{icon(key, x + 18, y + 20, 24)}'
                     f'<text class="an-t an-t--sm" x="{x + 50}" y="{y + 37}">{name}</text>'
                     f'<rect class="an-rail" x="{rx0}" y="{ry}" width="{rx1 - rx0}" height="12" rx="6"/>'
                     f'<g class="a-gx"{d(2.6 + i * .15, t="1s")}>{glass(p, rx0, ry, (rx1 - rx0) * v, 12, 6, "tinth")}</g>'
                     f'<path class="an-tick" d="M{base} {ry - 8} V{ry + 20}"/>'
                     f'<text class="an-m" x="{base}" y="{ry - 14}" text-anchor="middle">Base</text>'
                     f'<g class="a-pop"{d(3.3 + i * .12)}><circle class="an-ok" cx="{x + w - 22}" cy="{y + 22}" r="11"/>'
                     f'{icon("check", x + w - 30, y + 14, 16, "an-ico an-ico--on")}</g></g>')
    # the measured line, rising above the baseline period by period
    cx0, cx1, cyb = 92, 640, 430
    ys = [0, 4, 16, 34, 58, 80, 98, 112]
    xs = [cx0 + (cx1 - cx0) * k / (len(ys) - 1) for k in range(len(ys))]
    line = "M" + " L".join(f"{x:g} {cyb - v:g}" for x, v in zip(xs, ys))
    area = line + f" L{cx1} {cyb} L{cx0} {cyb} Z"
    ticks = "".join(f'<path class="an-gridv" d="M{x:g} {cyb - 150} V{cyb + 8}"/>' for x in xs[1:-1])
    chart = (f'<g class="a-pop"{d(.3)}>{glass(p, 30, 196, 660, 314, 20)}'
             f'<text class="an-t" x="58" y="236">Scorecard</text>'
             f'<text class="an-m" x="662" y="236" text-anchor="end">Against the baseline</text></g>'
             f'<g class="a-fade"{d(.8)}>{ticks}<path class="an-base" d="M{cx0} {cyb} H{cx1}"/>'
             f'<text class="an-m" x="{cx1}" y="{cyb + 26}" text-anchor="end">Baseline</text></g>'
             f'<path class="an-area a-fade" d="{area}" fill="url(#{p}-g)"{d(1.9, t=".8s")}/>'
             f'<path class="an-line a-draw" pathLength="1" d="{line}"{d(1.0, t="1.4s")}/>'
             f'<g class="a-pop"{d(2.3)}><circle class="an-dot" cx="{cx1}" cy="{cyb - ys[-1]}" r="7"/>'
             f'<text class="an-t an-t--sm" x="{cx1 - 14}" y="{cyb - ys[-1] - 18}" text-anchor="end">Measured</text></g>')
    return (svg_open("pv", W, H, "A scorecard of time saved, cost savings and new insight, each measured above its baseline.")
            + glass_defs(p) + chart + "".join(cards) + "</svg>")




# ---- homepage offering cards: simplified Assess, Build and Prove (no labels) ----
# Same structure as the Services phases, cut down for the narrower cards. No build-up: each graphic is
# already assembled and fades in as one piece (.anim--soft), then a slow repeating motion runs
# (amb-* classes in site.css). Reduced motion keeps it still.
def home_assess():
    p, W, H = "ha", 400, 300
    # loop: shuffled, glide into rank, the ones under the line frost over, hold, fade and reshuffle
    vals, start_slot, vmin = [9, 7, 5.5, 3.2, 2], [2, 4, 0, 3, 1], 4
    left, base, unit, step, w = 70, 262, 23, 56, 40
    right = left + 4 * step + w
    tmin = base - vmin * unit
    cols = []
    for i, (v, st) in enumerate(zip(vals, start_slot)):
        x, h = left + i * step, v * unit
        frost = f'<g class="hr-frost">{glass(p, x, base - h, w, h, 10)}</g>' if v < vmin else ""
        cols.append(f'<g class="hr-col" style="--i:{i};--dx:{(st - i) * step}px">{glass(p, x, base - h, w, h, 10, "tint")}{frost}</g>')
    return (svg_open("ha", W, H, "Opportunities ranked by return, with the ones below the minimum engagement set aside.")
            + glass_defs(p)
            + f'<path class="an-axis" d="M{left - 12} {base} H{right + 12}"/>'
            + '<g class="hr-set">' + "".join(cols) + "</g>"
            + f'<path class="an-min" d="M{left - 12} {tmin} H{right + 12}"/>'
            + f'<circle class="an-live" cx="{left - 12}" cy="{tmin}" r="4.5"/>'
            + "</svg>")


def home_build():
    p, W, H = "hb", 400, 300
    sx, sy, sw, sh = 40, 244, 320, 40
    tw, th = 120, 60
    spots = [(56, 158), (224, 158), (56, 50), (224, 50)]
    routes = [
        f"M126 {sy} C126 {sy - 14} 116 {158 + th + 14} 116 {158 + th}",
        f"M274 {sy} C274 {sy - 14} 284 {158 + th + 14} 284 {158 + th}",
        f"M194 {sy} C194 142 156 136 156 {50 + th}",
        f"M206 {sy} C206 142 244 136 244 {50 + th}",
    ]
    links, flows, nodes, tiles = [], [], [], []
    for i, ((key, _), (x, y), path) in enumerate(zip(BUILDS, spots, routes)):
        sxp = float(path.split()[0][1:])
        nodes.append(f'<circle class="an-node" cx="{sxp}" cy="{sy}" r="4.5"/>')
        links.append(f'<path class="an-link an-link--strong" d="{path}"/>')
        flows.append(f'<path class="an-flow a-flow" pathLength="1" d="{path}"{d(.8 + i * .7)}/>')
        tiles.append(f'<g>{glass(p, x, y, tw, th, 14)}'
                     f'<g>{glass(p, x + 12, y + 12, 36, 36, 10, "tint")}</g>{icon(key, x + 20, y + 20, 20, "an-ico an-ico--on")}'
                     f'<rect class="an-docline" x="{x + 60}" y="{y + 20}" width="44" height="6" rx="3"/>'
                     f'<rect class="an-docline" x="{x + 60}" y="{y + 34}" width="28" height="6" rx="3"/>'
                     f'<circle class="an-live amb-glow" cx="{x + tw - 14}" cy="{y + 14}" r="4"{d(i * .6)}/></g>')
    return (svg_open("hb", W, H, "Agents, workflows, software and reporting built out from one data layer.")
            + glass_defs(p)
            + glass(p, sx, sy, sw, sh, 14, "tinth")
            + "".join(links) + "".join(flows) + "".join(nodes) + "".join(tiles) + "</svg>")


def home_prove():
    p, W, H = "hp", 400, 300
    rows = []
    r0, r1 = 36, 318
    for i, v in enumerate((.86, .72, .92)):
        y = 58 + i * 78
        tick = r0 + (r1 - r0) * .42
        rows.append(f'<rect class="an-docline" x="{r0}" y="{y - 26}" width="{(70, 92, 80)[i]}" height="7" rx="3.5"/>'
                    f'<rect class="an-rail" x="{r0}" y="{y}" width="{r1 - r0}" height="18" rx="9"/>'
                    f'<g class="amb-x"{d(i * .7)}>{glass(p, r0, y, (r1 - r0) * v, 18, 9, "tinth")}</g>'
                    f'<path class="an-tick" d="M{tick} {y - 8} V{y + 26}"/>'
                    f'<circle class="an-ok" cx="{r1 + 30}" cy="{y + 9}" r="12"/>'
                    f'{icon("check", r1 + 22, y + 1, 16, "an-ico an-ico--on")}')
    return (svg_open("hp", W, H, "Time saved, cost savings and new insight, each measured above its baseline.")
            + glass_defs(p) + "".join(rows) + "</svg>")


HOME_ANIM = {"01": home_assess, "02": home_build, "03": home_prove}

PHASE_ANIM = {"01": rank_anim, "02": unify_anim, "03": build_anim, "04": prove_anim}


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
          <figure class="card__vis anim anim--soft">{HOME_ANIM[n]()}</figure>
          <div class="card__chip"><b>{n}</b><span>{chip}</span></div>
          <div class="card__panel">
            <div class="card__head">
              <h3>{title}</h3>
              <a class="btn btn--primary btn--sm card__go" href="/services/">Services <span aria-hidden="true">→</span></a>
            </div>
            <div class="card__more"><div>
              <p>{body}</p>
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
        <img class="feature__vis feature__img" src="/assets/photos/glass-blocks.jpg?v={ver("assets/photos/glass-blocks.jpg")}" alt="A wall of glass blocks lit softly from behind" width="2000" height="1333" loading="lazy" decoding="async" />
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
    if n in PHASE_ANIM:
        side = f'<figure class="phase__vis anim">\n            {PHASE_ANIM[n]()}\n          </figure>'
    elif anim:
        side = ph("anim", anim, "phase__vis")
    else:
        cards = "\n".join(f"""              <div class="path a-rise"{d(.15 + k * .15)}>
                <span class="path__ico" aria-hidden="true"><svg viewBox="0 0 24 24">{ICONS[ico]}</svg></span>
                <h4 class="path__title">{t}</h4>
                <p>{b}</p>
              </div>""" for k, ((t, b), ico) in enumerate(zip(PATHS, ("handoff", "team"))))
        side = f'<div class="paths anim">\n{cards}\n            </div>'
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
        <figure class="feature__vis anim">{vendor_anim()}</figure>
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
            <h3 class="tile__title">{t}</h3>
            <p class="tile__body">{b}</p>
          </article>""" for t, b in FIN_PRODUCTS)
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
    <section class="sec fin-products" aria-label="Financing products">
      <div class="wrap">
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
