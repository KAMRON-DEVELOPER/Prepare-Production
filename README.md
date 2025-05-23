# **General Layout**

- [ Manager Node ]
    - ├─ Traefik (Ingress)
    - ├─ Grafana (Dashboard)
    - ├─ Prometheus (Metrics DB)
    - └─ Loki (Logs DB)

- [ Worker Nodes ]
    - ├─ Your app containers
    - ├─ node-exporter
    - ├─ cAdvisor
    - ├─ promtail

# **Init Docker Swarm**

`docker swarm init --advertise-addr manager_node_public_ip # change the ip here with your machine ip`
**Get token again**
`docker swarm join-token worker`

**Adding worker nodes**
`docker swarm join --token manager_node_public_ip`

# **Create a traefik network**

`docker network create --driver=overlay --attachable traefik-public`
**or**
`docker network create -d overlay traefik-public`

# **Don't forget to run this**

`chmod 600 /mnt/data/traefik/acme.json`

# **Then hash password for traefik admin UI**

`echo $(htpasswd -nB kamronbek) | docker secret create traefik_auth -`

# **Create a volume for Portainer**

`docker volume create portainer_data`

## -------------------------------------------------------------------------------

## **docker node ls**

## **docker service create --replicas 2 -p 80:80 nginx**

## **docker service rm ID**

## **docker stack deploy -c docker-compose.yml medium**

## -------------------------------------------------------------------------------

## **Backend**

`echo "postgresql+asyncpg://kamronbek:kamronbek2003@<postgres_vps_ip>:5432/<postgres_db>" | docker secret create db_url -`
`echo "redis://default:<redis_password>@<redis_vps_ip>:6379" | docker secret create redis_url -`

## **Monitoring**

`echo "kamronbek2003" | docker secret create gf_security_admin_password -`

## **Redis and Postgres VPS**

`echo "kamronbek" | docker secret create postgres_user -`
`echo "dev_db" | docker secret create postgres_db -`
`echo "kamronbek2003" | docker secret create redis_password -`

## **Traefik admin UI**

`echo "kamronbek" | docker secret create traefik_username -`
`echo "kamronbek2003" | docker secret create traefik_password -`

## `docker stack deploy -c <traefik-compose> traefik-stack`

## `docker stack deploy -c <traefik-compose> backend-stack`


