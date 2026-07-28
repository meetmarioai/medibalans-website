# -*- coding: utf-8 -*-
"""
MediBalans · tillämpa den kanoniska menyn på samtliga sidor
============================================================
Ersätter innehållet i <nav>…</nav> (desktop) och i mobile-nav-blocket
med markup genererad ur canonical_nav.py. Efter körning har varje sida
exakt samma meny, och mobilen speglar desktop post för post.

Bevaras orört: <header>-hölje, logotyp, hamburgarknappen och all övrig
sidstruktur. Endast länklistorna byts.

Sidor utan <nav> eller utan mobile-nav hoppas över och rapporteras.

Torrkörning:  python3 scripts/apply_canonical_nav.py --dry
Skarpt:       python3 scripts/apply_canonical_nav.py
"""
import os, re, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from canonical_nav import desktop_html, mobile_html, all_hrefs

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DRY = "--dry" in sys.argv
SKIP = (".git", "node_modules", "scripts", ".vercel", "api", "downloads")


def lang_of(rel):
    return "en" if rel.startswith(("en/", "en-")) else "sv"


def exists(href):
    p = href.split("#")[0].strip("/")
    if not p:
        return True
    return os.path.exists(os.path.join(ROOT, p, "index.html")) or \
        os.path.exists(os.path.join(ROOT, p))


def process(path, lang):
    h = open(path, encoding="utf-8").read()
    orig = h
    did = []

    # ---- desktop: innehållet mellan <nav> och </nav> inuti <header> ----
    hm = re.search(r"<header\b.*?</header>", h, re.S)
    if hm:
        head = hm.group(0)
        nm = re.search(r"(<nav\b[^>]*>)(.*?)(</nav>)", head, re.S)
        if nm:
            new_head = head[:nm.start()] + nm.group(1) + "\n" + desktop_html(lang) + "\n    " + nm.group(3) + head[nm.end():]
            h = h[:hm.start()] + new_head + h[hm.end():]
            did.append("desktop")

    # ---- mobil ----
    i = h.find('<div class="mobile-nav"')
    if i != -1:
        m = re.search(r"</div>\s*(?=<(?!a\b)[a-zA-Z])", h[i:])
        if m:
            block = h[i:i + m.end()]
            open_tag = re.match(r'<div class="mobile-nav"[^>]*>', block).group(0)
            new_block = open_tag + "\n" + mobile_html(lang) + "\n</div>"
            h = h[:i] + new_block + h[i + m.end():]
            did.append("mobil")
    else:
        # Ingen mobilmeny finns. Sidor med hamburgarknapp men utan meny
        # (integritetspolicy och en/privacy-policy) har en knapp som inte
        # öppnar någonting. Skapa blocket direkt efter </header>.
        hm2 = re.search(r"</header>", h)
        if hm2 and "mobileToggle" in h:
            block = ('\n<div class="mobile-nav" id="mobileNav">\n'
                     + mobile_html(lang) + "\n</div>\n")
            h = h[:hm2.end()] + block + h[hm2.end():]
            did.append("mobil(ny)")

    if h != orig and not DRY:
        open(path, "w", encoding="utf-8").write(h)
    return did


def main():
    # förhandskontroll: alla kanoniska länkar måste finnas
    bad = []
    for lang in ("sv", "en"):
        for href in all_hrefs(lang):
            if not exists(href):
                bad.append((lang, href))
    if bad:
        print("AVBRYTER — kanoniska menyn pekar på sidor som inte finns:")
        for lang, href in bad:
            print(f"   {lang}: {href}")
        return
    print("Förhandskontroll: samtliga kanoniska länkar finns.\n")

    done = skipped = 0
    for dp, dirs, fs in os.walk(ROOT):
        dirs[:] = [d for d in dirs if d not in SKIP and not d.startswith(".")]
        for fn in fs:
            if fn != "index.html":
                continue
            p = os.path.join(dp, fn)
            if os.path.getsize(p) < 1000:
                continue
            rel = os.path.relpath(p, ROOT)
            did = process(p, lang_of(rel))
            if did:
                done += 1
                if len(did) < 2:
                    print(f"  ! {rel:50} endast {'+'.join(did)}")
            else:
                skipped += 1
                print(f"  · {rel:50} HOPPAD (ingen nav-region)")
    print("\n" + ("TORRKÖRNING — inget skrivet" if DRY else "SKRIVET"))
    print(f"  {done} sidor uppdaterade · {skipped} hoppade")


if __name__ == "__main__":
    main()
