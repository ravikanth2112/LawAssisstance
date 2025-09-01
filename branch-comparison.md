# Branch Comparison: DEV vs MAIN

## Files COMMON to both branches (✅ Same files):

### Core React App Files:
- `.github/copilot-instructions.md`
- `.gitignore`
- `.vscode/tasks.json`
- `README.md`
- `package-lock.json`
- `package.json`
- `public/index.html`
- `src/index.js`
- `src/styles/App.css`

### React Components:
- `src/App.js`
- `src/components/DashboardStats.js`
- `src/components/RecentActivity.js`
- `src/components/Sidebar.js`
- `src/components/Sidebar_bootstrap.js`
- `src/components/UpcomingDeadlines.js`
- `src/data/sampleData.js`

### React Pages:
- `src/pages/Analytics.js`
- `src/pages/Billing.js`
- `src/pages/Branding.js`
- `src/pages/Clients.js`
- `src/pages/Clients_bootstrap.js`
- `src/pages/Dashboard.js`
- `src/pages/Dashboard_bootstrap.js`
- `src/pages/Deadlines.js`
- `src/pages/Documents.js`
- `src/pages/FirmBranding.js`
- `src/pages/SignIn.js`

## Files ONLY in MAIN branch (❌ API/Backend code):

### Authentication & API Integration:
- `src/context/AuthContext.js`
- `src/services/api.js`

### Backend/API Code:
- `backend/.env`
- `backend/.env.example`
- `backend/README.md`
- `backend/app/database.py`
- `backend/app/main.py`
- `backend/app/models/__init__.py`
- `backend/app/models/case.py`
- `backend/app/models/client.py`
- `backend/app/models/lawyer.py`
- `backend/app/models/user.py`
- `backend/app/routers/auth.py`
- `backend/app/routers/cases.py`
- `backend/app/routers/clients.py`
- `backend/app/routers/dashboard.py`
- `backend/app/routers/lawyers.py`
- `backend/app/routers/users.py`
- `backend/app/schemas.py`
- `backend/app/schemas/__init__.py`
- `backend/app/schemas/case.py`
- `backend/app/schemas/client.py`
- `backend/app/schemas/lawyer.py`
- `backend/app/schemas/user.py`
- `backend/app/utils/auth.py`
- `backend/database_setup.md`
- `backend/requirements.txt`
- `backend/run_server.py`
- `backend/scripts/init_db.py`
- `backend/scripts/test_backend.py`
- `backend/start_server.bat`
- `backend/start_server.ps1`
- `backend/test_connection.py`

### Documentation & Build:
- `AUTHENTICATION_TEST_RESULTS.md`
- `PHASE_1_COMPLETE.md`
- `build/asset-manifest.json`
- `build/index.html`
- `build/static/js/main.5185e25d.js`
- `build/static/js/main.5185e25d.js.LICENSE.txt`
- `build/static/js/main.5185e25d.js.map`
- `docs/api-documentation.html`
- `docs/api-documentation.md`
- `docs/database-erd.html`
- `docs/database-erd.md`
- `index.html`
- `readme1.md`
- `test-credentials.md`
- `vite.config.js`

### Python Cache Files:
- All `backend/app/__pycache__/` files
- All `backend/app/models/__pycache__/` files
- All `backend/app/routers/__pycache__/` files
- All `backend/app/schemas/__pycache__/` files

## Files ONLY in DEV branch:
- None (DEV is a subset of MAIN)

## SUMMARY:

**DEV Branch**: 25 files (UI components only)
**MAIN Branch**: 87 files (UI + Backend + API + Documentation)

**Recommendation**: 
- Keep DEV as pure UI/frontend development
- Remove all backend/API code from MAIN to match your requirement
- Move all backend/API code to a separate branch or keep only in DEV for Phase 1 APIs
