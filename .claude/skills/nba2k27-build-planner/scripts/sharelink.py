#!/usr/bin/env python3
"""Encode / decode lockercodes.io NBA 2K27 MyPLAYER builder share links.

  python3 sharelink.py encode PG 79 192 79 CS=70 DL=71 DD=87 ... VRT=75 [--cb "9-5_2-3"]
  python3 sharelink.py decode '<url or b= value>'

Heights and wingspans are in inches (6'7" = 79). All 21 attributes are required for encode.
Format of ?b=: 'z' + base36(len(json text)) + '_' + body, where body is base64url (no padding) of a
raw-deflate JSON array whose first element is
'POS.heightIn.weight.wingspanIn.<21 ratings joined by ->.c<cap breakers idx-count joined by _>'.
A link that the live builder rejects falls back to defaults with
"That shared build is not legal under current tuning."
"""
import base64
import json
import sys
import zlib

ORDER = ['CS', 'DL', 'DD', 'SD', 'PC', 'MID', '3PT', 'FT', 'PASS', 'BH', 'SWB', 'ID', 'PD', 'STL',
         'BLK', 'OREB', 'DREB', 'SPD', 'AGI', 'STR', 'VRT']
B36 = '0123456789abcdefghijklmnopqrstuvwxyz'
BASE_URL = 'https://www.lockercodes.io/nba-2k/myplayer-builder?b='


def _b36(n):
    s = ''
    while n:
        s = B36[n % 36] + s
        n //= 36
    return s or '0'


def encode(pos, ht, wt, ws, attrs, cb=''):
    vals = '-'.join(str(attrs[k]) for k in ORDER)
    txt = json.dumps([f'{pos}.{ht}.{wt}.{ws}.{vals}.c{cb}', None, None], separators=(',', ':'))
    c = zlib.compressobj(9, zlib.DEFLATED, -15)
    raw = c.compress(txt.encode()) + c.flush()
    body = base64.urlsafe_b64encode(raw).decode().rstrip('=')
    return f'{BASE_URL}z{_b36(len(txt))}_{body}'


def decode(link):
    b = link.split('b=', 1)[-1]
    body = b.split('_', 1)[1]
    t = zlib.decompress(base64.urlsafe_b64decode(body + '=' * (-len(body) % 4)), -15)
    if t[:1] == b'\x01':
        t = t[1:]
    pos, ht, wt, ws, vals, cb = json.loads(t)[0].split('.', 5)
    attrs = dict(zip(ORDER, map(int, vals.split('-'))))
    cbs = {}
    for p in filter(None, cb[1:].split('_')):
        i, n = p.split('-')
        cbs[ORDER[int(i)]] = int(n)
    return {'position': pos, 'height_in': int(ht), 'weight': int(wt), 'wingspan_in': int(ws),
            'attrs': attrs, 'cap_breakers': cbs}


def main(argv):
    if len(argv) >= 2 and argv[0] == 'decode':
        print(json.dumps(decode(argv[1]), indent=1))
    elif len(argv) >= 5 and argv[0] == 'encode':
        cb = ''
        if '--cb' in argv:
            i = argv.index('--cb')
            cb = argv[i + 1]
            argv = argv[:i] + argv[i + 2:]
        attrs = dict(a.split('=') for a in argv[5:])
        missing = [k for k in ORDER if k not in attrs]
        if missing:
            sys.exit(f'missing attributes: {", ".join(missing)}')
        print(encode(argv[1], int(argv[2]), int(argv[3]), int(argv[4]), {k: int(v) for k, v in attrs.items()}, cb))
    else:
        sys.exit(__doc__)


if __name__ == '__main__':
    main(sys.argv[1:])
