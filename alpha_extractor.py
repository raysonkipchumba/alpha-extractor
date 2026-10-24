"""Export all your WorldQuant BRAIN alphas to alphas.json.

Usage:
    pip install requests
    python wq_export_alphas.py
        (asks for email + password; or set WQ_EMAIL / WQ_PASSWORD env vars)

Notes:
- Uses the unofficial BRAIN API (api.worldquantbrain.com). Endpoints may change.
- If your account has biometric (Persona) login, the script prints a link:
  open it, finish the check, then press Enter.
- Credentials stay on your machine and are never written to the output file.
"""
import getpass
import json
import os
import sys
import time

import requests

API = "https://api.worldquantbrain.com"
OUT = "alphas.json"
PAGE = 100


def login(session: requests.Session) -> None:
    email = os.environ.get("WQ_EMAIL") or input("BRAIN email: ").strip()
    password = os.environ.get("WQ_PASSWORD") or getpass.getpass("BRAIN password: ")
    session.auth = (email, password)

    r = session.post(f"{API}/authentication")
    if r.status_code == 401 and "persona" in r.headers.get("WWW-Authenticate", "").lower():
        link = r.headers.get("Location", "")
        if link and not link.startswith("http"):
            link = API + link
        print(f"\nBiometric check needed. Open this link and complete it:\n{link}\n")
        input("Press Enter once done... ")
        r = session.post(link)
    if r.status_code not in (200, 201):
        sys.exit(f"Login failed ({r.status_code}): {r.text[:200]}")
    session.auth = None  # session cookie is enough from here
    print("Logged in.")


def fetch_all(session: requests.Session) -> list:
    alphas, offset, total = [], 0, None
    while True:
        r = session.get(
            f"{API}/users/self/alphas",
            params={"limit": PAGE, "offset": offset, "order": "-dateCreated"},
        )
        if r.status_code == 429:
            time.sleep(float(r.headers.get("Retry-After", 5)))
            continue
        if r.status_code != 200:
            sys.exit(f"Fetch failed at offset {offset} ({r.status_code}): {r.text[:200]}")
        data = r.json()
        total = data.get("count", total)
        batch = data.get("results", [])
        if not batch:
            break
        alphas.extend(batch)
        offset += len(batch)
        print(f"Fetched {len(alphas)}/{total}")
        if total is not None and offset >= total:
            break
    return alphas


def main() -> None:
    s = requests.Session()
    login(s)
    alphas = fetch_all(s)
    with open(OUT, "w", encoding="utf-8") as f:
        json.dump(alphas, f, indent=2, ensure_ascii=False)
    print(f"Saved {len(alphas)} alphas to {OUT}")


if __name__ == "__main__":
    main()