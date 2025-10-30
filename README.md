# Unimicro Task Manager API

Et enkelt REST-API for å administrere oppgaver, bygget med  **FastAPI** ,  **SQLAlchemy** , og  **PostgreSQL/SQLite** . Støtter opprettelse, oppdatering, sletting og søk på oppgaver med tags, fullført-status og forfallsdato.

### Start hele systemet med runner-scriptet

Scriptet kjører docker-compose, og setter opp backend og GUI

<pre class="overflow-visible!" data-start="648" data-end="676"><div class="contain-inline-size rounded-2xl relative bg-token-sidebar-surface-primary"><div class="sticky top-9"><div class="absolute end-0 bottom-0 flex h-9 items-center pe-2"><div class="bg-token-bg-elevated-secondary text-token-text-secondary flex items-center gap-4 rounded-sm px-2 font-sans text-xs"></div></div></div><div class="overflow-y-auto p-4" dir="ltr"><code class="whitespace-pre! language-bash"><span><span>python runner.py</span></span></code></div></div></pre>

## Funksjoner

* RESTful API med følgende endepunkter:

  * `GET /tasks` — Hent liste over oppgaver, med valgfrie filter `query` (title/tags) og `completed`
  * `POST /tasks` — Opprett en oppgave med server-satte standardverdier (`id`, `created_at`, `completed=false`)
  * `PUT /tasks/{id}` — Partiell oppdatering av oppgave (title, tags, completed, due_date)
  * `DELETE /tasks/{id}` — Slett oppgave (returnerer 204 ved suksess)
* Pydantic-modeller for input-validering
* Automatisk håndtering av feil: 400, 404, 422, 500
* Enhetstester for CRUD-operasjoner

## Krav

pip install -r requirements.txt

## Endepunkter

### GET `/tasks`

Query-parametre:

* `query` (valgfritt) — søk på title eller tags
* `completed` (valgfritt, boolean) — filter på fullført-status

Eksempelrespons:

<pre class="overflow-visible!" data-start="304" data-end="525"><div class="contain-inline-size rounded-2xl relative bg-token-sidebar-surface-primary"><div class="sticky top-9"><div class="absolute end-0 bottom-0 flex h-9 items-center pe-2"><div class="bg-token-bg-elevated-secondary text-token-text-secondary flex items-center gap-4 rounded-sm px-2 font-sans text-xs"></div></div></div><div class="overflow-y-auto p-4" dir="ltr"><code class="whitespace-pre! language-json"><span><span>{</span><span>
  </span><span>"id"</span><span>:</span><span></span><span>1</span><span>,</span><span>
  </span><span>"title"</span><span>:</span><span></span><span>"Fullfør rapport"</span><span>,</span><span>
  </span><span>"tags"</span><span>:</span><span></span><span>[</span><span>"jobb"</span><span>,</span><span></span><span>"haste"</span><span>]</span><span>,</span><span>
  </span><span>"completed"</span><span>:</span><span></span><span>false</span><span></span><span>,</span><span>
  </span><span>"due_date"</span><span>:</span><span></span><span>"2025-11-01T15:30:00"</span><span>,</span><span>
  </span><span>"created_at"</span><span>:</span><span></span><span>"2025-10-27T14:50:00"</span><span>,</span><span>
  </span><span>"updated_at"</span><span>:</span><span></span><span>"2025-10-27T14:50:00"</span><span>
</span><span>}</span><span>
</span></span></code></div></div></pre>

* `created_at` — tidspunkt da oppgaven ble opprettet
* `updated_at` — tidspunkt for siste oppdatering av oppgaven

---

### POST `/tasks`

Body:

<pre class="overflow-visible!" data-start="2531" data-end="2641"><div class="contain-inline-size rounded-2xl relative bg-token-sidebar-surface-primary"><div class="sticky top-9"><div class="absolute end-0 bottom-0 flex h-9 items-center pe-2"><div class="bg-token-bg-elevated-secondary text-token-text-secondary flex items-center gap-4 rounded-sm px-2 font-sans text-xs"></div></div></div><div class="overflow-y-auto p-4" dir="ltr"><code class="whitespace-pre! language-json"><span><span>{</span><span>
  </span><span>"title"</span><span>:</span><span></span><span>"Fullfør rapport"</span><span>,</span><span>
  </span><span>"tags"</span><span>:</span><span></span><span>[</span><span>"jobb"</span><span>,</span><span></span><span>"haste"</span><span>]</span><span>,</span><span>
  </span><span>"due_date"</span><span>:</span><span></span><span>"2025-11-01T15:30:00"</span><span>
</span><span>}</span><span>
</span></span></code></div></div></pre>

* `completed` settes til `false` som standard
* `created_at` settes av serveren

---

### PUT `/tasks/{id}`

Body (partiell oppdatering):

<pre class="overflow-visible!" data-start="2784" data-end="2851"><div class="contain-inline-size rounded-2xl relative bg-token-sidebar-surface-primary"><div class="sticky top-9"><div class="absolute end-0 bottom-0 flex h-9 items-center pe-2"><div class="bg-token-bg-elevated-secondary text-token-text-secondary flex items-center gap-4 rounded-sm px-2 font-sans text-xs"></div></div></div><div class="overflow-y-auto p-4" dir="ltr"><code class="whitespace-pre! language-json"><span><span>{</span><span>
  </span><span>"title"</span><span>:</span><span></span><span>"Oppdatert oppgave"</span><span>,</span><span>
  </span><span>"completed"</span><span>:</span><span></span><span>true</span><span>
</span><span>}</span><span>
</span></span></code></div></div></pre>

* Returnerer 404 hvis oppgaven ikke finnes
* `updated_at` — tidspunkt for siste oppdatering av oppgaven

---

### DELETE `/tasks/{id}`

* Returnerer 204 ved suksess
* Returnerer 404 hvis oppgaven ikke finnes

# 🗂️ Unimicro Task Manager (Python GUI)

En enkel og effektiv desktop‑oppgavebehandler bygget med  **Python og Tkinter**

Programmet lar deg legge til, redigere, slette og se oppgaver. Alle API kall blir gjort async for å forhindre utsettelser

---

## 🚀 Funksjonalitet

### ✅ Kjernefunksjoner

* **Legg til nye oppgaver** via en modal dialog med:
  * Title
  * Tags (komma-separert)
  * Due Date (kalender‑velger)
  * Time (HH:MM)
* **Rediger eksisterende oppgaver** i en tilsvarende modal
* **Slett oppgaver** med bekreftelsesdialog
* **Merk oppgaver som fullført** ved dobbelklikk
* **Sorter oppgaver** ved å klikke på kolonneoverskrifter
* **Høyreklikk‑meny** for raske handlinger:
  * View full details
  * Edit
  * Delete


## 🧱 Datamodell

Hver oppgave har følgende felt:

| Felt                 | Type     | Beskrivelse                                        |
| -------------------- | -------- | -------------------------------------------------- |
| **id**         | Integer  | Unik identifikator                                 |
| **title**      | String   | Kort beskrivelse av oppgaven                       |
| **tags**       | String   | Komma-separerte nøkkelord                         |
| **completed**  | Boolean  | Om oppgaven er fullført                           |
| **due_date**   | DateTime | Når oppgaven skal være ferdig                    |
| **created_at** | DateTime | Når oppgaven ble opprettet                        |
| **updated_at** | DateTime | Når oppgaven sist ble oppdatert                   |
| **created_by** | String   | Brukernavnet til personen som opprettet oppgaven   |
| **updated_by** | String   | Brukernavnet til personen som sist endret oppgaven |

---

## 💻 GUI‑oversikt

### Hovedvindu

* Viser alle oppgaver i en sortérbar tabell
* Søkefelt
* Filtrering på fullført status
* Kolonner:  **Title** ,  **Tags** ,  **Due Date** , **Completed**
* Markering med rød bakgrunn vis over forfallsdato (markerer bakgrunnen så det er synlig for fargeblinde også)
* Knapper i header:
  * ➕ **Add Task**
  * ✏️ **Edit Task**
  * 🗑️ **Delete Task**

### Add/Edit Modal

* Ikke‑resizable popup‑vindu
* Inputfelt for:
  * Title
  * Tags
  * Due Date (kalenderwidget)
  * Time (manuell inntasting)
* Knapper:
  * 💾 **Save**
  * ❌ **Cancel**

### Task Details (Høyreklikk → View Details)

* Viser all informasjon om oppgaven:
  * Title, Tags, Completed
  * Due Date, Created At, Updated At, Created By, Updated By

### Login / Registrer Modal

En enkel modal for å enten logge inn eller å registrere deg

# Tester

Et par enkle CRUD tester, kjør test_crud.py

# Sikkerhet

### Brukerhåndtering og tilgangskontroll

I dette prosjektet er det implementert et enkelt brukersystem for å demonstrere grunnleggende autentisering og bruker-spesifikk datatilgang:

1. **Registrering og innlogging**

   * Brukere kan registrere seg med brukernavn og passord.
   * Passord lagres sikkert ved først å hashe med SHA-256 og deretter bcrypt.
   * Innlogging sjekker brukernavn og hashet passord mot databasen.
2. **Oppgave-eierskap**

   * Hver oppgave har feltene `created_by` og `updated_by` for å spore hvem som opprettet eller sist endret den.
   * Oppgaver hentes kun for brukeren som eier dem, slik at man kun ser egne oppgaver.
3. **Tilgangskontroll (grunnleggende)**

   * Selv om full tilgangskontroll ikke er implementert, sikrer API-et at brukere ikke kan endre eller slette oppgaver som tilhører andre.
   * Alle CRUD-operasjoner filtrerer oppgaver basert på `username`.


# Antakelser/avgrensninger

Systemet er utviklet som en forenklet demonstrasjon av et oppgavehåndteringssystem (ERP-lignende løsning) med støtte for flere brukere. Det antas at applikasjonen kjøres i et lukket miljø uten ondsinnede brukere. Brukerautentisering er implementert på et grunnleggende nivå med registrering og innlogging, men uten sesjonshåndtering eller token-basert autentisering. All filtrering og datatilgang baseres på brukernavn sendt fra klienten, og det forutsettes at dette håndteres korrekt. Målet har vært å fokusere på struktur, funksjonalitet og dataintegritet fremfor full sikkerhetsimplementering.

I den nåværende løsningen kan brukere hente alle oppgaver knyttet til et gitt brukernavn ved å sende et enkelt `GET`-kall til API-et, for eksempel `GET /tasks/<brukernavn>`. Dette innebærer at hvem som helst som kjenner et brukernavn, kan hente ut alle tilhørende oppgaver. Det er ingen reell tilgangskontroll implementert. I et produksjonsmiljø ville dette utgjort en alvorlig sikkerhetsrisiko.


# Fremtidige forbedringer

Implementere rollebasert tilgang for å skille mellom vanlige brukere, administratorer og andre roller. Innføre strengere rettigheter for å hindre uautorisert tilgang til andre brukeres oppgaver. For å forhindre innsyn til andres data burde autentisering og autorisering implementeres ved hjelp av **tokens** eller **session-basert innlogging.** Med, for eksempel, JWT-baset autentisering kan hver bruker få en signert token hved innloging som må sendes i alle kall.

En windows applikasjon er ikke det fineste, og kan få mer elegante løsninger ved bruk av webløsninger som React.

Måten jeg strukturerte API kallene kan bli forbedres f.eks @router.delete("/tasks/{username}/{task_id}", status_code=204) så trenger man ikke strengt tatt username, og som nevnt tidligere hadde jeg brukt JWT tokens så hadde det blitt en mye mer ryddig løsning på denne fronten.

# Bruk av hjelpemidler

ChatGPT og GitHub Copilot ble benyttet som støtteverktøy under utviklingen. De ble brukt til idéutvikling, forslag til funksjonsstruktur, og generering av deler av kildekoden, spesielt for GUI-komponenter og API-funksjonalitet. Og ble brukt til store deler av Readme-en
