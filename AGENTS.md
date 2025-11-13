# Repository Guidelines

## Project Structure & Module Organization
Presentations live in top-level folders such as `mi-presentacion/`, `equipazgo/`, `refactoring-cultural/`, and `remotework/`; each holds `contenidos.md`, an optional `images/` subfolder, and generated artifacts (`index.html`, `notas.html`). The entry point `presentacion.html` renders any presentation via the `?presentacion=` query parameter, while `index.html` lists the available decks and enables local folder uploads. Python utilities (`generate.py`, `server.py`, `server_dev.py`, `generate-notes.py`, `clean-standalone.py`) orchestrate generation, serving, and standalone exports; `reveal.js/` carries vendored assets that should not be edited manually.

## Build, Test, and Development Commands
- `./startdev.sh`: regenerates `index.html` and runs the dev server with no-cache headers at `http://localhost:8000`.
- `./start.sh`: rebuilds the listing and starts `server.py`, which auto-selects a free port between 3000-3010.
- `python3 generate.py`: refreshes `index.html`; run it after adding or renaming presentation folders.
- `./build.sh <deck>`: produces a Chrome-rendered standalone HTML in `<deck>/index.html`; requires `google-chrome` in PATH.
- `./generate-notes.sh <deck>`: emits `<deck>/notas.html` cards and reports parsing results.

## Cloud Features & Remote Control
- Copy `firebase-config.example.js` to `firebase-config.js` and paste the Firebase Web SDK configuration (Auth + Firestore enabled). Without it, cloud save and remote control silently stay disabled under a local-only mode.
- Auth uses Google sign-in (`firebase-auth`) with session persistence; bind additional providers in `js/firebaseService.js` if needed.
- Presenting while logged in lets you save the loaded deck to Firestore (`users/{uid}/presentations/{doc}`) and activate remote control. The first authenticated device to start a session becomes “master”; all other viewers fall back to slave mode with Reveal.js controls hidden.
- Remote sync persists the slide indices under `sessions/{sessionKey}`. Clearing the session (release control or leaving the page) removes the document; if a master crashes, a new login can reclaim control via the HUD button.

## Coding Style & Naming Conventions
Prefer PEP 8 style for Python (4-space indents, snake_case helpers) while matching any intentional local deviations in legacy files. Shell scripts follow `bash` with lowercase, hyphenated filenames and executable bit set. Presentation content stays in Markdown with Spanish headings, slide markers (`<!-- SLIDE -->`, `<!-- NOTES -->`), and WebP imagery housed under each deck’s `images/` folder.

## Testing Guidelines
There is no automated test suite. Validate changes by loading `http://localhost:8000/presentacion.html?presentacion=<deck>` (dev) or the standalone file produced by `./build.sh`. For content work, click through vertical and horizontal slides, check speaker notes, and ensure assets resolve. Run `./generate-notes.sh` on updated decks to confirm note extraction.

## Commit & Pull Request Guidelines
Git history favors concise Conventional Commit prefixes (`feat:`, `fix:`, `add:`) with imperative subjects (e.g., `fix: improve standalone HTML generation`). Group related edits per commit and keep subject lines ≈50 characters. Pull requests should outline the motivation, highlight impacted decks or scripts, note manual validation steps, and attach screenshots or printable-note previews whenever slides change. Reference issue IDs or meeting links when applicable.
