#!/usr/bin/env python3
"""Manueller (fern-tauglicher) OAuth-Flow für gcalcli.
Nutzung:
  Schritt 1 (Link erzeugen):   gcal_auth.py url <config_folder>
  Schritt 2 (Code eintauschen): gcal_auth.py exchange <config_folder> "<redirect_url_or_code>"
Speichert das Ergebnis als pickle unter <config_folder>/oauth (gcalcli-kompatibel).
State (flow) wird zwischen den Schritten in <config_folder>/.auth_state.json gehalten.
"""
import sys, os, json, pickle
from google_auth_oauthlib.flow import InstalledAppFlow

SCOPES = ["https://www.googleapis.com/auth/calendar"]
CLIENT_FILE = os.path.expanduser("~/.config/gcalcli/oauth_client.json")
REDIRECT = "urn:ietf:wg:oauth:2.0:oob"

def load_cfg():
    with open(CLIENT_FILE) as f:
        return json.load(f)

def make_flow():
    cfg = load_cfg()
    flow = InstalledAppFlow.from_client_config(cfg, scopes=SCOPES)
    flow.redirect_uri = "http://localhost"
    return flow

def cmd_url(config_folder):
    flow = make_flow()
    auth_url, state = flow.authorization_url(
        access_type="offline", prompt="consent", include_granted_scopes="true")
    os.makedirs(config_folder, exist_ok=True)
    with open(os.path.join(config_folder, ".auth_state.json"), "w") as f:
        json.dump({"state": state}, f)
    print(auth_url)

def extract_code(arg):
    if arg.startswith("http"):
        from urllib.parse import urlparse, parse_qs
        q = parse_qs(urlparse(arg).query)
        return q.get("code", [None])[0]
    return arg.strip()

def cmd_exchange(config_folder, redirect_arg):
    code = extract_code(redirect_arg)
    if not code:
        print("FEHLER: kein code gefunden", file=sys.stderr); sys.exit(1)
    flow = make_flow()
    flow.fetch_token(code=code)
    creds = flow.credentials
    oauth_path = os.path.join(config_folder, "oauth")
    with open(oauth_path, "wb") as f:
        pickle.dump(creds, f)
    print("OK gespeichert:", oauth_path)

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print(__doc__); sys.exit(1)
    action, folder = sys.argv[1], os.path.expanduser(sys.argv[2])
    if action == "url":
        cmd_url(folder)
    elif action == "exchange":
        cmd_exchange(folder, sys.argv[3])
    else:
        print(__doc__); sys.exit(1)
