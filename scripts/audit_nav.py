# -*- coding: utf-8 -*-
"""
MediBalans · navigationsrevision
=================================
Läser ut desktop- och mobilnavigationen från SAMTLIGA sidor och jämför.

Rapporterar:
  1. Döda länkar — href som inte motsvarar någon fil i repot
  2. Desktop/mobil-avvikelse — poster som finns i den ena men inte den andra
  3. Etikettglidning — samma href med olika text på olika sidor
  4. Saknade poster — sidor som avviker från den kanoniska menyn
  5. SV/EN-paritet — poster som saknar motsvarighet i det andra språket

Ändrar ingenting. Kör:  python3 scripts/audit_nav.py
"""
import os
import re
from collections import Counter, defaultdict

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SKIP_DIRS = (".git", "node_modules", "scripts", "downloads", ".vercel")


def pages():
    out = []
    for dp, dirs, fs in os.walk(ROOT):
        dirs[:] = [d for d in dirs if d not in SKIP_DIRS and not d.startswith(".")]
        for fn in fs:
            if fn != "index.html":
                continue
            p = os.path.join(dp, fn)
            if os.path.getsize(p) < 1000:      # redirect-stubbar
                continue
            out.append(p)
    return sorted(out)


def regions(h):
    """Desktop = <header>…</header>. Mobil = mobile-nav-blocket, avgränsat
    vid sitt egna avslutande </div> — INTE till </body>, annars sväljs
    hela sidan inklusive footern och jämförelsen blir meningslös."""
    d = re.search(r"<header\b.*?</header>", h, re.S)
    mob = None
    i = h.find('<div class="mobile-nav"')
    if i != -1:
        m = re.search(r"</div>\s*(?=<(?!a\b)[a-zA-Z])", h[i:])
        mob = h[i: i + m.end()] if m else None
    return (d.group(0) if d else None), mob


def links(region):
    """[(href, text)] för interna länkar, i dokumentordning."""
    if not region:
        return []
    out = []
    for m in re.finditer(r'<a\b[^>]*href="([^"]+)"[^>]*>(.*?)</a>', region, re.S):
        href, txt = m.group(1), re.sub(r"<[^>]+>", "", m.group(2))
        txt = re.sub(r"\s+", " ", txt).strip()
        if href.startswith("/cdn-cgi/"):      # Cloudflare e-postobfuskering
            continue
        if href.startswith("/") and not href.startswith("//"):
            out.append((href, txt))
    return out


def resolves(href):
    """Finns målet i repot?"""
    path = href.split("#")[0].split("?")[0]
    if path in ("/", ""):
        return True
    if "#" in href and path == "":
        return True
    p = path.strip("/")
    cands = [os.path.join(ROOT, p, "index.html"), os.path.join(ROOT, p)]
    if p.endswith(".html"):
        cands.append(os.path.join(ROOT, p))
    return any(os.path.exists(c) for c in cands)


def main():
    ps = pages()
    sv = [p for p in ps if not os.path.relpath(p, ROOT).startswith(("en/", "en-"))]
    en = [p for p in ps if os.path.relpath(p, ROOT).startswith(("en/", "en-"))]
    print(f"Sidor: {len(ps)}  (SV {len(sv)} · EN {len(en)})\n")

    desk_sets, mob_sets = {}, {}
    label_by_href = defaultdict(Counter)
    dead = defaultdict(list)
    no_region = []

    for p in ps:
        rel = os.path.relpath(p, ROOT)
        h = open(p, encoding="utf-8").read()
        d, m = regions(h)
        if not d:
            no_region.append((rel, "desktop"))
        if not m:
            no_region.append((rel, "mobil"))
        dl, ml = links(d), links(m)
        desk_sets[rel] = dl
        mob_sets[rel] = ml
        for href, txt in dl + ml:
            if txt:
                label_by_href[href][txt] += 1
            if not resolves(href):
                dead[href].append(rel)

    # ---------- 1. döda länkar ----------
    print("=" * 72)
    print("1. DÖDA LÄNKAR I NAVIGATIONEN")
    print("=" * 72)
    if not dead:
        print("  Inga.\n")
    else:
        for href, files in sorted(dead.items(), key=lambda x: -len(x[1])):
            print(f"  {href:44} saknas — {len(files)} sidor")
            for f in files[:3]:
                print(f"        {f}")
            if len(files) > 3:
                print(f"        … och {len(files)-3} till")
        print()

    # ---------- 2. desktop vs mobil ----------
    print("=" * 72)
    print("2. DESKTOP/MOBIL-AVVIKELSE (per sida)")
    print("=" * 72)
    diffs = []
    for rel in desk_sets:
        dh = {h for h, _ in desk_sets[rel]}
        mh = {h for h, _ in mob_sets[rel]}
        if not mh:
            continue
        only_d, only_m = dh - mh, mh - dh
        only_d = {x for x in only_d if not x.startswith("/#") and x != "/"}
        only_m = {x for x in only_m if not x.startswith("/#") and x != "/"}
        if only_d or only_m:
            diffs.append((rel, only_d, only_m))
    if not diffs:
        print("  Inga.\n")
    else:
        print(f"  {len(diffs)} sidor avviker.\n")
        agg_d, agg_m = Counter(), Counter()
        for rel, od, om in diffs:
            for x in od:
                agg_d[x] += 1
            for x in om:
                agg_m[x] += 1
        print("  Finns i DESKTOP men inte MOBIL:")
        for h, n in agg_d.most_common(15):
            print(f"    {h:44} {n} sidor")
        print("\n  Finns i MOBIL men inte DESKTOP:")
        for h, n in agg_m.most_common(15):
            print(f"    {h:44} {n} sidor")
        print()

    # ---------- 3. etikettglidning ----------
    print("=" * 72)
    print("3. ETIKETTGLIDNING (samma href, olika text)")
    print("=" * 72)
    drift = {h: c for h, c in label_by_href.items() if len(c) > 1}
    if not drift:
        print("  Inga.\n")
    else:
        for h, c in sorted(drift.items()):
            variants = " | ".join(f'"{t}" ×{n}' for t, n in c.most_common())
            print(f"  {h}\n      {variants}")
        print()

    # ---------- 4. kanonisk meny + saknade poster ----------
    print("=" * 72)
    print("4. AVVIKELSE MOT KANONISK MENY")
    print("=" * 72)
    for label, group in (("SV", sv), ("EN", en)):
        counts = Counter()
        for p in group:
            rel = os.path.relpath(p, ROOT)
            for h, _ in desk_sets.get(rel, []):
                counts[h] += 1
        n = len(group)
        canon = {h for h, c in counts.items() if c >= n * 0.8}
        print(f"\n  {label}: kanonisk desktop-meny = {len(canon)} poster (finns på ≥80% av {n} sidor)")
        missing = []
        for p in group:
            rel = os.path.relpath(p, ROOT)
            have = {h for h, _ in desk_sets.get(rel, [])}
            miss = canon - have
            if miss:
                missing.append((rel, miss))
        if not missing:
            print("     Alla sidor har hela den kanoniska menyn.")
        else:
            print(f"     {len(missing)} sidor saknar poster:")
            for rel, miss in missing[:12]:
                print(f"       {rel:46} saknar {len(miss)}: {', '.join(sorted(miss)[:4])}")
            if len(missing) > 12:
                print(f"       … och {len(missing)-12} till")

    # ---------- 5. saknade regioner ----------
    print("\n" + "=" * 72)
    print("5. SIDOR UTAN NAV-REGION")
    print("=" * 72)
    if not no_region:
        print("  Inga.")
    else:
        for rel, which in no_region:
            print(f"  {rel:52} saknar {which}")
    print()


if __name__ == "__main__":
    main()
