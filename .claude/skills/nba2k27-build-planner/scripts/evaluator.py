#!/usr/bin/env python3
"""NBA 2K27 MyPLAYER builder budget evaluator (Overall Potential, max 99).

Usage
  python3 evaluator.py '{"position":"PG","height_in":79,"weight":192,"wingspan_in":79,
                         "attrs":{"Close Shot":60, ... all 21 ...}}'
  python3 evaluator.py --json '<build>'   machine-readable output
  python3 evaluator.py --selftest         anchors, run-1 point and every live builder reading
  python3 evaluator.py --about            method notes

Output
  * linked-rule normalisation (the live builder raises "follower" ratings automatically,
    e.g. at 6'7": Close Shot >= Driving Layup-10, Post Control >= Ball Handle-40,
    Interior Defense >= Steal-35, Standing Dunk >= Driving Dunk-50),
  * u = estimated uncapped Overall Potential of the normalised build. The builder rejects
    u > 99.0 ("over budget") and shows round(u) otherwise, so 99 means 98.5 <= u <= 99.0,
  * margin to the 99.0 limit, verdict, and the marginal cost of +1 in every attribute
    (OVR points, including linked raises) plus how many points of it still fit.

Method (honest summary)
  * The exact lockercodes engine runs server side (Turnstile-gated `evaluate` call); the client
    JS could not be read in full, so this is a FITTED model, not the exact formula.
  * Training data: 3,591 complete (99 OVR) builds decoded from the share links of lockercodes'
    build-name directory (2026-10-08). Four of them were re-loaded in the live builder today and
    all showed 99 unchanged, so they match current tuning.
  * The overall depends on HEIGHT and attributes only (position/weight/wingspan only change
    caps): a 6'7" model predicts SG/SF/PF/C 6'7" builds with no bias. One model per height.
  * Form: u = 25 + 74*S, S = sum_i f_i(r_i) + sum_k g_k(r_(k)); f_i, g_k convex piecewise-linear
    (non-decreasing marginal cost); r_(k) = k-th highest rating excluding Free Throw.
    5-fold CV on held-out 99 builds: sd 0.55-0.65 OVR at 6'4"-6'8" (0.75 for the live-calibrated
    6'7" model, which additionally fits 13 live readings to within ~0.5 OVR).
  * Linked rules (follower >= driver + k) mined per height from the same builds; at 6'7" they
    reproduce the live builder's normalisations exactly (3 builds, 7 raised ratings).
"""
import json, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
O = ['CS', 'DL', 'DD', 'SD', 'PC', 'MID', '3PT', 'FT', 'PASS', 'BH', 'SWB', 'ID', 'PD', 'STL', 'BLK',
     'OREB', 'DREB', 'SPD', 'AGI', 'STR', 'VRT']
NAMES = {'Close Shot': 'CS', 'Driving Layup': 'DL', 'Driving Dunk': 'DD', 'Standing Dunk': 'SD',
         'Post Control': 'PC', 'Mid-Range': 'MID', 'Mid-Range Shot': 'MID', 'Three-Point': '3PT',
         'Three-Point Shot': '3PT', 'Free Throw': 'FT', 'Pass Accuracy': 'PASS', 'Ball Handle': 'BH',
         'Speed With Ball': 'SWB', 'Interior Defense': 'ID', 'Perimeter Defense': 'PD', 'Steal': 'STL',
         'Block': 'BLK', 'Offensive Rebound': 'OREB', 'Defensive Rebound': 'DREB', 'Speed': 'SPD',
         'Agility': 'AGI', 'Strength': 'STR', 'Vertical': 'VRT'}
FULL = {}
for _k, _v in NAMES.items():
    FULL.setdefault(_v, _k)
CV_SD = {74: 0.7, 75: 0.7, 76: 0.55, 77: 0.55, 78: 0.54, 79: 0.75, 80: 0.58, 81: 0.6, 82: 0.6}
LIVE_CALIBRATED = {79}


def load_json(name, default=None):
    p = os.path.join(HERE, name)
    if not os.path.exists(p):
        return default
    with open(p) as f:
        return json.load(f)


PARAMS = load_json('model_params.json')
KN = PARAMS['knots']
RULES = load_json('rules_by_height.json', {})
CAPS = load_json('caps.json', {'caps': {}, 'source': {}})


def conv(r):
    ov = [min(max(r - a, 0), b - a) for a, b in zip(KN[:-1], KN[1:])]
    out = [0.0] * len(ov); s = 0.0
    for j in range(len(ov) - 1, -1, -1):
        s += ov[j]; out[j] = s
    return out


def features(bd):
    v = []
    for a in O:
        v += conv(bd[a])
    s = sorted([bd[a] for a in O if a != 'FT'], reverse=True)
    for k in range(20):
        v += conv(s[k])
    return v


def model_for(ht):
    m = PARAMS['final'].get(str(ht))
    if m is None:
        raise SystemExit(f"No model for height {ht}\" (supported {min(map(int, PARAMS['final']))}-"
                         f"{max(map(int, PARAMS['final']))} in)")
    return m['d']


def u_of(bd, d):
    """Estimated uncapped Overall Potential."""
    return 25 + 74 * sum(x * y for x, y in zip(features(bd), d))


def normalize(bd, ht, caps=None):
    rules = RULES.get(str(ht), [])
    b = dict(bd); changes = []; conflicts = []
    for _ in range(60):
        moved = False
        for drv, fol, k, n in rules:
            need = b[drv] + k
            if b[fol] < need:
                if caps and fol in caps and need > caps[fol]:
                    conflicts.append(f"{FULL[fol]} would need {need} ({FULL[drv]} {b[drv]}{k:+d}) but cap is {caps[fol]}")
                    need = caps[fol]
                    if b[fol] >= need:
                        continue
                changes.append((fol, b[fol], need, f"{FULL[fol]} >= {FULL[drv]} {k:+d}"))
                b[fol] = need; moved = True
        if not moved:
            break
    # collapse repeated raises of the same attribute
    first = {}; last = {}
    for a, x, y, r in changes:
        first.setdefault(a, (x, r)); last[a] = (y, r)
    merged = [(a, first[a][0], last[a][0], last[a][1]) for a in first]
    return b, merged, sorted(set(conflicts))


def lookup_caps(ht, wt, ws):
    C = CAPS['caps']
    key = f"{ht}|{wt}|{ws}"
    if key in C:
        miss = [FULL[a] for a in O if a not in C[key]]
        return C[key], 'exact: ' + CAPS['source'].get(key, '') + (f" (not listed: {', '.join(miss)})" if miss else '')
    best = None
    for k, v in C.items():
        h, w, s = map(int, k.split('|'))
        if h != ht:
            continue
        dist = abs((s - h) - (ws - ht)) * 100 + abs(w - wt)
        if best is None or dist < best[0]:
            best = (dist, k, v)
    if best is None:
        return None, 'no cap data for this height (caps not checked)'
    return dict(best[2]), (f"APPROXIMATE - nearest known frame {best[1].replace('|', ' / ')} "
                           f"({CAPS['source'].get(best[1], '')}); verify caps in the builder")


def evaluate(build):
    ht = int(build['height_in']); wt = int(build.get('weight', 0)); ws = int(build.get('wingspan_in', ht))
    raw = {}
    for k, v in build['attrs'].items():
        a = NAMES.get(k, k if k in O else None)
        if a is None:
            raise SystemExit(f"Unknown attribute name: {k}")
        raw[a] = int(v)
    missing = [FULL[a] for a in O if a not in raw]
    if missing:
        raise SystemExit(f"Missing attributes: {missing}")
    d = model_for(ht)
    caps, capsrc = lookup_caps(ht, wt, ws)
    over_cap = [f"{FULL[a]} {raw[a]} > cap {caps[a]}" for a in O if caps and a in caps and raw[a] > caps[a]]
    norm, changes, conflicts = normalize(raw, ht, caps)
    u = u_of(norm, d)
    sig = CV_SD.get(ht, 0.7)
    margin = 99.0 - u
    if margin < -sig:
        verdict = 'OVER BUDGET: the builder will refuse this build (rejects u > 99.0)'
    elif margin < 0:
        verdict = 'PROBABLY OVER BUDGET (within 1 sd of the 99.0 limit) - verify live'
    elif margin < sig:
        verdict = 'BORDERLINE FIT (within 1 sd below the 99.0 limit) - verify live'
    else:
        verdict = 'FITS (more than 1 sd below the 99.0 limit)'
    out = {'frame': f"{build.get('position', '?')} {ht // 12}'{ht % 12}\" {wt} lb, {ws // 12}'{ws % 12}\" wingspan",
           'model': f"height {ht} in, n={PARAMS['final'][str(ht)]['n']} complete builds"
                    + ("; live-calibrated" if ht in LIVE_CALIBRATED else "; not live-calibrated"),
           'model_sd_ovr': sig, 'caps_source': capsrc, 'over_cap': over_cap,
           'linked_changes': [{'attr': FULL[a], 'from': x, 'to': y, 'rule': r} for a, x, y, r in changes],
           'linked_cap_conflicts': conflicts,
           'normalized_attrs': {FULL[a]: norm[a] for a in O},
           'uncapped_ovr_est': round(u, 2), 'margin_to_99': round(margin, 2),
           'exceeds_99': u > 99.0, 'verdict': verdict,
           'builder_display_est': (int(round(u)) if u <= 99.0 else 'rejected (over budget)')}
    marg = {}
    for a in O:
        cap_a = caps.get(a, 99) if caps else 99
        if norm[a] >= cap_a:
            marg[FULL[a]] = {'per_point': None, 'note': 'at cap'}
            continue
        b2 = dict(norm); b2[a] += 1
        b2, ch2, _ = normalize(b2, ht, caps)
        c1 = u_of(b2, d) - u
        top = min(norm[a] + 5, cap_a); n5 = top - norm[a]
        b5 = dict(norm); b5[a] = top; b5, _, _ = normalize(b5, ht, caps)
        c5 = (u_of(b5, d) - u) / n5
        room = 0; bb = dict(norm); ub = u
        while bb[a] < cap_a and room < 74:
            t = dict(bb); t[a] += 1; t, _, _ = normalize(t, ht, caps)
            ut = u_of(t, d)
            if ut > 99.0:
                break
            bb, ub, room = t, ut, room + 1
        marg[FULL[a]] = {'per_point': round(c1, 3), 'next5_avg': round(c5, 3),
                         'linked': [FULL[x[0]] for x in ch2], 'room_to_99': room}
    rules = RULES.get(str(ht), [])
    for a in O:
        if norm[a] <= 25:
            marg[FULL[a]]['minus1_saves'] = 0.0; marg[FULL[a]]['floor'] = 'min 25'
            continue
        bm = dict(norm); bm[a] -= 1
        blockers = [f"{FULL[fol]}>={FULL[drv]}{k:+d}" for drv, fol, k, n in rules if fol == a and bm[a] < bm[drv] + k]
        if blockers:
            marg[FULL[a]]['minus1_saves'] = None; marg[FULL[a]]['floor'] = 'linked floor: ' + ', '.join(blockers)
        else:
            marg[FULL[a]]['minus1_saves'] = round(u - u_of(bm, d), 3)
    out['marginal'] = marg
    return out


def report(o):
    L = [f"Frame: {o['frame']}", f"Model: {o['model']} (prediction sd ~{o['model_sd_ovr']} OVR)",
         f"Caps: {o['caps_source']}"]
    if o['over_cap']:
        L.append('  !! OVER BODY CAP (not enterable): ' + '; '.join(o['over_cap']))
    if o['linked_changes']:
        L.append('Linked creation rules raise (the live builder does this automatically):')
        for c in o['linked_changes']:
            L.append(f"  {c['attr']}: {c['from']} -> {c['to']}   [{c['rule']}]")
    if o['linked_cap_conflicts']:
        L.append('  !! ' + '; '.join(o['linked_cap_conflicts']))
    L.append(f"Estimated uncapped Overall Potential: {o['uncapped_ovr_est']:.2f}   (limit 99.00; margin {o['margin_to_99']:+.2f})")
    L.append(f"Builder would show: {o['builder_display_est']}   exceeds 99: {o['exceeds_99']}")
    L.append(f"Verdict: {o['verdict']}")
    L.append('')
    L.append(f"{'Attribute':20s} {'now':>4s} {'+1 cost':>8s} {'next5/pt':>8s} {'-1 saves':>8s} {'room':>5s}  linked raises")
    for a in O:
        m = o['marginal'][FULL[a]]; now = o['normalized_attrs'][FULL[a]]
        ms = 'floor' if m.get('minus1_saves') is None else f"{m['minus1_saves']:.3f}"
        extra = (' [' + m['floor'] + ']') if m.get('floor', '').startswith('linked') else ''
        if m.get('per_point') is None:
            L.append(f"{FULL[a]:20s} {now:4d} {'cap':>8s} {'':>8s} {ms:>8s}{extra}")
        else:
            L.append(f"{FULL[a]:20s} {now:4d} {m['per_point']:8.3f} {m['next5_avg']:8.3f} {ms:>8s} "
                     f"{m['room_to_99']:5d}  {','.join(m['linked'])}{extra}")
    L.append('Costs are OVR points per rating point (uncapped overall). room = extra points of that attribute alone')
    L.append('that keep u <= 99.0. Rule of thumb: 1 sd of model error ~ 0.6-0.75 OVR ~ 2-5 points of an expensive attribute.')
    return '\n'.join(L)


def selftest():
    cal = load_json('calibration.json', {'checks': []})
    print(f"{'case':44s} {'u_est':>7s} {'disp':>8s}  observed (live builder unless noted)")
    for c in cal['checks']:
        o = evaluate(c['build'])
        lk = ', '.join(f"{x['attr']}->{x['to']}" for x in o['linked_changes'])
        print(f"{c['label']:44s} {o['uncapped_ovr_est']:7.2f} {str(o['builder_display_est']):>8s}  {c['observed']}"
              + (f"   [linked: {lk}]" if lk else ''))


if __name__ == '__main__':
    args = sys.argv[1:]
    if not args or args[0] in ('-h', '--help', '--about'):
        print(__doc__); sys.exit(0)
    if args[0] == '--selftest':
        selftest(); sys.exit(0)
    as_json = args[0] == '--json'
    if as_json:
        args = args[1:]
    o = evaluate(json.loads(args[0]))
    print(json.dumps(o, indent=1) if as_json else report(o))
