---
typ: vorgang
status: in-arbeit
kategorie: tech/umzug
frist: 2026-07-12
tags: [iphone, umzug, banking, 2fa, apple]
---

# iPhone-Umzug 15 Pro Max → 17 Pro Max (08.07.2026)

**Status:** 🟡 In Vorbereitung · **Methode:** Quick Start (direkt, beide Geräte vorhanden) · **SIM:** physische Nano-SIM umstecken
**Kritisch:** alle 6 Banking-Apps müssen danach voll laufen · keine 2FA-Aussperrung
**Kernregel:** Altes iPhone bleibt unangetastet, bis am neuen Gerät ALLES verifiziert ist.

> ⏰ **Timing:** Umzug am besten **heute/morgen (08.–09.07.)** durchziehen → alles (inkl. Trade-Republic-Sperre ~4 Tage) ist bis Mallorca (13.–18.07.) gesetzt. **Altes iPhone mit nach Mallorca als Fallback**, erst nach Rückkehr (nach 18.07.) zurücksetzen.

---

## A) Vorbereitung (altes iPhone, VOR dem Umzug)

- [ ] Beide Geräte auf dieselbe iOS-26-Version, WLAN + Bluetooth an, ans Ladekabel
- [ ] iCloud-Schlüsselbund aktiv (Einstellungen → Name → iCloud → Passwörter). Bei Advanced Data Protection: Geräte-Code + Wiederherstellungsschlüssel bereitlegen
- [ ] Verschlüsseltes iCloud-Backup als Sicherheitsnetz gemacht
- [ ] **1Password Emergency Kit** raussuchen (E-Mail + Kontopasswort + **Secret Key**) — ohne Secret Key kein Login am neuen Gerät
- [ ] **Google Authenticator:** Cloud-Sync aufs Google-Konto an ODER „Konten übertragen → Exportieren" (QR). Alte App NICHT löschen
- [ ] **Microsoft Authenticator:** Cloud-Backup einschalten
- [ ] **Backup-/Recovery-Codes** sichern (Google, Apple, Amex, alles hinter einem Authenticator) — separat ablegen
- [ ] ⚠️ **Trade Republic:** alle Auszahlungen/Kartenzahlungen der nächsten Tage JETZT erledigen (danach ~4 Tage Sperre). TR-PIN bereit
- [ ] **ING:** Zugangsnummer/Benutzername + Internetbanking-PIN + neue mobilePIN + **Ausweis** (für sofortige Aktivierung per Scan)
- [ ] Restliche Zugangsdaten parat: N26, Revolut-Passcode, PayPal, Amex
- [ ] Wallet-Inventar notieren (Amex, N26, ggf. Revolut, DB/BahnCard)
- [ ] SIM-Werkzeug bereit, ~1–2 Std Zeitfenster einplanen

## B) Der Umzug (Quick Start)

- [ ] Neues iPhone neben das alte → „Neues iPhone einrichten"
- [ ] Wolke am Neuen mit Kamera des Alten scannen → Passcode des alten iPhones eingeben
- [ ] Face ID neu einrichten
- [ ] Übertragungsart **„Von iPhone übertragen"** (NICHT „Aus iCloud laden"); optional USB-C-Kabel
- [ ] **Schritt „Mobilfunk/Rufnummer übertragen" → „Später"** (physische SIM behalten, NICHT in eSIM wandeln)
- [ ] Beide Geräte nah + am Strom lassen bis fertig; iCloud-Schlüsselbund-Freigabe bestätigen
- [ ] Nano-SIM umstecken (altes aus → SIM ins neue → an)
- [ ] WhatsApp neu installieren, gleiche Nummer → am Altgerät „Chats auf iPhone übertragen" → QR scannen
- [ ] Apple Watch: Prompt „Deine Apple Watch verwenden?" bestätigen (nicht vorher manuell entkoppeln)

## C) Nach dem Umzug — Neu-Aktivierung (SIM steckt schon im neuen Gerät!)

**2FA zuerst:**
- [ ] iCloud-Schlüsselbund: Passwörter/Passkeys/WLAN da?
- [ ] 1Password neu anmelden (QR vom Altgerät oder Secret Key)
- [ ] Google Authenticator: Sync/QR → 1 Code live testen
- [ ] Microsoft Authenticator: Wiederherstellung → jeden Eintrag prüfen

**Banking (in dieser Reihenfolge):**
- [ ] **Trade Republic zuerst:** gleiche Nummer → PIN → Gerät koppeln → SMS-Code (Sperre darf laufen; nicht parallel am PC einloggen)
- [ ] **N26:** Login → SMS-Code → „Neues Gerät koppeln" (Code per SMS + PIN) → ggf. Confirm-Link per E-Mail
- [ ] **ING:** neue mobilePIN → Zugangsnummer + PIN → Aktivierung per Ausweis-Scan
- [ ] **Revolut:** Nummer + SMS-OTP → Passcode → ggf. Selfie (~12 Std Cooling-off für Transfers)
- [ ] **PayPal:** Login + 2FA
- [ ] **Amex:** Login + 2FA-Code

**Apple Pay / Wallet (alles neu):**
- [ ] Jede Karte (Amex, N26, ggf. Revolut) neu ins Wallet + verifizieren
- [ ] DB Navigator öffnen (Tickets/BahnCard); Boardingpässe ggf. neu laden

## D) Verifikation — ERST DANN altes Gerät zurücksetzen (nach Mallorca)

- [ ] Fotos, Nachrichten (SMS + iMessage), Mail, Kontakte, WhatsApp-Verlauf vollständig
- [ ] iCloud-Schlüsselbund + 1Password öffnen/entsperren OK
- [ ] Google + Microsoft Authenticator: JEDER Code getestet
- [ ] Alle 6 Banking-Apps eingeloggt/gekoppelt (TR-Sperre darf noch laufen)
- [ ] Apple Pay: alle Karten neu + verifiziert (eine Testzahlung)
- [ ] iMessage/FaceTime laufen am neuen Gerät
- [ ] Aufräumen: Karten am Altgerät aus Wallet, Apps abmelden, Altgerät in N26/ING/Amex-Gerätemanagement entfernen
- [ ] **Erst dann** altes iPhone zurücksetzen

---

## ⚠️ Fallstricke (nicht ignorieren)

- **TR-4-Tage-Sperre** → vorher Auszahlungen/Kartenzahlungen erledigen
- **Authenticator-Seeds ziehen NICHT automatisch mit** → ohne Sync/Export + Backup-Codes = Aussperrung
- **MS Authenticator oft unvollständig** (Arbeits-/Drittanbieterkonten) → Backup-Codes Pflicht
- **Alte Nummer = Lebensader** (SMS-2FA für N26/TR/Revolut/PayPal/Amex) → alte SIM/Nummer aktiv halten
- **1Password Secret Key** nicht wiederherstellbar → Emergency Kit vorher bereitlegen
- **Beim Setup NICHT „SIM in eSIM umwandeln"** wählen
- **Wallet-Karten** nicht aus Backup — jede neu hinzufügen
