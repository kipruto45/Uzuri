# Uzuri Frontend (React + Vite)

This is a small React frontend scaffold generated from the backend repository. It includes a tiny API explorer so you can quickly call your Django backend.

Quick start

1. Install dependencies

```powershell
cd frontend
npm install
```

2. Run the dev server (will run on http://localhost:5173)

```powershell
npm run dev
```

Notes

- The Vite dev server proxies `/api` to `http://localhost:8000` (see `vite.config.js`). This assumes your Django backend runs locally on port 8000.
- To change the default backend base URL in production builds, set `VITE_API_BASE` in an env file or replace API paths in the app.

Wired backend endpoints

The frontend now wires into multiple backend endpoints discovered from the Django backend configuration. Key mappings:

- Auth:
	- POST `/api/auth/login/` — login (expects JWT pair `{access, refresh}` or `token`)
	- POST `/api/auth/register/` — register (payload depends on backend)
	- GET `/api/auth/me/` — fetch current user

- Attachments:
	- GET `/api/attachments/` — list attachments (attachments page)
	- POST `/api/attachments/` — upload attachment (multipart/form-data: `file`, `title`, `description`)

- API discovery:
	- GET `/api/` — API root exposing links to resources (used by Resources page)

If any endpoint naming differs in your deployment, set `VITE_API_BASE` or edit the paths in `src` components accordingly.

Files created

- `src/components/ApiExplorer.jsx` — simple UI to call backend endpoints
- `vite.config.js` — dev server + proxy

Next steps you might want:

- Add route-based pages (React Router)
- Add authentication flows that wire into your Django auth endpoints
- Create typed API clients (TypeScript) for major backend resources

Docker (optional)

If you prefer to run the frontend inside Docker instead of installing Node locally, a simple Docker setup is available.

From the `frontend/` directory:

```powershell
docker compose up --build
```

This builds a container and exposes the dev server on port 5173. The compose file mounts the source so edits are reflected in the running container.

Generic CRUD UI

- The Resources page discovers available API endpoints via GET `/api/` and lists them.
- Click any resource to open a generic CRUD UI at `/crud/<resource-name>` where you can:
	- List items (GET)
	- View item details (GET)
	- Create a new item by pasting JSON and clicking Create (POST)
	- Delete an item (DELETE)

This UI is intentionally generic to help you explore and test backend viewsets quickly. For production UIs, create dedicated pages with proper forms and validation.

## Testing & CI

Local tests

```powershell
cd frontend
npm install
npm test
```

CI

A GitHub Actions workflow was added at `.github/workflows/frontend-ci.yml` that runs `npm ci`, executes the test suite, and builds the frontend on push/pull-request.

