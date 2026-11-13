# Brand

The Margin Wars brand as the site ships it. The site is the source of truth: tokens live in
`site/src/assets/suite.css` and `site/src/assets/calm.css`, and the generator for the logo and channel assets is
`site/layers/brand_logo/gen.py`. Use this page when you make anything else: repo images, channel art, decks.

<img src="../.github/assets/band.svg" width="100%" height="4" alt="">

## Logo

| Asset | Use |
| --- | --- |
| [`logo/lockup_light.svg`](logo/lockup_light.svg), [`logo/lockup_dark.svg`](logo/lockup_dark.svg) | Stacked wordmark with the magenta ledger rule, on light or dark surfaces |
| [`logo/mark32_light.svg`](logo/mark32_light.svg), [`logo/mark32_dark.svg`](logo/mark32_dark.svg) | Small mark (favicon size) |
| [`channel-assets/mark400.svg`](channel-assets/mark400.svg) | The banded M mark: avatars and profile images (built for a circle crop) |
| [`channel-assets/`](channel-assets) | Banners, avatars and cover images per channel |

The wordmark is always "The Margin Wars", set in Schibsted Grotesk, with the magenta rule on its left edge.

## Colour

Surfaces stay neutral. Colour marks an action or a state, and each accent keeps one job.

| Role | Colour | Text-safe shade (WCAG AA) | Job |
| --- | --- | --- | --- |
| Ink | `#111417` | | Text, dark surfaces |
| Paper | `#F4F6F7`, white `#FFFFFF` | | Surfaces |
| Rule | `#DDE1E4` | | Borders and dividers |
| Magenta | `#B5237F` | `#9A1C6B` | Calls to action that lead to Contact, and the wordmark rule. Nothing else |
| Sky | `#8FB0E0` | `#2E5A96` | Links, hover, keylines, eyebrow ticks, open disclosures |
| Mint | `#3FBF85` | `#1C7148` | Selected, current, success, live |
| Gold | `#D2A63A` | `#7D5B0E` | Focus ring and featured items only |
| Coral | `#EA6259` | `#A8342B` | Deadlines, alerts, new |
| Violet | `#A08FE6` | `#5250D8` | Band segment and the role-colour cycle |
| Grey | `#B7C1C9` | `#4A555B` | Band segment, muted text |

## The six-colour band

The site's signature: six equal segments in this order, sky `#8FB0E0`, violet `#A08FE6`, mint `#3FBF85`,
grey `#B7C1C9`, gold `#D2A63A`, coral `#EA6259`. It sits pinned to the top edge of every page (6px, 4px under
768px) and marks eyebrows, section keylines and hero edges. Repeated items take the six colours in turn.
In Markdown, use [`.github/assets/band.svg`](../.github/assets/band.svg) as a divider.

## Type

| Face | Use | Files |
| --- | --- | --- |
| Schibsted Grotesk | Headings, body, the wordmark | `site/layers/buildout/fonts_src/`, `site/layers/brand_logo/fonts/` |
| Martian Mono | Eyebrows (uppercase, wide tracking), numbers, code and URLs | Same folders |

Both fonts are licensed under the SIL Open Font License 1.1.

## Voice

A payments operator talking to payments and finance leaders. Tactics, not themes: one move per piece, with the
mechanics, the metric, the failure mode and the owner. Plain and precise. Cross-market by default (US, UK/EU,
Africa, APAC). No hype, no predictions for applause, and no invented facts: every number cites
[`facts/`](../facts) or is marked as an assumption. The long form is in [`docs/`](docs).

## Repo assets

[`.github/assets/`](../.github/assets) holds the README banners and change-flow diagram (light and dark), the band divider, the GitHub
social preview (1280×640) and the organisation avatar (500×500). They are rendered from
[`.github/assets/src/`](../.github/assets/src) with the site's fonts and tokens:
`python3 .github/assets/src/render.py`.
