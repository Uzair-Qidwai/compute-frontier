# Project handoff

- **Name:** Compute Frontier
- **Creator credit:** Uzair Qidwai & ChatGPT
- **Release snapshot:** September 28, 2026
- **Stack:** plain HTML, CSS and JavaScript; static JSON and PNG assets
- **Entry point:** `dist/index.html`
- **Local command:** `python3 -m http.server 8000 --directory dist`
- **Build:** none
- **Secrets / environment variables:** none required

## Current implementation

The basemap image is rectangular geographic projection with matching longitude/latitude bounds in JavaScript. Marker coordinates are approximations. The two curated-entry charts can filter the map; the published capacity charts remain independent of those filters. Theme colors use CSS variables. New chart interactions should support hover, tap and keyboard focus.

## Research provenance

Each published series is documented in `dist/market-context.json`. The forecast values are 88, 100 and 112 GW for 2027, 2028 and 2029 respectively, transcribed from Rystad Energy's chart on printed page 14. The PDF was visually checked on September 28, 2026. Only these published values were used; no annual interpolation was performed. Report text and chart images are not bundled.

The historical supply series uses each annual CBRE report as published. Market coverage changed across years. The country pie is a separate RaboResearch estimate. The register retains record-specific uncertainty and source-quality labels.

## Known limitations / follow-up work

- Complete row-level verification of supplied project claims.
- Replace annual snapshots when new comparable research is available, preserving prior vintages.
- The basemap view covers the selected continental markets, not all geographic North America.
- Counts and takeaway prose in HTML need manual review after a data update.
- The source and geometry checks do not replace browser visual testing.
- This environment could not run full browser QA for the latest changes. The user confirmed the preceding dashboard looked good in their browser.

## Repository handoff

Repository: https://github.com/Uzair-Qidwai/compute-frontier

The connected GitHub account is `Uzair-Qidwai`.

This release is imported directly onto `main` as requested by the project owner. Avoid changing the current Site's remote or publishing credentials. A repository archive is a portable source snapshot, not an automatic synchronization link to Sites.
