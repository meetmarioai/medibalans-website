# Hälsodeklaration före besök — MediBalans

**Status: UTKAST för klinisk granskning av Dr Mario Anthis.**
Innehållet nedan är strukturerat och motiverat, men de kliniska urvalsfrågorna måste godkännas
av behandlande läkare innan formuläret används. Jag är inte kliniker — jag har byggt underlaget
utifrån de behandlingar och tester MediBalans faktiskt erbjuder, och angett syftet med varje
säkerhetsfråga så att varje uppgift kan motiveras.

---

## Var formuläret ska ligga

**Rekommendation: Cliniko nu, Meet Mario senare.**

Cliniko är redan bokningssystemet. Formuläret kan kopplas till besökstypen och skickas
automatiskt vid bokning — vilket är precis "före varje besök". Cliniko är ett
journalsystem med åtkomstkontroll och loggning, vilket är vad patientdatalagen förutsätter.
Ingen utvecklingstid krävs.

**Ska inte ligga på medibalans.com.** En hälsodeklaration innehåller uppgifter om hälsa =
särskild kategori av personuppgifter (GDPR art. 9). Ett formulär på en statiskt hostad
webbplats som mejlar svaren till en inkorg uppfyller inte kraven på åtkomstkontroll,
loggning eller journalföring. Webbplatsen ska på sin höjd länka till formuläret.

När Meet Mario-bokningen är klar: flytta dit, och bygg in konverteringsspårningen samtidigt
(det saknas idag — se `docs/local-seo-actions.md`).

---

## Del 1 — Identitet och kontakt

| Fält | Typ | Obl. |
|---|---|---|
| Förnamn | text | ✔ |
| Efternamn | text | ✔ |
| Personnummer | text (ÅÅÅÅMMDD-XXXX) | ✔ |
| Telefon | tel | ✔ |
| E-post | email | ✔ |
| Adress, postnummer, ort | text | ✔ |
| Närmast anhörig + telefon | text | ✔ |
| Annan vårdgivare/läkare som följer dig | text | — |

*Personnummer krävs för journalföring enligt patientdatalagen. Anhörig krävs eftersom IV-behandling
ges på mottagningen.*

---

## Del 2 — Anledning till besöket

| Fält | Typ |
|---|---|
| Huvudsakligt besvär, med dina egna ord | textarea |
| Hur länge har besvären funnits? | < 3 mån / 3–12 mån / 1–5 år / > 5 år |
| Vad har redan utretts, och var? | textarea |
| Har du provsvar att bifoga? | fil-uppladdning (flera) |
| Vad hoppas du att besöket ska leda till? | textarea |

---

## Del 3 — Sjukdomshistoria

Kryssa allt som gäller, med årtal om möjligt:

- Hjärt-/kärlsjukdom · högt blodtryck · arytmi eller AV-block
- Njursjukdom eller nedsatt njurfunktion · njursten
- Leversjukdom
- Diabetes (typ 1 / typ 2)
- Sköldkörtelsjukdom (hypo-/hypertyreos, Hashimoto)
- Autoimmun sjukdom — ange vilken
- Cancer, pågående eller tidigare — ange när
- Blodsjukdom, blödningsbenägenhet eller anemi
- **G6PD-brist (glukos-6-fosfatdehydrogenasbrist)**
- **Hemokromatos eller järnöverskott**
- **Sarkoidos, hyperparatyreoidism eller tidigare hyperkalcemi**
- **Myasteni (myasthenia gravis)**
- Astma eller känd sulfitkänslighet
- Epilepsi
- Psykiatrisk diagnos under behandling
- Mag-/tarmsjukdom — IBD, celiaki, IBS
- Genomgången obesitaskirurgi eller annan tarmoperation
- Graviditet nu, planerad graviditet, eller amning
- Annat — fritext

### Varför de fetmarkerade frågorna finns

Dessa är direkta kontraindikationer eller doseringsspärrar för behandlingar MediBalans erbjuder.
De ska kunna motiveras var för sig vid en granskning:

| Fynd | Konsekvens |
|---|---|
| **G6PD-brist** | Högdos intravenöst C-vitamin kan utlösa hemolys. Absolut kontraindikation — måste efterfrågas före C-vitamin IV och Myers Cocktail. |
| **Njursvikt / njursten** | Högdos C-vitamin ökar oxalatbelastningen; magnesium ackumuleras vid nedsatt utsöndring. Dosjustering eller avstående. |
| **Sarkoidos, hyperparatyreoidism, tidigare hyperkalcemi** | D-vitamin kan utlösa hyperkalcemi. Relevant för D3 100 000 IE depå. |
| **Hemokromatos / järnöverskott** | C-vitamin ökar järnupptag och kan förvärra överskott. |
| **Myasteni** | Magnesium kan förvärra muskelsvaghet. Kontraindikation för magnesium IM/IV. |
| **Arytmi / AV-block** | Intravenöst magnesium påverkar hjärtets överledning. |
| **Astma / sulfitkänslighet** | Sulfit förekommer som konserveringsmedel i vissa injektionspreparat. |
| **Graviditet / amning** | Påverkar både D3-högdos och IV-behandling generellt. |

---

## Del 4 — Läkemedel, tillskott och reaktioner

| Fält | Typ | Obl. |
|---|---|---|
| Läkemedel du tar just nu — namn och dos | textarea | ✔ |
| Tar du blodförtynnande (Waran, Eliquis, Xarelto, ASA)? | ja/nej + vilket | ✔ |
| Kortison, immunhämmande eller biologiska läkemedel? | ja/nej + vilket | ✔ |
| **Kosttillskott och vitaminer just nu — namn, form och dos** | textarea | ✔ |
| Tar du NAD⁺-prekursorer (NMN, NR, niacinamid)? | ja/nej + dos | ✔ |
| Läkemedelsallergi eller överkänslighet | textarea | ✔ |
| **Har du någon gång reagerat på injektion, dropp eller kontrastmedel?** | ja/nej + beskriv | ✔ |
| Har du haft anafylaktisk reaktion? | ja/nej + beskriv | ✔ |

*Tillskottsfrågan är inte formalia. Form och dos av folat, B12 och NAD⁺-prekursorer påverkar
tolkningen av metylering och homocystein direkt — se `/homocystein/` och `/ratt-form-av-tillskott/`.
Blodförtynnande är relevant vid högdos C- och E-vitamin.*

---

## Del 5 — Inför provtagning

Dessa frågor avgör om ett test blir tolkningsbart. Ställs villkorat utifrån vad som är bokat.

| Fråga | Varför |
|---|---|
| Har du tagit antibiotika de senaste 4 veckorna? | Invaliderar SIBO-andningstest |
| Tar du probiotika, och sedan när? | Påverkar mikrobiomanalys |
| Tar du PPI/syrahämmare (omeprazol m.fl.)? | Påverkar tarm- och mikrobiomtester |
| **Har du redan uteslutit gluten eller andra livsmedel?** | Celiakiprov blir opålitligt efter glutenfri kost. Måste fångas före elimination. |
| Har du ändrat kosten inför besöket? | Påverkar ALCAT och organiska syror |
| Datum för senaste blodprov, och var | Undvik dubbelprovtagning |

---

## Del 6 — Levnadsvanor

Kort, men journalförs — och är kliniskt relevant för hans protokoll.

- Kost i stort (fritext) · antal måltider/dag
- Alkohol: enheter/vecka
- Tobak/nikotin: nej / snus / rökning / vape
- Fysisk aktivitet: ggr/vecka och typ
- Sömn: timmar/natt · insomningssvårigheter ja/nej
- Upplevd stressnivå 1–10
- Yrke och eventuell exponering (kemikalier, lösningsmedel, metaller)

---

## Del 7 — Samtycke

Två separata samtycken. De ska kunna kryssas var för sig — buntade samtycken håller inte.

**7.1 Samtycke till vård och behandling**

> Jag har lämnat uppgifterna ovan efter min bästa kännedom och förstår att ofullständiga
> uppgifter kan påverka min säkerhet vid provtagning och behandling. Jag förstår att
> legitimerad läkare gör en individuell bedömning före varje behandling, och att behandling
> kan avstås om det bedöms olämpligt.

☐ Jag samtycker *(obligatoriskt)*

**7.2 Information om personuppgifter**

> MediBalans behandlar dina uppgifter för att kunna ge vård och för att föra patientjournal.
> Uppgifter om hälsa är särskild kategori av personuppgifter. Rättslig grund är vård och
> behandling samt den lagstadgade skyldigheten att föra journal enligt patientdatalagen
> (2008:355). Journaluppgifter bevaras i minst tio år enligt lag. Du har rätt att begära
> registerutdrag och rättelse. Fullständig information finns i vår
> [integritetspolicy](https://www.medibalans.com/integritetspolicy/).

☐ Jag har tagit del av informationen *(obligatoriskt)*

**7.3 Frivilligt**

☐ Jag vill få information om nya utredningar och behandlingar via e-post *(frivilligt — får inte
vara ett villkor för vård)*

---

## Del 8 — Att bekräfta innan formuläret används

- [ ] **Klinisk granskning.** Läkare godkänner urvalsfrågorna i del 3–5, särskilt
      kontraindikationslistan. Lägg till eller ta bort utifrån vad ni faktiskt ger.
- [ ] **Uppgiftsminimering.** Varje fält ska ha ett syfte. Motiveringarna ovan finns just för
      detta — ta bort fält ni inte agerar på.
- [ ] **Personuppgiftsbiträdesavtal med Cliniko** finns och är aktuellt.
- [ ] **Var lagras uppladdade provsvar?** Om filer laddas upp måste lagringen omfattas av
      samma skydd som journalen.
- [ ] **Vem har åtkomst?** Endast vårdpersonal som deltar i vården. Loggning på.
- [ ] **Rutin vid röda flaggor.** Om patienten kryssar G6PD-brist, myasteni, sarkoidos,
      graviditet eller tidigare infusionsreaktion — vad händer då i flödet? Bör flaggas
      automatiskt före besöket, inte upptäckas i behandlingsrummet.
- [ ] **Barn och unga.** Egen variant krävs om vårdnadshavare fyller i (ni tar emot barn).
- [ ] **Språk.** Svensk och engelsk version, samma innehåll.

---

# Pre-appointment health declaration — English

Mirror of the Swedish version. Same fields, same required flags, same two-part consent.

## 1 — Identity and contact
First name · Surname · Personal ID number · Phone · Email · Address · Next of kin and phone ·
Other treating physician.

## 2 — Reason for visit
Main complaint in your own words · Duration (<3 months / 3–12 months / 1–5 years / >5 years) ·
What has already been investigated, and where · Upload previous results · What you hope the
visit will lead to.

## 3 — Medical history
Cardiovascular disease · hypertension · arrhythmia or AV block · Kidney disease or impaired
renal function · kidney stones · Liver disease · Diabetes (type 1 / 2) · Thyroid disease ·
Autoimmune disease (specify) · Cancer, current or previous (when) · Blood disorder, bleeding
tendency or anaemia · **G6PD deficiency** · **Haemochromatosis or iron overload** ·
**Sarcoidosis, hyperparathyroidism or previous hypercalcaemia** · **Myasthenia gravis** ·
Asthma or known sulphite sensitivity · Epilepsy · Psychiatric diagnosis under treatment ·
Gastrointestinal disease (IBD, coeliac, IBS) · Previous bariatric or bowel surgery ·
Pregnancy, planned pregnancy or breastfeeding · Other.

*The bolded items are contraindications or dose limits for treatments MediBalans provides —
see the rationale table in the Swedish section.*

## 4 — Medication, supplements and reactions
Current medication with doses · Anticoagulants (which) · Corticosteroids, immunosuppressants or
biologics · **Current supplements — name, form and dose** · NAD⁺ precursors (NMN, NR,
nicotinamide) · Drug allergy or hypersensitivity · **Any previous reaction to an injection,
infusion or contrast medium** · Any anaphylactic reaction.

## 5 — Before sampling
Antibiotics in the last 4 weeks (invalidates SIBO breath test) · Probiotics, and since when ·
PPI or acid suppression · **Have you already excluded gluten or other foods?** (coeliac testing
becomes unreliable) · Recent dietary change · Date and place of most recent blood test.

## 6 — Lifestyle
Diet overview · meals per day · Alcohol units per week · Tobacco/nicotine · Physical activity ·
Sleep hours and difficulty falling asleep · Perceived stress 1–10 · Occupation and any exposure
to chemicals, solvents or metals.

## 7 — Consent
**7.1 Consent to care and treatment** — I have provided the above to the best of my knowledge and
understand that incomplete information may affect my safety during sampling and treatment. I
understand a licensed physician makes an individual assessment before every treatment and may
decline treatment if considered inappropriate. ☐ *required*

**7.2 Personal data information** — MediBalans processes your data to provide care and maintain a
patient record. Health data is a special category of personal data. The legal basis is the
provision of care and the statutory obligation to keep records under the Swedish Patient Data Act
(2008:355). Records are retained for at least ten years as required by law. You may request access
and rectification. See our [privacy policy](https://www.medibalans.com/en/privacy-policy/).
☐ *required*

**7.3 Optional** — ☐ I would like information about new investigations and treatments by email
*(optional; may not be a condition of care)*
