
# A2 – Advance Containers – QuoteVault

> **Assignment 2 - Full Stack App with Docker Compose**  
> Author: Jithin Jyothi  
> Course: PROG8850 – Advanced Containers   
> Repo: [A2-Advance-Containers-QuoteVault](https://github.com/JithinJyothi95/A2-Advance-Containers-QuoteVault)

---

## Project Summary

QuoteVault is a full-stack motivational quote app containerized using Docker Compose. It consists of:
- A React frontend for submitting and displaying quotes.
- A Flask backend API to handle CRUD operations.
- A PostgreSQL database to store the quotes.
- An NGINX reverse proxy to route requests.

All services are run in containers using Docker Compose and communicate over an internal Docker network.

---
## Folder Structure

```
.
├── backend/
│   ├── app.py
│   ├── requirements.txt
│   └── Dockerfile
├── frontend/
│   ├── src/App.js
│   └── Dockerfile
├── db/
│   └── init.sql
├── nginx/
│   └── default.conf
├── docker-compose.yml
└── README.md
```

## Tech Stack

| Layer        | Technology         |
|--------------|--------------------|
| Frontend     | React              |
| Backend      | Flask (Python)     |
| Database     | PostgreSQL         |
| Reverse Proxy| NGINX              |
| Orchestration| Docker Compose     |

---

##  Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/JithinJyothi95/A2-Advance-Containers-QuoteVault.git
cd A2-Advance-Containers-QuoteVault
```

## Setup & Deployment
- Install frontend dependencies:
```bash
cd frontend
npm install
cd ..
```
- Create a .env file in the root directory (same level as docker-compose.yml) with the following content:
```
DB_NAME=quotevault
DB_USER=devtedsuser
DB_PASSWORD=devtedspass
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
```

# Step 1: Clean build and run
docker compose down -v
docker compose build --no-cache
docker compose up -d

## Step 2: Access the app in browser (GitHub Codespaces)
- Click the "PORTS" tab and open forwarded port 3000
```
https://<your-codespace-id>-3000.app.github.dev
```
---

## Database Verification

To confirm the PostgreSQL container and `quotes` table are working correctly:

```bash
docker exec -it <db-container-id> psql -U postgres -d quotevault
```

Inside the DB shell:

```sql
\dt
SELECT * FROM quotes;
```

_Expected output: quotes table with 3 seeded quotes from `init.sql`._

---


## Docker Compose Services

| Service   | Description                      | Port |
|-----------|----------------------------------|------|
| frontend  | React app (served via NGINX)     | 3000 |
| backend   | Flask API(proxied via frontend)  | 5000 |
| db        | PostgreSQL + quotevault DB       | 5432 |
| nginx     | Reverse proxy for API/frontend   | 80   |


## API Endpoints

| Method | Endpoint           | Description                 |
|--------|--------------------|-----------------------------|
| GET    | `/api/quotes`      | Retrieve all quotes         |
| POST   | `/api/quotes`      | Add a new quote (JSON body) |
| DELETE   | `/api/quotes/:id`    | Delete a quote by its id |

Sample `POST` body:
```json
{ "quote": "Believe in yourself - Jithin" }
```
Sample `DELETE`:
DELETE /api/quotes/6
---

## Sample Outputs

> Available in submitted screenshots (.docx/.pdf) and screenshots folder
- Docker containers (`docker ps`)
- Database query (`SELECT * FROM quotes;`)
- API output (`/api/quotes`)
- POST API using browser console
- React UI preview

## Security Best Practices

- All containers use minimal images (e.g., `python:slim`, `node:alpine`).
- Backend runs as a **non-root user** (`appuser`).
- Secrets are passed using environment variables only (not hardcoded).
- PostgreSQL access limited to backend container via Docker network.
- Volumes used for persistent DB storage.

---

##  Load Balancing

The backend service is scaled using Docker Compose:

```yaml
deploy:
  replicas: 2
```

If using Docker Swarm or NGINX with `upstream` config, load balancing will distribute traffic between containers.

---

## Use Case Diagram

![Use Case](screenshots/Use%20case%20diagram.png)

---

## Conclusion

- [x] Working containerized full-stack quote app
- [x] PostgreSQL DB with seed data and volumes
- [x] Docker Compose orchestration
- [x] Security best practices (non-root, minimal images)
- [x] API tested (GET, POST, DELETE)
- [x] Database tested (via psql)
- [x] Screenshots and documentation
- [x] UML Architecture diagram

---


