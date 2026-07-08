---
typ: dashboard-live
---

# 🔄 Live-Übersicht (Dataview)

> Aktualisiert sich automatisch aus dem Frontmatter der Notizen. Statische Version: [[00_Dashboard]].

## Aktive Vorgänge (nach Frist)
```dataview
TABLE status AS Status, frist AS Frist, kategorie AS Kategorie
FROM "01_Vorgänge"
WHERE typ = "vorgang"
SORT frist ASC
```

## Anstehende Fristen
```dataview
TABLE frist AS Frist, status AS Status, file.folder AS Ort
WHERE frist
SORT frist ASC
```

## Offene To-dos (ganzer Vault)
```dataview
TASK
WHERE !completed
GROUP BY file.link
```

## Personen & Geburtstage
```dataview
TABLE beziehung AS Beziehung, geburtstag AS Geburtstag
FROM "04_Personen"
SORT geburtstag ASC
```
