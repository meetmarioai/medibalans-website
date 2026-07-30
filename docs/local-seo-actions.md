# Local SEO — åtgärdslista
**Skapad 2026-07-30. Bakgrund:** Reco 4.87 (bäst i Sverige) men Google Business Profile visar bara
383 visningar/månad och Google efterfrågar aktivt fler recensioner. Recos omdömen räknas **inte**
som rankingsignal hos Google. Google-recensioner styr det lokala kartpaketet, som ligger **ovanför**
de organiska resultaten för sökningar som "iv drip stockholm" och "funktionsmedicin stockholm".

Konkurrensläget: Nordic Clinic har **0 verifierade Reco-omdömen** (profil ej verifierad,
trovärdighet "Låg"). Funmed Stockholm har 171 omdömen med 4.1 i snitt, ej verifierad profil.
Det lokala paketet är alltså den enda arenan där kvalitetsförsprånget kan omvandlas till synlighet
snabbt — ingen konkurrent har något att samla in.

---

## 1. Klart — gjort på webbplatsen

- **En kanonisk klinikentitet.** Alla 33 `MedicalClinic`-entiteter delar nu samma
  `@id` (`https://www.medibalans.com/#clinic`) och exakt samma adress. Tidigare fanns flera
  olänkade klinikentiteter, vilket lät "Medibalans Hudiksvall" och "Medibalans Göteborg"
  konkurrera om samma varumärke i Googles entitetsmodell.
- **Kompletterade lokala fält:** `addressRegion`, `openingHoursSpecification` (strukturerad form),
  `priceRange`, `currenciesAccepted`, `areaServed`, `geo`, `isAcceptingNewPatients`,
  `sameAs` → Reco.
- **NAP internt konsekvent:** Banérgatan 10, 1 tr · 115 23 Stockholm · +46 72 319 50 70 på samtliga
  sidor. Inga spår av Karlavägen, Birger Jarlsgatan eller Victoriakliniken kvar.

---

## 2. Google Business Profile — högst prioritet

Recensioner på Google är den enda recensionssignal som påverkar det lokala paketet.

**Hämta din recensionslänk:** Google Business Profile → **"Åtgärda begäran om recensioner" /
"Ask for reviews"** → kopiera kortlänken (formen `https://g.page/r/…/review`).
Klistra in den nedan så den finns på ett ställe:

    GOOGLE-RECENSIONSLÄNK: ______________________________________

**Att komplettera i profilen:**

- [ ] Tjänster — lägg in ALCAT, CMA, MethylDetox, IV-terapi, Glutation IV, D-vitamin injektion,
      SIBO-test, Kroppsskanning. Kategoriserade tjänster driver matchning på tjänstesökningar.
- [ ] Kategori — primär bör vara en medicinsk klinikkategori, **inte** skönhet/hudvård.
- [ ] Foton — kliniken, behandlingsrummet, utrustning. Nya bilder väger.
- [ ] Inlägg — publicera regelbundet (samma innehåll som kunskapsbanken fungerar).
- [ ] Bokningslänk — peka mot bokningsflödet.
- [ ] Öppettider, telefon, adress — måste matcha webbplatsen exakt (se NAP ovan).

---

## 3. Recensionsförfrågan — färdig text

**Regler som måste följas:**
- **Ingen ersättning eller rabatt** i utbyte mot omdöme. Bryter mot Googles policy.
- **Ingen gallring.** Fråga alla, inte bara de nöjda. "Review gating" bryter mot policyn.
- **Ingen hälsoinformation i meddelandet.** Skriv aldrig diagnos, provsvar eller behandling —
  meddelandet kan läsas av andra. Håll det neutralt.
- Skicka gärna 3–7 dagar efter återbesök/provsvarsgenomgång, när upplevelsen är färsk.

### Svenska (SMS / e-post)

> Hej [Förnamn],
>
> Tack för ditt besök hos MediBalans.
>
> Om du har två minuter skulle vi vara tacksamma för din återkoppling på Google. Det hjälper
> andra som letar efter en klinik att veta vad de kan förvänta sig — och det hjälper oss att bli
> bättre.
>
> [GOOGLE-RECENSIONSLÄNK]
>
> Skriv gärna precis som du upplevde det, både det som fungerade och det som kan bli bättre.
>
> Vänliga hälsningar,
> MediBalans · Banérgatan 10, Stockholm

### English (SMS / email)

> Hello [First name],
>
> Thank you for visiting MediBalans.
>
> If you have two minutes, we would be grateful for your feedback on Google. It helps other
> people looking for a clinic know what to expect — and it helps us improve.
>
> [GOOGLE REVIEW LINK]
>
> Please write it exactly as you experienced it, both what worked and what could be better.
>
> Kind regards,
> MediBalans · Banérgatan 10, Stockholm

---

## 4. Felaktiga externa listningar — måste rättas

Dessa motsäger varandra och undergräver den lokala rankingen. Google läser motstridiga
signaler om var verksamheten finns och vad den gör.

| Plats | Problem | Åtgärd |
|---|---|---|
| **Hitta.se** | Listar MediBalans på **Karlavägen 89** — inaktuell adress | Begär adressändring till Banérgatan 10, 1 tr, 115 23 Stockholm |
| **Bokadirekt** | Listar *MediBalans Christina Biri AB* som **"Ansiktsbehandling, microneedling, Dermapen, LPG — hudvård"** | Ändra kategori till medicinsk klinik, eller avpublicera listningen |
| **Reco** | Korrekt och verifierad — inget att göra | Behåll. Fortsätt samla omdömen här också (bra för konvertering) |
| **allabolag.se** | Korrekt: org.nr 559249-7290, Banérgatan 10 | Inget |

Bokadirekt-listningen är den allvarligaste: en precisionsmedicinsk klinik presenterad som
hudvårdsmottagning på en svensk bokningssajt med hög auktoritet förvirrar Googles bild av
vad verksamheten är.

---

## 5. Öppna frågor att bekräfta

- **Juridisk entitet i schema.** Webbplatsens footer anger "© MediBalans AB" medan Reco och
  allabolag anger "MediBalans Christina Biri AB" (org.nr 559249-7290, Banérgatan 10). Jag har
  medvetet **inte** lagt in `legalName`/organisationsnummer i strukturerad data eftersom de två
  bolagen skiljer sig — bekräfta vilket som är vårdgivaren innan det skrivs in. Org.nr i schema
  är den starkaste signalen för att skilja er från "Medibalans Hudiksvall" och "Göteborg".
- **`og-image.jpg` finns inte i repot** men refereras som `og:image` på samtliga sidor. Kontrollera
  att filen faktiskt ligger på servern — annars saknar alla delningar förhandsbild.
- **`aggregateRating` (4.87 / 86 omdömen) ligger i klinikens schema.** Google visar inte
  stjärnor för omdömen som en verksamhet publicerar om sig själv, så det ger inga rika resultat.
  Det är inte skadligt, men räkna inte med effekt. Riktiga stjärnor i sökresultatet kommer via
  Google-recensioner, inte via markup.
- **Sociala profiler till `sameAs`.** Reco och Facebook (`facebook.com/MediBalans/`) är inlagda
  på samtliga 33 klinikentiteter. Skicka URL till **Instagram och LinkedIn** så läggs även de in —
  varje verifierad profil stärker entitetskopplingen och hjälper Google skilja er från
  "Medibalans Hudiksvall" och "Medibalans Göteborg".

---

## 6. Ordning jag skulle ta det i

1. Google-recensioner igång (störst effekt, ingen konkurrens, veckor)
2. Bokadirekt-kategorin (aktiv skada)
3. Hitta.se-adressen (aktiv skada)
4. GBP-tjänster, foton, kategori
5. Bekräfta juridisk entitet → lägg in org.nr i schema
6. Skicka sociala URL:er → `sameAs`
