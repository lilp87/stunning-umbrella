---
name: nba2k27-build-planner
description: Plan, verify, or re-tune an NBA 2K27 MyPLAYER build (attributes, 99-OVR budget, badges, badge tokens, synergy, takeovers, cap breakers, jumpshot, dribble/dunk animations). Use when the user asks for a 2K27 build, asks whether the build in NBA2K27-ULTIMATE-BUILD.md still holds after a patch, or wants a build for a different position/height.
---

# NBA 2K27 build planner

The repo's current build lives in `NBA2K27-ULTIMATE-BUILD.md` (Hebrew, game terms in English).
Collected data is in `references/breakpoints.md`. Tools are in `scripts/`:

- `scripts/evaluator.py` – fitted model of the builder budget (Overall Potential ≤ 99).
  `python3 scripts/evaluator.py '{"position":"PG","height_in":79,"weight":192,"wingspan_in":79,"attrs":{"CS":70,...all 21...}}'`
  prints linked-rule raises, estimated uncapped OVR `u` (builder rejects u > 99.0, shows round(u)),
  verdict, and +1 cost per attribute. `--selftest` replays the live readings, `--about` explains the method.
  Live-calibrated only at 6'7" (sd ≈ 0.75); 6'4"–6'6" and 6'8" are fitted on saved builds only.
- `scripts/sharelink.py` – encode/decode lockercodes builder share links, so a build can be opened
  (and checked) in the live builder: `python3 scripts/sharelink.py encode PG 79 192 79 CS=70 ... VRT=75`.

## Workflow

1. **Check the patch first.** Read https://nba.2k.com/2k27/patch-updates/ (fresh, not cached) and
   note changes since the date in the build file to shooting, contests, steals, dunks, takeovers,
   badge thresholds or animation requirements.
2. **Lock the frame before points.** Height, weight and wingspan set every cap. Cap breakers can never
   exceed a body cap. Key facts at 6'7" PG: 3PT cap depends on wingspan (6'7" → 92, 6'8" → 90),
   SWB cap 83 only up to 192 lb, BH cap 91, PD cap 87, BLK cap 70.
3. **Respect the budget and linked floors.** The budget is Overall Potential ≤ 99, not a point pool;
   per-point cost rises steeply with rating (3PT/BH/PD/SPD/AGI expensive, DD/SD/PC/ID/rebounding cheap).
   The builder auto-raises "follower" ratings (e.g. CS ≥ DL−10 and ≥ MID−15, DL ≥ BH−15,
   PC ≥ BH−40, SD ≥ DD−50, ID ≥ STL−35 and ≥ PD−44, FT ≥ 3PT−20, OREB ≥ DREB−25 at 6'7").
   Run the evaluator, keep u ≤ ~98.4 for safety, and publish a cut ladder.
4. **Build to breakpoints.** Every attribute value must name what it unlocks (badge tier, takeover,
   animation) or be a linked floor. Use `references/breakpoints.md`; when sources disagree take the
   stricter value and flag it.
5. **Badges = 20 slots paid with tokens**, per-discipline maxima (Finishing 24, Shooting 23,
   Playmaking 23, Defense 22, Rebounding 15, Physicals 15), tokens from BASE ratings. Check the max
   tier reachable at the height (nba2klab badge-max-level-by-height). Prefer lab-measured value per
   token (e.g. Limitless Range Silver ≈ Bronze; Set and Fire Bronze gets most of the gain).
   Synergy (Fuse frees the badge's tokens) is earned over time; Season Synergy expires each season.
6. **One takeover per discipline**; re-check patch notes for takeover changes.
7. **Cap breakers:** max 5 per attribute, irreversible, only up to body caps; preview appears at 99 OVR.
   Physicals breakers are disputed – order Finishing/Playmaking/Shooting first.
8. **Jumpshot / dribble / dunks:** prefer measured data (2kjumpers ms tests, nba2klab tests) over
   blog recipes. Give base + releases + blend + cue + gate, a backup that survives the cut ladder,
   and shot-meter/release-speed advice from the lab tests.
9. **Verify live if at all possible.** Encode the build with `sharelink.py` and open it in the
   lockercodes builder (a rejected link falls back to defaults with "That shared build is not legal
   under current tuning"). Automated access needs a stealth browser (Cloudflare/anti-bot).
10. **Compare frames explicitly.** Sweep heights 6'2"–6'10" (and bigs/small guards qualitatively),
    score with several weightings (shooter / two-way / slasher), shift uncalibrated budgets by
    +0.5–1.5 OVR, vary the value of height, and report a regret table and the break-even height value.
    Only frames with exact caps count; reject extrapolated caps that fail the evaluator.
11. **Cap breakers and exploits:** follow the rules in references; list exploits separately with
    ban-risk labels and never include them in a build.
12. **Be honest about sources.** 2K publishes no threshold tables; nba2klab/lockercodes/2kjumpers are
    the best data; several guide sites sell VC/MT. End with an in-game checklist and sources.

## Research notes

- WebFetch is blocked for most 2K sites in this environment; the TinyFish connector
  (`mcp__TinyFish__fetch_content`, free) reads them, and vidIQ gives YouTube transcripts (credit-limited).
- Steam news for NBA 2K27 is app id 4356430 (2878980 is NBA 2K25).
- After updating the build, keep `references/breakpoints.md` and the evaluator data in sync.
