# Mitre site design language

The house style for mitregate.com. New sections and pages should be built from what is here,
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
  email?" link on the left; a contact form card on the right (stacks under 860px).
- **Form** (`.form`, `.field`, `.field__label`, `.field__input`): cream `--paper-raised` card,
  uppercase 12px labels in `--blue-800`, 46px inputs on `--paper` with a `--blue-200` border and a
  blue focus ring. Invalid fields get `aria-invalid="true"` and the `--error` border. Status text
  goes in `.form__status` (`role="status"`). A form with `data-placeholder="form"` validates but
  sends nothing and says so; it is waiting for a backend.

- **Badge** (`.badge`): small dark-blue pill with a pulsing green dot (`.badge__dot`), placed beside an
  eyebrow wrapped in `.eyebrow--row`. For status callouts like "Coming soon". The pulse stops with reduced motion.

- **Footer** (`.foot`): light, with a serif tagline ("Level up through AI transformation."), a
  two-column nav, and a "How can we help?" block with a Contact button. The bottom row holds the
  logo, © and email.

Removed 2026-10-29: the careers band (`.careers`), markup and CSS in `git show aaa5f82`.

Also styled but not on any page: **duo cards** (`.duo`), two tall image cards with a dark gradient, a serif headline and a light button. Removed from
the homepage 2026-10-29; markup in `git show b91eac5:index.html`.

Placeholder subpages use `.phero` (centered eyebrow, display title and lede) plus a wide
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
