# -*- coding: utf-8 -*-
"""
MediBalans · laga saknad navigations-JS
========================================
BAKGRUND
  Den kanoniska mobilmenyn anropar closeMobile() på varje länk. På sidor
  vars egen JavaScript aldrig definierade den funktionen kastar därför
  varje tryck på en menylänk ReferenceError, och menyn stängs inte.

  Ursprungsfelet var mitt: i apply_canonical_nav injicerade jag först
  menyn (som innehåller 40 anrop till closeMobile) och kontrollerade
  DÄREFTER med `if "closeMobile" not in h`. Strängen fanns då redan
  tack vare anropen, så injektionen av funktionsdefinitionen hoppades
  över. Kontrollen görs nu mot DEFINITIONEN, inte mot strängen.

OMFATTNING (funnen genom revision av samtliga sidor, inte de två
rapporterade):
  utredningsprotokoll          saknar både toggle-handler och closeMobile
  baby-balans                  saknar både toggle-handler och closeMobile
  en/alzheimers-assessment     toggle är kopplad, saknar closeMobile

KONVENTION
  .mobile-nav.active är klassen som visar menyn (91 sidor använder
  'active'). Blocket nedan följer den.

Torrkörning:  python3 scripts/fix_nav_js.py --dry
Skarpt:       python3 scripts/fix_nav_js.py
"""
import os, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DRY = "--dry" in sys.argv
SKIP = (".git", "node_modules", "scripts", ".vercel")

CLOSE_ONLY = """
<script>
/* nav-js-patch: closeMobile saknades — den kanoniska mobilmenyn anropar
   den på varje länk. Toggle-handlern finns redan på denna sida. */
function closeMobile(){
  var m=document.getElementById('mobileNav');
  var t=document.getElementById('mobileToggle');
  if(m)m.classList.remove('active');
  if(t)t.setAttribute('aria-expanded','false');
}
</script>
"""

FULL = """
<script>
/* nav-js-patch: varken toggle-handler eller closeMobile fanns på denna
   sida. Hamburgaren renderades men öppnade ingenting. */
document.addEventListener('DOMContentLoaded',function(){
  var hdr=document.getElementById('header');
  if(hdr)window.addEventListener('scroll',function(){
    hdr.classList.toggle('scrolled',window.scrollY>20);
  },{passive:true});

  var t=document.getElementById('mobileToggle');
  var m=document.getElementById('mobileNav');
  if(t&&m)t.addEventListener('click',function(){
    var open=m.classList.toggle('active');
    t.setAttribute('aria-expanded',open);
    document.body.style.overflow=open?'hidden':'';
  });

  document.querySelectorAll('.nav-dropdown').forEach(function(dd){
    var b=dd.querySelector('.nav-dd-btn');
    if(!b)return;
    b.addEventListener('click',function(e){
      e.stopPropagation();
      var isOpen=dd.classList.contains('open');
      document.querySelectorAll('.nav-dropdown.open').forEach(function(o){
        o.classList.remove('open');
        var ob=o.querySelector('.nav-dd-btn');
        if(ob)ob.setAttribute('aria-expanded','false');
      });
      dd.classList.toggle('open',!isOpen);
      b.setAttribute('aria-expanded',!isOpen);
    });
  });
  document.addEventListener('click',function(){
    document.querySelectorAll('.nav-dropdown.open').forEach(function(d){
      d.classList.remove('open');
    });
  });
  document.addEventListener('keydown',function(e){
    if(e.key==='Escape'){
      document.querySelectorAll('.nav-dropdown.open').forEach(function(d){
        d.classList.remove('open');
      });
      closeMobile();
    }
  });
});
function closeMobile(){
  var m=document.getElementById('mobileNav');
  var t=document.getElementById('mobileToggle');
  if(m)m.classList.remove('active');
  if(t)t.setAttribute('aria-expanded','false');
  document.body.style.overflow='';
}
</script>
"""


def inline_js(h):
    return "\n".join(re.findall(
        r'<script(?![^>]*src=)(?![^>]*ld\+json)[^>]*>(.*?)</script>', h, re.S))


def diagnose(h):
    """(behöver_closeMobile, behöver_toggle_handler)"""
    js = inline_js(h)
    calls = bool(re.search(r'closeMobile\(\)', h))
    # OBS: kontrollera DEFINITIONEN, inte strängen — det var ursprungsfelet
    defined = bool(re.search(r'function\s+closeMobile\s*\(', js))
    has_toggle = 'id="mobileToggle"' in h
    toggle_wired = "mobileToggle" in js
    return (calls and not defined), (has_toggle and not toggle_wired)


def main():
    fixed = 0
    for dp, dirs, fs in os.walk(ROOT):
        dirs[:] = [d for d in dirs if d not in SKIP and not d.startswith(".")]
        for fn in fs:
            if not fn.endswith(".html"):
                continue
            p = os.path.join(dp, fn)
            if os.path.getsize(p) < 1000:
                continue
            h = open(p, encoding="utf-8").read()
            need_close, need_toggle = diagnose(h)
            if not (need_close or need_toggle):
                continue
            block = FULL if need_toggle else CLOSE_ONLY
            if "</body>" in h:
                h2 = h.replace("</body>", block + "</body>", 1)
            else:
                h2 = h + block
            if not DRY:
                open(p, "w", encoding="utf-8").write(h2)
            fixed += 1
            rel = os.path.relpath(p, ROOT)
            what = "full nav-JS" if need_toggle else "closeMobile"
            print(f"  ✓ {rel:48} + {what}")
    print("\n" + ("TORRKÖRNING — inget skrivet" if DRY else "SKRIVET"))
    print(f"  {fixed} sidor")


if __name__ == "__main__":
    main()
