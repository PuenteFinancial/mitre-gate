# Mitre site design language

The house style for mitre.global. New sections and pages should be built from what is here,
so the site stays one consistent thing. The layout is modeled on bcg.com's homepage (used with
permission): floating-island header, a center-weighted photo carousel, rounded cards on warm
paper. The colors and copy are Mitre's own.

## How the site is built

- Plain static HTML. No framework and no bundler.
- **Every page is generated** by `scripts/build_pages.py`. Edit that script (and `v2/site.css`),
  then run `python3 scripts/build_pages.py`. Never hand-edit the generated `index.html` files.
- One stylesheet (`v2/site.css`) and one script (`v2/site.js`) for the whole site.
- The builder adds a content hash (`?v=…`) to the CSS, JS, favicon and carousel image links, so
  browsers never pair a new page with a stale cached file. Keep doing this for any new asset.
- Preview locally: `python3 -m http.server 4173 --directory .` then open http://localhost:4173.

## Color

All colors are tokens in `:root` in `v2/site.css`. Never write a hex value anywhere else.

| Role | Token | Use |
|---|---|---|
| Page | `--paper` `#F5F1E8` | Warm cream page background. Also the favicon tile. |
| Raised | `--paper-raised` `#FBF9F4` | Islands, cards, pill bar, inputs |
| Text | `--ink` / `--ink-muted` | Body text / secondary text |
| Hairline | `--stone` | Decorative dividers only |
| Primary | `--ocean` (`--blue-600` `#003B5C`) | Buttons, links, Contact island, focus ring |
| Deep blue | `--blue-800` `#002442` | Headings, dark bands (promo, newsletter) |
| Accent | `--forest` (`--green-600`) | Eyebrows, small labels |
| Tints | `--blue-50/100`, `--green-50/100/200` | Section washes, hover fills, glass |
| Error | `--error` / `--error-tint` | Invalid form fields only |

**Blue leads, green accents.** Green appears in eyebrows, the light green feature panel
(`--green-50`), and buttons that sit on dark blue (`.btn--light`, `--green-200`). Never make a
large surface green when blue would do.

## Type

- **Display:** Spectral 500 (serif). Hero (`.h-display`, 34–52px) and section titles
  (`.h-section`, 30–44px), always in `--blue-800`.
- **Body:** Manrope 400/600/700. Body 16/26, lede (`.lede`) 17/28 in `--ink-muted`.
- **Eyebrow:** `.eyebrow`, Manrope 700, 12px, uppercase, 0.12em tracking, `--forest`
  (`--ink` in the hero).
- **Mono:** Red Hat Mono 500 for small machine-ish labels (pill bar label, placeholder labels).
- Buttons and text links are uppercase, bold, 12px, 0.1em tracking.

## Shape, space, depth

- Radii: `--radius-sm` 8px (buttons, small cards), `--radius-md` 14px (islands, cards),
  `--radius-lg` 18px (banners, big panels). Pills use 999px.
- Content width `--max` 1440px with `--gutter` clamp(16px, 5vw, 80px). Use `.wrap`.
- Section rhythm `--section-y`: 96px desktop, 64px under 720px.
- One shadow: `--shadow` (soft, ink at 10%). Glass panels use `--glass` plus `backdrop-filter: blur`.

## Components

Live on the homepage now:

- **Island header** (`.hdr`): two floating bubbles 16px from the top. The left one (`.island--nav`)
  holds the logo and tabs, with Industries opening a dropdown panel. The right one
  (`.island--cta`) is the solid blue **Contact →**. Under 1000px the tabs collapse into a menu
  button inside the left island, which opens a rounded panel (`.mmenu`).
- **Hero** (`.hero`): centered eyebrow ("Welcome to Mitre Global") over the serif display line.
- **Photo carousel** (`[data-carousel]`): 6 slides, 5 visible. The center photo is full size and the
  others step down by distance (0.6, 0.8, 1.0). It advances every 5s and has pause, previous and
  next controls. Clicking a side photo centers it, and it can be swiped on touch screens. The
  center slide shows an industry chip at the top and a glass card at the bottom with a one-line
  title, a one-sentence blurb and a small **Learn more →** (`.btn--sm`). Photos are 3:4,
  `object-fit: cover`: **cropped, never stretched**.
- **Pill bar** (`.pills`): white rounded bar with a mono label and underlined uppercase links.
  It scrolls sideways on phones.
- **Promo banner** (`.promo__card`): dark blue rounded card with a gradient or image background,
  a serif headline on the left, and a blurb with a `.btn--light` on the right.
- **Logo marquee** (`.logos`): sits as the bottom row inside the promo card, under a hairline. A
  static label ("Experience working on diverse teams") and logos scrolling in a loop (40s, pauses on
  hover, edges faded). On the dark card the logos are white at 75%. Badge logos (`.logo--badge`)
  invert to light tiles, and light-bodied badges (`.logo--light`) only lose their color. With
  reduced motion it becomes a static row.

- **Offering cards** (`.cards` / `.card`): three 4:5 cards with an animation background, a numbered
  glass chip top-left, and a glass panel bottom-left that reveals its text on hover. They become a
  sideways scroller under 960px.
- **Feature panel** (`.feature`): full-width `--green-50` band, text and button on the left, a large
  rounded visual on the right.
- **Split** (`.split`): a wide photo on the left, eyebrow, headline, lede and button on the right.
- **Contact band** (`.reach`): full-width dark blue band. Eyebrow, headline, lede and a "Prefer
  email?" link on the left; a contact form card on the right (stacks under 860px). Built by
  `reach(eyebrow, headline, lede)` in the builder, so every page that ends with it shares one source.
- **Form** (`.form`, `.field`, `.field__label`, `.field__input`): cream `--paper-raised` card,
  uppercase 12px labels in `--blue-800`, 46px inputs on `--paper` with a `--blue-200` border and a
  blue focus ring. Invalid fields get `aria-invalid="true"` and the `--error` border. Status text
  goes in `.form__status` (`role="status"`). A form with `data-placeholder="form"` validates but
  sends nothing and says so; it is waiting for a backend.

- **Badge** (`.badge`): small dark-blue pill with a pulsing green dot (`.badge__dot`), placed beside an
  eyebrow wrapped in `.eyebrow--row`. For status callouts like "Coming soon". The pulse stops with reduced motion.

Services page (`/services/`):

- **Photo hero** (`.phero--photo` / `.phero__box`): the page hero boxed in a rounded `--radius-lg` card
  inside `.wrap` (not edge to edge), with a cover photo (`.phero__bg`, decorative `alt=""`) under a soft
  `--blue-800` overlay. Text turns light: green eyebrow, cream headline, `--blue-100` lede, `.btn--light`.
  Services uses the water photo (`assets/photos/water.jpg`); Financing uses the glass towers
  (`assets/photos/glass-towers.jpg`) with `.phero--busy`, a heavier overlay for photos with lots of
  bright detail. On the photo the **Badge** turns light (cream pill, dark text).

- **Value tiles** (`.tiles` / `.tile`): three equal quiet cards on `--paper-raised` with a `--stone`
  hairline and `--radius-md`. A mono number in `--forest`, a Manrope 700 title in `--blue-800`, body in
  `--ink-muted`. No images. They stack under 860px.
- **Compact feature** (`.feature--compact`): the green feature band with 60% of the section padding,
  a narrower text column and a shorter 16:9 visual. A spotlight on one idea, usually with no button.
- **Phase stepper** (`.phases`, `data-phases`): the page's centerpiece. On screens 861px and wider,
  `site.js` turns it into ARIA tabs: a pill-bar tablist (mono numbers, uppercase names, active tab
  filled `--ocean`) over one panel, arrow keys / Home / End, and Previous / Next buttons. Panels
  crossfade (0.25s, off under reduced motion). Each panel (`.phase`) is a two-column card: mono label
  (`Phase 01 · Assess`), Spectral title, description, keyword chips (`.tags`, mono on `--blue-50`), an
  optional deliverable line in `--forest` (`.phase__deliv`) and `.more` link, with a 4:3 visual on the
  right. A panel can hold two **path cards** (`.paths` / `.path`) instead of chips and a visual. Under
  861px and without JS, every phase is stacked and visible (visuals hidden on phones); the tablist
  and nav carry `hidden`, which the CSS respects.
- **Ownership band** (`.promo--page`): the promo card with no logo row and no button, on its own in a
  section. A light green eyebrow (`.promo__card .eyebrow`) sits above the headline.
- **FAQ** (`.faq` / `.faq__item`): native `<details>`/`<summary>`, single column up to 800px, `--stone`
  hairlines between items. Questions in Manrope 600 `--blue-800`; a drawn `+` that turns to `−` when
  open; answers in `--ink-muted`. All start closed.

- **Footer** (`.foot`): light, with a serif tagline ("Level up through AI transformation."), a
  two-column nav, and a "How can we help?" block with a Contact button. The bottom row holds the
  logo, © and email.

Removed 2026-10-29: the careers band (`.careers`), markup and CSS in `git show aaa5f82`.

Also styled but not on any page: **duo cards** (`.duo`), two tall image cards with a dark gradient, a serif headline and a light button. Removed from
the homepage 2026-10-29; markup in `git show b91eac5:index.html`.

Financing page (`/financing/`): a coming-soon page. The photo hero (`.phero--photo`) carries the **Badge** beside
its eyebrow (centered), then a small "What's coming" label over four short tiles with a one-line description each (`.tiles--4`:
four across, two under 860px, one under 480px). Still `noindex`.

Careers page (`/careers/`): the standard `.phero` hero, then a slim **role filter** card (`.jobfilter`, `data-jobfilter`): one row of search plus Team / Location / Type
/ Sort selects with `aria-label`s instead of visible labels, and a thin bar with the live count
("0 open roles", `role="status"`) and Clear filters. Roles go in `[data-jobs]` as
`<li data-job data-team data-location data-type data-date data-title>`; `site.js` filters, sorts and
counts them, and shows the "No open roles" banner when none match ("No roles match these filters."
when roles exist but are filtered out). Search gets its own row under 860px; selects go two across
under 560px.

Contact page (`/contact/`): `.phero` hero, then a two-column `.contact` grid: a dark blue info panel
(`.contact__panel`, the promo gradient, a serif line, a short note and the email pinned to the bottom)
beside the shared contact form. Stacks under 860px. The form comes from `contact_form()` in the
builder, the same markup the contact band uses. Still `noindex` until the form is wired up.

Services is built out (see above). The remaining placeholder subpages use `.phero` (centered eyebrow, display title and lede) plus a wide
`.phero__ph` placeholder block.

## Placeholders

Anything not yet supplied is a labeled placeholder, never a fake. Use `.ph` with `.ph--photo` (blue,
`.ph--g` green, `.ph--mix`, `.ph--dark`) or `.ph--anim` (soft blob gradients), and put the label
in `.ph__label` (for example "Animation placeholder: the Manifest"). Placeholder links use
`data-placeholder="link"` so they do nothing when clicked.

## Copy rules

- Plain, confident, short. No em dashes in customer-facing copy.
- Never reuse BCG's wording or imagery. Only the layout is borrowed.
- Every image needs alt text, and decorative duplicates (like the marquee's second row) get `alt=""`.

## Motion

Motion is quiet and purposeful: the carousel step (0.8s ease-out), the dropdown fade, the marquee.
Everything respects `prefers-reduced-motion`. The carousel starts paused and the marquee stops.

## Favicon

The blue M at 70% on a rounded cream tile (`favicon.svg`, `favicon-32.png`). The 180px
`apple-touch-icon.png` stays square because iOS rounds it. This keeps the icon visible on dark tabs.

## Visuals and animation (in progress)

The language for the six animation placeholders and any future brand graphics. Sections marked
**Decided** are settled; **Open** is still being worked out. Update this as decisions land.

### Decided

- **Water and glass are core brand materials.** Water surfaces and waves; glass on buildings and
  inside warehouses; anything that slightly refracts or distorts light or the image behind it. The
  deep blues and sea greens of water and glass are part of the identity, and the photography already
  leans on them (`water.jpg`, `glass-towers.jpg`). Keep returning to these materials.
- **Weighted, not dainty.** Lines and shapes are solid and carry weight. Take stroke weight cues
  from the M mark's stems, not hairlines.
- **Light-touch metaphor.** Borrow a little from the mitre gate: chevrons, levels, flow. No literal
  canal-lock scenes or illustrations.
- **Quiet, on palette.** Core tokens only (blues lead, greens accent, cream ground). Visuals should
  feel like they live inside the site, never loud or attention-grabbing.
- **Stills first, motion second.** Every visual is first approved as a static image. Motion, a
  distortion effect or 3D is a layer added on top of an approved still, never designed from scratch.
- **Some movement is wanted**, either inside the visual or as a water/glass distortion over it.
  Keep it simple at first. Respect `prefers-reduced-motion` (show the still).
- **One shared world.** Placeholders 1 to 4 tell one story (sources, data layer, what's built on it,
  results). Recurring objects (a source, the data layer, an agent/app, a metric) look the same in
  every visual they appear in.

### The six placeholders

| # | Visual | Where | Container |
|---|---|---|---|
| 1 | Opportunities ranked by return (Assess) | Home + industry offering card 01; Services phase 01 | 4:5 card background, and 4:3 phase visual |
| 2 | Scattered sources flowing into one data layer (Unify) | Services phase 02 | 4:3 phase visual |
| 3 | Agents and apps built on the data layer (Build) | Offering card 02; Services phase 03 | 4:5 card background, and 4:3 phase visual |
| 4 | Scorecard against the baseline (Prove) | Offering card 03; Services phase 04 | 4:5 card background, and 4:3 phase visual |
| 5 | Vendor tools consolidating into one owned system | Services compact feature | 16:9, on the `--green-50` band |
| 6 | Trade financing | Home feature panel | Large rounded visual on the `--green-50` band |

Layout constraints: on offering cards the visual is a background under a glass chip (top-left) and
a glass text panel (bottom-left), so keep the subject clear of those corners and make sure it reads
through `backdrop-filter: blur`. Visuals 1, 3 and 4 must compose for both 4:5 and 4:3. Phase visuals
are hidden on phones.

### Open

- References (Colton gathering examples).
- Abstraction level: schematic diagram, product-like UI, or schematic with realistic mono labels.
- How water/glass shows up: as the subject, as a material the diagram sits behind, or as a
  distortion layer over a still.
- Exact stroke weights, corner radii and color roles inside visuals.
- Medium for stills (code-drawn SVG vs rendered image) and for the motion layer.
