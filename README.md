Export all your WorldQuant BRAIN alphas to alphas.json.

Usage:
    pip install requests
    python wq_export_alphas.py
        (asks for email + password; or set WQ_EMAIL / WQ_PASSWORD env vars)

Notes:
- Uses the unofficial BRAIN API (api.worldquantbrain.com). Endpoints may change.
- If your account has biometric (Persona) login, the script prints a link:
  open it, finish the check, then press Enter.
- Credentials stay on your machine and are never written to the output file.