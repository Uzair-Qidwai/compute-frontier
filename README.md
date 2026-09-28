# Compute Frontier

Created by **Uzair Qidwai & ChatGPT**.

*Mapping North America’s data center footprint and future.*

An interactive, responsive dashboard of selected North American data center markets and projects, with operating, construction and proposed stages, capacity disclosures, historical context and a three-year outlook.

[Live dashboard](https://north-america-data-center-atlas.qidwai978493.chatgpt.site/) · [LinkedIn](https://www.linkedin.com/in/uzair-qidwai/) · [GitHub repository](https://github.com/Uzair-Qidwai/compute-frontier)

The hosted dashboard may require access through its current sharing settings.

## Run locally

Requires Python 3. No JavaScript dependencies or API key are required.

1. Extract the project ZIP or clone your repository.
2. Open a terminal in the project folder.
3. Run:

```bash
python3 -m http.server 8000 --directory dist
```

4. Open `http://localhost:8000` in your browser.
5. Press `Ctrl+C` in the terminal to stop the server.

On Windows, use `py -m http.server 8000 --directory dist` if `python3` is unavailable. Serve the folder over HTTP: opening `index.html` directly can prevent the JSON files from loading.

VS Code users can open `compute-frontier.code-workspace`.

## Tech stack

Plain HTML5, CSS and browser JavaScript, with local JSON/CSV data and pre-rendered PNG maps. Python scripts prepare and validate records; optional Basemap dependencies regenerate the maps. There is no application build step or JavaScript package installation.

## Features

- Locally bundled, 3,840 × 2,400 geographic basemaps with interactive markers, clustering, pan and zoom.
- Filters for country, development stage, entry type and text search.
- Location details showing capacity or **Unknown**, measurement basis and source notes.
- Interactive development-stage and disclosure summaries.
- Country capacity donut and five year-end supply snapshots, 2021–2025.
- Separate North America capacity forecast for 2027–2029.
- Light/dark appearance with saved preference, responsive layout and keyboard support.
- Creator credit and social profile links.

## What the data means

This is a curated research snapshot, **not a facility census or a live feed**. The map contains 52 selected market/project entries, including 30 without a usable numeric capacity. Data is compiled from public sources; some supplied project claims still await primary-source verification. Check each record's source quality and qualification.

| View | Measure | Coverage / limitation |
| --- | --- | --- |
| Map and register | Selected markets and named projects | Approximate city/county coordinates; operating and future capacity bases differ |
| Stage and disclosure | Counts of selected entries | Not a count of all North American facilities |
| Country donut | Live IT capacity, GW | RaboResearch, published March 2026; rounded estimates for US, Canada and Mexico |
| Historical bars | Wholesale colocation supply, GW | CBRE US primary markets, year-end 2021–2025; changing market coverage and revisions |
| Forecast | Projected facility capacity, GW | Rystad Energy 2026 report, p. 14; North America, 2027–2029; includes project-delivery risk |

Do not sum the map capacities: market aggregates can include projects listed separately. Do not join the three published capacity charts into one time series: their definitions and geographic coverage differ. The historical chart is capacity growth, not facility-count growth. No constant-coverage historical growth rate is claimed. Forecast values are projections, not assured delivery dates or confidence intervals.

## Project layout

| Path | Purpose |
| --- | --- |
| `dist/index.html` | Page structure and explanatory text |
| `dist/style.css` | Layout, responsive rules and both themes |
| `dist/app.js` | Map, filters, chart rendering and interaction |
| `dist/data.json` | Dashboard-ready curated location records |
| `dist/market-context.json` | Published chart data, units, dates and source URLs |
| `dist/north-america-map*.png` | Bundled light and dark basemaps |
| `dist/source.csv`, `dist/sources.md` | Downloadable supplied source material |
| `data/` | Original CSV and research notes |
| `scripts/prepare_data.py` | Normalizes the source CSV and applies documented record corrections |
| `scripts/render_map.py` | Optional basemap regeneration |
| `scripts/validate.py` | Asset, JSON, record and secret-pattern checks |
| `PROJECT.md` | Maintenance and handoff details |
| `GITHUB_SETUP.md` | Repository setup and upload instructions |

## Update the data

1. Edit `data/source.csv` and supporting notes in `data/sources.md`.
2. Review the explicit corrections and source links in `scripts/prepare_data.py`.
3. Run `python3 scripts/prepare_data.py`.
4. Keep the downloadable CSV and source notes in `dist/` aligned with `data/`.
5. Update `dist/market-context.json` separately for the published chart series. Record source, units and vintage; do not silently replace a metric with a different one.
6. Review explanatory text and hard-coded counts/takeaways in `dist/index.html` whenever records or sources change.
7. Run the checks below, then inspect both themes at phone and desktop widths.

Unknown values must remain JSON `null`, not zero. Verify status, capacity basis and dates before promoting supplied claims to verified figures. For the current basemap extent, records must be inside longitude −129 to −62 and latitude 14 to 58; changing the map extent also requires changing `bounds` in `app.js`.

## Checks

```bash
python3 scripts/validate.py
node --check dist/app.js
```

Node.js is needed only for the optional syntax check. Browser review should cover a small phone, tablet and desktop; both themes; search/clear; marker selection; chart hover/tap; keyboard focus; sources drawer; and profile links.

## Optional map regeneration

The ready-to-use PNGs are included. To regenerate them in a Python virtual environment:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements-maps.txt
python scripts/render_map.py
python scripts/render_map.py --dark
```

On Windows, activate with `.venv\Scripts\activate`. Map regeneration dependencies are optional and unpinned; image output can vary by library version.

## Hosting and external services

Publish the contents of `dist/` on a static host. All application asset paths are relative. No database, backend, map tiles, CARTO key or paid API is needed. Fonts load from Google Fonts with system-font fallbacks. External source/profile links open in a new tab. Theme preference is stored only in the browser's local storage; there is no analytics code in this project.

The existing ChatGPT Site was updated as Compute Frontier on September 28, 2026, at the live dashboard URL above. Its owner-only access settings are preserved. The `.openai/hosting.json` file records the existing Sites binding; it contains no credentials. GitHub commits do not automatically deploy to Sites.

## Attribution and reuse

Geographic boundaries: GSHHG / GMT through Basemap. Published research and data retain their original authorship; source links and scope notes are included. No blanket open-source license has been selected for this project. Before adding a license, decide the intended code license and review third-party map/data terms separately.
