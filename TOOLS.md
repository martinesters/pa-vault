# TOOLS.md - Local Notes

Skills define _how_ tools work. This file is for _your_ specifics — the stuff that's unique to your setup.

## What Goes Here

Things like:

- Camera names and locations
- SSH hosts and aliases
- Preferred voices for TTS
- Speaker/room names
- Device nicknames
- Anything environment-specific

## Examples

```markdown
### Cameras

- living-room → Main area, 180° wide angle
- front-door → Entrance, motion-triggered

### SSH

- home-server → 192.168.1.100, user: admin

### TTS

- Preferred voice: "Nova" (warm, slightly British)
- Default speaker: Kitchen HomePod
```

## Why Separate?

Skills are shared. Your setup is yours. Keeping them apart means you can update skills without losing your notes, and share skills without leaking your infrastructure.

---

Add whatever helps you do your job. This is your cheat sheet.

## Google Kalender (gcalcli)

gcalcli ist im venv installiert: `~/.gcalcli-venv/bin/gcalcli`
OAuth-Client liegt in `~/.config/gcalcli/oauth_client.json` (Projekt ava-calendar-501820).
Manueller Fern-Login-Flow: `~/PA/tools/gcal_auth.py` (url / exchange).

Zwei Accounts, getrennte config-folder:
- **Account 1 (privat):** `--config-folder ~/.config/gcalcli-1` → martinesters88@gmail.com (Familie, Privat)
- **Account 2 (Business):** `--config-folder ~/.config/gcalcli-2` → Screen on Demand (Team-Kalender, SOD)

Beispiele:
```
~/.gcalcli-venv/bin/gcalcli --config-folder ~/.config/gcalcli-1 agenda today "in 14 days"
~/.gcalcli-venv/bin/gcalcli --config-folder ~/.config/gcalcli-1 add   # interaktiv
~/.gcalcli-venv/bin/gcalcli --config-folder ~/.config/gcalcli-1 quick "Zahnarzt morgen 15 Uhr"
```
Stderr voller Python-3.9-FutureWarnings → mit grep -viE rausfiltern.
Re-Auth bei Bedarf: `gcal_auth.py url ~/.config/gcalcli-N` → Link → `gcal_auth.py exchange ...`.

## Related

- [Agent workspace](/concepts/agent-workspace)
