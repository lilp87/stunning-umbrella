# NBA 2K27 breakpoints (collected 2026-10-08, patch v2.0)

Tiers are Bronze / Silver / Gold / Hall of Fame. "+" = both required (AND), "or" = either.
Badge thresholds: four trackers (2kmyplayer, 2kfilmroom, nba2klab, filmroom.gg) agree; measured on
the 2026-08-22 builder build. Where sources disagreed the stricter value is listed and the
alternative noted. Caps and budget readings come from the live lockercodes builder (2026-10-08).

## Builder mechanics

- 53 badges (19 new, 6 cut vs 2K26's 40). 20 badge slots, filled with Badge Tokens. Token and
  slot totals use BASE ratings (cap breakers do not add tokens).
- Default max tokens per discipline (Mike Wang): Finishing 24, Shooting 23, Playmaking 23,
  Defense 22, Rebounding 15, Physicals 15. Tokens come from discipline meters, Team Practice,
  Gatorade workouts, Build Specialization (9 flexible tokens), Season and Crew rewards.
  Discipline tokens stay in their discipline.
- Cumulative token cost B/S/G/HoF (nba2klab = filmroom.gg):
  - 3/5/6/7: Deadeye, Limitless Range, Arc Cadence, Quick Trigger, Smooth Operator, Ankle Assassin,
    Lightning Launch, Unpluckable, Challenger, Pick Dodger, Seatbelt, Posterizer, Layup Mixmaster,
    Float Game, Flash.
  - 2/4/5/6: Set and Fire, Static Middy, Handles for Days, Pace, Versatile Visionary, Glove,
    Interceptor, Ankle Braces, Physical Finisher, Slippery Off-Ball, Work Horse, Strong Handle.
  - 1/3/4/5: Dimer, Aerial Wizard, Off-Ball Pest, Immovable Enforcer, Pogo Stick, Mini Marksman,
    Paint Prodigy, Ghost Stepper. (High-Flying Denier Bronze 1, Paint Patroller Bronze 3,
    Bruiser Bronze 2, Sync Snatcher Bronze 1.)
- Synergy: 16 slots (12 × Max +1, 4 × Max +2). Fuse = boost for the whole game and frees the
  badge's tokens. Reaction = paired to a Fuse badge, triggers after N activations, uses a badge
  slot. Legend only via Synergy. Season-reward Synergy expires at season end; Build Spec goal 10
  (+2, Fuse must match the spec discipline), Crew 28/39 and REP Synergy are permanent.
- Loadouts: 1 by default, up to 4 (REP, Challenges, Crews), switchable before a game.
- Cap Breakers: 28 total (11 REP, 4 Crew, 2 Build Spec goal 9 — locked to the spec discipline or
  FT, 2 Lifetime, 9 Seasons); max 5 per attribute; permanent; cannot exceed body caps; gain per
  breaker shrinks as the rating rises (+1 near the cap). Preview appears only at 99 OVR.
  Physicals breakers: lockercodes allows, nba2klab builder video says no — unresolved.
- Rebirth: Tier I releases 25% of default tokens, Tier IV all of them.
- Takeovers: 5 disciplines, 19 abilities + 5 defaults. Discipline levels unlock in order:
  Rebounding (1), Finishing (2), Playmaking (3), Defense (4), Shooting (5).

## Budget (Overall Potential ≤ 99)

- No fixed point pool: Overall Potential is capped at 99; the builder rejects builds whose
  uncapped overall exceeds 99.0 and shows round(u) otherwise. Overall depends on height and
  attributes only (position/weight/wingspan only change caps). See `scripts/evaluator.py`.
- Linked floors the live builder enforces at 6'7" (auto-raise): CS ≥ DL−10 and ≥ MID−15,
  DL ≥ BH−15, PC ≥ BH−40, SD ≥ DD−50, ID ≥ STL−35 and ≥ PD−44, FT ≥ 3PT−20, OREB ≥ DREB−25,
  SPD ≥ SWB−4, DREB ≥ PD−40, PASS ≥ BH−25.
- Live reading (PG 6'3" 213/6'3", 2026-10-09): `CS80 DL72 DD89 SD35 PC32 MID85 3PT94 FT69 PASS62 BH87
  SWB88 ID59 PD85 STL83 BLK35 OREB35 DREB60 SPD87 AGI81 STR89 VRT78` → 98, room ~1 (loaded unchanged).
- Live readings (PG 6'7" 192/6'7"): repo build `CS70 DL71 DD87 SD37 PC46 MID85 3PT92 FT72 PASS70
  BH86 SWB83 ID60 PD85 STL77 BLK70 OREB30 DREB55 SPD85 AGI77 STR71 VRT75` → 98 (loaded unchanged).
  The 2026-10-08 first draft (3PT92 DD89 PD86 DL85 PASS80 …) was rejected, as were 3PT 88/90 + DD 85
  variants; 3PT 87 + DD 85 loaded at 98.

## Cap breaker rules and exploits (researched 2026-10-09)

- Official: max 5 per attribute, permanent, no respec, never above the body cap. Build Spec goal-9
  CBs go only to that discipline or FT (not Physicals, unlike 2K26). General CBs on Physicals are
  very likely allowed (the Physicals track pays Physicals CBs; lockercodes models them).
- Eligibility (badges, takeovers, animations) uses CB-raised ratings; tokens and slots use BASE
  ratings. The CB screen reportedly needs the build at 99 OVR (unconfirmed) → always plan a fill-to-99.
- 2K: a CB adds +1 to your highest ratings and more to low ones, so ladders depend on the whole build.
  PG 6'7" is the least CB-generous guard frame (+1 on 3PT/BH/SWB/PD/STL/SPD/AGI); low-base Driving Dunk
  (61-64 → 89-90 with 5 CBs) is the one big legal win there. At 6'3" it is not worth it.
- Exploits: crew kick/re-level CB duplication (breaks "crew CBs earned once" — ban/rollback risk);
  account sharing / paid grinding, scripts, VC/account trading (ban waves). Never put these in a build.
- Season 1 level-40 CB must be earned before 2026-10-16 (catch-up CBs only for unplayed seasons).

## Model notes

- Every one of 3,591 saved builds satisfies MID ≥ 3PT − 10 (all heights); the evaluator does not
  enforce it at 6'2"/6'3"/6'7" — apply it by hand.
- Out of sample (31 saved pages with OVR) the evaluator reads low by 0.47 on average, worst −2.05
  at 6'5" and long wingspans; ≈ −0.1 at 6'3"; 6'7" is calibrated.
- Frame choice is sensitive to how much height is worth in contests (no lab test after v2.0).
  Always report the break-even height value and a regret table across weightings.

## Frame caps (live lockercodes builder)

| Frame | 3PT | MID | DL | DD | BH | SWB | PASS | PD | STL | BLK | SPD | AGI | STR | VRT |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| PG 6'7" 192 / 6'7" WS | 92 | 98 | 92 | 90 | 91 | 83 | 99 | 87 | 88 | 70 | 91 | 89 | 82 | 98 |
| PG 6'7" 180 / 6'7" | 92 | 98 | 92 | 90 | 91 | 83 | 99 | 87 | 88 | 70 | 91 | 91 | 76 | 99 |
| PG 6'7" 200 / 6'7" | 92 | 98 | 92 | 90 | 91 | 82 | 99 | 88 | 88 | 70 | 90 | 88 | 86 | 98 |
| PG 6'7" 180 / 6'8" | 90 | 96 | 94 | 92 | 91 | 83 | – | 89 | 91 | 73 | 91 | 91 | 75 | 99 |
| PG 6'7" 180 / 6'10" | 87 | 93 | 99 | 96 | 91 | 83 | – | 93 | 95 | 79 | 91 | 91 | 73 | 99 |
| PG 6'3" 213 / 6'3" | 99 | – | – | 90 | 97 | 91 | – | – | – | 59 | – | – | 89 | – |
| PG 6'4" 175 / 6'4" | 99 | 99 | 92 | 90 | 96 | 91 | – | 87 | 92 | – | 99 | 99 | 60 | 99 |
| SG 6'5" 183 / 6'5" | 99 | 99 | 92 | 90 | 95 | 89 | – | 88 | 92 | – | 97 | 96 | 70 | 99 |
| SG 6'5" 222 / 6'8" | 93 | – | – | 95 | 95 | 88 | – | – | – | 67 | – | – | 89 | – |
| PG 6'5" 228 / 6'10" | 89 | 92 | 99 | 99 | 95 | 87 | 99 | 99 | 99 | – | 95 | 90 | 89 | 98 |
| SF 6'8" 190 / 6'8" | 92 | 97 | 92 | 88 | 86 | 80 | – | 87 | 84 | – | 88 | 88 | 81 | – |

- 6'7" PG 3PT cap by wingspan: 6'7" 92, 6'8" 90, 6'9" 88, 6'10" 87, 6'11" 85, 7'0" 83, 7'1" 81.
- 2K Signature Blueprint caps list higher DD/PD than the custom builder (e.g. 6'7"/206/6'7" DD 95,
  PD 96) — trust the custom builder.

## Max badge tier reachable by attributes (nba2klab, all 18,935 combos)

- 6'7": Limitless Range, Ankle Assassin, Lightning Launch, Pace → Silver; Deadeye, Quick Trigger,
  Set and Fire, Arc Cadence, Smooth Operator, Handles for Days, Ankle Braces, Slippery, Flash → Gold.
- 6'5"–6'6": LR, AA, LL one tier higher; at 6'6" Deadeye/QT/Smooth Operator/Ankle Braces/Flash/
  Slippery reach HoF.

## Lab tests (nba2klab, pre-v2.0)

- Limitless Range at 27 ft: none 35.4%, Bronze 40.2%, Silver 39.8%, Gold 46.2%.
- Set and Fire: none 57.6%, Bronze 64.65%, Gold 67.45%. Static Middy stand-still mids: none 46.67%,
  Gold 58.78% (also boosts stand-still 3s near the line/corner).
- Deadeye semi-open: none 60.5, S 63, G 64.25, HoF 69.25%. Arc Cadence moving 3s: none 39%, G 43.6%.
- Quick Trigger: no-dips unbadged 33.1% vs normal 50.4% (needs Gold+).
- Lightning Launch / Pace boost: 4/5/8/9/14% (B/S/G/HoF/Legend).
- Handles for Days stamina drain: Silver −23.4%, Gold −39.5%. Dimer Silver: teammates' C&S +3.1 pts.
- Shot meter off: +10.0% (all on late releases). Release speed vs Normal: Quick −8.5%,
  Very Quick −12.1%, Slow/Very Slow +1.1% (noise); ~15 ms per notch.
- Speed/Agility: 85 best stopping point; 76–83 dead zone. Calibrated +15.2 pts (date unknown).

## Takeovers

| Takeover | Discipline | Requirement |
|---|---|---|
| Shot Artist | Shooting | 89 3PT or MID (nerfed v1.3) |
| Calibrated | Shooting | 85 3PT or MID (nerfed v1.3) |
| Zip Code | Shooting | 91 3PT |
| Navigator | Finishing | 85 Driving Layup |
| Airspace | Finishing | 87 DD + 75 VRT (output cut in 2.0, countered by Rim Guardian) |
| Inside Touch | Finishing | 85 Close Shot |
| Detonator | Finishing | 85 Standing Dunk (output cut in 2.0) |
| Paint Surgeon | Finishing | 80 Close Shot + 75 Post Control |
| Blur | Playmaking | 85 Ball Handle + 80 Speed With Ball |
| Cook | Playmaking | 90 Ball Handle |
| Dishmaster | Playmaking | 80 Pass Accuracy |
| Glue | Defense | 85 Perimeter D |
| Hawk | Defense | 85 Steal |
| Rim Guardian | Defense | 80 Interior D (+ Block per 2K producer) |
| Muscle | Rebounding | 80 OREB + 80 DREB + 80 STR |
| See The Future | Rebounding | DREB + OREB |
| Hydration Hero | any | no rating, Progression Level 6 |

## Shooting badges

| Badge | Attribute | Tiers | Height |
|---|---|---|---|
| Deadeye | 3PT or MID | 65/85/92/99 | any |
| Set and Fire | 3PT | 60/78/89/97 | any |
| Limitless Range | 3PT | 83/89/93/99 | any |
| Arc Cadence | 3PT | 70/86/91/98 | ≤ 6'11" |
| Quick Trigger | 3PT or MID | 80/88/95/99 | any |
| Smooth Operator | MID | 70/87/93/99 | any |
| Static Middy | MID | 55/75/85/95 (single source) | any |
| Mini Marksman | 3PT or MID | 60/79/94/99 | ≤ 6'4" |

## Finishing badges

| Badge | Attribute | Tiers | Height |
|---|---|---|---|
| Posterizer | DD + VRT | 73+65 / 87+75 / 93+80 / 99+90 (Destructoid HoF: 96+85) | any |
| Physical Finisher | DL + STR | 60+60 / 80+70 / 90+80 / 96+90 | any |
| Rise Up | SD + VRT | 60+55 / 81+62 / 90+66 / 99+70 (Destructoid Bronze 72+60) | ≥ 6'5" |
| Aerial Wizard | DD or SD | 60/70/80/94 (SD 93 HoF) | any |
| Float Game | CS or DL | CS 65/80/90/96, DL 65/85/93/95 | any |
| Layup Mixmaster | DL | 70/83/90/99 | ≤ 7'0" |
| Ghost Stepper | CS or PC | 55/77/86/94 | any |
| Post Powerhouse | PC + STR | 60+65 / 75+79 / 85+86 / 95+95 | ≥ 6'5" |

## Playmaking badges

| Badge | Attribute | Tiers | Height |
|---|---|---|---|
| Ankle Assassin | BH | 75/86/93/96 | ≤ 6'10" |
| Handles for Days | BH | 71/81/90/95 | ≤ 7'0" |
| Strong Handle | BH + STR | 60+75 / 67+82 / 73+89 / 78+95 | 5'9"–6'11" |
| Unpluckable | BH or PC | BH 65/80/92/97, PC 65/86/96/– | any |
| Pace | SWB | 70/80/88/93 | ≤ 6'10" |
| Lightning Launch | SWB | 68/75/86/91 | ≤ 6'11" |
| Dimer | PASS | 50/70/86/95 | any |
| Break Starter | PASS | 65/77/89/97 (nba2klab) vs 72/82/91/96, 6'7"+ (2k27.org) | disputed |

## Defense badges

| Badge | Attribute | Tiers | Height |
|---|---|---|---|
| Seatbelt | PD + AGI | 75+70 / 85+77 / 91+80 / 99+86 (Destructoid Silver AGI 90) | ≤ 6'9" |
| Pick Dodger | PD + AGI | 73+71 / 83+81 / 90+88 / 97+91 | ≤ 6'10" |
| Ankle Braces | PD + AGI | 60+65 / 86+82 / 93+89 / 95+92 (single source) | ≤ 6'9" |
| Challenger | PD | 71/82/92/98 | ≤ 6'11" |
| Glove | STL | 70/83/93/99 | ≤ 7'0" |
| Interceptor | STL | 60/77/90/97 | any |
| Off-Ball Pest | ID or PD | ID 60/76/85/93, PD 55/68/80/89 | any |
| Wall Up | ID + STR | 80+75 / 85+80 / 95+90 / 99+92 | ≥ 6'5" |
| Post Lockdown | ID + STR | 65+65 / 82+74 / 88+80 / 93+88 | ≥ 6'5" |
| Paint Patroller | ID + BLK | 60+70 / 71+84 / 77+93 / 84+99 (single source) | ≥ 6'5" |
| High-Flying Denier | BLK + VRT | 68+60 / 78+74 / 88+80 / 92+83 | ≥ 6'3" |

## Physicals badges

| Badge | Attribute | Tiers | Height |
|---|---|---|---|
| Flash | SPD + AGI | 70+60 / 82+78 / 87+81 / 95+91 | any |
| Slippery Off-Ball | SPD + AGI | 57+57 / 73+65 / 85+77 / 94+90 | ≤ 6'9" |
| Work Horse | AGI or STR | 60/75/85/95 | any |
| Bruiser | STR | 71/84/93/99 | any |
| Brick Wall | STR | 75/83/95/99 | ≥ 6'5" |
| Pogo Stick | VRT | 63/70/80/90 | any |

## Rebounding badges (new discipline)

Crasher (OREB), Possession Closer (DREB), Sync Snatcher (timed jump), Boxout Boss
(DREB + STR or OREB, disputed), Breaker (OREB + STR, disputed).

## Animations

| Animation | Requirement |
|---|---|
| Dribble style Zach LaVine | 83 SWB, 5'9"–6'9" |
| Dribble style Ja Morant | 85 SWB |
| Size-up James Harden | 86 BH, ≤ 6'9" |
| Size-up Jayson Tatum | 75 BH, ≤ 6'9" |
| Crossover Zach LaVine | 85 BH |
| Crossover Jordan Poole | 86 BH |
| Crossover Shaedon Sharpe | 78 BH, 6'5"–6'9" |
| Crossover escape Jimmy Butler / Steph Curry | 80 BH |
| Crossover escape Anthony Edwards | 76 BH |
| Behind-back escape Kawhi Leonard | 80 BH |
| Hesitation escape Coby White | 85 BH |
| Between-legs escape Zach LaVine | 85 BH |
| Jumpshot base Ray Allen | 6'5"–6'9", base 88–89 3PT or MID; the measured recipe below needs 92 |
| Jumper (measured) Ray Allen / Oscar Robertson 42% + Beluba 58%, Push | gate 92; 50 ms window 555–605 ms, 100% at 580 ms, 62% avg (2kjumpers, pre-Sep 17) |
| Jumper (measured) Quentin Grimes / Oscar Robertson 44% + Sam Hauser 56%, Push | gate 80, < 6'10"; 50 ms window opening 505 ms, 86.7% peak |
| Jumper Michael Porter Jr. base (measured recipe) | ≥ 6'10" only |
| Dribble style SGA | 84 SWB (Koza 7.0, 7/7) |
| Size-up / escapes SGA | 91 BH; Kobe 88 (6'5"–6'9"); Harden/Poole/Paul George 86 |
| Dribble pull-up Pro 2 | 92 3PT or MID, ≤ 6'9"; Kyrie Irving 90; Cade/Booker/Vassell/Kawhi 89 |
| Dunk sigs | Obi Toppin 87/75, LaVine 88/73, DJJ 90/75 (6'5"–6'9"), Kobe 92/76, Westbrook 93/80 |
| Alley-oop: Pro contact | 84 DD + 70 VRT |
| Dunk: Ja Morant signature | 89 DD + 68 VRT, < 6'10" |
| Dunk: Pro two-foot contact | 87 DD + 75 VRT |
| Dunk: Elite two-foot contact | 96 DD + 82 VRT (some report 85 VRT) |
| Dunk: Pro one-foot contact | 89 DD + 78 VRT |
| Dunk: Elite one-foot contact | 99 DD + 90 VRT |
| Dunk: Small contacts | 93/80 one-foot, 86/75 two-foot, ≤ 6'4" |
| Dunk: Bigman standing contacts | Pro 80 SD + 60 VRT, Elite 90 SD + 70 VRT, ≥ 6'10" |
| Alley-oop: Elite contact | 92 DD + 80 VRT |
| Layup: Anthony Edwards | 84 DL, 5'9"–6'9" |
| Layup: Amen Thompson | 82 DL, 6'5"–6'9" |

## Patch history relevant to builds (official: nba.2k.com/2k27/patch-updates)

- v1.2 (2026-08-28): no gameplay changes.
- v1.3 (2026-08-31): Shot Artist and Calibrated nerfed; REP and Crew XP retuned.
- v1.4 (09-03), v1.5 (09-11): stability only.
- 2026-09-17 (server-side, all platforms): contests strengthened, wide-open boost, standing dunks
  better, Rise Up Gold+ better, Steal rating properly rewarded on contact, game speed standardized.
- v2.0 (2026-10-08 PS5/XSX; 2026-10-16 PC/Switch 2): ghost contests fixed (defender position at
  release, must be squarely in front); open shots from quality shooters more effective; mid-range
  boosted in competitive modes; 3PT % slightly rebalanced; shot range fixed for several shooting
  badges; contact dunks succeed more at every Rise Up tier; correctly timed dunks no longer miss;
  Shot Artist / Calibrated / Navigator timing windows adjusted; Navigator and Airspace "make defense
  matter more"; Airspace and Detonator dunk frequency/success reduced; Rim Guardian counters Airspace;
  steal animations match rating, failed steals by low-rated / out-of-adrenaline defenders penalized;
  anklebreakers only on hard decels / quick launches; faster passing; BTB escape input fix;
  Physicals Build Spec tiers 7/9 easier; Crew Divisions use REC settings with shot meters on.
- Season 2 starts 2026-10-16; 2K said a broader patch would land around Season 2.
