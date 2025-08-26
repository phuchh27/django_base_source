python -c "import secrets; print(secrets.token_urlsafe())"

docker
```
  docker compose -f local.yml down
  docker compose -f local.yml up --build -d --remove-orphans 

```

backup
```
  docker compose -f local.yml exec postgres backup   
```