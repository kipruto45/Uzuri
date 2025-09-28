# Uzuri University Production Deployment Checklist

## 1. Pre-Deployment
- [ ] All code committed and pushed to main branch
- [ ] All migrations created and tested
- [ ] All tests pass (unit, integration, API)
- [ ] Static and media files collected
- [ ] Environment variables set for all secrets/credentials
- [ ] DEBUG = False in settings
- [ ] ALLOWED_HOSTS set to production domains
- [ ] SECRET_KEY is strong and secret

## 2. Server Setup
- [ ] Ubuntu 22.04 LTS (or similar) server provisioned
- [ ] System updated (`sudo apt update && sudo apt upgrade`)
- [ ] Python 3.10+ and pip installed
- [ ] PostgreSQL and Redis installed and secured
- [ ] Nginx installed for reverse proxy/static/media
- [ ] Certbot/Let's Encrypt for HTTPS

## 3. Application Setup
- [ ] Python virtualenv created and activated
- [ ] All requirements installed (`pip install -r requirements.txt`)
- [ ] Database configured and migrated (`python manage.py migrate`)
- [ ] Superuser created (`python manage.py createsuperuser`)
- [ ] Static files collected (`python manage.py collectstatic`)
- [ ] Media directory permissions set

## 4. Services
- [ ] Gunicorn/uvicorn configured as systemd service
- [ ] Celery worker and beat configured as systemd services
- [ ] Nginx configured for domain, static, media, proxy to Gunicorn/uvicorn
- [ ] HTTPS enabled and tested

## 5. Monitoring & Backups
- [ ] Sentry or error monitoring enabled
- [ ] Log rotation configured
- [ ] Automated database and media backups scheduled
- [ ] Health checks and uptime monitoring enabled

## 6. Security
- [ ] All secrets in environment variables
- [ ] Secure cookies, HSTS, CSRF, CORS enabled
- [ ] SSH keys for server access, password login disabled
- [ ] Firewall enabled (ufw)
- [ ] Regular dependency updates scheduled

## 7. Go Live
- [ ] Final smoke test on production
- [ ] Announce launch to users
- [ ] Monitor logs and metrics closely for first 48 hours

---

# Example Gunicorn systemd Service
```
[Unit]
Description=gunicorn daemon
After=network.target

[Service]
User=ubuntu
Group=www-data
WorkingDirectory=/path/to/backend
ExecStart=/path/to/venv/bin/gunicorn --workers 4 --bind unix:/path/to/backend/gunicorn.sock uzuri_university.wsgi:application

[Install]
WantedBy=multi-user.target
```

# Example Celery systemd Service
```
[Unit]
Description=Celery Service
After=network.target

[Service]
User=ubuntu
Group=www-data
WorkingDirectory=/path/to/backend
ExecStart=/path/to/venv/bin/celery -A uzuri_university worker --loglevel=info

[Install]
WantedBy=multi-user.target
```

# Example Nginx Config Snippet
```
server {
    listen 80;
    server_name yourdomain.com www.yourdomain.com;
    location = /favicon.ico { access_log off; log_not_found off; }
    location /static/ { root /path/to/backend; }
    location /media/ { root /path/to/backend; }
    location / {
        include proxy_params;
        proxy_pass http://unix:/path/to/backend/gunicorn.sock;
    }
}
```

---

**Replace all /path/to/backend and domain placeholders with your actual values.**
