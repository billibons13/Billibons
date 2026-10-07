> **Для владельца (RU):** черновик Datenschutzerklärung (политика конфиденциальности по DSGVO) для бота @RAIV_FISH_bot и витрины Mini App. Описано то, что бот реально делает по коду (Make eu1, Data Store, уведомления продавцу в Telegram, Stripe-тест, Claude-помощник, GitHub Pages). Заполните `[...]`, проверьте пометки **«AVV/DPA prüfen»** (договоры обработки данных с сервисами — заключить/скачать в их кабинетах) и сроки хранения. Если какой-то функции нет (например, онлайн-оплата не включена) — удалите раздел. Перед публикацией — проверить у юриста.

> ⚠️ **Entwurf — vor Veröffentlichung juristisch prüfen lassen.**

# Datenschutzerklärung

für den Telegram-Bot **@RAIV_FISH_bot** und die Web-App / Online-Vitrine **https://billibons13.github.io/Billibons/** („Mini App“)

Stand: [Datum]

## 1. Verantwortlicher
Verantwortlich im Sinne von Art. 4 Nr. 7 DSGVO:

[Name / Firma]
[Anschrift]
E-Mail: [E-Mail]
Telefon: [Telefon]

Ein Datenschutzbeauftragter ist [nicht benannt / benannt: Name, Kontakt — prüfen, ob Pflicht nach § 38 BDSG besteht].

## 2. Überblick
Über den Bot und die Mini App können Sie Fisch und weitere Produkte ansehen, bestellen, sich liefern lassen und an einem Bonusprogramm teilnehmen. Die technische Verarbeitung erfolgt über die Automatisierungsplattform Make (Server-Region EU). Wir verarbeiten nur die Daten, die für Bestellung, Lieferung und Kundenbetreuung nötig sind.

## 3. Welche Daten wir verarbeiten
**a) Telegram-Kontodaten** (automatisch beim Schreiben an den Bot): Telegram-Nutzer-ID / Chat-ID, Vorname/Name und Benutzername (@username), soweit in Ihrem Telegram-Profil hinterlegt, gewählte Sprache.

**b) Bestell- und Lieferdaten** (von Ihnen eingegeben): Telefonnummer, Lieferanschrift, bestellte Produkte, Mengen, Preise, Bestellnummer, Zeitpunkt, Zahlungsart, ggf. Kommentar zur Bestellung.

**c) Kundenkonto-/Bonusdaten:** Anzahl bisheriger Bestellungen, Bonusstand bzw. gewährte Rabatte, Spracheinstellung.

**d) Nachrichteninhalte:** Texte und Tastenbefehle, die Sie an den Bot senden, soweit für die Bearbeitung nötig.

**e) Mini App:** Beim Aufruf der Mini App verarbeitet der Hoster technisch Ihre IP-Adresse und Browser-/Geräteinformationen (siehe 6.c). Die Mini App lädt die Produktliste (Preise, Verfügbarkeit) von unserem Make-Server; dabei wird ebenfalls Ihre IP-Adresse übertragen. Bei einer Bestellung aus der Mini App werden Warenkorb-Daten über Telegram an den Bot übermittelt. Im lokalen Speicher Ihres Geräts (localStorage) werden ausschließlich Ihr Warenkorb („raiv_cart“) und ggf. der Punktestand des Mini-Spiels („raiv_best“) gespeichert; diese Daten verlassen Ihr Gerät nicht von selbst. Wir setzen keine Analyse- oder Werbe-Cookies und kein Tracking ein. [prüfen, falls später ergänzt]

**f) Zahlungsdaten (nur bei Online-Zahlung, falls angeboten):** Die Zahlung erfolgt direkt bei Stripe. Kartendaten u. Ä. erhalten wir nicht; wir erhalten nur Betrag, Zahlungsstatus und Zahlungs-/Sitzungs-ID.

## 4. Zwecke und Rechtsgrundlagen
| Zweck | Daten | Rechtsgrundlage |
|---|---|---|
| Bestellung annehmen, bestätigen, liefern, Rückfragen | 3 a, b, d | Art. 6 Abs. 1 lit. b DSGVO (Vertrag/vorvertragliche Maßnahmen) |
| Benachrichtigung des Verkäufers/Lieferpersonals über neue Bestellungen (Telegram) | 3 a, b | Art. 6 Abs. 1 lit. b DSGVO |
| Bonusprogramm, Wiedererkennung als Stammkunde | 3 a, c | Art. 6 Abs. 1 lit. b DSGVO (Teilnahmebedingungen) |
| Bezahlung (bar bei Lieferung; online über Stripe, falls angeboten) | 3 b, f | Art. 6 Abs. 1 lit. b DSGVO |
| Erinnerung an eine nicht abgeschlossene Bestellung im Bot [nur falls aktiv] | 3 a, b | Art. 6 Abs. 1 lit. f DSGVO (berechtigtes Interesse an Kundenbetreuung) — Widerspruch jederzeit möglich |
| Interne Verkaufsauswertung, Bestandsplanung, KI-gestützte Auswertung für den Inhaber (Abschnitt 6.e) | Bestell- und Verkaufsdaten | Art. 6 Abs. 1 lit. f DSGVO (berechtigtes Interesse an wirtschaftlicher Betriebsführung) |
| Bereitstellung und Sicherheit der Mini App | IP, technische Daten | Art. 6 Abs. 1 lit. f DSGVO; localStorage: § 25 Abs. 2 Nr. 2 TDDDG (unbedingt erforderlich für den gewünschten Dienst) |
| Aufbewahrung nach Handels- und Steuerrecht | Rechnungs-/Bestelldaten | Art. 6 Abs. 1 lit. c DSGVO i. V. m. § 147 AO, § 257 HGB [prüfen] |

Die Angabe von Telefonnummer und Lieferanschrift ist für eine Lieferung erforderlich; ohne diese Angaben können wir nicht liefern. Eine automatisierte Entscheidungsfindung einschließlich Profiling im Sinne von Art. 22 DSGVO findet nicht statt.

## 5. Speicherort
Kundendaten (3 a–c) werden in einem Make Data Store (Region EU, „eu1“) gespeichert. Bestellbenachrichtigungen werden zusätzlich als Nachrichten in einem Telegram-Chat des Verkäufers gespeichert.

## 6. Empfänger und Auftragsverarbeiter
Ihre Daten erhalten nur Personen bzw. Dienstleister, die sie für die genannten Zwecke benötigen (Inhaber, ggf. Lieferpersonal [anpassen]). Wir setzen folgende Dienstleister ein:

**a) Telegram** — Messenger, über den der Bot und die Mini App laufen; Benachrichtigungen an den Verkäufer. Anbieter: [Telegram-Anbieter laut aktueller Telegram-Datenschutzerklärung eintragen]. Telegram verarbeitet Ihre Daten auch in eigener Verantwortung nach seinen Bedingungen: https://telegram.org/privacy. Die Mini App lädt außerdem ein Skript von telegram.org (dabei wird Ihre IP-Adresse übermittelt). Drittlandübermittlung möglich — **prüfen**.

**b) Make (Celonis)** — Automatisierungsplattform, Verarbeitung der Bot-Nachrichten und Speicherung im Data Store, Server-Region EU (eu1). Anbieter: [Anbieterangaben laut Make-DPA eintragen]. **AVV/DPA prüfen.** Unterauftragsverarbeiter/Drittlandbezug laut DPA **prüfen**.

**c) GitHub Pages** — Hosting der Mini App. Anbieter: GitHub, Inc., USA [prüfen]. GitHub verarbeitet beim Aufruf technisch Ihre IP-Adresse (Server-Logfiles). Drittlandübermittlung (USA) — Rechtsgrundlage, z. B. EU-US Data Privacy Framework oder Standardvertragsklauseln, **prüfen**. **AVV/DPA prüfen.**

**d) Stripe** — nur bei Online-Zahlung, falls angeboten. Anbieter: [z. B. Stripe Payments Europe, Ltd., Irland — prüfen]. Stripe ist für die Zahlungsabwicklung teilweise eigener Verantwortlicher; Datenschutzhinweise: https://stripe.com/de/privacy. **AVV/DPA prüfen.**

**e) Anthropic (Claude)** — KI-Assistent, der für den Inhaber Verkaufsdaten auswertet (z. B. Umsätze, beliebte Produkte); Aufruf über Make. Anbieter: [Anthropic-Vertragspartner laut DPA eintragen — prüfen]. Übermittelt werden [nur zusammengefasste Bestell-/Verkaufsdaten ohne Namen und Telefonnummern — **vor Veröffentlichung im Make-Szenario prüfen und Text anpassen**]. Drittlandübermittlung (USA) — Rechtsgrundlage **prüfen**. **AVV/DPA prüfen.**

**f) Google Maps** — der Verkäufer/Fahrer kann die Lieferanschrift zur Routenplanung in Google Maps öffnen; dabei wird die Anschrift an Google übermittelt. [prüfen, ob beibehalten; Anbieter: Google Ireland Ltd. — prüfen]

Eine Weitergabe an sonstige Dritte erfolgt nur, wenn wir gesetzlich dazu verpflichtet sind.

## 7. Speicherdauer
- Kundenprofil und Bonusdaten (3 a, c): [Frist eintragen, z. B. bis Löschwunsch bzw. X Monate nach der letzten Bestellung].
- Bestell- und Lieferdaten: [Frist eintragen]; steuer- und handelsrechtlich relevante Unterlagen bis zu 6 bzw. 10 Jahre [prüfen].
- Bestellbenachrichtigungen im Telegram-Chat des Verkäufers: [Frist eintragen / regelmäßige Löschung festlegen].
- Protokolle der Make-Ausführungen: [laut Make-Einstellung/Tarif eintragen].
- Server-Logfiles von GitHub Pages: nach den Fristen von GitHub [prüfen].
- localStorage in der Mini App: bis Sie den Speicher in Telegram/Browser löschen.

## 8. Ihre Rechte
Sie haben das Recht auf:
- Auskunft (Art. 15 DSGVO),
- Berichtigung (Art. 16 DSGVO),
- Löschung (Art. 17 DSGVO),
- Einschränkung der Verarbeitung (Art. 18 DSGVO),
- Datenübertragbarkeit (Art. 20 DSGVO).

Wenden Sie sich dazu an [E-Mail] oder schreiben Sie dem Bot [Befehl/Weg eintragen, z. B. „/privacy“].

## 9. Widerspruchsrecht (Art. 21 DSGVO)
**Soweit wir Daten auf Grundlage von Art. 6 Abs. 1 lit. f DSGVO verarbeiten, können Sie aus Gründen, die sich aus Ihrer besonderen Situation ergeben, jederzeit widersprechen. Wir verarbeiten die Daten dann nicht mehr, es sei denn, wir können zwingende schutzwürdige Gründe nachweisen. Einer Verarbeitung zu Zwecken der Direktwerbung (z. B. Erinnerungs- oder Angebotsnachrichten) können Sie jederzeit ohne Angabe von Gründen widersprechen.** Ein formloser Hinweis an [E-Mail] oder im Bot genügt.

## 10. Beschwerderecht
Sie haben das Recht, sich bei einer Datenschutz-Aufsichtsbehörde zu beschweren (Art. 77 DSGVO), insbesondere in dem Bundesland Ihres Aufenthalts oder unseres Sitzes. Zuständig für uns: [Landesdatenschutzbehörde des Bundeslandes des Verantwortlichen eintragen, mit Anschrift/Website].

## 11. Datensicherheit
Die Übertragung erfolgt verschlüsselt (HTTPS/TLS). Zugriff auf Kundendaten haben nur berechtigte Personen. [Weitere Maßnahmen ergänzen, z. B. Zwei-Faktor-Anmeldung bei Make/Telegram.]

## 12. Änderungen
Wir passen diese Datenschutzerklärung an, wenn sich der Bot oder die Rechtslage ändert. Es gilt die jeweils im Bot/in der Mini App verlinkte Fassung.
