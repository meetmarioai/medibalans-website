/**
 * MediBalans booking block.
 *
 * Replaces the embedded Cliniko iframe. Native markup on medibalans.com, calling
 * the booking API on meetmario.ai.
 *
 * Usage — one element, one script tag, no build step:
 *
 *   <div data-mb-booking data-service="konsultation"></div>
 *   <script src="/assets/booking.js" defer></script>
 *
 * data-service is optional; omitted, it books the in-person initial consultation.
 * The slug names a SERVICE, never an appointment type — the server holds a closed
 * allow-list and re-resolves everything. Nothing this file sends is trusted.
 *
 * ── Why not the iframe ──────────────────────────────────────────────────────
 *
 * The Cliniko iframe could not be styled, could not be measured, offered every
 * appointment type the account has — including the IV infusions the clinic does
 * not take on request — and could not collect a personnummer. It also broke the
 * page's own reveal animations by resizing itself after paint.
 *
 * ── Scheduling only ─────────────────────────────────────────────────────────
 *
 * There is deliberately NO symptom, condition, or reason-for-visit field. Adding
 * one would pull this inside EU MDR and would put health information into an
 * email and SMS channel that must never carry it. Do not add one.
 */
(function () {
  "use strict";

  var API = "https://www.meetmario.ai";

  // ── Copy ──────────────────────────────────────────────────────────────────
  var T = {
    sv: {
      pickDay: "Välj en dag",
      pick: "Välj en tid",
      pickWho: "Välj läkare",
      anyone: "Först ledig",
      withWhom: "Läkare",
      prevMonth: "Föregående månad",
      nextMonth: "Nästa månad",
      noneThisMonth: "Inga lediga tider den här månaden. Bläddra framåt.",
      backToCalendar: "Byt dag",
      loading: "Hämtar lediga tider…",
      noSlots:
        "Inga tider är lediga just nu. Ring 072-319 50 70 så hittar vi en tid åt dig.",
      loadError:
        "Kunde inte hämta lediga tider just nu. Försök igen om en stund, eller ring 072-319 50 70.",
      retry: "Försök igen",
      details: "Dina uppgifter",
      firstName: "Förnamn",
      lastName: "Efternamn",
      personnummer: "Personnummer",
      pnrHint: "ÅÅÅÅMMDD-XXXX — vi använder det för att identifiera din journal.",
      email: "E-post",
      phone: "Mobilnummer",
      phoneHint: "Hit skickar vi din påminnelse.",
      submit: "Bekräfta bokning",
      submitting: "Bokar…",
      back: "Byt tid",
      chosen: "Vald tid",
      confirmedTitle: "Din tid är bokad",
      // Future tense, deliberately. The API returns the channel it INTENDS to
      // use, not one it has used — the confirmation is sent in the background
      // after the response has gone out. On 2026-08-05 a real booking reported
      // "vi har skickat" for an email that was never sent, because the
      // serverless function ended before the send completed. "Är på väg" is
      // true whether it has left yet or not.
      confirmedBoth: "En bekräftelse är på väg till din e-post och ditt mobilnummer.",
      confirmedEmail: "En bekräftelse är på väg till din e-post.",
      confirmedSms: "En bekräftelse är på väg till ditt mobilnummer.",
      confirmedNone: "Skriv gärna upp tiden — bekräftelsen kunde inte skickas.",
      taken: "Den tiden blev precis bokad av någon annan. Välj en annan tid.",
      rateLimited: "För många försök. Vänta en stund och försök igen.",
      upstream: "Något gick fel hos oss. Ingen bokning gjordes. Ring 072-319 50 70 så hjälper vi dig.",
      required: "Fyll i fältet.",
      integrity:
        "Dina uppgifter används endast för att boka och bekräfta ditt besök.",
    },
    en: {
      pickDay: "Choose a day",
      pick: "Choose a time",
      pickWho: "Choose a doctor",
      anyone: "First available",
      withWhom: "Doctor",
      prevMonth: "Previous month",
      nextMonth: "Next month",
      noneThisMonth: "No times available this month. Try the next one.",
      backToCalendar: "Change day",
      loading: "Loading available times…",
      noSlots:
        "No times are free right now. Call +46 72 319 50 70 and we will find you one.",
      loadError:
        "We could not load available times just now. Try again shortly, or call +46 72 319 50 70.",
      retry: "Try again",
      details: "Your details",
      firstName: "First name",
      lastName: "Last name",
      personnummer: "Personal ID number",
      pnrHint: "YYYYMMDD-XXXX — we use it to identify your record.",
      email: "Email",
      phone: "Mobile number",
      phoneHint: "This is where your reminder goes.",
      submit: "Confirm booking",
      submitting: "Booking…",
      back: "Change time",
      chosen: "Chosen time",
      confirmedTitle: "Your appointment is booked",
      // Future tense — see the Swedish block above for why.
      confirmedBoth: "A confirmation is on its way to your email and your mobile.",
      confirmedEmail: "A confirmation is on its way to your email.",
      confirmedSms: "A confirmation is on its way to your mobile.",
      confirmedNone: "Please note the time down — the confirmation could not be sent.",
      taken: "That time was just taken by someone else. Please choose another.",
      rateLimited: "Too many attempts. Please wait a moment and try again.",
      upstream: "Something went wrong on our side. No booking was made. Call +46 72 319 50 70.",
      required: "This field is required.",
      integrity: "Your details are used only to book and confirm your visit.",
    },
  };

  function lang() {
    if (/^\/en(\/|$)/.test(location.pathname)) return "en";
    var l = (document.documentElement.lang || "sv").slice(0, 2).toLowerCase();
    return l === "en" ? "en" : "sv";
  }

  // ── Personnummer, client side ─────────────────────────────────────────────
  //
  // The server validates again and its answer is the one that counts. This is
  // here so a typo is caught before the patient has filled in five more fields.
  // Same Luhn check as app/lib/personnummer.js.
  function pnrValid(raw) {
    var d = String(raw || "").replace(/\D/g, "");
    if (d.length === 12) d = d.slice(2);
    if (d.length !== 10) return false;
    var sum = 0;
    for (var i = 0; i < 9; i++) {
      var n = Number(d[i]) * (i % 2 === 0 ? 2 : 1);
      sum += n > 9 ? n - 9 : n;
    }
    return (10 - (sum % 10)) % 10 === Number(d[9]);
  }

  var esc = function (s) {
    return String(s == null ? "" : s).replace(/[&<>"']/g, function (c) {
      return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c];
    });
  };

  // ── Styles ────────────────────────────────────────────────────────────────
  function injectStyles() {
    if (document.getElementById("mb-booking-styles")) return;
    var css = document.createElement("style");
    css.id = "mb-booking-styles";
    css.textContent = [
      ".mb-bk{font-family:var(--font-body,'IBM Plex Sans',sans-serif);color:var(--text,#1A2A3A)}",
      ".mb-bk__lead{font-size:.94rem;line-height:1.65;color:var(--text-mid,#4A5A6A);margin:0 0 1.5rem}",
      ".mb-bk__meta{font-family:var(--font-mono,monospace);font-size:.7rem;letter-spacing:.1em;text-transform:uppercase;color:var(--text-light,#7A8A9A);margin:0 0 .4rem}",
      ".mb-bk__h{font-family:var(--font-display,Georgia,serif);font-size:1.35rem;margin:0 0 .3rem;color:var(--navy,#0B1D33)}",
      // ── practitioner selector ──
      ".mb-bk__who{display:flex;flex-wrap:wrap;gap:.5rem;margin:0 0 1.4rem}",
      ".mb-bk__whobtn{font-family:inherit;font-size:.85rem;padding:.55rem 1rem;border:1px solid var(--border,#D0DBE5);border-radius:999px;background:var(--white,#FAFCFE);color:var(--navy,#0B1D33);cursor:pointer;transition:border-color .15s,background .15s}",
      ".mb-bk__whobtn:hover{border-color:var(--blue,#2E6B9E);background:var(--ice-faint,#EDF5FA)}",
      ".mb-bk__whobtn[aria-pressed=true]{background:var(--navy,#0B1D33);border-color:var(--navy,#0B1D33);color:#fff}",
      ".mb-bk__slotwho{display:block;font-size:.62rem;letter-spacing:.06em;opacity:.7;margin-top:2px}",
      // ── calendar ──
      ".mb-bk__cal{margin:0 0 1.5rem}",
      ".mb-bk__calhead{display:flex;align-items:center;justify-content:space-between;margin:0 0 .9rem}",
      ".mb-bk__month{font-family:var(--font-display,Georgia,serif);font-size:1.1rem;color:var(--navy,#0B1D33);text-transform:capitalize}",
      ".mb-bk__nav{display:flex;gap:.4rem}",
      ".mb-bk__navbtn{width:34px;height:34px;border:1px solid var(--border,#D0DBE5);border-radius:8px;background:var(--white,#FAFCFE);color:var(--navy,#0B1D33);cursor:pointer;font-size:1rem;line-height:1;display:flex;align-items:center;justify-content:center}",
      ".mb-bk__navbtn:hover:not(:disabled){border-color:var(--blue,#2E6B9E);background:var(--ice-faint,#EDF5FA)}",
      ".mb-bk__navbtn:disabled{opacity:.3;cursor:default}",
      ".mb-bk__grid{display:grid;grid-template-columns:repeat(7,1fr);gap:.35rem}",
      ".mb-bk__dow{font-family:var(--font-mono,monospace);font-size:.62rem;letter-spacing:.1em;text-transform:uppercase;color:var(--text-light,#7A8A9A);text-align:center;padding:.3rem 0}",
      ".mb-bk__cell{aspect-ratio:1;border:1px solid transparent;border-radius:8px;background:none;font-family:var(--font-mono,monospace);font-size:.85rem;color:var(--text-light,#7A8A9A);display:flex;flex-direction:column;align-items:center;justify-content:center;gap:2px;padding:0}",
      ".mb-bk__cell--open{border-color:var(--border,#D0DBE5);background:var(--white,#FAFCFE);color:var(--navy,#0B1D33);cursor:pointer;transition:border-color .15s,background .15s}",
      ".mb-bk__cell--open:hover{border-color:var(--blue,#2E6B9E);background:var(--ice-faint,#EDF5FA)}",
      ".mb-bk__cell--open:focus-visible{outline:2px solid var(--blue,#2E6B9E);outline-offset:2px}",
      ".mb-bk__cell[aria-pressed=true]{background:var(--navy,#0B1D33);border-color:var(--navy,#0B1D33);color:#fff}",
      ".mb-bk__cell[aria-pressed=true] .mb-bk__dot{background:#fff}",
      ".mb-bk__dot{width:4px;height:4px;border-radius:50%;background:var(--blue,#2E6B9E)}",
      ".mb-bk__day{margin:0 0 1.25rem}",
      ".mb-bk__dayname{font-family:var(--font-mono,monospace);font-size:.7rem;letter-spacing:.12em;text-transform:uppercase;color:var(--text-light,#7A8A9A);margin:0 0 .5rem}",
      ".mb-bk__times{display:flex;flex-wrap:wrap;gap:.5rem}",
      ".mb-bk__slot{font-family:var(--font-mono,monospace);font-size:.85rem;padding:.6rem 1rem;border:1px solid var(--border,#D0DBE5);border-radius:8px;background:var(--white,#FAFCFE);color:var(--navy,#0B1D33);cursor:pointer;transition:border-color .15s,background .15s,transform .1s}",
      ".mb-bk__slot:hover{border-color:var(--blue,#2E6B9E);background:var(--ice-faint,#EDF5FA)}",
      ".mb-bk__slot:focus-visible{outline:2px solid var(--blue,#2E6B9E);outline-offset:2px}",
      ".mb-bk__slot[aria-pressed=true]{background:var(--navy,#0B1D33);border-color:var(--navy,#0B1D33);color:#fff}",
      ".mb-bk__form{display:grid;gap:.9rem;margin-top:.4rem}",
      ".mb-bk__row{display:grid;gap:.9rem;grid-template-columns:1fr 1fr}",
      "@media(max-width:520px){.mb-bk__row{grid-template-columns:1fr}}",
      ".mb-bk__field label{display:block;font-size:.78rem;font-weight:500;margin:0 0 .3rem;color:var(--text-mid,#4A5A6A)}",
      ".mb-bk__field input{width:100%;box-sizing:border-box;padding:.7rem .8rem;font-family:inherit;font-size:.92rem;border:1px solid var(--border,#D0DBE5);border-radius:8px;background:var(--white,#FAFCFE);color:var(--text,#1A2A3A)}",
      ".mb-bk__field input:focus{outline:none;border-color:var(--blue,#2E6B9E);box-shadow:0 0 0 3px rgba(46,107,158,.12)}",
      ".mb-bk__field input[aria-invalid=true]{border-color:#B85040}",
      ".mb-bk__hint{font-size:.72rem;color:var(--text-light,#7A8A9A);margin:.3rem 0 0}",
      ".mb-bk__err{font-size:.75rem;color:#B85040;margin:.3rem 0 0;min-height:1em}",
      ".mb-bk__btn{font-family:inherit;font-size:.92rem;font-weight:500;padding:.85rem 1.6rem;border:none;border-radius:8px;background:var(--navy,#0B1D33);color:#fff;cursor:pointer;transition:background .15s}",
      ".mb-bk__btn:hover:not(:disabled){background:var(--navy-light,#1A3A5E)}",
      ".mb-bk__btn:disabled{opacity:.55;cursor:default}",
      ".mb-bk__link{background:none;border:none;padding:0;font-family:inherit;font-size:.82rem;color:var(--blue,#2E6B9E);cursor:pointer;text-decoration:underline}",
      ".mb-bk__chosen{display:flex;align-items:baseline;justify-content:space-between;gap:1rem;padding:.85rem 1rem;border:1px solid var(--ice,#D8EAF5);background:var(--ice-faint,#EDF5FA);border-radius:8px;margin:0 0 1.25rem}",
      ".mb-bk__chosen b{font-family:var(--font-mono,monospace);font-weight:500;font-size:.9rem;color:var(--navy,#0B1D33)}",
      ".mb-bk__note{font-size:.72rem;color:var(--text-light,#7A8A9A);margin:1rem 0 0;line-height:1.6}",
      ".mb-bk__alert{padding:.9rem 1rem;border-radius:8px;font-size:.86rem;line-height:1.6;border:1px solid #E8C0B8;background:#FBF2F0;color:#7A3428;margin:0 0 1rem}",
      ".mb-bk__ok{text-align:center;padding:2rem 1rem}",
      ".mb-bk__ok h3{font-family:var(--font-display,Georgia,serif);font-size:1.5rem;color:var(--navy,#0B1D33);margin:0 0 .6rem}",
      ".mb-bk__ok p{color:var(--text-mid,#4A5A6A);font-size:.92rem;line-height:1.65;margin:0 auto;max-width:34ch}",
      ".mb-bk__when{font-family:var(--font-mono,monospace);font-size:1rem;color:var(--navy,#0B1D33);margin:1rem 0 .4rem}",
      ".mb-bk__spin{font-size:.88rem;color:var(--text-light,#7A8A9A)}",
    ].join("");
    document.head.appendChild(css);
  }

  // ── Rendering ─────────────────────────────────────────────────────────────
  function Booking(root) {
    var t = T[lang()];
    var slug = root.getAttribute("data-service") || "";
    var state = {
      slots: [], type: null, practitionerId: null, service: null, chosen: null,
      // Calendar position. `month` is the first of the month being shown;
      // `day` is the selected date key, or null while the grid is up.
      month: null, day: null, cache: {},
      practitioners: [], who: null,
    };

    var MAX_MONTHS_AHEAD = 6;

    function set(html) { root.innerHTML = html; }

    function hhmm(iso) {
      return new Date(iso).toLocaleTimeString(lang() === "en" ? "en-GB" : "sv-SE", {
        timeZone: "Europe/Stockholm", hour: "2-digit", minute: "2-digit",
      });
    }

    // ── Dates ─────────────────────────────────────────────────────────────
    // Stockholm, not the visitor's timezone. A patient in London must not be
    // shown a slot on the wrong day because their browser is an hour behind.
    var TZ = "Europe/Stockholm";
    function dayKeyOf(iso) {
      return new Date(iso).toLocaleDateString("sv-SE", { timeZone: TZ });
    }
    function ymd(d) {
      return d.getFullYear() + "-" + String(d.getMonth() + 1).padStart(2, "0") +
        "-" + String(d.getDate()).padStart(2, "0");
    }
    function firstOfMonth(d) { return new Date(d.getFullYear(), d.getMonth(), 1); }
    function addMonths(d, n) { return new Date(d.getFullYear(), d.getMonth() + n, 1); }

    /** Fetch one month, from today onward. Cached — arrows should be instant. */
    function loadMonth(monthStart) {
      var key = ymd(monthStart) + "|" + (state.who || "all");
      state.month = monthStart;

      if (state.cache[key]) {
        state.slots = state.cache[key];
        renderCalendar();
        return;
      }

      var today = new Date();
      var from = monthStart < firstOfMonth(today) ? today : monthStart;
      // Clamp to today so we never ask for, or display, a time in the past.
      if (from < today) from = today;
      var last = new Date(monthStart.getFullYear(), monthStart.getMonth() + 1, 0);

      set('<p class="mb-bk__spin">' + t.loading + "</p>");
      var url = API + "/api/booking/slots?from=" + ymd(from) + "&to=" + ymd(last) +
        (slug ? "&service=" + encodeURIComponent(slug) : "") +
        (state.who ? "&practitioner=" + encodeURIComponent(state.who) : "");

      fetch(url, { headers: { Accept: "application/json" } })
        .then(function (r) {
          // A failed fetch must never render as "no times available" — an empty
          // month means fully booked, which is a different thing and a lie.
          if (!r.ok) throw new Error("HTTP " + r.status);
          return r.json();
        })
        .then(function (d) {
          if (d.error) throw new Error(d.error);
          state.slots = d.slots || [];
          state.cache[key] = state.slots;
          state.type = d.appointmentType || state.type;
          state.practitionerId = d.practitionerId || state.practitionerId;
          state.service = d.service || state.service;
          if (d.practitioners && d.practitioners.length) state.practitioners = d.practitioners;
          renderCalendar();
        })
        .catch(function (e) {
          if (window.console) console.warn("[mb-booking]", e.message);
          set(
            '<div class="mb-bk__alert">' + t.loadError + "</div>" +
            '<button class="mb-bk__btn" data-retry>' + t.retry + "</button>"
          );
          var b = root.querySelector("[data-retry]");
          if (b) b.addEventListener("click", function () { loadMonth(state.month); });
        });
    }

    function load() { loadMonth(firstOfMonth(new Date())); }

    function serviceHead() {
      var s = state.service;
      if (!s) return "";
      return (
        '<p class="mb-bk__meta">' + esc(s.location && (s.location[lang()] || s.location.sv)) + "</p>" +
        '<h3 class="mb-bk__h">' + esc(s.title && (s.title[lang()] || s.title.sv)) + "</h3>" +
        '<p class="mb-bk__lead">' + esc(s.blurb && (s.blurb[lang()] || s.blurb.sv)) + "</p>"
      );
    }

    /** Slots for the current month, grouped by Stockholm date. */
    function byDay() {
      var m = {};
      state.slots.forEach(function (sl) {
        var k = dayKeyOf(sl.startsAtUtc);
        (m[k] = m[k] || []).push(sl);
      });
      return m;
    }

    function renderCalendar() {
      var locale = lang() === "en" ? "en-GB" : "sv-SE";
      var days = byDay();
      var month = state.month;
      var monthName = month.toLocaleDateString(locale, { month: "long", year: "numeric" });

      var thisMonth = firstOfMonth(new Date());
      var atStart = month <= thisMonth;
      var atEnd = month >= addMonths(thisMonth, MAX_MONTHS_AHEAD);

      // Monday-first, as Sweden and the UK both read it.
      var dow = lang() === "en"
        ? ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
        : ["Mån", "Tis", "Ons", "Tor", "Fre", "Lör", "Sön"];

      var firstWeekday = (new Date(month.getFullYear(), month.getMonth(), 1).getDay() + 6) % 7;
      var daysInMonth = new Date(month.getFullYear(), month.getMonth() + 1, 0).getDate();

      var cells = "";
      for (var i = 0; i < firstWeekday; i++) cells += '<div class="mb-bk__cell"></div>';
      for (var d = 1; d <= daysInMonth; d++) {
        var key = ymd(new Date(month.getFullYear(), month.getMonth(), d));
        var open = (days[key] || []).length;
        cells += open
          ? '<button type="button" class="mb-bk__cell mb-bk__cell--open" aria-pressed="false" ' +
            'data-day="' + key + '" aria-label="' + key + ", " + open + ' tider">' +
            d + '<span class="mb-bk__dot"></span></button>'
          : '<div class="mb-bk__cell" aria-hidden="true">' + d + "</div>";
      }

      var who = "";
      if (state.practitioners.length > 1) {
        who =
          '<p class="mb-bk__meta">' + t.pickWho + "</p>" +
          '<div class="mb-bk__who">' +
          '<button type="button" class="mb-bk__whobtn" data-who="" aria-pressed="' +
            (state.who ? "false" : "true") + '">' + esc(t.anyone) + "</button>" +
          state.practitioners.map(function (p) {
            return '<button type="button" class="mb-bk__whobtn" data-who="' + esc(p.id) +
              '" aria-pressed="' + (state.who === p.id ? "true" : "false") + '">' +
              esc(p.name) + "</button>";
          }).join("") +
          "</div>";
      }

      set(
        serviceHead() + who +
        '<p class="mb-bk__meta">' + t.pickDay + "</p>" +
        '<div class="mb-bk__cal">' +
          '<div class="mb-bk__calhead">' +
            '<span class="mb-bk__month">' + esc(monthName) + "</span>" +
            '<span class="mb-bk__nav">' +
              '<button type="button" class="mb-bk__navbtn" data-prev aria-label="' + t.prevMonth + '"' +
                (atStart ? " disabled" : "") + ">&#8249;</button>" +
              '<button type="button" class="mb-bk__navbtn" data-next aria-label="' + t.nextMonth + '"' +
                (atEnd ? " disabled" : "") + ">&#8250;</button>" +
            "</span>" +
          "</div>" +
          '<div class="mb-bk__grid">' +
            dow.map(function (w) { return '<div class="mb-bk__dow">' + w + "</div>"; }).join("") +
            cells +
          "</div>" +
        "</div>" +
        (Object.keys(days).length ? "" : '<div class="mb-bk__alert">' + t.noneThisMonth + "</div>")
      );

      var prev = root.querySelector("[data-prev]");
      var next = root.querySelector("[data-next]");
      if (prev && !atStart) prev.addEventListener("click", function () { loadMonth(addMonths(month, -1)); });
      if (next && !atEnd) next.addEventListener("click", function () { loadMonth(addMonths(month, 1)); });

      root.querySelectorAll("[data-who]").forEach(function (b) {
        b.addEventListener("click", function () {
          var v = b.getAttribute("data-who");
          state.who = v || null;
          state.cache = {};   // availability differs per clinician
          loadMonth(state.month);
        });
      });

      root.querySelectorAll("[data-day]").forEach(function (b) {
        b.addEventListener("click", function () {
          state.day = b.getAttribute("data-day");
          renderTimes();
        });
      });
    }

    function renderTimes() {
      var days = byDay();
      var list = days[state.day] || [];
      var heading = new Date(list[0] ? list[0].startsAtUtc : state.day)
        .toLocaleDateString(lang() === "en" ? "en-GB" : "sv-SE",
          { timeZone: TZ, weekday: "long", day: "numeric", month: "long" });

      set(
        '<div class="mb-bk__chosen"><span><span class="mb-bk__meta" style="margin:0">' + t.pick +
        '</span><br><b>' + esc(heading) + "</b></span>" +
        '<button type="button" class="mb-bk__link" data-back>' + t.backToCalendar + "</button></div>" +
        '<div class="mb-bk__times">' +
        list.map(function (sl) {
          var whoLabel = (!state.who && state.practitioners.length > 1 && sl.practitionerName)
            ? '<span class="mb-bk__slotwho">' + esc(sl.practitionerName) + "</span>" : "";
          return '<button type="button" class="mb-bk__slot" aria-pressed="false" data-utc="' +
            esc(sl.startsAtUtc) + '" data-prac="' + esc(sl.practitionerId || "") + '">' +
            esc(hhmm(sl.startsAtUtc)) + whoLabel + "</button>";
        }).join("") +
        "</div>"
      );

      root.querySelector("[data-back]").addEventListener("click", renderCalendar);
      root.querySelectorAll(".mb-bk__slot").forEach(function (b) {
        b.addEventListener("click", function () {
          // Match on time AND practitioner. With two doctors both free at
          // 10:00, matching on time alone silently books whichever the server
          // happened to list first — the patient clicks one name and gets the
          // other, and nothing anywhere disagrees.
          var utc = b.getAttribute("data-utc");
          var prac = b.getAttribute("data-prac") || "";
          state.chosen = state.slots.filter(function (x) {
            return x.startsAtUtc === utc && (!prac || String(x.practitionerId || "") === prac);
          })[0];
          renderForm();
        });
      });
    }

    function field(id, label, type, hint, extra) {
      return (
        '<div class="mb-bk__field"><label for="mb-' + id + '">' + label + "</label>" +
        '<input id="mb-' + id + '" name="' + id + '" type="' + type + '" ' + (extra || "") + ">" +
        (hint ? '<p class="mb-bk__hint">' + hint + "</p>" : "") +
        '<p class="mb-bk__err" data-err="' + id + '"></p></div>'
      );
    }

    function renderForm() {
      var when = new Date(state.chosen.startsAtUtc).toLocaleDateString(
        lang() === "en" ? "en-GB" : "sv-SE",
        { timeZone: TZ, weekday: "long", day: "numeric", month: "long" }
      ) + " " + hhmm(state.chosen.startsAtUtc);
      set(
        '<div class="mb-bk__chosen"><span><span class="mb-bk__meta" style="margin:0">' + t.chosen +
        '</span><br><b>' + esc(when) + "</b></span>" +
        '<button type="button" class="mb-bk__link" data-back>' + t.back + "</button></div>" +
        '<p class="mb-bk__meta">' + t.details + "</p>" +
        '<form class="mb-bk__form" novalidate>' +
        '<div class="mb-bk__row">' +
        field("firstName", t.firstName, "text", "", 'autocomplete="given-name" required') +
        field("lastName", t.lastName, "text", "", 'autocomplete="family-name" required') +
        "</div>" +
        field("personnummer", t.personnummer, "text", t.pnrHint,
          'inputmode="numeric" autocomplete="off" required placeholder="ÅÅÅÅMMDD-XXXX"') +
        '<div class="mb-bk__row">' +
        field("email", t.email, "email", "", 'autocomplete="email" required') +
        field("phone", t.phone, "tel", t.phoneHint, 'autocomplete="tel" required') +
        "</div>" +
        '<div><button type="submit" class="mb-bk__btn">' + t.submit + "</button></div>" +
        '<p class="mb-bk__note">' + t.integrity + "</p>" +
        "</form>"
      );
      root.querySelector("[data-back]").addEventListener("click", renderTimes);
      root.querySelector("form").addEventListener("submit", submit);
    }

    function showErrors(fields) {
      root.querySelectorAll("[data-err]").forEach(function (p) { p.textContent = ""; });
      root.querySelectorAll(".mb-bk__field input").forEach(function (i) {
        i.setAttribute("aria-invalid", "false");
      });
      var first = null;
      Object.keys(fields || {}).forEach(function (k) {
        var p = root.querySelector('[data-err="' + k + '"]');
        var i = root.querySelector("#mb-" + k);
        if (p) p.textContent = fields[k];
        if (i) { i.setAttribute("aria-invalid", "true"); first = first || i; }
      });
      if (first) first.focus();
    }

    function submit(ev) {
      ev.preventDefault();
      var f = ev.target;
      var v = {};
      ["firstName", "lastName", "personnummer", "email", "phone"].forEach(function (k) {
        v[k] = (f.elements[k].value || "").trim();
      });

      var local = {};
      ["firstName", "lastName", "email", "phone"].forEach(function (k) {
        if (!v[k]) local[k] = t.required;
      });
      if (!v.personnummer) local.personnummer = t.required;
      else if (!pnrValid(v.personnummer)) local.personnummer = T[lang()].pnrHint;
      if (Object.keys(local).length) { showErrors(local); return; }
      showErrors({});

      var btn = f.querySelector("button[type=submit]");
      btn.disabled = true;
      btn.textContent = t.submitting;

      fetch(API + "/api/booking/create", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          firstName: v.firstName, lastName: v.lastName, personnummer: v.personnummer,
          email: v.email, phone: v.phone,
          startsAtUtc: state.chosen.startsAtUtc,
          appointmentTypeId: state.type && state.type.id,
          // Whoever owns the slot that was clicked. With "Först ledig" the
          // patient never named a doctor, so the page has no single answer —
          // only the slot does. The server re-checks it against its own
          // allow-list regardless.
          practitionerId: (state.chosen && state.chosen.practitionerId) || state.practitionerId,
          service: slug || undefined,
          pagePath: location.pathname,
        }),
      })
        .then(function (r) { return r.json().then(function (d) { return { s: r.status, d: d }; }); })
        .then(function (res) {
          btn.disabled = false;
          btn.textContent = t.submit;
          if (res.d && res.d.ok) return confirmed(res.d);
          var code = res.d && res.d.code;
          if (code === "VALIDATION") return showErrors(res.d.fields);
          if (code === "SLOT_TAKEN") { alertTop(t.taken); return load(); }
          if (code === "RATE_LIMITED") return alertTop(t.rateLimited);
          alertTop(t.upstream);
        })
        .catch(function () {
          btn.disabled = false;
          btn.textContent = t.submit;
          alertTop(t.upstream);
        });
    }

    function alertTop(msg) {
      var old = root.querySelector(".mb-bk__alert");
      if (old) old.remove();
      var d = document.createElement("div");
      d.className = "mb-bk__alert";
      d.setAttribute("role", "alert");
      d.textContent = msg;
      root.insertBefore(d, root.firstChild);
      root.scrollIntoView({ behavior: "smooth", block: "nearest" });
    }

    function confirmed(d) {
      var msg =
        d.confirmationChannel === "both" ? t.confirmedBoth :
        d.confirmationChannel === "email" ? t.confirmedEmail :
        d.confirmationChannel === "sms" ? t.confirmedSms : t.confirmedNone;
      set(
        '<div class="mb-bk__ok"><h3>' + t.confirmedTitle + "</h3>" +
        '<p class="mb-bk__when">' + esc(d.startsAtLabel || d.startsAtLocal || "") + "</p>" +
        ((state.chosen && state.chosen.practitionerName)
          ? '<p class="mb-bk__meta" style="margin:0 0 .8rem">' + esc(t.withWhom) + ": " +
            esc(state.chosen.practitionerName) + "</p>" : "") +
        "<p>" + msg + "</p></div>"
      );
      root.scrollIntoView({ behavior: "smooth", block: "center" });
      if (typeof window.gtag === "function") {
        window.gtag("event", "booking_confirmed", { service: slug || "konsultation" });
      }
    }

    load();
  }

  /**
   * Stop the site chat widget opening itself on top of the booking form.
   *
   * The widget is inlined into all 111 pages and schedules `setTimeout(show,
   * 2000)` on load. Everywhere else that is a friendly nudge; on a booking page
   * it drops a fixed 380×560 panel over the bottom-right of the viewport, which
   * is where the calendar and the submit button live. A patient who came to
   * book has to dismiss a chat window first, and some will simply leave.
   *
   * The bubble stays — anyone who wants Mario can still open him, and on this
   * page he is genuinely useful. Only the automatic opening is suppressed.
   *
   * Done from here rather than by editing 111 files, and it has to be after the
   * fact: the widget is inline and evaluates its condition before this deferred
   * script runs, so the timer is already scheduled by the time we get control.
   * Setting the widget's own session key stops it coming back.
   */
  function suppressChatAutoOpen() {
    try {
      sessionStorage.setItem("__mbClosed", "1");
    } catch (e) { /* private browsing — fall through to the close below */ }

    var tries = 0;
    var timer = setInterval(function () {
      var panel = document.getElementById("__mb_panel");
      if (panel && panel.classList.contains("mbopen")) {
        var close = document.getElementById("__mb_close");
        if (close) close.click();
        clearInterval(timer);
      }
      // The widget opens at 2s; stop watching a little after that.
      if (++tries > 30) clearInterval(timer);
    }, 100);
  }

  function init() {
    var nodes = document.querySelectorAll("[data-mb-booking]");
    if (!nodes.length) return;
    injectStyles();
    suppressChatAutoOpen();
    nodes.forEach(function (n) { Booking(n); });
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", init);
  } else {
    init();
  }
})();
