# -*- coding: utf-8 -*-
"""
MediBalans · robust CSS för hamburgare och mobilmeny
=====================================================
BAKGRUND
Playwright-verifiering mot 25f11d0 hittade två verkliga fel som all
statisk JS-analys missade, eftersom JavaScript var korrekt i båda fallen:

  methyldetox           En befintlig nav-patch KLONAR togglknappen för att
                        ta bort gamla lyssnare och kopplar sedan en egen
                        som sätter .active. Sidans CSS har bara
                        .mobile-nav.open. Klassen som faktiskt sätts har
                        ingen matchande regel — menyn öppnas aldrig.

  utredningsprotokoll   Hamburgaren renderas ~4x4 px och går inte att
                        träffa med ett riktigt tryck, och mobilmenyn
                        beräknas till display:block i stängt läge.

Mina tidigare kontroller missade methyldetox tre gånger, senast för att
regexen som skulle hitta variabeln för mobileNav inte klarade en
deklaration med flera variabler (var mt=..., mn=...). Slutsats: sluta
härleda vilken klass som gäller och gör i stället CSS:en tolerant.

ÅTGÄRD
  1. Varje sida med mobilmeny får BÅDA klassreglerna, .open och .active,
     med samma display-värde som sidan redan använder. Vilken klass en
     handler än sätter fungerar menyn då.
  2. Ett litet block med ID-selektorer läggs sist i head. ID slår klass i
     specificitet, så blocket kan inte överröstas av sidans egen CSS
     oavsett ordning:
        #mobileNav{display:none}
        #mobileNav.active,#mobileNav.open{display:flex}
        #mobileToggle explicit storlek och träffyta
     Detta gör åtgärden oberoende av hur den enskilda sidans kaskad ser ut.

Torrkörning:  python3 scripts/fix_mobile_nav_css.py --dry
Skarpt:       python3 scripts/fix_mobile_nav_css.py
"""
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DRY = "--dry" in sys.argv
SKIP = (".git", "node_modules", "scripts", ".vercel")
MARKER = "nav-robust-css"

BLOCK = """
<style>/* {marker}: ID-selektorer så att kaskaden inte kan slå ut menyn.
   Bakgrund: nav-patchen på vissa sidor sätter .active medan sidans egen
   CSS bara har .open. Båda stöds nu, och storleken på hamburgaren är
   explicit så att den går att träffa med ett tryck. */
#mobileNav{display:none}
#mobileNav.active,#mobileNav.open{display:flex;flex-direction:column}
#mobileToggle{display:none;flex-direction:column;justify-content:center;gap:5px;
  width:44px;height:44px;padding:10px;background:none;border:none;cursor:pointer}
#mobileToggle span{display:block;width:22px;height:2px;background:var(--navy,#0B1D33);
  border-radius:2px}
@media(max-width:900px){
  #mobileToggle{display:flex}
  header nav{display:none}
}
</style>
""".replace("{marker}", MARKER)


def display_varde(h):
    """Vilket display-värde använder sidan för öppen meny?"""
    m = re.search(r'\.mobile-nav\.(?:open|active)\s*\{[^}]*display:\s*([\w-]+)', h)
    return m.group(1) if m else "flex"


def fix(path):
    h = open(path, encoding="utf-8").read()
    if 'id="mobileNav"' not in h:
        return False, "ingen mobilmeny"
    if MARKER in h:
        return False, "redan patchad"

    atgard = []

    # 1) tvillingregel för den klass som saknas
    disp = display_varde(h)
    har_open = bool(re.search(r'\.mobile-nav\.open\s*\{', h))
    har_active = bool(re.search(r'\.mobile-nav\.active\s*\{', h))
    tillagg = ""
    if har_open and not har_active:
        tillagg = f".mobile-nav.active{{display:{disp}}}"
        atgard.append("+.active")
    elif har_active and not har_open:
        tillagg = f".mobile-nav.open{{display:{disp}}}"
        atgard.append("+.open")
    elif not har_open and not har_active:
        tillagg = f".mobile-nav.active,.mobile-nav.open{{display:{disp}}}"
        atgard.append("+bada")

    # 2) ID-blocket sist i head
    block = BLOCK
    if tillagg:
        block = block.replace("</style>", tillagg + "\n</style>")
    h = h.replace("</head>", block + "</head>", 1)
    atgard.append("id-block")

    if not DRY:
        open(path, "w", encoding="utf-8").write(h)
    return True, "+".join(atgard)


def main():
    n = 0
    detalj = {}
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
                n += 1
                detalj[why] = detalj.get(why, 0) + 1
                if "+.active" in why or "+bada" in why:
                    print(f"  ! {os.path.relpath(p, ROOT):46} {why}")
    print("\n" + ("TORRKORNING — inget skrivet" if DRY else "SKRIVET"))
    print(f"  {n} sidor · {detalj}")


if __name__ == "__main__":
    main()
