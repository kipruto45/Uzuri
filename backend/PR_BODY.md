Title: chore: cleanup .gitignore, untrack compiled artifacts, use in-memory channels during tests

Summary:
- Add repository-level and backend .gitignore to ignore __pycache__, *.pyc, db.sqlite3, media test uploads, and common backup files.
- Remove tracked compiled artifacts and sqlite DB from the repo history (untracked in this branch).
- During test runs, override CHANNEL_LAYERS to use the in-memory layer to avoid requiring Redis and to silence connection refused logs in tests.
- Small cleanup: provide a clean no-op debug middleware and remove test-only debug middleware references.

Why:
- Test runs in CI/dev shouldn't require Redis running and should avoid noisy logs.
- Committed pyc and db files are noise and can cause merge conflicts; ignoring them avoids accidental commits.

Files changed (high level):
- Added: .gitignore, backend/.gitignore
- Modified: backend/uzuri_university/settings.py (in-memory CHANNEL_LAYERS during tests)
- Added/removed many compiled artifacts from the index
- Added regression tests and migrations (previously committed during earlier debugging)

Test run:
- From backend/: python manage.py test
- Result: Ran 51 tests — OK

Notes and next steps:
- I created branch 'chore/cleanup-ignore-inmemory-channels' and pushed it to origin.
- Use the GitHub URL to open a PR: https://github.com/kipruto45/Uzuri/pull/new/chore/cleanup-ignore-inmemory-channels
- If you'd like, I can create the PR body via the GitHub API given a token, or run the gh CLI if you prefer and it's configured.
- Optional tidy: move StudentIDSequence to a top-level model file with a dedicated migration to make the history clearer; I can implement that in a follow-up PR.
