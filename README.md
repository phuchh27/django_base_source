python -c "import secrets; print(secrets.token_urlsafe())"

docker

```
  docker compose -f local.yml down
  docker compose -f local.yml up --build -d --remove-orphans

```

backup

```
  docker compose -f local.yml exec postgres backup

  CREATE ROLE backup_admin WITH LOGIN PASSWORD 'backup123';
  GRANT CONNECT ON DATABASE "authors-live" TO backup_admin;
  GRANT USAGE ON SCHEMA public TO backup_admin;
  GRANT SELECT ON ALL TABLES IN SCHEMA public TO backup_admin;
  GRANT SELECT ON ALL SEQUENCES IN SCHEMA public TO backup_admin;
```
