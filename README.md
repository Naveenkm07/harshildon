# harshildon

Offline-first **Contact Manager** built with Flask, SQLAlchemy, and pure HTML/CSS/JS. The full application lives in the `contact-manager/` directory and ships with everything needed to run entirely on your machine (SQLite persistence, CSV import/export, search, pagination, logging, etc.). Vercel configuration is included for optional one-click hosting, but no cloud database is required.

## 🚀 Local Development (offline)

```bash
git clone https://github.com/Naveenkm07/harshildon.git
cd harshildon/contact-manager
python -m venv venv
venv\Scripts\activate           # source venv/bin/activate on macOS/Linux
pip install -r requirements.txt
python app.py                   # launches on http://localhost:4000
```

- A fresh `contacts.db` SQLite file is created automatically on first launch.
- All data stays on disk under `contact-manager/contacts.db`, so you can use the app completely offline.
- Logs are written to `contact-manager/logs/app.log` for quick debugging.

## 🌐 Optional: Deploying to Vercel

The repo root contains `vercel.json`, which points the Python builder at `contact-manager/app.py`. To publish a demo build:

1. Install the [Vercel CLI](https://vercel.com/docs/cli): `npm i -g vercel`
2. From the repo root:
   ```bash
   vercel          # preview deployment
   vercel --prod   # production deployment
   ```
3. Environment variables (Dashboard → Settings → Environment Variables, or `vercel env add`):
   - `DATABASE_URL` – optional. Defaults to `sqlite:///tmp/contacts.db` for ephemeral demos. Provide a hosted DB URI (Postgres/MySQL/etc.) if you need persistence online.
   - `SECRET_KEY` – Flask secret key. Defaults to `replace-me-secret`; override in production.

Everything else is automatic: the runtime is pinned to Python 3.11 and all routes are proxied to Flask.

## 📚 Documentation

See [`contact-manager/README.md`](contact-manager/README.md) for the full feature list, screenshots, CSV format, troubleshooting tips, and development notes. That file also explains how to change database backends (SQLite/MySQL) or customize pagination, logging, and import/export behavior.
