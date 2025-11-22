# VPS Deployment (Hetzner / DO / Linode)

This guide shows how to run the application on a small VPS with Docker Compose.

## 1. Provision VPS
- Distro: Ubuntu 22.04 LTS (recommended)
- Size: 1–2GB RAM (Hetzner CX11 or similar)
- Add your SSH key when creating the server.

## 2. Initial Server Setup
```bash
sudo apt update
sudo apt install -y ca-certificates curl gnupg
install -m 0755 -d /etc/apt/keyrings
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg
echo "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu $(. /etc/os-release; echo $VERSION_CODENAME) stable" | \
  sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
sudo apt update
sudo apt install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
sudo usermod -aG docker $USER
# Re-login (new shell) so docker group applies
```

Optionally enable automatic security updates:
```bash
sudo apt install -y unattended-upgrades
sudo dpkg-reconfigure --priority=low unattended-upgrades
```

## 3. Clone Repo & Prepare Env
```bash
git clone https://github.com/phil-keita/facturation.git
cd facturation
cp .env.sample .env
# Edit .env: set POSTGRES_PASSWORD and SECRET_KEY
```

Generate a strong SECRET_KEY:
```bash
python -c "import secrets; print(secrets.token_hex(32))"
```

## 4. Bring Services Up
```bash
docker compose pull   # (no effect first time, but habit)
docker compose build
docker compose up -d
```

## 5. Access App
- HTTP: http://YOUR_SERVER_IP:8000 (before Caddy domain setup)
- After domain + Caddy config, just use https://yourdomain.com

## 6. Set Domain & HTTPS (Caddy)
1. Point your domain A record to the VPS public IP.
2. Edit `Caddyfile` and replace `example.com` with your domain.
3. Restart Caddy:
```bash
docker compose restart caddy
```
Caddy issues/renews LetsEncrypt certs automatically.

## 7. Backups
Simple nightly Postgres dump (example):
```bash
mkdir -p /opt/backups
crontab -e
# Add line (runs at 02:00):
0 2 * * * docker exec $(docker ps -qf name=db) pg_dump -U facturation facturation > /opt/backups/facturation-$(date +\%F).sql
```
Consider offsite sync (rclone to object storage) for redundancy.

## 8. Updating App
```bash
git pull
docker compose build
docker compose up -d
```

## 9. Logs & Health
```bash
docker compose logs -f web
```
Healthcheck ensures Postgres readiness before web starts.

## 10. Security Basics
- Disable password SSH login (use keys)
- Keep system patched monthly
- Use strong POSTGRES_PASSWORD & SECRET_KEY
- Optional: Enable UFW firewall
```bash
sudo apt install -y ufw
sudo ufw allow 22
sudo ufw allow 80
sudo ufw allow 443
sudo ufw enable
```

## 11. Restoring From Dump
```bash
docker compose down
rm -rf docker volumes for pgdata if needed
# Bring up fresh db
docker compose up -d db
cat backup.sql | docker exec -i $(docker ps -qf name=db) psql -U facturation facturation
# Start web
docker compose up -d web caddy
```

## 12. Changing Passwords
If you change POSTGRES_PASSWORD in `.env`, also update any existing running containers by recreating them:
```bash
docker compose down
docker compose up -d
```

## 13. Receipts Storage
PDF receipts stored in volume `receipts`. Include this in any offsite backup strategy.

## 14. Troubleshooting
- Web container exits: check `docker compose logs web` for missing deps.
- Permission denied on docker: ensure you re-logged after adding user to docker group.
- SSL not issued: domain DNS may not have propagated or port 80 blocked.

## 15. Scaling Later
- Move Postgres to managed (Neon/RDS) by swapping `DATABASE_URL`.
- Add monitoring (Prometheus + Grafana) if needed.

---
Minimal stack ready for 3-user usage with low maintenance.
