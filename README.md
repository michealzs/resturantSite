# Restaurant Site

A simple Flask-powered restaurant website with registration/login, profile pages, and basic informational pages.

## Requirements

- Python 3.11+
- `pip`

## Local Development

```bash
python -m venv .venv
source .venv/bin/activate
pip install flask passlib
python main.py
```

The app listens on `http://localhost:81`.

## Docker Compose

```bash
docker compose up --build
```

Then visit `http://localhost:8080`.

## Notes

- User data is stored in `users.json` in the project root.
