# OpenClaw auf Mac mini einrichten (08.07.2026)

**Status:** ✅ Läuft (08.07.2026) — Bot `@martin_esters_pa_bot` antwortet auf Telegram; **geteiltes Gehirn (Git-Auto-Sync) live** zwischen Mac mini (`~/PA`) und MacBook (`~/Documents/PA`) via privatem GitHub-Repo `martinesters/pa-vault` · **Ziel:** OpenClaw läuft 24/7 auf dem Mac mini und ist per Telegram steuerbar

> **Ergebnis / Abweichungen vom Plan (08.07.2026):** Node NICHT via Homebrew (dessen Auto-Install scheiterte an non-TTY/sudo beim `curl|bash`), sondern **offizieller Node-.pkg von nodejs.org**, dann `sudo npm install -g openclaw@latest`. Danach Rechte-Fix nötig: `sudo chown -R martin ~/.openclaw` (EACCES, weil sudo-Install den Ordner root gab). Telegram wurde im Wizard NICHT abgefragt → **manuell** verbunden: `openclaw config set channels.telegram.{enabled true | botToken "…" | dmPolicy allowlist | allowFrom '["tg:7428142565"]'}`, dann `openclaw daemon restart`. Modell: Sonnet. Guthaben: $20 hart (kein Auto-Reload). Gateway loopback, gesund. **Noch offen/optional:** Auto-Login (für unbeaufsichtigten Reboot), `chmod 700 ~/.openclaw`, Gmail-Entwürfe mit Key/Token löschen, Reboot-Test, `openclaw security audit --deep`.
**KI-Zugang:** Anthropic API-Key (Pay-as-you-go) · **Vorlage:** Video „Clawd Bot einrichten" von Johannes Kliesch
**Ausführung:** heute Abend live mit Claude, Schritt für Schritt

> **Namens-Hinweis:** OpenClaw hieß früher „Clawdbot"/„Clawd" → kurz „Moltbot" → seit 30.01.2026 **OpenClaw** (gleiches Projekt). Einzige echten Quellen: `github.com/openclaw/openclaw`, `openclaw.ai`, `docs.openclaw.ai`. Klon-/Spam-Domains (openclawd.ai, clawd-bot.org …) ignorieren.

---

## ⚠️ Sicherheit — zuerst lesen
OpenClaw ist ein autonomer Agent mit **weitreichenden Rechten**: nach voller Einrichtung kann er jede Datei lesen/schreiben, Tastatur/Maus steuern und den Bildschirm aufnehmen — inklusive API-Keys und Tokens. Unabhängige Sicherheitsforschung (Microsoft, Giskard) stuft ihn als anfällig für Prompt-Injection ein. Deshalb fest eingebaut:
- **Dedizierter, nicht-administrativer macOS-Benutzer** nur für OpenClaw — nicht dein Alltags-Login.
- Gateway nur auf **loopback** (Standard), nie offen ins LAN/Internet.
- Telegram-DMs strikt auf **deine eigene numerische ID** gesperrt.
- `chmod 700 ~/.openclaw`.
- **Budget-Limit** in der Anthropic Console (24/7-Agent = Kosten pro Token → Kostenfalle vermeiden).

---

## ✅ JETZT vorbereiten (vor heute Abend)
- [ ] **Anthropic API-Key erstellen:** `console.anthropic.com` → einloggen/registrieren → **Settings → API Keys → Create Key** → `sk-ant-…` kopieren, sicher ablegen (1Password). Dann **Billing** hinterlegen + **Usage/Budget-Limit** (z. B. 20–50 €/Monat) setzen.
- [ ] **Telegram** auf dem iPhone bereit. **Bot-Username** überlegen — muss auf `bot` enden und global eindeutig sein (Vorschläge: `martin_pa_bot`, `esters_assistant_bot`, `me_clawbot`).
- [ ] **FileVault-Entscheidung** treffen (siehe Stage 1b). Empfehlung: **an** (verschlüsselt) — Preis: manuelles Entsperren nach dem (seltenen) Neustart.
- [ ] Optional, falls der Mac mini **ohne Monitor** läuft: **HDMI-Dummy-Plug** (Display-Emulator) besorgen.

---

## Stage 0 — Voraussetzungen
- Mac mini (Apple Silicon), aktuelles macOS. Kabel-Ethernet bevorzugt; im Router **feste/reservierte IP** vergeben.
- Xcode Command Line Tools (heute Abend am Mac):
```
xcode-select --install
```

## Stage 1 — macOS für 24/7
**1a. Dedizierter Benutzer** (wichtigste Sicherheitsmaßnahme)
- System Settings → Users & Groups → **Add Account…** → **Standard**-Benutzer (nicht Admin) nur für OpenClaw. Ab hier unter diesem Benutzer arbeiten.

**1b. FileVault vs. Auto-Login** (Entscheidung)
- Auto-Login (für unbeaufsichtigten Neustart) funktioniert **nicht** mit aktivem FileVault.
- **FileVault AN** = SSD verschlüsselt, Secrets bei Diebstahl geschützt, aber nach jedem Neustart manuell entsperren. *(Empfehlung — du bist theft-conscious; ein Home-Server rebootet selten.)*
- **FileVault AUS** = voll hands-off (Auto-Login + Auto-Restart nach Stromausfall), aber SSD unverschlüsselt.
- Umschalten: System Settings → Privacy & Security → **FileVault**.

**1c. Auto-Login** (nur wenn FileVault aus)
- System Settings → Users & Groups → (Schloss) → **Automatically log in as** → OpenClaw-Benutzer. (Neuere macOS: Lock Screen → „Log in automatically as".)

**1d. Schlaf verhindern** (persistent)
```
sudo pmset -a sleep 0
sudo pmset -a disksleep 0
sudo pmset -a displaysleep 0
sudo pmset -a tcpkeepalive 1
sudo pmset -a womp 1
sudo pmset -a autorestart 1
pmset -g          # prüfen: sleep 0, disksleep 0, autorestart 1
```

**1e. Energie-GUI**
- System Settings → **Battery/Energy** → Options → **„Prevent automatic sleeping when the display is off"** an + **„Start up automatically after a power failure"** an.

**1f. Remote-Zugang (headless)**
```
sudo systemsetup -setremotelogin on     # SSH
sudo systemsetup -getremotelogin
ipconfig getifaddr en0                    # lokale IP (en1 = WLAN)
```
- GUI-Fernzugriff (um Berechtigungsdialoge zu klicken): System Settings → General → **Sharing** → **Screen Sharing** → On. Verbinden: Finder → Gehe zu → Mit Server verbinden → `vnc://<mac-mini-ip>`.
- **SSH/Screen Sharing nie direkt ins Internet öffnen.** Fernzugriff von unterwegs nur über **Tailscale/VPN**.

## Stage 2 — OpenClaw installieren
```
curl -fsSL --proto '=https' --tlsv1.2 https://openclaw.ai/install.sh | bash
```
> Installiert nur die CLI (Node wird bei Bedarf mitinstalliert). Startet das Onboarding **nicht** von selbst. *(Pipe-to-Bash führt Remote-Code aus — wenn vorsichtig: URL erst laden & lesen, oder `npm install -g openclaw@latest`.)*

Onboarding + Daemon anlegen (Schlüsselbefehl für 24/7):
```
openclaw onboard --install-daemon
```
Wizard-Reihenfolge: (1) evtl. Reset · (2) **Risiko-Bestätigung → YES** · (3) Provider/Modell → Stage 3 · (4) Workspace (Default) · (5) Gateway → **loopback** lassen · (6) Channels → Telegram, Stage 4 · … · Health-Check. **Quickstart** wählen.

Nach Abschluss:
```
chmod 700 ~/.openclaw
```

## Stage 3 — KI-Provider (im Wizard, VOR Telegram)
- Provider: **Anthropic (Claude)**.
- Auth: **Anthropic API key** → `sk-ant-…` einfügen. (Nicht-interaktiv: `openclaw onboard --anthropic-api-key "$ANTHROPIC_API_KEY"`.)
- Modell **erst live prüfen**, dann setzen (IDs bewegen sich):
```
openclaw models list --provider anthropic
openclaw models set anthropic/claude-opus-4-8      # ID zuvor verifizieren
```
> Starkes, aktuelles Modell wählen (Opus- oder aktuelle Sonnet-Klasse), **kein** kleines — der Agent verarbeitet nicht-vertrauenswürdige Telegram-Nachrichten (Prompt-Injection-Risiko).

## Stage 4 — Telegram-Bot
**4a. Bot erstellen** — in Telegram **@BotFather** (blauer Haken) öffnen:
```
/newbot
```
→ Anzeigenamen (z. B. `Martin PA`) → Username auf `bot` endend → BotFather antwortet mit **HTTP API Token** `7123456789:AAF…` → **kopieren, geheim halten** (Leak: BotFather `/revoke`).

**4b. Token an OpenClaw** — im Wizard-Channels-Schritt einfügen, **oder** in `~/.openclaw/openclaw.json` unter `channels.telegram` (`enabled: true`, `botToken: "…"`). *(Telegram nutzt NICHT `openclaw channels login telegram`.)*

**4c. Eigene numerische ID holen** — in Telegram **@userinfobot** öffnen → **Start** → numerische ID (z. B. `8734062810`). *(Nur Zahl! `@username` wird stillschweigend ignoriert → Selbst-Aussperrung.)*

**4d. Bot auf NUR dich sperren:**
```
openclaw config set channels.telegram.dmPolicy allowlist
openclaw config set channels.telegram.allowFrom '["tg:DEINE_NUMERISCHE_ID"]'
```
Ergebnis in `~/.openclaw/openclaw.json`:
```json5
{ channels: { telegram: {
    enabled: true,
    botToken: "7123456789:AAF...",
    dmPolicy: "allowlist",
    allowFrom: ["tg:8734062810"]
} } }
```
> Nie `open`/`disabled`. Keine negativen Gruppen-IDs (`-100…`) in `allowFrom`. Gruppen erben DM-Freigaben **nicht** — separat unter `channels.telegram.groups`.

**4e. Gateway starten & prüfen**
```
openclaw gateway            # bzw. läuft schon via Daemon:
openclaw gateway status     # gesund: „RPC probe: ok"
openclaw doctor             # falls node nicht gefunden (launchd-PATH)
```

**4f. Erster Test** — eigenen Bot über `@username` öffnen → **Start** / `hallo` senden → Antwort binnen Sekunden = ✅. Falls nichts: `openclaw logs --follow` in zweitem Terminal, erneut senden; Allowlist-Ablehnung → numerische ID stimmt nicht.

**4g. Härtung**
```
openclaw security audit --deep
```
- Hochrisiko-Tools (exec/process/browser/cron) per Default **deny**.
- **Reboot-Test:** Mac mini neu starten → prüfen: (Auto-)Login, kein Schlaf (`pmset -g`), SSH erreichbar, Daemon wieder oben.

---

## Ava-Zugriff auf weitere Projekte (08.07.2026)
Ava kann jetzt auch **FLYR Claude** und **SoD** bearbeiten. Als private GitHub-Repos (`martinesters/flyr-claude`, `martinesters/sod`), **content-only** (große Medien via `.gitignore` ausgeschlossen — bleiben nur am MacBook). Auf dem Mini geklont nach `~/flyr-claude` und `~/sod` (Home-Root, TCC-frei). Ava arbeitet auf Branch `ava/work` (nie `main`); Review/Merge macht Martin in VS Code (Source Control). MacBook-Ordner: `~/Documents/FLYR Claude` (mit Leerzeichen) und `~/Documents/SoD`. Zugriff per Telegram-Test bestätigt.

**Quellen:** `docs.openclaw.ai/install`, `/channels/telegram`, `/providers/anthropic`, `/platforms/mac/permissions`, `/gateway/security`, `github.com/openclaw/openclaw`. Befehle/Modell-IDs können je Version driften → vor dem Festschreiben `openclaw --help` / `openclaw models list` live prüfen.
