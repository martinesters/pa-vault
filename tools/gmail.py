#!/usr/bin/env python3
"""Gmail-CLI für Ava. Token: <token_dir>/gmail_token.json
Befehle:
  gmail.py <token_dir> list [query] [max]        # Nachrichten auflisten (default: in:inbox)
  gmail.py <token_dir> read <message_id>         # eine Mail vollständig lesen
  gmail.py <token_dir> draft <to> <subject> <body_file>   # Entwurf anlegen
  gmail.py <token_dir> send  <to> <subject> <body_file>   # direkt senden
  gmail.py <token_dir> whoami
"""
import sys, os, json, base64
from email.mime.text import MIMEText
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from googleapiclient.discovery import build

def service(token_dir):
    tok = os.path.join(os.path.expanduser(token_dir), "gmail_token.json")
    creds = Credentials.from_authorized_user_file(tok)
    if creds.expired and creds.refresh_token:
        creds.refresh(Request())
        with open(tok, "w") as f:
            f.write(creds.to_json())
    return build("gmail", "v1", credentials=creds)

def hdr(msg, name):
    for h in msg.get("payload", {}).get("headers", []):
        if h["name"].lower() == name.lower():
            return h["value"]
    return ""

def cmd_whoami(svc):
    p = svc.users().getProfile(userId="me").execute()
    print(p.get("emailAddress"), "| Nachrichten:", p.get("messagesTotal"))

def cmd_list(svc, query="in:inbox", maxn=15):
    res = svc.users().messages().list(userId="me", q=query, maxResults=int(maxn)).execute()
    msgs = res.get("messages", [])
    if not msgs:
        print("(keine Treffer)"); return
    for m in msgs:
        full = svc.users().messages().get(userId="me", id=m["id"], format="metadata",
              metadataHeaders=["From","Subject","Date"]).execute()
        unread = "UNREAD" in full.get("labelIds", [])
        mark = "●" if unread else " "
        print(f"{mark} [{m['id']}] {hdr(full,'Date')[:22]:22} | {hdr(full,'From')[:35]:35} | {hdr(full,'Subject')[:60]}")

def _extract_body(payload):
    if payload.get("body", {}).get("data"):
        return base64.urlsafe_b64decode(payload["body"]["data"]).decode("utf-8","replace")
    for part in payload.get("parts", []):
        if part.get("mimeType") == "text/plain" and part.get("body",{}).get("data"):
            return base64.urlsafe_b64decode(part["body"]["data"]).decode("utf-8","replace")
    for part in payload.get("parts", []):
        r = _extract_body(part)
        if r: return r
    return ""

def cmd_read(svc, mid):
    m = svc.users().messages().get(userId="me", id=mid, format="full").execute()
    print("Von:    ", hdr(m,"From"))
    print("An:     ", hdr(m,"To"))
    print("Betreff:", hdr(m,"Subject"))
    print("Datum:  ", hdr(m,"Date"))
    print("-"*60)
    print(_extract_body(m.get("payload", {})).strip()[:5000])

def _raw(to, subject, body):
    msg = MIMEText(body, _charset="utf-8")
    msg["to"] = to; msg["subject"] = subject
    return base64.urlsafe_b64encode(msg.as_bytes()).decode()

def cmd_draft(svc, to, subject, body_file):
    body = open(os.path.expanduser(body_file)).read()
    d = svc.users().drafts().create(userId="me", body={"message":{"raw":_raw(to,subject,body)}}).execute()
    print("OK Entwurf angelegt, id:", d["id"])

def cmd_send(svc, to, subject, body_file):
    body = open(os.path.expanduser(body_file)).read()
    s = svc.users().messages().send(userId="me", body={"raw":_raw(to,subject,body)}).execute()
    print("OK gesendet, id:", s["id"])

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print(__doc__); sys.exit(1)
    td, cmd = sys.argv[1], sys.argv[2]
    svc = service(td)
    if cmd == "whoami": cmd_whoami(svc)
    elif cmd == "list": cmd_list(svc, *(sys.argv[3:5] or ["in:inbox"]))
    elif cmd == "read": cmd_read(svc, sys.argv[3])
    elif cmd == "draft": cmd_draft(svc, sys.argv[3], sys.argv[4], sys.argv[5])
    elif cmd == "send": cmd_send(svc, sys.argv[3], sys.argv[4], sys.argv[5])
    else: print(__doc__); sys.exit(1)
