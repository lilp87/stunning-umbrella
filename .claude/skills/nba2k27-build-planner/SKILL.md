---
name: nba2k27-build-planner
description: Plan, verify, or re-tune an NBA 2K27 MyPLAYER build (attributes, badges, badge tokens, synergy, takeovers, cap breakers, jumpshot, dribble/dunk animations). Use when the user asks for a 2K27 build, asks whether the build in NBA2K27-ULTIMATE-BUILD.md still holds after a patch, or wants a build for a different position/height.
---

# NBA 2K27 build planner

The repo's current build lives in `NBA2K27-ULTIMATE-BUILD.md` (Hebrew, game terms in English).
Breakpoint data collected so far is in `references/breakpoints.md`.

## Workflow

1. **Check the patch first.** Search for the latest NBA 2K27 patch notes (official page:
   https://nba.2k.com/2k27/patch-updates/) and note any change to shooting, contests, steals,
   dunks, takeovers, badge thresholds, or animation requirements since the date in the build file.
2. **Lock the frame before points.** Height, weight and wingspan set every attribute cap,
   badge eligibility and token cost in 2K27. Pick the frame from the role, then confirm the caps
   the build depends on (e.g. 91 3PT for Zip Code, 83 Speed With Ball for the LaVine style).
3. **Build to breakpoints, not round numbers.** Every attribute target must name what it unlocks
   (badge tier, takeover, animation). If a number unlocks nothing, its points go elsewhere.
   Use `references/breakpoints.md`; when sources disagree, take the stricter value.
4. **Write a cut order.** The point pool is fixed, so list which attributes drop first if the
   builder runs out, and which are never cut.
5. **Badges = 20 slots paid with tokens.** Order them in two waves (core first). Put the most
   expensive, most-used badges in Synergy Fuse slots; Legend is only reachable via Synergy.
6. **One takeover per discipline** (Shooting, Finishing, Playmaking, Defense, Rebounding).
   Re-check patch notes for takeover nerfs before recommending one.
7. **Cap breakers:** max 5 per attribute, irreversible, previewable in the builder. Order them
   by the next breakpoint each one reaches.
8. **Jumpshot / dribble / dunks:** give base + releases + blend + speed + cue, and every
   animation's rating and height gate. Tell the player to confirm an A/A+ release window grade.
9. **Be honest about sources.** 2K publishes no official threshold tables; community sites
   (nba2klab, lockercodes, Operation Sports, games.gg, timesaver) are the data. Several guide sites
   sell VC/MT — cross-check them. End with an in-game verification checklist and a source list.

## Research notes

- Many 2K data sites are blocked by this environment's network egress policy for WebFetch;
  WebSearch still returns their content. Prefer `mode: "extended"` for 2K27-specific queries.
- After updating the build, keep `references/breakpoints.md` in sync with any new numbers.
