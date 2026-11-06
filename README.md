Export all your WorldQuant BRAIN alphas to alphas.json.

Usage:

    pip install requests
    python alpha_extractor.py

    (asks for email + password; or set WQ_EMAIL / WQ_PASSWORD env vars)

- You must have python installed in your pc and make sure requests is installed.
- Or you can download the **alpha_extractor.exe**, put it in the folder where you want your alphas to be created and run the file.


Notes:
- Uses the unofficial BRAIN API (api.worldquantbrain.com). Endpoints may change.
- If your account has biometric (Persona) login, the script prints a link:
  open it, finish the check, then press Enter.
- Credentials stay on your machine and are never written to the output file.

