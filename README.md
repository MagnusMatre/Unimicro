# Unimicro Task Manager API

Et enkelt REST-API for å administrere oppgaver, bygget med  **FastAPI** ,  **SQLAlchemy** , og  **PostgreSQL/SQLite** . Støtter opprettelse, oppdatering, sletting og søk på oppgaver med tags, fullført-status og forfallsdato.

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

---

## CLI-grensesnitt

* `cli.py` gir enkel interaktiv terminal for å opprette, oppdatere og slette oppgaver
* Forfallsdatoer legges inn som `YYYY-MM-DD HH:MM` og lagres i ISO-format
