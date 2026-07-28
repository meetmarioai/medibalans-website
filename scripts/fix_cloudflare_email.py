# -*- coding: utf-8 -*-
"""
MediBalans · avobfuskera Cloudflare-e-post i källkoden
=======================================================
PROBLEMET
  16 sidor har sparats EFTER att ha passerat Cloudflares e-postobfuskering
  och därefter committats. På dessa sidor är adressen ersatt med

      <span class="__cf_email__" data-cfemail="89e0e7...">[email&#160;protected]</span>

  och avkodningen sker av /cdn-cgi/scripts/.../email-decode.min.js.
  Webbplatsen serveras från Vercel, där /cdn-cgi/ inte finns. Scriptet
  ger 404, avkodningen uteblir och besökaren ser bokstavligen texten
  "[email protected]" — bland annat på den engelska startsidan.

ÅTGÄRD
  · Avkoda data-cfemail (första byten är nyckel, XOR på resten)
  · Ersätt spannet med en riktig mailto-länk
  · Ersätt /cdn-cgi/l/email-protection#<hex> med mailto:<avkodad adress>
  · Ta bort <script ... email-decode.min.js></script>

Torrkörning:  python3 scripts/fix_cloudflare_email.py --dry
Skarpt:       python3 scripts/fix_cloudflare_email.py
"""
import os, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DRY = "--dry" in sys.argv
SKIP = (".git", "node_modules", "scripts", ".vercel")


def decode(hexstr):
    key = int(hexstr[:2], 16)
    return "".join(chr(int(hexstr[i:i + 2], 16) ^ key) for i in range(2, len(hexstr), 2))


SPAN_RE = re.compile(
    r'<(?P<tag>span|a)\b[^>]*class="[^"]*__cf_email__[^"]*"[^>]*data-cfemail="(?P<hex>[a-f0-9]+)"[^>]*>'
    r'.*?</(?P=tag)>', re.S)
LINK_RE = re.compile(r'<a\b[^>]*href="/cdn-cgi/l/email-protection#(?P<hex>[a-f0-9]+)"[^>]*>(?P<txt>.*?)</a>', re.S)
BARE_HREF_RE = re.compile(r'href="/cdn-cgi/l/email-protection#(?P<hex>[a-f0-9]+)"')
# OBS: måste matcha HELA elementet inklusive </script>. En tidigare variant
# tillät att bara starttaggen togs bort, vilket lämnade en föräldralös
# </script> och obalanserad HTML i 7 filer.
SCRIPT_RE = re.compile(r'<script[^>]*email-decode\.min\.js[^>]*>.*?</script>', re.S)

# Cloudflares bot-detection (__CF$cv$params) har också bakats in i källkoden.
# Den injicerar /cdn-cgi/challenge-platform/... som ger 404 på Vercel:
# en misslyckad request och ett konsolfel per sidladdning, utan funktion.
CF_CHALLENGE_RE = re.compile(r"<script>\(function\(\)\{.*?__CF\$cv\$params.*?</script>", re.S)


def fix(path):
    h = open(path, encoding="utf-8").read()
    orig = h
    found = {"span": 0, "link": 0, "script": 0, "challenge": 0}

    def span_sub(m):
        found["span"] += 1
        addr = decode(m.group("hex"))
        return f'<a href="mailto:{addr}">{addr}</a>'

    h = SPAN_RE.sub(span_sub, h)

    def link_sub(m):
        found["link"] += 1
        addr = decode(m.group("hex"))
        txt = m.group("txt")
        if "email" in txt.lower() and "protected" in txt.lower():
            txt = addr
        return f'<a href="mailto:{addr}">{txt}</a>'

    h = LINK_RE.sub(link_sub, h)

    def bare_sub(m):
        found["link"] += 1
        return f'href="mailto:{decode(m.group("hex"))}"'

    h = BARE_HREF_RE.sub(bare_sub, h)

    n_script = len(SCRIPT_RE.findall(h))
    if n_script:
        h = SCRIPT_RE.sub("", h)
        found["script"] = n_script

    n_ch = len(CF_CHALLENGE_RE.findall(h))
    if n_ch:
        h = CF_CHALLENGE_RE.sub("", h)
        found["challenge"] = n_ch

    if h != orig and not DRY:
        open(path, "w", encoding="utf-8").write(h)
    return (h != orig), found


def main():
    changed = 0
    for dp, dirs, fs in os.walk(ROOT):
        dirs[:] = [d for d in dirs if d not in SKIP and not d.startswith(".")]
        for fn in fs:
            if not fn.endswith(".html"):
                continue
            p = os.path.join(dp, fn)
            h = open(p, encoding="utf-8").read()
            if not any(x in h for x in ("__cf_email__", "email-protection", "email-decode", "__CF$cv$params")):
                continue
            did, found = fix(p)
            if did:
                changed += 1
                rel = os.path.relpath(p, ROOT)
                print(f"  ✓ {rel:48} span={found['span']} länk={found['link']} script={found['script']} challenge={found['challenge']}")
    print("\n" + ("TORRKÖRNING — inget skrivet" if DRY else "SKRIVET"))
    print(f"  {changed} filer")


if __name__ == "__main__":
    main()
