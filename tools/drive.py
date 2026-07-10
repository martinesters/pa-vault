#!/usr/bin/env python3
"""Google Drive CLI für Ava (readonly). Token: <token_dir>/drive_token.json
Befehle:
  drive.py <token_dir> whoami
  drive.py <token_dir> list [query] [max]      # Dateien auflisten/suchen (Drive-Query oder Freitext)
  drive.py <token_dir> tree [folder_id]        # Ordnerinhalt
  drive.py <token_dir> get <file_id> [outfile]  # Datei herunterladen (Docs/Sheets -> export)
  drive.py <token_dir> cat <file_id>            # Textinhalt ausgeben (Docs/txt)
Freitext-Suche wird zu fullText/name-Query. Drive-Query-Syntax (name contains '...', mimeType=...) direkt nutzbar.
"""
import sys, os, io, json

def svc(token_dir):
    from googleapiclient.discovery import build
    from google.oauth2.credentials import Credentials
    from google.auth.transport.requests import Request
    p = os.path.join(token_dir, "drive_token.json")
    creds = Credentials.from_authorized_user_file(p)
    if creds.expired and creds.refresh_token:
        creds.refresh(Request())
        with open(p, "w") as f: f.write(creds.to_json())
    return build("drive", "v3", credentials=creds)

def is_drive_query(q):
    ops = ["contains", "mimeType", "'me' in", "parents", "=", "name ", "fullText", "trashed"]
    return any(o in q for o in ops)

def cmd_whoami(td):
    s = svc(td)
    a = s.about().get(fields="user").execute()
    print(a["user"].get("emailAddress"), "-", a["user"].get("displayName"))

def cmd_list(td, query=None, mx=25):
    s = svc(td)
    if query and not is_drive_query(query):
        q = f"(name contains '{query}' or fullText contains '{query}') and trashed=false"
    elif query:
        q = query if "trashed" in query else f"({query}) and trashed=false"
    else:
        q = "trashed=false"
    r = s.files().list(q=q, pageSize=int(mx), orderBy="modifiedTime desc",
        fields="files(id,name,mimeType,modifiedTime,size,owners(emailAddress))",
        supportsAllDrives=True, includeItemsFromAllDrives=True).execute()
    for f in r.get("files", []):
        mt = f["mimeType"].split(".")[-1]
        sz = f.get("size", "-")
        print(f"{f['id']}  [{mt:14.14}] {f['modifiedTime'][:10]}  {f['name']}")

def cmd_tree(td, folder="root"):
    s = svc(td)
    r = s.files().list(q=f"'{folder}' in parents and trashed=false", pageSize=100,
        orderBy="folder,name", fields="files(id,name,mimeType,modifiedTime)",
        supportsAllDrives=True, includeItemsFromAllDrives=True).execute()
    for f in r.get("files", []):
        d = "DIR " if f["mimeType"].endswith("folder") else "    "
        print(f"{d}{f['id']}  {f['name']}")

EXPORT = {
    "application/vnd.google-apps.document": ("application/pdf", ".pdf"),
    "application/vnd.google-apps.spreadsheet": ("application/vnd.openxmlformats-officedocument.spreadsheetml.sheet", ".xlsx"),
    "application/vnd.google-apps.presentation": ("application/pdf", ".pdf"),
}

def cmd_get(td, fid, outfile=None):
    from googleapiclient.http import MediaIoBaseDownload
    s = svc(td)
    meta = s.files().get(fileId=fid, fields="name,mimeType", supportsAllDrives=True).execute()
    name, mime = meta["name"], meta["mimeType"]
    if mime in EXPORT:
        emime, ext = EXPORT[mime]
        req = s.files().export_media(fileId=fid, mimeType=emime)
        if not outfile: outfile = name + ext
    else:
        req = s.files().get_media(fileId=fid, supportsAllDrives=True)
        if not outfile: outfile = name
    fh = io.FileIO(outfile, "wb")
    dl = MediaIoBaseDownload(fh, req)
    done = False
    while not done:
        _, done = dl.next_chunk()
    fh.close()
    print("saved:", outfile)

def cmd_cat(td, fid):
    s = svc(td)
    meta = s.files().get(fileId=fid, fields="name,mimeType", supportsAllDrives=True).execute()
    mime = meta["mimeType"]
    if mime == "application/vnd.google-apps.document":
        data = s.files().export(fileId=fid, mimeType="text/plain").execute()
        sys.stdout.buffer.write(data)
    elif mime.startswith("text/"):
        data = s.files().get_media(fileId=fid, supportsAllDrives=True).execute()
        sys.stdout.buffer.write(data)
    else:
        print(f"(kein Text-Export für {mime}; nutze 'get')", file=sys.stderr)

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print(__doc__); sys.exit(1)
    td = os.path.expanduser(sys.argv[1]); cmd = sys.argv[2]; rest = sys.argv[3:]
    if cmd == "whoami": cmd_whoami(td)
    elif cmd == "list": cmd_list(td, *rest)
    elif cmd == "tree": cmd_tree(td, *(rest or ["root"]))
    elif cmd == "get": cmd_get(td, *rest)
    elif cmd == "cat": cmd_cat(td, *rest)
    else: print(__doc__); sys.exit(1)
