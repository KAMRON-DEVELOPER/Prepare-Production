# 🐳 Docker Swarm Deployment Guide for Kronk

## 🗂️ General Layout

### [ Manager Node ]

- Traefik (Ingress Controller)
- Grafana (Dashboard)
- Prometheus (Metrics DB)
- Loki (Logs DB)

### [ Worker Nodes ]

- FastAPI App Containers
- node-exporter (System metrics)
- cAdvisor (Container metrics)
- promtail (Log shipping)

---

## 🔧 1. Initialize Docker Swarm

On the **manager node**:

```bash
docker swarm init --advertise-addr <MANAGER_NODE_PUBLIC_IP>
```

Get the worker token:

```bash
docker swarm join-token worker
```

Use the printed command to add worker nodes:

```bash
docker swarm join --token <TOKEN> <MANAGER_NODE_PUBLIC_IP>:2377
```

---

## 🔐 2. Create Secrets (on Manager Node)

```bash
# Database URLs
 echo "postgresql+asyncpg://kamronbek:kamronbek2003@<postgres_vps_ip>:5432/<postgres_db>" | docker secret create db_url -
 echo "redis://default:<redis_password>@<redis_vps_ip>:6379" | docker secret create redis_url -

# Monitoring (Grafana)
 echo "kamronbek2003" | docker secret create gf_security_admin_password -

# Redis/Postgres credentials
 echo "kamronbek" | docker secret create postgres_user -
 echo "dev_db" | docker secret create postgres_db -
 echo "kamronbek2003" | docker secret create redis_password -

# Traefik Admin UI
 echo "kamronbek" | docker secret create traefik_username -
 echo "kamronbek2003" | docker secret create traefik_password -

# Traefik Auth (hashed password)
 echo "$(htpasswd -nB kamronbek)" | docker secret create traefik_auth -
```

---

## 🌐 3. Create Overlay Network

```bash
docker network create --driver=overlay --attachable traefik-public
```

---

## 🔒 4. Set Permissions on ACME File (TLS Certs)

```bash
chmod 600 cluster/swarm/traefik/config/acme.json
```

---

## 📦 5. Deploying Services (From Your Local Machine)

Ensure you are using the right context:

```bash
docker context use dev-kronk
```

### 🛡️ Traefik

```bash
docker stack deploy -c cluster/swarm/traefik/traefik.yml traefik-stack
```

### 🧠 Backend

```bash
docker stack deploy -c cluster/swarm/backend/backend_stack.yml backend-stack
```

### 📊 Monitoring

```bash
docker stack deploy -c cluster/swarm/monitoring/portainer.yml monitoring-stack
```

Add others similarly:

```bash
docker stack deploy -c cluster/swarm/monitoring/grafana.yml monitoring-stack
```

---

## 🧪 6. Useful Commands

- List stacks:
  ```bash
  docker stack ls
  ```

- List services:
  ```bash
  docker service ls
  ```

- Remove a service:
  ```bash
  docker service rm <SERVICE_ID>
  ```

- Check nodes:
  ```bash
  docker node ls
  ```

- Check logs:
  ```bash
  docker service logs <SERVICE_NAME>
  ```

- Run a test service:
  ```bash
  docker service create --replicas 2 -p 80:80 nginx
  ```

---

## 🌍 7. Access Services via Subdomains (Traefik)

Make sure DNS A records point to your **manager node IP**:

- `https://traefik.kronk.uz`
- `https://grafana.kronk.uz`
- `https://prometheus.kronk.uz`
- `https://portainer.kronk.uz`

---

## 🗃️ Project Structure Overview

```plaintext
~/Documents/deployment
├── cluster
│   └── swarm
│       ├── backend
│       │   └── backend_stack.yml
│       ├── monitoring
│       │   ├── alertmanager/
│       │   ├── grafana.yml
│       │   ├── loki/
│       │   ├── prometheus/
│       │   └── promtail.yml
│       └── traefik
│           ├── config/
│           └── traefik.yml
├── pod
│   └── FastAPI source code & Dockerfile
├── service
│   ├── configurations
│   └── docker-compose.yml
└── README.md
```

---

## 🧠 Docker Context Info

```bash
docker context ls
```

Example:

```plaintext
NAME        DESCRIPTION                               DOCKER ENDPOINT               ERROR
default *   Current DOCKER_HOST based configuration   unix:///var/run/docker.sock   
dev-kronk                                             ssh://root@178.212.35.106     
```

Now you’re ready to manage, deploy, and teach Docker Swarm workflows! 🚀
