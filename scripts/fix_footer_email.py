# -*- coding: utf-8 -*-
"""
MediBalans · lägg tillbaka e-postadressen i footern
====================================================
52 av 97 sidor saknade info@medibalans.com i footern. Telefonnumret fanns,
adressen fanns, men e-posten var borta. Det är en befintlig inkonsekvens i
repot — inte något som uppstod i den här sessionen — men den träffade också
de nya sidorna eftersom de ärvde footern från gi-effects-test, som saknar den.

Åtgärd: sätt in en mailto-länk direkt efter telefonlänken i footern, med
exakt samma inline-stil som telefonlänken på respektive sida, så att den
smälter in i den lokala varianten.

Torrkörning:  python3 scripts/fix_footer_email.py --dry
Skarpt:       python3 scripts/fix_footer_email.py
"""
import os, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DRY = "--dry" in sys.argv
SKIP = (".git", "node_modules", "scripts", ".vercel")
MAIL = "info@medibalans.com"

# telefonlänken i footern, med sin ev. inline-stil och efterföljande <br>
TEL_RE = re.compile(
    r'(<a\s+href="tel:\+46723195070"([^>]*)>[^<]*</a>)(\s*(?:<br\s*/?>\s*)*)',
    re.I)


def fix(path):
    h = open(path, encoding="utf-8").read()
    fm = re.search(r"<footer\b.*?</footer>", h, re.S)
    if not fm:
        return False, "ingen footer"
    footer = fm.group(0)
    if MAIL in footer:
        return False, "har redan"

    m = TEL_RE.search(footer)
    if not m:
        return False, "ingen telefonlänk"

    tel_tag, attrs, brs = m.group(1), m.group(2), m.group(3)
    # ärv exakt samma style-attribut som telefonlänken
    style = ""
    sm = re.search(r'style="([^"]*)"', attrs)
    if sm:
        style = f' style="{sm.group(1)}"'

    mail_tag = f'<br>\n          <a href="mailto:{MAIL}"{style}>{MAIL}</a>'
    new_footer = footer[:m.end(1)] + mail_tag + brs + footer[m.end():]
    h = h[:fm.start()] + new_footer + h[fm.end():]

    if not DRY:
        open(path, "w", encoding="utf-8").write(h)
    return True, "tillagd"


def main():
    added = skipped = 0
    reasons = {}
    for dp, dirs, fs in os.walk(ROOT):
        dirs[:] = [d for d in dirs if d not in SKIP and not d.startswith(".")]
        for fn in fs:
            if fn != "index.html":
                continue
            p = os.path.join(dp, fn)
            if os.path.getsize(p) < 1000:
                continue
            did, why = fix(p)
            if did:
                added += 1
            else:
                skipped += 1
                reasons[why] = reasons.get(why, 0) + 1
                if why not in ("har redan",):
                    print(f"  · {os.path.relpath(p, ROOT):48} {why}")
    print("\n" + ("TORRKÖRNING — inget skrivet" if DRY else "SKRIVET"))
    print(f"  {added} sidor fick e-post · {skipped} orörda {reasons}")


if __name__ == "__main__":
    main()
