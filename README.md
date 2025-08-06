# Coolify FastAPI Postgres Demo

A minimal async FastAPI CRUD API using an **external Postgres** instance, ready for container deployment (Coolify).

## Quick Start

```bash
git clone <repo-url>
cd coolify-fastapi-demo
docker-compose up --build
```

**API available at:** `http://localhost:8000/docs`

## Endpoints

- `POST   /items` - Create item
- `GET    /items` - List all items
- `GET    /items/{item_id}` - Get item by id
- `PATCH  /items/{item_id}` - Update item
- `DELETE /items/{item_id}` - Delete item

## Environment

All settings can be controlled via the `DATABASE_URL` env variable. Provided for local/external use.

---

## Coolify Deploy

- Push to your repo
- Add to Coolify as a Docker Compose project

---
