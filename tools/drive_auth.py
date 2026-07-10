#!/usr/bin/env python3
"""Manueller (fern-tauglicher) OAuth-Flow inkl. Google Drive.
  drive_auth.py url <token_dir>
  drive_auth.py exchange <token_dir> "<redirect_url_or_code>"
Speichert Credentials als JSON unter <token_dir>/drive_token.json.
Scopes: Drive readonly + Gmail (mitgenommen, damit ein Token alle PA-Aufgaben abdeckt).
"""
import sys, os, json
os.environ["OAUTHLIB_RELAX_TOKEN_SCOPE"] = "1"
from google_auth_oauthlib.flow import InstalledAppFlow

SCOPES = [
    "https://www.googleapis.com/auth/drive.readonly",
    "https://www.googleapis.com/auth/gmail.modify",
    "https://www.googleapis.com/auth/gmail.compose",
    "https://www.googleapis.com/auth/gmail.send",
]
CLIENT_FILE = os.path.expanduser("~/.config/gcalcli/oauth_client.json")

def make_flow():
    with open(CLIENT_FILE) as f:
        cfg = json.load(f)
    flow = InstalledAppFlow.from_client_config(cfg, scopes=SCOPES)
    flow.redirect_uri = "http://localhost"
    return flow

def cmd_url(token_dir):
    flow = make_flow()
    auth_url, state = flow.authorization_url(
        access_type="offline", prompt="consent", include_granted_scopes="true")
    os.makedirs(token_dir, exist_ok=True)
    with open(os.path.join(token_dir, ".drive_auth_state.json"), "w") as f:
        json.dump({"state": state, "code_verifier": flow.code_verifier}, f)
    print(auth_url)

def extract_code(arg):
    if arg.startswith("http"):
        from urllib.parse import urlparse, parse_qs
        return parse_qs(urlparse(arg).query).get("code", [None])[0]
    return arg.strip()

def cmd_exchange(token_dir, redirect_arg):
    code = extract_code(redirect_arg)
    if not code:
        print("FEHLER: kein code", file=sys.stderr); sys.exit(1)
    flow = make_flow()
    sp = os.path.join(token_dir, ".drive_auth_state.json")
    if os.path.exists(sp):
        with open(sp) as f:
            st = json.load(f)
        if st.get("code_verifier"):
            flow.code_verifier = st["code_verifier"]
    flow.fetch_token(code=code)
    c = flow.credentials
    out = os.path.join(token_dir, "drive_token.json")
    with open(out, "w") as f:
        f.write(c.to_json())
    os.chmod(out, 0o600)
    print("OK gespeichert:", out)

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print(__doc__); sys.exit(1)
    action, td = sys.argv[1], os.path.expanduser(sys.argv[2])
    if action == "url": cmd_url(td)
    elif action == "exchange": cmd_exchange(td, sys.argv[3])
    else: print(__doc__); sys.exit(1)
