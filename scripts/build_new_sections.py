# -*- coding: utf-8 -*-
"""
MediBalans · generator för /symtom/ och /skrifter/
==================================================
Bygger nya sidor genom att ÅTERANVÄNDA den befintliga sidans skal — samma
<style>-block, samma <header>, samma <footer>, samma script-svans. Inget
typsnitt, ingen färg och ingen navigation är återskapad för hand; allt hämtas
ur mallsidan så att nya sidor blir identiska med resten av webbplatsen.

Mall:  gi-effects-test/index.html
Ut:    symtom/index.html, symtom/<slug>/index.html
       skrifter/index.html, skrifter/<slug>/index.html

Kör från repo-roten:  python3 scripts/build_new_sections.py
"""
import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TEMPLATE = os.path.join(ROOT, "gi-effects-test", "index.html")
BASE = "https://www.medibalans.com"


# --------------------------------------------------------------- skalextraktion
def extract_shell():
    h = open(TEMPLATE, encoding="utf-8").read()

    # alla <style>-block i <head> (före <body>)
    body_i = h.index("<body")
    styles = "".join(m.group(0) for m in re.finditer(r"<style[^>]*>.*?</style>", h[:body_i], re.S))

    # google fonts-länk
    fonts = "".join(re.findall(r'<link[^>]*fonts\.(?:googleapis|gstatic)[^>]*>', h[:body_i]))

    # meta pixel base (noscript + script) — behåll spårning konsekvent
    pixel = ""
    m = re.search(r"<script>!function\(f,b,e,v,n,t,s\).*?</script>", h, re.S)
    if m:
        pixel = m.group(0)

    body_open = re.search(r"<body[^>]*>", h).group(0)

    # VIKTIGT: mobilmenyn ligger UTANFÖR </header> på den här webbplatsen.
    # Slutar extraktionen vid </header> får nya sidor en hamburgarknapp
    # som inte öppnar någonting. Vi tar därför med mobilnav-blocket.
    h_start = h.index("<header")
    h_end = h.index("</header>") + len("</header>")
    mn = h.find('id="mobileNav"', h_end)
    if mn != -1:
        m = re.search(r"</div>\s*(?=<(?!a\b)[a-zA-Z])", h[mn:])
        header = h[h_start: mn + m.end()] if m else h[h_start:h_end]
    else:
        header = h[h_start:h_end]
    assert 'id="mobileNav"' in header, "mobilnav saknas i extraherat skal"
    footer = h[h.index("<footer"): h.index("</footer>") + len("</footer>")]
    tail = h[h.index("</footer>") + len("</footer>"):]

    return dict(styles=styles, fonts=fonts, pixel=pixel,
                body_open=body_open, header=header, footer=footer, tail=tail)


SHELL = extract_shell()


def page(title, desc, canonical, schema_blocks, content, hreflang_en=None):
    alts = f'\n<link rel="alternate" hreflang="en" href="{hreflang_en}">' if hreflang_en else ""
    schema = "\n".join(schema_blocks)
    return f"""<!DOCTYPE html>
<html lang="sv" class="no-js" style="overflow-x:hidden;">
<head>
<meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{title}</title>
<meta name="description" content="{desc}">
<meta name="robots" content="index, follow">
<link rel="canonical" href="{canonical}">
<link rel="alternate" hreflang="sv" href="{canonical}">{alts}
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:type" content="article">
<meta property="og:url" content="{canonical}">
<meta property="og:locale" content="sv_SE">
<meta property="og:image" content="{BASE}/og-image.jpg">
<meta name="twitter:card" content="summary_large_image">
{schema}
{SHELL['pixel']}
{SHELL['fonts']}
{SHELL['styles']}
<style>
/* ---- sektionsspecifikt: ärver alla tokens ur mallens :root ---- */
.sec-hero{{background:linear-gradient(135deg,var(--navy) 0%,var(--navy-light) 100%);color:var(--white);padding:5rem 0 4.5rem;}}
.sec-hero .eyebrow{{font-family:var(--font-mono);font-size:.7rem;letter-spacing:.18em;text-transform:uppercase;color:var(--blue-light);margin-bottom:1.4rem;}}
.sec-hero h1{{font-family:var(--font-display);font-size:clamp(2.1rem,5vw,3.2rem);line-height:1.15;font-weight:400;margin-bottom:1.4rem;color:var(--white);}}
.sec-hero h1 em{{display:block;font-style:italic;color:var(--blue-light);}}
.sec-hero .lead{{color:var(--ice);font-size:1.08rem;max-width:42rem;line-height:1.7;margin-bottom:2rem;}}
.sec-hero .fine{{color:rgba(216,234,245,.62);font-size:.85rem;margin-top:1rem;}}
.btn-row{{display:flex;gap:.75rem;flex-wrap:wrap;align-items:center;}}
.btn-p{{display:inline-block;background:var(--blue);color:#fff;text-decoration:none;padding:.9rem 1.7rem;border-radius:4px;font-size:.92rem;font-weight:600;}}
.btn-p:hover{{background:var(--blue-light);}}
.btn-s{{display:inline-block;color:var(--white);text-decoration:none;padding:.9rem 1.5rem;border:1px solid rgba(216,234,245,.35);border-radius:4px;font-size:.9rem;}}
.btn-s:hover{{border-color:var(--blue-light);color:var(--blue-light);}}
.reco-badge{{display:inline-flex;align-items:center;gap:1.1rem;text-decoration:none;border:1px solid rgba(216,234,245,.26);border-radius:6px;background:rgba(255,255,255,.05);padding:.9rem 1.3rem;margin-top:2.2rem;}}
.reco-badge:hover{{border-color:rgba(216,234,245,.5);}}
.reco-badge .score{{font-family:var(--font-display);font-size:1.8rem;color:var(--white);line-height:1;}}
.reco-badge .stars{{color:var(--warm);font-size:.9rem;letter-spacing:.08em;display:block;}}
.reco-badge .lbl{{font-family:var(--font-mono);font-size:.62rem;letter-spacing:.15em;text-transform:uppercase;color:var(--warm);display:block;margin:.15rem 0;}}
.reco-badge .sub{{font-size:.78rem;color:rgba(216,234,245,.78);}}
.reco-badge .ver{{padding-left:1.1rem;border-left:1px solid rgba(216,234,245,.22);font-size:.71rem;color:rgba(216,234,245,.65);line-height:1.4;}}
.reco-badge .ver b{{display:block;color:var(--warm);}}
.sec-stats{{display:flex;gap:3rem;flex-wrap:wrap;margin-top:2.6rem;padding-top:1.9rem;border-top:1px solid rgba(216,234,245,.2);}}
.sec-stats .v{{font-family:var(--font-display);font-size:1.7rem;color:var(--white);line-height:1.1;}}
.sec-stats .l{{font-family:var(--font-mono);font-size:.62rem;letter-spacing:.14em;text-transform:uppercase;color:rgba(216,234,245,.55);margin-top:.35rem;}}
.sec-toc{{background:var(--ice-faint);border-bottom:1px solid var(--border);}}
.sec-toc .inner{{display:flex;gap:1.5rem;flex-wrap:wrap;align-items:center;padding:1rem 0;}}
.sec-toc .lbl{{font-family:var(--font-mono);font-size:.63rem;letter-spacing:.15em;text-transform:uppercase;color:var(--text-light);}}
.sec-toc a{{font-size:.85rem;color:var(--navy);text-decoration:none;border-bottom:1px solid transparent;}}
.sec-toc a:hover{{border-bottom-color:var(--blue);}}
.sec-body{{max-width:47rem;}}
.sec-body section{{padding:3.2rem 0;}}
.sec-body section + section{{border-top:1px solid var(--border);}}
.sec-body h2{{font-family:var(--font-display);font-weight:400;font-size:clamp(1.6rem,3.2vw,2.2rem);line-height:1.22;color:var(--navy);margin-bottom:1.1rem;}}
.sec-body h2 em{{font-style:italic;color:var(--blue);}}
.sec-body h3{{font-size:1rem;font-weight:600;color:var(--navy);margin:1.9rem 0 .5rem;}}
.sec-body p{{color:var(--text-mid);line-height:1.75;margin-bottom:1.1rem;}}
.sec-body .lead-p{{font-size:1.08rem;color:var(--text);}}
.sec-body ul{{padding-left:1.15rem;margin-bottom:1.1rem;color:var(--text-mid);}}
.sec-body li{{margin-bottom:.5rem;line-height:1.7;}}
.sec-body table{{width:100%;border-collapse:collapse;margin:1.4rem 0;font-size:.92rem;}}
.sec-body th,.sec-body td{{text-align:left;padding:.8rem .75rem .8rem 0;border-bottom:1px solid var(--border);vertical-align:top;}}
.sec-body th{{font-family:var(--font-mono);font-size:.64rem;letter-spacing:.13em;text-transform:uppercase;color:var(--navy);font-weight:600;}}
.sec-body td{{color:var(--text-mid);}}
.sec-body td strong{{color:var(--navy);}}
.box{{background:var(--ice-faint);border-left:3px solid var(--blue);padding:1.3rem 1.5rem;margin:1.6rem 0;}}
.box p:last-child{{margin-bottom:0;}}
.box-warn{{background:var(--bg-warm);border-left:3px solid var(--warm);padding:1.3rem 1.5rem;margin:1.6rem 0;}}
.box-warn ul{{margin-bottom:0;}}
.card-grid{{display:grid;grid-template-columns:repeat(auto-fit,minmax(255px,1fr));gap:1rem;margin-top:1.5rem;}}
.mb-card{{border:1px solid var(--border);padding:1.4rem;text-decoration:none;display:block;background:#fff;transition:border-color .18s,transform .18s;}}
.mb-card:hover{{border-color:var(--blue);transform:translateY(-2px);}}
.mb-card .k{{font-family:var(--font-mono);font-size:.6rem;letter-spacing:.14em;text-transform:uppercase;color:var(--blue);display:block;margin-bottom:.5rem;}}
.mb-card .t{{font-family:var(--font-display);font-size:1.1rem;color:var(--navy);margin-bottom:.35rem;line-height:1.3;}}
.mb-card .d{{font-size:.86rem;color:var(--text-mid);margin:0;line-height:1.6;}}
.mb-card .p{{font-family:var(--font-mono);font-size:.75rem;color:var(--blue);margin-top:.65rem;}}
.faq-i{{border-bottom:1px solid var(--border);padding:1.3rem 0;}}
.faq-i .q{{font-weight:600;color:var(--navy);margin-bottom:.5rem;}}
.faq-i .a{{color:var(--text-mid);margin:0;line-height:1.72;}}
.sec-band{{background:linear-gradient(135deg,var(--navy) 0%,var(--navy-light) 100%);color:var(--white);padding:3.6rem 0;}}
.sec-band h2{{font-family:var(--font-display);font-weight:400;font-size:clamp(1.6rem,3.2vw,2.1rem);color:var(--white);margin-bottom:1rem;}}
.sec-band h2 em{{font-style:italic;color:var(--blue-light);}}
.sec-band p{{color:var(--ice);max-width:40rem;margin-bottom:1.7rem;line-height:1.7;}}
.src{{font-size:.86rem;color:var(--text-mid);}}
.src li{{margin-bottom:.6rem;}}
@media(max-width:760px){{.sec-stats{{gap:1.6rem;}}.reco-badge{{flex-wrap:wrap;gap:.8rem;}}}}
</style>
</head>
{SHELL['body_open']}
{SHELL['header']}
{content}
{SHELL['footer']}
{SHELL['tail']}"""


def reco():
    return """<a class="reco-badge" href="https://www.reco.se/medibalans-christina-biri-ab" rel="noopener">
<span class="score">4.87</span>
<span>
  <span class="stars">★★★★★</span>
  <span class="lbl">Bäst i Sverige</span>
  <span class="sub">Verifierade patientrecensioner · Reco.se</span>
</span>
<span class="ver">Reco.se<b>Verifierad</b></span>
</a>"""


def hero(eyebrow, h1, h1_em, lead, buttons, fine="", stats=None):
    s = ""
    if stats:
        s = '<div class="sec-stats">' + "".join(
            f'<div><div class="v">{v}</div><div class="l">{l}</div></div>' for v, l in stats) + "</div>"
    return f"""<section class="sec-hero"><div class="container">
<p class="eyebrow">{eyebrow}</p>
<h1>{h1}<em>{h1_em}</em></h1>
<p class="lead">{lead}</p>
<div class="btn-row">{buttons}</div>
{f'<p class="fine">{fine}</p>' if fine else ''}
{reco()}
{s}
</div></section>"""


def toc(items):
    links = "".join(f'<a href="#{a}">{t}</a>' for a, t in items)
    return f'<div class="sec-toc"><div class="container"><div class="inner"><span class="lbl">På denna sida</span>{links}</div></div></div>'


def band(h2, h2em, p):
    return f"""<section class="sec-band"><div class="container">
<h2>{h2}<em> {h2em}</em></h2><p>{p}</p>
<div class="btn-row">
<a class="btn-p" href="/#booking">Boka konsultation</a>
<a class="btn-s" href="tel:+46723195070">072-319 50 70</a>
</div></div></section>"""


def faq_html(items):
    return "".join(f'<div class="faq-i"><p class="q">{q}</p><p class="a">{a}</p></div>' for q, a in items)


def faq_schema(url, items):
    import json
    return ('<script type="application/ld+json">' + json.dumps({
        "@context": "https://schema.org", "@type": "FAQPage",
        "@id": url + "#faq",
        "mainEntity": [{"@type": "Question", "name": q,
                        "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in items]
    }, ensure_ascii=False) + "</script>")
