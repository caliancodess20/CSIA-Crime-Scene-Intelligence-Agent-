# CSIA Frontend

React + Tailwind UI for the Crime Scene Investigation Assistant. Built to run
standalone against mock data so you're never blocked waiting on a teammate's
backend — flip one flag per module as each one ships.

## Run it

```bash
npm install
npm run dev
```

Opens on http://localhost:5173.

## Wiring in real backend routes

Every backend call is isolated in `src/api/*.js`. Nothing else in the app
talks to axios directly — components only ever import from `src/api/`.

1. Open `src/api/client.js` and set `MOCK_MODE = false`.
2. Each file in `src/api/` (`cases.js`, `evidence.js`, `timeline.js`, `nlp.js`,
   `search.js`, `report.js`) has a `if (MOCK_MODE) { ... }` branch and a real
   `apiClient` call below it. Confirm the real path/payload shape against
   whatever the teammate's `routes.py` actually implements, and adjust that
   one function — the component using it doesn't need to change.
3. `vite.config.js` proxies `/api` to `http://localhost:8000` — update the
   `target` if the FastAPI backend runs elsewhere (e.g. via docker-compose).

Mapping of file → owner, so you know who to check the contract with:

| api file        | owns it   | module                    |
|------------------|-----------|---------------------------|
| `cases.js`       | Yojit     | case_management           |
| `search.js`      | Yojit     | case_management/search.py |
| `evidence.js`    | Tanya     | evidence_upload           |
| `report.js`      | Tanya     | report_generator          |
| `timeline.js`    | Sanskruti | timeline_suggestions      |
| `nlp.js`         | Anmol     | nlp_engine                |
| `imageAnalysis.js` | Anwesha | image_analysis           |

`imageAnalysis.js` is now wired to Anwesha's real, confirmed `app.py`
(`POST /analyze-evidence/`) — uploading an image in the Evidence tab
automatically runs it through detection + OCR and shows the results inline.

## Known integration risks (worth raising with the team)

- **Anwesha's image_analysis service runs standalone.** Her `app.py` calls
  `uvicorn.run()` itself instead of being mounted into `main.py` like the
  other modules — so it's a separate process on its own port. The frontend
  proxies `/image-api` to `localhost:8001` as a placeholder; confirm the
  real port with her and update `vite.config.js`.
- **Stack mismatch:** Sanskruti's `timeline_suggestions` uses Flask
  (`Blueprint`), while `main.py` (and Anwesha's service) use FastAPI. Both
  can run as separate processes so this isn't blocking, but it means there's
  no single `docker-compose` entrypoint yet — someone needs to decide how
  these get deployed together.
- **`evidence_upload/routes.py` and `report_generator/routes.py` haven't
  been shared yet** — only `storage.py`, `format_spec.py`, and
  `report_builder.py` have. `api/evidence.js` and `api/report.js` are
  wired to the schema those files imply, but the actual endpoint paths in
  `routes.py` still need confirming when Tanya sends them.

## Structure
