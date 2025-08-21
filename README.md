# India Music Insights / Indie Melody Pulse

A full-stack music analytics platform. Backend ingests and serves Top 50 playlist insights; frontend visualizes live charts, KPIs, genres, top artists, and cross-market comparisons.

This README is your single, authoritative reference. It explains the project hierarchy folder-by-folder and file-by-file, the data flow, and how to run and extend it.

## Table of contents
- High-level architecture
- Backend hierarchy and roles
- Frontend hierarchy and roles
- Data flow and contracts
- Environment variables (backend + frontend)
- Run locally (Windows friendly)
- API matrix (endpoints at a glance)
- Diagrams (ERD + request flow)
- Extend and maintain
- Troubleshooting
- Author

## High-level architecture
- Backend (FastAPI + SQLAlchemy + SQLite)
  - Normalized schema: Tracks, Artists, Playlists, PlaylistTrackSnapshots, and yearly rollups.
  - Endpoints: today’s chart, yearly stats, analytics (overview, top artists, genres), compare across markets, and historical Spotify search.
- Frontend (Vite + React + TypeScript + Tailwind + shadcn)
  - Pages: Overview, Compare. Components for tables, cards, footer, audio preview.
  - Single API client matches backend contracts.

## Backend hierarchy and roles
Path: `india-music-insights/`

- `app/main.py`
  - FastAPI app factory: middleware (CORS, request context), router registration, global exception handler, and lifespan hooks (DB init/close, optional scheduler).
  - Exposes docs at `/docs`, health at `/v1/health` via `routers/health.py`.

- `app/config.py`
  - Settings (app name, version, host/port, debug flags, CORS, markets). Used by `main.py` to configure runtime.

- `app/db.py`
  - SQLAlchemy engine/session setup, `init_db()` to create tables, `close_db()` for teardown.

- `app/deps.py`
  - FastAPI dependencies: `get_database()` (Session), Spotify client provider, market/year/limit validators, admin key checker.

- `app/routers/health.py`
  - `/v1/health` basic service health.

- `app/routers/charts.py` (core API)
  - `/v1/charts/top-today` Today’s chart by market: joins latest `PlaylistTrackSnapshot` → `Track` and `Artist` to return ordered `ChartTrack` objects.
  - `/v1/charts/top-year` Yearly aggregated stats (uses `YearlyTrackStats`).
  - `/v1/search/tracks/year/{year}` and `/v1/search/tracks/year-range/{start}-{end}` Historical Spotify queries for exploration.
  - `/v1/search/top-of-year/{year}` Finds top tracks by popularity for a year via multiple searches.
  - Analytics:
    - `/v1/analytics/overview` Counts and basic growth proxies (tracks, artists, snapshots, last updated).
    - `/v1/analytics/top-artists` Artists ranked by track count.
    - `/v1/analytics/genres` Approximate genre distribution from current catalog.
    - `/v1/analytics/compare-genres` Cross-market genre-bucket counts using latest snapshots.
  - Helpers: `_format_duration()`.

- `app/models/` (ORM)
  - `base.py` Declarative base and shared columns (id, created_at, updated_at) via `BaseModel`.
  - `track.py`
    - `Artist`: spotify_id, name, popularity, followers, genres_json, image_url, external_url; relation `tracks`.
    - `Track`: spotify_id, name, album, album_release_date, explicit, popularity, preview/external URLs, audio features; relations `artists`, `playlist_snapshots`.
    - `Playlist`: spotify_id, name, market, image/external URLs; relation `snapshots`.
    - `PlaylistTrackSnapshot`: playlist_id, track_id, snapshot_date, rank, fetched_at, added_at; unique + index constraints.
    - `track_artists` association table for many-to-many.
  - `aggregates.py`, `yearly_*` (if present): yearly rollups for tracks/artists/genres.

- `app/services/ingest.py`
  - `IngestionService.ingest_top_playlist(market)` fetches Top 50, upserts artists and tracks, links via `track_artists`, creates playlist if missing, and inserts `PlaylistTrackSnapshot` with ranks.
  - Used by the scheduler when enabled; can also be called from an internal script for one-off backfills.

- `app/clients/spotify.py`
  - Auth + minimal Spotify API wrappers used by search/ingest flows.

- `app/utils/`
  - `logging.py` structured logging + request context middleware + request logger helper.
  - `caching.py` simple async cache facade.
  - `time.py` helpers like `today_in_timezone`.

- Other
  - `requirements.txt` backend dependencies.
  - `docker-compose.yml`, `Dockerfile` (optional containerization).
  - `create_tables.py` quick DB init scripts.

## Frontend hierarchy and roles
Path: `frontend/indie-melody-pulse-89/`

- Root build/config
  - `package.json` scripts and dependencies.
  - `vite.config.ts` dev server/build config.
  - `tsconfig*.json` TypeScript configs (base/app/node environments).
  - `tailwind.config.ts`, `postcss.config.js`, `eslint.config.js` style and linting.
  - `components.json` (shadcn) generated component registry.

- Public assets (served at `/`)
  - `public/favicon.ico` legacy favicon.
  - `public/favicon.svg` modern scalable icon (primary).
  - `public/safari-pinned-tab.svg` pinned tab mask icon.
  - `public/site.webmanifest` PWA manifest.
  - `public/robots.txt` crawl rules + sitemap reference.
  - `public/sitemap.xml` search engine sitemap.

- HTML entry
  - `index.html` SEO meta (canonical, OG/Twitter cards, JSON-LD), icons/manifest links, root container.

- App entry
  - `src/main.tsx` React root, Tailwind/global CSS import, router/app mount.
  - `src/App.tsx` High-level app shell and route composition (if used).

- Pages
  - `src/pages/Overview.tsx` Dashboard:
    - Fetches: `/v1/charts/top-today`, `/v1/analytics/overview`, `/v1/analytics/genres`, `/v1/analytics/top-artists`.
    - Renders KPIs (real), genre distribution (real), top artists (real), and Top 50 table (real).
  - `src/pages/Compare.tsx` Market comparison:
    - Fetches `/v1/analytics/compare-genres?markets=...`.
    - Renders a multi-series genre-bucket bar chart by market with insights.

- Components
  - `src/components/TrackTable.tsx` Ranked track table (uses ChartTrack shape).
  - `src/components/KPICard.tsx` KPI card with trend indicators.
  - `src/components/Layout.tsx`, `Footer.tsx` App scaffolding.
  - `src/components/AudioPreview.tsx` Preview audio control when `preview_url` exists.
  - `src/components/ui/*` shadcn UI primitives.

- API and utilities
  - `src/lib/apiClient.ts`
    - Central axios client with `VITE_API_BASE_URL`.
    - Types aligned to backend responses (ChartTrack, TodayChartResponse, analytics payloads).
    - Functions: `getTopToday`, `getAnalyticsOverview`, `getTopArtistsByTracks`, `getGenreDistribution`, `compareGenres`, historical searches.
  - `src/lib/utils.ts` small helpers.
  - `src/hooks/use-toast.ts`, `src/hooks/use-mobile.ts` UI hooks.

- Styles
  - `src/index.css`, `src/App.css` Tailwind layers and app styles.

## Data flow and contracts
- Ingestion (server-side) writes normalized entities and daily `PlaylistTrackSnapshot` ranks.
- Today chart endpoint returns latest snapshot per market as a list of `ChartTrack` items:
  - `{ rank, track_name, artists: string[], album, release_date, popularity, explicit, preview_url, spotify_url, duration_formatted }`
- Frontend consumes these directly in tables and charts, avoiding Spotify’s raw shape.
- Analytics endpoints return counts/aggregations used to drive KPIs, genre/artist widgets, and comparisons.

## Environment variables

Backend (.env in `india-music-insights/`)

- SPOTIFY_CLIENT_ID: required. Any non-empty string lets the server boot; real value needed when calling Spotify-backed endpoints.
- SPOTIFY_CLIENT_SECRET: required.
- DATABASE_URL: required. Example: `sqlite:///./india_music_insights.db`.
- ADMIN_KEY: required. Arbitrary string for privileged ops (future/admin tooling).
- MARKETS: optional, default `IN,US,GB`.
- INDIA_TOP50_PLAYLIST_ID: optional, default Spotify ID for India Top 50.
- GLOBAL_TOP50_PLAYLIST_ID: optional, default Spotify Global Top 50.
- TIMEZONE: optional, default `Asia/Kolkata`.
- ENABLE_SCHEDULER: optional, default `True`. Set `False` for local dev to avoid scheduled jobs.

Frontend (.env.local in `frontend/indie-melody-pulse-89/`)

- VITE_API_BASE_URL: base API URL. Example: `http://127.0.0.1:8001`.

## Run locally (Windows friendly)
Backend (Python 3.9+)
- From `india-music-insights/`:
  1) Copy `.env.sample` to `.env` and fill required values. Minimum viable local dev:
    - `SPOTIFY_CLIENT_ID=dev`
    - `SPOTIFY_CLIENT_SECRET=dev`
    - `DATABASE_URL=sqlite:///./india_music_insights.db`
    - `ADMIN_KEY=dev-admin`
  2) Start the API without inline env (avoids PowerShell pitfalls):
    - `python -m uvicorn app.main:app --host 127.0.0.1 --port 8001`

Frontend (Node 18+)
- From `frontend/indie-melody-pulse-89/`:
  - `npm install`
  - `npm run dev`
- If needed, create `.env.local` with `VITE_API_BASE_URL=http://127.0.0.1:8001`.

## Extend and maintain
- Add markets: ensure playlists exist, run ingestion, endpoints will pick latest snapshots.
- Enhance genres: replace heuristic buckets with real per-track genres once available; extend `models` + ingestion accordingly.
- Add overlap analytics: implement endpoints for artist/track intersection across markets and wire new UI cards.

## API matrix (at a glance)

- GET `/v1/health` — service health.
- GET `/` — root info (name, version, markets).
- GET `/v1/charts/top-today?market=IN` — latest Top 50 snapshot for a market.
- GET `/v1/charts/top-year?market=IN&year=2025` — yearly aggregates.
- GET `/v1/analytics/overview` — KPI counts + last_updated.
- GET `/v1/analytics/top-artists?limit=10` — artists by track presence.
- GET `/v1/analytics/genres?market=IN` — genre-bucket distribution.
- GET `/v1/analytics/compare-genres?markets=IN&markets=US` — cross-market genre buckets.
- Historical search (Spotify-powered):
  - GET `/v1/search/tracks/year/{year}`
  - GET `/v1/search/tracks/year-range/{start}-{end}`
  - GET `/v1/search/top-of-year/{year}`

Response (example, top-today item):

```json
{
  "rank": 1,
  "track_name": "Heeriye",
  "artists": ["Jasleen Royal", "Arijit Singh"],
  "album": "Heeriye",
  "release_date": "2023-07-05",
  "popularity": 86,
  "explicit": false,
  "preview_url": null,
  "spotify_url": "https://open.spotify.com/track/...",
  "duration_formatted": "3:12"
}
```

## Diagrams

Entity-relationship (simplified)

```mermaid
erDiagram
    ARTIST {
      int id PK
      string spotify_id
      string name
    }
    TRACK {
      int id PK
      string spotify_id
      string name
      string album
      date album_release_date
      bool explicit
      int popularity
    }
    PLAYLIST {
      int id PK
      string spotify_id
      string name
      string market
    }
    PLAYLISTTRACKSNAPSHOT {
      int id PK
      int playlist_id FK
      int track_id FK
      date snapshot_date
      int rank
    }
    ARTIST ||--o{ TRACK : "appears_on via track_artists"
    TRACK }o--o{ ARTIST : "many-to-many"
    PLAYLIST ||--o{ PLAYLISTTRACKSNAPSHOT : has
    TRACK ||--o{ PLAYLISTTRACKSNAPSHOT : ranked
```

Request flow (Overview page)

```mermaid
sequenceDiagram
    participant UI as React (Overview)
    participant API as FastAPI (charts/analytics)
    participant DB as SQLite
    UI->>API: GET /v1/charts/top-today?market=IN
    API->>DB: Query latest PlaylistTrackSnapshot join Track/Artist
    DB-->>API: Rows
    API-->>UI: ChartTrack[]
    UI->>API: GET /v1/analytics/overview
    API->>DB: Counts/last_updated
    DB-->>API: Aggregates
    API-->>UI: KPIs
```

## Troubleshooting
- No tracks in UI: ensure DB has snapshots for your market (look at `playlist_track_snapshots`).
- Cross-origin errors: confirm CORS settings in `app/main.py` and `app/config.py`.
- PowerShell env: prefer `.env.local` for `VITE_API_BASE_URL` over inline env assignment.
 - Backend won’t start (pydantic ValidationError): create `india-music-insights/.env` (see `.env.sample`) and provide required keys.
 - Uvicorn reload loop or exit code 1 on Windows: avoid inline `$env:VAR=...` chains; start with an `.env` file and a clean command.
 - Port already in use: change `--port` or terminate the existing process.
 - SQLite locked: stop the API, delete temporary `*.db-shm/*.db-wal` files, then restart.

## Author

**Vishesh Sanghvi**

🌐 **Website:** [visheshsanghvi.me](https://www.visheshsanghvi.me/)  
💼 **LinkedIn:** [vishesh-sanghvi](https://www.linkedin.com/in/vishesh-sanghvi-96b16a237/)  
🐙 **GitHub:** [@visheshsanghvi112](https://github.com/visheshsanghvi112)

Full-stack developer passionate about music analytics and data visualization. This project combines modern web technologies with real-time music data to create insightful analytics dashboards.

---

*Built with ❤️ using FastAPI, React, TypeScript, and the Spotify Web API*

