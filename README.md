# Garmin iPhone Web-App (PWA)

Diese App ist für Safari auf dem iPhone gestaltet. Nach dem Hosting kann sie über „Teilen → Zum Home-Bildschirm“ installiert werden.

## Was enthalten ist
- Mobiloptimierte Web-App
- Backend nutzt Garmins offiziellen Python-Client für die Personal API
- Ruft Gewicht, Schritte, Tageszusammenfassungen, Schlaf, HRV, Body Battery und Aktivitäten für die letzten 30 Tage ab
- API-Schlüssel wird serverseitig als Umgebungsvariable gespeichert, nicht im Browser
- PWA-Manifest und Service Worker

## Bereitstellung ohne eigenen PC/Mac
Der einfachste Weg vom iPhone ist ein Hosting-Konto, das GitHub-Repositories deployen kann, zum Beispiel Render. Dafür müssen die Dateien in ein privates GitHub-Repository hochgeladen und mit dem Hosting verbunden werden. Danach wird `GARMIN_PERSONAL_API_KEY` im Hosting-Dashboard als Secret/Environment Variable gesetzt.

`render.yaml` ist als Blueprint vorbereitet. Im Hosting-Dienst:
1. Erstelle ein privates GitHub-Repository und lade alle Dateien dieses Ordners hoch.
2. Erstelle einen neuen Blueprint/Web Service aus diesem Repository.
3. Setze `GARMIN_PERSONAL_API_KEY` als Secret/Environment Variable mit deinem Garmin Personal API Key.
4. Deploye und öffne die bereitgestellte HTTPS-Adresse auf dem iPhone.
5. In Safari: Teilen → Zum Home-Bildschirm.

Die kostenlose Hosting-Stufe kann schlafen gehen oder beim ersten Aufruf langsam sein; Verfügbarkeit und kostenlose Limits hängen vom Anbieter ab. Das Hosting ist ein externer Dienst und kann seine Bedingungen ändern.

## Sicherheit
- API-Key nur in den Server-Secrets hinterlegen; nie in `index.html`, GitHub-Dateien oder Browser-Eingaben einfügen.
- Der vorher in Chat geteilte API-Key sollte aus Sicherheitsgründen in Garmin Connect widerrufen und neu erstellt werden.
- Verwende ein privates Repository. Diese Vorlage enthält noch keine zusätzliche Benutzeranmeldung vor dem Dashboard. Vor einer öffentlichen Bereitstellung sollte ein Zugriffsschutz (z. B. vorgeschaltete Authentifizierung) aktiviert werden, da Gesundheitsdaten sensibel sind.
- Der Server gibt nur Daten für das eine hinterlegte Garmin-Konto zurück. Teile die Web-Adresse nicht öffentlich.
- Garmin Personal API ist laut Garmin für persönliche Anwendungen gedacht und read-only. Sie kann nur Daten abrufen, die Garmin in den API-Ressourcen bereitstellt.

## Hinweise
- Die API-Antworten können je nach verfügbarer Garmin-Ressource und Kontodaten variieren. Die App ist ein Startpunkt; nach dem ersten Deployment sollte geprüft werden, ob alle Datenfelder in der aktuellen Garmin-API-Antwort korrekt angezeigt werden.
- Das Dashboard berechnet noch kein Kaloriendefizit, da dafür eine zuverlässige tägliche Kalorienaufnahme als zusätzliche Datenquelle erforderlich ist.
- Referenzen:
  - https://developer.garmin.com/gc-developer-program/personal/personal-faq
  - https://github.com/garmin/connect-personal-api-python
