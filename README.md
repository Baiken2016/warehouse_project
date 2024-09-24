# warehouse_project
1. Create env var

```bash
touch .env
```
Past env vars
SQLALCHEMY_DATABASE_URL="postgresql+asyncpg://postgres:postgres@database:5432/warehouse_db"

2. Run command 
```bash
docker-compose -up --build
```

3. App works on 127.0.0.1:8000