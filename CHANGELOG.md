## v-unreleased - design-system rollout & clearance cleanup

### Added
- `PageShell`, `Card`, `CardContent` primitives to standardize page layouts.
- Screenshot helper: `frontend/scripts/screenshot.js` (captures desktop and mobile screenshots for updated pages).

### Changed
- Updated multiple pages to use `PageShell` and `Card`:
  - Dashboard, Attachments, Accessibility, AiSupport, Calendar, Clearance.
- Replaced corrupted `src/modules/clearance/ClearancePage.jsx` with clean implementation and preserved upload/preview/edit flows.

### Fixed
- Fixed duplicate heading in Clearance page that caused unit test failures.
- Re-enabled a short-term test shim in `src/setupTests.js` to reduce CI deprecation noise.

### Notes
- The test shim is intended as a temporary stopgap. Remove after upgrading test dependencies.
- Consider running `npx prettier --write .` to normalize formatting across the repo (many files currently flagged by Prettier).

