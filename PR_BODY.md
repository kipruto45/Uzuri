Title: feat(ui): apply PageShell/Card primitives + clearance page polish

Summary
- Applied design-system primitives (`PageShell`, `Card`, `CardContent`) across several high-impact pages (Dashboard, Attachments, Clearance, Calendar, AiSupport, Accessibility) to standardize layout and header/top actions.
- Cleaned and restored the Clearance page (`src/modules/clearance/ClearancePage.jsx`) after a corrupted commit; preserved upload/list/preview and metadata editing flows.
- Temporarily re-enabled a test shim in `src/setupTests.js` to map deprecated test-utils `act` usage to `React.act` and reduce CI noise.
- Fixed duplicate heading issues and aligned page titles so unit tests pass.

Files of note
- src/components/ui/PageShell.jsx
- src/components/ui/Card.jsx, CardContent
- src/modules/clearance/ClearancePage.jsx
- src/setupTests.js
- frontend/scripts/screenshot.js (helper for capturing screenshots locally)

Testing
- Ran full Jest suite locally: all unit tests pass.
- Prettier check run: many style issues detected across the repo (I did not auto-format).

Screenshots
- I attempted to capture desktop and mobile screenshots automatically, but the dev server encountered a couple of dev-time module resolution issues in this environment. A helper script is included at `frontend/scripts/screenshot.js` to capture screenshots locally once the dev server runs.
- To run locally:
  1. Start dev server from `frontend` folder: `npm run dev --prefix C:\\Uzuri\\frontend` (Vite will print the local URL).
  2. Run the screenshot script from `frontend` folder: `node scripts/screenshot.js`. The script tries ports 5173 and 5174 and writes images to `frontend/screenshots/`.

Test shim note
- The test shim in `src/setupTests.js` is temporary. Please remove it after upgrading testing dependencies or after addressing imports that use `act` from `react-dom/test-utils`.

Follow-ups / TODOs
- Remove temporary test shim after dependency upgrades.
- Confirm pdf.js worker bundling for production (worker path may need explicit configuration).
- Optionally run `npx prettier --write .` to apply consistent formatting before merging.

Reviewer guidance
- Run `npm ci` in `frontend` and `npm run test` to verify locally.
- The branch is `feature/clearance-enhancements`. Target branch: `ci-frontend-tests`.

Screenshots placeholders
- If CI or reviewer needs, attach `frontend/screenshots/*` after running the helper locally.

— end of PR body
