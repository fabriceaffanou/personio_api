# Personio API – Sync Microservice

Microservice zum Abruf und zur Normalisierung von Personio-Personendaten über die [Personio API v2](https://developer.personio.de/). Stellt eine FastAPI-Anwendung bereit, die per HTTP Basic Auth authentifiziert wird und eine Liste **SyncPerson** (angereicherte Personen inkl. Employments, Cost Centers, Legal Entities, Workplaces) zurückgibt.

---

## Übersicht

- **Zweck:** Personio als zentrale HR-Datenquelle anbinden; Personen inkl. Employments, Kostenstellen, Rechtsträger und Standorte in einem einheitlichen Modell (**SyncPerson**) bereitstellen.
- **Stack:** Python 3.12+, FastAPI, httpx (OAuth2 Client Credentials, Retries), Marshmallow für Deserialisierung.
- **Struktur:** Klare Trennung in **PersonioClient** (API-Client, OAuth, Paginierung), **PersonioSyncService** (Mapping Person → SyncPerson) und **main.py** (HTTP-API).

---

## Projektstruktur

```
personio_api/
├── main.py                    # FastAPI-App, Endpoints, HTTP Basic Auth
├── requirements.txt
├── README.md
└── src/
    ├── PersonioClient/        # Personio API v2 Client
    │   ├── i_personio_client.py    # Interface (get_persons, get_employments, …)
    │   ├── factory.py             # create_personio_client(client_id, client_secret, base_url?)
    │   ├── _personio_client.py    # Implementierung: httpx, Paginierung, Caching
    │   ├── _oauth_authenticator.py # OAuth2 Client Credentials (Bearer Token)
    │   └── Data/                   # API-Modelle (Person, Employment, LegalEntity, …)
    │
    └── PersonioSyncService/     # Mapping zu Sync-Modellen
        ├── i_personio_sync_service.py
        ├── factory.py              # create_personio_sync_service(personio_client)
        ├── personio_sync_service.py # get_sync_persons(): Person[] → SyncPerson[]
        ├── person_mapper.py        # build_sync_person (Person → SyncPerson)
        ├── employment_mapper.py   # build_sync_employment (Employment → SyncEmployment)
        ├── org_units_mapper.py    # Department/Team Lookup
        ├── legal_entity_mapper.py
        ├── cost_center_mapper.py
        ├── custom_serializer.py   # to_dict() für JSON-Response (Enum, datetime, nested)
        └── Data/                  # SyncPerson, SyncEmployment, SyncCostCenter
```

---

## Architektur

- **PersonioClient** kapselt die Personio API v2: OAuth2 (Client Credentials), Paginierung, Caching für Department/Team, Retries. Implementierung hinter `IPersonioClient`; Erzeugung nur über `create_personio_client(...)`.
- **PersonioSyncService** nutzt ausschließlich `IPersonioClient`. Er holt Personen, Cost Centers, Legal Entities, Workplaces einmal, mappt jede Person inkl. Employments zu **SyncPerson** (mit aufgelösten Referenzen: Legal Entity, Office, Org Units, Cost Centers). Keine Änderung an Personio-Daten.
- **main.py** erstellt pro Request einen neuen Client und Sync-Service (Credentials aus HTTP Basic Auth), ruft `get_sync_persons()` auf und serialisiert das Ergebnis mit `custom_serializer.to_dict()` zu JSON.

Optionaler **root_path** (z. B. `/microservice/personio`) ist für Reverse-Proxy-Setups vorgesehen.

---

## API

- **Base URL (lokal):** `http://localhost:8007` (oder konfigurierter Host/Port).  
  Mit `root_path`: z. B. `https://<host>/microservice/personio`.

| Methode | Pfad            | Auth        | Beschreibung |
|--------|------------------|------------|--------------|
| GET    | `/sync-persons`  | HTTP Basic | Liefert Liste aller SyncPerson (JSON). |
| GET    | `/health`        | –          | Health-Check, z. B. für Load Balancer. |

**Authentifizierung `/sync-persons`:**  
HTTP Basic Auth; **Username** = Personio `client_id`, **Password** = Personio `client_secret`.  
Beispiel:

```bash
curl -u "CLIENT_ID:CLIENT_SECRET" "http://localhost:8007/sync-persons"
```

**Response:** Array von Objekten vom Typ SyncPerson (inkl. `employments`, Cost Centers, Legal Entity, Office, Org Units etc.), serialisiert über `to_dict()` (datetime als ISO, Enums als Wert).

---

## Laufzeit & Konfiguration

- **Python:** 3.12+ empfohlen.
- **Abhängigkeiten:** `pip install -r requirements.txt`
- **Starten (Beispiel):**

  ```bash
  uvicorn main:app --reload --port 8007 --host 0.0.0.0
  ```

  Mit `root_path` (z. B. hinter Reverse-Proxy):

  ```bash
  uvicorn main:app --reload --port 8007 --host 0.0.0.0 --root-path /microservice/personio
  ```

- **Umgebung:** Keine Pflicht-Umgebungsvariablen; Credentials kommen pro Request aus HTTP Basic. Personio Base URL ist im Client default `https://api.personio.de/v2`, ggf. über `create_personio_client(..., base_url=...)` anpassbar (derzeit nur intern; Erweiterung z. B. per Query/Header denkbar).

---

## Design-Entscheidungen (Kurz)

- **Credentials pro Request:** Keine serverseitige Speicherung; jeder Aufruf nutzt die mitgelieferten Personio-Credentials (client_id/client_secret als HTTP Basic). Gut für Multi-Mandanten oder verschiedene Personio-Instanzen.
- **Sync-Modelle (SyncPerson, SyncEmployment, …):** Eigenes Modell statt Roh-API-Response, um z. B. Cost Centers, Legal Entity, Office, Org Units aufgelöst und typisiert zu liefern; API-Änderungen können im Client/Sync-Layer abgefangen werden.
- **Optional-Felder:** Felder wie `employment.office` oder `legal_entity` sind optional; Mapper prüfen auf `None`, um Fehler wie `'NoneType' object has no attribute 'id'` zu vermeiden.
- **Serialisierung:** `custom_serializer.to_dict()` für einheitliche JSON-Ausgabe (Enums, datetime, verschachtelte Objekte) ohne Pydantic-Modelle in der Response.

---

## Erweiterungsideen

- **Caching:** SyncPerson-Ergebnis oder Personio-Rohdaten pro Credentials/Mandant cachen (TTL, invalidation).
- **Filtering:** Query-Parameter für Status, Legal Entity, Standort etc., Filterung in `get_sync_persons()` oder nachgelagert.
- **Pagination:** Bei vielen Personen paginierte Response (z. B. limit/offset oder cursor).
- **Strukturierte Fehler:** Personio-Fehler (4xx/5xx) in ein einheitliches Fehlerformat mappen und ggf. Statuscode weitergeben.
- **Tests:** Unit-Tests für Mapper (inkl. `office=None`, fehlende Legal Entity), Integrationstests für Client (Mock) und für `GET /sync-persons` (Test-Credentials/Mock-Personio).

---

## Lizenz / Hinweise

Projekt-intern. Personio API Nutzung gemäß [Personio Developer](https://developer.personio.de/) und den geltenden Vertragsbedingungen.
