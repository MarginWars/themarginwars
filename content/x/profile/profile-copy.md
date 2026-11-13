---
id: x-profile-2026-11
channel: x
kind: profile
status: draft
owner: channels
approvals: {}
sources: []
---

# The Margin Wars — @marginwars profile suite

**Status: drafts and QA mocks only. Nothing has been uploaded, posted or changed on X, LinkedIn or anywhere else.** Prepared 11 Nov 2026. Soft launch still applies: Avi approves before any of this goes live.

Handle is already @marginwars (renamed from @themarginwars). The account has 0 posts and a blank profile. This folder is the proposed full suite: avatar, header, profile fields and a pinned intro draft.

---

## Display name

The Margin Wars

15 characters (X allows 50). Same as the site and the LinkedIn page name.

---

## Bio (max 160 characters)

**Recommended (81 characters)**

> Nobody loses margin on the rate. Payments tactics for the line items nobody owns.

Source: the approved LinkedIn tagline proposal in `linkedin_page_1110/engaging_proposal.md`, itself built from the live site H1 (“Nobody loses margin on the rate. You lose it in the line items nobody owns.”) and the “payments tactics” positioning. No new claims.

**Alternate 1 (105 characters)** — site H1 plus the official slogan.

> Nobody loses margin on the rate. You lose it in the line items nobody owns. Tactics from the front lines.

Source: home H1, plus the Organization slogan “Payments tactics from the front lines.”

**Alternate 2 (109 characters)** — slogan, line items, cross-market.

> Payments tactics from the front lines. For the line items nobody owns, across the US, UK/EU, Africa and APAC.

Source: slogan, home H1, and the public market list already used on the site and LinkedIn about (“US, UK/EU, Africa and APAC”).

On a 600px desktop mock the recommended bio wraps so the last word, “owns.”, sits alone on the second line. X’s live bio width may differ. The wording is left as the approved tagline rather than rewritten to fix the wrap.

---

## Website

https://themarginwars.com/?utm_source=x&utm_medium=social&utm_campaign=always-on&utm_content=profile-link

Registry id: `always-on-x-profile-link` in `marketing/links.csv`. Destination is the home page. X will likely display the domain only (`themarginwars.com`); the UTM tags stay on the URL.

---

## Location

Leave blank.

The brand docs are explicit: the site does not state a registered company headquarters, and Palo Alto is Avi’s location, not a stated company office (`linkedin_page_1110/about.md`). Nothing public is added here.

---

## Pinned intro (draft, max 280 characters)

Not posted. Needs Avi’s go. Destination is Insights (`/warroom`), so the profile website (home) and the pinned post can be told apart in analytics. Same tagging convention as the LinkedIn page button, which already points at `/warroom`.

X counts each http(s) URL as 23 characters. Both raw length and that X-weighted length are given. Both drafts sit under 280 either way.

**Recommended (164 characters of copy + URL; raw 276, X-weighted 187)**

> Nobody loses margin on the rate. You lose it in the line items nobody owns.
>
> Payments tactics from the front lines, each shown for the US, UK/EU, Africa and APAC.
>
> https://themarginwars.com/warroom?utm_source=x&utm_medium=social&utm_campaign=always-on&utm_content=pinned-intro

Source: live home H1, the official slogan, and “Each shown for US, UK/EU, Africa and APAC” from the public about copy. Quiet positioning, not a launch announcement.

**Alternate (135 characters of copy + URL; raw 247, X-weighted 158)**

> Payments tactics for the line items nobody owns. Mechanics, an owner, failure modes, and a column for the US, UK/EU, Africa and APAC.
>
> https://themarginwars.com/warroom?utm_source=x&utm_medium=social&utm_campaign=always-on&utm_content=pinned-intro

Source: the tagline, the Insights lede (“mechanics, owner, failure modes, four markets”), and the about line on the cross-continent campaign column. No counts of moves, no new claims.

Registry id: `always-on-x-pinned-intro` in `marketing/links.csv`.

---

## Assets (upload these; the rest are QA only)

| File | Use |
|---|---|
| `avatar_400.png` | X profile photo, 400×400. Same M mark as the LinkedIn page logo (ink field, six-colour ledger rule, paper M). X will crop it to a circle. |
| `header_1500x500.png` | X header, 1500×500. Paper `#F4F6F7`, six-colour band, no text — same language as the clean LinkedIn cover. |
| `header_3000x1000.png` | Same header at 2×, for a crisp upload if X accepts it. |

The header is text-free on purpose, after the LinkedIn cover text was hidden by the logo and the crop. The six-colour band sits at the top of X’s centre 1500×360 safe area (y=70, 24px tall at 1×; y=140, 48px at 2×), so it survives the mobile top/bottom crop and stays clear of the bottom-left avatar. On desktop that reads as a ledger margin: a short paper inset, then the rule. Six equal segments, 250px (1×) / 500px (2×), in the approved cycle: sky, violet, mint, grey, gold, coral.

---

## QA mocks (not for upload)

| File | What it shows |
|---|---|
| `qa/avatar_circle_400.png` | Circle crop at 400px (transparent corners). |
| `qa/avatar_circle_48.png` | Circle crop at 48px, X’s mid sidebar size. |
| `qa/avatar_circle_32.png` | Circle crop at 32px, smallest frequent size. The six-colour rule and the M still read. |
| `qa/avatar_safe_circle.png` | Square mark with the inscribed X circle (coral), the 78% safe radius the mark was built for (mint), and the content bounding box (gold). Content stays 36.6px inside the crop circle (max radius 163.4 of 200). The rule’s outer corners sit a little outside the 78% ring (ratio 0.817) and well inside the crop. |
| `qa/avatar_sizes_sheet.png` | Square and circle 400, plus 48 and 32 on paper, white (X chrome) and ink. |
| `qa/header_desktop_600.png` | 600px-wide profile column, full 1500×500 header, 135px avatar at left 15px overlapping the lower 70px, recommended bio. Labelled “not live”. |
| `qa/header_mobile_390.png` | 390px column, banner cropped to the centre 1500×360, 80px avatar. The band sits at the top of what remains visible. Labelled “not live”. |
| `qa/header_safezone.png` | 1500×500 source with the mobile crop, the 1500×360 safe rectangle, and the desktop avatar overlap marked. |
| `qa/measurements.json`, `qa/qa_log.txt` | Measured sizes, band segments, circle margins. Final pass: no deviations. |
| `gen.py` | Reproducible generator. Reuses `linkedin_page_1110/gen.py` `render_mark()`. |

---

## QA, in the spirit of the spacing and symmetry checks

Checked: avatar at 400 / 48 / 32, header at 1500×500 and 3000×1000, desktop mock at 600, mobile mock at 390, plus the safe-zone and circle-crop guides. Visual pass and a measurement script (band position, height, segment widths, colours, paper field, circle margin, band-colour survival at 32 and 48).

**Pass, after two fixes found on the first visual pass:**

1. A 16px source band (LinkedIn-proportional) displayed as only ~4px on the 390px mobile crop and almost disappeared under the mock chrome. Thickened to 24px at 1× (48px at 2×): 9.6px on the 600px desktop column, 6.2px on the mobile crop. Still a slim ledger rule, now readable at both sizes. Segments stayed exactly equal (250 / 500). The band remains fully inside the safe area and clear of the avatar.
2. The first safe-zone guide put the avatar overlay and the bottom crop tint on top of the caption. Overlays are now clipped to the header, and the caption sits on a clear bar below. Mock “not live” labels were also moved from the top of the profile column to the bottom, so they no longer sit on the band.

No clipping of the mark in the circle crop. No gaps in the band. Left and right edges of the band are flush (full width, by design). Sibling band segments are the same width (delta 0). Nothing important lives in the bottom-left avatar overlap or in the mobile top/bottom crop.

Devices not tested for real: a physical iPhone or Android X app. Mobile crop is the conservative centre 1500×360 described in the brief, not a live device screenshot. If the live app crops less, more of the paper inset above the band will show; the band itself stays in view.

---

## links.csv rows added

```
always-on-x-profile-link,https://themarginwars.com/,x,social,always-on,profile-link,,https://themarginwars.com/?utm_source=x&utm_medium=social&utm_campaign=always-on&utm_content=profile-link,avi,active,2026-11-11,X @marginwars profile website field. Reserved; not live until Avi approves.
always-on-x-pinned-intro,https://themarginwars.com/warroom,x,social,always-on,pinned-intro,,https://themarginwars.com/warroom?utm_source=x&utm_medium=social&utm_campaign=always-on&utm_content=pinned-intro,avi,active,2026-11-11,X @marginwars pinned intro post draft. Reserved; not posted until Avi approves.
```

Minted with `marketing/mint_link.py`. Status is `active` on the reserved URL; the profile field and the post themselves are not live.
