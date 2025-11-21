# harshildon

This repository hosts the **Contact Manager** Flask application located in `contact-manager/`. The app delivers full CRUD contact management, CSV import/export, search, pagination, logging, and a responsive UI.

## Quick Start (Local)

```bash
cd contact-manager
python -m venv venv
venv\Scripts\activate           # source venv/bin/activate on macOS/Linux
pip install -r requirements.txt
python app.py                   # served on http://localhost:4000
```

## Deploying to Vercel

1. Install the [Vercel CLI](https://vercel.com/docs/cli): `npm i -g vercel`
2. From the repo root run:
   ```bash
   vercel
   vercel --prod
   ```
   Vercel reads `vercel.json` and builds `contact-manager/app.py` using `@vercel/python`.
3. Configure environment variables in Vercel (Dashboard → Settings → Environment Variables or `vercel env add`):
   - `DATABASE_URL` – production database connection string (SQLite on Vercel is ephemeral; prefer hosted DBs such as Neon, Supabase, PlanetScale, etc.).
   - `SECRET_KEY` – Flask secret key.

All traffic is routed to the Flask app through `vercel.json`, which pins the runtime to Python 3.11. Refer to `contact-manager/README.md` for the full feature list and usage details.
