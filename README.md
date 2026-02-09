# StokerCloud Custom Integration für Home Assistant

Diese Custom Integration liest Daten von der StokerCloud API und stellt sie als Sensoren in Home Assistant bereit.

## Features

✅ Einfache Einrichtung über die GUI - nur Benutzername erforderlich
✅ Automatische Aktualisierung alle 60 Sekunden
✅ Alle wichtigen Heizungsdaten als Sensoren:
  - Kesseltemperatur
  - Puffertemperatur
  - Abgastemperatur
  - Schafttemperatur
  - Externe Puffertemperatur
  - Leistung (kW und %)
  - Lambda Ist/Soll
  - Lichtsensor
  - Heizungsmodus (mit deutscher Übersetzung)

## Installation

### Methode 1: Manuell

1. Kopieren Sie den Ordner `stokercloud_custom` nach `/config/custom_components/`
2. Starten Sie Home Assistant neu
3. Gehen Sie zu **Einstellungen → Geräte & Dienste**
4. Klicken Sie auf **+ Integration hinzufügen**
5. Suchen Sie nach **"StokerCloud Custom"**
6. Geben Sie Ihren Benutzernamen ein (z.B. `Nbe-Pellet`)
7. Fertig! 🎉

### Methode 2: HACS (empfohlen für Updates)

1. Öffnen Sie HACS
2. Gehen Sie zu **Integrationen**
3. Klicken Sie auf die **3 Punkte** oben rechts → **Benutzerdefinierte Repositories**
4. Fügen Sie die Repository-URL hinzu
5. Kategorie: **Integration**
6. Installieren Sie die Integration
7. Starten Sie Home Assistant neu
8. Fügen Sie die Integration über die GUI hinzu (siehe Methode 1, Schritte 3-6)

## Konfiguration

Nach der Installation werden automatisch folgende Sensoren erstellt:

- `sensor.stokercloud_kesseltemperatur`
- `sensor.stokercloud_puffertemperatur`
- `sensor.stokercloud_abgastemperatur`
- `sensor.stokercloud_schafttemperatur`
- `sensor.stokercloud_externe_puffertemperatur`
- `sensor.stokercloud_leistung`
- `sensor.stokercloud_leistung_prozent`
- `sensor.stokercloud_lambda_ist`
- `sensor.stokercloud_lambda_soll`
- `sensor.stokercloud_lichtsensor`
- `sensor.stokercloud_modus`
- `sensor.stokercloud_datum`

## Fehlerbehebung

### Integration wird nicht gefunden
- Stellen Sie sicher, dass der Ordner korrekt unter `/config/custom_components/stokercloud_custom/` liegt
- Starten Sie Home Assistant neu

### Sensoren zeigen keine Werte
- Überprüfen Sie den Benutzernamen
- Prüfen Sie die Logs: **Einstellungen → System → Protokolle**
- Testen Sie die API manuell: `http://stokercloud.dk/dev/getdriftjson.php?mac=IHR_USERNAME`

### Update der Integration
- Löschen Sie den alten Ordner
- Kopieren Sie die neue Version
- Starten Sie Home Assistant neu

## Support

Bei Problemen oder Fragen öffnen Sie bitte ein Issue auf GitHub.

## Lizenz

MIT License
