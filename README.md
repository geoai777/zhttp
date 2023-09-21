# zhttp
Fast and simple app to get /sys server information. Could be used as Docker container.

# Installation
As simple as that
```bash
# git clone https://github.com/p0rc0jet/zhttp.git
# cd zhttp
# docker build --tag zhttp .
```

# Deployment
I prefer docker-compose. Put this into `docker-compose.yml`
```yaml
version: '3.5'

services:
  zhttp:
    image: p0rc0r0ss0/zhttp
    container_name: zhttp
    restart: unless-stopped
    environment:
      TZ: "<your time zone here>"
    volumes:
      - /sys:/sys:ro
    network_mode: host
```
and then
```bash
docker compose up -d
```

# Usage
Navigate to `http://<your_boar_ip>:8080/`
