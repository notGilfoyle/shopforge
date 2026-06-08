# ShopForge

A full-stack learning project that applies database concepts using a realistic e-commerce domain.

## Purpose

ShopForge exists to explore **when and why** you reach for different database technologies.
It is not production software — it is a learning sandbox.

---

## Architecture

```
shopforge/
├── backend/          # FastAPI (Python) — REST API and database logic
├── frontend/         # React — UI that consumes the API
└── docker-compose.yml
```

### Why two databases?

| Database       | Used for                                  | Why it fits                                                                 |
|----------------|-------------------------------------------|-----------------------------------------------------------------------------|
| **PostgreSQL** | Users, orders, order items, payments, inventory | Data is relational and transactional. You need JOINs, foreign keys, and ACID guarantees (e.g., decrement inventory *and* record the order atomically). |
| **MongoDB**    | Product catalog, product reviews          | Products have wildly different attributes (a book has an ISBN, a TV has screen size). MongoDB's flexible documents handle this without dozens of nullable columns. Reviews are also naturally document-shaped. |

### Tech stack

| Layer      | Technology | Notes                                      |
|------------|------------|--------------------------------------------|
| Backend    | FastAPI     | Modern async Python, automatic API docs at `/docs` |
| Python deps| uv          | Fast dependency management, replaces pip/poetry |
| Frontend   | React       | Vite-based, talks to the FastAPI backend   |
| SQL DB     | PostgreSQL 16 | Runs locally via Docker                  |
| NoSQL DB   | MongoDB 7   | Runs locally via Docker                   |

---

## Getting started

### Prerequisites
- [Docker Desktop](https://www.docker.com/products/docker-desktop/) (or Docker + Docker Compose)
- [uv](https://docs.astral.sh/uv/) for Python
- [Node.js](https://nodejs.org/) (v20+) for the frontend

### 1. Start the databases

```bash
docker compose up -d
```

This starts PostgreSQL on `localhost:5432` and MongoDB on `localhost:27017`.
Both use the credentials `shopforge / shopforge_pass` (local dev only).

Check that they're running:

```bash
docker compose ps
```

### 2. Backend (coming in Phase 1)

```bash
cd backend
uv sync
uv run fastapi dev main.py
```

### 3. Frontend (coming in Phase 1)

```bash
cd frontend
npm install
npm run dev
```

---

## Database connection strings (local)

```
PostgreSQL:  postgresql://shopforge:shopforge_pass@localhost:5433/shopforge
MongoDB:     mongodb://shopforge:shopforge_pass@localhost:27018/shopforge?authSource=admin
```

---

## Phases

- [x] **Phase 0** — Repo structure, Docker Compose for local databases
- [ ] **Phase 1** — Backend skeleton: FastAPI app, DB connections, health check
- [ ] **Phase 2** — PostgreSQL: user and order models, migrations with Alembic
- [ ] **Phase 3** — MongoDB: product catalog and review documents
- [ ] **Phase 4** — Full CRUD API for orders and catalog
- [ ] **Phase 5** — React frontend connecting to the API
- [ ] **Phase 6** — Advanced queries: aggregations, transactions, indexes
